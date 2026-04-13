#!/usr/bin/env python3
"""
전기기사 기출문제 PDF 일괄 처리 파이프라인.

Task A: 이미지 기반 기출 PDF → Mathpix OCR → 파싱 → Claude Haiku 태깅 → JSON + Obsidian
Task B: CBT 텍스트 기반 JSON (solution="" 항목) → Claude Haiku 풀이 생성

Usage:
    python scripts/batch_gichul_pipeline.py [--start-year YYYY] [--end-year YYYY] [--skip-ocr]
"""

import argparse
import base64
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from typing import Optional

import requests
import fitz  # PyMuPDF

# ── Project root & paths ──────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
VAULT_BASE = Path("/Users/jeong-ujin_1/Documents/Obsidian Vault")

PROGRESS_FILE = DATA_DIR / "batch_progress.json"
ERROR_LOG_FILE = DATA_DIR / "batch_errors.json"
CONCEPT_MAP_FILE = DATA_DIR / "full_concept_mapping.json"

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


# ── Subject map (fallback only) ───────────────────────────────────────────────
# Used when keyword detection fails. Splits Q61~80 into 회로이론 + 제어공학 —
# this is the canonical layout for the 전기기사 필기 exam. Previous map lumped
# Q61~80 into 회로이론 and excluded 제어공학 entirely.
SUBJECT_MAP: list[tuple[range, str]] = [
    (range(1, 21), "전기자기학"),
    (range(21, 41), "전력공학"),
    (range(41, 61), "전기기기"),
    (range(61, 71), "회로이론"),
    (range(71, 81), "제어공학"),
    (range(81, 101), "전기설비기술기준"),
]


# Lazy-init parser; instantiating Komoran is expensive.
_PARSER: "KoreanQuestionParser | None" = None


def _get_parser() -> "KoreanQuestionParser":
    global _PARSER
    if _PARSER is None:
        from ee_agent.ingestion.korean_parser import KoreanQuestionParser

        _PARSER = KoreanQuestionParser()
    return _PARSER


def get_subject(q_no: int, text: str = "") -> str:
    """Classify subject with keyword-first, number-range fallback.

    1. Keyword match via KoreanQuestionParser.detect_subject_by_keyword
    2. Fallback to SUBJECT_MAP number range when no keyword matches
    3. "기타" when neither works
    """
    if text:
        try:
            subj = _get_parser().detect_subject_by_keyword(text)
            if subj is not None:
                return subj.value
        except Exception as exc:  # pragma: no cover
            log.debug("Keyword-based subject detection failed: %s", exc)

    for r, subj_name in SUBJECT_MAP:
        if q_no in r:
            return subj_name
    return "기타"


# ── Regex patterns ────────────────────────────────────────────────────────────
Q_RE = re.compile(r"문제\s*(\d{1,3})\s")
ANS_RE = re.compile(
    r"[【\[［]\s*[딥답덥]\s*[】\]］]"
    r"|\s*[（(]\s*([1-4①②③④])\s*[）)]"
)
ANS_CLEAN_RE = re.compile(
    r"[【\[［]\s*[딥답덥][】\]］]\s*[（(]?\s*([1-4①②③④])\s*[）)]?"
)
CHOICE_NUM_MAP = {"①": 1, "②": 2, "③": 3, "④": 4,
                  "1": 1, "2": 2, "3": 3, "4": 4}


# ── Progress helpers ──────────────────────────────────────────────────────────
def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "errors": []}


def save_progress(progress: dict) -> None:
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def load_errors() -> list:
    if ERROR_LOG_FILE.exists():
        with open(ERROR_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_errors(errors: list) -> None:
    with open(ERROR_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(errors, f, ensure_ascii=False, indent=2)


# ── OCR cache helpers ─────────────────────────────────────────────────────────
def ocr_cache_path(year: int, session: str) -> Path:
    safe_session = session.replace(",", "_").replace(" ", "")
    return DATA_DIR / f"mathpix_기출_{year}_{safe_session}.json"


def load_ocr_cache(year: int, session: str) -> Optional[list[dict]]:
    path = ocr_cache_path(year, session)
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_ocr_cache(year: int, session: str, pages: list[dict]) -> None:
    path = ocr_cache_path(year, session)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)


# ── Environment loading ───────────────────────────────────────────────────────
def load_env() -> tuple[Optional[str], Optional[str], Optional[str]]:
    """Load ANTHROPIC_API_KEY, MATHPIX_APP_ID, MATHPIX_APP_KEY."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        log.warning("[WARN] python-dotenv not installed; reading env vars directly")
        load_dotenv = None  # type: ignore[assignment]

    claude_env = PROJECT_ROOT / "claude_api.env"
    mathpix_env = PROJECT_ROOT / "mathpix.env"

    if load_dotenv:
        if claude_env.exists():
            load_dotenv(claude_env, override=False)
        if mathpix_env.exists():
            load_dotenv(mathpix_env, override=False)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    app_id = os.getenv("APP_ID")
    app_key = os.getenv("APP_KEY")

    return api_key, app_id, app_key


# ── Mathpix OCR ───────────────────────────────────────────────────────────────
def ocr_page(img_bytes: bytes, app_id: str, app_key: str) -> tuple[str, float]:
    """OCR a single page image via Mathpix API."""
    b64 = base64.b64encode(img_bytes).decode()
    try:
        resp = requests.post(
            "https://api.mathpix.com/v3/text",
            json={
                "src": f"data:image/jpeg;base64,{b64}",
                "formats": ["text"],
                "text_formats": ["text"],
                "math_inline_delimiters": ["\\(", "\\)"],
                "math_display_delimiters": ["\\[", "\\]"],
            },
            headers={"app_id": app_id, "app_key": app_key},
            timeout=30,
        )
        data = resp.json()
        if "error" in data:
            log.warning(f"  Mathpix error: {data['error']}")
            return "", 0.0
        return data.get("text", ""), data.get("confidence", 0.0)
    except Exception as e:
        log.warning(f"  OCR request failed: {e}")
        return "", 0.0


def ocr_pdf(
    pdf_path: str,
    year: int,
    session: str,
    app_id: str,
    app_key: str,
    skip_ocr: bool = False,
) -> list[dict]:
    """
    OCR all pages of a PDF. Returns list of {page, text, confidence}.
    Uses cache if available.
    """
    cached = load_ocr_cache(year, session)
    if cached is not None:
        log.info(f"  OCR cache hit ({len(cached)} pages)")
        return cached

    if skip_ocr:
        log.warning("  --skip-ocr set and no cache found; returning empty pages")
        return []

    doc = fitz.open(pdf_path)
    total = len(doc)
    log.info(f"  OCR: {total} pages via Mathpix...")

    pages = []
    for i in range(total):
        page = doc[i]
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")

        text, confidence = ocr_page(img_bytes, app_id, app_key)
        pages.append({"page": i + 1, "text": text, "confidence": confidence})
        log.info(
            f"  Page {i+1}/{total} confidence={confidence:.3f} "
            f"chars={len(text)}"
        )
        time.sleep(1)  # Mathpix rate limit: max 1 req/sec

    doc.close()
    save_ocr_cache(year, session, pages)
    return pages


# ── OCR text parsing ──────────────────────────────────────────────────────────
def parse_ocr_pages(pages: list[dict]) -> list[dict]:
    """
    Parse OCR page texts into question records.
    Handles 문제 NN pattern; extracts choices and answer.
    """
    full_text = "\n".join(p["text"] for p in pages)
    return _parse_ocr_text(full_text)


def _parse_ocr_text(full_text: str) -> list[dict]:
    """Core OCR text parser."""
    questions: list[dict] = []

    # Find all question positions
    q_positions: list[tuple[int, int]] = []  # (char_pos, q_no)
    for m in Q_RE.finditer(full_text):
        q_no = int(m.group(1))
        if 1 <= q_no <= 100:
            q_positions.append((m.start(), q_no))

    # Deduplicate by q_no (keep first occurrence)
    seen: set[int] = set()
    unique_positions: list[tuple[int, int]] = []
    for pos, q_no in q_positions:
        if q_no not in seen:
            seen.add(q_no)
            unique_positions.append((pos, q_no))

    for idx, (start_pos, q_no) in enumerate(unique_positions):
        end_pos = (
            unique_positions[idx + 1][0]
            if idx + 1 < len(unique_positions)
            else len(full_text)
        )
        block = full_text[start_pos:end_pos]

        # Remove "문제 NN" header
        block_body = re.sub(r"^문제\s*\d{1,3}\s*", "", block, count=1)

        # Extract answer from 【답】 or [답] marker
        answer = 0
        ans_match = re.search(
            r"[【\[]\s*[딥답덥][】\]]\s*[（(]?\s*([1-4①②③④])\s*[）)]?",
            block_body,
        )
        if ans_match:
            raw_ans = ans_match.group(1)
            answer = CHOICE_NUM_MAP.get(raw_ans, 0)

        # Extract solution: text between 풀이 and 【답】
        solution_text = ""
        sol_match = re.search(
            r"풀이\s*(.*?)\s*(?:[【\[]\s*[딥답덥][】\]]|$)",
            block_body,
            re.DOTALL,
        )
        if sol_match:
            solution_text = sol_match.group(1).strip()

        # Extract question text (before first choice marker or 풀이)
        q_body = re.split(r"\(1\)|\（1\）|풀이|【답】", block_body)[0].strip()
        # Remove trailing whitespace artifacts
        q_text = re.sub(r"\s{2,}", " ", q_body).strip()

        # Extract choices: (1) ... (2) ... (3) ... (4) ...
        choices = ["", "", "", ""]
        choice_pattern = re.compile(
            r"[（(]\s*([1-4])\s*[）)]\s*(.*?)(?=[（(][1-4][）)]|풀이|【답】|$)",
            re.DOTALL,
        )
        for cm in choice_pattern.finditer(block_body):
            cnum = int(cm.group(1)) - 1
            ctext = re.sub(r"\s{2,}", " ", cm.group(2)).strip()
            if 0 <= cnum <= 3:
                choices[cnum] = ctext

        questions.append(
            {
                "q_no": q_no,
                "text": q_text,
                "choices": choices,
                "answer": answer,
                "solution_ocr": solution_text,
            }
        )

    # Sort by q_no
    questions.sort(key=lambda x: x["q_no"])
    return questions


# ── Claude Haiku: tag + solution ──────────────────────────────────────────────
def build_haiku_client(api_key: str):
    import anthropic
    return anthropic.Anthropic(api_key=api_key)


def complete_question_with_haiku(
    questions: list[dict],
    concept_map: dict,
    api_key: str,
    batch_size: int = 5,
) -> list[dict]:
    """
    For each question, use Claude Haiku to:
    - Select up to 2 concepts from the subject concept list
    - Assign difficulty (1-5) and q_type
    - Write/complete the solution in Korean

    Returns the same list with solution, concept, difficulty, q_type filled.
    """
    client = build_haiku_client(api_key)
    result = list(questions)

    log.info(f"  Claude Haiku: tagging {len(result)} questions in batches of {batch_size}...")

    for batch_start in range(0, len(result), batch_size):
        batch = result[batch_start: batch_start + batch_size]
        batch_prompts: list[str] = []

        for q in batch:
            subj = q.get("subject", "")
            concepts = concept_map.get(subj, [])
            concept_list_str = ", ".join(concepts[:60])
            choices_text = "\n".join(
                f"  ({i+1}) {c}" for i, c in enumerate(q.get("choices", []))
            )
            sol_ocr = q.get("solution_ocr") or q.get("solution") or "없음"

            batch_prompts.append(
                f"Q{q['q_no']} [{subj}]\n"
                f"문제: {q['text']}\n"
                f"보기:\n{choices_text}\n"
                f"정답: {q.get('answer', 0)}번\n"
                f"풀이(OCR/기존): {sol_ocr[:500]}\n"
                f"사용 가능한 개념 목록: {concept_list_str}"
            )

        prompt = (
            "아래 전기기사 기출 문제들을 분석하여 JSON으로 반환하세요.\n"
            "각 문제에 대해 다음 필드를 채워주세요:\n"
            "- concept: 사용 가능한 개념 목록에서 핵심 개념 최대 2개 선택 (배열)\n"
            "- difficulty: 1-5 (1=쉬움, 5=어려움)\n"
            "- q_type: '계산형' or '암기형' or '개념형'\n"
            "- solution_complete: 완전한 한국어 풀이\n"
            "  (핵심 공식 제시, 단계별 계산 또는 개념 설명, 정답 도출 과정, 오답 이유 간단히)\n"
            "  수식은 LaTeX inline: \\( ... \\) 또는 display: \\[ ... \\] 형식 사용\n\n"
            "반환 형식 (Q번호 기준 객체):\n"
            '{"1": {"concept": ["개념A", "개념B"], "difficulty": 3, '
            '"q_type": "계산형", "solution_complete": "풀이 텍스트"}, ...}\n\n"'
            "---\n\n"
            + "\n\n---\n\n".join(batch_prompts)
        )

        for attempt in range(3):
            try:
                response = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=4096,
                    messages=[{"role": "user", "content": prompt}],
                )
                content = response.content[0].text.strip()

                # Extract JSON block
                json_match = re.search(r"\{.*\}", content, re.DOTALL)
                if not json_match:
                    raise ValueError("No JSON found in response")

                assignments = json.loads(json_match.group())

                for q in batch:
                    key = str(q["q_no"])
                    if key in assignments:
                        data = assignments[key]
                        q["concept"] = data.get("concept", [])[:2]
                        q["difficulty"] = data.get("difficulty", "")
                        q["q_type"] = data.get("q_type", "")
                        sol_complete = data.get("solution_complete", "")
                        if sol_complete:
                            q["solution"] = sol_complete
                        elif not q.get("solution"):
                            q["solution"] = q.get("solution_ocr", "")

                log.info(
                    f"  Haiku tagged Q{batch[0]['q_no']}-Q{batch[-1]['q_no']} "
                    f"({len(batch)} questions)"
                )
                break

            except Exception as e:
                if attempt < 2:
                    log.warning(f"  Haiku error (attempt {attempt+1}): {e}; retrying...")
                    time.sleep(1)
                else:
                    log.error(
                        f"  [ERROR] Haiku failed for batch Q{batch[0]['q_no']}-"
                        f"Q{batch[-1]['q_no']}: {e}"
                    )

        time.sleep(10)  # rate limit 대응 (10,000 tokens/min limit)

    return result


# ── Solution generation for CBT files ────────────────────────────────────────
def generate_solutions_for_cbt(
    json_path: Path,
    concept_map: dict,
    api_key: str,
) -> tuple[int, int]:
    """
    Load a CBT JSON, generate solutions for questions with solution=="".
    Returns (total_questions, solutions_generated).
    """
    with open(json_path, "r", encoding="utf-8") as f:
        questions: list[dict] = json.load(f)

    # Find questions needing solutions
    needs_solution = [q for q in questions if not q.get("solution")]
    total = len(questions)

    if not needs_solution:
        log.info(f"  All {total} questions already have solutions — skipping")
        return total, 0

    log.info(f"  Generating solutions for {len(needs_solution)}/{total} questions...")

    # Ensure solution_ocr field exists (for CBT questions it won't)
    for q in needs_solution:
        q.setdefault("solution_ocr", "")

    updated = complete_question_with_haiku(needs_solution, concept_map, api_key)

    # Merge back by q_no
    updated_map = {q["q_no"]: q for q in updated}
    for q in questions:
        if q["q_no"] in updated_map:
            upd = updated_map[q["q_no"]]
            q["solution"] = upd.get("solution", "")
            if upd.get("difficulty"):
                q["difficulty"] = upd["difficulty"]
            if upd.get("q_type"):
                q["q_type"] = upd["q_type"]
            # Preserve existing concept if already tagged
            if not q.get("concept") and upd.get("concept"):
                q["concept"] = upd["concept"]

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    solutions_generated = sum(1 for q in questions if q.get("solution"))
    return total, len(needs_solution)


# ── Obsidian output ───────────────────────────────────────────────────────────
CHOICE_LABELS = ["①", "②", "③", "④"]
STAR_MAP = {1: "★☆☆☆☆", 2: "★★☆☆☆", 3: "★★★☆☆", 4: "★★★★☆", 5: "★★★★★"}


def save_obsidian(questions: list[dict], year: int, session: str) -> None:
    """Create Obsidian index file and per-question files."""
    session_tag = f"{year}_{session}"
    subjects = ["전기자기학", "전력공학", "전기기기", "회로이론", "전기설비기술기준"]

    # Count stats
    n_total = len(questions)
    n_solutions = sum(1 for q in questions if q.get("solution"))
    n_tagged = sum(1 for q in questions if q.get("concept"))
    from datetime import date
    today = date.today().isoformat()

    # ── Index file ──
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
        f"created: {today}",
        "---",
        "",
        f"# {year}년 {session} 기출문제",
        "",
        f"총 {n_total}문제 | 풀이: {n_solutions}/{n_total} | 개념태깅: {n_tagged}/{n_total}",
        "",
        "## 과목별",
    ]
    for subj in subjects:
        subj_qs = [q for q in questions if q.get("subject") == subj]
        lines.append(f"- {subj}: {len(subj_qs)}문제")

    lines += [
        "",
        "## 문제 목록",
        "",
        "| 번호 | 과목 | 정답 | 개념 | 난이도 |",
        "|------|------|------|------|--------|",
    ]
    for q in questions:
        q_no = q["q_no"]
        subj = q.get("subject", "")
        answer = q.get("answer", 0)
        concept = ", ".join(q.get("concept", [])[:2]) if q.get("concept") else ""
        diff = q.get("difficulty", "")
        star = STAR_MAP.get(int(diff), "") if str(diff).isdigit() else ""
        lines.append(f"| Q{q_no:02d} | {subj} | {answer} | {concept} | {star} |")

    out_dir = VAULT_BASE / "기출문제"
    out_dir.mkdir(parents=True, exist_ok=True)
    index_path = out_dir / f"{session_tag}.md"
    index_path.write_text("\n".join(lines), encoding="utf-8")

    # ── Per-question files ──
    for q in questions:
        subj = q.get("subject", "기타")
        q_no = q["q_no"]
        answer_idx = q.get("answer", 0) - 1

        choice_lines = []
        for i, ct in enumerate(q.get("choices", [])):
            marker = CHOICE_LABELS[i] if i < 4 else f"({i+1})"
            bold = answer_idx == i
            prefix = "**" if bold else ""
            choice_lines.append(f"- {prefix}{marker} {ct}{'**' if bold else ''}")

        concepts = q.get("concept", [])
        diff = q.get("difficulty", "")
        star = STAR_MAP.get(int(diff), "") if str(diff).isdigit() else ""

        q_lines = [
            "---",
            "tags:",
            "  - 전기기사/기출",
            f"  - 전기기사/{session_tag}",
            f"  - 전기기사/{subj}",
            "  - 학습상태/미숙",
            "---",
            "",
            f"# Q{q_no:03d}. {q.get('text', '')}",
            "",
            "## 선택지",
            "",
        ]
        q_lines.extend(choice_lines)
        q_lines += [
            "",
            f"**정답:** {q.get('answer', 0)}번",
            "",
        ]
        if star:
            q_lines += [f"**난이도:** {star}", ""]
        if q.get("q_type"):
            q_lines += [f"**유형:** {q['q_type']}", ""]
        if concepts:
            q_lines += [
                "## 관련 개념",
                "",
                ", ".join(concepts),
                "",
            ]
        if q.get("solution"):
            q_lines += [
                "## 해설",
                "",
                q["solution"],
                "",
            ]

        q_dir = VAULT_BASE / "기출문제" / session_tag / subj
        q_dir.mkdir(parents=True, exist_ok=True)
        (q_dir / f"Q{q_no:03d}.md").write_text("\n".join(q_lines), encoding="utf-8")

    log.info(f"  Obsidian saved: {index_path} + {n_total} question files")


# ── PDF filename parsing ──────────────────────────────────────────────────────
def parse_pdf_filename(pdf_path: Path) -> Optional[tuple[int, str]]:
    """
    Extract (year, session) from PDF filename patterns:
    - 문제_YYYY_N회_...pdf
    - 문제 _YYYY_N회_...pdf
    - 문제YYYY_N회_...pdf
    - 문제_YYYY_N,M회_...pdf  → session="N,M회"
    """
    import unicodedata as _ud
    name = _ud.normalize("NFC", pdf_path.stem)  # macOS NFD → NFC

    # Skip duplicates: contains " (1)" etc.
    if re.search(r"\s*\(\d+\)\s*$", name):
        return None

    # Pattern: 문제[_optional space_]YYYY_N회
    m = re.search(r"문제\s*_?\s*(\d{4})_(.+회)", name)
    if m:
        year = int(m.group(1))
        session = m.group(2)
        return year, session

    return None


def collect_image_pdfs(
    data_dir: Path,
    start_year: int,
    end_year: int,
) -> list[tuple[Path, int, str]]:
    """
    Collect image-based 기출 PDFs sorted oldest→newest.
    Returns list of (pdf_path, year, session).
    """
    pdfs: list[tuple[Path, int, str]] = []
    # macOS NFD encoding: glob("문제*.pdf") fails; normalize to NFC before matching
    import unicodedata as _ud
    all_pdfs = sorted(
        p for p in data_dir.glob("*.pdf")
        if "문제" in _ud.normalize("NFC", p.name)
    )
    for pdf in all_pdfs:
        parsed = parse_pdf_filename(pdf)
        if parsed is None:
            continue
        year, session = parsed
        if not (start_year <= year <= end_year):
            continue
        pdfs.append((pdf, year, session))

    # Sort by year then session
    pdfs.sort(key=lambda x: (x[1], x[2]))
    return pdfs


# ── Load concept map ──────────────────────────────────────────────────────────
def load_concept_map() -> dict:
    with open(CONCEPT_MAP_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    result: dict = {}
    for subj, entries in raw.items():
        names = []
        for entry in entries:
            if isinstance(entry, dict) and "name" in entry:
                names.append(entry["name"])
            elif isinstance(entry, str):
                names.append(entry)
        result[subj] = names
    return result


# ── Pipeline: Task B (CBT solution generation) ────────────────────────────────
def run_task_b(concept_map: dict, api_key: str) -> dict:
    """Process CBT JSON files: generate solutions for empty solution fields."""
    cbt_files = [
        DATA_DIR / "questions_기출_2020_1회.json",
        DATA_DIR / "questions_기출_2022_2회.json",
    ]

    summary: dict = {
        "task_b_files": [],
        "task_b_total_questions": 0,
        "task_b_solutions_generated": 0,
    }

    for json_path in cbt_files:
        if not json_path.exists():
            log.warning(f"  CBT file not found: {json_path}")
            continue

        # Derive year/session from filename for Obsidian
        m = re.search(r"questions_기출_(\d{4})_(.+)\.json", json_path.name)
        if not m:
            continue
        year = int(m.group(1))
        session = m.group(2)

        log.info(f"\n[CBT] {json_path.name}")
        total, generated = generate_solutions_for_cbt(json_path, concept_map, api_key)

        # Reload and update Obsidian
        with open(json_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
        save_obsidian(questions, year, session)

        summary["task_b_files"].append(json_path.name)
        summary["task_b_total_questions"] += total
        summary["task_b_solutions_generated"] += generated

    return summary


# ── Pipeline: Task A (image PDF OCR + parse + tag) ────────────────────────────
def run_task_a(
    pdfs: list[tuple[Path, int, str]],
    concept_map: dict,
    api_key: Optional[str],
    app_id: Optional[str],
    app_key: Optional[str],
    skip_ocr: bool,
    progress: dict,
    errors: list,
) -> dict:
    """Process image-based PDFs."""
    summary: dict = {
        "task_a_processed": 0,
        "task_a_skipped": 0,
        "task_a_errors": 0,
        "task_a_total_questions": 0,
        "task_a_solutions": 0,
        "task_a_tagged": 0,
    }

    total_pdfs = len(pdfs)

    for i, (pdf_path, year, session) in enumerate(pdfs, 1):
        safe_session = session.replace(",", "_").replace(" ", "")
        exam_key = f"{year}_{safe_session}"
        out_json = DATA_DIR / f"questions_기출_{year}_{safe_session}.json"

        # Skip if already completed
        if exam_key in progress.get("completed", []):
            log.info(f"[{i}/{total_pdfs}] {exam_key}: 이미 완료 — 스킵")
            summary["task_a_skipped"] += 1
            continue

        if out_json.exists():
            log.info(f"[{i}/{total_pdfs}] {exam_key}: 출력 JSON 존재 — 스킵")
            summary["task_a_skipped"] += 1
            progress["completed"].append(exam_key)
            save_progress(progress)
            continue

        log.info(f"\n[{i}/{total_pdfs}] {exam_key}: 처리 시작")

        try:
            # Step 1: OCR
            if app_id and app_key:
                ocr_pages = ocr_pdf(
                    str(pdf_path), year, session, app_id, app_key, skip_ocr
                )
            else:
                log.warning("  Mathpix credentials not found; trying OCR cache only")
                ocr_pages = load_ocr_cache(year, session) or []

            log.info(f"  OCR 완료({len(ocr_pages)}p)")

            if not ocr_pages:
                raise ValueError("No OCR pages available")

            # Step 2: Parse
            raw_questions = parse_ocr_pages(ocr_pages)
            log.info(f"  파싱({len(raw_questions)}문제)")

            if not raw_questions:
                raise ValueError("No questions parsed from OCR text")

            # Build full question records
            questions: list[dict] = []
            for q in raw_questions:
                questions.append(
                    {
                        "year": year,
                        "session": session,
                        "subject": get_subject(
                            q["q_no"],
                            q.get("text", "") + " " + " ".join(q.get("choices", [])),
                        ),
                        "q_no": q["q_no"],
                        "text": q["text"],
                        "choices": q["choices"],
                        "answer": q["answer"],
                        "solution": q.get("solution_ocr", ""),
                        "solution_ocr": q.get("solution_ocr", ""),
                        "concept": [],
                        "difficulty": "",
                        "q_type": "",
                    }
                )

            # Step 3: Claude Haiku tagging + solution completion
            if api_key:
                questions = complete_question_with_haiku(
                    questions, concept_map, api_key
                )
                log.info("  태깅 완료")
            else:
                log.warning("  ANTHROPIC_API_KEY 없음 — 태깅 스킵")

            # Remove internal helper field
            for q in questions:
                q.pop("solution_ocr", None)

            # Step 4: Save JSON
            with open(out_json, "w", encoding="utf-8") as f:
                json.dump(questions, f, ensure_ascii=False, indent=2)
            log.info(f"  저장 → {out_json.name}")

            # Step 5: Obsidian
            save_obsidian(questions, year, session)

            n_sol = sum(1 for q in questions if q.get("solution"))
            n_tag = sum(1 for q in questions if q.get("concept"))
            summary["task_a_processed"] += 1
            summary["task_a_total_questions"] += len(questions)
            summary["task_a_solutions"] += n_sol
            summary["task_a_tagged"] += n_tag

            progress["completed"].append(exam_key)
            save_progress(progress)
            log.info(
                f"[{i}/{total_pdfs}] {exam_key}: 완료 "
                f"({len(questions)}문제, 풀이:{n_sol}, 태깅:{n_tag})"
            )

        except Exception as e:
            log.error(f"[{i}/{total_pdfs}] {exam_key}: 오류 — {e}")
            errors.append({"exam": exam_key, "error": str(e), "pdf": str(pdf_path)})
            save_errors(errors)
            summary["task_a_errors"] += 1
            continue

    return summary


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(
        description="전기기사 기출문제 PDF 일괄 처리 파이프라인"
    )
    parser.add_argument("--start-year", type=int, default=1998)
    parser.add_argument("--end-year", type=int, default=2020)
    parser.add_argument(
        "--skip-ocr",
        action="store_true",
        help="Mathpix OCR를 건너뛰고 캐시만 사용",
    )
    args = parser.parse_args()

    log.info("=" * 60)
    log.info("전기기사 기출문제 일괄 처리 파이프라인")
    log.info(f"대상 연도: {args.start_year} ~ {args.end_year}")
    log.info("=" * 60)

    # Load credentials
    api_key, app_id, app_key = load_env()
    if api_key:
        log.info("✓ ANTHROPIC_API_KEY 로드됨")
    else:
        log.warning("✗ ANTHROPIC_API_KEY 없음 — 태깅/풀이 생성 불가")
    if app_id and app_key:
        log.info("✓ Mathpix credentials 로드됨")
    else:
        log.warning("✗ Mathpix credentials 없음 — OCR 캐시만 사용 가능")

    # Load concept map
    if not CONCEPT_MAP_FILE.exists():
        log.error(f"개념 맵 파일 없음: {CONCEPT_MAP_FILE}")
        sys.exit(1)
    concept_map = load_concept_map()
    total_concepts = sum(len(v) for v in concept_map.values())
    log.info(
        f"✓ 개념 맵 로드: {len(concept_map)}과목 × 합계 {total_concepts}개 개념"
    )

    # Load progress & errors
    progress = load_progress()
    errors = load_errors()
    log.info(
        f"✓ 진행 현황: 완료={len(progress.get('completed', []))}, "
        f"오류={len(errors)}"
    )

    # ── Task B: CBT solution generation (fast, no OCR) ──
    if api_key:
        log.info("\n" + "─" * 60)
        log.info("[Task B] CBT 파일 풀이 생성")
        log.info("─" * 60)
        summary_b = run_task_b(concept_map, api_key)
    else:
        log.warning("\n[Task B] API 키 없음 — CBT 풀이 생성 스킵")
        summary_b = {
            "task_b_files": [],
            "task_b_total_questions": 0,
            "task_b_solutions_generated": 0,
        }

    # ── Task A: image PDF pipeline ──
    log.info("\n" + "─" * 60)
    log.info("[Task A] 이미지 기출 PDF 처리")
    log.info("─" * 60)

    pdfs = collect_image_pdfs(DATA_DIR, args.start_year, args.end_year)
    log.info(f"대상 PDF: {len(pdfs)}개 ({args.start_year}~{args.end_year})")

    if not pdfs:
        log.warning("처리할 PDF가 없습니다.")
    else:
        summary_a = run_task_a(
            pdfs,
            concept_map,
            api_key,
            app_id,
            app_key,
            args.skip_ocr,
            progress,
            errors,
        )
    summary_a = locals().get("summary_a", {
        "task_a_processed": 0,
        "task_a_skipped": 0,
        "task_a_errors": 0,
        "task_a_total_questions": 0,
        "task_a_solutions": 0,
        "task_a_tagged": 0,
    })

    # ── Final summary ──
    log.info("\n" + "=" * 60)
    log.info("최종 요약")
    log.info("=" * 60)

    total_exams = summary_a["task_a_processed"] + len(summary_b["task_b_files"])
    total_questions = (
        summary_a["task_a_total_questions"] + summary_b["task_b_total_questions"]
    )
    total_solutions = summary_a["task_a_solutions"] + summary_b["task_b_solutions_generated"]
    total_tagged = summary_a["task_a_tagged"]

    log.info(f"처리 완료 시험: {total_exams}개")
    log.info(f"  - Task A (이미지 PDF): {summary_a['task_a_processed']}개 처리, "
             f"{summary_a['task_a_skipped']}개 스킵, "
             f"{summary_a['task_a_errors']}개 오류")
    log.info(f"  - Task B (CBT): {len(summary_b['task_b_files'])}개 파일")
    log.info(f"총 문제 수: {total_questions}")
    log.info(f"풀이 생성: {total_solutions}")
    log.info(f"개념 태깅: {total_tagged} (Task A 기준)")

    if errors:
        log.info(f"\n오류 ({len(errors)}개):")
        for err in errors:
            log.info(f"  - {err['exam']}: {err['error']}")

    log.info("\n완료.")


if __name__ == "__main__":
    main()
