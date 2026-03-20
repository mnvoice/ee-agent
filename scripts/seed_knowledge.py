"""Seed RAG knowledge base from DreamingRyan summary PDF."""
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ee_agent.ingestion.pdf_extractor import PDFExtractor
from ee_agent.rag.tfidf_retriever import TFIDFKnowledgeRetriever

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

SUBJECT_MAP = {
    range(4, 13): "회로이론",
    range(13, 19): "제어공학",
    range(19, 28): "전자기학",
    range(28, 41): "전기기기",
    range(41, 51): "전력공학",
    range(51, 62): "전기설비기술기준",
}

FORMULA_KEYWORDS = ["=", "∝", "±", "∑", "∫", "√", "sin", "cos", "tan", "log",
                    "공식", "법칙", "정리", "계산", "변환", "[A]", "[V]", "[Ω]",
                    "[W]", "[Hz]", "[F]", "[H]", "[kW]", "[kV]", "[MVA]"]


def get_subject(page_num: int) -> str:
    for page_range, subject in SUBJECT_MAP.items():
        if page_num in page_range:
            return subject
    return "일반"


def is_formula_section(text: str) -> bool:
    return any(kw in text for kw in FORMULA_KEYWORDS)


def extract_sections(pages) -> list[dict]:
    """Extract ■-delimited sections from PDF pages."""
    sections = []

    for page in pages:
        subject = get_subject(page.page_number)
        text = page.text

        # Remove buyer watermark
        text = re.sub(r"구매자\s*:\s*\S+\n?", "", text)

        # Split on ■ headers
        chunks = re.split(r"(■[^\n]+)", text)

        current_name = f"페이지{page.page_number}"
        current_body = ""

        for chunk in chunks:
            if chunk.startswith("■"):
                # Save previous section
                if current_body.strip():
                    sections.append({
                        "name": current_name.strip(),
                        "text": (current_name + "\n" + current_body).strip(),
                        "subject": subject,
                        "is_formula": is_formula_section(current_body),
                        "page": page.page_number,
                    })
                current_name = chunk.strip()
                current_body = ""
            else:
                current_body += chunk

        # Save last section of page
        if current_body.strip():
            sections.append({
                "name": current_name.strip(),
                "text": (current_name + "\n" + current_body).strip(),
                "subject": subject,
                "is_formula": is_formula_section(current_body),
                "page": page.page_number,
            })

    return sections


def main():
    pdf_path = Path("data/DreamingRyan_16.pdf")
    store_path = "data/knowledge_store"

    if not pdf_path.exists():
        logger.error(f"PDF not found: {pdf_path}")
        sys.exit(1)

    logger.info(f"Loading PDF: {pdf_path}")
    extractor = PDFExtractor()
    pages = extractor.extract_pages(pdf_path)
    logger.info(f"Extracted {len(pages)} pages")

    sections = extract_sections(pages)
    logger.info(f"Found {len(sections)} sections")

    formula_count = sum(1 for s in sections if s["is_formula"])
    concept_count = len(sections) - formula_count
    logger.info(f"  Formulas: {formula_count}, Concepts: {concept_count}")

    logger.info("Building TF-IDF knowledge base...")
    retriever = TFIDFKnowledgeRetriever()

    for section in sections:
        if section["is_formula"]:
            retriever.add_formula(
                name=section["name"],
                latex=section["text"],
                description=f"{section['subject']} | {section['name']}",
            )
        else:
            retriever.add_concept(
                name=section["name"],
                definition=section["text"],
                subject=section["subject"],
            )

    logger.info(f"Saving to {store_path}...")
    retriever.save(store_path)
    logger.info(f"Done. Total entries: {retriever.size()}")

    # Quick verification
    logger.info("\n=== Verification ===")
    test_queries = [
        "옴의 법칙 전류 전압 저항",
        "변압기 효율 계산",
        "접지 시스템 KEC",
        "유도전동기 슬립",
    ]
    for q in test_queries:
        results = retriever.retrieve_formulas(q, k=1)
        if not results:
            results = retriever.retrieve_concepts(q, k=1)
        if results:
            name = results[0]["metadata"].get("name", "?")
            score = results[0]["score"]
            logger.info(f"  '{q}' → {name} (score={score:.3f})")


if __name__ == "__main__":
    main()
