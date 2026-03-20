#!/usr/bin/env python3
"""
Re-parse answer keys from Mathpix OCR cache with improved regex.

The original parser missed answers due to:
- LaTeX-encoded answers: 【답】\({ }^{3}\)
- Full-width parentheses: 【답】（2）
- Missing parentheses: 【답】 4
- Corrupted OCR: 【답】 I (should be 1)

This script re-extracts answers from cached OCR text and applies them
to questions that have text+choices but answer=0.

Usage:
    python scripts/reparse_answers_from_ocr.py --dry-run
    python scripts/reparse_answers_from_ocr.py --apply
"""

import argparse
import json
import logging
import re
import unicodedata
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# Answer extraction patterns (ordered by specificity)
ANSWER_PATTERNS = [
    # Standard: 【답】(3) or [답] (4)
    re.compile(
        r"[【\[]\s*[딥답덥]\s*[】\]]\s*[（(]\s*([1-4])\s*[）)]"
    ),
    # Circle numbers: 【답】③
    re.compile(
        r"[【\[]\s*[딥답덥]\s*[】\]]\s*([①②③④])"
    ),
    # Bare number: 【답】 4
    re.compile(
        r"[【\[]\s*[딥답덥]\s*[】\]]\s+([1-4])(?:\s|$)"
    ),
    # LaTeX: 【답】\({ }^{3}\) or 【답】\(3\)
    re.compile(
        r"[【\[]\s*[딥답덥]\s*[】\]]\s*\\[\(\{]\s*\{?\s*\}?\s*\^?\s*\{?\s*([1-4])\s*\}?\s*\\[\)\}]"
    ),
    # Filled circles: 【답】❸
    re.compile(
        r"[【\[]\s*[딥답덥]\s*[】\]]\s*([❶❷❸❹])"
    ),
]

CHOICE_MAP = {
    "①": 1, "②": 2, "③": 3, "④": 4,
    "❶": 1, "❷": 2, "❸": 3, "❹": 4,
    "1": 1, "2": 2, "3": 3, "4": 4,
}

# Question header pattern
Q_RE = re.compile(r"문제\s*(\d{1,3})")


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def extract_answers_from_ocr(ocr_text: str) -> dict[int, int]:
    """Extract all answers from OCR text, keyed by question number.

    Strategy: Find each question block, then search for answer pattern within it.
    """
    answers: dict[int, int] = {}

    # Find all question positions
    q_positions = [(m.start(), int(m.group(1))) for m in Q_RE.finditer(ocr_text)]

    # Deduplicate by q_no (keep first)
    seen = set()
    unique = []
    for pos, qno in q_positions:
        if qno not in seen and 1 <= qno <= 100:
            seen.add(qno)
            unique.append((pos, qno))

    for idx, (start, qno) in enumerate(unique):
        end = unique[idx + 1][0] if idx + 1 < len(unique) else len(ocr_text)
        block = ocr_text[start:end]

        # Try each pattern
        for pattern in ANSWER_PATTERNS:
            m = pattern.search(block)
            if m:
                raw = m.group(1)
                ans = CHOICE_MAP.get(raw, 0)
                if ans:
                    answers[qno] = ans
                    break

    return answers


def main():
    parser = argparse.ArgumentParser(description="Re-parse answers from OCR cache")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.apply:
        args.dry_run = True

    total_fixed = 0
    files_modified = 0

    for ocr_fp in sorted(DATA_DIR.glob("mathpix_기출_*.json")):
        fname = _nfc(ocr_fp.name)
        m = re.search(r"mathpix_기출_(\d{4})_(.+?)\.json", fname)
        if not m:
            continue

        year_str, session = m.group(1), m.group(2)
        json_file = DATA_DIR / f"questions_기출_{year_str}_{session}.json"
        if not json_file.exists():
            continue

        # Load OCR cache
        cache = json.loads(ocr_fp.read_text(encoding="utf-8"))
        full_text = "\n".join(p.get("text", "") for p in cache)

        # Extract answers
        ocr_answers = extract_answers_from_ocr(full_text)
        if not ocr_answers:
            continue

        # Load questions
        qs = json.loads(json_file.read_text(encoding="utf-8"))
        file_fixed = 0

        for q in qs:
            if q.get("answer", 0) in [1, 2, 3, 4]:
                continue  # Already has valid answer
            qno = q.get("q_no", 0)
            if qno in ocr_answers:
                q["answer"] = ocr_answers[qno]
                file_fixed += 1

        if file_fixed > 0:
            if args.apply:
                json_file.write_text(
                    json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            total_fixed += file_fixed
            files_modified += 1
            logger.info("  %s: %d answers fixed", json_file.name, file_fixed)

    logger.info("")
    logger.info("=" * 60)
    logger.info("OCR ANSWER RE-PARSE RESULTS")
    logger.info("=" * 60)
    logger.info("Total answers fixed: %d", total_fixed)
    logger.info("Files modified: %d", files_modified)
    if args.dry_run:
        logger.info("DRY RUN — no files modified. Use --apply to write.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
