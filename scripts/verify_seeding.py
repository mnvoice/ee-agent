#!/usr/bin/env python3
"""
Layer 2 — DB 시딩 검증 (verify_seeding.py)
knowledge_store 무결성 확인

사용법:
  python3 verify_seeding.py --before 1790 --query "전력계통 안정도"
  python3 verify_seeding.py --store data/knowledge_store_1.json --before 500
"""
import json
import sys
import os
import argparse
import glob
import numpy as np
from pathlib import Path

# ── 불변식 임계값 ──────────────────────────────────────────────
INVARIANTS = {
    "min_text_len":    50,    # 엔트리 최소 텍스트 길이 (자)
    "sample_size":     10,    # 무작위 샘플 검사 수
    "min_entry_ratio": 0.95,  # 시딩 후 엔트리 수가 before 대비 최소 비율
}

PASS = "✅ PASS"
WARN = "⚠️  WARN"
FAIL = "❌ FAIL"

results = []

def check(label, passed, warn=False, detail=""):
    status = PASS if passed else (WARN if warn else FAIL)
    results.append((status, label, detail))
    return passed


def load_all_stores(data_dir: str) -> list:
    """분할 저장된 knowledge_store JSON 파일 전체 로드"""
    all_entries = []
    store_files = sorted(glob.glob(os.path.join(data_dir, "knowledge_store_*.json")))
    if not store_files:
        # 단일 파일 시도
        single = os.path.join(data_dir, "knowledge_store.json")
        if os.path.exists(single):
            store_files = [single]
    for f in store_files:
        with open(f, encoding="utf-8") as fh:
            entries = json.load(fh)
            all_entries.extend(entries)
    return all_entries, store_files


def run(data_dir: str, size_before: int, query: str = None):
    print(f"\n{'='*60}")
    print(f"Layer 2 — DB 시딩 검증: {data_dir}")
    print(f"{'='*60}")

    entries, store_files = load_all_stores(data_dir)
    size_after = len(entries)

    print(f"  로드된 파일: {[os.path.basename(f) for f in store_files]}")
    print(f"  전체 엔트리: {size_after}개")
    print()

    # ── INV-1: 절대 감소 금지 ─────────────────────────────────
    check(
        "INV-1: 시딩 후 엔트리 수 감소 없음 (절대 금지)",
        size_after >= size_before,
        detail=f"before={size_before}, after={size_after} "
               f"({'증가' if size_after >= size_before else '⚠ 감소!'})"
    )

    # ── INV-2: 최소 비율 ──────────────────────────────────────
    ratio = size_after / size_before if size_before > 0 else 1.0
    min_ratio = INVARIANTS["min_entry_ratio"]
    check(
        "INV-2: 시딩 후 엔트리 비율",
        ratio >= min_ratio,
        detail=f"{ratio*100:.1f}% 유지 (임계값: {min_ratio*100:.0f}%)"
    )

    # ── INV-3: 텍스트 최소 길이 샘플링 ───────────────────────
    import random
    sample_n = min(INVARIANTS["sample_size"], size_after)
    sample = random.sample(entries, sample_n) if size_after >= sample_n else entries
    short = [i for i, e in enumerate(sample)
             if len(e.get("text", e.get("content", "")).strip()) < INVARIANTS["min_text_len"]]
    check(
        f"INV-3: 엔트리 텍스트 최소 길이 (>{INVARIANTS['min_text_len']}자, 샘플 {sample_n}개)",
        len(short) == 0,
        warn=len(short) > 0,
        detail=f"짧은 엔트리 {len(short)}개" if short else "전체 정상"
    )

    # ── INV-4: 과목 태깅 N/A 비율 ────────────────────────────
    na_count = sum(1 for e in entries
                   if e.get("subject", "N/A").strip() in ("N/A", "", "null", "None"))
    na_rate = na_count / size_after if size_after else 0
    max_na = 0.05  # N/A 5% 이하
    check(
        "INV-4: 과목 태깅 N/A 비율",
        na_rate <= max_na,
        warn=0.01 < na_rate <= max_na,
        detail=f"{na_count}/{size_after} ({na_rate*100:.1f}%) — 임계값: {max_na*100:.0f}%"
    )

    # ── INV-5: 벡터 파일 정합성 ──────────────────────────────
    vec_file = os.path.join(data_dir, "knowledge_store.npy")
    if os.path.exists(vec_file):
        vecs = np.load(vec_file)
        vec_count = vecs.shape[0]
        check(
            "INV-5: 벡터 수 ≈ 엔트리 수",
            abs(vec_count - size_after) <= 5,
            detail=f"벡터 {vec_count}개 vs 엔트리 {size_after}개"
        )
    else:
        results.append((WARN, "INV-5: 벡터 파일 없음", f"{vec_file} 미존재"))

    # ── INV-6: 대표 쿼리 응답 확인 (옵션) ────────────────────
    if query:
        # 키워드 매칭으로 간단히 확인 (SBERT 없이)
        keyword = query.split()[0]
        hits = [e for e in entries
                if keyword in e.get("text", e.get("content", ""))]
        check(
            f"INV-6: 대표 쿼리 '{keyword}' 검색 결과",
            len(hits) > 0,
            warn=len(hits) == 0,
            detail=f"{len(hits)}건 hit"
        )

    # ── 리포트 출력 ────────────────────────────────────────────
    print()
    fails = 0
    warns = 0
    for status, label, detail in results:
        print(f"  {status}  {label}")
        if detail:
            print(f"           {detail}")
        if status.startswith("❌"):
            fails += 1
        elif status.startswith("⚠️"):
            warns += 1

    print(f"\n{'─'*60}")
    print(f"  결과: FAIL {fails}개 / WARN {warns}개 / PASS {len(results)-fails-warns}개")
    if fails > 0:
        print("  → 시딩 실패. 백업에서 복원 후 재시딩 필요.")
    elif warns > 0:
        print("  → 경고 항목 확인 권장.")
    else:
        print("  → DB 시딩 정상. 파이프라인 실행 가능.")
    print(f"{'='*60}\n")

    return fails


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default="data", help="knowledge_store 폴더 경로")
    parser.add_argument("--before", type=int, required=True, help="시딩 전 엔트리 수")
    parser.add_argument("--query", default=None, help="대표 쿼리 키워드 (선택)")
    args = parser.parse_args()

    fails = run(args.dir, args.before, args.query)
    sys.exit(1 if fails > 0 else 0)
