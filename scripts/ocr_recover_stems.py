"""Recover missing stem formulas and choice text via Claude Vision.

Extension of ocr_recover_choices.py — targets questions where the STEM
contains inline formula images that pdfplumber cannot extract.

Usage:
  python3 scripts/ocr_recover_stems.py
  python3 scripts/ocr_recover_stems.py --pdf data/20200424_1회.pdf --questions 64,65,68,80
"""
from __future__ import annotations

import argparse
import base64
import io
import json
import logging
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import anthropic
import pdfplumber
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

MODEL = "claude-haiku-4-5-20251001"
RENDER_RESOLUTION = 200


STEM_EXTRACT_PROMPT = """이 이미지는 전기기사 필기 기출문제 PDF의 한 페이지입니다.

아래 문제 번호들에 대해 다음을 추출해주세요:
1. **stem**: 문제 전체 텍스트 (수식 포함). 이미지로 렌더링된 수식도 텍스트로 변환.
2. **choices**: ①②③④ 선지 텍스트 (이미지 수식 포함)

대상 문제 번호: {q_numbers}

수식 표현 규칙:
- 분수: a/b 또는 (a+b)/(c+d)
- 전달함수: G(s) = K/[s(s+1)(s+4)]
- 행렬: [[a,b],[c,d]]
- 라플라스: F(s) = (s+1)/((s+2)²+4)
- z변환: F(z) = z/(z-e^(-aT))
- 그리스 문자: ω, ζ, ε, μ, λ, Φ, δ
- 지수: e^(-t), e^(st)
- 미적분: ∂D/∂t, d²c/dt²
- 벡터: (ax + by) 형태로 방향 표시

출력 형식 (JSON만, 다른 텍스트 금지):
{{
  "questions": [
    {{
      "number": 64,
      "stem": "다음의 개루프 전달함수 G(s)H(s) = K/[s(s+1)(s+4)] 에 대한 근궤적이 실수축에서 이탈하게 되는 분리점은 약 얼마인가?",
      "choices": {{
        "1": "-0.93",
        "2": "-5.74",
        "3": "-6.0",
        "4": "-1.33"
      }}
    }}
  ]
}}"""


def render_page_jpeg(pdf_path: str, page_num: int) -> bytes:
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_num - 1]
        pil_image = page.to_image(resolution=RENDER_RESOLUTION).original
        buf = io.BytesIO()
        pil_image.convert("RGB").save(buf, format="JPEG", quality=85)
        return buf.getvalue()


def call_vision(client: anthropic.Anthropic, image_bytes: bytes, q_numbers: list[int]) -> dict:
    b64 = base64.standard_b64encode(image_bytes).decode()
    prompt = STEM_EXTRACT_PROMPT.format(q_numbers=q_numbers)
    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": b64,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    )
    content = response.content[0].text.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        content = "\n".join(l for l in lines if not l.startswith("```"))
    return json.loads(content)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default="data/20200424_1회.pdf")
    ap.add_argument("--questions", default="64,65,68,80",
                    help="Comma-separated question numbers")
    ap.add_argument("--output", default="output/stem_ocr_recovered.json")
    args = ap.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    target_qs = [int(q.strip()) for q in args.questions.split(",")]

    # Map questions to pages (hardcoded for 2020_1회 — extend as needed)
    from ee_agent.ingestion.pdf_extractor import PDFExtractor
    from ee_agent.ingestion.korean_parser import KoreanQuestionParser

    ext = PDFExtractor()
    parser = KoreanQuestionParser()
    text, offsets = ext.extract_full_text_with_offsets(args.pdf)
    all_qs = parser.parse_text(text, year=2020, session=1, page_offsets=offsets)

    from collections import defaultdict
    by_page: dict[int, list[int]] = defaultdict(list)
    q_index = {}
    for q in all_qs:
        if q.question_number in target_qs and q.source_page:
            by_page[q.source_page].append(q.question_number)
            q_index[q.question_number] = q

    if not by_page:
        logger.error("No target questions found with source_page")
        sys.exit(1)

    logger.info("Target: %d questions across %d pages", len(target_qs), len(by_page))

    results = []
    for page_num in sorted(by_page):
        q_nums = sorted(by_page[page_num])
        logger.info("Page %d: Q%s", page_num, q_nums)

        try:
            image_bytes = render_page_jpeg(args.pdf, page_num)
        except Exception as exc:
            logger.error("Page %d render failed: %s", page_num, exc)
            continue

        try:
            vision_result = call_vision(client, image_bytes, q_nums)
        except Exception as exc:
            logger.error("Page %d Vision call failed: %s", page_num, exc)
            continue

        for item in vision_result.get("questions", []):
            qn = item.get("number")
            if qn not in q_index:
                continue

            orig = q_index[qn]
            recovered_stem = item.get("stem", "")
            recovered_choices = item.get("choices", {})

            results.append({
                "q_no": qn,
                "page": page_num,
                "subject": orig.subject.value,
                "original_stem": orig.stem,
                "original_stem_len": len(orig.stem),
                "recovered_stem": recovered_stem,
                "recovered_stem_len": len(recovered_stem),
                "original_choices": [
                    {"idx": c.index, "text": c.text} for c in orig.choices
                ],
                "recovered_choices": recovered_choices,
                "correct_answer": orig.correct_answer,
            })
            logger.info("  Q%d: stem %d→%d chars", qn, len(orig.stem), len(recovered_stem))

        time.sleep(0.4)

    # Save
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    logger.info("Saved %d results to %s", len(results), args.output)


if __name__ == "__main__":
    main()
