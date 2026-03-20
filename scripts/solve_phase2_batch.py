#!/usr/bin/env python3
"""
Phase 2 — Anthropic Message Batches API (50% discount, 24h turnaround)

Usage:
    # Step 1: Submit batch
    python scripts/solve_phase2_batch.py submit

    # Step 2: Check status
    python scripts/solve_phase2_batch.py status

    # Step 3: Download results and apply
    python scripts/solve_phase2_batch.py download

    # One-shot dry run (cost estimate)
    python scripts/solve_phase2_batch.py estimate
"""

import argparse
import json
import re
import time
from pathlib import Path

import anthropic

# ── paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BATCH_DIR = DATA_DIR / "batch_phase2"
BATCH_DIR.mkdir(exist_ok=True)

REQUESTS_FILE = BATCH_DIR / "requests.jsonl"
BATCH_ID_FILE = BATCH_DIR / "batch_id.txt"
RESULTS_FILE = BATCH_DIR / "results.jsonl"
MAPPING_FILE = BATCH_DIR / "id_mapping.json"
FAILED_FILE = BATCH_DIR / "failed_ids.json"

MODEL = "claude-haiku-4-5-20251001"  # Haiku first strategy
MAX_TOKENS = 800


# ── prompt (same as solve_phase2.py) ─────────────────────────────────────────
def build_prompt(q: dict) -> str:
    choices = q.get("choices", [])
    choices_str = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(choices))
    answer_idx = q.get("answer", 0)
    answer_text = (
        choices[answer_idx]
        if isinstance(answer_idx, int) and 0 <= answer_idx < len(choices)
        else str(answer_idx)
    )

    solution_section = ""
    if q.get("solution", "").strip():
        sol = q["solution"].strip()[:500]
        solution_section = f"\n참고 풀이:\n{sol}\n"

    tag = q.get("tag") or (
        q["concept"][0] if isinstance(q.get("concept"), list) and q["concept"] else "?"
    )

    return (
        f"전기기사 기출문제 풀이를 3단계로 작성합니다.\n\n"
        f"태그(핵심 개념): {tag}\n"
        f"과목: {q.get('subject', '')}\n"
        f"문제: {q.get('text', '')[:300]}\n"
        f"선택지:\n{choices_str}\n"
        f"정답: {answer_text}"
        f"{solution_section}\n\n"
        f"아래 형식으로만 출력하세요 (다른 말 없이):\n"
        f"===인식===\n"
        f'왜 "{tag}" 문제인가? 어떤 조건/키워드가 이 개념을 가리키는가? (2~3문장)\n'
        f"===변환===\n"
        f"어떻게 풀 수 있는 형태로 바꾸는가? 핵심 공식을 KaTeX(\\(...\\) 또는 \\[...\\])로 포함.\n"
        f"===계산===\n"
        f"수치 대입 및 단계별 계산. KaTeX 수식 사용. 정답 명시."
    )


def parse_steps(raw: str) -> dict:
    sections = {"인식": "", "변환": "", "계산": ""}
    for key in ["인식", "변환", "계산"]:
        m = re.search(rf"==={key}===(.+?)(?====|\Z)", raw, re.DOTALL)
        if m:
            sections[key] = m.group(1).strip()
    return sections


def is_valid_steps(steps: dict) -> bool:
    return all(steps.get(k, "").strip() for k in ["인식", "변환", "계산"])


def _has_valid_steps(q: dict) -> bool:
    s = q.get("steps")
    return bool(s) and is_valid_steps(s)


# ── Step 0: Estimate cost ────────────────────────────────────────────────────
def cmd_estimate():
    files = sorted(DATA_DIR.glob("questions_기출_*.json"))
    total = need = 0
    for fp in files:
        qs = json.load(open(fp))
        for q in qs:
            total += 1
            if not _has_valid_steps(q):
                need += 1

    # Haiku pricing (batch = 50% off)
    input_cost_per_1m = 0.40   # batch: $0.40/1M (regular $0.80)
    output_cost_per_1m = 2.00  # batch: $2.00/1M (regular $4.00)

    avg_input_tokens = 700
    avg_output_tokens = 400

    input_cost = need * avg_input_tokens / 1_000_000 * input_cost_per_1m
    output_cost = need * avg_output_tokens / 1_000_000 * output_cost_per_1m
    total_cost = input_cost + output_cost

    print(f"총 문제: {total}")
    print(f"처리 필요: {need}")
    print(f"이미 완료: {total - need}")
    print()
    print(f"모델: {MODEL}")
    print(f"예상 입력: {need * avg_input_tokens:,} tokens (${input_cost:.2f})")
    print(f"예상 출력: {need * avg_output_tokens:,} tokens (${output_cost:.2f})")
    print(f"예상 총 비용: ${total_cost:.2f} (Batch 50% 할인 적용)")
    print(f"예상 시간: 최대 24시간 (보통 1~6시간)")


# ── Step 1: Build requests and submit ────────────────────────────────────────
def cmd_submit():
    files = sorted(DATA_DIR.glob("questions_기출_*.json"))

    # Build ID mapping: custom_id -> (file_path, question_index)
    id_mapping = {}
    requests = []

    for fp in files:
        qs = json.load(open(fp))
        for idx, q in enumerate(qs):
            if _has_valid_steps(q):
                continue

            # custom_id must be [a-zA-Z0-9_-]{1,64}
            safe_stem = re.sub(r'[^a-zA-Z0-9_-]', '', fp.stem.replace("questions_기출_", "q_").replace("회", ""))
            custom_id = f"{safe_stem}_{idx}"
            id_mapping[custom_id] = {"file": fp.name, "index": idx}

            request = {
                "custom_id": custom_id,
                "params": {
                    "model": MODEL,
                    "max_tokens": MAX_TOKENS,
                    "messages": [
                        {"role": "user", "content": build_prompt(q)}
                    ]
                }
            }
            requests.append(request)

    if not requests:
        print("처리할 문제가 없습니다. 모두 완료!")
        return

    # Save mapping
    with open(MAPPING_FILE, "w") as f:
        json.dump(id_mapping, f, ensure_ascii=False, indent=2)

    # Write JSONL requests file
    with open(REQUESTS_FILE, "w") as f:
        for req in requests:
            f.write(json.dumps(req, ensure_ascii=False) + "\n")

    print(f"요청 {len(requests)}개 생성 완료 → {REQUESTS_FILE}")
    print(f"매핑 저장 → {MAPPING_FILE}")

    # Submit batch
    client = anthropic.Anthropic()
    print("\nBatch 제출 중...")

    batch = client.messages.batches.create(
        requests=[
            {
                "custom_id": req["custom_id"],
                "params": {
                    "model": req["params"]["model"],
                    "max_tokens": req["params"]["max_tokens"],
                    "messages": req["params"]["messages"],
                },
            }
            for req in requests
        ]
    )

    # Save batch ID
    with open(BATCH_ID_FILE, "w") as f:
        f.write(batch.id)

    print(f"\nBatch 제출 완료!")
    print(f"Batch ID: {batch.id}")
    print(f"요청 수: {len(requests)}")
    print(f"상태: {batch.processing_status}")
    print(f"\n다음 단계: python scripts/solve_phase2_batch.py status")


# ── Step 2: Check status ─────────────────────────────────────────────────────
def cmd_status():
    if not BATCH_ID_FILE.exists():
        print("Batch ID가 없습니다. 먼저 submit을 실행하세요.")
        return

    batch_id = BATCH_ID_FILE.read_text().strip()
    client = anthropic.Anthropic()

    batch = client.messages.batches.retrieve(batch_id)

    print(f"Batch ID: {batch.id}")
    print(f"상태: {batch.processing_status}")
    print(f"요청 수: {batch.request_counts.processing + batch.request_counts.succeeded + batch.request_counts.errored + batch.request_counts.canceled + batch.request_counts.expired}")
    print(f"  처리중: {batch.request_counts.processing}")
    print(f"  성공: {batch.request_counts.succeeded}")
    print(f"  실패: {batch.request_counts.errored}")
    print(f"  취소: {batch.request_counts.canceled}")
    print(f"  만료: {batch.request_counts.expired}")

    if batch.processing_status == "ended":
        print(f"\n처리 완료! 다음 단계: python scripts/solve_phase2_batch.py download")


# ── Step 3: Download and apply results ───────────────────────────────────────
def cmd_download():
    if not BATCH_ID_FILE.exists():
        print("Batch ID가 없습니다.")
        return
    if not MAPPING_FILE.exists():
        print("매핑 파일이 없습니다.")
        return

    batch_id = BATCH_ID_FILE.read_text().strip()
    id_mapping = json.load(open(MAPPING_FILE))
    client = anthropic.Anthropic()

    # Check status first
    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status != "ended":
        print(f"아직 처리 중입니다. 상태: {batch.processing_status}")
        print(f"처리중: {batch.request_counts.processing}")
        return

    # Download results
    print("결과 다운로드 중...")
    results = []
    for result in client.messages.batches.results(batch_id):
        results.append(result)

    print(f"결과 {len(results)}개 다운로드 완료")

    # Group by file
    file_updates = {}  # file_name -> [(index, steps), ...]
    failed_records = []  # failed ID records for tech support
    success = fail = 0

    for result in results:
        custom_id = result.custom_id
        mapping = id_mapping.get(custom_id)
        if not mapping:
            continue

        file_name = mapping["file"]
        idx = mapping["index"]

        if result.result.type == "succeeded":
            # Extract text from response
            raw = ""
            for block in result.result.message.content:
                if block.type == "text":
                    raw += block.text

            steps = parse_steps(raw)
            if is_valid_steps(steps):
                if file_name not in file_updates:
                    file_updates[file_name] = []
                file_updates[file_name].append((idx, steps))
                success += 1
            else:
                failed_records.append({
                    "custom_id": custom_id,
                    "file": file_name,
                    "index": idx,
                    "reason": "parse_failed",
                    "detail": "3단계(인식/변환/계산) 파싱 실패 — 일부 섹션 누락",
                    "raw_preview": raw[:200] if raw else "(empty)",
                })
                fail += 1
        else:
            error_type = result.result.type  # "errored", "canceled", "expired"
            error_detail = ""
            if hasattr(result.result, "error") and result.result.error:
                error_detail = str(result.result.error)
            failed_records.append({
                "custom_id": custom_id,
                "file": file_name,
                "index": idx,
                "reason": error_type,
                "detail": error_detail or f"Batch API {error_type}",
            })
            fail += 1

    # Save failed IDs for tech support
    if failed_records:
        with open(FAILED_FILE, "w") as f:
            json.dump({
                "batch_id": batch_id,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "model": MODEL,
                "total_failed": len(failed_records),
                "records": failed_records,
            }, f, ensure_ascii=False, indent=2)
        print(f"\n실패 기록 저장 → {FAILED_FILE} ({len(failed_records)}건)")

    # Apply updates to JSON files
    print(f"\n파일 업데이트 중... ({len(file_updates)}개 파일)")
    for file_name, updates in file_updates.items():
        fp = DATA_DIR / file_name
        qs = json.load(open(fp))
        for idx, steps in updates:
            qs[idx]["steps"] = steps
        with open(fp, "w") as f:
            json.dump(qs, f, ensure_ascii=False, indent=2)
        print(f"  {file_name}: {len(updates)}개 업데이트")

    print(f"\n완료!")
    print(f"성공: {success}")
    print(f"실패: {fail}")
    if success + fail > 0:
        print(f"성공률: {success/(success+fail)*100:.1f}%")
    if failed_records:
        print(f"\n기술 지원용 실패 기록: {FAILED_FILE}")
        print(f"Batch ID: {batch_id} (Anthropic 지원팀에 제출 가능)")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Phase 2 Batch API")
    parser.add_argument("command", choices=["estimate", "submit", "status", "download"],
                        help="estimate: cost estimate, submit: submit batch, "
                             "status: check progress, download: apply results")
    args = parser.parse_args()

    if args.command == "estimate":
        cmd_estimate()
    elif args.command == "submit":
        cmd_submit()
    elif args.command == "status":
        cmd_status()
    elif args.command == "download":
        cmd_download()


if __name__ == "__main__":
    main()
