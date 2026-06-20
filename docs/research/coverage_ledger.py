#!/usr/bin/env python3
"""5,331 coverage ledger — 정답 신뢰 × 그림 정합 2축 교차 집계.

[왜 이 ledger 가 필요한가]
  정답 검증(answer_trust, 5331건)과 그림 정합(figure_flags, 1900건)을 지금까지 따로 봤다.
  이 ledger 는 둘을 questions 를 다리로 join 해, 전체 5331 중 무엇이 닫혔고 무엇이
  생성/검토/보류 대상인지 한 표로 가른다. 이건 *검증 실행*이 아니라 *현재 상태의 측정/집계*다
  — 일괄 선행검증을 새로 돌리지 않는다(verification-spiral-done-condition 준수). 닫힌
  1900건(그림)부터 학습 전술을 적용할 때, 무엇이 이미 닫혔는지 숫자로 보는 지도다.

[두 키 체계의 다리 — 측정으로 확정한 사실]
  - questions.json  : 5331 문제. qid = "year_session_q_no"(예: 1998_2회_1). solution_svg 보유 = 1900.
    q_no 가 null 인 27행은 _id 충돌(identity_broken)로 figure join 에서 격리한다(추측 매칭 안 함).
  - answer_trust.json: trust[str(row_index)].level. 키는 qid 가 아니라 questions 의 0-based
    행 인덱스다(출처 scripts/answer_trust_close.py:94 `trust[str(i)]`). trust 에 없는 행은
    level=unverified 로 본다(5331 - 3217 = 2114 = unverified).
  - figure_flags.json: flags[qid] = keep/review/reject (1900건). 키는 qid 문자열.
  → 그래서 questions 를 순회하며 (행 인덱스로 answer level) + (qid 로 figure flag)를 동시에 붙인다.

[입력] 셋 다 읽기전용. [출력] coverage_ledger.json + 사람용 요약.

사용:
  python3 docs/research/coverage_ledger.py            # 집계 + 요약(stdout)
  python3 docs/research/coverage_ledger.py --build    # coverage_ledger.json 생성/갱신
  python3 docs/research/coverage_ledger.py --verify   # 기존 ledger 와 재생성 비교(드리프트 감지)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
LEDGER_PATH = HERE / "coverage_ledger.json"

QUESTIONS = REPO_ROOT / "app/data/questions.json"
ANSWER_TRUST = REPO_ROOT / "app/data/answer_trust.json"
FIGURE_FLAGS = REPO_ROOT / "app/data/figure_flags.json"

# answer level 을 의사결정 lane 으로 묶는다(닫힘/미검증/의심/제외).
ANSWER_LANE = {
    "verified": "trust_closed",        # 권위 출처로 확정 — 닫힘
    "self_consistent": "trust_closed", # 풀이↔답 교차 일치 — 닫힘
    "unverified": "answer_open",        # 미검증 — 생성/검토 대상
    "suspect": "answer_flagged",        # 의심 — 보류/검토
    "damaged": "excluded",              # 본문 손상 — 학습 제외
}
ANSWER_LEVELS = ("verified", "self_consistent", "unverified", "suspect", "damaged")
FIGURE_STATES = ("keep", "review", "reject", "none")


def sha16(path: Path) -> str:
    """입력 파일 내용의 sha256 앞 16자리. ledger 가 어떤 입력으로 만들어졌는지 박는 앵커."""
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def build_ledger() -> dict:
    """세 소스를 join 해 2축 교차 집계를 만든다(결정적 — 같은 입력이면 같은 출력)."""
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    trust = json.loads(ANSWER_TRUST.read_text(encoding="utf-8"))["trust"]
    flags = json.loads(FIGURE_FLAGS.read_text(encoding="utf-8"))["flags"]

    answer_counter = Counter()
    figure_counter = Counter()
    crosstab = defaultdict(Counter)           # answer level -> figure state -> 수
    lane_counter = Counter()
    seen_qids = set()
    identity_broken = 0

    for i, q in enumerate(questions):
        level = trust.get(str(i), {}).get("level", "unverified")  # 미기재 = unverified
        # q_no 없는(null) 행은 _id 가 "..._null" 로 충돌·합쳐진다. figure join 에서 격리한다
        # (앱 index.html guard 와 동일 정책). number fallback 으로 추측 매칭하지 않는다 —
        # identity 가 깨진 행에 잘못된 그림 신뢰를 붙이지 않는다(codex 권고: 복구 전까지 격리).
        qno = q.get("q_no")
        if qno in (None, ""):
            identity_broken += 1
            fig = "none"
        else:
            qid = f"{q['year']}_{q['session']}_{qno}"
            seen_qids.add(qid)
            fig = flags.get(qid)
            fig = fig if fig in ("keep", "review", "reject") else "none"

        answer_counter[level] += 1
        figure_counter[fig] += 1
        crosstab[level][fig] += 1
        lane_counter[ANSWER_LANE.get(level, "unknown")] += 1

    # figure_flags 에 있으나 q_no 정상 qid 와 매칭 안 되는 키(qid=None 데이터 위생 결함).
    # 침묵하면 "그림 1900건 다 반영됨"처럼 보인다 — 정직하게 orphan 으로 드러낸다(사례 21).
    figure_orphans = sorted(k for k in flags if k not in seen_qids)
    total = len(questions)
    learnable = total - answer_counter["damaged"]   # 손상 제외 학습 대상
    # 그림이 붙은 1900건이 정답 신뢰별로 어떻게 닫혔는가(교차의 핵심 관심)
    fig_have = total - figure_counter["none"]
    fig_reject_in_open = sum(crosstab[lv]["reject"] for lv in ("unverified", "suspect"))

    return {
        "schema": "coverage_ledger_v1",
        "total": total,
        "inputs": {
            "questions_sha16": sha16(QUESTIONS),
            "answer_trust_sha16": sha16(ANSWER_TRUST),
            "figure_flags_sha16": sha16(FIGURE_FLAGS),
        },
        "answer_levels": {k: answer_counter[k] for k in ANSWER_LEVELS},
        "figure_states": {k: figure_counter[k] for k in FIGURE_STATES},
        "lanes": {
            "trust_closed": lane_counter["trust_closed"],
            "answer_open": lane_counter["answer_open"],
            "answer_flagged": lane_counter["answer_flagged"],
            "excluded": lane_counter["excluded"],
        },
        "crosstab": {lv: {st: crosstab[lv][st] for st in FIGURE_STATES} for lv in ANSWER_LEVELS},
        "derived": {
            "learnable_excl_damaged": learnable,
            "figure_present": fig_have,
            "figure_reject_on_unverified_or_suspect": fig_reject_in_open,
            "identity_broken_rows": identity_broken,
        },
        "figure_orphans": figure_orphans,
        "note": "검증 실행 아님 — 현재 상태 측정. figure_orphans 는 qid 가 깨져(None) "
                "어떤 문제와도 join 안 되는 figure_flags 키 — 데이터 위생 결함으로 노출.",
    }


def print_summary(led: dict) -> None:
    """사람이 읽을 한국어 coverage 요약 — '무엇이 닫혔고 무엇이 대상인가'를 숫자로."""
    print(f"=== 5,331 coverage ledger (총 {led['total']}) ===")
    print("\n[정답 신뢰 lane]")
    L = led["lanes"]
    print(f"  trust_closed (verified+self_consistent): {L['trust_closed']}  ← 닫힘")
    print(f"  answer_open  (unverified)              : {L['answer_open']}  ← 생성/검토 대상")
    print(f"  answer_flagged (suspect)               : {L['answer_flagged']}  ← 보류/검토")
    print(f"  excluded     (damaged)                 : {L['excluded']}  ← 학습 제외")
    print(f"  → 학습 대상(손상 제외): {led['derived']['learnable_excl_damaged']}")
    print("\n[그림 정합]")
    F = led["figure_states"]
    print(f"  keep {F['keep']} / review {F['review']} / reject {F['reject']} / 그림없음 {F['none']}")
    print(f"  → 그림 보유: {led['derived']['figure_present']}")
    print("\n[교차표] 행=정답신뢰, 열=그림(keep/review/reject/none)")
    print(f"  {'level':<16} {'keep':>6}{'review':>7}{'reject':>7}{'none':>7}")
    for lv in ANSWER_LEVELS:
        c = led["crosstab"][lv]
        print(f"  {lv:<16} {c['keep']:>6}{c['review']:>7}{c['reject']:>7}{c['none']:>7}")
    print(f"\n[관심] 미검증·의심인데 그림이 reject: "
          f"{led['derived']['figure_reject_on_unverified_or_suspect']}건 "
          f"(정답도 불확실 + 그림도 경고 — 학습 시 우선 주의)")
    print(f"[데이터 위생] q_no=null identity_broken 행: {led['derived']['identity_broken_rows']}건 "
          f"(figure join 격리됨)")
    orph = led.get("figure_orphans", [])
    if orph:
        print(f"[데이터 위생] join 안 되는 figure_flags 키 {len(orph)}건: {orph} "
              f"(qid=None — 어떤 문제에도 안 붙음)")


def main() -> None:
    ap = argparse.ArgumentParser(description="5,331 coverage ledger")
    ap.add_argument("--build", action="store_true", help="coverage_ledger.json 생성/갱신")
    ap.add_argument("--verify", action="store_true", help="기존 ledger 와 재생성 비교(드리프트 감지)")
    args = ap.parse_args()

    led = build_ledger()

    if args.build:
        LEDGER_PATH.write_text(json.dumps(led, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"생성: {LEDGER_PATH}")
        print_summary(led)
        return

    if args.verify:
        if not LEDGER_PATH.exists():
            sys.exit("기존 ledger 없음 — 먼저 --build 하라")
        old = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
        # inputs sha 와 집계 본문이 모두 일치해야 한다(입력이 바뀌면 sha 가 먼저 어긋난다).
        drift = {k: (old.get(k), led.get(k)) for k in ("inputs", "answer_levels",
                 "figure_states", "lanes", "crosstab", "derived", "figure_orphans")
                 if old.get(k) != led.get(k)}
        if drift:
            print("드리프트 감지 — ledger 가 현재 데이터와 불일치:")
            for k, (o, n) in drift.items():
                print(f"  {k}: 기존 {o} != 현재 {n}")
            sys.exit(1)
        print("verify PASS — ledger 가 현재 데이터와 일치")
        return

    print_summary(led)


if __name__ == "__main__":
    main()
