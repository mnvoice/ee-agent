---
title: trap-map active supervisor layer
date: 2026-05-23
branch: feat/phase-b-migration
type: active-supervisor-layer
tags:
  - ee-agent/trap-map
  - ee-agent/supervisor-decision
  - ee-agent/active-layer
related:
  - docs/audit/decision_records/trap_map_active_decisions.jsonl
  - docs/audit/trap_map_A_priority_pilot_learning_package_closeout_2026-05-22.md
  - docs/audit/trap_map_B_priority_pilot_learning_package_closeout_2026-05-22.md
  - docs/audit/trap_map_B_priority_gigi_18_steps_cleanup_followup_erratum_2026-05-23.md
  - docs/audit/trap_map_B_priority_gigi_17_record_identity_targeted_audit_2026-05-23.md
  - docs/audit/trap_map_B_priority_gigi_17_correction_plan_2026-05-23.md
---

# Trap-Map Active Supervisor Layer

이 문서는 trap-map 트랙의 **능동 감독 레이어**다. 각 audit/review/closeout 문서에 흩어진
판단을 다시 모아, 다음 작업자가 "무엇을 했는가"보다 먼저 **왜 그 선택을 했는가**를
확인하게 한다.

이 레이어는 정답 데이터가 아니다. 실행 로그도 아니다. 판단의 원장이다.

---

## 0. 왜 이 레이어를 만들었는가

trap-map 트랙은 단순 문서 작성이 아니었다. A-priority 26항과 B-priority 10항을 만들면서
우리는 여러 번 멈췄다. 대표 기출이 맞는지, 정답이 충돌하는지, source label이 추정인지,
record identity가 실제 PDF와 맞는지 확인했다. 그 과정에서 선택은 계속 생겼지만, 선택의
이유는 closeout·errata·review 문서 곳곳에 흩어졌다.

그 상태는 위험하다. 다음 작업자는 최신 문서 하나만 보고 "왜 교체하지 않았는지", "왜
data 수정을 미뤘는지", "왜 9항으로 낮췄다가 다시 10항으로 복귀했는지"를 다시 추론해야
한다.

그래서 이 문서가 맡는 일은 세 가지다.

1. 감독자의 선택을 한곳에 모은다.
2. 선택의 이유와 버린 대안을 같이 남긴다.
3. 다음 step의 허용 범위와 금지 범위를 먼저 보이게 한다.

---

## 1. 이 레이어의 작동 규칙

앞으로 trap-map 트랙에서 다음 상황이 생기면 decision record를 남긴다.

- PASS / NEEDS_FIX / BLOCKED / ACCEPT 같은 gate 판정이 바뀔 때
- blocked, caution, clean count가 바뀔 때
- data 수정 허용 범위가 열릴 때
- "교체", "보류", "정정", "문서만 정정", "data normalization" 중 하나를 선택할 때
- 웹 reviewer와 CLI reviewer의 판단이 갈리고 감독자가 어느 쪽을 채택할 때
- 기존 closeout 이후 새 결함이 발견되어 상태를 정정할 때

각 decision은 최소한 다음 필드를 갖는다.

| 필드 | 의미 |
|---|---|
| id | 고유 decision id |
| date | 판단 날짜 |
| scope | 어떤 항목/트랙에 대한 판단인지 |
| decision | 감독자가 고른 결론 |
| rationale | 왜 그 결론인지 |
| rejected_alternatives | 왜 다른 선택을 하지 않았는지 |
| state_effect | clean count, blocked/caution, next gate에 미친 영향 |
| next_gate | 다음에 통과해야 할 gate |
| forbidden_until_gate | 다음 gate 전까지 금지되는 일 |

구조화 레코드는 `docs/audit/decision_records/trap_map_active_decisions.jsonl`에 함께 둔다.

---

## 2. 현재 상태 요약

최신 기준은 2026-05-23 현재 다음과 같다.

| 영역 | 상태 |
|---|---|
| A-priority | 26항 / 31문제 closeout 완료 |
| B-priority pilot | 10항 학습 패키지 작성 완료 |
| 사용 가능 | 36항 / 41문제 |
| 완전 클린 | 35항 / 40문제 |
| caution | 1항 / 1문제 = 기기-17 |
| blocked | 0항 / 0문제 |
| 기기-18 | answer/choice/solution/steps 정정 후 완전 클린 복귀 |
| 기기-17 | content는 유효하지만 source identity mismatch가 남아 caution 유지 |

기기-17은 아직 완전 클린이 아니다. 이유는 보기 artifact나 solution 오류만이 아니라,
`2020_1회_52`라는 storage/source label이 실제 PDF source와 어긋난 record identity 문제이기
때문이다.

---

## 3. 핵심 감독 판단

### D1 — A-priority 26항 package를 closeout으로 인정

**결정:** A-priority 26항 / 31문제는 학습자 사용 준비 완료로 closeout한다.

**이유:** study set, day plan, inline trap cues, pilot learning logs, package review를 거쳐
coverage·partial+sub·adjacent·exact 검증을 통과했다. deferred `2001_3회_43`은 외부 교재
필요 항목으로 별도 보류했다.

**버린 대안:** A-priority를 더 넓히기. 이유는 26항 패키지가 먼저 닫혀야 B-priority 확장
기준을 만들 수 있기 때문이다.

**상태 영향:** A-priority 26항 / 31문제 유지.

### D2 — B-priority는 full expansion이 아니라 10항 pilot으로 제한

**결정:** B-priority 전체 확장이 아니라 10항 pilot만 진행한다.

**이유:** B-pool은 source-clean 상태가 A보다 약했다. 초기 representative dryrun에서 10항 중
5항이 탈락했다. 이 조건에서 바로 확장하면 정답 충돌·OCR 손상·mismatch가 학습 패키지로
들어갈 위험이 컸다.

**버린 대안:** B 전체 확장. 이유는 reserve 소진, 회로 커버리지 0, S/F 편중이 이미 드러났기
때문이다.

**상태 영향:** B-priority는 10항 pilot만 closeout 대상으로 삼는다.

### D3 — B initial dryrun 실패 후 replacement를 먼저 한다

**결정:** needs_replacement 5항은 학습 패키지로 보내지 않고 replacement selection을 먼저 한다.

**이유:** 기기-19 mismatch, 기기-25 정답 충돌, 기기-28 source-clean fail, 설비-30 OCR 손상,
회로-20 정답 충돌이 확인됐다. representative-ready 추정은 full-content 검증에서 과대평가된
것으로 본다.

**버린 대안:** caution으로 포함. 이유는 정답 충돌과 source-clean fail은 학습자에게 오답을
줄 수 있어 caution 수준이 아니기 때문이다.

**상태 영향:** replacement 후 redryrun 10/10 PASS로 B study set v1 작성 가능 상태가 됐다.

### D4 — v3.2 source integrity 이슈는 A/B pilot을 자동 무효화하지 않는다

**결정:** v3.2 corrected actionable 문서의 count/source-label 이슈는 별도 errata로 분리하고,
A/B pilot은 자동 무효화하지 않는다.

**이유:** A/B pilot은 v3.2를 최종 정답 source가 아니라 주제 목록 source로 사용했고,
representative questions는 별도 dryrun/redryrun으로 검증했다. confirmed issue는 주로 §5.2
cell count 오류와 "대표 보기 함정"의 추정 label 문제였다.

**버린 대안:** A/B 산출물 전면 무효화. 이유는 후속 문서들이 항목 단위 검증을 별도로 수행했기
때문이다.

**상태 영향:** v3.2는 canonical source로 쓰기 전 보완 필요. A/B pilot은 계속 진행.

### D5 — 기기-18은 즉시 교체하지 않고 공식 source 대조를 먼저 한다

**결정:** 기기-18은 needs_replacement로 즉시 빼지 않고, 공식 정답표/PDF 대조를 최우선으로
한다.

**이유:** answer·choice·solution이 충돌했지만, 문항 자체가 건전할 가능성이 남아 있었다.
공식 PDF 대조로 정답을 확정할 수 있으면 reserve를 더 쓰지 않고 원 항목을 살릴 수 있다.

**버린 대안:** 9항 세트로 고정, 즉시 replacement. 이유는 기기-18이 B-pilot coverage에서
의미 있는 변압기 등가회로 항목이었고, source 대조 비용이 낮았기 때문이다.

**상태 영향:** 기기-18은 공식 PDF 기준 answer 4, choice "절연내력"으로 정정 가능함이 확인됐다.

### D6 — 기기-18은 correction track으로 보낸다

**결정:** 기기-18은 needs_replacement가 아니라 correction track으로 처리한다.

**이유:** 원본 PDF에서 문제·보기·풀이·정답이 명확했고, questions.json의 answer/choice/solution
오류가 source-grounded하게 정정 가능했다.

**버린 대안:** 대표 문항 교체. 이유는 문항 자체가 clean source였고, 오류는 데이터 필드 문제였기
때문이다.

**상태 영향:** Commit A(answer/choice), Commit B(solution), Commit C(steps)를 거쳐 기기-18은
caution에서 완전 클린으로 복귀했다.

### D7 — 기기-18 steps는 rewrite가 아니라 null cleanup으로 처리

**결정:** 기기-18 `steps`는 문제 47 풀이로 억지 재작성하지 않고 `null`로 둔다.

**이유:** 원본 PDF 풀이가 개념형 분류 단락이라 `{인식, 변환, 계산}` schema로 자연스럽게
나뉘지 않는다. 재작성은 새 해설 창작 위험이 있다. corpus 내 `steps=null` 선례도 있다.

**버린 대안:** source-grounded rewrite. 이유는 PDF에 없는 단계 구조를 만들어야 하므로 G-1 위반
위험이 높았다.

**상태 영향:** 기기-18은 완전 클린으로 전환, clean count는 완전 클린 35/40으로 상승.

### D8 — 기기-17은 단순 cleanup이 아니라 record identity 문제로 격상

**결정:** 기기-17은 보기 artifact/solution cleanup만 하지 않고, record identity normalization
track으로 격상한다.

**이유:** `questions.json 2020_1회_52` 본문은 변압기 Delta-Y 권수비 문제인데, 실제 2020년 1회
52번 PDF는 동기전동기 V곡선 문제였다. 또한 `2020_1,2회_52`가 실제 2020년 1회 52번과 맞았다.
이는 단순 OCR 문제가 아니라 source label mismatch다.

**버린 대안:** choices/solution만 정정. 이유는 잘못된 source label 아래 본문만 깨끗하게 만드는
것은 무결성을 회복하지 못하기 때문이다.

**상태 영향:** 기기-17은 caution 유지. true source audit로 넘어간다.

### D9 — 기기-17 true source는 2022-04-24 표지 PDF q52로 본다

**결정:** 기기-17 변압기 Delta-Y 권수비 문제의 true source는 `data/20200424_1회.pdf` page 4
q52로 기록한다. 표지 기재 일자는 2022-04-24다.

**이유:** PDF page 4 q52가 본문·보기·정답과 정합했고, q41 sanity check도 같은 PDF와 맞았다.
`questions_기출_2020_1회.json` 100항 전체가 실제로는 2022년 1회 content일 가능성이 생겼다.

**주의:** `20200424`가 `20220424`의 typo라는 판단은 강한 가설로 둔다. 파일명/metadata 정정은
B-track 전수 측정 후에만 결정한다.

**상태 영향:** 학습 content는 valid. source 표기와 data identity는 아직 caution.

### D10 — 기기-17 N3a는 학습 문서 표기만 먼저 정정한다

**결정:** 기기-17은 A-track을 먼저 적용한다. W-1 학습 패키지 3종에서 대표 기출 표기와 PDF
보기 인용만 정정하고, data/id/meta는 건드리지 않는다.

**이유:** 학습자에게 보이는 source 혼동을 먼저 줄일 수 있고, data key/id 수정은 app 참조 영향과
100항 일괄 가능성이 있어 고위험이다.

**버린 대안:** questions.json metadata 즉시 정정. 이유는 `2020_1회` set 전체, per-year json,
PDF filename, app route/index 영향이 아직 측정되지 않았기 때문이다.

**상태 영향:** A-track은 학습 문서 보호 조치다. 기기-17 caution 해제는 아직 아니다.

---

## 4. 현재 active queue

| 우선순위 | 작업 | 상태 | gate |
|---|---|---|---|
| 1 | 기기-17 N3a A-track 적용 리뷰 | `b69ab80` 로컬 커밋 확인됨, push/review 필요 | N3a diff review |
| 2 | 기기-17 B-track 영향 측정 | 대기 | 100항 sanity + app id grep |
| 3 | 기기-17 data normalization plan | 대기 | B-track plan gate |
| 4 | 기기-17 redryrun | 대기 | A/B 정정 후 |
| 5 | clean count 갱신 | 대기 | 기기-17 caution 해제 가능 시 |
| 6 | v3.2 §5.2 cell 오류 v3.3 정정 | 대기 | 별도 source integrity track |
| 7 | 추출 파이프라인 인접 문항 혼입 회귀 방지 | 대기 | pipeline hygiene track |

---

## 5. 현재 금지 범위

다음 gate 전까지 금지한다.

- `questions.json`의 기기-17 id/year/session/q_no 수정
- `data/questions_기출_2020_1회.json` 수정
- PDF filename 또는 pdf_pages 디렉터리 rename
- app code route/index 수정
- 기기-17 caution 해제 선언
- B-priority full expansion
- C/D fallback 폐기 선언

---

## 6. 다음 작업자가 먼저 확인할 것

1. `git status -sb`
2. `git log -5 --oneline`
3. `b69ab80`이 push됐는지 여부
4. W-1 학습 패키지 3종만 바뀌었는지
5. 기기-17 외 카드가 바뀌지 않았는지
6. `2020_1회_52`가 W-1 기기-17 대표 기출 표기로 남아 있지 않은지
7. `2022_1회_52`, `2022-04-24`, `data/20200424_1회.pdf page 4 q52` caveat가 들어갔는지

---

## 7. 이 레이어의 원칙

우리는 빠르게 많은 것을 고치는 쪽보다, 왜 멈추고 왜 진행했는지를 남기는 쪽을 택했다.
그 이유는 단순하다. 이 트랙의 품질은 정답 하나가 아니라, 다음 사람이 같은 함정을 다시
밟지 않게 하는 기억에서 나온다.

이 문서는 그 기억을 능동적으로 관리하는 자리다.

