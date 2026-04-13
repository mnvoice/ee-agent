"""Re-tag subject field of existing questions_기출_*.json using the new
keyword-first + number-range fallback strategy. Does not re-parse or OCR.
"""
import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent))

from batch_gichul_pipeline import get_subject

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


def retag(path: Path) -> tuple[int, dict[str, int], dict[str, int]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = data["questions"] if isinstance(data, dict) and "questions" in data else data

    before: dict[str, int] = {}
    after: dict[str, int] = {}
    changed = 0
    for q in questions:
        prev = q.get("subject", "기타")
        before[prev] = before.get(prev, 0) + 1

        text_bits = [q.get("text", ""), " ".join(q.get("choices", []) or [])]
        new_subj = get_subject(q.get("q_no", 0), " ".join(text_bits))
        if new_subj != prev:
            changed += 1
        q["subject"] = new_subj
        after[new_subj] = after.get(new_subj, 0) + 1

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return changed, before, after


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+", help="JSON file paths to retag")
    args = ap.parse_args()

    for p in args.paths:
        path = Path(p)
        if not path.exists():
            log.warning("Skip (missing): %s", path)
            continue
        changed, before, after = retag(path)
        log.info("%s: %d subject changes", path.name, changed)
        subjects = sorted(set(before) | set(after))
        for s in subjects:
            b = before.get(s, 0)
            a = after.get(s, 0)
            if b != a:
                log.info("  %-14s: %d → %d", s, b, a)


if __name__ == "__main__":
    main()
