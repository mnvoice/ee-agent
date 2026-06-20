#!/usr/bin/env python3
"""앱 게이트 완전성 가드 — 앱이 노출하는 모든 풀이 그림이 게이트됐는가.

[배경]
  풀이 SVG 생성 batch 는 이미 적용·게이트 완료다(실측: app/data/questions.json 의 q_no 정상
  solution_svg 1897건 전부 figure_flags 에 판정 존재, 누락 0). batch results 는 만료됐지만
  앱이 읽는 데이터는 디스크에 있고 완전하다.

[이 가드의 역할 — §1.7 검증 통로]
  생성 데이터에는 게이트가 동반돼야 한다. 이 가드는 그 불변식을 고정한다:
    solution_svg 를 가진 문제(q_no 정상)는 figure_flags 에 판정(keep/review/reject)이 반드시 있어야 한다.
  앞으로 새 그림이 생성·적용되면, figure_flags 판정 없이는 이 가드가 FAIL 한다 — 즉
  '게이트 안 된 그림이 앱에 노출되는' 사례 0 을 회귀 방지선으로 막는다.

[규칙]
  - solution_svg 보유 + q_no 정상(identity 격리 아님) → figure_flags 판정 필수.
  - q_no=null 행은 _id 충돌로 격리됨(figure join guard 와 동일 정책) → 게이트 대상에서 제외.
  - 누락이 하나라도 있으면 FAIL(종료 1) + 목록. 0 이면 PASS(종료 0).

사용: python3 docs/research/figure_gate_completeness.py
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
QUESTIONS = ROOT / "app/data/questions.json"
FIGURE_FLAGS = ROOT / "app/data/figure_flags.json"


def qid(q: dict) -> str | None:
    """year_session_q_no. q_no 가 null 이면 _id 충돌 격리 대상이라 None(게이트 제외)."""
    n = q.get("q_no")
    if n in (None, ""):
        return None
    return f"{q['year']}_{q['session']}_{n}"


def main() -> None:
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))
    flags = json.loads(FIGURE_FLAGS.read_text(encoding="utf-8"))["flags"]

    svg_total = 0
    isolated = 0
    missing = []
    for q in questions:
        if not q.get("solution_svg"):
            continue
        svg_total += 1
        qd = qid(q)
        if qd is None:
            isolated += 1            # q_no null — figure join 격리(가드 제외)
            continue
        if qd not in flags:
            missing.append(qd)        # 그림은 있는데 게이트 판정이 없음

    dist = Counter(flags.values())
    print("=== 앱 게이트 완전성 가드 ===")
    print(f"solution_svg 보유: {svg_total} | q_no null 격리(제외): {isolated} "
          f"| 게이트 대상: {svg_total - isolated}")
    print(f"게이트 누락(그림 있으나 미판정): {len(missing)}")
    for m in missing[:20]:
        print(f"  - {m}")
    print(f"figure_flags 분포: keep {dist['keep']} / review {dist['review']} / reject {dist['reject']}")

    if missing:
        print("\nFAIL — 게이트 안 된 풀이 그림이 앱에 노출됨(생성 후 figure judge 게이트 필요)")
        sys.exit(1)
    print("\nPASS — 앱의 모든 풀이 그림이 게이트됨")
    sys.exit(0)


if __name__ == "__main__":
    main()
