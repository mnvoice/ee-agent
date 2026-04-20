"""Agent 5: Vision Solver — reads PDF page images to solve questions
that pdfplumber cannot extract (inline formula images, diagrams).

Triggered only when needs_vision() returns True. Falls back gracefully
to text-only solver when Vision API is unavailable.
"""
from __future__ import annotations

import base64
import json
import logging
import re

from ee_agent.agents.base import AgentInput, AgentOutput, BaseAgent

logger = logging.getLogger(__name__)

VISION_SOLVE_PROMPT = """이 이미지는 전기기사 필기 기출문제 PDF의 한 페이지입니다.

문제 번호 {q_no}번을 찾아서:
1. 문제 전체 텍스트(stem)를 수식 포함해서 읽어주세요
2. 4개 선지(①②③④)를 모두 읽어주세요
3. 문제를 풀고 정답 번호를 골라주세요

수식 표현 규칙:
- 분수: (a+b)/(c+d), 전달함수: G(s)=K/[s(s+1)(s+4)]
- 행렬: [[a,b],[c,d]], 라플라스: F(s)=(s+1)/((s+2)²+4)
- z변환: F(z)=z/(z-e^(-aT)), 그리스: ω, ζ, ε, μ, λ, δ
- 벡터: (ax̂ + bŷ) 형태

반드시 아래 JSON 형식으로만 응답 (다른 텍스트 금지):
{{
  "stem": "문제 전체 텍스트 (수식 포함)",
  "choices": {{
    "1": "선지1",
    "2": "선지2",
    "3": "선지3",
    "4": "선지4"
  }},
  "selected_choice": 정답번호,
  "law_used": "사용한 공식/법칙",
  "final_answer": "계산 결과값"
}}"""


CONF_VISION_SOLVE = 0.70


def needs_vision(question) -> bool:
    """Detect questions that pdfplumber could not fully extract.

    Returns True when the solver needs a page image to answer.
    """
    stem = question.stem or ""
    choices = question.choices or []

    # 1. Stem extremely short — tiered detection
    #    <15 chars: definitely broken (e.g., "는?" 2자) → always True
    #    15~50 chars: broken only if choices are ALSO incomplete
    placeholder = "[formula - OCR required]"
    if len(stem) < 15:
        return True
    if len(stem) < 50:
        broken_choices = sum(
            1 for c in choices
            if c.text in (placeholder, "[diagram]") or not c.text.strip()
        )
        if broken_choices >= 2:
            return True

    # 2. needs_ocr flag still set
    if getattr(question, "needs_ocr", False):
        return True

    # 3. Placeholder or [diagram] in choices
    placeholder = "[formula - OCR required]"
    if any(c.text == placeholder or c.text == "[diagram]" for c in choices):
        return True

    # 4. Stem references an inline formula that was an image and is now missing.
    #    Pattern: "전달함수가 [gap] 과 같이" — connective word after keyword
    #    but no actual formula (no "=") between them.
    #    vs. concept question: "전달함수는?" — asks WHAT the TF is, no gap.
    inline_gap_patterns = [
        r"전달함수가?\s+과\s+같",    # "전달함수가 과 같이" (formula image was here)
        r"전달함수에\s+대한",         # "전달함수에 대한" (formula image before this)
        r"상태방정식으로\s+표현",      # state equation was image
    ]
    for pat in inline_gap_patterns:
        if re.search(pat, stem):
            return True

    # 5. Stem references diagram/block but choices are all [diagram]
    diagram_refs = ["신호흐름", "블록선도", "그림"]
    has_diagram_ref = any(r in stem for r in diagram_refs)
    all_diagram_choices = all(
        c.text in ("[diagram]", "[formula - OCR required]") for c in choices
    )
    if has_diagram_ref and all_diagram_choices:
        return True

    return False


class VisionSolver(BaseAgent):
    """Solves questions by reading PDF page images via Vision API.

    When Vision API is unavailable, returns a graceful fallback
    with confidence 0.10.
    """

    def __init__(self, llm=None, config: dict | None = None):
        super().__init__(config)
        self.llm = llm  # Must support vision (e.g., AnthropicClient)

    @property
    def name(self) -> str:
        return "vision_solver"

    async def run(self, input_data: AgentInput) -> AgentOutput:
        trace: list[str] = []
        q_no = input_data.context.get("question_number", 0)
        page_jpeg = input_data.context.get("page_jpeg")

        if not page_jpeg:
            trace.append("No page image provided — cannot solve via Vision")
            return self._fallback(input_data.question_id, trace)

        if self.llm is None:
            trace.append("Vision LLM not configured — falling back")
            return self._fallback(input_data.question_id, trace)

        trace.append(f"Vision-Solve: reading Q{q_no} from page image")

        try:
            b64 = base64.standard_b64encode(page_jpeg).decode()
            prompt = VISION_SOLVE_PROMPT.format(q_no=q_no)

            response = await self.llm.complete_vision(
                image_b64=b64,
                prompt=prompt,
                max_tokens=2048,
            )
            content = response.content.strip()

            # Strip code fences
            if content.startswith("```"):
                lines = content.splitlines()
                content = "\n".join(l for l in lines if not l.startswith("```"))

            result = json.loads(content)
            choice = result.get("selected_choice")
            if not isinstance(choice, int) or not (1 <= choice <= 4):
                # Try extracting from string
                sc = re.search(r'"selected_choice"\s*:\s*([1-4])', content)
                if sc:
                    result["selected_choice"] = int(sc.group(1))
                else:
                    trace.append(f"Vision returned invalid choice: {choice}")
                    return self._fallback(input_data.question_id, trace)

            result["confidence"] = CONF_VISION_SOLVE
            result["method"] = "vision_solve"
            trace.append(
                f"Vision solved: choice={result['selected_choice']}, "
                f"law={result.get('law_used', '?')[:60]}"
            )
            if result.get("stem"):
                trace.append(f"Recovered stem: {result['stem'][:80]}...")

            return AgentOutput(
                agent_name=self.name,
                question_id=input_data.question_id,
                result=result,
                confidence=CONF_VISION_SOLVE,
                reasoning_trace=trace,
            )

        except json.JSONDecodeError as e:
            trace.append(f"Vision JSON parse error: {e}")
            return self._fallback(input_data.question_id, trace)
        except Exception as e:
            trace.append(f"Vision API error: {e}")
            return self._fallback(input_data.question_id, trace)

    def _fallback(self, question_id: str, trace: list[str]) -> AgentOutput:
        trace.append("Vision fallback: returning empty result")
        return AgentOutput(
            agent_name=self.name,
            question_id=question_id,
            result={
                "selected_choice": None,
                "confidence": 0.10,
                "method": "vision_fallback",
                "stem": "",
                "law_used": "vision_unavailable",
            },
            confidence=0.10,
            reasoning_trace=trace,
        )
