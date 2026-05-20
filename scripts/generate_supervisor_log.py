#!/usr/bin/env python3
"""Generate the supervisor decision log (Obsidian-ready Markdown) and the
decision-record dataset (JSONL) for a work cycle.

Why this exists
---------------
`docs/audit/t3_5_regeneration_decision_log.md` is a result-centric log: it records
what was decided, not always the reasoning behind it. Conversation-time rationale is
easily lost. This script produces two durable artifacts from one seed:

  - a human-facing Obsidian-ready Markdown operations journal, and
  - a machine-facing JSONL decision dataset for later search / analysis / reuse.

Design
------
Seed-based generator. The structured decision records live in the ``DECISIONS`` seed
below (single source of truth). Full auto-summarization of the prose decision log
would need an LLM; instead this script renders both outputs deterministically from
the seed. The source decision log is referenced (and checked for existence) but its
prose is not parsed.

Input  (reference): docs/audit/t3_5_regeneration_decision_log.md
Outputs:
  docs/audit/supervisor_logs/2026-05-20_t3_5_g5_h1_supervisor_log.md
  docs/audit/decision_records/t3_5_g5_h1_decisions.jsonl

Usage: python3 scripts/generate_supervisor_log.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_LOG = ROOT / "docs/audit/t3_5_regeneration_decision_log.md"
MD_OUT = ROOT / "docs/audit/supervisor_logs/2026-05-20_t3_5_g5_h1_supervisor_log.md"
JSONL_OUT = ROOT / "docs/audit/decision_records/t3_5_g5_h1_decisions.jsonl"

CYCLE = {
    "cycle": "T3.5 / G5 / H1",
    "date": "2026-05-20",
    "branch": "feat/phase-b-migration",
    "summary": (
        "answer-locked 재생성 74건의 G5 브라우저 검증 종결(CLOSED/PASS)과, "
        "그림 의존 hold 3건의 figure-crop 트랙(H1) 진행 cycle."
    ),
}

# (hash, description) — oldest first.
COMMITS = [
    ("3e3feb4", "G5 정적 검증 74/74 + 표본 6건 기록"),
    ("17a0c2d", "Batch 1 (2025_1회 19건) clean-Chrome 검증 기록"),
    ("34e83eb", "Batch 2/3 (2025_2·3회 36건) clean-Chrome 검증 기록"),
    ("9771347", "Batch 4 (2026_1회 13건) + G5 종결 기록"),
    ("50f1908", ".gitignore — gstack 워크스페이스 무시"),
    ("bd99bc8", "hold 3건 figure crop 원본 자산 추가"),
    ("5bf8e50", "hold figure crop 트랙(T3.5-K) 기록"),
]

NEXT_CYCLE = [
    "A. 2026_1회_67 — 기존 old 해설 유지 + crop overlay 적용.",
    "B. 2025_2회_60 — crop 기반 answer-locked 재생성 (멀티모달 API 필요).",
    "C. 2025_3회_79 — crop 기반 멀티모달 answer-locked 재생성 (API 필요).",
    "D. 2025_3회_79 — 임시 '풀이 미제공 + 그림 참고' 패턴(폴백).",
    "별건. data/pdf_pages/index.json 추적 방식 A/B/C 결정 (DR-T35-12).",
]

# Single source of truth — the 12 decision records of this cycle.
DECISIONS = [
    {
        "id": "DR-T35-01",
        "topic": "clean Chrome / gstack 검증 기준 채택",
        "scope": "G5 브라우저 검증 환경",
        "situation": "재생성 해설의 실제 표시를 브라우저로 검증해야 하며, gstack headless와 "
                     "Codex in-app browser 등 복수 컨텍스트가 존재한다.",
        "decision": "서비스워커 unregister + caches 삭제 + reload를 선행한 clean Chrome "
                    "(gstack headless)를 G5 판정의 고정 기준으로 채택한다.",
        "rationale": "서비스워커/HTTP 캐시 stale 영향을 배제해야 재생성 해설의 실제 렌더를 "
                     "정확히 측정할 수 있다. clean context는 사전 캐시가 없다.",
        "alternatives": ["Codex in-app browser 사용", "캐시 정리 없이 검증"],
        "rejected_alternatives": [
            "Codex in-app browser — stale 캐시 가능성으로 기준 부적합",
            "캐시 미정리 — 구버전 표시 위험",
        ],
        "risks": "headless 렌더가 실제 사용자 브라우저와 미세 차이 가능 (낮음).",
        "status": "fixed",
        "related_commits": ["3e3feb4", "17a0c2d", "34e83eb", "9771347"],
        "next_actions": ["후속 모든 batch에 동일 기준 적용"],
    },
    {
        "id": "DR-T35-02",
        "topic": "Codex in-app browser stale 분리",
        "scope": "검증 기준 / 캐시 이슈 판정",
        "situation": "Codex in-app browser가 일부 항목에서 재생성 이전(구) 해설을 표시했다.",
        "decision": "이를 데이터/렌더 결함이 아닌 서비스워커/HTTP 캐시 stale 환경 문제로 "
                    "판정하고 G5 판정 기준에서 제외한다.",
        "rationale": "(1) 앱이 서비스워커(app/sw.js)를 보유; (2) 정적 hash 검사 74/74가 "
                     "questions.json/v2에 재생성 내용 적재를 확인; (3) clean Chrome는 신해설을 "
                     "정상 렌더 — 세 근거가 캐시 문제임을 가리킨다.",
        "alternatives": ["데이터 재점검", "재생성 롤백"],
        "rejected_alternatives": [
            "데이터 재점검/롤백 — hash 검사로 데이터 정상이 확인되어 불필요",
        ],
        "risks": "사용자 브라우저 캐시 stale 시 구해설 표시 — hard-reload/SW 해제로 해소.",
        "status": "fixed",
        "related_commits": ["9771347"],
        "next_actions": ["decision log에 캐시 vs 데이터 분리 근거를 영구 기록 (완료)"],
    },
    {
        "id": "DR-T35-03",
        "topic": "유료 API 미사용 판단",
        "scope": "이번 cycle 전체 (검증 / crop)",
        "situation": "G5 검증, hold 트랙 조사, figure crop 작업을 수행해야 한다.",
        "decision": "유료 Claude/OpenAI API 호출 없이 정적 검사 + clean Chrome/gstack 자동화 "
                    "+ 로컬 PDF 도구(PyMuPDF)만 사용한다.",
        "rationale": "검증과 crop은 결정적(deterministic) 작업으로 LLM 추론이 불필요하다. "
                     "비용 0으로 동일 결과를 얻는다.",
        "alternatives": ["멀티모달 LLM로 검증/crop 수행"],
        "rejected_alternatives": [
            "멀티모달 LLM — 불필요한 비용; 정적 비교/렌더 자동화로 충분",
        ],
        "risks": "figure-dependent 해설 재생성(H2)은 그림 분석에 멀티모달 LLM이 필요 — "
                 "별도 예산 승인 대상으로 분리.",
        "status": "fixed (this cycle)",
        "related_commits": [],
        "next_actions": ["H2 재생성 단계는 별도 API 예산 승인 후 진행"],
    },
    {
        "id": "DR-T35-04",
        "topic": "Claude CLI / 웹 Claude / 감독자 역할 분리",
        "scope": "검증 거버넌스",
        "situation": "검증 결과의 신뢰성을 단일 인스턴스 편향 없이 확보해야 한다.",
        "decision": "Claude CLI(실행 검증), 웹 Claude(독립 판정), 감독자(최종 승인)의 "
                    "3-채널 역할 분리를 유지한다.",
        "rationale": "빌더-감사자 분리 원칙. 실행 주체와 독립 판정 주체를 나눠 자기 검증 편향을 "
                     "차단하고, 감독자가 최종 게이트로 기록/commit을 승인한다.",
        "alternatives": ["단일 채널 검증"],
        "rejected_alternatives": [
            "단일 채널 — 실행자가 자기 결과를 검증하는 편향 발생",
        ],
        "risks": "채널 간 sandbox stale 시 상호 불일치 가능 — 보고로 동기화.",
        "status": "fixed",
        "related_commits": ["17a0c2d", "34e83eb", "9771347"],
        "next_actions": ["batch별로 3-채널 판정을 기록에 명시"],
    },
    {
        "id": "DR-T35-05",
        "topic": "index.lock 충돌 판단",
        "scope": "git 운영",
        "situation": "commit 중 .git/index.lock 충돌이 2회 발생했다 (병렬 프로세스 추정).",
        "decision": "활성 git 프로세스 부재 + lock 파일 자체 해제를 확인한 뒤 재시도한다. "
                    "강제 삭제는 하지 않는다.",
        "rationale": "일시적 race로 판단. 강제 삭제는 다른 git 프로세스 진행 중일 경우 인덱스 "
                     "손상 위험이 있어 안전한 재시도를 택한다.",
        "alternatives": ["index.lock 강제 삭제"],
        "rejected_alternatives": [
            "강제 삭제 — 동시 진행 중인 git 작업의 인덱스 손상 위험",
        ],
        "risks": "낮음 — 매 충돌이 자체 해제되었고 재시도로 정상 commit됨.",
        "status": "resolved",
        "related_commits": ["9771347", "50f1908"],
        "next_actions": ["반복 시 병렬 프로세스 출처 확인"],
    },
    {
        "id": "DR-T35-06",
        "topic": "G5 74/74 CLOSED/PASS 판단",
        "scope": "G5 게이트 종결",
        "situation": "answer-locked 재생성 74건의 G5 브라우저 검증.",
        "decision": "정적 74/74 + 브라우저 전수(표본 6 + Batch 1~4 = 74) PASS를 근거로 "
                    "G5 브라우저 검증을 CLOSED/PASS로 고정한다.",
        "rationale": "데이터 5-layer 일치, 렌더 게이팅 meaningful, console error 0, "
                     ".katex-error 0, PUA/U+FFFD 0이 누적 확인되었다.",
        "alternatives": ["표본만 검증 후 종결"],
        "rejected_alternatives": [
            "표본 검증 종결 — 전수 검증이 재현성·신뢰성에서 우위 (완전성 원칙)",
        ],
        "risks": "없음 — 누적 FAIL 0.",
        "status": "closed",
        "related_commits": ["3e3feb4", "17a0c2d", "34e83eb", "9771347"],
        "next_actions": [],
    },
    {
        "id": "DR-T35-07",
        "topic": "hold 3건을 G5에서 분리",
        "scope": "검증 범위 정의",
        "situation": "2025_2회_60 / 2025_3회_79 / 2026_1회_67은 figure-dependent 문항이다.",
        "decision": "이 3건을 G5 검증 범위에서 제외하고 별도 트랙(T3.5-K)으로 분리한다.",
        "rationale": "그림 없이는 answer-locked 재생성이 q.answer 역산이 되어 검증 의미가 "
                     "없다 (R8 정책). G5는 적용된 74건에 한정한다.",
        "alternatives": ["hold 항목을 G5에 포함해 강행"],
        "rejected_alternatives": [
            "강행 — 그림 부재 시 해설이 정답 역산 → 검증 무효",
        ],
        "risks": "hold 트랙 미해소 시 3건이 장기 보류될 수 있음.",
        "status": "fixed",
        "related_commits": ["9771347", "5bf8e50"],
        "next_actions": ["H1 figure crop 확보로 별도 트랙 진행"],
    },
    {
        "id": "DR-T35-08",
        "topic": "H1 figure crop 자산 확보",
        "scope": "hold 트랙 H1",
        "situation": "hold 3건의 answer-locked 재생성에는 원본 그림이 필요하다.",
        "decision": "원본 CBT PDF에서 그림 영역을 crop하여 "
                    "data/pdf_pages/figure_crops/{회차}/ 에 저장하고 commit한다.",
        "rationale": "AI 합성 figure_svg/solution_svg는 헌법상 정답/원문 근거로 쓸 수 없다. "
                     "원본 crop만 정당한 근거이며, PDF + PyMuPDF로 API 없이 확보 가능하다.",
        "alternatives": ["AI 합성 figure_svg 사용", "그림 없이 진행"],
        "rejected_alternatives": [
            "AI 합성물 — 원문 근거 사용 금지 규약 위반",
            "그림 없이 진행 — figure-dependent 문항 해소 불가",
        ],
        "risks": "crop 품질 불충분 시 재crop 필요 — 본 cycle 3건은 모두 양호.",
        "status": "done",
        "related_commits": ["bd99bc8"],
        "next_actions": ["crop을 앱에서 참조 가능하게 연결 (DR-T35-12)"],
    },
    {
        "id": "DR-T35-09",
        "topic": "2025_2회_60 정책 판단",
        "scope": "hold 항목 / 직류기 권선도 식별",
        "situation": "직류기 전기자 권선도를 보고 권선법을 식별하는 문항. old 해설(220자)은 "
                     "환상권/고상권 개념 설명이나 '이 그림이 왜 환상권인지'의 식별 논거가 약하다.",
        "decision": "old 해설 유지 해제는 약함 → crop 기반 재생성 후보로 분류. 본 cycle은 "
                    "원본 crop 표시 + old 해설 유지로 처리한다.",
        "rationale": "old 해설이 그림 식별 결론을 명확히 서술하지 않는다. crop은 확보되었으나 "
                     "재생성은 그림 분석(멀티모달 API)이 필요해 H2 대상이다.",
        "alternatives": ["old 해설 유지로 즉시 hold 해제", "즉시 재생성"],
        "rejected_alternatives": [
            "즉시 hold 해제 — old 식별 논거가 약해 부적합",
            "즉시 재생성 — 이번 cycle은 무 API 원칙",
        ],
        "risks": "재생성 전까지 식별 논거가 약한 해설이 노출됨.",
        "status": "pending (재생성 후보)",
        "related_commits": ["bd99bc8", "5bf8e50"],
        "next_actions": ["H2에서 crop 기반 answer-locked 재생성 검토"],
    },
    {
        "id": "DR-T35-10",
        "topic": "2025_3회_79 정책 판단",
        "scope": "hold 항목 / 블록선도 4개 비교",
        "situation": "블록선도 4개를 비교하는 문항. old 해설이 무실체('블록선도 출력 × × × × ×').",
        "decision": "새 해설을 생성하지 않고, 원본 crop 표시 + '풀이 재작성 보류' 상태로 "
                    "처리한다. 재생성은 필수이나 멀티모달 API가 필요해 H2 대상이다.",
        "rationale": "old 해설이 무실체라 유지가 불가능하다. 4개 블록선도 전달함수 비교는 "
                     "그림 분석이 필수다. 본 cycle은 무 API 원칙이므로 crop 표시 + 보류 명시.",
        "alternatives": ["무실체 old 해설 그대로 노출", "즉시 멀티모달 재생성"],
        "rejected_alternatives": [
            "무실체 노출 — 사용자에게 의미 없는 풀이 제공",
            "즉시 재생성 — 이번 cycle 무 API 원칙",
        ],
        "risks": "재작성 보류 상태가 장기화될 수 있음.",
        "status": "pending (재생성 필수) — 본 cycle: 그림 표시 + 재작성 보류",
        "related_commits": ["bd99bc8", "5bf8e50"],
        "next_actions": ["H2에서 crop 기반 멀티모달 answer-locked 재생성"],
    },
    {
        "id": "DR-T35-11",
        "topic": "2026_1회_67 정책 판단",
        "scope": "hold 항목 / 게이트 회로도 식별",
        "situation": "게이트 회로도의 명칭을 식별하는 문항. old 해설(143자)은 'A·B·C 동시 "
                     "입력 시 Tr 동작 → Z 소멸 → NAND'로 회로 동작 논리에 실체가 있다.",
        "decision": "old 해설 유지 해제의 강한 후보로 분류. 본 cycle은 원본 crop 표시 + "
                    "old 해설 유지로 처리하되, clean Chrome 검증 + decision log 기록 "
                    "전까지 hold 상태를 유지한다.",
        "rationale": "old 해설이 회로 동작 논리로 NAND를 도출하여 실체가 있다. crop 확보로 "
                     "그림 근거가 보강된다.",
        "alternatives": ["즉시 정식 hold 해제", "재생성"],
        "rejected_alternatives": [
            "즉시 해제 — clean Chrome 검증·기록 전 해제는 절차 미준수",
            "재생성 — old 해설이 충분해 불필요할 수 있음",
        ],
        "risks": "낮음 — old 해설 실체 있음.",
        "status": "pending (old 유지 해제 강한 후보)",
        "related_commits": ["bd99bc8", "5bf8e50"],
        "next_actions": ["clean Chrome 검증 + 기록 후 hold 해제 검토"],
    },
    {
        "id": "DR-T35-12",
        "topic": "data/pdf_pages/index.json 추적 여부 미결정",
        "scope": "crop 연결 / 재현성",
        "situation": "crop을 앱에 연결하려 index.json(pdfPageIndex)에 3건을 추가했으나 "
                     "index.json은 repo에서 미추적 상태다 (133KB, 193 key 중 190이 무관, "
                     "참조 이미지 1,222개 대부분 미추적).",
        "decision": "미결정 — A(index.json 통째 추적) / B(소형 manifest 신설 + merge) / "
                    "C(app/index.html 상수) 중 C를 추천하고 감독자 결정을 대기한다.",
        "rationale": "A는 무관 190 key 대량 commit + 참조 이미지 미추적으로 재현성을 실제로 "
                     "확보하지 못한다. C는 app/index.html 상수 + 이미 추적된 crop PNG 3개로 "
                     "git만으로 자족하며 변경 범위가 최소다.",
        "alternatives": [
            "A: index.json 통째 신규 추적",
            "B: hold 전용 소형 manifest 신설 + app merge",
            "C: app/index.html에 crop 경로 상수",
        ],
        "rejected_alternatives": [
            "A — 범위 과도(190 무관 key) + 참조 이미지 미추적으로 재현성 미해결",
        ],
        "risks": "미결정 상태 — crop 연결 방식이 확정되지 않으면 재현성 위험이 남는다.",
        "status": "open / undecided",
        "related_commits": ["bd99bc8"],
        "next_actions": ["감독자가 A/B/C 결정 → 선택안으로 crop 연결 확정 후 재검증"],
    },
]


def write_jsonl():
    JSONL_OUT.parent.mkdir(parents=True, exist_ok=True)
    with JSONL_OUT.open("w", encoding="utf-8") as f:
        for d in DECISIONS:
            rec = {
                "id": d["id"],
                "date": CYCLE["date"],
                "topic": d["topic"],
                "scope": d["scope"],
                "situation": d["situation"],
                "decision": d["decision"],
                "rationale": d["rationale"],
                "alternatives": d["alternatives"],
                "rejected_alternatives": d["rejected_alternatives"],
                "risks": d["risks"],
                "status": d["status"],
                "related_commits": d["related_commits"],
                "next_actions": d["next_actions"],
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def write_markdown():
    MD_OUT.parent.mkdir(parents=True, exist_ok=True)
    L = []
    # Obsidian-ready YAML frontmatter
    L.append("---")
    L.append(f"title: 감독자 판단 근거 로그 — {CYCLE['cycle']} ({CYCLE['date']})")
    L.append(f"date: {CYCLE['date']}")
    L.append(f"cycle: {CYCLE['cycle']}")
    L.append(f"branch: {CYCLE['branch']}")
    L.append("tags:")
    L.append("  - 전기기사/supervisor-log")
    L.append("  - 전기기사/decision-rationale")
    L.append("  - ee-agent/T3.5")
    L.append("source: docs/audit/t3_5_regeneration_decision_log.md")
    L.append("generator: scripts/generate_supervisor_log.py")
    L.append("---")
    L.append("")
    L.append(f"# 감독자 판단 근거 로그 — {CYCLE['cycle']}")
    L.append("")
    L.append("> 이 문서는 결과 중심 decision log와 짝을 이루는 *판단 근거* 운영 일지다. "
             "원본 결과 기록은 `docs/audit/t3_5_regeneration_decision_log.md`, "
             "기계용 데이터셋은 `docs/audit/decision_records/t3_5_g5_h1_decisions.jsonl`. "
             "본 파일은 `scripts/generate_supervisor_log.py`로 생성된다.")
    L.append("")
    L.append("## 개요")
    L.append("")
    L.append(f"- **Cycle**: {CYCLE['cycle']}")
    L.append(f"- **Date**: {CYCLE['date']}")
    L.append(f"- **Branch**: {CYCLE['branch']}")
    L.append(f"- **요약**: {CYCLE['summary']}")
    L.append("")
    L.append("## 판단 근거 (12건)")
    L.append("")
    for i, d in enumerate(DECISIONS, 1):
        L.append(f"### D{i}. {d['topic']}  `{d['id']}`")
        L.append("")
        L.append(f"- **범위(scope)**: {d['scope']}")
        L.append(f"- **상황(situation)**: {d['situation']}")
        L.append(f"- **결정(decision)**: {d['decision']}")
        L.append(f"- **근거(rationale)**: {d['rationale']}")
        if d["alternatives"]:
            L.append(f"- **검토한 대안**: {'; '.join(d['alternatives'])}")
        if d["rejected_alternatives"]:
            L.append(f"- **기각한 대안**: {'; '.join(d['rejected_alternatives'])}")
        L.append(f"- **위험(risks)**: {d['risks']}")
        L.append(f"- **상태(status)**: {d['status']}")
        rc = ", ".join(f"`{c}`" for c in d["related_commits"]) or "(없음)"
        L.append(f"- **관련 commit**: {rc}")
        if d["next_actions"]:
            L.append(f"- **다음 조치**: {'; '.join(d['next_actions'])}")
        L.append("")
    L.append("## Commit trail")
    L.append("")
    L.append("| hash | 내용 |")
    L.append("| --- | --- |")
    for h, desc in COMMITS:
        L.append(f"| `{h}` | {desc} |")
    L.append("")
    L.append("## 다음 cycle 후보")
    L.append("")
    for c in NEXT_CYCLE:
        L.append(f"- {c}")
    L.append("")
    MD_OUT.write_text("\n".join(L), encoding="utf-8")


def main():
    if not SOURCE_LOG.exists():
        print(f"WARN: source decision log not found: {SOURCE_LOG}", file=sys.stderr)
    write_jsonl()
    write_markdown()
    print(f"decision records: {len(DECISIONS)} -> {JSONL_OUT.relative_to(ROOT)}")
    print(f"supervisor log   -> {MD_OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
