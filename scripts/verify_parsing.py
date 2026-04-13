#!/usr/bin/env python3
"""
Layer 1 — 파싱 검증 (verify_parsing.py)
ee-agent용 verify-agent 불변식 검사

사용법:
  python3 verify_parsing.py data/questions_기출_2020_1회.json
  python3 verify_parsing.py data/questions_기출_2022_2회.json
"""
import json
import sys
import os
from pathlib import Path
from collections import Counter

# ── 불변식 임계값 ──────────────────────────────────────────────
INVARIANTS = {
    "parsed_rate_min":    0.95,   # 파싱 성공률 최소 95%
    "needs_ocr_rate_max": 0.25,   # OCR 필요 비율 최대 25%
    "choice_min_len":     5,      # 선택지 최소 글자 수
    "ocr_placeholder":   "[formula - OCR required]",
    "subjects_required": {        # 6과목 필수
        "전기자기학", "전력공학", "전기기기",
        "회로이론", "제어공학", "전기설비기술기준"
    },
    "total_questions_range": (75, 110),  # 문제 수 허용 범위
}

PASS = "✅ PASS"
WARN = "⚠️  WARN"
FAIL = "❌ FAIL"

results = []

def check(label, passed, warn=False, detail=""):
    status = PASS if passed else (WARN if warn else FAIL)
    results.append((status, label, detail))
    return passed


def run(filepath: str):
    print(f"\n{'='*60}")
    print(f"Layer 1 — 파싱 검증: {filepath}")
    print(f"{'='*60}")

    if not os.path.exists(filepath):
        print(f"{FAIL} 파일 없음: {filepath}")
        sys.exit(1)

    with open(filepath, encoding="utf-8") as f:
        data = json.load(f)

    questions = data if isinstance(data, list) else list(data.values())
    total = len(questions)

    # ── INV-1: 문제 수 범위 ────────────────────────────────────
    lo, hi = INVARIANTS["total_questions_range"]
    check(
        "INV-1: 문제 수 범위",
        lo <= total <= hi,
        detail=f"{total}문제 (허용: {lo}~{hi})"
    )

    # ── INV-2: needs_ocr 비율 ──────────────────────────────────
    ocr_count = sum(1 for q in questions if q.get("needs_ocr") or q.get("quality") == "needs_ocr")
    ocr_rate = ocr_count / total if total else 0
    max_rate = INVARIANTS["needs_ocr_rate_max"]
    is_warn = ocr_rate > max_rate
    check(
        "INV-2: needs_ocr 비율",
        not is_warn,
        warn=is_warn,
        detail=f"{ocr_count}/{total} ({ocr_rate*100:.1f}%) — 임계값: {max_rate*100:.0f}%"
    )

    # ── INV-3: 파싱 성공률 ─────────────────────────────────────
    parsed = sum(1 for q in questions if q.get("text") and len(q["text"].strip()) > 5)
    parse_rate = parsed / total if total else 0
    min_rate = INVARIANTS["parsed_rate_min"]
    check(
        "INV-3: 파싱 성공률",
        parse_rate >= min_rate,
        detail=f"{parsed}/{total} ({parse_rate*100:.1f}%) — 임계값: {min_rate*100:.0f}%"
    )

    # ── INV-4: OCR 플레이스홀더 잔존 ──────────────────────────
    placeholder = INVARIANTS["ocr_placeholder"]
    ph_in_choices = []
    for q in questions:
        choices = q.get("choices", [])
        for c in choices:
            if isinstance(c, str) and placeholder in c:
                ph_in_choices.append(q.get("q_no", "?"))
    check(
        "INV-4: OCR 플레이스홀더 잔존 (선택지)",
        len(ph_in_choices) == 0,
        detail=f"잔존 문제: {ph_in_choices[:10]}" if ph_in_choices else "없음"
    )

    # ── INV-5: 선택지 최소 길이 ───────────────────────────────
    short_choices = []
    for q in questions:
        choices = q.get("choices", [])
        for i, c in enumerate(choices):
            if isinstance(c, str) and len(c.strip()) < INVARIANTS["choice_min_len"]:
                short_choices.append(f"Q{q.get('q_no','?')}-{i+1}")
    check(
        "INV-5: 선택지 최소 길이 (>5자)",
        len(short_choices) == 0,
        warn=len(short_choices) > 0,
        detail=f"짧은 선택지: {short_choices[:5]}" if short_choices else "없음"
    )

    # ── INV-6: 6과목 존재 ─────────────────────────────────────
    subjects_found = set()
    for q in questions:
        s = q.get("subject", "").strip()
        if s:
            subjects_found.add(s)
    required = INVARIANTS["subjects_required"]
    missing = required - subjects_found
    check(
        "INV-6: 6과목 분포 (최소 1문제씩)",
        len(missing) == 0,
        detail=f"누락 과목: {missing}" if missing else f"발견: {len(subjects_found)}과목"
    )

    # ── INV-7: 중복 문제 번호 ─────────────────────────────────
    q_nos = [q.get("q_no") for q in questions if q.get("q_no") is not None]
    dup = [k for k, v in Counter(q_nos).items() if v > 1]
    check(
        "INV-7: 중복 question_number",
        len(dup) == 0,
        detail=f"중복: {dup}" if dup else "없음"
    )

    # ── INV-8: Q0 존재 여부 (0번 시작 버그) ───────────────────
    has_q0 = 0 in q_nos
    check(
        "INV-8: Q0 부재 (1번 시작 확인)",
        not has_q0,
        detail="Q0 존재 — 파싱 버그 의심" if has_q0 else "Q0 없음 (정상)"
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
        print("  → 파이프라인 실행 전 수정 필요")
    elif warns > 0:
        print("  → 경고 확인 후 실행 권장")
    else:
        print("  → 파싱 품질 정상. 다음 단계 진행 가능.")
    print(f"{'='*60}\n")

    return fails


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python3 verify_parsing.py <questions_json_path>")
        sys.exit(1)
    fails = run(sys.argv[1])
    sys.exit(1 if fails > 0 else 0)
