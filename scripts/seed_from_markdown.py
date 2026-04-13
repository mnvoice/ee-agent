"""Append ■-delimited sections from a markdown file into knowledge_store.

Unlike seed_knowledge.py (which rebuilds from a PDF), this script loads the
existing store, appends new sections, and saves — preserving prior entries.
"""
import argparse
import logging
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ee_agent.rag.tfidf_retriever import TFIDFKnowledgeRetriever

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


FORMULA_KEYWORDS = [
    "=", "∝", "±", "∑", "∫", "√", "sin", "cos", "tan", "log",
    "공식", "법칙", "정리", "계산", "변환",
    "[A]", "[V]", "[Ω]", "[W]", "[Hz]", "[F]", "[H]",
    "ωn", "ζ", "s²", "G(s)",
]


def is_formula_section(text: str) -> bool:
    return any(kw in text for kw in FORMULA_KEYWORDS)


def parse_markdown(path: Path) -> list[dict]:
    """Split markdown on ■ headers into sections."""
    text = path.read_text(encoding="utf-8")
    chunks = re.split(r"(■[^\n]+)", text)
    sections: list[dict] = []
    current_name = ""
    current_body = ""
    for chunk in chunks:
        if chunk.startswith("■"):
            if current_body.strip() and current_name:
                sections.append(
                    {
                        "name": current_name.strip(),
                        "text": (current_name + "\n" + current_body).strip(),
                        "is_formula": is_formula_section(current_body),
                    }
                )
            current_name = chunk.strip()
            current_body = ""
        else:
            current_body += chunk
    if current_body.strip() and current_name:
        sections.append(
            {
                "name": current_name.strip(),
                "text": (current_name + "\n" + current_body).strip(),
                "is_formula": is_formula_section(current_body),
            }
        )
    return sections


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", required=True, help="Path to ■-delimited markdown")
    ap.add_argument("--subject", required=True, help="Subject tag (e.g., 제어공학)")
    ap.add_argument("--store", default="data/knowledge_store")
    args = ap.parse_args()

    md_path = Path(args.md)
    if not md_path.exists():
        logger.error("Markdown not found: %s", md_path)
        sys.exit(1)

    sections = parse_markdown(md_path)
    logger.info("Parsed %d sections from %s", len(sections), md_path)
    formula_n = sum(1 for s in sections if s["is_formula"])
    logger.info("  Formula: %d, Concept: %d", formula_n, len(sections) - formula_n)

    retriever = TFIDFKnowledgeRetriever()
    # Load existing entries so we append. Retriever.load() handles both
    # single-file and chunked layouts.
    store_dir = Path(args.store).parent
    store_name = Path(args.store).name
    has_single = Path(args.store + ".json").exists()
    has_chunks = any(store_dir.glob(store_name + "_[0-9]*.json"))
    if has_single or has_chunks:
        retriever.load(args.store)
        before = retriever.size()
        logger.info("Loaded existing store: %d entries", before)
    else:
        before = 0
        logger.info("No existing store — creating new")

    for s in sections:
        if s["is_formula"]:
            retriever.add_formula(
                name=s["name"],
                latex=s["text"],
                description=f"{args.subject} | {s['name']}",
                subject=args.subject,
            )
        else:
            retriever.add_concept(
                name=s["name"],
                definition=s["text"],
                subject=args.subject,
            )

    retriever.save(args.store)
    after = retriever.size()
    logger.info("Saved store: %d → %d (+%d)", before, after, after - before)

    # Verification queries
    logger.info("\n=== Verification ===")
    for q in [
        "근궤적 분리점 공식",
        "근궤적 점근선 교차점",
        "2차 시스템 감쇠율 고유주파수",
        "표준 전달함수 계수 매칭",
    ]:
        results = retriever.retrieve_formulas(q, k=1)
        if not results:
            results = retriever.retrieve_concepts(q, k=1)
        if results:
            name = results[0]["metadata"].get("name", "?")
            score = results[0]["score"]
            logger.info("  '%s' → %s (score=%.3f)", q, name, score)


if __name__ == "__main__":
    main()
