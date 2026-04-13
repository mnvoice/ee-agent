#!/usr/bin/env python3
"""
Layer 3 — 실행 결과 검증 (verify_results.py)
ee-agent results_*.json 자동 검증

사용법:
  python3 verify_results.py output/results_2020_after_rag.json
  python3 verify_results.py output/results_2020_after_rag.json \
          --prev output/results_2020_before_rag.json
"""
import json
import sys
import os
import argparse
from collections import Counter, defaultdict

# ── 불변식 임계값 ──────────────────────────────────────────────
INVARIANTS = {
    "subject_gap_max":        30,   # 과목별 정답률 편차 최대 (%)
    "fallback_rate_max":      0.50, # confidence==0.85 비율 최대 50%
    "regression_delta_max":   3,    # 이전 대비 정답 수 변동 허용 ±3
    "suspicious_keywords":    ["retry", "unknown", "없음", "모름", "불확실"],
    "stem_ocr_len_threshold": 100,  # stem 길이 < 이 값이면 수식 소실 의심
    "confidence_fallback":    0.85, # fallback confidence 값
}

PASS = "✅ PASS"
WARN = "⚠️  WARN"
FAIL = "❌ FAIL"

results = []

def check(label, passed, warn=False, detail=""):
    status = PASS if passed else (WARN if warn else FAIL)
    results.append((status, label, detail))
    return passed


def run(curr_path: str, prev_path: str = None):
    print(f"\n{'='*60}")
    print(f"Layer 3 — 실행 결과 검증: {curr_path}")
    print(f"{'='*60}")

    with open(curr_path, encoding="utf-8") as f:
        raw = json.load(f)

    # results 구조 정규화
    if isinstance(raw, dict):
        questions = list(raw.values())
    else:
        questions = raw

    total = len(questions)
    correct = sum(1 for q in questions if q.get("is_correct"))
    accuracy = correct / total if total else 0
    print(f"  문제 수: {total}, 정답: {correct} ({accuracy*100:.1f}%)")
    print()

    # ── INV-1: 과목별 정답률 편차 ─────────────────────────────
    subject_stats = defaultdict(lambda: {"t": 0, "c": 0})
    for q in questions:
        s = q.get("subject", "?").strip()
        subject_stats[s]["t"] += 1
        if q.get("is_correct"):
            subject_stats[s]["c"] += 1

    rates = {}
    for s, v in subject_stats.items():
        if v["t"] > 0:
            rates[s] = v["c"] / v["t"] * 100

    if rates:
        gap = max(rates.values()) - min(rates.values())
        max_gap = INVARIANTS["subject_gap_max"]
        worst = min(rates, key=rates.get)
        detail_lines = [f"{s}: {r:.0f}%" for s, r in sorted(rates.items(), key=lambda x: x[1])]
        check(
            f"INV-1: 과목별 정답률 편차 (임계값: >{max_gap}%p)",
            gap <= max_gap,
            warn=max_gap * 0.7 < gap <= max_gap,
            detail=f"편차 {gap:.0f}%p | 최저: {worst} {rates[worst]:.0f}% | "
                   + " / ".join(detail_lines)
        )

    # ── INV-2: fallback confidence 비율 ───────────────────────
    fb_val = INVARIANTS["confidence_fallback"]
    fb_count = sum(1 for q in questions
                   if q.get("confidence") == fb_val or
                   q.get("final_confidence") == fb_val)
    fb_rate = fb_count / total if total else 0
    max_fb = INVARIANTS["fallback_rate_max"]
    check(
        f"INV-2: fallback confidence({fb_val}) 비율",
        fb_rate <= max_fb,
        warn=max_fb * 0.7 < fb_rate <= max_fb,
        detail=f"{fb_count}/{total} ({fb_rate*100:.1f}%) — 임계값: {max_fb*100:.0f}%"
    )

    # ── INV-3: 회귀 비교 (prev 있을 때만) ────────────────────
    if prev_path and os.path.exists(prev_path):
        with open(prev_path, encoding="utf-8") as f:
            prev_raw = json.load(f)
        prev_qs = list(prev_raw.values()) if isinstance(prev_raw, dict) else prev_raw
        prev_correct = sum(1 for q in prev_qs if q.get("is_correct"))
        delta = correct - prev_correct
        max_delta = INVARIANTS["regression_delta_max"]
        check(
            f"INV-3: 이전 대비 정답 수 변동 (허용: ±{max_delta})",
            abs(delta) <= max_delta,
            warn=-max_delta <= delta < 0,
            detail=f"이전={prev_correct} / 현재={correct} / 변동={delta:+d}"
        )
        # 이전에 맞고 지금 틀린 문제 (회귀)
        prev_map = {}
        for q in prev_qs:
            qno = q.get("question_number") or q.get("q_no")
            prev_map[qno] = q.get("is_correct")
        regressions = []
        for q in questions:
            qno = q.get("question_number") or q.get("q_no")
            if prev_map.get(qno) is True and not q.get("is_correct"):
                regressions.append(qno)
        check(
            "INV-3b: 회귀 문제 (이전 정답 → 현재 오답)",
            len(regressions) == 0,
            warn=len(regressions) > 0,
            detail=f"회귀: {regressions}" if regressions else "없음"
        )

    # ── INV-4: stem 소실 의심 문제 플래그 ────────────────────
    ocr_suspects = []
    for q in questions:
        stem = q.get("text", q.get("question", ""))
        q_type = q.get("q_type", q.get("question_type", ""))
        if (len(stem) < INVARIANTS["stem_ocr_len_threshold"]
                and "계산" in q_type):
            ocr_suspects.append(q.get("question_number") or q.get("q_no"))
    check(
        f"INV-4: stem 소실 의심 문제 (길이<{INVARIANTS['stem_ocr_len_threshold']}자 + 계산형)",
        len(ocr_suspects) == 0,
        warn=len(ocr_suspects) > 0,
        detail=f"의심 문제: {ocr_suspects}" if ocr_suspects else "없음"
    )

    # ── INV-5: reasoning_trace 이상 키워드 ───────────────────
    suspicious = INVARIANTS["suspicious_keywords"]
    sus_qs = []
    for q in questions:
        trace = str(q.get("reasoning_trace", q.get("reasoning", "")))
        if any(kw in trace for kw in suspicious):
            sus_qs.append(q.get("question_number") or q.get("q_no"))
    check(
        "INV-5: reasoning 이상 키워드 (retry/unknown 등)",
        len(sus_qs) == 0,
        warn=len(sus_qs) > 0,
        detail=f"이상 문제: {sus_qs[:10]}" if sus_qs else "없음"
    )

    # ── INV-6: law_used ↔ stem 교차 확인 ─────────────────────
    hallucination_suspects = []
    for q in questions:
        if q.get("is_correct"):
            continue
        law = q.get("law_used", "")
        stem = q.get("text", q.get("question", ""))
        # law에 G(s)나 수식이 있는데 stem에는 없는 경우
        if ("G(s)" in law or "H(s)" in law) and ("G(s)" not in stem and "H(s)" not in stem):
            hallucination_suspects.append(q.get("question_number") or q.get("q_no"))
    check(
        "INV-6: law_used ↔ stem 할루시네이션 의심 (수식 불일치)",
        len(hallucination_suspects) == 0,
        warn=len(hallucination_suspects) > 0,
        detail=f"의심 문제: {hallucination_suspects}" if hallucination_suspects else "없음"
    )

    # ── 격리 리스트 출력 ──────────────────────────────────────
    all_flagged = list(set(ocr_suspects + sus_qs + hallucination_suspects))
    if all_flagged:
        print(f"\n  📋 격리 대상 문제: {sorted(all_flagged)}")
        print(f"  → stem Vision OCR 또는 수동 확인 권장")

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
    print(f"  정답률: {correct}/{total} ({accuracy*100:.1f}%)")
    if fails > 0:
        print("  → 심각한 문제 발견. 파이프라인 재점검 필요.")
    elif warns > 0:
        print("  → 경고 항목 수동 확인 권장.")
    else:
        print("  → 실행 결과 정상.")
    print(f"{'='*60}\n")

    return fails


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("results", help="현재 results JSON 파일")
    parser.add_argument("--prev", default=None, help="이전 results JSON (회귀 비교용)")
    args = parser.parse_args()

    fails = run(args.results, args.prev)
    sys.exit(1 if fails > 0 else 0)
