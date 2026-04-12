"""Recover missing choice text for needs_ocr questions via Claude Vision.

Pipeline:
  1. Parse PDFs to identify questions flagged needs_ocr=True.
  2. Group these by source_page to batch Vision calls per page.
  3. Render each affected page to JPEG via pdfplumber.
  4. Ask Claude Haiku Vision to extract ①②③④ texts for the listed Q numbers.
  5. Merge results into the parsed questions and write
     data/ocr_recovered.json with the updated choices.
"""
from __future__ import annotations

import base64
import io
import json
import logging
import os
import sys
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import anthropic
import pdfplumber
from dotenv import load_dotenv

from ee_agent.ingestion.korean_parser import KoreanQuestionParser
from ee_agent.ingestion.pdf_extractor import PDFExtractor

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

MODEL = "claude-haiku-4-5-20251001"
RENDER_RESOLUTION = 200  # DPI for page rasterization
PLACEHOLDER = "[formula - OCR required]"


EXTRACT_PROMPT_TEMPLATE = """이 이미지는 전기기사 필기 기출문제 PDF의 한 페이지입니다.
아래 문제 번호들의 4개 선지(①②③④)를 정확히 추출해주세요.

대상 문제 번호: {q_numbers}

출력 규칙:
- 반드시 아래 JSON 형식으로만 응답 (다른 텍스트 금지)
- 수식은 유니코드/ASCII 혼합 텍스트로 표현 (예: λ²/(2πε₀d), e^(-t), ω², √(R²+X²))
- 선지가 그림/도식이어서 텍스트로 표현 불가능하면 "[diagram]"
- 해당 번호가 페이지에 없으면 스킵

{{
  "questions": [
    {{
      "number": 3,
      "choices": {{
        "1": "선지1 텍스트",
        "2": "선지2 텍스트",
        "3": "선지3 텍스트",
        "4": "선지4 텍스트"
      }}
    }}
  ]
}}"""


def render_page_jpeg(pdf_path: str, page_index: int, resolution: int = RENDER_RESOLUTION) -> bytes:
    """Rasterize a 1-indexed PDF page to JPEG bytes."""
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[page_index - 1]
        pil_image = page.to_image(resolution=resolution).original
        buf = io.BytesIO()
        pil_image.convert("RGB").save(buf, format="JPEG", quality=85)
        return buf.getvalue()


def call_vision(client: anthropic.Anthropic, image_bytes: bytes, q_numbers: list[int]) -> dict:
    """Send one page image to Claude Vision and return parsed JSON."""
    b64 = base64.standard_b64encode(image_bytes).decode()
    prompt = EXTRACT_PROMPT_TEMPLATE.format(q_numbers=q_numbers)
    response = client.messages.create(
        model=MODEL,
        max_tokens=2048,
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
    # Strip markdown code fences if present.
    if content.startswith("```"):
        lines = content.splitlines()
        content = "\n".join(l for l in lines if not l.startswith("```"))
    return json.loads(content)


def recover_pdf(pdf_path: str, year: int, session: int, client: anthropic.Anthropic) -> list[dict]:
    """Run OCR recovery for one PDF and return list of question dicts."""
    extractor = PDFExtractor()
    parser = KoreanQuestionParser()

    logger.info("Parsing %s", pdf_path)
    text, offsets = extractor.extract_full_text_with_offsets(pdf_path)
    questions = parser.parse_text(text, year=year, session=session, page_offsets=offsets)

    by_page: dict[int, list] = defaultdict(list)
    for q in questions:
        if q.needs_ocr and q.source_page:
            by_page[q.source_page].append(q)

    if not by_page:
        logger.info("No needs_ocr questions in %s", pdf_path)
        return []

    logger.info(
        "Recovering %d questions across %d pages",
        sum(len(qs) for qs in by_page.values()),
        len(by_page),
    )

    # Map question_number -> Question for merge.
    q_index = {q.question_number: q for q in questions}
    recovered: list[dict] = []

    for page_num in sorted(by_page):
        q_list = sorted(by_page[page_num], key=lambda x: x.question_number)
        q_numbers = [q.question_number for q in q_list]
        logger.info("Page %d: Q%s", page_num, q_numbers)

        try:
            image_bytes = render_page_jpeg(pdf_path, page_num)
        except Exception as exc:
            logger.error("Page %d render failed: %s", page_num, exc)
            continue

        try:
            result = call_vision(client, image_bytes, q_numbers)
        except Exception as exc:
            logger.error("Page %d Vision call failed: %s", page_num, exc)
            continue

        for item in result.get("questions", []):
            q_num = item.get("number")
            choices = item.get("choices", {})
            question = q_index.get(q_num)
            if not question:
                logger.warning("Q%s not in parsed set, skipping", q_num)
                continue

            # Update choices in place.
            updated = []
            all_filled = True
            for c in question.choices:
                new_text = choices.get(str(c.index), "").strip()
                if not new_text:
                    new_text = c.text  # keep placeholder
                    if new_text == PLACEHOLDER:
                        all_filled = False
                updated.append({"index": c.index, "text": new_text})

            recovered.append(
                {
                    "year": year,
                    "session": session,
                    "question_number": q_num,
                    "source_page": page_num,
                    "subject": question.subject.value,
                    "stem": question.stem,
                    "correct_answer": question.correct_answer,
                    "choices": updated,
                    "needs_ocr_resolved": all_filled,
                }
            )
            status = "OK" if all_filled else "partial"
            logger.info("  Q%s: %s", q_num, status)

        # Gentle rate-limit.
        time.sleep(0.4)

    return recovered


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    targets = [
        ("data/20200424_1회.pdf", 2020, 1),
        ("data/20220305_2회.pdf", 2022, 2),
    ]

    all_recovered: list[dict] = []
    for pdf_path, year, session in targets:
        if not Path(pdf_path).exists():
            logger.warning("Missing: %s", pdf_path)
            continue
        recovered = recover_pdf(pdf_path, year, session, client)
        all_recovered.extend(recovered)

    output_path = Path("data/ocr_recovered.json")
    output_path.write_text(
        json.dumps(all_recovered, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    resolved = sum(1 for r in all_recovered if r["needs_ocr_resolved"])
    logger.info(
        "Saved %d recovered questions to %s (%d fully resolved)",
        len(all_recovered),
        output_path,
        resolved,
    )


if __name__ == "__main__":
    main()
