#!/usr/bin/env python3
"""
Targeted answer key extraction from PDF last pages.

The main repair batch extracted questions well but missed most answer keys.
This script specifically targets the last 2 pages of each PDF where answer
keys are typically located.

Usage:
    python scripts/repair_answers_batch.py estimate
    python scripts/repair_answers_batch.py submit
    python scripts/repair_answers_batch.py status
    python scripts/repair_answers_batch.py download
"""

import argparse
import base64
import io
import json
import logging
import re
import time
import unicodedata
from pathlib import Path

import anthropic
import fitz
from PIL import Image

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BATCH_DIR = DATA_DIR / "batch_answer_key"
BATCH_DIR.mkdir(exist_ok=True)

BATCH_ID_FILE = BATCH_DIR / "batch_ids.json"
MAPPING_FILE = BATCH_DIR / "mapping.json"
REPAIR_LOG = BATCH_DIR / "repair_log.json"

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 2048
DPI_SCALE = 1.5
JPEG_QUALITY = 80
ANSWER_PAGES_TO_CHECK = 2  # Last N pages per PDF

# Dedicated answer key prompt — much more specific
ANSWER_KEY_PROMPT = """이 이미지는 전기기사 필기시험의 정답표(답안지) 페이지입니다.

모든 문제의 정답 번호를 추출하세요.
정답표가 없으면 이 페이지에 보이는 문제의 정답을 추출하세요.

JSON 형식으로 출력:
{"answers": {"1": 정답번호, "2": 정답번호, "3": 정답번호, ...}}

규칙:
- 정답 번호는 1~4 사이의 정수
- 문제 번호는 1~100 사이
- 정답이 ①이면 1, ②이면 2, ③이면 3, ④이면 4
- 정답이 ❶이면 1, ❷이면 2, ❸이면 3, ❹이면 4
- 가능한 모든 문제의 정답을 추출
- 정답표가 아닌 페이지면 빈 객체 출력: {"answers": {}}
- JSON만 출력, 다른 텍스트 없이"""


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def find_pdf_for_json(json_name: str) -> Path | None:
    match = re.search(r'questions_기출_(\d{4})_(.+?)\.json', json_name)
    if not match:
        return None
    year, session_raw = match.group(1), match.group(2)
    session_variants = [session_raw]
    if '_' in session_raw:
        session_variants.append(session_raw.replace('_', ','))

    for pdf_path in DATA_DIR.glob("*.pdf"):
        pdf_name = _nfc(pdf_path.name)
        if year not in pdf_name:
            continue
        if '문제' not in pdf_name and not re.match(r'\d{8}', pdf_name):
            continue
        for variant in session_variants:
            if variant in pdf_name:
                return pdf_path
    return None


def page_to_base64(page: fitz.Page) -> str:
    mat = fitz.Matrix(DPI_SCALE, DPI_SCALE)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True)
    return base64.b64encode(buf.getvalue()).decode()


def parse_answer_response(raw_text: str) -> dict[str, int]:
    """Parse answer key JSON, return {q_no_str: answer_int}."""
    text = raw_text.strip()
    text = re.sub(r'```(?:json)?\s*', '', text).strip()
    # Fix LaTeX escapes
    text = text.replace('\\\\', '\x00D\x00')
    text = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)
    text = text.replace('\x00D\x00', '\\\\')

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        # Try extracting JSON object
        m = re.search(r'\{[\s\S]*\}', text)
        if m:
            try:
                data = json.loads(m.group())
            except json.JSONDecodeError:
                return {}
        else:
            return {}

    answers = data.get("answers", data)
    if not isinstance(answers, dict):
        return {}

    result = {}
    for k, v in answers.items():
        try:
            q_no = str(int(str(k)))
            ans = int(v)
            if 1 <= ans <= 4:
                result[q_no] = ans
        except (ValueError, TypeError):
            continue
    return result


def get_files_needing_answers() -> list[dict]:
    """Find JSON files with questions that have invalid answers."""
    result = []
    for fp in sorted(DATA_DIR.glob("questions_기출_*.json")):
        qs = json.loads(fp.read_text(encoding='utf-8'))
        bad_answer_count = sum(1 for q in qs if q.get('answer', 0) not in [1, 2, 3, 4])
        if bad_answer_count == 0:
            continue
        pdf = find_pdf_for_json(fp.name)
        if not pdf:
            continue
        result.append({
            'json_file': fp.name,
            'pdf_path': pdf,
            'bad_answers': bad_answer_count,
            'total': len(qs),
        })
    return result


def cmd_estimate():
    files = get_files_needing_answers()
    total_pages = sum(ANSWER_PAGES_TO_CHECK for _ in files)
    total_bad = sum(f['bad_answers'] for f in files)

    # Cost estimate
    input_per_page = 2300
    output_per_page = 500
    input_cost = total_pages * input_per_page / 1_000_000 * 0.40
    output_cost = total_pages * output_per_page / 1_000_000 * 2.00
    total_cost = input_cost + output_cost

    logger.info("=" * 60)
    logger.info("ANSWER KEY REPAIR ESTIMATE")
    logger.info("=" * 60)
    logger.info("PDFs to process: %d", len(files))
    logger.info("Pages to extract: %d (last %d per PDF)", total_pages, ANSWER_PAGES_TO_CHECK)
    logger.info("Questions needing answers: %d", total_bad)
    logger.info("Model: %s (Batch 50%% discount)", MODEL)
    logger.info("Est. cost: $%.2f", total_cost)
    logger.info("=" * 60)


def cmd_submit():
    files = get_files_needing_answers()
    if not files:
        logger.info("No files need answer repair.")
        return

    page_mapping = {}
    requests = []

    for entry in files:
        pdf_path = entry['pdf_path']
        json_file = entry['json_file']

        doc = fitz.open(str(pdf_path))
        total_pages = len(doc)

        # Extract last N pages (answer key is typically at the end)
        for offset in range(min(ANSWER_PAGES_TO_CHECK, total_pages)):
            page_idx = total_pages - 1 - offset
            page = doc[page_idx]
            b64 = page_to_base64(page)

            safe_name = re.sub(r'[^a-zA-Z0-9_-]', '',
                               json_file.replace("questions_기출_", "ak_")
                               .replace("회.json", ""))
            custom_id = f"{safe_name}_p{page_idx}"

            page_mapping[custom_id] = {
                "json_file": json_file,
                "pdf_file": _nfc(pdf_path.name),
                "page_num": page_idx,
            }

            requests.append({
                "custom_id": custom_id,
                "params": {
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "messages": [{
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": b64,
                                },
                            },
                            {"type": "text", "text": ANSWER_KEY_PROMPT},
                        ],
                    }],
                },
            })

        doc.close()

    # Save mapping
    MAPPING_FILE.write_text(
        json.dumps(page_mapping, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    logger.info("Requests: %d pages from %d PDFs", len(requests), len(files))

    # Submit batch
    client = anthropic.Anthropic()
    logger.info("Submitting batch...")

    batch = client.messages.batches.create(
        requests=[{"custom_id": r["custom_id"], "params": r["params"]} for r in requests]
    )

    BATCH_ID_FILE.write_text(
        json.dumps([{"batch_id": batch.id, "request_count": len(requests)}], indent=2)
    )
    logger.info("Batch ID: %s (status: %s)", batch.id, batch.processing_status)
    logger.info("Next: python scripts/repair_answers_batch.py status")


def cmd_status():
    if not BATCH_ID_FILE.exists():
        logger.error("No batch ID. Run submit first.")
        return
    batch_ids = json.loads(BATCH_ID_FILE.read_text())
    client = anthropic.Anthropic()

    for entry in batch_ids:
        batch = client.messages.batches.retrieve(entry["batch_id"])
        c = batch.request_counts
        logger.info("Batch %s: %s", entry["batch_id"], batch.processing_status)
        logger.info("  Success: %d | Error: %d | Processing: %d",
                     c.succeeded, c.errored, c.processing)

    if all(
        client.messages.batches.retrieve(e["batch_id"]).processing_status == "ended"
        for e in batch_ids
    ):
        logger.info("Complete! Next: python scripts/repair_answers_batch.py download")


def cmd_download():
    if not BATCH_ID_FILE.exists() or not MAPPING_FILE.exists():
        logger.error("Missing batch or mapping files.")
        return

    batch_ids = json.loads(BATCH_ID_FILE.read_text())
    page_mapping = json.loads(MAPPING_FILE.read_text(encoding='utf-8'))
    client = anthropic.Anthropic()

    # Collect answer keys per json_file
    # Merge from multiple pages — later page (closer to end) overrides
    file_answers = {}  # json_file -> {q_no_str: answer}
    success = fail = 0

    for entry in batch_ids:
        batch = client.messages.batches.retrieve(entry["batch_id"])
        if batch.processing_status != "ended":
            logger.warning("Batch not done: %s", entry["batch_id"])
            continue

        for result in client.messages.batches.results(entry["batch_id"]):
            m = page_mapping.get(result.custom_id)
            if not m:
                continue

            json_file = m["json_file"]
            if json_file not in file_answers:
                file_answers[json_file] = {}

            if result.result.type != "succeeded":
                fail += 1
                continue

            raw = "".join(b.text for b in result.result.message.content if b.type == "text")
            answers = parse_answer_response(raw)
            if answers:
                # Merge — don't overwrite existing answers
                for qno, ans in answers.items():
                    if qno not in file_answers[json_file]:
                        file_answers[json_file][qno] = ans
                success += 1
            else:
                fail += 1

    logger.info("Pages: %d extracted answers, %d no answers", success, fail)

    # Apply answers to JSON files
    total_fixed = 0
    file_stats = []

    for json_file, answers in file_answers.items():
        if not answers:
            continue
        fp = DATA_DIR / json_file
        if not fp.exists():
            continue

        qs = json.loads(fp.read_text(encoding='utf-8'))
        fixed = 0

        for q in qs:
            if q.get('answer', 0) in [1, 2, 3, 4]:
                continue  # Already has valid answer
            q_no = str(q.get('q_no', 0))
            if q_no in answers:
                q['answer'] = answers[q_no]
                fixed += 1

        if fixed > 0:
            fp.write_text(
                json.dumps(qs, ensure_ascii=False, indent=2), encoding='utf-8'
            )
            total_fixed += fixed
            file_stats.append({"file": json_file, "fixed": fixed})
            logger.info("  %s: %d answers fixed", json_file, fixed)

    # Save log
    REPAIR_LOG.write_text(json.dumps({
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "total_fixed": total_fixed,
        "files": file_stats,
    }, ensure_ascii=False, indent=2))

    logger.info("")
    logger.info("=" * 60)
    logger.info("ANSWER KEY REPAIR RESULTS")
    logger.info("=" * 60)
    logger.info("Total answers fixed: %d", total_fixed)
    logger.info("Files updated: %d", len(file_stats))
    logger.info("=" * 60)

    # Post-repair validation
    total_q = still_bad = 0
    for fp in sorted(DATA_DIR.glob("questions_기출_*.json")):
        qs = json.loads(fp.read_text(encoding='utf-8'))
        for q in qs:
            total_q += 1
            text_ok = bool(q.get('text', '').strip())
            choices = q.get('choices', [])
            choices_ok = len(choices) == 4 and all(c.strip() for c in choices)
            answer_ok = q.get('answer', 0) in [1, 2, 3, 4]
            if not (text_ok and choices_ok and answer_ok):
                still_bad += 1

    logger.info("Post-repair: %d/%d complete (%.1f%%)",
                total_q - still_bad, total_q, (total_q - still_bad) / total_q * 100)


def main():
    parser = argparse.ArgumentParser(description="Answer key repair via Vision Batch API")
    parser.add_argument("command", choices=["estimate", "submit", "status", "download"])
    args = parser.parse_args()

    {"estimate": cmd_estimate, "submit": cmd_submit,
     "status": cmd_status, "download": cmd_download}[args.command]()


if __name__ == "__main__":
    main()
