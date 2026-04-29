#!/usr/bin/env python3
"""
solution_svg Batch — 풀이 SVG 생성 (회로이론 + 전자기학 미보유 영역)

기존 691건 정책 확장:
- 회로이론 803건 미보유 + 전자기학 1,045건 미보유 = 1,848건 대상
- Sonnet 4.6 batch 50% 할인, 1건당 ~$0.0087, 총 ~$16

Usage:
    python scripts/generate_solution_svg_batch.py estimate    # 비용 추정 ($0)
    python scripts/generate_solution_svg_batch.py submit      # Batch 제출 (결제 발생)
    python scripts/generate_solution_svg_batch.py status      # 상태 확인
    python scripts/generate_solution_svg_batch.py download    # 결과 다운로드
"""

import argparse
import base64
import json
import logging
import re
import time
from pathlib import Path
from typing import Optional

import anthropic

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

# ── paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
BATCH_DIR = DATA_DIR / "batch_solution_svg_v2"
BATCH_DIR.mkdir(exist_ok=True)

REQUESTS_FILE = BATCH_DIR / "requests.jsonl"
BATCH_ID_FILE = BATCH_DIR / "batch_id.txt"
MAPPING_FILE = BATCH_DIR / "id_mapping.json"
FAILED_FILE = BATCH_DIR / "failed_ids.json"

MODEL = "claude-sonnet-4-6"  # SVG 생성은 Sonnet 필요
MAX_TOKENS = 2000  # SVG는 토큰이 더 필요

# ── PDF filename mapping ─────────────────────────────────────────────────────
PDF_DIR = DATA_DIR


def find_pdf_for_question(year: int, session: str) -> Optional[Path]:
    """Find the PDF file matching a question's year and session."""
    session_num = re.sub(r"[^0-9]", "", str(session))
    patterns = [
        f"문제_{year}_{session_num}회_*.pdf",
        f"문제 _{year}_{session_num}회_*.pdf",
        f"{year}*_{session_num}회*.pdf",
    ]
    for pattern in patterns:
        matches = list(PDF_DIR.glob(pattern))
        if matches:
            return matches[0]
    return None


# ── Solution target detection ────────────────────────────────────────────────
TARGET_SUBJECTS = {"회로이론", "전기자기학"}

def find_figure_questions() -> list[dict]:
    """Find all 회로이론+전자기학 questions without solution_svg (with non-empty solution)."""
    figure_qs = []
    files = sorted(DATA_DIR.glob("questions_기출_*.json"))

    for fp in files:
        qs = json.load(open(fp))
        for idx, q in enumerate(qs):
            subject = q.get("subject", "")
            solution = (q.get("solution") or "").strip()
            if subject in TARGET_SUBJECTS and solution:
                figure_qs.append({
                    "file": fp.name,
                    "file_path": str(fp),
                    "index": idx,
                    "year": q.get("year"),
                    "session": q.get("session", ""),
                    "q_no": q.get("q_no"),
                    "subject": subject,
                    "tag": q.get("tag", ""),
                    "text": q.get("text", ""),
                    "choices": q.get("choices", []),
                    "answer": q.get("answer"),
                    "solution": solution,
                    "has_figure_svg": bool(q.get("solution_svg")),  # NOTE: name reused, semantic = has_solution_svg
                })
    return figure_qs


# ── SVG prompt ───────────────────────────────────────────────────────────────
def build_svg_prompt(q: dict) -> str:
    """Build prompt for solution_svg (단계별 풀이 시각화) generation."""
    choices_str = "\n".join(
        f"  {i+1}. {c}" for i, c in enumerate(q.get("choices", []))
    )

    return (
        "전기기사 기출문제의 풀이 과정을 SVG로 단계별 시각화합니다.\n\n"
        f"과목: {q.get('subject', '')}\n"
        f"태그: {q.get('tag', '')}\n"
        f"문제: {q['text'][:400]}\n"
        f"선택지:\n{choices_str}\n\n"
        f"풀이 단계 (이 내용을 SVG로 시각화):\n{q['solution'][:1200]}\n\n"
        "규칙:\n"
        "1. 풀이의 핵심 단계 (공식/대입/계산/결론)를 SVG 박스로 분리해 표현\n"
        "2. viewBox는 '0 0 600 400' 기본 (필요시 조정)\n"
        "3. 배경 없음 (transparent)\n"
        "4. 색상: 공식 #2d6abf, 대입값 #e74c3c, 결론 #27ae60, 레이블 #333\n"
        "5. 한글 레이블 사용, font-size 12~16, 박스 padding 8\n"
        "6. 단계 간 화살표(→) 또는 ∴ 기호로 연결\n"
        "7. 최종 답은 별도 강조 박스 (테두리 + 굵은 글씨)\n"
        "8. 수식은 SVG text로 표현 (LaTeX 불가, 일반 텍스트로 √, ², π 등 사용)\n"
        "9. 제목 박스 상단 (예: '단상 반파 정류 회로 해석')\n\n"
        "출력 형식: SVG 코드만 출력 (```svg 태그 없이, <svg> 태그로 시작하고 </svg>로 종료)\n"
        "다른 설명 없이 순수 SVG 코드만 반환하세요."
    )


def extract_svg(raw: str) -> Optional[str]:
    """Extract SVG code from response text. Auto-close truncated SVGs."""
    # Try complete SVG first
    m = re.search(r"(<svg[\s\S]*?</svg>)", raw, re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Truncated SVG — has <svg> but no </svg> (token limit exceeded)
    m = re.search(r"(<svg[\s\S]+)", raw, re.IGNORECASE)
    if m:
        svg = m.group(1).strip()
        # Close any unclosed tags and add </svg>
        if not svg.endswith("</svg>"):
            svg += "\n</svg>"
        return svg

    return None


# ── Commands ─────────────────────────────────────────────────────────────────
def cmd_estimate() -> None:
    """Estimate cost for SVG generation batch."""
    figure_qs = find_figure_questions()
    need = sum(1 for q in figure_qs if not q["has_figure_svg"])
    done = sum(1 for q in figure_qs if q["has_figure_svg"])

    # Sonnet Batch pricing (50% off)
    input_cost_per_1m = 1.50    # batch: $1.50/1M
    output_cost_per_1m = 7.50   # batch: $7.50/1M

    avg_input_tokens = 500
    avg_output_tokens = 800  # SVG is verbose

    input_cost = need * avg_input_tokens / 1_000_000 * input_cost_per_1m
    output_cost = need * avg_output_tokens / 1_000_000 * output_cost_per_1m
    total_cost = input_cost + output_cost

    # Subject breakdown
    subjects: dict[str, int] = {}
    for q in figure_qs:
        s = q["subject"] or "기타"
        subjects[s] = subjects.get(s, 0) + 1

    log.info(f"전체 '그림' 문제: {len(figure_qs)}")
    log.info(f"SVG 생성 필요: {need}")
    log.info(f"이미 완료: {done}")
    log.info("")
    log.info("과목별 분포:")
    for s, cnt in sorted(subjects.items(), key=lambda x: -x[1]):
        log.info(f"  {s}: {cnt}")
    log.info("")
    log.info(f"모델: {MODEL}")
    log.info(f"예상 입력: {need * avg_input_tokens:,} tokens (${input_cost:.2f})")
    log.info(f"예상 출력: {need * avg_output_tokens:,} tokens (${output_cost:.2f})")
    log.info(f"예상 총 비용: ${total_cost:.2f} (Batch 50% 할인 적용)")
    log.info(f"예상 시간: 최대 24시간 (보통 1~6시간)")


def cmd_submit() -> None:
    """Build and submit SVG generation batch."""
    figure_qs = find_figure_questions()
    targets = [q for q in figure_qs if not q["has_figure_svg"]]

    if not targets:
        log.info("처리할 문제가 없습니다. 모두 완료!")
        return

    id_mapping: dict[str, dict] = {}
    requests: list[dict] = []

    for q in targets:
        safe_stem = re.sub(
            r"[^a-zA-Z0-9_-]", "",
            q["file"].replace("questions_기출_", "sol_").replace("회", ""),
        )
        custom_id = f"{safe_stem}_{q['index']}"

        id_mapping[custom_id] = {"file": q["file"], "index": q["index"]}
        requests.append({
            "custom_id": custom_id,
            "params": {
                "model": MODEL,
                "max_tokens": MAX_TOKENS,
                "messages": [
                    {"role": "user", "content": build_svg_prompt(q)}
                ],
            },
        })

    # Save mapping
    with open(MAPPING_FILE, "w") as f:
        json.dump(id_mapping, f, ensure_ascii=False, indent=2)

    # Write JSONL
    with open(REQUESTS_FILE, "w") as f:
        for req in requests:
            f.write(json.dumps(req, ensure_ascii=False) + "\n")

    log.info(f"요청 {len(requests)}개 생성 → {REQUESTS_FILE}")

    # Submit batch
    client = anthropic.Anthropic()
    log.info("Batch 제출 중...")

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

    with open(BATCH_ID_FILE, "w") as f:
        f.write(batch.id)

    log.info(f"\nBatch 제출 완료!")
    log.info(f"Batch ID: {batch.id}")
    log.info(f"요청 수: {len(requests)}")
    log.info(f"상태: {batch.processing_status}")
    log.info(f"\n다음: python scripts/generate_figures_batch.py status")


def cmd_status() -> None:
    """Check batch status."""
    if not BATCH_ID_FILE.exists():
        log.info("Batch ID가 없습니다. 먼저 submit을 실행하세요.")
        return

    batch_id = BATCH_ID_FILE.read_text().strip()
    client = anthropic.Anthropic()
    batch = client.messages.batches.retrieve(batch_id)

    total = (
        batch.request_counts.processing
        + batch.request_counts.succeeded
        + batch.request_counts.errored
        + batch.request_counts.canceled
        + batch.request_counts.expired
    )

    log.info(f"Batch ID: {batch.id}")
    log.info(f"상태: {batch.processing_status}")
    log.info(f"총 요청: {total}")
    log.info(f"  처리중: {batch.request_counts.processing}")
    log.info(f"  성공: {batch.request_counts.succeeded}")
    log.info(f"  실패: {batch.request_counts.errored}")
    log.info(f"  취소: {batch.request_counts.canceled}")
    log.info(f"  만료: {batch.request_counts.expired}")

    if batch.processing_status == "ended":
        log.info(f"\n완료! 다음: python scripts/generate_figures_batch.py download")


def cmd_download() -> None:
    """Download results and save SVGs to question JSON files."""
    if not BATCH_ID_FILE.exists():
        log.info("Batch ID가 없습니다.")
        return
    if not MAPPING_FILE.exists():
        log.info("매핑 파일이 없습니다.")
        return

    batch_id = BATCH_ID_FILE.read_text().strip()
    id_mapping = json.load(open(MAPPING_FILE))
    client = anthropic.Anthropic()

    batch = client.messages.batches.retrieve(batch_id)
    if batch.processing_status != "ended":
        log.info(f"아직 처리 중: {batch.processing_status}")
        log.info(f"처리중: {batch.request_counts.processing}")
        return

    log.info("결과 다운로드 중...")
    results = list(client.messages.batches.results(batch_id))
    log.info(f"결과 {len(results)}개 다운로드")

    file_updates: dict[str, list[tuple[int, str]]] = {}
    failed_records: list[dict] = []
    success = fail = 0

    for result in results:
        custom_id = result.custom_id
        mapping = id_mapping.get(custom_id)
        if not mapping:
            continue

        file_name = mapping["file"]
        idx = mapping["index"]

        if result.result.type == "succeeded":
            raw = ""
            for block in result.result.message.content:
                if block.type == "text":
                    raw += block.text

            svg = extract_svg(raw)
            if svg:
                if file_name not in file_updates:
                    file_updates[file_name] = []
                file_updates[file_name].append((idx, svg))
                success += 1
            else:
                failed_records.append({
                    "custom_id": custom_id,
                    "file": file_name,
                    "index": idx,
                    "reason": "svg_parse_failed",
                    "detail": "SVG 태그를 찾을 수 없음",
                    "raw_preview": raw[:300] if raw else "(empty)",
                })
                fail += 1
        else:
            error_type = result.result.type
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

    # Save failed records
    if failed_records:
        with open(FAILED_FILE, "w") as f:
            json.dump({
                "batch_id": batch_id,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "model": MODEL,
                "total_failed": len(failed_records),
                "records": failed_records,
            }, f, ensure_ascii=False, indent=2)
        log.info(f"실패 기록 → {FAILED_FILE} ({len(failed_records)}건)")

    # Apply SVGs to JSON files
    log.info(f"\n파일 업데이트 중... ({len(file_updates)}개 파일)")
    for file_name, updates in file_updates.items():
        fp = DATA_DIR / file_name
        qs = json.load(open(fp))
        for idx, svg in updates:
            qs[idx]["solution_svg"] = svg
        with open(fp, "w") as f:
            json.dump(qs, f, ensure_ascii=False, indent=2)
        log.info(f"  {file_name}: {len(updates)}개 SVG 추가")

    log.info(f"\n완료! 성공: {success}, 실패: {fail}")
    if success + fail > 0:
        log.info(f"성공률: {success / (success + fail) * 100:.1f}%")


# ── Main ─────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="그림 문제 SVG 생성 Batch")
    parser.add_argument(
        "command",
        choices=["estimate", "submit", "status", "download"],
        help="estimate/submit/status/download",
    )
    args = parser.parse_args()

    cmds = {
        "estimate": cmd_estimate,
        "submit": cmd_submit,
        "status": cmd_status,
        "download": cmd_download,
    }
    cmds[args.command]()


if __name__ == "__main__":
    main()
