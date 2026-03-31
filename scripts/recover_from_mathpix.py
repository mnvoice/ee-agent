#!/usr/bin/env python3
"""
Recover incomplete questions from Mathpix OCR data.
Parses mathpix_기출_*.json files and fills gaps in questions_기출_*.json.
Cost: $0 (no API calls needed).
"""
import json
import glob
import logging
import os
import re
from typing import Optional

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Subject mapping by question number range (1-indexed, 20 per subject)
SUBJECT_MAP = {
    range(1, 21): "전기자기학",
    range(21, 41): "전력공학",
    range(41, 61): "전기기기",
    range(61, 81): "회로이론",
    range(81, 101): "전기설비기술기준",
}


def get_subject(qnum: int) -> str:
    for r, subj in SUBJECT_MAP.items():
        if qnum in r:
            return subj
    return "unknown"


def parse_mathpix_text(pages: list[dict]) -> list[dict]:
    """Parse Mathpix page text into structured questions."""
    all_text = "\n".join(p["text"] for p in pages)

    # Find all question positions
    q_pattern = re.compile(r'문제\s*(\d+)\s*')
    q_matches = list(q_pattern.finditer(all_text))

    if not q_matches:
        return []

    questions = []
    for i, match in enumerate(q_matches):
        qnum = int(match.group(1))
        start = match.end()
        end = q_matches[i + 1].start() if i + 1 < len(q_matches) else len(all_text)

        block = all_text[start:end].strip()
        parsed = parse_question_block(qnum, block)
        if parsed:
            questions.append(parsed)

    return questions


def parse_question_block(qnum: int, block: str) -> Optional[dict]:
    """Parse a single question block into structured data."""
    # Split into pre-solution and solution parts
    solution_split = re.split(r'\n\s*풀이\s*\n?', block, maxsplit=1)
    main_part = solution_split[0].strip()
    solution = solution_split[1].strip() if len(solution_split) > 1 else ""

    # Extract answer from solution or end of block
    answer = extract_answer(solution if solution else block)

    # Extract choices from main part
    choices, text_before_choices = extract_choices(main_part)

    if not text_before_choices:
        return None

    return {
        "number": qnum,
        "subject": get_subject(qnum),
        "text": clean_text(text_before_choices),
        "choices": choices,
        "answer": answer,
        "solution": clean_text(solution) if solution else "",
    }


def extract_choices(text: str) -> tuple[list[str], str]:
    """Extract 4 choices and return (choices, text_before_choices)."""
    # Pattern: (1) ... (2) ... (3) ... (4) ...
    choice_pattern = re.compile(r'\(\s*([1-4])\s*\)\s*')
    matches = list(choice_pattern.finditer(text))

    if len(matches) < 4:
        return ["", "", "", ""], text

    choices = ["", "", "", ""]
    first_choice_pos = matches[0].start()
    text_before = text[:first_choice_pos].strip()

    # Group matches by choice number, take the last 4 valid ones
    choice_positions = []
    for m in matches:
        num = int(m.group(1))
        choice_positions.append((num, m.start(), m.end()))

    # Find the best set of 4 consecutive choices (1,2,3,4)
    for i in range(len(choice_positions)):
        if choice_positions[i][0] == 1:
            group = [choice_positions[i]]
            expected = 2
            for j in range(i + 1, len(choice_positions)):
                if choice_positions[j][0] == expected:
                    group.append(choice_positions[j])
                    expected += 1
                    if expected > 4:
                        break
            if len(group) == 4:
                text_before = text[:group[0][1]].strip()
                for idx, (num, start, end) in enumerate(group):
                    next_start = group[idx + 1][1] if idx + 1 < len(group) else len(text)
                    choices[num - 1] = text[end:next_start].strip()
                return choices, text_before

    return ["", "", "", ""], text


def extract_answer(text: str) -> int:
    """Extract answer number from solution text."""
    # Various OCR patterns for [답]
    answer_patterns = [
        r'\[(?:답|덥|담|닫)\]\s*\(?(\d)\)?',
        r'정답\s*[:\-]?\s*\(?(\d)\)?',
        r'∴\s*\(?(\d)\)?$',
        r'답\s*[:\-]?\s*\(?(\d)\)?',
    ]
    for pat in answer_patterns:
        m = re.search(pat, text)
        if m:
            ans = int(m.group(1))
            if ans in [1, 2, 3, 4]:
                return ans
    return 0


def clean_text(text: str) -> str:
    """Clean LaTeX artifacts for display."""
    # Remove excessive whitespace but preserve formula structure
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip()
    return text


def normalize_text(text: str) -> str:
    """Normalize text for comparison: remove whitespace, LaTeX, punctuation."""
    t = re.sub(r'\\\(.*?\\\)', '', text)  # remove inline LaTeX
    t = re.sub(r'\\\[.*?\\\]', '', t, flags=re.DOTALL)  # remove display LaTeX
    t = re.sub(r'[^\w가-힣]', '', t)  # keep only alphanumeric + Korean
    return t.lower()


def text_similarity(a: str, b: str) -> float:
    """Simple character-level Jaccard similarity."""
    na, nb = normalize_text(a), normalize_text(b)
    if not na or not nb:
        return 0.0
    sa, sb = set(na), set(nb)
    intersection = len(sa & sb)
    union = len(sa | sb)
    return intersection / union if union else 0.0


def is_incomplete(q: dict) -> bool:
    """Check if a question is incomplete."""
    text = q.get("text", "").strip()
    choices = q.get("choices", [])
    answer = q.get("answer", 0)
    has_text = bool(text) and len(text) > 10 and not re.match(r'^[룬분탄문]제?\s*\d', text)
    has_choices = choices and not all(not c.strip() for c in choices)
    has_answer = answer in [1, 2, 3, 4]
    return not (has_text and has_choices and has_answer)


def recover_questions() -> dict:
    """Main recovery: rebuild from Mathpix, preserving enrichment from existing data."""
    stats = {"files_processed": 0, "recovered": 0, "failed": 0, "already_complete": 0}

    q_files = sorted(glob.glob(os.path.join(DATA_DIR, "questions_기출_*.json")))

    for q_file in q_files:
        fname = os.path.basename(q_file)
        match = re.search(r'questions_기출_(\d+)_(\d+회)', fname)
        if not match:
            continue

        year = int(match.group(1))
        session = match.group(2)
        year_session = f"{year}_{session}"
        mathpix_file = os.path.join(DATA_DIR, f"mathpix_기출_{year_session}.json")

        if not os.path.exists(mathpix_file):
            continue

        # Load existing questions
        with open(q_file, "r", encoding="utf-8") as f:
            existing = json.load(f)

        incomplete_count = sum(1 for q in existing if is_incomplete(q))
        if incomplete_count == 0:
            continue

        # Parse Mathpix
        with open(mathpix_file, "r", encoding="utf-8") as f:
            pages = json.load(f)

        parsed = parse_mathpix_text(pages)
        if not parsed:
            logger.warning("  %s: Mathpix parsing failed", year_session)
            continue

        parsed_by_num = {q["number"]: q for q in parsed}

        # Strategy: match complete existing questions to Mathpix by text similarity
        # Then fill remaining positions from Mathpix
        matched_nums = set()
        existing_by_match = {}

        # Step 1: Match complete existing questions to Mathpix numbers
        for q in existing:
            if is_incomplete(q):
                continue
            best_score = 0.0
            best_num = None
            q_text = q.get("text", "")
            for num, mp in parsed_by_num.items():
                if num in matched_nums:
                    continue
                # Also check subject compatibility
                mp_subject = get_subject(num)
                if q.get("subject") and q["subject"] != mp_subject:
                    continue
                score = text_similarity(q_text, mp["text"])
                if score > best_score:
                    best_score = score
                    best_num = num
            if best_num and best_score > 0.3:
                matched_nums.add(best_num)
                existing_by_match[best_num] = q

        # Step 2: Build final question list from Mathpix, merging existing enrichment
        rebuilt = []
        file_recovered = 0

        for num in sorted(parsed_by_num.keys()):
            mp = parsed_by_num[num]

            if num in existing_by_match:
                # Keep existing complete question, just add number
                eq = existing_by_match[num]
                eq["number"] = num
                rebuilt.append(eq)
                stats["already_complete"] += 1
            else:
                # Use Mathpix data for this question
                new_q = {
                    "year": year,
                    "session": session,
                    "subject": get_subject(num),
                    "number": num,
                    "text": mp["text"],
                    "choices": mp["choices"],
                    "answer": mp["answer"],
                }
                if mp.get("solution"):
                    new_q["solution"] = mp["solution"]

                # Try to find enrichment from existing incomplete questions
                # Match by tag if available (same subject, similar position)
                for eq in existing:
                    if eq.get("subject") == new_q["subject"] and eq.get("tag"):
                        eq_text = eq.get("text", "")
                        if text_similarity(eq_text, mp["text"]) > 0.25:
                            new_q["tag"] = eq["tag"]
                            for field in ("steps", "figure_svg", "solution_svg"):
                                if eq.get(field):
                                    new_q[field] = eq[field]
                            break

                if new_q["text"] and any(new_q["choices"]):
                    rebuilt.append(new_q)
                    file_recovered += 1
                    stats["recovered"] += 1
                else:
                    stats["failed"] += 1

        if file_recovered > 0:
            with open(q_file, "w", encoding="utf-8") as f:
                json.dump(rebuilt, f, ensure_ascii=False, indent=2)
            logger.info("  %s: %d recovered, %d kept (%d total)",
                        year_session, file_recovered,
                        len(rebuilt) - file_recovered, len(rebuilt))
            stats["files_processed"] += 1

    return stats


if __name__ == "__main__":
    logger.info("Starting Mathpix recovery...")
    logger.info("")

    stats = recover_questions()

    logger.info("")
    logger.info("=" * 50)
    logger.info("RECOVERY COMPLETE")
    logger.info("=" * 50)
    logger.info("Files processed: %d", stats["files_processed"])
    logger.info("Questions recovered: %d", stats["recovered"])
    logger.info("Failed (no match): %d", stats["failed"])
    logger.info("Skipped (already ok): %d", stats["skipped"])
