# Trap-Map B-Priority Pilot — Study Set v1 Review (2026-05-22)

B-priority pilot study set v1(`08041ec`)을 day plan 착수 전 검토한다. v3.2 source
integrity errata(`2e62f7e`)까지 반영된 시점에서, study set v1이 day plan 작성
가능 상태인지 7개 기준으로 판정한다.

이번 단계는 리뷰 문서 작성만 — day plan·learning log 미작성. app/data·
questions.json 미수정. solution/steps 미적용. answer/choices/text 미수정. 유료 API
미호출. local server 미실행.

- 리뷰 대상: `docs/audit/trap_map_B_priority_pilot_study_set_v1_2026-05-22.md`
- 대조 참조:
  - `docs/audit/trap_map_B_priority_10_item_representative_redryrun_2026-05-22.md`
  - `docs/audit/trap_map_B_priority_replacement_selection_2026-05-22.md`
  - `docs/audit/trap_map_v3_2_source_integrity_errata_2026-05-22.md`

---

## 판정: **PASS** — B-priority pilot day plan 작성 가능

study set v1은 7개 리뷰 기준을 모두 충족한다. P0·P1 결함 없음. P2 1건(errata
교차 참조 부재)은 day plan 진행을 막지 않는 문서 위생 항목이다.

→ **B-priority pilot day plan 작성 가능.** P2는 day plan 또는 study set v1.1에서
선택적으로 흡수 가능(필수 아님).

---

## 1. 기준별 검토

### 기준 1 — 10항 coverage ✅

study set v1 §1 학습 카드 10장 + §2 요약표 10행 = 기기-17·18·4·23, 설비-13·14·
10·21, 전력-25·18. redryrun proposed include 10항과 ID·대표 기출 전수 일치.
과목 분포 기기 4 / 설비 4 / 전력 2 / 회로 0 정합.

### 기준 2 — redryrun 판정 ready/ready_with_note 10/10 유지 ✅

| 항목 | study set 판정 | redryrun 판정 | 일치 |
|---|---|---|:--:|
| 설비-13, 전력-18 | ready | ready | ✅ |
| 기기-17·18·4·23, 설비-14·10·21, 전력-25 | ready_with_note | ready_with_note | ✅ |

ready 2 / ready_with_note 8 / needs_replacement 0 / defer 0 — redryrun(`6164d6f`)
판정 그대로. 임의 승격·강등 없음.

### 기준 3 — exact 3 / adjacent 7 정직 표기 ✅

study set §0·§2·§4가 일관되게 exact 3 / adjacent 7로 표기. 항목별:
- exact 3: 기기-17, 설비-13, 전력-18
- adjacent 7: 기기-18·4·23, 설비-14·10·21, 전력-25

redryrun §검증표 alignment(exact 3 / adjacent 7)와 항목 단위까지 전수 일치.
adjacent를 exact로 끌어올린 항목 없음.

### 기준 4 — adjacent 항목 원래 카드 함정 / 대표 기출 함정 분리 ✅

adjacent 7항 전부 카드에 별도 라인 2개("원래 카드 함정:" / "대표 기출이 검증하는
함정:")를 두고, 후자에 "→ 원래 카드 함정...과 **다르다**"를 명시:

| 항목 | 원래 카드 함정 | 대표 기출이 검증하는 함정 | 분리 |
|---|---|---|:--:|
| 기기-18 | 1차/2차 환산 혼동 | 시험-파라미터 식별 | ✅ |
| 기기-4 | %Z↔효율 연결 | 철심 포화 시 거동 | ✅ |
| 기기-23 | 2차 저항제어 효율 | 형식별 적용 가능성 | ✅ |
| 설비-14 | 상하 배치 순서 | 이격거리 수치 | ✅ |
| 설비-10 | 사용 가능 조건 | 접속 거리 수치 | ✅ |
| 설비-21 | 과전류 단일 | 냉각이상 보호 | ✅ |
| 전력-25 | 만능 계전기 | 전압요소 필요 여부 축 | ✅ |

exact 3항은 "→ 원래 카드 함정과 동일(exact)"로만 표기 — redryrun이 questions.json
대조로 확인한 결과이므로 과장 아님. "외울 핵심 문장"·"3회독 체크 질문"은 카드
core와 기출 포인트를 함께 다루나, 함정 분류 라인은 분리 유지 — 혼입 없음.

### 기준 5 — 기기-17 LaTeX artifact 표시 ✅

study set 기기-17 카드:
- 판정 **ready_with_note** (exact alignment이나 artifact로 note 부여).
- 주의 문장에 보기 [1] LaTeX `√3·aV/√3` 잉여 √3 명시, "물리 풀이·정답 키(1)·trap
  정합", "학습 자료 노출 전 `aV/√3`로 cleanup" 명시.
- §5 다음 단계 #2에 "day plan 착수 전 cleanup: 기기-17 보기 [1] LaTeX 잉여 √3"
  재기재 — questions.json DQ 트랙 대상으로 표시.

ready_with_note 취급 + cleanup 대상 표시 둘 다 충족. redryrun의 ready→
ready_with_note 조정 사유와 일치.

### 기준 6 — residual 3건 day plan 이전 리스크 기록 ✅

study set §3 Residual에 3건 전수 기록 + 각 발생 원인 설명 + "day plan·learning
log 단계로 그대로 이월" 명시:
1. 회로 커버리지 0 (B등급 유일 회로 항목 회로-20 제외, 보충 불가)
2. trap type S/F 6/10 편중 (B-pool 자체 S/F 편중)
3. reserve 5항 소진 (대체 투입 후보 0)

§5 다음 단계 #3 "residual 3건은 day plan·learning log 단계에서 명시적으로 안고
간다" 재확인. day plan 이전 리스크로 충분히 기록됨.

### 기준 7 — v3.2 errata 영향 반영 ✅ (P2 1건)

- **"대표 보기 함정" 과장 여부**: study set은 v3.2 "대표 보기 함정"을 "원래 카드
  함정"으로 인용하되, 이를 검증 완료 사실로 제시하지 않는다. 별도로 "대표 기출이
  검증하는 함정"을 두고 exact(동일)/adjacent(다름)로 결과를 표기 — v3.2 추정과
  실제 기출 검증 결과를 구분. 과장 없음. errata F5의 "(c) 추정" 성격을 구조적으로
  반영.
- **exact/adjacent 분리가 추정 약점 흡수**: adjacent 7항의 함정 분리 표기(기준 4)가
  errata F5가 지적한 "대표 보기 함정이 실제 기출과 다를 수 있다"를 항목 단위로
  흡수. errata §3 근거 4가 이미 이 점을 study set v1의 무결성 근거로 인정.
- **errata F2(§5.2 오류) 영향**: study set은 §5.2를 인용하지 않고 redryrun·
  replacement selection 경로(§4 본문 기반)를 따르므로 F2 무관 — 정상.

→ errata의 실질 영향은 study set v1에 구조적으로 반영됨. 단 study set v1은 errata
(`2e62f7e`)보다 먼저 작성(`08041ec`)되어 **errata 문서를 교차 참조하지 않는다**.
이는 P2(아래).

---

## 2. 수정 필요 항목

### P0 (day plan 차단) — 없음

### P1 (day plan 전 권장) — 없음

### P2 (선택, day plan 비차단) — 1건

- **P2-1 errata 교차 참조 부재**: study set v1은 v3.2 errata보다 먼저 작성되어
  errata를 참조하지 않는다. study set의 "원래 카드 함정" 라인이 v3.2 (c) 추정에서
  온 것임을 errata F5 기준으로 명시하면 추적성이 향상된다. 단 errata §3이 이미
  study set v1을 invalidate 대상에서 제외하고 무결성을 인정했으므로, 이는 정확성
  결함이 아닌 문서 위생 항목. day plan 문서 서두 또는 study set v1.1에서 errata
  pointer 한 줄 추가로 해소 가능 — **필수 아님**.

---

## 3. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 7개 기준 전수 검토 | ✅ 기준 1~7 |
| 10항 coverage | ✅ 기기 4 / 설비 4 / 전력 2 / 회로 0 = 10 |
| redryrun 판정 일치 | ✅ ready 2 / ready_with_note 8 — 항목 단위 전수 일치 |
| exact 3 / adjacent 7 | ✅ redryrun alignment와 항목 단위 일치 |
| adjacent 함정 분리 | ✅ 7항 전부 "원래 카드 함정 ≠ 대표 기출 함정" 분리 |
| 기기-17 artifact | ✅ ready_with_note + cleanup 대상 2곳 표시 |
| residual 3건 | ✅ §3에 전수 + day plan 이월 명시 |
| errata 영향 반영 | ✅ 구조적 반영, P2 1건(교차 참조 부재) |
| P0/P1/P2 분류 | ✅ P0 0 / P1 0 / P2 1 |
| 판정 출력 | ✅ PASS + day plan 작성 가능 명시 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps 미수정 / API·server 미실행 / day plan·learning log 미작성 / amend·rebase·reset 없음 |

---

## 4. 결론

- 판정: **PASS**.
- P0 0건 / P1 0건 / P2 1건(errata 교차 참조 부재 — 비차단).
- **B-priority pilot day plan 작성 가능.** day plan 착수 시 권장:
  1. 기기-17 보기 [1] LaTeX·기기-18 보기 [4] 용어 cleanup(questions.json DQ 트랙).
  2. residual 3건(회로 커버리지 0 / S/F 6/10 편중 / reserve 소진)을 day plan
     문서에 리스크로 명시 이월.
  3. (선택) P2-1 — day plan 서두에 v3.2 errata pointer 추가.

(이 문서는 study set v1 리뷰까지 — day plan·learning log는 별도 트랙·별도 승인.)

---

## Status

- B-priority pilot study set v1(`08041ec`) 리뷰 완료 — 7개 기준 전수 검토.
- 판정 **PASS**. P0 0 / P1 0 / P2 1(errata 교차 참조 부재, 비차단).
- 10항 coverage·redryrun 판정 10/10·exact 3/adjacent 7·adjacent 함정 분리·
  기기-17 artifact 표시·residual 3건·errata 영향 반영 — 전부 충족.
- **B-priority pilot day plan 작성 가능.**
- 이 문서는 리뷰 문서다. day plan·learning log·산출물 수정 없음.
