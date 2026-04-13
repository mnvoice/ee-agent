"""Extract text from image-based PDF using Claude Vision API, then seed into RAG."""
import base64
import json
import logging
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import anthropic
import pdfplumber
from dotenv import load_dotenv

from ee_agent.rag.tfidf_retriever import TFIDFKnowledgeRetriever

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

EXTRACT_PROMPT = """이 이미지는 전기기사 전기자기학 요약 교재의 한 페이지입니다.
페이지의 모든 텍스트 내용을 정확하게 추출해 주세요.

다음 형식으로 출력해 주세요:
- 섹션 제목(■ 기호로 시작하는 항목)은 그대로 유지
- 공식은 최대한 텍스트로 표현 (예: F = Q1*Q2 / (4*pi*epsilon*r^2))
- 수식 기호: 엡실론=ε, 뮤=μ, 파이=π, 오메가=Ω, 루트=√
- 페이지 번호나 구매자 워터마크는 제외
- 내용이 없는 페이지는 '내용없음' 으로만 출력"""

FORMULA_KEYWORDS = [
    "=", "공식", "법칙", "정리", "계산",
    "[A]", "[V]", "[Ω]", "[W]", "[Hz]", "[F]", "[H]",
    "sin", "cos", "tan", "√", "∫", "∑", "π",
]


def is_formula_section(text: str) -> bool:
    return any(kw in text for kw in FORMULA_KEYWORDS)


def extract_page_image(page) -> bytes | None:
    """Extract raw JPEG bytes from a pdfplumber page."""
    if not page.images:
        return None
    img_obj = page.images[0]
    stream = img_obj.get("stream")
    if stream is None:
        return None
    try:
        return stream.get_rawdata()
    except Exception:
        return None


def extract_sections_from_text(text: str, page_num: int) -> list[dict]:
    """Split Claude-extracted text into ■-delimited sections."""
    sections = []
    chunks = re.split(r"(■[^\n]+)", text)

    current_name = f"전기자기학_p{page_num}"
    current_body = ""

    for chunk in chunks:
        if chunk.startswith("■"):
            if current_body.strip():
                sections.append({
                    "name": current_name.strip(),
                    "text": (current_name + "\n" + current_body).strip(),
                    "is_formula": is_formula_section(current_body),
                })
            current_name = chunk.strip()
            current_body = ""
        else:
            current_body += chunk

    if current_body.strip():
        sections.append({
            "name": current_name.strip(),
            "text": (current_name + "\n" + current_body).strip(),
            "is_formula": is_formula_section(current_body),
        })

    return sections


def process_pdf(pdf_path: str, client: anthropic.Anthropic, skip_pages: int = 1) -> list[dict]:
    """Process all pages and return extracted sections."""
    all_sections = []

    with pdfplumber.open(pdf_path) as pdf:
        total = len(pdf.pages)
        logger.info(f"총 {total}페이지 처리 시작")

        for i, page in enumerate(pdf.pages):
            page_num = i + 1

            # 앞쪽 목차/색인 페이지 skip
            if page_num <= skip_pages:
                logger.info(f"페이지 {page_num}: skip (목차/색인)")
                continue

            raw_jpeg = extract_page_image(page)
            if raw_jpeg is None:
                logger.warning(f"페이지 {page_num}: 이미지 없음, skip")
                continue

            b64 = base64.standard_b64encode(raw_jpeg).decode()
            logger.info(f"페이지 {page_num}/{total}: Claude Vision 처리 중...")

            try:
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
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
                                {"type": "text", "text": EXTRACT_PROMPT},
                            ],
                        }
                    ],
                )
                extracted = response.content[0].text.strip()

                if "내용없음" in extracted or len(extracted) < 20:
                    logger.info(f"페이지 {page_num}: 내용 없음")
                    continue

                sections = extract_sections_from_text(extracted, page_num)
                logger.info(f"페이지 {page_num}: {len(sections)}개 섹션 추출")
                all_sections.extend(sections)

                # API rate limit 방지
                time.sleep(0.3)

            except Exception as e:
                logger.error(f"페이지 {page_num} 처리 실패: {e}")
                continue

    return all_sections


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", default="data/전기자기학_가이드.pdf")
    ap.add_argument("--subject", default="전자기학")
    ap.add_argument("--skip-pages", type=int, default=1, help="앞에서 건너뛸 페이지 수 (목차 등)")
    args = ap.parse_args()

    pdf_path = Path(args.pdf)
    subject = args.subject
    skip_pages = args.skip_pages
    store_path = "data/knowledge_store"

    if not pdf_path.exists():
        logger.error(f"파일 없음: {pdf_path}")
        sys.exit(1)

    import os
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY 환경변수 없음")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    logger.info(f"PDF 처리: {pdf_path} (subject={subject}, skip={skip_pages}페이지)")
    sections = process_pdf(str(pdf_path), client, skip_pages=skip_pages)
    logger.info(f"총 {len(sections)}개 섹션 추출 완료")

    if not sections:
        logger.error("추출된 섹션 없음")
        sys.exit(1)

    # 기존 knowledge store 로드
    retriever = TFIDFKnowledgeRetriever()
    if Path(store_path + ".json").exists():
        retriever.load(store_path)
        before = retriever.size()
        logger.info(f"기존 DB 로드: {before}개")
    else:
        before = 0

    # 새 섹션 추가
    added = 0
    for section in sections:
        if section["is_formula"]:
            retriever.add_formula(
                name=section["name"],
                latex=section["text"],
                description=f"{subject} | {section['name']}",
                subject=subject,
            )
        else:
            retriever.add_concept(
                name=section["name"],
                definition=section["text"],
                subject=subject,
            )
        added += 1

    retriever.save(store_path)
    logger.info(f"저장 완료: {before}개 → {retriever.size()}개 (+{added}개)")

    # 추출 결과 저장 (검토용)
    safe_name = subject.replace("/", "_")
    output_path = Path(f"data/{safe_name}_extracted.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=2)
    logger.info(f"추출 텍스트 저장: {output_path}")


if __name__ == "__main__":
    main()
