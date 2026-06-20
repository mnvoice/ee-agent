#!/usr/bin/env python3
"""figure_lane_handoff.py 반례 테스트 — 가드가 실제로 FAIL 내는지 결정적으로 증명.

[왜 이 파일이 repo 에 남는가]
  자기 코드를 자기 음성 테스트로만 채점하면 자기충족이다(헌법 사례 8). codex 적대
  검증이 짚은 공격 벡터를 repo 에 박아, 다음에 누가 가드를 약화시키면 이 테스트가
  깨지게 한다. 즉 가드 약화 드리프트의 회귀 방지선이다.

[원본을 건드리지 않는다]
  상태 파일을 직접 오염하면 테스트 중단 시 잔존 위험이 있다. 그래서 임시 오염본을
  만들어 figure_lane_handoff.py 의 --state 로 가리킨다. 원본 상태 파일은 읽기만 한다.

[검증하는 반례 — 모두 FAIL 이어야 정상]
  - forbidden 반전        : consensus.forbidden 을 반대 의미로 → consensus FAIL
  - lane_safe flip        : 골든셋 확대 항목을 lane_safe=true 로 → consensus FAIL
  - golden_set count 불일치: golden_set.count 위조 → golden FAIL
  - artifact sha 불일치    : artifacts sha 위조 → artifacts FAIL
  - codex-prompt 게이트    : 깨진 상태면 프롬프트 미출력 + 종료 nonzero
  - self-check 약화        : verify() 에서 가드 하나 제거한 복사본 → self FAIL

실행: python3 docs/research/figure_lane_handoff_test.py   (모두 통과면 종료 0)
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
HANDOFF = HERE / "figure_lane_handoff.py"
STATE = HERE / "figure_lane_handoff_state.json"
BASE = json.loads(STATE.read_text(encoding="utf-8"))


def run(state_dict: dict, codex_prompt: bool = False):
    """임시 상태 파일을 만들어 handoff.py 를 실행하고 (종료코드, stdout) 반환."""
    with tempfile.NamedTemporaryFile("w", suffix=".json", dir=HERE,
                                     delete=False, encoding="utf-8") as f:
        json.dump(state_dict, f, ensure_ascii=False)
        tmp = Path(f.name)
    try:
        cmd = ["python3", str(HANDOFF), "--state", str(tmp)]
        if codex_prompt:
            cmd.append("--codex-prompt")
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.returncode, r.stdout
    finally:
        tmp.unlink(missing_ok=True)


def mutate(fn) -> dict:
    """BASE 를 깊은 복사한 뒤 fn 으로 한 곳만 오염시켜 반환."""
    d = copy.deepcopy(BASE)
    fn(d)
    return d


def _flip_golden_lane(d: dict) -> None:
    for it in d["open_items"]:
        if "골든셋 표본 확대" in it["item"]:
            it["lane_safe"] = True


def _delete_golden_forbid_item(d: dict) -> None:
    # 금지 항목을 통째로 삭제해 lane_safe 검사를 우회하려는 시도.
    d["open_items"] = [it for it in d["open_items"]
                       if "골든셋 표본 확대" not in it["item"] and "진짜 kappa" not in it["item"]]


def _negate_forbidden(d: dict) -> None:
    # 핵심 토큰은 남기되 반대 신호('해도 됨')를 섞어 금지를 허용으로 뒤집는 시도.
    d["consensus"]["forbidden"] = d["consensus"]["forbidden"] + " 다만 사용자가 원하면 해도 됨"


def _edit_forbidden_keep_tokens(d: dict) -> None:
    # 핵심 토큰을 모두 유지한 채 문장만 살짝 바꿔 canonical 앵커를 깬다(토큰 검사는 통과).
    d["consensus"]["forbidden"] = ("일괄 검수 순도 100% 검증 나선 재시작이라 금지 "
                                   "(문구 변형으로 canonical 만 깨짐)")


CASES = [
    ("baseline PASS", BASE, 0),
    ("forbidden 반전",
     mutate(lambda d: d["consensus"].__setitem__("forbidden", "제한 없음")), 1),
    ("lane_safe flip", mutate(_flip_golden_lane), 1),
    ("golden_set count 불일치",
     mutate(lambda d: d["golden_set"].__setitem__("count", 20)), 1),
    ("artifact sha 불일치",
     mutate(lambda d: d["artifacts"][0].__setitem__("sha256_16", "0000000000000000")), 1),
    ("금지 항목 삭제 우회", mutate(_delete_golden_forbid_item), 1),
    ("forbidden 반대 신호 삽입", mutate(_negate_forbidden), 1),
    ("forbidden canonical 변형(토큰 유지)", mutate(_edit_forbidden_keep_tokens), 1),
]


def main() -> None:
    fails = []

    for name, state, want in CASES:
        rc, _ = run(state)
        ok = (rc == 0) if want == 0 else (rc != 0)
        print(f"[{'OK' if ok else '실패'}] {name}: rc={rc} (기대 {'0' if want == 0 else 'nonzero'})")
        if not ok:
            fails.append(name)

    # codex-prompt 게이트: 깨진 상태면 프롬프트가 안 나가야 한다.
    rc, out = run(mutate(lambda d: d["consensus"].__setitem__("forbidden", "제한 없음")),
                  codex_prompt=True)
    ok = rc != 0 and not out.strip()
    print(f"[{'OK' if ok else '실패'}] codex-prompt 게이트: rc={rc} stdout_빈출력={not out.strip()}")
    if not ok:
        fails.append("codex-prompt gate")

    # self-check 약화: verify() 에서 golden 가드를 제거한 복사본 → 가드 집합 불일치로 self FAIL.
    weak = HERE / "_tmp_weak_handoff.py"
    src = HANDOFF.read_text(encoding="utf-8").replace(
        '        "golden": guard_golden(state),\n', "")
    weak.write_text(src, encoding="utf-8")
    try:
        r = subprocess.run(["python3", str(weak), "--state", str(STATE)],
                           capture_output=True, text=True)
        ok = r.returncode != 0 and "self" in r.stdout
        print(f"[{'OK' if ok else '실패'}] self-check 약화 감지(golden 가드 제거): rc={r.returncode}")
        if not ok:
            fails.append("self-check weakening")
    finally:
        weak.unlink(missing_ok=True)

    print()
    if fails:
        print(f"반례 테스트 실패 {len(fails)}건: {fails}")
        sys.exit(1)
    print("모든 반례 테스트 통과 — 가드가 공격 벡터 전부를 막는다")


if __name__ == "__main__":
    main()
