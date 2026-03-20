#!/usr/bin/env python3
"""
Phase 1 전체 실행 — 5,362문제 V3 단일 태깅
- 기존 concept 필드 유지, 새 tag 필드(단일 문자열) 추가
- 파일 단위로 저장 → 중단 후 재시작 가능
- 진행 상황을 data/tag_all_progress.json 에 기록

Usage:
    python scripts/tag_all_questions.py          # 전체 실행
    python scripts/tag_all_questions.py --dry-run # 통계만 출력
    python scripts/tag_all_questions.py --resume  # 이미 처리된 파일 건너뜀
"""

import argparse
import json
import os
import re
import time
from collections import Counter
from pathlib import Path

import anthropic

# ── 경로 ──────────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR     = PROJECT_ROOT / "data"
CONCEPT_MAP  = DATA_DIR / "full_concept_mapping.json"
PROGRESS_FILE = DATA_DIR / "tag_all_progress.json"

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL   = "claude-haiku-4-5-20251001"
DELAY   = 0.25   # 초 (rate limit 대응)

# ── 어휘집 로드 ────────────────────────────────────────────────────────────────
def load_vocabulary() -> list[str]:
    with open(CONCEPT_MAP, encoding="utf-8") as f:
        concept_map = json.load(f)
    vocab = []
    for concepts in concept_map.values():
        for c in concepts:
            name = c["name"] if isinstance(c, dict) else c
            if name not in vocab:
                vocab.append(name)
    return vocab

# ── 프롬프트 ───────────────────────────────────────────────────────────────────
def build_prompt(q: dict, vocab: list[str]) -> str:
    concept_str = (
        ", ".join(q["concept"]) if isinstance(q.get("concept"), list)
        else str(q.get("concept") or "없음")
    )
    tag_list = "\n".join(f"  - {t}" for t in vocab)
    return f"""\
전기기사 문제를 분류합니다.

규칙: 태그 = 이 공식 하나를 알면 풀 수 있다 (공식 1개 = 태그 1개)

나쁜 예: "전자기파"(단원명), "선전하와 도체"(재료묘사)
좋은 예: "고유 임피던스", "영상법", "최종값 정리"

허용 태그 목록 (이 중에서만 선택):
{tag_list}

문제: {q.get("text", "")[:200]}
과목: {q.get("subject", "")}
기존 개념: {concept_str}

[출력 규칙] 태그 이름만 한 줄. 설명·마크다운 절대 금지.
태그:"""

# ── API 호출 + 후처리 ──────────────────────────────────────────────────────────
def clean_tag(raw: str, vocab_set: set) -> str:
    line = raw.strip().split("\n")[0].strip()
    line = re.sub(r"\*+", "", line).strip('"\'').strip()
    # 너무 길거나 설명 패턴이면 파싱 실패
    if len(line) > 80 or any(kw in line[:10] for kw in ["분석", "문제", "이 문제"]):
        return ""
    return line

def call_api(client: anthropic.Anthropic, prompt: str, vocab_set: set) -> str:
    for attempt in range(3):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=60,
                messages=[{"role": "user", "content": prompt}],
            )
            return clean_tag(resp.content[0].text, vocab_set)
        except anthropic.RateLimitError:
            wait = 10 * (attempt + 1)
            print(f"\n  Rate limit — {wait}초 대기...")
            time.sleep(wait)
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
            else:
                return ""
    return ""

# ── 진행 상황 ──────────────────────────────────────────────────────────────────
def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"done_files": [], "total_tagged": 0, "total_questions": 0}

def save_progress(progress: dict) -> None:
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

# ── 단일 파일 처리 ────────────────────────────────────────────────────────────
def process_file(
    fp: Path,
    client: anthropic.Anthropic,
    vocab: list[str],
    vocab_set: set,
    dry_run: bool = False,
) -> dict:
    with open(fp, encoding="utf-8") as f:
        questions = json.load(f)

    needs_tag = [q for q in questions if not q.get("tag")]
    already   = len(questions) - len(needs_tag)

    if dry_run:
        return {"file": fp.name, "total": len(questions),
                "already": already, "to_do": len(needs_tag)}

    tagged_count = 0
    for i, q in enumerate(needs_tag):
        prompt = build_prompt(q, vocab)
        tag = call_api(client, prompt, vocab_set)

        if tag:
            q["tag"] = tag
            tagged_count += 1
        else:
            # 빈 태그: 기존 concept 첫 항목 fallback
            concept = q.get("concept")
            if isinstance(concept, list) and concept:
                q["tag"] = concept[0]
            elif isinstance(concept, str) and concept:
                q["tag"] = concept
            else:
                q["tag"] = "미분류"

        time.sleep(DELAY)

    # 파일 저장
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

    return {
        "file": fp.name,
        "total": len(questions),
        "already": already,
        "new_tagged": tagged_count,
        "fallback": len(needs_tag) - tagged_count,
    }

# ── 메인 ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="통계만 출력, 실제 처리 없음")
    parser.add_argument("--resume",  action="store_true", help="이미 처리된 파일 건너뜀")
    args = parser.parse_args()

    if not API_KEY and not args.dry_run:
        print("ANTHROPIC_API_KEY 환경변수가 없습니다.")
        return

    print("어휘집 로드...")
    vocab     = load_vocabulary()
    vocab_set = set(vocab)
    print(f"  {len(vocab)}개 태그 어휘집 준비 완료")

    files = sorted(DATA_DIR.glob("questions_기출_*.json"))
    print(f"\n대상 파일: {len(files)}개")

    # 진행 상황 로드 (resume 모드)
    progress = load_progress()
    done_files = set(progress.get("done_files", []))

    if args.resume and done_files:
        print(f"Resume 모드: {len(done_files)}개 파일 건너뜀")

    # dry-run: 통계만
    if args.dry_run:
        total_q = 0
        total_need = 0
        for fp in files:
            r = process_file(fp, None, vocab, vocab_set, dry_run=True)
            total_q    += r["total"]
            total_need += r["to_do"]
            if r["to_do"] > 0:
                print(f"  {fp.name}: {r['already']}/{r['total']} 완료, {r['to_do']}개 필요")
        est_min = total_need * DELAY / 60
        print(f"\n총 {total_q}문제 중 {total_need}개 태깅 필요")
        print(f"예상 시간: {est_min:.0f}분 (DELAY={DELAY}s)")
        return

    # 실제 실행
    client = anthropic.Anthropic(api_key=API_KEY)
    grand_total = grand_new = grand_fallback = 0

    for i, fp in enumerate(files, 1):
        fname = fp.name

        # resume 건너뜀
        if args.resume and fname in done_files:
            print(f"[{i:02d}/{len(files)}] SKIP {fname}")
            continue

        print(f"[{i:02d}/{len(files)}] {fname} ...", end=" ", flush=True)
        t0 = time.time()

        result = process_file(fp, client, vocab, vocab_set)
        elapsed = time.time() - t0

        grand_total    += result["total"]
        grand_new      += result["new_tagged"]
        grand_fallback += result["fallback"]

        print(f"새태그 {result['new_tagged']}개 / fallback {result['fallback']}개  ({elapsed:.0f}s)")

        # 진행 저장
        done_files.add(fname)
        progress["done_files"]       = list(done_files)
        progress["total_tagged"]     = grand_total
        progress["total_questions"]  = grand_total
        save_progress(progress)

    print(f"\n완료: {grand_total}문제, 새 태그 {grand_new}개, fallback {grand_fallback}개")
    print(f"결과 저장 위치: {DATA_DIR}/questions_기출_*.json")

    # 최종 통계
    tag_counter: Counter = Counter()
    for fp in files:
        with open(fp, encoding="utf-8") as f:
            qs = json.load(f)
        for q in qs:
            tag_counter[q.get("tag", "미분류")] += 1

    stats_path = DATA_DIR / "tag_stats.json"
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump({"tag_counts": dict(tag_counter.most_common())}, f,
                  ensure_ascii=False, indent=2)
    print(f"태그 통계 저장: {stats_path}")
    print(f"상위 10개 태그: {dict(tag_counter.most_common(10))}")


if __name__ == "__main__":
    main()
