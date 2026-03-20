#!/usr/bin/env python3
"""
Resolve cross-references in question JSON files.

The 1998-2010 "D-60 series" PDFs contain cross-references like:
    "문제 06 2014년도 2회 문제08"
meaning "Question 06 = see 2014 session 2 Q8".

This script:
1. Parses Mathpix OCR cache to find cross-reference patterns
2. Looks up the referenced question in existing JSON data
3. Copies text, choices, and answer from the source question

Usage:
    python scripts/resolve_crossrefs.py --dry-run
    python scripts/resolve_crossrefs.py --apply
"""

import argparse
import json
import logging
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

XREF_PATTERN = re.compile(
    r"문제\s*(\d{1,3})\s+(\d{4})년도\s*(\d)회\s*문제\s*(\d{1,3})"
)


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def build_question_index() -> dict[tuple[int, str, int], dict]:
    """Build lookup: (year, session, q_no) -> question dict."""
    index = {}
    for fp in sorted(DATA_DIR.glob("questions_기출_*.json")):
        qs = json.loads(fp.read_text(encoding="utf-8"))
        for q in qs:
            key = (q.get("year"), q.get("session"), q.get("q_no"))
            index[key] = q
    return index


def find_crossrefs() -> dict[str, list[dict]]:
    """Parse Mathpix OCR cache for cross-references.

    Returns: {json_filename: [{src_q_no, tgt_year, tgt_session, tgt_q_no}, ...]}
    """
    result: dict[str, list[dict]] = defaultdict(list)

    for fp in sorted(DATA_DIR.glob("mathpix_기출_*.json")):
        fname = _nfc(fp.name)
        m_file = re.search(r"mathpix_기출_(\d{4})_(.+?)\.json", fname)
        if not m_file:
            continue

        source_year = m_file.group(1)
        source_session = m_file.group(2)
        json_file = f"questions_기출_{source_year}_{source_session}.json"

        cache = json.loads(fp.read_text(encoding="utf-8"))
        full_text = "\n".join(p.get("text", "") for p in cache)

        for m in XREF_PATTERN.finditer(full_text):
            result[json_file].append(
                {
                    "src_q_no": int(m.group(1)),
                    "tgt_year": int(m.group(2)),
                    "tgt_session": f"{m.group(3)}회",
                    "tgt_q_no": int(m.group(4)),
                }
            )

    return dict(result)


def is_question_complete(q: dict) -> bool:
    text_ok = bool(q.get("text", "").strip())
    choices = q.get("choices", [])
    choices_ok = len(choices) == 4 and all(c.strip() for c in choices)
    answer_ok = q.get("answer", 0) in [1, 2, 3, 4]
    return text_ok and choices_ok and answer_ok


def main():
    parser = argparse.ArgumentParser(description="Resolve cross-references")
    parser.add_argument(
        "--apply", action="store_true", help="Apply fixes (default: dry-run)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show what would be fixed"
    )
    args = parser.parse_args()

    if not args.apply:
        args.dry_run = True

    logger.info("Building question index...")
    q_index = build_question_index()
    logger.info("Index: %d questions", len(q_index))

    logger.info("Finding cross-references...")
    xrefs = find_crossrefs()
    total_xrefs = sum(len(v) for v in xrefs.values())
    logger.info("Cross-references: %d in %d files", total_xrefs, len(xrefs))

    resolved = 0
    skipped_already_ok = 0
    skipped_target_broken = 0
    skipped_target_missing = 0
    files_modified = 0

    for json_file, refs in sorted(xrefs.items()):
        fp = DATA_DIR / json_file
        if not fp.exists():
            continue

        qs = json.loads(fp.read_text(encoding="utf-8"))
        q_by_no = {q["q_no"]: q for q in qs}
        file_fixed = 0

        for ref in refs:
            src_q = q_by_no.get(ref["src_q_no"])
            if not src_q:
                continue

            # Skip if source question is already complete
            if is_question_complete(src_q):
                skipped_already_ok += 1
                continue

            # Find target
            target = q_index.get(
                (ref["tgt_year"], ref["tgt_session"], ref["tgt_q_no"])
            )
            if not target:
                skipped_target_missing += 1
                continue

            if not is_question_complete(target):
                skipped_target_broken += 1
                continue

            # Copy fields from target to source
            if not src_q.get("text", "").strip():
                src_q["text"] = target["text"]
            if not (
                len(src_q.get("choices", [])) == 4
                and all(c.strip() for c in src_q.get("choices", []))
            ):
                src_q["choices"] = target["choices"]
            if src_q.get("answer", 0) not in [1, 2, 3, 4]:
                src_q["answer"] = target["answer"]

            resolved += 1
            file_fixed += 1

        if file_fixed > 0 and args.apply:
            fp.write_text(
                json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            files_modified += 1
            logger.info("  %s: %d questions resolved", json_file, file_fixed)

    logger.info("")
    logger.info("=" * 60)
    logger.info("CROSS-REFERENCE RESOLUTION RESULTS")
    logger.info("=" * 60)
    logger.info("Resolved: %d", resolved)
    logger.info("Skipped (already OK): %d", skipped_already_ok)
    logger.info("Skipped (target broken): %d", skipped_target_broken)
    logger.info("Skipped (target not found): %d", skipped_target_missing)
    if args.apply:
        logger.info("Files modified: %d", files_modified)
    else:
        logger.info("DRY RUN — no files modified. Use --apply to write.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
