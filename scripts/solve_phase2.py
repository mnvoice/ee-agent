#!/usr/bin/env python3
"""
Phase 2 — 3단계 풀이 구조 생성 (Claude Code CLI 사용, API 키 불필요)
[문제 인식] → [문제 변환] → [계산]

Usage:
    python scripts/solve_phase2.py           # 전체 실행
    python scripts/solve_phase2.py --dry-run # 통계만 출력
    python scripts/solve_phase2.py --resume  # steps 없는 문제만 처리
"""

import argparse
import asyncio
import json
import re
import time
from pathlib import Path

# ── 경로 ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT  = Path(__file__).parent.parent
DATA_DIR      = PROJECT_ROOT / "data"
PROGRESS_FILE = DATA_DIR / "solve_phase2_progress.json"

CONCURRENCY   = 5    # claude -p 프로세스 동시 실행 수
CLAUDE_BIN    = "/Users/jeong-ujin_1/.npm-global/bin/claude"
CALL_TIMEOUT  = 240  # 초

# ── 프롬프트 ──────────────────────────────────────────────────────────────────
def build_prompt(q: dict) -> str:
    choices = q.get("choices", [])
    choices_str = "\n".join(f"  {i+1}. {c}" for i, c in enumerate(choices))
    answer_idx  = q.get("answer", 0)
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

# ── 출력 파싱 ──────────────────────────────────────────────────────────────────
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

# ── claude -p 호출 ─────────────────────────────────────────────────────────────
async def call_claude(prompt: str, semaphore: asyncio.Semaphore) -> str:
    async with semaphore:
        for attempt in range(3):
            try:
                proc = await asyncio.create_subprocess_exec(
                    CLAUDE_BIN, "-p", prompt,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await asyncio.wait_for(
                    proc.communicate(), timeout=CALL_TIMEOUT
                )
                if proc.returncode == 0:
                    return stdout.decode("utf-8", errors="replace").strip()
                # 실패 시 잠시 대기 후 재시도
                await asyncio.sleep(5 * (attempt + 1))
            except asyncio.TimeoutError:
                print(f"\n  Timeout (시도 {attempt+1}/3)...")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"\n  오류: {e}")
                await asyncio.sleep(3)
        return ""

# ── 단일 파일 처리 ─────────────────────────────────────────────────────────────
async def process_file(
    fp: Path,
    semaphore: asyncio.Semaphore | None,
    dry_run: bool = False,
) -> dict:
    with open(fp, encoding="utf-8") as f:
        questions = json.load(f)

    needs   = [q for q in questions if not _has_valid_steps(q)]
    already = len(questions) - len(needs)

    if dry_run:
        return {"file": fp.name, "total": len(questions),
                "already": already, "to_do": len(needs)}

    if not needs:
        return {"file": fp.name, "total": len(questions),
                "already": already, "new": 0, "failed": 0}

    async def process_one(q: dict) -> bool:
        raw = await call_claude(build_prompt(q), semaphore)
        if raw:
            steps = parse_steps(raw)
            if is_valid_steps(steps):
                q["steps"] = steps
                return True
        q["steps"] = {"인식": "", "변환": "", "계산": ""}
        return False

    results = await asyncio.gather(*[process_one(q) for q in needs])

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    return {
        "file": fp.name, "total": len(questions), "already": already,
        "new": sum(results), "failed": len(results) - sum(results),
    }

# ── 진행 상황 ──────────────────────────────────────────────────────────────────
def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"done_files": []}

def save_progress(progress: dict) -> None:
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

# ── 메인 ──────────────────────────────────────────────────────────────────────
async def main_async(args):
    files = sorted(DATA_DIR.glob("questions_기출_*.json"))
    print(f"대상 파일: {len(files)}개  (병렬: {CONCURRENCY})\n")

    if args.dry_run:
        total_q = total_need = 0
        for fp in files:
            r = await process_file(fp, None, dry_run=True)
            total_q    += r["total"]
            total_need += r["to_do"]
            if r["to_do"] > 0:
                print(f"  {fp.name}: {r['already']}/{r['total']} 완료, {r['to_do']}개 필요")
        avg_sec = 10  # claude -p 호출당 평균 10초 추정
        est_min = total_need * avg_sec / CONCURRENCY / 60
        print(f"\n총 {total_q}문제 중 {total_need}개 처리 필요")
        print(f"예상 시간: ~{est_min:.0f}분 ({CONCURRENCY} 병렬, 문제당 ~{avg_sec}초)")
        return

    semaphore = asyncio.Semaphore(CONCURRENCY)
    progress  = load_progress()
    done_files = set(progress.get("done_files", []))

    grand_total = grand_new = grand_failed = 0

    for i, fp in enumerate(files, 1):
        fname = fp.name
        if args.resume and fname in done_files:
            print(f"[{i:02d}/{len(files)}] SKIP {fname}")
            continue

        print(f"[{i:02d}/{len(files)}] {fname} ...", end=" ", flush=True)
        t0 = time.time()

        result  = await process_file(fp, semaphore)
        elapsed = time.time() - t0

        grand_total  += result["total"]
        grand_new    += result["new"]
        grand_failed += result["failed"]

        print(f"새 steps {result['new']}개 / fallback {result['failed']}개  ({elapsed:.0f}s)")

        done_files.add(fname)
        progress["done_files"] = list(done_files)
        save_progress(progress)

    print(f"\n완료: {grand_total}문제, 새 steps {grand_new}개, fallback {grand_failed}개")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="통계만 출력")
    parser.add_argument("--resume",  action="store_true", help="완료 파일 건너뜀")
    args = parser.parse_args()
    asyncio.run(main_async(args))

if __name__ == "__main__":
    main()
