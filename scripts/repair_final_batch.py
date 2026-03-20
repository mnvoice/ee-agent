#!/usr/bin/env python3
"""
Final comprehensive repair batch.

Combines two repair strategies in a single batch:
1. Answer extraction from ALL pages (not just last 2) for answer-only defects
2. Full question re-extraction for text/choices defects

Usage:
    python scripts/repair_final_batch.py estimate
    python scripts/repair_final_batch.py submit
    python scripts/repair_final_batch.py status
    python scripts/repair_final_batch.py download
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
BATCH_DIR = DATA_DIR / "batch_final_repair"
BATCH_DIR.mkdir(exist_ok=True)

BATCH_ID_FILE = BATCH_DIR / "batch_ids.json"
MAPPING_FILE = BATCH_DIR / "mapping.json"
REPAIR_LOG = BATCH_DIR / "repair_log.json"

MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 4096
DPI_SCALE = 1.5
JPEG_QUALITY = 80
MAX_REQUESTS_PER_BATCH = 100

# Prompt for answer extraction from all pages
ANSWER_PROMPT = """이 이미지는 전기기사 필기시험 PDF의 한 페이지입니다.

이 페이지에서 문제 번호와 정답을 모두 추출하세요.
정답은 다음 위치에 있을 수 있습니다:
- 정답표/답안지 (번호-답 그리드)
- 풀이 뒤 【답】(N) 또는 [답](N) 마커
- 문제 풀이 끝의 정답 표시

JSON 형식으로 출력:
{"answers": {"1": 정답번호, "2": 정답번호, ...}}

규칙:
- 정답 번호는 1~4 사이의 정수
- ①=1, ②=2, ③=3, ④=4
- 가능한 모든 문제의 정답을 추출
- 정답이 없는 페이지면: {"answers": {}}
- JSON만 출력, 다른 텍스트 없이"""

# Prompt for full question extraction
FULL_PROMPT = """이 이미지는 전기기사 필기시험 PDF의 한 페이지입니다.

이 페이지의 모든 문제를 추출하세요.
각 문제에서 다음을 추출:
1. 문제 번호 (q_no)
2. 문제 텍스트 (text)
3. 보기 4개 (choices)
4. 정답 번호 (answer) — 【답】마커 또는 풀이에서 추출

JSON 형식:
{"questions": [
  {"q_no": 번호, "text": "문제 내용", "choices": ["①보기", "②보기", "③보기", "④보기"], "answer": 정답번호},
  ...
]}

규칙:
- 정답 번호는 1~4 사이의 정수 (모르면 0)
- 보기 번호(①②③④)는 제거하고 텍스트만
- 수식은 원본 그대로 유지
- 교차참조 문제("YYYY년도 N회 문제NN"만 있고 실제 내용 없음)는 건너뛰기
- 문제가 없는 페이지면: {"questions": []}
- JSON만 출력"""


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s)


def find_pdf_for_json(json_name: str) -> Path | None:
    match = re.search(r"questions_기출_(\d{4})_(.+?)\.json", json_name)
    if not match:
        return None
    year, session_raw = match.group(1), match.group(2)
    session_variants = [session_raw]
    if "_" in session_raw:
        session_variants.append(session_raw.replace("_", ","))

    for pdf_path in DATA_DIR.glob("*.pdf"):
        pdf_name = _nfc(pdf_path.name)
        if year not in pdf_name:
            continue
        if "문제" not in pdf_name and not re.match(r"\d{8}", pdf_name):
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


def classify_defects(qs: list[dict]) -> str:
    """Classify defect type: 'answer_only' or 'full'."""
    broken = [
        q for q in qs
        if not (
            q.get("text", "").strip()
            and len(q.get("choices", [])) == 4
            and all(c.strip() for c in q.get("choices", []))
            and q.get("answer", 0) in [1, 2, 3, 4]
        )
    ]
    if not broken:
        return "none"

    # If all broken questions have text+choices, just need answers
    all_have_content = all(
        q.get("text", "").strip()
        and len(q.get("choices", [])) == 4
        and all(c.strip() for c in q.get("choices", []))
        for q in broken
    )
    return "answer_only" if all_have_content else "full"


def parse_answer_response(raw_text: str) -> dict[str, int]:
    text = raw_text.strip()
    text = re.sub(r"```(?:json)?\s*", "", text).strip()
    text = text.replace("\\\\", "\x00D\x00")
    text = re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", text)
    text = text.replace("\x00D\x00", "\\\\")

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", text)
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


def parse_full_response(raw_text: str) -> list[dict]:
    text = raw_text.strip()
    text = re.sub(r"```(?:json)?\s*", "", text).strip()
    text = text.replace("\\\\", "\x00D\x00")
    text = re.sub(r'\\(?!["\\/bfnrtu])', r"\\\\", text)
    text = text.replace("\x00D\x00", "\\\\")

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                data = json.loads(m.group())
            except json.JSONDecodeError:
                return []
        else:
            return []

    questions = data.get("questions", [])
    if not isinstance(questions, list):
        return []

    result = []
    for q in questions:
        try:
            qno = int(q.get("q_no", 0))
            text_val = str(q.get("text", "")).strip()
            choices = q.get("choices", [])
            answer = int(q.get("answer", 0))

            if not text_val or qno < 1:
                continue

            if len(choices) == 4:
                choices = [str(c).strip() for c in choices]
            else:
                choices = ["", "", "", ""]

            if answer not in [1, 2, 3, 4]:
                answer = 0

            result.append(
                {
                    "q_no": qno,
                    "text": text_val,
                    "choices": choices,
                    "answer": answer,
                }
            )
        except (ValueError, TypeError):
            continue

    return result


def get_broken_files() -> list[dict]:
    result = []
    for fp in sorted(DATA_DIR.glob("questions_기출_*.json")):
        qs = json.loads(fp.read_text(encoding="utf-8"))
        defect = classify_defects(qs)
        if defect == "none":
            continue

        pdf = find_pdf_for_json(fp.name)
        if not pdf:
            continue

        broken_count = sum(
            1 for q in qs
            if not (
                q.get("text", "").strip()
                and len(q.get("choices", [])) == 4
                and all(c.strip() for c in q.get("choices", []))
                and q.get("answer", 0) in [1, 2, 3, 4]
            )
        )
        result.append(
            {
                "json_file": fp.name,
                "pdf_path": pdf,
                "defect_type": defect,
                "broken_count": broken_count,
                "total": len(qs),
            }
        )
    return result


def cmd_estimate():
    files = get_broken_files()
    answer_only = [f for f in files if f["defect_type"] == "answer_only"]
    full_repair = [f for f in files if f["defect_type"] == "full"]

    total_pages = 0
    for entry in files:
        doc = fitz.open(str(entry["pdf_path"]))
        total_pages += len(doc)
        doc.close()

    total_broken = sum(f["broken_count"] for f in files)

    input_cost = total_pages * 2300 / 1_000_000 * 0.40
    output_cost = total_pages * 500 / 1_000_000 * 2.00
    total_cost = input_cost + output_cost

    logger.info("=" * 60)
    logger.info("FINAL COMPREHENSIVE REPAIR ESTIMATE")
    logger.info("=" * 60)
    logger.info("Answer-only PDFs: %d (%d broken questions)", len(answer_only), sum(f["broken_count"] for f in answer_only))
    logger.info("Full repair PDFs: %d (%d broken questions)", len(full_repair), sum(f["broken_count"] for f in full_repair))
    logger.info("Total pages: %d", total_pages)
    logger.info("Total broken questions: %d", total_broken)
    logger.info("Model: %s (Batch 50%% discount)", MODEL)
    logger.info("Est. cost: $%.2f", total_cost)
    logger.info("=" * 60)


def cmd_submit():
    files = get_broken_files()
    if not files:
        logger.info("No files need repair.")
        return

    page_mapping = {}
    all_requests = []

    for entry in files:
        pdf_path = entry["pdf_path"]
        json_file = entry["json_file"]
        defect_type = entry["defect_type"]

        doc = fitz.open(str(pdf_path))
        prompt = ANSWER_PROMPT if defect_type == "answer_only" else FULL_PROMPT

        for page_idx in range(len(doc)):
            page = doc[page_idx]
            b64 = page_to_base64(page)

            safe_name = re.sub(
                r"[^a-zA-Z0-9_-]",
                "",
                json_file.replace("questions_기출_", "fr_").replace("회.json", ""),
            )
            custom_id = f"{safe_name}_p{page_idx}"

            page_mapping[custom_id] = {
                "json_file": json_file,
                "pdf_file": _nfc(pdf_path.name),
                "page_num": page_idx,
                "defect_type": defect_type,
            }

            all_requests.append(
                {
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
                                            "data": b64,
                                        },
                                    },
                                    {"type": "text", "text": prompt},
                                ],
                            }
                        ],
                    },
                }
            )

        doc.close()

    MAPPING_FILE.write_text(
        json.dumps(page_mapping, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    logger.info("Total requests: %d pages from %d PDFs", len(all_requests), len(files))

    # Split into batches
    client = anthropic.Anthropic()
    batch_ids = []

    for i in range(0, len(all_requests), MAX_REQUESTS_PER_BATCH):
        chunk = all_requests[i : i + MAX_REQUESTS_PER_BATCH]
        logger.info("Submitting batch %d/%d (%d requests)...",
                     i // MAX_REQUESTS_PER_BATCH + 1,
                     (len(all_requests) + MAX_REQUESTS_PER_BATCH - 1) // MAX_REQUESTS_PER_BATCH,
                     len(chunk))

        batch = client.messages.batches.create(
            requests=[
                {"custom_id": r["custom_id"], "params": r["params"]} for r in chunk
            ]
        )
        batch_ids.append(
            {"batch_id": batch.id, "request_count": len(chunk)}
        )
        logger.info("  Batch ID: %s (status: %s)", batch.id, batch.processing_status)

    BATCH_ID_FILE.write_text(json.dumps(batch_ids, indent=2))
    logger.info("All %d batches submitted.", len(batch_ids))
    logger.info("Next: python scripts/repair_final_batch.py status")


def cmd_status():
    if not BATCH_ID_FILE.exists():
        logger.error("No batch IDs. Run submit first.")
        return

    batch_ids = json.loads(BATCH_ID_FILE.read_text())
    client = anthropic.Anthropic()
    all_done = True

    for entry in batch_ids:
        batch = client.messages.batches.retrieve(entry["batch_id"])
        c = batch.request_counts
        logger.info(
            "Batch %s: %s (ok:%d err:%d proc:%d)",
            entry["batch_id"],
            batch.processing_status,
            c.succeeded,
            c.errored,
            c.processing,
        )
        if batch.processing_status != "ended":
            all_done = False

    if all_done:
        logger.info("All batches complete! Next: python scripts/repair_final_batch.py download")


def cmd_download():
    if not BATCH_ID_FILE.exists() or not MAPPING_FILE.exists():
        logger.error("Missing batch or mapping files.")
        return

    batch_ids = json.loads(BATCH_ID_FILE.read_text())
    page_mapping = json.loads(MAPPING_FILE.read_text(encoding="utf-8"))
    client = anthropic.Anthropic()

    # Collect results per json_file
    file_answers: dict[str, dict[str, int]] = {}
    file_questions: dict[str, list[dict]] = {}
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
            defect_type = m["defect_type"]

            if result.result.type != "succeeded":
                fail += 1
                continue

            raw = "".join(
                b.text for b in result.result.message.content if b.type == "text"
            )

            if defect_type == "answer_only":
                answers = parse_answer_response(raw)
                if answers:
                    if json_file not in file_answers:
                        file_answers[json_file] = {}
                    for qno, ans in answers.items():
                        if qno not in file_answers[json_file]:
                            file_answers[json_file][qno] = ans
                    success += 1
                else:
                    fail += 1
            else:
                questions = parse_full_response(raw)
                answers = parse_answer_response(raw)  # Also try answer extraction
                if questions or answers:
                    if json_file not in file_questions:
                        file_questions[json_file] = []
                    file_questions[json_file].extend(questions)
                    if answers:
                        if json_file not in file_answers:
                            file_answers[json_file] = {}
                        for qno, ans in answers.items():
                            if qno not in file_answers[json_file]:
                                file_answers[json_file][qno] = ans
                    success += 1
                else:
                    fail += 1

    logger.info("Pages: %d with data, %d empty/error", success, fail)

    # Apply fixes
    total_text_fixed = 0
    total_choices_fixed = 0
    total_answer_fixed = 0
    file_stats = []

    all_json_files = set(file_answers.keys()) | set(file_questions.keys())

    for json_file in sorted(all_json_files):
        fp = DATA_DIR / json_file
        if not fp.exists():
            continue

        qs = json.loads(fp.read_text(encoding="utf-8"))
        q_by_no = {q["q_no"]: q for q in qs}

        text_fixed = choices_fixed = answer_fixed = 0

        # Apply full question data
        if json_file in file_questions:
            # Deduplicate by q_no (keep first occurrence)
            seen = set()
            for extracted in file_questions[json_file]:
                qno = extracted["q_no"]
                if qno in seen:
                    continue
                seen.add(qno)

                target = q_by_no.get(qno)
                if not target:
                    continue

                # Fix missing text
                if not target.get("text", "").strip() and extracted["text"]:
                    target["text"] = extracted["text"]
                    text_fixed += 1

                # Fix missing choices
                if not (
                    len(target.get("choices", [])) == 4
                    and all(c.strip() for c in target.get("choices", []))
                ):
                    if len(extracted["choices"]) == 4 and all(
                        c.strip() for c in extracted["choices"]
                    ):
                        target["choices"] = extracted["choices"]
                        choices_fixed += 1

                # Fix missing answer
                if target.get("answer", 0) not in [1, 2, 3, 4]:
                    if extracted["answer"] in [1, 2, 3, 4]:
                        target["answer"] = extracted["answer"]
                        answer_fixed += 1

        # Apply answer-only data
        if json_file in file_answers:
            for qno_str, ans in file_answers[json_file].items():
                qno = int(qno_str)
                target = q_by_no.get(qno)
                if not target:
                    continue
                if target.get("answer", 0) not in [1, 2, 3, 4]:
                    target["answer"] = ans
                    answer_fixed += 1

        total_fixes = text_fixed + choices_fixed + answer_fixed
        if total_fixes > 0:
            fp.write_text(
                json.dumps(qs, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            total_text_fixed += text_fixed
            total_choices_fixed += choices_fixed
            total_answer_fixed += answer_fixed
            file_stats.append(
                {
                    "file": json_file,
                    "text": text_fixed,
                    "choices": choices_fixed,
                    "answer": answer_fixed,
                }
            )
            logger.info(
                "  %s: text=%d choices=%d answer=%d",
                json_file,
                text_fixed,
                choices_fixed,
                answer_fixed,
            )

    REPAIR_LOG.write_text(
        json.dumps(
            {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "total_text_fixed": total_text_fixed,
                "total_choices_fixed": total_choices_fixed,
                "total_answer_fixed": total_answer_fixed,
                "files": file_stats,
            },
            ensure_ascii=False,
            indent=2,
        )
    )

    logger.info("")
    logger.info("=" * 60)
    logger.info("FINAL REPAIR RESULTS")
    logger.info("=" * 60)
    logger.info("Text fixed: %d", total_text_fixed)
    logger.info("Choices fixed: %d", total_choices_fixed)
    logger.info("Answers fixed: %d", total_answer_fixed)
    logger.info("Total fixes: %d", total_text_fixed + total_choices_fixed + total_answer_fixed)
    logger.info("Files updated: %d", len(file_stats))
    logger.info("=" * 60)

    # Post-repair validation
    total_q = complete = 0
    for fp in sorted(DATA_DIR.glob("questions_기출_*.json")):
        qs = json.loads(fp.read_text(encoding="utf-8"))
        for q in qs:
            total_q += 1
            if (
                q.get("text", "").strip()
                and len(q.get("choices", [])) == 4
                and all(c.strip() for c in q.get("choices", []))
                and q.get("answer", 0) in [1, 2, 3, 4]
            ):
                complete += 1

    logger.info(
        "Post-repair: %d/%d complete (%.1f%%)",
        complete,
        total_q,
        complete / total_q * 100,
    )


def main():
    parser = argparse.ArgumentParser(description="Final comprehensive repair batch")
    parser.add_argument(
        "command", choices=["estimate", "submit", "status", "download"]
    )
    args = parser.parse_args()

    {"estimate": cmd_estimate, "submit": cmd_submit, "status": cmd_status, "download": cmd_download}[
        args.command
    ]()


if __name__ == "__main__":
    main()
