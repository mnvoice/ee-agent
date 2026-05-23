# Trap-Map Active State (2026-05-23)

이 문서는 trap-map active supervisor layer의 2층 현재 상태 요약이다. decision
record는 append-only 원장이고, 이 문서는 현재 작업자가 먼저 봐야 할 활성 상태다.

- 기준 branch: `feat/phase-b-migration`
- 기준 origin: `16c61f2`
- 현재 로컬 stack (hardening follow-up 작성 시작 시점):
  1. `b69ab80` docs: apply 기기-17 A-track source citation correction
  2. `02f7f4b` docs: add trap-map active supervisor layer
  3. `d450f67` docs: review 기기-17 A-track source citation correction
  4. `dd20392` docs: review trap-map active supervisor layer
- push 상태: 미수행
- 이 문서의 역할: 현재 열린 트랙, 금지 범위, 다음 gate, stale 후보를 한 화면에 둔다.
- hardening follow-up commit이 생성되면 push 전 `git log --oneline --decorate -6`로
  stack을 다시 확인한다.

---

## 1. 현재 판정

| 트랙 | 현재 상태 | 판정 |
|---|---|---|
| b69ab80 N3a A-track 적용 | review 완료 (`d450f67`) | PASS |
| 기기-17 caution | 유지 | content valid / source identity mismatch 잔존 |
| 02f7f4b active supervisor layer | review 완료 (`dd20392`) | NEEDS_FIX |
| push | 보류 | active layer hardening 후 재판단 |

---

## 2. 현재 count

| 구분 | 상태 |
|---|---|
| A-priority | 26항 / 31문제 closeout 완료 |
| B-priority pilot | 10항 학습 패키지 완료 |
| 사용 가능 | 36항 / 41문제 |
| 완전 클린 | 35항 / 40문제 |
| caution | 1항 / 1문제 = 기기-17 |
| blocked | 0항 / 0문제 |

기기-17 caution은 해제하지 않는다. N3a A-track은 학습 문서 표기 정정이며,
data/id/meta/source identity mismatch는 B-track 별도다.

---

## 3. Active Queue

| 우선순위 | 작업 | 상태 | next gate |
|---|---|---|---|
| 1 | active supervisor layer hardening | 본 follow-up에서 반영 | 1층/2층/3층 분리 반영 |
| 2 | hardening review | 대기 | active-state / audit protocol / JSONL append 검토 |
| 3 | push 여부 판단 | 대기 | local stack 전체 review |
| 4 | 기기-17 B-track 영향 측정 | 대기 | 100항 sanity + app id grep |
| 5 | 기기-17 data normalization plan | 대기 | B-track plan gate |
| 6 | 기기-17 redryrun | 대기 | A/B 정정 후 |
| 7 | clean count 갱신 | 대기 | 기기-17 caution 해제 가능 시 |

---

## 4. 현재 금지 범위

다음 gate 전까지 금지한다.

- push
- `questions.json`의 기기-17 id/year/session/q_no 수정
- `data/questions_기출_2020_1회.json` 수정
- PDF filename 또는 pdf_pages 디렉터리 rename
- app code route/index 수정
- 기기-17 caution 해제 선언
- B-priority full expansion
- C/D fallback 폐기 선언
- 02f7f4b amend/rebase/reset

---

## 5. Stale 후보

| 항목 | 이유 | 처리 |
|---|---|---|
| `02f7f4b` supervisor log §4 active queue | b69ab80 review가 `d450f67`로 이미 PASS 처리됨 | historical snapshot으로 강등, 본 active-state 문서를 canonical로 사용 |
| CLI 요약의 "origin 대비 2 commit ahead" | 실제 로컬은 `b69ab80`, `02f7f4b`, `d450f67`, `dd20392` 포함 | push 판단 전 `git log --oneline --decorate -6` 재확인 |

---

## 6. Cross-Track Dependency Watch

| decision | 영향 가능 트랙 | 필요한 확인 |
|---|---|---|
| 기기-17 source identity 정책 | questions.json, per-year json, pdf_pages, app route/index, clean count | B-track 전 app/data grep + 100항 sanity |
| active supervisor layer push | 이후 모든 trap-map decision 기록 방식 | hardening review PASS 전 push 금지 |
| 기기-17 caution 해제 | closeout, post-closeout errata, B-pilot count | data/id/meta 정합 결정 전 해제 금지 |

---

## 7. 다음 작업자가 먼저 볼 것

1. `git status -sb`
2. `git log --oneline --decorate -6`
3. 이 active-state 문서
4. `docs/audit/trap_map_active_supervisor_layer_review_2026-05-23.md`
5. `docs/audit/supervisor_audits/trap_map_supervisor_layer_audit_protocol_2026-05-23.md`

---

## Status

- 2층 active-state 문서 생성.
- b69ab80/d450f67은 PASS로 반영.
- 02f7f4b는 NEEDS_FIX로 반영.
- push 보류.
