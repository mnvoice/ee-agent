#!/usr/bin/env python3
"""
CBT-format 전기기사 PDF parser.
Extracts questions, choices, and answers from CBT PDF files.
Supports cross-validation with answer key grid on the last page.
"""

import json
import re
import os
import sys
from pathlib import Path
from typing import Optional
import fitz  # PyMuPDF

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────

SUBJECT_MAP = {
    range(1, 21): "전기자기학",
    range(21, 41): "전력공학",
    range(41, 61): "전기기기",
    range(61, 81): "회로이론",
    range(81, 101): "전기설비기술기준",
}

# Unicode filled circles (correct answer marker)
FILLED_CIRCLES = {
    "\u2776": 1,  # ❶
    "\u2777": 2,  # ❷
    "\u2778": 3,  # ❸
    "\u2779": 4,  # ❹
}

# Unicode open circles (regular choice markers)
OPEN_CIRCLES = {
    "\u2460": 1,  # ①
    "\u2461": 2,  # ②
    "\u2462": 3,  # ③
    "\u2463": 4,  # ④
}

ALL_CIRCLES = {**FILLED_CIRCLES, **OPEN_CIRCLES}

# Answer map for digit strings
ANSWER_CHAR_MAP = {"①": 1, "②": 2, "③": 3, "④": 4,
                   "❶": 1, "❷": 2, "❸": 3, "❹": 4}


def get_subject(q_no: int) -> str:
    for r, subject in SUBJECT_MAP.items():
        if q_no in r:
            return subject
    return "알 수 없음"


# ──────────────────────────────────────────────
# Answer key extraction (last page)
# ──────────────────────────────────────────────

def extract_answer_key(text: str) -> dict[int, int]:
    """
    Parse the answer key grid from the last page.
    Handles both space-separated rows and single-entry-per-line formats.
    Returns {q_no: answer} dict.
    """
    answer_key = {}
    lines = text.strip().splitlines()

    answer_map = {"①": 1, "②": 2, "③": 3, "④": 4}

    # Collect all tokens that are either digits or answer chars in order
    # The grid appears as: q_num, q_num, ..., ans, ans, ... repeated
    all_tokens = []
    for line in lines:
        for token in line.split():
            token = token.strip()
            if token.isascii() and token.isdigit() and 1 <= int(token) <= 100:
                all_tokens.append(("q", int(token)))
            elif token in answer_map:
                all_tokens.append(("a", answer_map[token]))

    # Now pair them: a block of q nums followed by same-count answers
    i = 0
    while i < len(all_tokens):
        # Collect consecutive q nums
        q_block = []
        while i < len(all_tokens) and all_tokens[i][0] == "q":
            q_block.append(all_tokens[i][1])
            i += 1
        # Collect consecutive answers
        a_block = []
        while i < len(all_tokens) and all_tokens[i][0] == "a":
            a_block.append(all_tokens[i][1])
            i += 1
        # Pair them
        for q, a in zip(q_block, a_block):
            answer_key[q] = a

    return answer_key


# ──────────────────────────────────────────────
# Question block parsing
# ──────────────────────────────────────────────

# Regex to find question starts like "1. " or "12. " at line start
# Also handles image-only questions like "65.\xa0" (non-breaking space, no text)
Q_START_RE = re.compile(r"^(\d{1,3})\.\s*(.*)", re.MULTILINE)

# Choice line: starts with ①②③④❶❷❸❹ optionally preceded by spaces
CHOICE_LINE_RE = re.compile(r"^\s*([①②③④❶❷❸❹])\s*(.*)")


def parse_full_text(full_text: str) -> list[dict]:
    """
    Parse all question blocks from concatenated PDF text.
    Returns list of raw question dicts.
    """
    questions = []

    # Split text into lines for line-by-line processing
    lines = full_text.splitlines()

    # Find all question start positions
    q_starts = []
    for i, line in enumerate(lines):
        m = Q_START_RE.match(line)
        if m:
            q_no = int(m.group(1))
            # Filter out noise (valid range 1-100)
            if 1 <= q_no <= 100:
                q_starts.append((i, q_no, m.group(2).strip()))

    # Remove duplicate q_no (keep first occurrence in order)
    seen = set()
    unique_starts = []
    for item in q_starts:
        if item[1] not in seen:
            seen.add(item[1])
            unique_starts.append(item)

    # For each question, collect lines until next question
    for idx, (line_i, q_no, first_line) in enumerate(unique_starts):
        if idx + 1 < len(unique_starts):
            end_line = unique_starts[idx + 1][0]
        else:
            end_line = len(lines)

        block_lines = lines[line_i:end_line]
        q_text_parts = [first_line]
        choices_raw = []
        answer = None

        state = "question"  # states: question, choices

        for bl in block_lines[1:]:
            cm = CHOICE_LINE_RE.match(bl)
            if cm:
                state = "choices"
                marker = cm.group(1)
                choice_text = cm.group(2).strip()
                choice_num = ALL_CIRCLES.get(marker, 0)
                if marker in FILLED_CIRCLES:
                    answer = FILLED_CIRCLES[marker]
                choices_raw.append((choice_num, choice_text, marker in FILLED_CIRCLES))
            else:
                if state == "question":
                    stripped = bl.strip()
                    # Skip header lines (CBT website, date lines)
                    if (stripped and
                            "www.comcbt.com" not in stripped and
                            "전자문제집" not in stripped and
                            "최강 자격증" not in stripped and
                            "전기기사" not in stripped):
                        q_text_parts.append(stripped)
                else:
                    # Could be continuation of last choice
                    stripped = bl.strip()
                    if (stripped and
                            choices_raw and
                            "www.comcbt.com" not in stripped and
                            "전자문제집" not in stripped and
                            "최강 자격증" not in stripped and
                            "전기기사" not in stripped):
                        # Append to last choice
                        last = choices_raw[-1]
                        choices_raw[-1] = (last[0], (last[1] + " " + stripped).strip(), last[2])

        # Build q_text
        q_text = " ".join(q_text_parts).strip()

        # Build choices list (4 items, index by choice_num)
        choices = ["", "", "", ""]
        for (cnum, ctext, _) in choices_raw:
            if 1 <= cnum <= 4:
                choices[cnum - 1] = ctext

        questions.append({
            "q_no": q_no,
            "text": q_text,
            "choices": choices,
            "answer_inline": answer,
        })

    return questions


# ──────────────────────────────────────────────
# PDF extraction
# ──────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> tuple[str, str]:
    """
    Returns (question_pages_text, last_page_text).
    """
    doc = fitz.open(pdf_path)
    total = len(doc)

    question_texts = []
    for i in range(total - 1):  # all but last
        page = doc[i]
        question_texts.append(page.get_text())

    last_text = doc[total - 1].get_text()
    doc.close()

    return "\n".join(question_texts), last_text


# ──────────────────────────────────────────────
# Main parser
# ──────────────────────────────────────────────

def parse_pdf(pdf_path: str, year: int, session: str) -> list[dict]:
    """
    Full parse pipeline: extract -> parse -> validate -> build output.
    """
    print(f"\n[parse_pdf] Processing: {pdf_path}")
    print(f"  Year={year}, Session={session}")

    q_text, last_text = extract_text_from_pdf(pdf_path)

    # Extract answer key from last page
    answer_key = extract_answer_key(last_text)
    print(f"  Answer key extracted: {len(answer_key)} entries")

    # Parse questions
    raw_questions = parse_full_text(q_text)
    print(f"  Raw questions parsed: {len(raw_questions)}")

    # Build final records
    results = []
    mismatch_count = 0

    for q in raw_questions:
        q_no = q["q_no"]
        subject = get_subject(q_no)

        # Determine answer
        inline_ans = q["answer_inline"]
        key_ans = answer_key.get(q_no)

        if inline_ans and key_ans:
            if inline_ans != key_ans:
                print(f"  [WARN] Q{q_no}: inline={inline_ans}, key={key_ans} -> using key")
                mismatch_count += 1
            answer = key_ans
        elif key_ans:
            answer = key_ans
        elif inline_ans:
            answer = inline_ans
        else:
            answer = 0
            print(f"  [WARN] Q{q_no}: no answer found")

        results.append({
            "year": year,
            "session": session,
            "subject": subject,
            "q_no": q_no,
            "text": q["text"],
            "choices": q["choices"],
            "answer": answer,
            "solution": "",
            "concept": [],
            "difficulty": "",
            "q_type": "",
        })

    print(f"  Answer mismatches (key used): {mismatch_count}")
    print(f"  Final records: {len(results)}")

    # Sort by q_no
    results.sort(key=lambda x: x["q_no"])

    return results


# ──────────────────────────────────────────────
# Concept tagging with Haiku
# ──────────────────────────────────────────────

def load_concept_mapping(mapping_path: str) -> dict:
    """Load full_concept_mapping.json and build subject -> [concept names] map."""
    with open(mapping_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    concept_map = {}
    for subject, entries in raw.items():
        names = []
        for entry in entries:
            if isinstance(entry, dict) and "name" in entry:
                names.append(entry["name"])
            elif isinstance(entry, str):
                names.append(entry)
        concept_map[subject] = names

    return concept_map


def tag_concepts_haiku(questions: list[dict], concept_map: dict, api_key: str) -> list[dict]:
    """
    Use Claude Haiku to tag up to 3 concepts per question.
    Processes in batches to reduce API calls.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    BATCH_SIZE = 10

    tagged = list(questions)  # copy

    print(f"\n[tag_concepts] Tagging {len(tagged)} questions with Haiku...")

    for batch_start in range(0, len(tagged), BATCH_SIZE):
        batch = tagged[batch_start:batch_start + BATCH_SIZE]

        # Build prompt
        prompt_lines = []
        for q in batch:
            subject = q["subject"]
            concepts = concept_map.get(subject, [])
            concept_list_str = ", ".join(concepts[:80])  # limit to avoid token overflow

            prompt_lines.append(
                f"Q{q['q_no']} [{subject}]: {q['text']}\n"
                f"Available concepts: {concept_list_str}"
            )

        prompt = (
            "For each question below, select up to 3 most relevant concepts from the available concept list.\n"
            "Return ONLY a JSON object mapping question numbers to arrays of concept names.\n"
            "Example: {\"1\": [\"개념A\", \"개념B\"], \"2\": [\"개념C\"]}\n\n"
            + "\n\n".join(prompt_lines)
        )

        try:
            response = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.content[0].text.strip()

            # Extract JSON from response
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                concept_assignments = json.loads(json_match.group())
                for q in batch:
                    key = str(q["q_no"])
                    if key in concept_assignments:
                        q["concept"] = concept_assignments[key][:3]
            else:
                print(f"  [WARN] Could not parse JSON for batch starting at Q{batch[0]['q_no']}")

            print(f"  Tagged Q{batch[0]['q_no']}-Q{batch[-1]['q_no']} ({len(batch)} questions)")

        except Exception as e:
            print(f"  [ERROR] Haiku API error for batch {batch_start}: {e}")

    return tagged


# ──────────────────────────────────────────────
# Obsidian output
# ──────────────────────────────────────────────

CHOICE_LABELS = ["①", "②", "③", "④"]


def questions_to_obsidian_main(
    questions: list[dict], year: int, session: str, vault_base: str
) -> str:
    """
    Create main overview Obsidian file for a session.
    Returns the file path.
    """
    subjects = ["전기자기학", "전력공학", "전기기기", "회로이론", "전기설비기술기준"]
    session_tag = f"{year}_{session}"

    lines = [
        "---",
        "tags:",
        "  - 전기기사/기출",
        f"  - 전기기사/{session_tag}",
    ]
    for subj in subjects:
        lines.append(f"  - 전기기사/{subj}")
    lines += [
        "  - 학습상태/미숙",
        "---",
        "",
        f"# 전기기사 기출문제 {year}년 {session}",
        "",
        "## 과목별 문제",
        "",
    ]

    for subj in subjects:
        subj_qs = [q for q in questions if q["subject"] == subj]
        lines.append(f"### {subj} ({len(subj_qs)}문제)")
        lines.append("")
        for q in subj_qs:
            link = f"[[{session_tag}/{subj}/Q{q['q_no']:03d}]]"
            lines.append(f"- {link} {q['text'][:40]}...")
        lines.append("")

    content = "\n".join(lines)

    out_dir = Path(vault_base) / "기출문제"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{session_tag}.md"
    out_path.write_text(content, encoding="utf-8")
    print(f"  Saved: {out_path}")
    return str(out_path)


def questions_to_obsidian_subject(
    questions: list[dict], year: int, session: str, vault_base: str
) -> list[str]:
    """
    Create one Obsidian file per question under subject subdirectory.
    Returns list of file paths.
    """
    session_tag = f"{year}_{session}"
    saved_paths = []

    for q in questions:
        subj = q["subject"]
        q_no = q["q_no"]

        answer_idx = q["answer"] - 1 if 1 <= q["answer"] <= 4 else -1

        choice_lines = []
        for i, choice_text in enumerate(q["choices"]):
            marker = CHOICE_LABELS[i]
            prefix = "**" if i == answer_idx else ""
            suffix = "**" if i == answer_idx else ""
            choice_lines.append(f"- {prefix}{marker} {choice_text}{suffix}")

        concepts = q.get("concept", [])
        concept_str = ", ".join(concepts) if concepts else ""

        lines = [
            "---",
            "tags:",
            "  - 전기기사/기출",
            f"  - 전기기사/{session_tag}",
            f"  - 전기기사/{subj}",
            "  - 학습상태/미숙",
            "---",
            "",
            f"# Q{q_no:03d}. {q['text']}",
            "",
            "## 선택지",
            "",
        ]
        lines.extend(choice_lines)
        lines += [
            "",
            f"**정답:** {q['answer']}번",
            "",
        ]
        if concept_str:
            lines += [
                "## 관련 개념",
                "",
                concept_str,
                "",
            ]
        if q.get("solution"):
            lines += [
                "## 해설",
                "",
                q["solution"],
                "",
            ]

        content = "\n".join(lines)

        out_dir = Path(vault_base) / "기출문제" / session_tag / subj
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / f"Q{q_no:03d}.md"
        out_path.write_text(content, encoding="utf-8")
        saved_paths.append(str(out_path))

    print(f"  Saved {len(saved_paths)} subject files for {session_tag}")
    return saved_paths


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────

def main():
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"
    vault_base = Path("/Users/jeong-ujin_1/Documents/Obsidian Vault")

    # Load API key
    env_path = project_root / "claude_api.env"
    api_key = None
    if env_path.exists():
        from dotenv import load_dotenv
        load_dotenv(env_path)
        api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("[WARN] ANTHROPIC_API_KEY not found, skipping concept tagging")

    # Load concept mapping
    concept_map_path = data_dir / "full_concept_mapping.json"
    concept_map = load_concept_mapping(str(concept_map_path))
    print(f"Loaded concept mapping: {sum(len(v) for v in concept_map.values())} total concepts across {len(concept_map)} subjects")

    # Define targets
    targets = [
        {
            "pdf": data_dir / "20200424_1회.pdf",
            "year": 2020,
            "session": "1회",
            "out_json": data_dir / "questions_기출_2020_1회.json",
        },
        {
            "pdf": data_dir / "20220305_2회.pdf",
            "year": 2022,
            "session": "2회",
            "out_json": data_dir / "questions_기출_2022_2회.json",
        },
    ]

    summary = []

    for target in targets:
        year = target["year"]
        session = target["session"]
        pdf_path = str(target["pdf"])
        out_json = target["out_json"]

        # ── Step 1: Parse PDF ──
        questions = parse_pdf(pdf_path, year, session)
        answers_confirmed = sum(1 for q in questions if q["answer"] > 0)
        print(f"  Answers confirmed: {answers_confirmed}/{len(questions)}")

        # ── Step 2: Concept tagging ──
        concepts_tagged = 0
        if api_key:
            questions = tag_concepts_haiku(questions, concept_map, api_key)
            concepts_tagged = sum(1 for q in questions if q["concept"])
        print(f"  Concepts tagged: {concepts_tagged}/{len(questions)}")

        # ── Step 3: Save JSON ──
        with open(out_json, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
        print(f"  JSON saved: {out_json}")

        # ── Step 4: Save Obsidian ──
        questions_to_obsidian_main(questions, year, session, str(vault_base))
        questions_to_obsidian_subject(questions, year, session, str(vault_base))

        summary.append({
            "file": f"{year}_{session}",
            "total_questions": len(questions),
            "answers_confirmed": answers_confirmed,
            "concepts_tagged": concepts_tagged,
        })

    # ── Final summary ──
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    for s in summary:
        print(f"\n{s['file']}:")
        print(f"  Total questions  : {s['total_questions']}")
        print(f"  Answers confirmed: {s['answers_confirmed']}")
        print(f"  Concepts tagged  : {s['concepts_tagged']}")
    print()


if __name__ == "__main__":
    main()
