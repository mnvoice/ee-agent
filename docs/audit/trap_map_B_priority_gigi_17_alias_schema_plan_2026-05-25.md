# Trap-Map B-Priority — 기기-17 Alias Schema Plan (2026-05-25)

기기-17 B-track decision record 이후, Alias-first 설계 검토를 위한 alias schema를
정의한다. 본 문서는 **schema plan**이며, alias registry artifact 생성이나 app/data
반영을 실행하지 않는다.

이번 단계는 docs-only schema plan 작성까지다. **app/data, `questions.json`, per-year
json, PDF filename, `pdf_pages/index.json`은 수정하지 않는다.** push 없음.
amend/rebase/reset 없음. 기기-17 caution 유지. q52 단독 id 재발급 금지 유지.

- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`
- 관련 correction plan: `docs/audit/trap_map_B_priority_gigi_17_B_track_correction_plan_v2_2026-05-25.md`
- 관련 decision record: `docs/audit/trap_map_B_priority_gigi_17_B_track_decision_record_2026-05-25.md`
- active decision id: `DR-TRAP-GIGI17-BTRACK-ALIAS-FIRST-GATE`

---

## 0. Scope

Alias-first는 실행 결정이 아니라 **다음 설계 검토 대상**이다. 이 plan은 alias row의
모양, validation, review evidence, 다음 gate를 정의한다.

이 plan에서 하지 않는 일:

- alias registry 파일 생성
- app alias resolver 구현
- app/data alias table 추가
- question record metadata 추가
- `questions.json` 또는 per-year json 수정
- `pdf_pages/index.json` 수정
- 기기-17 caution 해제

---

## 1. Source-of-Truth Position

tracked docs registry는 plan v2 §3.1A의 **위험 회피 기본 선호 기준에 따른 1차 SoT
후보**다. 아직 확정된 SoT도, 생성된 artifact도 아니다.

| 후보 | 이 plan에서의 상태 | authoritative 시점 |
|---|---|---|
| tracked docs registry | 1차 후보 | registry artifact가 별도 승인/생성되고 review를 통과한 뒤 |
| tracked app data registry | 보류 | app/data 수정 승인, schema migration, app read-path review 뒤 |
| record metadata field | 보류 | `questions.json`/per-year 수정 승인과 migration plan 뒤 |
| app hardcoded mapping | 비선호 | 임시 실험 외 장기 SoT로 사용하지 않음 |

authoritative artifact 정의:

- **schema-authoritative**: 본 plan과 후속 schema review가 alias row shape와 validation을
  정의한다.
- **source-authoritative**: source PDF/page/q_no evidence는 targeted audit과 impact audit이
  담당한다.
- **runtime-authoritative**: app/data registry 또는 resolver는 아직 없다. 별도 승인 전까지
  runtime source of truth로 취급하지 않는다.
- **caution-release-authoritative**: caution release review가 별도 문서로 작성되기 전까지
  어떤 alias 문서도 caution 해제 근거가 아니다.

---

## 2. Alias Row Schema

alias registry가 생성될 경우, 최소 row는 아래 필드를 가진다.

| field | type | required | meaning |
|---|---|---:|---|
| `storage_id` | string | yes | app persisted key. 현재 `_id`와 같은 legacy key |
| `canonical_source_id` | string | yes | source citation용 canonical id |
| `source_pdf` | string | yes | source PDF path |
| `source_pdf_page` | number | yes | PDF page number, 1-based |
| `source_q_no` | number | yes | source PDF의 문제 번호 |
| `cover_date` | string | yes | PDF 표지 기재 일자, `YYYY-MM-DD` |
| `evidence_ref` | string | yes | audit/review 문서와 섹션 또는 commit reference |
| `status` | string | yes | `candidate`, `approved`, `superseded`, `blocked` 중 하나 |
| `notes` | string | no | residual risk, caution, filename/date caveat |

field rules:

1. `storage_id`는 app persisted key를 뜻한다. canonical id로 바꾸지 않는다.
2. `canonical_source_id`는 source citation id이며 app persisted key가 아니다.
3. `cover_date`는 시행일 확정이 아니라 "PDF 표지 기재 일자"로만 사용한다.
4. `status=candidate`는 design/review 전 상태다. caution 해제 근거가 아니다.
5. `status=approved`가 되려면 schema review, registry artifact approval, integrity check를
   통과해야 한다.
6. `status=superseded` 또는 `blocked`는 원 row를 삭제하지 않고 대체/차단 사유를 남긴다.
7. Active rows are `candidate` and `approved`. Historical rows are `superseded` and
   `blocked`.
8. `evidence_ref` should include both first-source audit evidence and downstream impact/decision
   evidence when both exist.

---

## 3. q52 Seed Row Example

아래는 registry 생성 시 사용할 수 있는 seed row 예시다. 이 예시는 **registry 생성이
아니며**, q52 단독 id 재발급도 아니다.

| field | value |
|---|---|
| `storage_id` | `2020_1회_52` |
| `canonical_source_id` | `2022_1회_52` |
| `source_pdf` | `data/20200424_1회.pdf` |
| `source_pdf_page` | `4` |
| `source_q_no` | `52` |
| `cover_date` | `2022-04-24` |
| `evidence_ref` | `trap_map_B_priority_gigi_17_record_identity_targeted_audit_2026-05-23.md §2, §3; trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md §1, §3` |
| `status` | `candidate` |
| `notes` | `legacy storage key retained; PDF filename/date mismatch handled as cover-date evidence; caution remains` |

source-clean constraints:

- `storage_id=2020_1회_52` remains the app storage key.
- `canonical_source_id=2022_1회_52` is a citation target, not a new app id.
- q52 alone must not be reissued as `2022_1회_52`.
- `source_pdf_page=4` and `source_q_no=52` must remain tied to the evidence audit.

---

## 4. Storage And Validation Model

Storage model:

- Store alias rows one-way: `storage_id -> canonical_source_id`.
- Do not store canonical rows as replacement question ids.
- Do not mutate question `_id`.
- Do not write app progress/annotation migration data in this phase.

Validation model:

- Build a temporary reverse index during validation:
  `canonical_source_id -> [storage_id...]`.
- Multiple storage ids pointing to one canonical id are allowed only if listed as intentional aliases.
- One storage id pointing to multiple canonical ids is not allowed.
- Validation output is evidence, not a runtime artifact.

This resolves the one-way storage / bidirectional validation split:

| layer | direction | purpose |
|---|---|---|
| registry storage | `storage_id -> canonical_source_id` | preserve app key ownership |
| validation reverse index | `canonical_source_id -> storage_id[]` | detect unintended many-to-one aliases |
| app persisted data | `storage_id` only | preserve progress/annotation compatibility |

---

## 5. Integrity Checks

Before any registry artifact can be approved, the following checks must pass.

| check | pass criterion |
|---|---|
| duplicate storage mapping | every `storage_id` has exactly one active `canonical_source_id`; historical `superseded`/`blocked` rows are excluded |
| intentional shared canonical | any `canonical_source_id` with multiple storage ids has an explicit intentional-alias note |
| dangling storage id | every `storage_id` exists in the current question set or is explicitly historical |
| orphan canonical id | every `canonical_source_id` has source PDF/page/q_no evidence |
| source 3-way evidence | `canonical_source_id`, `source_pdf_page`, `source_q_no` agree with cited audit evidence |
| q52 guardrail | q52 row is alias/inventory only; no app id reissue |
| status validity | all rows use allowed status values |
| evidence ref | every row links to an audit/review/decision artifact |

Initial q52 acceptance:

- q52 seed row may remain `candidate`.
- q52 seed row cannot be used to release caution.
- q52 seed row cannot trigger app/data changes.

---

## 6. User-Facing Impact Evaluation

User-facing impact must be evaluated before any alias resolver, display change, or caution release
review.

Trigger:

- app display begins showing `canonical_source_id`
- docs/current-state begins describing storage/canonical split as user-facing state
- alias registry moves from `candidate` to `approved`
- caution release review is requested

Evaluation methods:

| method | evidence |
|---|---|
| app screen smoke | screenshot or textual smoke result showing storage id and canonical source are not confused |
| display-layer code grep | grep result showing display/citation code path uses explicit storage/canonical naming |
| docs-only state diff | diff showing current-state/errata text distinguishes legacy storage from canonical source |
| reviewer checklist | caution release review confirms no user-facing id ambiguity |

Required result:

- If user-facing citation still shows only `2020_1회_52`, caution remains.
- If canonical source is shown, it must be labeled as source citation, not app id.
- If display creates ambiguity between storage id and source id, alias registry cannot move to
  `approved`.

---

## 7. Docs Errata Only vs Alias-First Schema

Docs Errata Only is a temporary preservation state. Alias-first schema is a structured design path.

| axis | Docs Errata Only | Alias-first schema |
|---|---|---|
| artifact | prose errata/current-state note | structured alias row schema |
| runtime effect | none | none until separately approved |
| caution release | not eligible by itself | still not eligible until review gates pass |
| validation | prose review only | integrity checks and evidence refs |
| app/data change | none | still none in this phase |

Docs Errata Only cannot be promoted into cleanup without an alias schema or Batch migration plan.

---

## 8. `2020_1,2회` 66항

The `2020_1,2회` 66항 issue remains a separate systemic session-label track.

Policy:

- Do not fold the 66항 policy into the q52 alias seed row.
- Do not use q52 alias schema to normalize `2020_1,2회`.
- Alias-first can proceed as schema design while 66항 remains a residual risk.
- Any caution release review must state whether unresolved 66항 risk is separable from q52 source
  citation cleanup.

Timing:

- Alias schema plan can be reviewed before the 66항 plan.
- After alias schema review passes, 66항 separability evaluation should start in parallel with
  registry artifact approval.
- Registry artifact approval should not claim that 66항 is resolved.
- Batch migration cannot proceed until the 66항 policy is defined.

---

## 9. Next Gates

1. **Schema review**
   - Review this document only.
   - Confirm row fields, guardrails, validation model, and q52 seed row.
2. **Registry artifact approval**
   - Decide whether to create a tracked docs registry artifact.
   - Decide exact path and format.
   - Still no app/data changes unless separately approved.
3. **66항 separability evaluation**
   - Decide whether unresolved `2020_1,2회` 66항 risk is separable from q52 source citation.
   - This may run in parallel with registry artifact approval.
   - Caution release review cannot skip this evaluation.
4. **Registry artifact creation**
   - Create the docs registry with q52 candidate row only if approved.
   - Run integrity checks.
5. **App/data decision**
   - Decide whether runtime resolver, app data registry, or record metadata is needed.
   - Requires separate approval and app-specific review.
6. **Caution release review**
   - Only after registry artifact, user-facing impact evidence, and redryrun evidence exist.

---

## 10. Forbidden Until Approved

- q52 단독 id 재발급
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- `pdf_pages/index.json` 수정
- app alias resolver 구현
- app/data alias table 추가
- record metadata field 추가
- Docs Errata Only를 cleanup으로 간주
- 기기-17 caution 해제 선언

---

## Status

- Alias schema plan 작성 완료.
- Registry artifact 미생성.
- app/data/pdf_pages 미수정.
- q52 단독 id 재발급 금지 유지.
- 기기-17 caution 유지.
- PASS/NEEDS_FIX 판정 없음.
