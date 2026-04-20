"""Stage 1 Pilot: validate needs_vision() detection + VisionSolver logic
using pre-captured OCR results as fixtures (no API calls needed).

Tests:
  1. needs_vision() correctly flags 7 target questions
  2. needs_vision() does NOT flag normal questions
  3. VisionSolver produces correct answers from fixture data
"""
from __future__ import annotations

import asyncio
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ee_agent.agents.base import AgentInput, AgentOutput
from ee_agent.agents.vision_solver import VisionSolver, needs_vision
from ee_agent.ingestion.korean_parser import KoreanQuestionParser
from ee_agent.ingestion.pdf_extractor import PDFExtractor
from ee_agent.pipeline.runner import _merge_ocr_recovered

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PASS = "\033[92m✅ PASS\033[0m"
FAIL = "\033[91m❌ FAIL\033[0m"

# Pre-captured Vision OCR results from Claude direct reading (2026-04-20)
FIXTURES = {
    64: {
        "stem": "다음의 개루프 전달함수 G(s)H(s) = K/[s(s+3)(s+8)], K≥0 에 대한 근궤적이 실수축에서 이탈하게 되는 분리점은 약 얼마인가?",
        "choices": {"1": "-0.93", "2": "-5.74", "3": "-6.0", "4": "-1.33"},
        "selected_choice": 4,
        "law_used": "근궤적 분리점: dK/ds=-(3s²+22s+24)=0 → s=-1.33",
        "final_answer": "-1.33",
    },
    65: {
        "stem": "F(z) = (1-e^(-aT))z / [(z-1)(z-e^(-aT))] 의 역 z 변환은?",
        "choices": {"1": "t·e^(-at)", "2": "at·e^(-at)", "3": "1+e^(-at)", "4": "1-e^(-at)"},
        "selected_choice": 4,
        "law_used": "부분분수 전개: F(z)/z = 1/(z-1) - 1/(z-e^(-aT))",
        "final_answer": "1-e^(-at)",
    },
    67: {
        "stem": "다음의 상태방정식 ẋ=[[0,1],[-3,-4]]x 으로 표현되는 시스템의 상태천이행렬은?",
        "choices": {
            "1": "[[1.5e^(-t)-0.5e^(-3t), -1.5e^(-t)+1.5e^(-3t)], [0.5e^(-t)-0.5e^(-3t), -0.5e^(-t)+1.5e^(-3t)]]",
            "2": "[[1.5e^(-t)-0.5e^(-3t), 0.5e^(-t)-0.5e^(-3t)], [-1.5e^(-t)+1.5e^(-3t), -0.5e^(-t)+1.5e^(-3t)]]",
            "3": "matrix3", "4": "matrix4",
        },
        "selected_choice": 2,
        "law_used": "고유값 λ=-1,-3, 상태천이행렬 e^(At)",
        "final_answer": "choice 2",
    },
    68: {
        "stem": "제어시스템의 전달함수가 T(s) = 1/(4s²+s+1) 과 같이 표현될 때 이 시스템의 고유주파수(ωn)와 감쇠율(ζ)은?",
        "choices": {"1": "ωn=0.25,ζ=1.0", "2": "ωn=0.5,ζ=0.25", "3": "ωn=0.5,ζ=0.5", "4": "ωn=1.0,ζ=0.5"},
        "selected_choice": 2,
        "law_used": "2차 표준형: s²+0.25s+0.25 → ωn=0.5, ζ=0.25",
        "final_answer": "ωn=0.5, ζ=0.25",
    },
    80: {
        "stem": "f(t) = L⁻¹[(s²+3s+2)/(s²+2s+5)] 는?",
        "choices": {
            "1": "δ(t)+e^(-t)(cos2t-sin2t)", "2": "δ(t)+e^(-t)(cos2t+2sin2t)",
            "3": "δ(t)+e^(-t)(cos2t-2sin2t)", "4": "δ(t)+e^(-t)(cos2t+sin2t)",
        },
        "selected_choice": 3,
        "law_used": "다항식 나눗셈 + 부분분수: 1+(s-3)/((s+1)²+4)",
        "final_answer": "δ(t)+e^(-t)(cos2t-2sin2t)",
    },
    11: {
        "stem": "진공 중에서 점(1,3)m에 -2×10⁻⁹C 점전하, 점(2,1)m에 1C → 힘(N)?",
        "choices": {
            "1": "(-18/(5√5))x̂+(36/(5√5))ŷ",
            "2": "(18/(5√5))x̂+(36/(5√5))ŷ",
            "3": "(-18/(5√5))x̂-(36/(5√5))ŷ",
            "4": "(18/(5√5))x̂-(36/(5√5))ŷ",
        },
        "selected_choice": 1,
        "law_used": "쿨롱 법칙: F=kQ₁Q₂r̂/r²",
        "final_answer": "(-18/(5√5))x̂+(36/(5√5))ŷ",
    },
    75: {
        "stem": "그림과 같은 부하에 선간전압 Vab=100∠30°(V)인 평형 3상 전압을 가했을 때 선전류 Ia(A)는?",
        "choices": {"1": "choice1", "2": "choice2", "3": "choice3", "4": "choice4"},
        "selected_choice": 1,
        "law_used": "3상 Y부하 전류 계산",
        "final_answer": "choice 1",
    },
}


def test_needs_vision() -> tuple[int, int]:
    """Test needs_vision() detection accuracy."""
    ext = PDFExtractor()
    parser = KoreanQuestionParser()
    text, offsets = ext.extract_full_text_with_offsets("data/20200424_1회.pdf")
    qs = parser.parse_text(text, year=2020, session=1, page_offsets=offsets)
    _merge_ocr_recovered(qs, 2020)

    target_set = set(FIXTURES.keys())
    passes = 0
    fails = 0

    # Test 1: target questions SHOULD be flagged
    print("\n[Test 1] needs_vision() — 7 target questions should be True")
    for q in sorted(qs, key=lambda x: x.question_number):
        if q.question_number in target_set:
            result = needs_vision(q)
            mark = PASS if result else FAIL
            print(f"  {mark}  Q{q.question_number:3d}: needs_vision={result}")
            if result:
                passes += 1
            else:
                fails += 1

    # Test 2: sample normal questions should NOT be flagged
    print("\n[Test 2] needs_vision() — normal questions should be False")
    normals = [q for q in qs if q.question_number in (1, 7, 26, 50, 66, 82)]
    for q in normals:
        result = needs_vision(q)
        expected = False
        mark = PASS if result == expected else FAIL
        print(f"  {mark}  Q{q.question_number:3d}: needs_vision={result} (expected {expected})")
        if result == expected:
            passes += 1
        else:
            fails += 1

    return passes, fails


async def test_vision_solver() -> tuple[int, int]:
    """Test VisionSolver with fixture data (no API calls)."""
    print("\n[Test 3] VisionSolver — fixture-based solve")

    class MockLLM:
        """Returns pre-captured fixture as if Vision API responded."""
        def __init__(self):
            self._current_qno = 0

        async def complete_vision(self, image_b64: str, prompt: str, max_tokens: int = 2048):
            fixture = FIXTURES.get(self._current_qno, {})
            fixture_copy = {**fixture, "confidence": 0.70, "method": "vision_solve"}

            class MockResponse:
                content = json.dumps(fixture_copy, ensure_ascii=False)
            return MockResponse()

    mock_llm = MockLLM()
    solver = VisionSolver(llm=mock_llm)

    ext = PDFExtractor()
    parser = KoreanQuestionParser()
    text, offsets = ext.extract_full_text_with_offsets("data/20200424_1회.pdf")
    qs = parser.parse_text(text, year=2020, session=1, page_offsets=offsets)
    _merge_ocr_recovered(qs, 2020)
    q_map = {q.question_number: q for q in qs}

    passes = 0
    fails = 0

    for qn, fixture in sorted(FIXTURES.items()):
        q = q_map.get(qn)
        if not q:
            continue
        mock_llm._current_qno = qn
        inp = AgentInput(
            question_id=q.id,
            context={
                "question_number": qn,
                "stem": q.stem,
                "choices": [{"index": c.index, "text": c.text} for c in q.choices],
                "page_jpeg": b"fake_jpeg_bytes",  # mock
            },
        )
        out = await solver.run(inp)
        expected = q.correct_answer
        got = out.result.get("selected_choice")
        correct = got == expected
        mark = PASS if correct else FAIL
        method = out.result.get("method", "?")
        conf = out.confidence
        print(f"  {mark}  Q{qn:3d}: got={got} expected={expected} conf={conf} method={method}")
        if correct:
            passes += 1
        else:
            fails += 1

    return passes, fails


async def main():
    print("=" * 60)
    print("Stage 1 Pilot: VisionSolver (fixture-based)")
    print("=" * 60)

    p1, f1 = test_needs_vision()
    p2, f2 = await test_vision_solver()

    total_pass = p1 + p2
    total_fail = f1 + f2

    print(f"\n{'=' * 60}")
    print(f"  Pilot 결과: PASS {total_pass} / FAIL {total_fail}")
    if total_fail == 0:
        print(f"  → Stage 1 통과. Stage 2 (harness 통합) 진행 가능.")
    else:
        print(f"  → Stage 1 실패. {total_fail}건 수정 필요.")
    print(f"{'=' * 60}")

    sys.exit(1 if total_fail > 0 else 0)


if __name__ == "__main__":
    asyncio.run(main())
