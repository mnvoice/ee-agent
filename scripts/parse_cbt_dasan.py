#!/usr/bin/env python3
"""
Parser for 다산에듀 CBT exam PDFs.

Extracts questions, choices, answers, and solutions from:
- 2026년 1회 (34 pages, single exam)
- 2025년 1-3회 (87 pages, three exams combined)

Output format matches existing questions_기출_*.json files.

Commands:
    estimate  -- show what will be parsed without writing files
    parse     -- parse and write JSON files to data/
    verify    -- check output quality of existing JSON files
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"

PDF_2026 = DATA_DIR / "전기기사필기과년도2026년 1회 전기기사 필기 CBT 기출문제.pdf"
PDF_2025 = DATA_DIR / "전기기사필기과년도2025년 전기기사 필기 CBT 기출문제(1-3회).pdf"

# Subject mapping: question number range -> subject name
SUBJECT_RANGES: list[tuple[range, str]] = [
    (range(1, 21), "전기자기학"),
    (range(21, 41), "전력공학"),
    (range(41, 61), "전기기기"),
    (range(61, 81), "회로이론"),
    (range(81, 101), "전기설비기술기준"),
]

# Circled number characters used as answer choices in question text
CHOICE_CHARS: dict[str, int] = {
    "①": 1,
    "②": 2,
    "③": 3,
    "④": 4,
}

# Watermark strings to strip from extracted text
WATERMARKS: list[str] = [
    "값진 노력속에 성장 중인 정우진님의 꿈을 응원합니다!!",
    "34359920 mnvoice@naver.com",
    "다산에듀 www.e-dasan.net",
    "(주)다산에듀 All rights reserved.",
]

# Regex: question start line like "01. " or "1. "
Q_START_RE = re.compile(r"^(0?\d{1,2}|1\d{2})\.\s*(.*)", re.MULTILINE)

# Regex: explanation header line like "01. ④" or "1. ④"
EXP_HEADER_RE = re.compile(r"^(0?\d{1,2}|1\d{2})\.\s*([①②③④])\s*$")

# Regex: subject header in explanations like "[제1과목. 전기자기학]"
SUBJECT_HEADER_RE = re.compile(r"\[제\d+과목")

# Regex: page header like "2026년 1회 전기기사"
PAGE_HEADER_RE = re.compile(r"^20\d\d년 \d회 전기기사")

# Regex: page footer like "다산에듀 www.e-dasan.net  | 1"
PAGE_FOOTER_RE = re.compile(r"다산에듀\s+www\.e-dasan\.net")


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class Question:
    year: int
    session: str
    q_no: int
    subject: str
    text: str
    choices: list[str] = field(default_factory=lambda: ["", "", "", ""])
    answer: int = 0
    solution: str = ""
    concept: list[str] = field(default_factory=list)
    difficulty: int = 0
    q_type: str = ""

    def to_dict(self) -> dict:
        return {
            "year": self.year,
            "session": self.session,
            "q_no": self.q_no,
            "subject": self.subject,
            "text": self.text,
            "choices": self.choices,
            "answer": self.answer,
            "solution": self.solution,
            "concept": self.concept,
            "difficulty": self.difficulty,
            "q_type": self.q_type,
        }


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def get_subject(q_no: int) -> str:
    """Return subject name for a given question number."""
    for r, name in SUBJECT_RANGES:
        if q_no in r:
            return name
    return "알 수 없음"


def normalize_q_no(raw: str) -> int:
    """Convert raw question number string (e.g. '01', '1') to int."""
    return int(raw.lstrip("0") or "0")


def clean_text(text: str) -> str:
    """
    Remove watermarks, page headers/footers, and normalize whitespace.
    Strips the personal watermark text unique to this user's copy.
    """
    for wm in WATERMARKS:
        text = text.replace(wm, "")

    lines = text.splitlines()
    cleaned: list[str] = []
    for line in lines:
        stripped = line.strip()
        # Skip page headers
        if PAGE_HEADER_RE.match(stripped):
            continue
        # Skip page footers (dasan URL lines)
        if PAGE_FOOTER_RE.search(stripped):
            continue
        # Skip [문제해설] and [제N과목...] markers in explanations
        if stripped in ("[문제해설]", "[정답]"):
            continue
        if SUBJECT_HEADER_RE.match(stripped):
            continue
        cleaned.append(line)

    return "\n".join(cleaned)


def is_noise_line(line: str) -> bool:
    """Return True for lines that should be ignored in question text."""
    s = line.strip()
    if not s:
        return True
    for wm in WATERMARKS:
        if wm in s:
            return True
    if PAGE_FOOTER_RE.search(s):
        return True
    if PAGE_HEADER_RE.match(s):
        return True
    return False


# ---------------------------------------------------------------------------
# Answer grid parser (정답 page)
# ---------------------------------------------------------------------------

def parse_answer_grid(text: str) -> dict[int, int]:
    """
    Parse the [정답] grid page.

    The grid looks like:
        1  2  3  ...  10
        ④ ③ ④  ...  ④

    Returns {q_no: answer_int} mapping for all 100 questions.
    """
    answer_map: dict[int, int] = {}

    char_to_int: dict[str, int] = {"①": 1, "②": 2, "③": 3, "④": 4}

    # Only parse content after [정답] marker to avoid page header/footer numbers
    # being confused with question numbers
    marker = "[정답]"
    idx = text.find(marker)
    if idx >= 0:
        text = text[idx + len(marker):]

    # Stop at watermark section to avoid stray digits there
    for wm in WATERMARKS:
        wm_idx = text.find(wm)
        if wm_idx >= 0:
            text = text[:wm_idx]

    lines = text.splitlines()

    # Collect all tokens in order
    tokens: list[tuple[str, int]] = []
    for line in lines:
        for token in line.split():
            token = token.strip()
            # Use isascii() to exclude circled numbers like ①②③④ which
            # also return True for isdigit() in Python's Unicode handling
            if token.isascii() and token.isdigit() and 1 <= int(token) <= 100:
                tokens.append(("q", int(token)))
            elif token in char_to_int:
                tokens.append(("a", char_to_int[token]))

    # Pair blocks of question numbers with blocks of answers
    i = 0
    while i < len(tokens):
        q_block: list[int] = []
        while i < len(tokens) and tokens[i][0] == "q":
            q_block.append(tokens[i][1])
            i += 1
        a_block: list[int] = []
        while i < len(tokens) and tokens[i][0] == "a":
            a_block.append(tokens[i][1])
            i += 1
        for q, a in zip(q_block, a_block):
            answer_map[q] = a

    return answer_map


# Regex to detect and split inline multi-choice line:
#   "① text  ② text  ③ text  ④ text"
# We split on each marker character that is preceded by whitespace
_INLINE_CHOICE_SPLIT_RE = re.compile(r"(?:^|(?<=\s))([①②③④])\s*")


def _parse_inline_choices(line: str) -> dict[int, str]:
    """
    Parse a line that may contain multiple choices like:
        "① 1.2       ② 1.3       ③ 1.5       ④ 1.7"

    Returns {choice_num: text} dict if multiple markers found, else empty dict.
    Single-marker lines (normal choice lines) return empty dict.
    """
    markers = list(_INLINE_CHOICE_SPLIT_RE.finditer(line))
    if len(markers) < 2:
        return {}

    result: dict[int, str] = {}
    for i, m in enumerate(markers):
        choice_num = CHOICE_CHARS[m.group(1)]
        start = m.end()
        end = markers[i + 1].start() if i + 1 < len(markers) else len(line)
        text = line[start:end].strip()
        result[choice_num] = text

    return result


# ---------------------------------------------------------------------------
# Question text parser
# ---------------------------------------------------------------------------

def parse_questions_from_text(
    text: str,
    year: int,
    session: str,
    answer_grid: dict[int, int],
) -> list[Question]:
    """
    Parse all questions from concatenated question-page text.

    Handles:
    - 2-column layout (PyMuPDF join column order is fine for line-based parsing)
    - Question numbers with or without leading zero: "01." and "1."
    - Choices marked with ①②③④
    - Continuation lines for both question text and choice text
    """
    questions: list[Question] = []
    lines = text.splitlines()

    # Find all question start positions
    q_starts: list[tuple[int, int, str]] = []  # (line_idx, q_no, first_text)
    seen_q_nos: set[int] = set()

    for idx, line in enumerate(lines):
        if is_noise_line(line):
            continue
        m = Q_START_RE.match(line)
        if m:
            q_no = normalize_q_no(m.group(1))
            if 1 <= q_no <= 100 and q_no not in seen_q_nos:
                seen_q_nos.add(q_no)
                q_starts.append((idx, q_no, m.group(2).strip()))

    if not q_starts:
        log.warning("No questions found in text block")
        return []

    # Parse each question block
    for i, (line_idx, q_no, first_text) in enumerate(q_starts):
        end_idx = q_starts[i + 1][0] if i + 1 < len(q_starts) else len(lines)
        block = lines[line_idx:end_idx]

        text_parts: list[str] = [first_text] if first_text else []
        choices: list[str] = ["", "", "", ""]
        state = "question"  # "question" | "choices"

        for bl in block[1:]:
            if is_noise_line(bl):
                continue
            stripped = bl.strip()
            if not stripped:
                continue

            # Check if this line contains multiple choices on a single line,
            # e.g. "① 1.2       ② 1.3       ③ 1.5       ④ 1.7"
            inline_choices = _parse_inline_choices(stripped)
            if inline_choices:
                state = "choices"
                for choice_num, choice_text in inline_choices.items():
                    if 1 <= choice_num <= 4:
                        choices[choice_num - 1] = choice_text
            # Check if it starts with a single choice marker
            elif stripped and stripped[0] in CHOICE_CHARS:
                state = "choices"
                choice_num = CHOICE_CHARS[stripped[0]]
                choice_text = stripped[1:].strip()
                if 1 <= choice_num <= 4:
                    choices[choice_num - 1] = choice_text
            else:
                if state == "question":
                    text_parts.append(stripped)
                elif state == "choices" and choices:
                    # Continuation of last non-empty choice
                    for ci in range(3, -1, -1):
                        if choices[ci]:
                            choices[ci] = (choices[ci] + " " + stripped).strip()
                            break

        q_text = " ".join(text_parts).strip()
        subject = get_subject(q_no)
        answer = answer_grid.get(q_no, 0)

        if answer == 0:
            log.warning("Q%d: answer not found in grid", q_no)

        questions.append(
            Question(
                year=year,
                session=session,
                q_no=q_no,
                subject=subject,
                text=q_text,
                choices=choices,
                answer=answer,
            )
        )

    questions.sort(key=lambda q: q.q_no)
    return questions


# ---------------------------------------------------------------------------
# Explanation parser
# ---------------------------------------------------------------------------

def parse_explanations(text: str) -> dict[int, str]:
    """
    Parse solution text for each question from the explanation section.

    Explanation lines look like:
        01. ④
        쿨롱의 법칙 (점전하에 의한 힘)
        ...
        02. ③
        전위계수
        ...

    Returns {q_no: solution_text} mapping.
    """
    explanations: dict[int, str] = {}
    lines = text.splitlines()

    current_q_no: Optional[int] = None
    current_lines: list[str] = []

    def flush() -> None:
        if current_q_no is not None:
            sol = "\n".join(current_lines).strip()
            # Remove trailing glyphs-only lines (math formulas lost to encoding)
            sol_lines = sol.splitlines()
            # Keep lines that have at least one Korean char or useful ASCII
            kept: list[str] = []
            for sl in sol_lines:
                # Keep if contains Korean, Latin letters/digits, or common symbols
                if re.search(r"[가-힣a-zA-Z0-9\[\](){}.,:;=+\-×÷∴∵°※%]", sl):
                    kept.append(sl)
            explanations[current_q_no] = "\n".join(kept).strip()

    for line in lines:
        stripped = line.strip()

        # Skip noise
        if not stripped:
            continue
        if is_noise_line(line):
            continue
        if stripped in ("[문제해설]", "[정답]"):
            continue
        if SUBJECT_HEADER_RE.match(stripped):
            continue
        if PAGE_HEADER_RE.match(stripped):
            continue

        # Check for explanation header: "01. ④"
        m = EXP_HEADER_RE.match(stripped)
        if m:
            flush()
            current_q_no = normalize_q_no(m.group(1))
            current_lines = []
            continue

        if current_q_no is not None:
            current_lines.append(stripped)

    flush()
    return explanations


# ---------------------------------------------------------------------------
# PDF section extractors
# ---------------------------------------------------------------------------

def extract_pages_text(pdf_path: Path, page_indices: list[int]) -> str:
    """Extract and clean text from specified 0-indexed pages."""
    doc = fitz.open(str(pdf_path))
    parts: list[str] = []
    for idx in page_indices:
        if 0 <= idx < len(doc):
            raw = doc[idx].get_text()
            parts.append(clean_text(raw))
    doc.close()
    return "\n".join(parts)


def find_answer_page_index(doc: fitz.Document, start: int, end: int) -> Optional[int]:
    """
    Find the [정답] page within page range [start, end).
    Returns 0-indexed page number or None.
    """
    for i in range(start, end):
        text = doc[i].get_text()
        if "[정답]" in text:
            return i
    return None


def find_explanation_start_index(doc: fitz.Document, start: int, end: int) -> Optional[int]:
    """
    Find first [문제해설] page within range.
    Returns 0-indexed page number or None.
    """
    for i in range(start, end):
        text = doc[i].get_text()
        if "[문제해설]" in text:
            return i
    return None


# ---------------------------------------------------------------------------
# Main parse function for a single exam within a PDF
# ---------------------------------------------------------------------------

def parse_exam(
    pdf_path: Path,
    year: int,
    session: str,
    q_page_start: int,   # 0-indexed, first question page
    q_page_end: int,     # 0-indexed, exclusive, last question page+1
    ans_page: int,       # 0-indexed answer grid page
    exp_page_start: int, # 0-indexed, first explanation page
    exp_page_end: int,   # 0-indexed, exclusive
) -> list[Question]:
    """
    Parse a single exam from a PDF.

    All page indices are 0-based (PyMuPDF convention).
    """
    log.info(
        "Parsing %d년 %s: q_pages=%d-%d, ans=%d, exp=%d-%d",
        year, session,
        q_page_start + 1, q_page_end,
        ans_page + 1,
        exp_page_start + 1, exp_page_end,
    )

    doc = fitz.open(str(pdf_path))

    # 1. Answer grid
    ans_text = doc[ans_page].get_text()
    answer_grid = parse_answer_grid(ans_text)
    log.info("  Answer grid: %d entries", len(answer_grid))

    # 2. Question pages
    q_parts = [clean_text(doc[i].get_text()) for i in range(q_page_start, q_page_end)]
    q_full_text = "\n".join(q_parts)

    questions = parse_questions_from_text(q_full_text, year, session, answer_grid)
    log.info("  Questions parsed: %d", len(questions))

    # 3. Explanation pages
    exp_parts = [clean_text(doc[i].get_text()) for i in range(exp_page_start, exp_page_end)]
    exp_full_text = "\n".join(exp_parts)

    explanations = parse_explanations(exp_full_text)
    log.info("  Explanations parsed: %d", len(explanations))

    # 4. Attach explanations to questions
    for q in questions:
        q.solution = explanations.get(q.q_no, "")

    doc.close()

    # Validate
    missing_answers = [q.q_no for q in questions if q.answer == 0]
    if missing_answers:
        log.warning("  Missing answers for: %s", missing_answers)

    empty_text = [q.q_no for q in questions if not q.text]
    if empty_text:
        log.warning("  Empty question text for: %s", empty_text)

    return questions


# ---------------------------------------------------------------------------
# Exam configurations
# ---------------------------------------------------------------------------

@dataclass
class ExamConfig:
    year: int
    session: str
    pdf_path: Path
    q_page_start: int   # 0-indexed
    q_page_end: int     # exclusive
    ans_page: int
    exp_page_start: int
    exp_page_end: int
    output_file: Path


def get_exam_configs() -> list[ExamConfig]:
    """
    Return exam configurations based on known PDF structure.

    2026년 1회 (34 pages total):
      p1-2: cover/TOC
      p3-14 (idx 2-13): questions
      p15 (idx 14): answer grid
      p16-34 (idx 15-33): explanations

    2025년 1-3회 (87 pages total):
      p1-2: cover/TOC
      1회: p3-15 (idx 2-14) questions, p16 (idx 15) answers, p17-29 (idx 16-28) exp
      2회: p30-41 (idx 29-40) questions, p42 (idx 41) answers, p43-55 (idx 42-54) exp
      3회: p56-67 (idx 55-66) questions, p68 (idx 67) answers, p69-87 (idx 68-86) exp
    """
    configs = [
        ExamConfig(
            year=2026,
            session="1회",
            pdf_path=PDF_2026,
            q_page_start=2,    # page 3
            q_page_end=14,     # through page 14 (exclusive = 14)
            ans_page=14,       # page 15
            exp_page_start=15, # page 16
            exp_page_end=34,   # through page 34
            output_file=DATA_DIR / "questions_기출_2026_1회.json",
        ),
        ExamConfig(
            year=2025,
            session="1회",
            pdf_path=PDF_2025,
            q_page_start=2,
            q_page_end=15,
            ans_page=15,
            exp_page_start=16,
            exp_page_end=29,
            output_file=DATA_DIR / "questions_기출_2025_1회.json",
        ),
        ExamConfig(
            year=2025,
            session="2회",
            pdf_path=PDF_2025,
            q_page_start=29,
            q_page_end=41,
            ans_page=41,
            exp_page_start=42,
            exp_page_end=55,
            output_file=DATA_DIR / "questions_기출_2025_2회.json",
        ),
        ExamConfig(
            year=2025,
            session="3회",
            pdf_path=PDF_2025,
            q_page_start=55,
            q_page_end=67,
            ans_page=67,
            exp_page_start=68,
            exp_page_end=87,
            output_file=DATA_DIR / "questions_기출_2025_3회.json",
        ),
    ]
    return configs


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_estimate() -> None:
    """Show what will be parsed without writing any files."""
    configs = get_exam_configs()

    for cfg in configs:
        if not cfg.pdf_path.exists():
            log.warning("PDF not found: %s", cfg.pdf_path)
            continue

        doc = fitz.open(str(cfg.pdf_path))
        total_pages = len(doc)

        # Count questions
        q_count = 0
        seen: set[int] = set()
        for page_idx in range(cfg.q_page_start, cfg.q_page_end):
            if page_idx >= total_pages:
                continue
            text = doc[page_idx].get_text()
            for m in Q_START_RE.finditer(text):
                q_no = normalize_q_no(m.group(1))
                if 1 <= q_no <= 100 and q_no not in seen:
                    seen.add(q_no)
                    q_count += 1

        # Check answer grid
        ans_text = doc[cfg.ans_page].get_text() if cfg.ans_page < total_pages else ""
        answer_grid = parse_answer_grid(ans_text)

        # Count explanations
        exp_count = 0
        for page_idx in range(cfg.exp_page_start, cfg.exp_page_end):
            if page_idx >= total_pages:
                continue
            text = doc[page_idx].get_text()
            for line in text.splitlines():
                if EXP_HEADER_RE.match(line.strip()):
                    exp_count += 1

        doc.close()

        print(
            f"\n{cfg.year}년 {cfg.session}"
            f"\n  PDF: {cfg.pdf_path.name}"
            f"\n  Q pages: {cfg.q_page_start + 1}-{cfg.q_page_end}"
            f"\n  Questions found: {q_count}"
            f"\n  Answer grid entries: {len(answer_grid)}"
            f"\n  Explanations found: {exp_count}"
            f"\n  Output: {cfg.output_file.name}"
        )

    total = sum(1 for cfg in configs if cfg.pdf_path.exists()) * 100
    print(f"\nExpected total questions: {total} (4 exams × 100)")


def cmd_parse() -> None:
    """Parse all exams and write JSON output files."""
    configs = get_exam_configs()
    total_written = 0

    for cfg in configs:
        if not cfg.pdf_path.exists():
            log.error("PDF not found: %s", cfg.pdf_path)
            continue

        questions = parse_exam(
            pdf_path=cfg.pdf_path,
            year=cfg.year,
            session=cfg.session,
            q_page_start=cfg.q_page_start,
            q_page_end=cfg.q_page_end,
            ans_page=cfg.ans_page,
            exp_page_start=cfg.exp_page_start,
            exp_page_end=cfg.exp_page_end,
        )

        records = [q.to_dict() for q in questions]

        with open(cfg.output_file, "w", encoding="utf-8") as f:
            json.dump(records, f, ensure_ascii=False, indent=2)

        log.info(
            "Wrote %d questions to %s",
            len(records),
            cfg.output_file.name,
        )
        total_written += len(records)

    print(f"\nTotal questions written: {total_written}")


def cmd_verify() -> None:
    """Check quality of existing output JSON files."""
    configs = get_exam_configs()
    all_ok = True

    for cfg in configs:
        if not cfg.output_file.exists():
            print(f"MISSING: {cfg.output_file.name}")
            all_ok = False
            continue

        with open(cfg.output_file, encoding="utf-8") as f:
            records: list[dict] = json.load(f)

        issues: list[str] = []

        # Check count
        if len(records) != 100:
            issues.append(f"Expected 100 questions, got {len(records)}")

        # Check required fields
        required = {"year", "session", "q_no", "subject", "text", "choices", "answer", "solution"}
        for rec in records:
            missing = required - rec.keys()
            if missing:
                issues.append(f"Q{rec.get('q_no','?')}: missing fields {missing}")
                break

        # Check question numbers are 1-100
        q_nos = sorted(r["q_no"] for r in records)
        expected = list(range(1, 101))
        if q_nos != expected:
            missing_nos = sorted(set(expected) - set(q_nos))
            extra_nos = sorted(set(q_nos) - set(expected))
            if missing_nos:
                issues.append(f"Missing q_nos: {missing_nos[:10]}")
            if extra_nos:
                issues.append(f"Extra q_nos: {extra_nos[:10]}")

        # Check answers are in 1-4 range
        bad_answers = [r["q_no"] for r in records if r["answer"] not in (1, 2, 3, 4)]
        if bad_answers:
            issues.append(f"Invalid answers at Q{bad_answers}")

        # Check choices have 4 items
        bad_choices = [r["q_no"] for r in records if len(r["choices"]) != 4]
        if bad_choices:
            issues.append(f"Wrong choice count at Q{bad_choices}")

        # Check empty question texts
        empty_texts = [r["q_no"] for r in records if not r.get("text", "").strip()]
        if empty_texts:
            issues.append(f"Empty question text at Q{empty_texts[:5]}")

        # Check subject distribution
        subject_counts: dict[str, int] = {}
        for r in records:
            s = r.get("subject", "?")
            subject_counts[s] = subject_counts.get(s, 0) + 1

        # Check solution coverage
        with_solution = sum(1 for r in records if r.get("solution", "").strip())
        solution_pct = with_solution / max(len(records), 1) * 100

        status = "OK" if not issues else "FAIL"
        if issues:
            all_ok = False

        print(f"\n{cfg.year}년 {cfg.session} [{status}]: {cfg.output_file.name}")
        print(f"  Questions: {len(records)}")
        print(f"  Subject distribution: {subject_counts}")
        print(f"  Solutions: {with_solution}/{len(records)} ({solution_pct:.0f}%)")

        if issues:
            for issue in issues:
                print(f"  ISSUE: {issue}")

    print("\nOverall:", "PASS" if all_ok else "FAIL")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse 다산에듀 CBT PDF files into question JSON format.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "command",
        choices=["estimate", "parse", "verify"],
        help=(
            "estimate: show what will be parsed; "
            "parse: extract and save JSON files; "
            "verify: check quality of output files"
        ),
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    if args.command == "estimate":
        cmd_estimate()
    elif args.command == "parse":
        cmd_parse()
    elif args.command == "verify":
        cmd_verify()


if __name__ == "__main__":
    main()
