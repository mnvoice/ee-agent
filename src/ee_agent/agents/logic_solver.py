"""Agent 2: Logic First-Principles Solver."""
import asyncio
import json
import logging
import re

from ee_agent.agents.base import AgentInput, AgentOutput, BaseAgent
from ee_agent.agents.prompts.logic_prompts import (
    CALC_PROMPT,
    CONCEPT_PROMPT,
    JIT_REMINDER,
    SYSTEM_PROMPT,
    WRONG_QUESTION_HINT,
)

logger = logging.getLogger(__name__)


class LogicFirstPrinciplesSolver(BaseAgent):
    """
    Agent 2: Logic First-Principles Solver
    Strategy: Schema Exclusion + JIT Reminder

    Schema Exclusion: Answer choices are NOT passed to LLM — prevents memorization.
    JIT Reminder: Inject relevant formulas from RAG just before the calculation prompt.
    """

    def __init__(self, llm_client=None, retriever=None, config: dict | None = None):
        super().__init__(config)
        self.llm = llm_client
        self.retriever = retriever  # GMMDynamicRetriever

    @property
    def name(self) -> str:
        return "logic_solver"

    async def run(self, input_data: AgentInput) -> AgentOutput:
        trace: list[str] = []
        stem = input_data.context.get("stem", "")
        topology = input_data.context.get("topology", {})
        topology_str = topology.get("circuit_type", "unknown") if topology else "unknown"
        raw_choices = input_data.context.get("choices", [])
        choices_text = "\n".join(
            f"{c['index']}. {c['text']}" for c in raw_choices
        ) if raw_choices else "No choices available"

        trace.append("Solver: deriving answer and selecting from choices")

        # JIT Reminder: fetch relevant knowledge from RAG (formulas + regulations + concepts)
        formulas_text = ""
        if self.retriever:
            trace.append("JIT: retrieving relevant formulas from knowledge base")
            # Retrieve all types and merge by relevance score
            all_results = self.retriever.retrieve(stem, max_k=5)
            if all_results:
                formulas_text = "\n".join(
                    f"- {r['metadata']['name']}: {r['metadata'].get('latex', r['metadata'].get('definition', r.get('text', '')[:200]))}"
                    for r in all_results[:3]
                )
                types_found = set(r['metadata'].get('type', '?') for r in all_results[:3])
                trace.append(f"JIT injected {min(len(all_results), 3)} formula(s) (types: {', '.join(types_found)})")
            else:
                trace.append("JIT: no formulas in knowledge base yet")
        else:
            trace.append("JIT: retriever not configured")

        trace.append(f"JIT reminder: {JIT_REMINDER.strip()[:80]}...")

        q_type = self._detect_question_type(stem)
        trace.append(f"Question type: {q_type}")
        inference_result = await self._blind_inference(stem, topology_str, formulas_text, choices_text, trace, q_type)

        return AgentOutput(
            agent_name=self.name,
            question_id=input_data.question_id,
            result=inference_result,
            confidence=inference_result.get("confidence", 0.7),
            reasoning_trace=trace,
        )

    async def _retry_simple(self, stem: str, choices_text: str, trace: list[str]) -> dict:
        """Ultra-simple retry with multiple attempts."""
        if self.llm is None:
            trace.append("Retry skipped: no LLM")
            return {"final_answer": "unknown", "law_used": "unknown", "confidence": 0.2}

        prompts = [
            (
                f"전기기사 시험 문제입니다. 정답 번호만 답하세요.\n\n"
                f"문제: {stem}\n\n보기:\n{choices_text}\n\n"
                f'JSON으로 답하세요: {{"selected_choice": 정답번호}}'
            ),
            (
                f"Pick the correct answer (1, 2, 3, or 4).\n\n"
                f"Q: {stem}\n{choices_text}\n\n"
                f"Answer with ONLY a number (1-4):"
            ),
        ]

        for i, prompt in enumerate(prompts):
            try:
                response = await self.llm.complete(prompt, max_tokens=64)
                content = response.content.strip()
                # Try JSON extraction
                sc = re.search(r'"selected_choice"\s*:\s*([1-4])', content)
                if not sc:
                    sc = re.search(r'["\s]([1-4])["\s,}]', content)
                if not sc:
                    sc = re.search(r'^([1-4])$', content, re.MULTILINE)
                if not sc:
                    sc = re.search(r'\b([1-4])\b', content)
                if sc:
                    choice = int(sc.group(1))
                    trace.append(f"Retry {i+1} succeeded: selected_choice={choice}")
                    return {"final_answer": "unknown", "law_used": "retry", "selected_choice": choice, "confidence": 0.5}
                trace.append(f"Retry {i+1}: no choice found in '{content[:60]}'")
            except Exception as exc:
                trace.append(f"Retry {i+1} failed: {exc}")

        trace.append("Retry failed — defaulting")
        return {"final_answer": "unknown", "law_used": "unknown", "confidence": 0.2}

    @staticmethod
    def _is_wrong_question(stem: str) -> bool:
        """Detect '틀린 것은?' / '옳지 않은 것은?' question type."""
        wrong_cues = ["틀린 것", "옳지 않은", "잘못된 것", "틀린것", "옳지않은"]
        return any(cue in stem for cue in wrong_cues)

    @staticmethod
    def _detect_question_type(stem: str) -> str:
        """Detect if question is calculation-type or concept/regulation-type."""
        import re as _re
        # Calc: has numbers followed by electrical units
        calc_patterns = [
            r"\d+\.?\d*\s*(V|A|Ω|W|kW|Hz|F|H|kΩ|mH|μF|kV|MVA|kVA|Wb|T|N|J|nF|pF|mΩ|MΩ)",
            r"몇\s*(V|A|Ω|W|kW|Hz|F|H|kΩ|mH|μF|배|Wb|T|배|%|m²|cm²)",
            r"\d+\s*[%배]",
        ]
        for p in calc_patterns:
            if _re.search(p, stem):
                return "calc"
        return "concept"

    async def _blind_inference(
        self, stem: str, topology: str, formulas: str, choices: str, trace: list[str],
        q_type: str = "calc",
    ) -> dict:
        """Derive answer and select best matching choice."""
        if self.llm is None:
            trace.append("LLM not configured, using fallback extraction")
            return self._fallback_extract(stem)

        formulas_section = f"\n관련 공식:\n{formulas}\n" if formulas else ""
        if q_type == "concept":
            prompt = CONCEPT_PROMPT.format(stem=stem, formulas_section=formulas_section, choices=choices)
        else:
            prompt = CALC_PROMPT.format(
                stem=stem,
                formulas_section=formulas_section,
                choices=choices,
            )
        max_retries = 3
        last_error = None
        for attempt in range(max_retries):
            try:
                response = await self.llm.complete(prompt, system=SYSTEM_PROMPT, max_tokens=1024)
                break
            except Exception as e:
                last_error = e
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    logger.warning(f"API call failed (attempt {attempt + 1}/{max_retries}): {e}, retrying in {wait}s")
                    trace.append(f"Retry {attempt + 1}: {e}")
                    await asyncio.sleep(wait)
                else:
                    logger.error(f"API call failed after {max_retries} retries: {e}")
                    trace.append(f"Solver error after {max_retries} retries: {e}")
                    return {"final_answer": "unknown", "law_used": "unknown", "question_type": q_type, "confidence": 0.2}
        try:
            content = response.content.strip()
            if not content:
                logger.warning("Empty LLM response received")
                return {"final_answer": "unknown", "law_used": "unknown", "confidence": 0.2}
            logger.debug(f"Raw LLM response ({len(content)} chars): {content[:300]!r}")
            # Strip markdown code fences if present
            json_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", content)
            if json_match:
                content = json_match.group(1).strip()
            # Try to find JSON object if no code fences
            elif not content.startswith("{"):
                obj_match = re.search(r"\{[\s\S]*\}", content)
                if obj_match:
                    content = obj_match.group(0)
            # Fix lone backslashes (e.g. \Omega, \mu) that are invalid in JSON
            content_fixed = re.sub(r'\\(?!["\\/bfnrtu0-9])', r'\\\\', content)
            try:
                result = json.loads(content_fixed)
            except json.JSONDecodeError:
                result = json.loads(content)
            trace.append(
                f"Derived: {result.get('final_answer')} {result.get('unit', '')} "
                f"via {result.get('law_used', 'unknown')}"
            )
            result["confidence"] = 0.8
            return result
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parse error: {e}")
            # Partial extraction: grab final_answer field even if full JSON is broken
            fa_match = re.search(r'"final_answer"\s*:\s*"([^"]*)"', content)
            law_match = re.search(r'"law_used"\s*:\s*"([^"]*)"', content)
            sc_match = re.search(r'"selected_choice"\s*:\s*([1-4])', content)
            if fa_match or sc_match:
                fa_val = fa_match.group(1) if fa_match else "unknown"
                sc_val = int(sc_match.group(1)) if sc_match else None
                # final_answer가 있지만 selected_choice가 없으면 보기와 매칭 시도
                if sc_val is None and fa_val and fa_val != "unknown":
                    sc_val = self._match_answer_to_choice(fa_val, choices)
                    if sc_val:
                        trace.append(f"Partial JSON: final_answer={fa_val!r} → matched choice {sc_val}")
                    else:
                        trace.append(f"Partial JSON: final_answer={fa_val!r}, no match found")
                else:
                    trace.append(f"Partial JSON: final_answer={fa_val!r}, selected_choice={sc_val}")
                return {
                    "final_answer": fa_val,
                    "law_used": law_match.group(1) if law_match else "unknown",
                    "selected_choice": sc_val,
                    "confidence": 0.6,
                }
            # Retry with minimal prompt
            return await self._retry_simple(stem=stem, choices_text=choices, trace=trace)
        except Exception as e:
            logger.error(f"Logic solver error: {e}")
            trace.append(f"Solver error: {e}")
            return {"final_answer": "unknown", "law_used": "unknown", "question_type": q_type, "confidence": 0.2}

    @staticmethod
    def _match_answer_to_choice(final_answer: str, choices_text: str) -> int | None:
        """Match final_answer string against choices text to find best choice number."""
        if not choices_text or not final_answer:
            return None
        # Normalize: strip whitespace, lowercase, remove units spacing
        def normalize(s: str) -> str:
            s = re.sub(r'\s+', '', s.lower())
            s = s.replace(',', '')  # 1,407 → 1407
            return s

        fa_norm = normalize(final_answer)
        # Extract numeric value from final_answer for numeric comparison
        fa_nums = re.findall(r'[\d.]+', final_answer)

        best_choice = None
        best_score = 0
        for line in choices_text.strip().split('\n'):
            m = re.match(r'^([1-4])[.)]\s*(.*)', line.strip())
            if not m:
                continue
            choice_num = int(m.group(1))
            choice_text = m.group(2).strip()
            choice_norm = normalize(choice_text)

            # Exact substring match
            if fa_norm in choice_norm or choice_norm in fa_norm:
                return choice_num

            # Numeric match: all numbers in final_answer appear in choice
            if fa_nums:
                choice_nums = re.findall(r'[\d.]+', choice_text)
                matches = sum(1 for n in fa_nums if n in choice_nums)
                score = matches / len(fa_nums)
                if score > best_score:
                    best_score = score
                    best_choice = choice_num

        return best_choice if best_score >= 0.5 else None

    @staticmethod
    def _fallback_extract(stem: str) -> dict:
        """Basic extraction when LLM unavailable."""
        nums = re.findall(r"[\d.]+\s*(?:Ω|V|A|W|kW|Hz|F|H|kΩ|mH|μF)", stem)
        return {
            "given": {"extracted_numbers": nums},
            "find": "unknown",
            "law_used": "unknown",
            "calculation_steps": ["LLM unavailable — manual calculation required"],
            "final_answer": "unknown",
            "unit": "",
            "confidence": 0.1,
        }
