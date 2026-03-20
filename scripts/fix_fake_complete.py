#!/usr/bin/env python3
"""
Fix fake-complete questions where cross-reference text was left in the text field.

These questions have choices+answer copied from the target, but the text field
still contains cross-reference pointers like "2013년도 1회 문제09".

This script:
1. Detects questions with cross-reference text patterns
2. Resolves the cross-reference to find the actual question
3. Replaces the text with the real question text

Usage:
    python scripts/fix_fake_complete.py --dry-run
    python scripts/fix_fake_complete.py --apply
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

# Detect cross-reference text
XREF_TEXT_PATTERN = re.compile(r"^\s*(\d{4})년도\s*(\d)회\s*문제\s*(\d{1,3})")


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def build_question_index() -> dict[tuple[int, str, int], dict]:
    index = {}
    for fp in sorted(DATA_DIR.glob("questions_기출_*.json")):
        qs = json.loads(fp.read_text(encoding="utf-8"))
        for q in qs:
            key = (q.get("year"), q.get("session"), q.get("q_no"))
            index[key] = q
    return index


def is_crossref_text(text: str) -> bool:
    """Check if question text is actually a cross-reference pointer."""
    return bool(XREF_TEXT_PATTERN.match(text.strip()))


def extract_crossref(text: str) -> tuple[int, str, int] | None:
    """Extract (year, session, q_no) from cross-reference text."""
    m = XREF_TEXT_PATTERN.match(text.strip())
    if not m:
        return None
    return (int(m.group(1)), f"{m.group(2)}회", int(m.group(3)))


def main():
    parser = argparse.ArgumentParser(description="Fix fake-complete questions")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.apply:
        args.dry_run = True

    logger.info("Building question index...")
    q_index = build_question_index()

    total_fake = 0
    total_fixed = 0
    total_demoted = 0
    files_modified = 0

    for fp in sorted(DATA_DIR.glob("questions_기출_*.json")):
        qs = json.loads(fp.read_text(encoding="utf-8"))
        file_fixed = 0
        file_demoted = 0

        for q in qs:
            text = q.get("text", "").strip()
            if not is_crossref_text(text):
                continue

            total_fake += 1
            ref = extract_crossref(text)
            if not ref:
                continue

            target = q_index.get(ref)
            if target and target.get("text", "").strip() and not is_crossref_text(target["text"]):
                # Replace with real text from target
                q["text"] = target["text"]
                file_fixed += 1
            else:
                # Can't resolve — demote to incomplete by clearing text
                # so it's no longer counted as "complete"
                q["text"] = ""
                file_demoted += 1

        changes = file_fixed + file_demoted
        if changes > 0:
            if args.apply:
                fp.write_text(
                    json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            total_fixed += file_fixed
            total_demoted += file_demoted
            files_modified += 1
            logger.info(
                "  %s: %d text replaced, %d demoted",
                fp.name, file_fixed, file_demoted,
            )

    logger.info("")
    logger.info("=" * 60)
    logger.info("FAKE COMPLETE FIX RESULTS")
    logger.info("=" * 60)
    logger.info("Fake-complete found: %d", total_fake)
    logger.info("Text replaced from target: %d", total_fixed)
    logger.info("Demoted (target unavailable): %d", total_demoted)
    logger.info("Files modified: %d", files_modified)
    if args.dry_run:
        logger.info("DRY RUN — use --apply to write.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
