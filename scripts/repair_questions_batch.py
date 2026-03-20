#!/usr/bin/env python3
"""
Repair broken exam questions using Claude Vision API + Batch API.

Scans questions_기출_*.json files for incomplete questions,
re-extracts them from original PDF files using Claude Vision,
and updates the JSON files with repaired data.

Usage:
    python scripts/repair_questions_batch.py scan      # Scan and report broken questions
    python scripts/repair_questions_batch.py estimate   # Cost estimate
    python scripts/repair_questions_batch.py submit     # Convert PDFs → images, submit batch
    python scripts/repair_questions_batch.py status     # Check batch status
    python scripts/repair_questions_batch.py download   # Apply results to JSON files
"""

import argparse
import base64
import json
import logging
import re
import time
import unicodedata
from pathlib import Path

import io

import anthropic
import fitz  # PyMuPDF
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BATCH_DIR = DATA_DIR / "batch_repair"
BATCH_DIR.mkdir(exist_ok=True)

BATCH_ID_FILE = BATCH_DIR / "batch_ids.json"
MAPPING_FILE = BATCH_DIR / "page_mapping.json"
RESULTS_DIR = BATCH_DIR / "results"
RESULTS_DIR.mkdir(exist_ok=True)
FAILED_FILE = BATCH_DIR / "failed_pages.json"
REPAIR_LOG = BATCH_DIR / "repair_log.json"

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 4096
DPI_SCALE = 1.5  # 1.5x = 108 DPI (72 * 1.5)
JPEG_QUALITY = 80
MAX_REQUESTS_PER_BATCH = 100  # Keep payload under Cloudflare limit

# ── Vision prompt ────────────────────────────────────────────────────────────
QUESTION_PAGE_PROMPT = """이 이미지는 전기기사 필기시험 기출문제지의 한 페이지입니다.
이 페이지에 있는 내용을 분석하고 JSON으로 출력하세요.

경우 1: 시험 문제가 있는 페이지
{
  "type": "questions",
  "items": [
    {
      "q_no": 문제번호(정수),
      "text": "문제 본문 텍스트",
      "choices": ["선택지1 내용", "선택지2 내용", "선택지3 내용", "선택지4 내용"],
      "has_figure": true또는false
    }
  ]
}

경우 2: 정답표 페이지
{
  "type": "answer_key",
  "answers": {"1": 정답번호, "2": 정답번호, "3": 정답번호, ...}
}

경우 3: 기타 페이지 (표지, 안내문 등)
{
  "type": "other"
}

규칙:
- 수학 공식은 LaTeX로 작성: \\(인라인 공식\\) 또는 \\[블록 공식\\]
- 선택지 앞 번호 기호(①②③④)는 제외하고 내용만 기록
- 그림, 회로도, 도표가 포함된 문제는 has_figure: true
- 정답표의 정답 번호는 1~4 사이의 정수
- JSON만 출력하세요. 다른 텍스트 없이 JSON만."""


# ── Helpers ──────────────────────────────────────────────────────────────────
def is_broken(q: dict) -> bool:
    """Check if a question has any data quality issue."""
    text = q.get('text', '').strip()
    choices = q.get('choices', [])
    answer = q.get('answer', 0)

    text_empty = not text
    choices_all_empty = all(not c.strip() for c in choices) if choices else True
    choices_some_empty = any(not c.strip() for c in choices) if choices else True
    answer_bad = answer not in [1, 2, 3, 4]

    return text_empty or choices_all_empty or choices_some_empty or answer_bad


def _nfc(s: str) -> str:
    """Normalize Unicode to NFC (macOS stores filenames in NFD)."""
    return unicodedata.normalize("NFC", s)


def find_pdf_for_json(json_name: str) -> Path | None:
    """Find the matching PDF file for a JSON question file."""
    # Extract year and session from 'questions_기출_YYYY_N회.json'
    match = re.search(r'questions_기출_(\d{4})_(.+?)\.json', json_name)
    if not match:
        return None

    year = match.group(1)
    session_raw = match.group(2)  # e.g., '1회', '1_2회', '3회'

    # Build search patterns
    # JSON '1_2회' → PDF may have '1,2회' or '1_2회'
    session_variants = [session_raw]
    if '_' in session_raw:
        session_variants.append(session_raw.replace('_', ','))

    # Search PDF files (normalize to NFC for macOS compatibility)
    candidates = []
    for pdf_path in DATA_DIR.glob("*.pdf"):
        pdf_name = _nfc(pdf_path.name)
        # Must contain year
        if year not in pdf_name:
            continue
        # Must be an exam PDF (문제 or date-prefixed like 20200424)
        if '문제' not in pdf_name and not re.match(r'\d{8}', pdf_name):
            continue

        # Check session match
        for variant in session_variants:
            if variant in pdf_name:
                candidates.append(pdf_path)
                break

    if not candidates:
        return None

    # Prefer exact match, then first candidate
    return candidates[0]


def pdf_page_to_base64(page: fitz.Page) -> str:
    """Convert a PDF page to base64-encoded JPEG image."""
    mat = fitz.Matrix(DPI_SCALE, DPI_SCALE)
    pix = page.get_pixmap(matrix=mat)

    # Convert to JPEG via Pillow for smaller payload
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def parse_vision_response(raw_text: str) -> dict | None:
    """Parse Claude Vision JSON response with robust markdown fence handling."""
    text = raw_text.strip()

    # Remove ALL markdown code fences (opening and closing)
    text = re.sub(r'```(?:json)?\s*', '', text).strip()

    # Fix invalid JSON escape sequences from LaTeX
    # Protect already-escaped backslashes (\\), then fix lone backslashes
    text = text.replace('\\\\', '\x00DBL_BS\x00')
    text = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)
    text = text.replace('\x00DBL_BS\x00', '\\\\')

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to extract the outermost JSON object
    # Find the first { and last }
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace != -1 and last_brace > first_brace:
        candidate = text[first_brace:last_brace + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    # Try fixing truncated JSON (max_tokens cutoff)
    # Add missing closing brackets/braces
    if first_brace != -1:
        candidate = text[first_brace:]
        # Count unclosed brackets
        open_braces = candidate.count('{') - candidate.count('}')
        open_brackets = candidate.count('[') - candidate.count(']')
        # Try to close them
        if open_braces > 0 or open_brackets > 0:
            # Remove trailing incomplete string (after last complete value)
            # Trim to last comma or complete value
            trimmed = re.sub(r',\s*"[^"]*$', '', candidate)
            trimmed = re.sub(r',\s*$', '', trimmed)
            trimmed += ']' * open_brackets + '}' * open_braces
            try:
                return json.loads(trimmed)
            except json.JSONDecodeError:
                pass

    return None


# ── Commands ─────────────────────────────────────────────────────────────────
def cmd_scan():
    """Scan all question files and report broken questions."""
    files = sorted(DATA_DIR.glob("questions_기출_*.json"))

    total_questions = 0
    total_broken = 0
    file_report = []

    for fp in files:
        qs = json.loads(fp.read_text(encoding='utf-8'))
        broken_count = sum(1 for q in qs if is_broken(q))
        total_questions += len(qs)
        total_broken += broken_count

        pdf = find_pdf_for_json(fp.name)
        pdf_status = "OK" if pdf else "MISSING"

        if broken_count > 0:
            file_report.append({
                'file': fp.name,
                'total': len(qs),
                'broken': broken_count,
                'pdf': pdf.name if pdf else None,
                'pdf_status': pdf_status,
            })

    logger.info("=" * 70)
    logger.info("REPAIR SCAN REPORT")
    logger.info("=" * 70)
    logger.info("Total questions: %d", total_questions)
    logger.info("Broken questions: %d (%.1f%%)", total_broken,
                total_broken / total_questions * 100 if total_questions else 0)
    logger.info("")

    pdf_found = sum(1 for r in file_report if r['pdf_status'] == 'OK')
    pdf_missing = sum(1 for r in file_report if r['pdf_status'] == 'MISSING')
    logger.info("PDF mapping: %d found, %d missing", pdf_found, pdf_missing)
    logger.info("")

    for r in file_report:
        pct = r['broken'] / r['total'] * 100 if r['total'] else 0
        pdf_info = f"→ {r['pdf']}" if r['pdf'] else "→ PDF NOT FOUND"
        logger.info("  %s: %d/%d broken (%.0f%%) %s",
                     r['file'], r['broken'], r['total'], pct, pdf_info)

    if pdf_missing > 0:
        logger.warning("")
        logger.warning("Missing PDFs (%d files):", pdf_missing)
        for r in file_report:
            if r['pdf_status'] == 'MISSING':
                logger.warning("  %s", r['file'])

    logger.info("=" * 70)


def cmd_estimate():
    """Estimate cost for batch processing."""
    files = sorted(DATA_DIR.glob("questions_기출_*.json"))

    total_pages = 0
    total_broken = 0
    pdfs_to_process = []

    for fp in files:
        qs = json.loads(fp.read_text(encoding='utf-8'))
        broken_count = sum(1 for q in qs if is_broken(q))
        if broken_count == 0:
            continue

        pdf = find_pdf_for_json(fp.name)
        if not pdf:
            continue

        doc = fitz.open(str(pdf))
        page_count = len(doc)
        doc.close()

        total_pages += page_count
        total_broken += broken_count
        pdfs_to_process.append({
            'json': fp.name,
            'pdf': pdf.name,
            'pages': page_count,
            'broken': broken_count,
        })

    # Haiku Batch pricing (50% discount)
    # Image input: ~2000 tokens per page (estimated for 144 DPI A4)
    # Text prompt: ~300 tokens
    # Output: ~800 tokens per page (JSON with questions)
    input_tokens_per_page = 2300
    output_tokens_per_page = 800
    input_cost_per_1m = 0.40   # Batch: $0.40/1M
    output_cost_per_1m = 2.00  # Batch: $2.00/1M

    total_input = total_pages * input_tokens_per_page
    total_output = total_pages * output_tokens_per_page
    input_cost = total_input / 1_000_000 * input_cost_per_1m
    output_cost = total_output / 1_000_000 * output_cost_per_1m
    total_cost = input_cost + output_cost

    batches_needed = (total_pages + MAX_REQUESTS_PER_BATCH - 1) // MAX_REQUESTS_PER_BATCH

    logger.info("=" * 60)
    logger.info("REPAIR COST ESTIMATE")
    logger.info("=" * 60)
    logger.info("PDFs to process: %d", len(pdfs_to_process))
    logger.info("Total pages: %d", total_pages)
    logger.info("Broken questions: %d", total_broken)
    logger.info("Batches needed: %d (max %d per batch)", batches_needed, MAX_REQUESTS_PER_BATCH)
    logger.info("")
    logger.info("Model: %s (Batch API, 50%% discount)", MODEL)
    logger.info("Est. input:  %s tokens ($%.2f)", f"{total_input:,}", input_cost)
    logger.info("Est. output: %s tokens ($%.2f)", f"{total_output:,}", output_cost)
    logger.info("Est. total:  $%.2f", total_cost)
    logger.info("Est. time:   max 24h (usually 1-6h)")
    logger.info("=" * 60)


def cmd_submit():
    """Convert PDF pages to images and submit batch requests."""
    files = sorted(DATA_DIR.glob("questions_기출_*.json"))

    # Build page mapping and requests
    page_mapping = {}  # custom_id -> {json_file, pdf_file, page_num}
    all_requests = []

    for fp in files:
        qs = json.loads(fp.read_text(encoding='utf-8'))
        broken_count = sum(1 for q in qs if is_broken(q))
        if broken_count == 0:
            continue

        pdf = find_pdf_for_json(fp.name)
        if not pdf:
            logger.warning("PDF not found for %s, skipping", fp.name)
            continue

        logger.info("Processing %s → %s (%d broken questions)",
                     fp.name, pdf.name, broken_count)

        doc = fitz.open(str(pdf))
        for page_idx in range(len(doc)):
            page = doc[page_idx]

            # Convert page to base64 image
            b64_image = pdf_page_to_base64(page)

            # Create custom_id: safe ASCII only
            safe_json = re.sub(r'[^a-zA-Z0-9_-]', '',
                               fp.stem.replace("questions_기출_", "q_")
                               .replace("회", ""))
            custom_id = f"{safe_json}_p{page_idx}"

            page_mapping[custom_id] = {
                "json_file": fp.name,
                "pdf_file": pdf.name,
                "page_num": page_idx,
            }

            request = {
                "custom_id": custom_id,
                "params": {
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image",
                                    "source": {
                                        "type": "base64",
                                        "media_type": "image/jpeg",
                                        "data": b64_image,
                                    },
                                },
                                {"type": "text", "text": QUESTION_PAGE_PROMPT},
                            ],
                        }
                    ],
                },
            }
            all_requests.append(request)

        doc.close()

    if not all_requests:
        logger.info("No pages to process. All questions are complete or PDFs missing.")
        return

    # Save mapping
    MAPPING_FILE.write_text(
        json.dumps(page_mapping, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    logger.info("Mapping saved: %s (%d pages)", MAPPING_FILE, len(page_mapping))

    # Split into batches and submit
    client = anthropic.Anthropic()
    batch_ids = []
    total_batches = (len(all_requests) + MAX_REQUESTS_PER_BATCH - 1) // MAX_REQUESTS_PER_BATCH

    for batch_num in range(total_batches):
        start = batch_num * MAX_REQUESTS_PER_BATCH
        end = min(start + MAX_REQUESTS_PER_BATCH, len(all_requests))
        batch_requests = all_requests[start:end]

        logger.info("Submitting batch %d/%d (%d requests)...",
                     batch_num + 1, total_batches, len(batch_requests))

        batch = client.messages.batches.create(
            requests=[
                {
                    "custom_id": req["custom_id"],
                    "params": req["params"],
                }
                for req in batch_requests
            ]
        )

        batch_ids.append({
            "batch_id": batch.id,
            "batch_num": batch_num + 1,
            "request_count": len(batch_requests),
            "status": batch.processing_status,
        })
        logger.info("  Batch ID: %s (status: %s)", batch.id, batch.processing_status)

        # Small delay between batch submissions
        if batch_num < total_batches - 1:
            time.sleep(1)

    # Save batch IDs
    BATCH_ID_FILE.write_text(
        json.dumps(batch_ids, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )

    logger.info("")
    logger.info("All batches submitted!")
    logger.info("Total: %d batches, %d requests", len(batch_ids), len(all_requests))
    logger.info("Batch IDs saved: %s", BATCH_ID_FILE)
    logger.info("")
    logger.info("Next: python scripts/repair_questions_batch.py status")


def cmd_status():
    """Check status of all submitted batches."""
    if not BATCH_ID_FILE.exists():
        logger.error("No batch IDs found. Run 'submit' first.")
        return

    batch_ids = json.loads(BATCH_ID_FILE.read_text())
    client = anthropic.Anthropic()

    all_done = True
    for entry in batch_ids:
        batch = client.messages.batches.retrieve(entry["batch_id"])

        counts = batch.request_counts
        total = counts.processing + counts.succeeded + counts.errored + counts.canceled + counts.expired

        logger.info("Batch %d/%d [%s]:",
                     entry["batch_num"], len(batch_ids), entry["batch_id"])
        logger.info("  Status: %s", batch.processing_status)
        logger.info("  Total: %d | Success: %d | Error: %d | Processing: %d",
                     total, counts.succeeded, counts.errored, counts.processing)

        if batch.processing_status != "ended":
            all_done = False

    if all_done:
        logger.info("")
        logger.info("All batches complete! Next: python scripts/repair_questions_batch.py download")
    else:
        logger.info("")
        logger.info("Some batches still processing. Check again later.")


def cmd_download():
    """Download batch results and apply repairs to JSON files."""
    if not BATCH_ID_FILE.exists():
        logger.error("No batch IDs found.")
        return
    if not MAPPING_FILE.exists():
        logger.error("No mapping file found.")
        return

    batch_ids = json.loads(BATCH_ID_FILE.read_text())
    page_mapping = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
    client = anthropic.Anthropic()

    # Phase 1: Download and parse all results
    # Organize by json_file: {q_no: {text, choices, has_figure}, answer_key: {q_no: answer}}
    file_data = {}  # json_file -> {"questions": {q_no: {...}}, "answer_key": {q_no: answer}}
    failed_pages = []
    parse_errors = 0
    success_pages = 0

    for entry in batch_ids:
        batch = client.messages.batches.retrieve(entry["batch_id"])
        if batch.processing_status != "ended":
            logger.warning("Batch %s not yet complete (status: %s), skipping",
                           entry["batch_id"], batch.processing_status)
            continue

        logger.info("Downloading batch %d results...", entry["batch_num"])

        for result in client.messages.batches.results(entry["batch_id"]):
            custom_id = result.custom_id
            mapping = page_mapping.get(custom_id)
            if not mapping:
                continue

            json_file = mapping["json_file"]
            if json_file not in file_data:
                file_data[json_file] = {"questions": {}, "answer_key": {}}

            if result.result.type != "succeeded":
                failed_pages.append({
                    "custom_id": custom_id,
                    "json_file": json_file,
                    "page_num": mapping["page_num"],
                    "reason": result.result.type,
                })
                continue

            # Extract text from response
            raw = ""
            for block in result.result.message.content:
                if block.type == "text":
                    raw += block.text

            parsed = parse_vision_response(raw)
            if not parsed:
                failed_pages.append({
                    "custom_id": custom_id,
                    "json_file": json_file,
                    "page_num": mapping["page_num"],
                    "reason": "json_parse_failed",
                    "raw_preview": raw[:200],
                })
                parse_errors += 1
                continue

            success_pages += 1
            page_type = parsed.get("type", "other")

            if page_type == "questions":
                items = parsed.get("items", [])
                for item in items:
                    q_no = item.get("q_no")
                    if q_no is None:
                        continue
                    file_data[json_file]["questions"][str(q_no)] = {
                        "text": item.get("text", ""),
                        "choices": item.get("choices", []),
                        "has_figure": item.get("has_figure", False),
                    }

            elif page_type == "answer_key":
                answers = parsed.get("answers", {})
                for q_no_str, ans in answers.items():
                    if isinstance(ans, int) and 1 <= ans <= 4:
                        file_data[json_file]["answer_key"][q_no_str] = ans

    logger.info("Downloaded: %d pages success, %d parse errors, %d failed",
                success_pages, parse_errors, len(failed_pages))

    # Phase 2: Apply repairs
    total_repaired = 0
    total_text_fixed = 0
    total_choices_fixed = 0
    total_answer_fixed = 0
    repair_details = []

    for json_file, data in file_data.items():
        fp = DATA_DIR / json_file
        if not fp.exists():
            logger.warning("JSON file not found: %s", json_file)
            continue

        qs = json.loads(fp.read_text(encoding='utf-8'))
        questions_data = data["questions"]
        answer_key = data["answer_key"]
        file_repairs = 0

        for idx, q in enumerate(qs):
            if not is_broken(q):
                continue

            q_no = q.get("q_no", idx + 1)
            q_no_str = str(q_no)
            repaired = False

            # Fix text
            if not q.get("text", "").strip():
                extracted = questions_data.get(q_no_str, {})
                if extracted.get("text", "").strip():
                    q["text"] = extracted["text"]
                    total_text_fixed += 1
                    repaired = True

            # Fix choices
            choices = q.get("choices", [])
            if not choices or all(not c.strip() for c in choices) or any(not c.strip() for c in choices):
                extracted = questions_data.get(q_no_str, {})
                extracted_choices = extracted.get("choices", [])
                if len(extracted_choices) == 4 and all(c.strip() for c in extracted_choices):
                    q["choices"] = extracted_choices
                    total_choices_fixed += 1
                    repaired = True
                elif len(extracted_choices) == 4:
                    # Partial fix: fill in missing choices only
                    for ci in range(4):
                        if ci < len(choices) and not choices[ci].strip():
                            if ci < len(extracted_choices) and extracted_choices[ci].strip():
                                choices[ci] = extracted_choices[ci]
                                repaired = True
                    if repaired:
                        total_choices_fixed += 1

            # Fix answer
            if q.get("answer", 0) not in [1, 2, 3, 4]:
                if q_no_str in answer_key:
                    q["answer"] = answer_key[q_no_str]
                    total_answer_fixed += 1
                    repaired = True

            if repaired:
                file_repairs += 1
                total_repaired += 1

        # Save updated JSON
        if file_repairs > 0:
            fp.write_text(
                json.dumps(qs, ensure_ascii=False, indent=2),
                encoding='utf-8',
            )
            logger.info("  %s: %d questions repaired", json_file, file_repairs)
            repair_details.append({
                "file": json_file,
                "repaired": file_repairs,
            })

    # Save repair log
    repair_log = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "model": MODEL,
        "pages_processed": success_pages,
        "parse_errors": parse_errors,
        "total_repaired": total_repaired,
        "text_fixed": total_text_fixed,
        "choices_fixed": total_choices_fixed,
        "answer_fixed": total_answer_fixed,
        "files": repair_details,
    }
    REPAIR_LOG.write_text(
        json.dumps(repair_log, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )

    # Save failed pages
    if failed_pages:
        FAILED_FILE.write_text(
            json.dumps(failed_pages, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )

    logger.info("")
    logger.info("=" * 60)
    logger.info("REPAIR RESULTS")
    logger.info("=" * 60)
    logger.info("Total repaired: %d questions", total_repaired)
    logger.info("  Text fixed:    %d", total_text_fixed)
    logger.info("  Choices fixed: %d", total_choices_fixed)
    logger.info("  Answer fixed:  %d", total_answer_fixed)
    logger.info("Files updated: %d", len(repair_details))
    if failed_pages:
        logger.info("Failed pages: %d (see %s)", len(failed_pages), FAILED_FILE)
    logger.info("Repair log: %s", REPAIR_LOG)
    logger.info("=" * 60)

    # Post-repair validation
    logger.info("")
    logger.info("Running post-repair validation...")
    total_q = 0
    still_broken = 0
    for fp in sorted(DATA_DIR.glob("questions_기출_*.json")):
        qs = json.loads(fp.read_text(encoding='utf-8'))
        for q in qs:
            total_q += 1
            if is_broken(q):
                still_broken += 1

    fixed_pct = (1 - still_broken / total_q) * 100 if total_q else 0
    logger.info("Post-repair: %d/%d complete (%.1f%%)", total_q - still_broken, total_q, fixed_pct)
    logger.info("Still broken: %d (%.1f%%)", still_broken, still_broken / total_q * 100 if total_q else 0)


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Repair broken exam questions using Claude Vision + Batch API"
    )
    parser.add_argument(
        "command",
        choices=["scan", "estimate", "submit", "status", "download"],
        help="scan: report broken questions, estimate: cost estimate, "
             "submit: submit batch, status: check progress, download: apply results",
    )
    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan()
    elif args.command == "estimate":
        cmd_estimate()
    elif args.command == "submit":
        cmd_submit()
    elif args.command == "status":
        cmd_status()
    elif args.command == "download":
        cmd_download()


if __name__ == "__main__":
    main()
