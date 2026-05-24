# Trap-Map B-Priority — 기기-17 B-Track Decision Record (2026-05-25)

기기-17 B-track correction plan v2와 203c380 review 결과를 받아, alias schema 작성
전에 필요한 정책 판단을 기록한다. 본 문서는 실행 decision이 아니라 다음 설계의
입력값을 정리하는 decision record다.

이번 단계는 decision record 작성까지다. **app/data, `questions.json`, per-year json,
PDF filename, `pdf_pages/index.json`은 수정하지 않는다.** push 없음. amend/rebase/reset
없음. 기기-17 caution 유지. q52 단독 id 재발급 금지 유지.

- 관련 plan: `docs/audit/trap_map_B_priority_gigi_17_B_track_correction_plan_v2_2026-05-25.md`
- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`
- latest plan-hardening commit: `203c380`
- active decision id: `DR-TRAP-GIGI17-BTRACK-ALIAS-FIRST-GATE`

---

## 1. Decision Summary

| 항목 | 결정 |
|---|---|
| B-track primary direction | Alias-first를 다음 설계 검토 대상으로 진입 |
| Batch migration | 보류. 100항 source evidence, 66항 policy, persisted key migration 전에는 실행 금지 |
| canonical + legacy 상태 | clean으로 보지 않는다. caution 유지 상태에서 alias schema와 review gate로 이동 |
| alias table SoT | 위험 회피 우선 시 tracked docs registry를 1차 SoT 후보로 둔다(plan v2 §3.1A 기준) |
| Docs Errata Only | cleanup이 아니라 temporary preservation state로 분류 |
| `2020_1,2회` 66항 | 기기-17 q52와 분리된 별도 systemic session-label 트랙 |
| acceptance criteria | plan v2 §7 measurable criteria를 caution release review 입력으로 사용 |

---

Alias-first는 실행 결정이 아니다. alias schema plan에서 SoT, integrity check, user-facing
impact, app/data 반영 여부를 다시 gate로 다룬다.

## 2. Rationale

Alias-first를 다음 설계 검토 대상으로 진입시키는 이유:

- app `_id`가 progress, annotations, wrong-note filter, pdfPageIndex lookup에 사용된다.
- `2020_1회` 100항 batch mis-label 가능성이 있어 q52 단독 id 재발급은 위험하다.
- `2022_1회` 슬롯은 비어 있지만, Batch migration은 data/app/pdf_pages/user persisted
  key를 함께 다루어야 한다.
- Alias-first는 legacy storage key를 유지하면서 canonical source를 표현할 수 있어
  다음 설계 단계의 blast radius가 작다.

Batch migration을 보류하는 이유:

- `2020_1회` 100항 전체 source claim이 아직 전수 확정되지 않았다.
- `2020_1,2회` 66항 session policy가 별도로 필요하다.
- app persisted key migration 또는 compatibility alias가 설계되지 않았다.
- `pdf_pages/index.json` key 이동/alias 정책이 실행 수준으로 확정되지 않았다.

canonical + legacy 상태를 caution으로 유지하는 이유:

- canonical source가 문서화되어도 storage key가 legacy인 상태는 user-facing 혼동 가능성이 남는다.
- app/data 또는 authoritative alias registry가 아직 없다.
- caution 해제는 alias SoT, integrity checks, app/display evidence, redryrun, review가 필요하다.

---

## 3. Rejected Alternatives

| 대안 | 기각 사유 |
|---|---|
| q52 단독 `2022_1회_52` 재발급 | 100항 batch 가능성과 app persisted key 영향을 무시함 |
| `questions.json` 즉시 수정 | app key, per-year, pdf_pages, closeout/errata sync 없이 source identity만 바뀜 |
| Batch migration 즉시 실행 | 66항 policy와 user data compatibility가 미정 |
| Docs Errata Only를 cleanup으로 간주 | app/user-facing source identity가 legacy key 중심으로 남음 |
| 기기-17 caution 해제 | measurable criteria와 review gate 미완료 |

---

## 4. Next Gates

1. Alias schema plan 작성
   - docs registry SoT 후보를 기준으로 schema를 먼저 정의한다.
   - one-way storage, bidirectional validation 원칙을 포함한다.
   - app/data 반영은 별도 승인 전 금지한다.
2. Alias integrity check 설계
   - duplicate storage mapping, intentional shared canonical mapping, dangling ids, source PDF/page/q_no 정합을 점검한다.
3. Caution release review format 적용
   - plan v2 §6.3과 §7 measurable criteria를 사용한다.
4. `2020_1,2회` 66항 별도 plan
   - Alias-first 실행 여부와 별개로 systemic session-label 트랙으로 유지한다.

---

## 5. Forbidden Until Next Gate

- q52 단독 id 재발급
- `questions.json` year/session/q_no 수정
- per-year json 수정
- PDF filename rename
- `pdf_pages/index.json` 수정
- app read-path alias resolver 구현
- Docs Errata Only 신규 문서 작성
- 기기-17 caution 해제 선언

---

## Status

- Decision record 작성 완료.
- 다음 본작업은 alias schema plan.
- data/app/pdf_pages 미수정.
- 기기-17 caution 유지.
