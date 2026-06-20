#!/usr/bin/env python3
"""figure lane 계승 검증기 — 산문 핸드오프를 대신하는 '코드 핸드오프'

[왜 이 파일이 있는가]
  figure lane 의 계승은 그동안 산문 .md(SESSION_HANDOFF)로 넘겼다. 그런데 산문은
  모순과 오류를 담을 수 있고, 실제로 그렇게 됐다 — 골든셋을 한쪽(통찰)에서는
  "순도 추구 금지"라 적고 다른 쪽(다음단계)에서는 "표본 확대"라 적어, 다음 세션이
  금지된 작업을 다시 하려 했다. 파일명도 틀렸고(figure_lane_flags → figure_flags),
  골든셋 건수도 틀렸다(20 → 30).
  → 해법: 계승을 '상태 파일(JSON) + 불변식 가드(코드)'로 박는다. 코드는 모순을 담을
    수 없다. 실행하면 상태 파일이 실제 repo 와 일치하는지 검증되고, 어긋나면 실패한다.

[어떻게 작동하는가 — 한눈에]
  1) figure_lane_handoff_state.json 을 읽는다(figure lane 의 단일 진실).
  2) 네 개의 불변식 가드를 차례로 돌린다:
       - 산출물 가드 : 상태가 가리키는 파일이 실재하고 내용(sha)이 안 바뀌었는가.
       - 분포 가드   : 앱이 읽는 figure_flags.json 의 keep/review/reject 수가 상태와 같은가.
       - 적용 가드   : app/index.html 에 로드/매핑/배지 코드가 실재하는가(앱 적용 드리프트).
       - 합의 가드   : 골든셋 합의(감시기준/일괄검수금지/lazy교정)가 상태에 온전한가.
  3) 사람/Claude 가 읽을 한국어 요약을 출력한다.
  4) 끝-술어: 가드가 전부 통과하면 종료코드 0(계승 가능), 하나라도 깨지면 0이 아닌 코드
     (거짓 계승 금지 — "이어받았다"고 거짓 보고하지 못하게).

[codex 와의 연결]
  --codex-prompt 를 주면, codex 가 read-only 로 figure lane 을 이어받기 위한 계승
  프롬프트(상태 요약 + 다음 작업 + 금지 규약)를 표준출력으로 낸다. 그 문자열을
  blind_runner 의 codex 호출과 같은 방식(npx --yes @openai/codex exec ... -s read-only)
  으로 넘기면, codex 도 동일한 단일 진실 위에서 이어간다.

사용:
  python3 figure_lane_handoff.py              # 계승 검증 + 요약(기본)
  python3 figure_lane_handoff.py --json       # 검증 결과를 기계용 JSON 으로
  python3 figure_lane_handoff.py --codex-prompt  # codex 계승 프롬프트만 출력
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

# 이 스크립트는 docs/research/ 안에 있고, repo 루트는 두 단계 위다.
# 상태 파일은 같은 폴더, 검증 대상 경로는 repo 루트 기준(상태 파일에 그렇게 적힘).
HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent.parent
STATE_PATH = HERE / "figure_lane_handoff_state.json"


def sha16(path: Path) -> str | None:
    """파일 내용의 sha256 앞 16자리. 없으면 None.

    불변식 가드의 핵심 도구다 — 상태 파일에 박아둔 sha 와 지금 다시 계산한 sha 를
    비교해, 산출물이 핸드오프 이후 바뀌었는지(드리프트) 결정적으로 감지한다.
    """
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def canon_sha16(text: str) -> str:
    """문장을 공백 정규화(strip + 내부 공백 단일화)한 뒤 sha256 앞 16자리.

    forbidden 문장의 canonical 앵커 계산용. 토큰 검사는 핵심 단어가 살아있는지만 보지만,
    이건 문장 전체가 한 글자도 안 바뀌었는지(정규화 후)를 고정한다 — 가장 강한 잠금.
    """
    return hashlib.sha256(" ".join(text.split()).encode("utf-8")).hexdigest()[:16]


def load_state(path: Path = STATE_PATH) -> dict:
    """figure lane 의 단일 진실(상태 파일)을 읽는다. 없으면 계승 자체가 불가하므로 즉시 실패.

    path 인자는 반례 테스트가 원본을 건드리지 않고 임시 오염본을 검증하기 위한 것이다.
    """
    if not path.exists():
        sys.exit(f"상태 파일 없음: {path} — figure lane 계승 불가")
    return json.loads(path.read_text(encoding="utf-8"))


def guard_artifacts(state: dict) -> list[str]:
    """산출물 가드: 상태가 가리키는 파일이 실재하고 sha 가 일치하는가.

    실패 = 파일이 사라졌거나(경로 오류·삭제) 내용이 바뀐 것(판정 데이터·코드 변경).
    어느 쪽이든 산문 핸드오프가 못 잡던 계승 오류를 여기서 잡는다.
    """
    problems = []
    for a in state["artifacts"]:
        p = REPO_ROOT / a["path"]
        cur = sha16(p)
        if cur is None:
            problems.append(f"산출물 없음: {a['path']}")
        elif cur != a["sha256_16"]:
            problems.append(f"산출물 변경됨(sha 불일치): {a['path']} 기대 {a['sha256_16']} 현재 {cur}")
    return problems


def guard_distribution(state: dict) -> list[str]:
    """분포 가드: 앱이 읽는 figure_flags.json 의 판정 수가 상태와 일치하는가.

    keep/review/reject 의 수는 figure lane 의 결과 그 자체다. 이 수가 상태와 어긋나면
    상태 파일이 낡았거나 판정이 바뀐 것 — 어느 경우든 계승하면 안 된다.
    """
    fd = state["flag_distribution"]
    p = REPO_ROOT / fd["source"]
    if not p.exists():
        return [f"분포 소스 없음: {fd['source']}"]
    flags = json.loads(p.read_text(encoding="utf-8"))["flags"]
    # 앱용 축약본은 dict(qid->flag), 상세본은 list 일 수 있어 둘 다 받는다.
    vals = flags.values() if isinstance(flags, dict) else [x.get("figure_flag") for x in flags]
    dist = Counter(vals)
    problems = []
    if len(flags) != fd["total"]:
        problems.append(f"총건수 불일치: 기대 {fd['total']} 현재 {len(flags)}")
    for k in ("keep", "review", "reject"):
        if dist.get(k, 0) != fd[k]:
            problems.append(f"{k} 수 불일치: 기대 {fd[k]} 현재 {dist.get(k, 0)}")
    return problems


def guard_app_applied(state: dict) -> list[str]:
    """적용 가드: app/index.html 에 로드/매핑/배지 코드가 실재하는가.

    "적용 완료"라는 산문 보고는 거짓일 수 있다(과거 main.js 실착 사례). 실제 인라인
    스크립트를 grep 해서 세 지점(데이터 로드·문제 매핑·reject 배지)이 모두 살아있는지
    확인한다. 하나라도 없으면 배지가 화면에 안 나온다는 뜻이다.
    """
    app = state["app_application"]
    p = REPO_ROOT / app["file"]
    if not p.exists():
        return [f"앱 파일 없음: {app['file']}"]
    text = p.read_text(encoding="utf-8")
    problems = []
    for label, key in (("로드", "load_grep"), ("매핑", "map_grep"), ("배지", "badge_grep")):
        if app[key] not in text:
            problems.append(f"앱 {label} 코드 없음: {app[key]!r} in {app['file']}")
    return problems


# 골든셋 일괄 검수를 가리키는 항목은 반드시 lane_safe=false 여야 한다(검증 나선 금지).
GOLDEN_EXPAND_MARKERS = ("골든셋 표본 확대", "표본 확대", "진짜 kappa")
# consensus.forbidden 이 의미를 잃지 않게 반드시 담아야 할 핵심 토큰.
FORBIDDEN_REQUIRED_TOKENS = ("일괄 검수", "순도 100%", "금지", "검증 나선")
# consensus.forbidden 에 들어오면 안 되는 반대 신호(금지를 허용으로 뒤집는 말).
FORBIDDEN_NEGATION_TOKENS = ("허용", "금지 아님", "제한 없음", "해도 됨", "해도 좋", "괜찮")
# lane_safe=true 로 표시된 작업의 item 텍스트에 들어오면 안 되는 금지 신호.
FORBID_SIGNAL_TOKENS = ("골든셋 표본 확대", "표본 확대", "진짜 kappa", "일괄 검수", "순도 100%", "금지", "검증 나선")

# self-check: verify() 가 반드시 돌려야 할 가드 집합(self 제외). 가드가 제거되면 감지된다.
EXPECTED_GUARDS = ("artifacts", "distribution", "app_applied", "consensus", "golden")
# handoff.py 소스에 반드시 살아있어야 할 의미 검증 시그니처. 누군가 가드를 키검사만으로
# 되돌리거나(약화 드리프트) 게이트를 빼면, 해당 시그니처가 사라져 self-check 가 FAIL 낸다.
SELF_CHECK_SIGNATURES = (
    "FORBIDDEN_REQUIRED_TOKENS",   # forbidden 의미 토큰 검사
    "FORBIDDEN_NEGATION_TOKENS",   # forbidden 반대 신호 검사
    "GOLDEN_EXPAND_MARKERS",       # 골든셋 확대 lane 강제
    "is not False",                # lane_safe=false 강제 비교
    "def guard_golden",            # 골든셋 실로드 가드
    "FORBID_SIGNAL_TOKENS",        # lane_safe=true 금지 토큰 검사
    "canon_sha16",                 # forbidden canonical 잠금
    "골든셋 확대/진짜 kappa 금지 항목이 없음",  # 금지 항목 존재 강제
)


def guard_consensus(state: dict) -> list[str]:
    """합의 가드: 골든셋 합의가 형식뿐 아니라 '의미'까지 온전한가.

    이 가드의 존재 이유가 figure lane 계승 실패의 핵심이다 — 골든셋은 '감시 기준'일 뿐
    일괄 검수·순도 추구는 금지(검증 나선 재시작)인데, 산문 핸드오프가 이 합의를
    모순되게 담아 다음 세션이 금지된 작업을 재제안했다.

    초판은 '키가 비어있지 않은가'만 봐서, forbidden 문장을 반대로 뒤집거나 금지 항목을
    lane_safe=true 로 바꿔도 통과하는 형식 검증이었다(codex 적대 검증이 노출). 그래서:
      (1) 세 합의 키 존재(기존).
      (2) forbidden 에 핵심 의미 토큰이 실재(반대로 뒤집으면 토큰이 빠져 실패).
      (3) open_items 중 골든셋 일괄 검수류 항목은 반드시 lane_safe=false.
      (4) lane_safe=true 항목의 item 에 금지 신호 토큰이 섞이면 실패.
    """
    c = state.get("consensus", {})
    problems = []
    # (1) 세 합의 키 존재
    for key in ("golden_set_role", "forbidden", "lazy_only"):
        if not c.get(key):
            problems.append(f"합의 누락: consensus.{key} — 골든셋 모순 재발 위험")
    # (2) forbidden 핵심 의미 토큰 실재(핵심 단어를 빼면 걸린다)
    forbidden_text = c.get("forbidden", "")
    missing = [t for t in FORBIDDEN_REQUIRED_TOKENS if t not in forbidden_text]
    if missing:
        problems.append(f"consensus.forbidden 핵심 의미 누락: {missing} — 금지 뜻이 약화됨")
    # (2-반대) forbidden 에 반대 신호가 섞이면 금지를 허용으로 뒤집은 것 → FAIL
    negations = [t for t in FORBIDDEN_NEGATION_TOKENS if t in forbidden_text]
    if negations:
        problems.append(f"consensus.forbidden 에 반대 신호: {negations} — 금지를 허용으로 뒤집음")
    # (2-canonical) forbidden 문장이 canonical 앵커와 글자 단위로 일치하는가(가장 강한 잠금)
    anchor = c.get("forbidden_canonical_sha16")
    if not anchor:
        problems.append("consensus.forbidden_canonical_sha16 앵커 누락 — canonical 잠금 불가")
    elif canon_sha16(forbidden_text) != anchor:
        problems.append(f"consensus.forbidden canonical 불일치: 기대 {anchor} 현재 {canon_sha16(forbidden_text)}")
    # (3) 골든셋 일괄 검수 금지 항목이 open_items 에 '최소 1개' 존재해야 한다(삭제 우회 차단)
    golden_forbid_items = [it for it in state.get("open_items", [])
                           if any(m in it.get("item", "") for m in GOLDEN_EXPAND_MARKERS)]
    if not golden_forbid_items:
        problems.append("open_items 에 골든셋 확대/진짜 kappa 금지 항목이 없음 — 금지 항목 삭제 우회")
    # (4)(5) open_items 의 lane safety 의미 검사
    for it in state.get("open_items", []):
        item_text = it.get("item", "")
        if any(m in item_text for m in GOLDEN_EXPAND_MARKERS) and it.get("lane_safe") is not False:
            problems.append(f"open_items 위반: '{item_text}' 는 lane_safe=false 여야 함(검증 나선 금지)")
        if it.get("lane_safe") is True and any(t in item_text for t in FORBID_SIGNAL_TOKENS):
            problems.append(f"open_items 위반: lane_safe=true 인데 금지 신호 토큰 포함: '{item_text}'")
    return problems


def guard_golden(state: dict) -> list[str]:
    """골든셋 가드: golden_set.source 를 실제 로드해 건수·분포가 상태와 일치하는가.

    초판은 골든셋을 숫자(30)로만 적어두고 파일을 읽지 않았다. 파일이 바뀌면(라벨 추가·삭제,
    판정 변경) 상태와 어긋나는데 그걸 못 잡았다. 여기서 실제 labels 를 로드해 건수와
    decision 분포를 대조한다 — distribution 가드가 판정 결과를 닫듯, 이건 감시 기준을 닫는다.
    """
    gs = state.get("golden_set", {})
    p = REPO_ROOT / gs.get("source", "")
    if not gs or not p.exists():
        return [f"골든셋 소스 없음: {gs.get('source')}"]
    labels = json.loads(p.read_text(encoding="utf-8")).get("labels", [])
    problems = []
    if len(labels) != gs.get("count"):
        problems.append(f"골든셋 건수 불일치: 기대 {gs.get('count')} 현재 {len(labels)}")
    dist = Counter(x.get("decision") for x in labels)
    for k, v in gs.get("distribution", {}).items():
        if dist.get(k, 0) != v:
            problems.append(f"골든셋 {k} 불일치: 기대 {v} 현재 {dist.get(k, 0)}")
    return problems


def guard_self(guard_names) -> list[str]:
    """self-check 가드: 이 스크립트의 가드가 약화/제거되지 않았는가.

    다른 가드들은 '상태 vs repo'를 검증하지만, 정작 검증기 자신이 약화되면(누가
    guard_consensus 를 키검사만으로 되돌리거나 가드를 통째 지우면) 아무도 못 잡는다.
    그래서 두 가지를 본다:
      (1) verify() 가 실제로 돌린 가드 집합이 EXPECTED_GUARDS 와 정확히 일치하는가
          (가드가 빠지면 감지).
      (2) 이 파일 소스에 핵심 의미 검증 시그니처가 모두 실재하는가
          (가드 본문이 비워지는 약화 드리프트를 부분 감지).
    """
    problems = []
    if set(guard_names) != set(EXPECTED_GUARDS):
        problems.append(f"가드 집합 변경: 기대 {sorted(EXPECTED_GUARDS)} 현재 {sorted(guard_names)}")
    src = Path(__file__).read_text(encoding="utf-8")
    for sig in SELF_CHECK_SIGNATURES:
        if sig not in src:
            problems.append(f"가드 약화 의심: 핵심 시그니처 누락 '{sig}'")
    return problems


def verify(state: dict) -> dict:
    """모든 가드를 돌려 결과를 모은다. ok=True 면 계승 가능."""
    results = {
        "artifacts": guard_artifacts(state),
        "distribution": guard_distribution(state),
        "app_applied": guard_app_applied(state),
        "consensus": guard_consensus(state),
        "golden": guard_golden(state),
    }
    # self-check 는 다른 가드 이름을 알아야 하므로 마지막에 그 키집합으로 호출한다.
    results["self"] = guard_self(results.keys())
    ok = all(not v for v in results.values())
    return {"ok": ok, "problems": results}


def print_summary(state: dict, result: dict) -> None:
    """사람/Claude 가 읽을 한국어 계승 요약. 산문 핸드오프를 대체하는 출력이다."""
    fd = state["flag_distribution"]
    print("=== figure lane 계승 요약 (코드 핸드오프) ===")
    print(state["what_is_figure_lane"])
    print(f"\n[판정 분포] 총 {fd['total']} | keep {fd['keep']} / review {fd['review']} / reject {fd['reject']}")
    print(f"[앱 적용] {state['app_application']['file']} — reject 만 노란 경고 배지")
    print(f"[골든셋] {state['golden_set']['count']}건 (감시 기준)")
    c = state["consensus"]
    print("\n[HARD 합의 — 골든셋]")
    print(f"  역할 : {c['golden_set_role']}")
    print(f"  금지 : {c['forbidden']}")
    print(f"  교정 : {c['lazy_only']}")
    print("\n[다음 작업 후보]")
    for it in state["open_items"]:
        mark = "OK" if it.get("lane_safe") else "금지"
        extra = f" ({it['reason']})" if it.get("reason") else (f" — 주의: {it['caution']}" if it.get("caution") else "")
        print(f"  [{mark}] {it['item']}{extra}")
    print("\n[불변식 가드 결과]")
    for name, probs in result["problems"].items():
        if probs:
            for pr in probs:
                print(f"  FAIL {name}: {pr}")
        else:
            print(f"  PASS {name}")
    print(f"\n계승 판정: {'PASS — 코드와 상태가 일치, 온전히 이어받을 수 있다' if result['ok'] else 'FAIL — 위 어긋남을 먼저 해소하라'}")


def codex_prompt(state: dict) -> str:
    """codex 가 read-only 로 figure lane 을 이어받기 위한 계승 프롬프트를 만든다.

    blind_runner 의 codex 호출과 같은 read-only 방식으로 이 문자열을 넘기면, codex 도
    동일한 단일 진실(상태 파일) 위에서 시작한다. 금지 규약을 명시해 codex 가 검증 나선을
    재시작하지 않게 막는다.
    """
    fd = state["flag_distribution"]
    c = state["consensus"]
    safe = [it["item"] for it in state["open_items"] if it.get("lane_safe")]
    forbid = [it["item"] for it in state["open_items"] if not it.get("lane_safe")]
    return (
        "당신은 figure lane(전기기사 학습앱의 풀이 그림이 문제와 맞는지 판정) 작업을 "
        "이어받는다. 다음은 코드로 검증된 단일 진실이다.\n"
        f"- 무엇: {state['what_is_figure_lane']}\n"
        f"- 판정 분포: 총 {fd['total']} (keep {fd['keep']}/review {fd['review']}/reject {fd['reject']})\n"
        f"- 판정기: docs/research/figure_lane_judge.py (결정적). codex 배치 러너: "
        "docs/research/figure_lane_blind_runner.py.\n"
        f"- 앱 적용처: {state['app_application']['file']} (reject 만 경고 배지).\n"
        f"- HARD 합의: 골든셋은 {c['golden_set_role']} 금지: {c['forbidden']} 교정: {c['lazy_only']}\n"
        f"- 진행 가능한 다음 작업: {', '.join(safe)}\n"
        f"- 금지된 작업(하지 말 것): {', '.join(forbid)}\n"
        "먼저 docs/research/figure_lane_handoff.py 를 read-only 로 실행해 가드가 PASS 인지 "
        "확인한 뒤 작업하라."
    )


def main() -> None:
    ap = argparse.ArgumentParser(description="figure lane 코드 핸드오프")
    ap.add_argument("--json", action="store_true", help="검증 결과를 기계용 JSON 으로 출력")
    ap.add_argument("--codex-prompt", action="store_true", help="codex 계승 프롬프트만 출력")
    ap.add_argument("--state", type=Path, default=STATE_PATH, help="상태 파일 경로(반례 테스트용)")
    args = ap.parse_args()

    state = load_state(args.state)

    if args.codex_prompt:
        # codex 에게 넘기기 전 반드시 verify 를 통과해야 한다. 깨진 상태로 만든 프롬프트는
        # codex 를 잘못된 단일 진실 위에서 출발시키므로, 실패 시 프롬프트를 내지 않는다.
        result = verify(state)
        if not result["ok"]:
            print("verify 실패 — codex 계승 프롬프트를 내지 않는다(거짓 계승 차단):", file=sys.stderr)
            for name, probs in result["problems"].items():
                for pr in probs:
                    print(f"  FAIL {name}: {pr}", file=sys.stderr)
            sys.exit(1)
        print(codex_prompt(state))
        return

    result = verify(state)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_summary(state, result)

    # 끝-술어: 가드가 깨지면 0이 아닌 종료코드로 거짓 계승을 막는다.
    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()
