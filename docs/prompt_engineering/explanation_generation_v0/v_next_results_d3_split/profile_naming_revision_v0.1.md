# Profile Naming Revision v0.1

작성일: 2026-05-28
작성 목적: ee-agent schema-first governance 흐름에서 누적된 naming/state vocabulary 사용을 일관 어휘로 정리한다. 본 문서는 새 구현이 아니라 어휘 governance 보존 기록이며, schema·profile·instance 파일 자체를 수정하지 않는다.

## 0. Gate Title

Profile Naming Revision Gate (v0.1) — Vocabulary Governance Decision

## 1. Scope

본 게이트가 다루는 영역:

- 다음 어휘의 사용 컨텍스트와 충돌 진단: `draft / candidate / confirmed / proposal / proposed / policy / record / review / profile / instance / schema / threshold / mandatory / optional / advisory / deferred / review_later / accepted / rejected / superseded`
- ee-agent rule schema / profile / instance 3 자산 사이의 의미 경계 명시
- 파일 자산 명명 규칙 (`<topic>_<v0.x>_draft.<ext>` / `_v0.x.md` 패턴)
- 버전 라벨 (`<major>.<minor>-draft` vs `<major>.<minor>`) 의미
- 분류 상태 enum의 도메인별 분리 (threshold / L7 policy / review gate / runtime data state)
- decision/policy/record/design/report 문서 접미사 구분

본 게이트가 다루는 분리 보조 단원 (Profile Scope Definition):

- schema/profile/instance 3 자산의 책임 영역
- 다른 도메인 이식 시 명명 변환 영역
- 본 단원은 별도 Profile Scope Decision Gate로 증식하지 않는다 (사용자 명시 지시).

## 2. Non-goals

본 게이트가 수행하지 않는 작업:

- schema/profile/instance 파일 자체의 내용 수정 (`rule_schema_v0.1_draft.schema.json`, `ee_agent_rule_profile_v0.x_draft.json`, `policy_change_rules_v0.x_draft_instance.json` 수정 0)
- scripts/ 수정
- validator 실행
- threshold profile 반영
- L7 enforcement 도입
- Instance v0.2 구현
- MVP Roadmap 결정
- Threshold Confirm 추가 결정 (v0.1 결정은 `threshold_confirmation_decision_v0.1.md`에서 이미 완료)
- 전기자기학 제외 결정
- curriculum mapping의 정책 승격
- gate_metrics mandatory 도입
- harness/ontology engineering 완료 주장
- DEVLOG · Vault · MEMORY · decision JSONL 작성
- Profile Scope를 별도 gate로 분리

## 3. Vocabulary Inventory Summary

조사 범위:

- `docs/prompt_engineering/explanation_generation_v0/decision_records/`
- `docs/prompt_engineering/explanation_generation_v0/v_next_results_d3_split/`
- `docs/prompt_engineering/explanation_generation_v0/v_next_policy/`
- `docs/prompt_engineering/explanation_generation_v0/v3_policy/`
- `docs/prompt_engineering/explanation_generation_v0/v_full_policy/`
- v_next_results_d3_split 산하 schema/profile/instance JSON 3 자산

### 3.1 어휘별 빈도 (md / json)

| 어휘 | md 빈도 | json 빈도 | 1차 의미 |
|---|---:|---:|---|
| draft | 92 | 29 | pre-stable 자산 또는 외부 JSON Schema spec name |
| candidate | 60 | 4 | gate 후보 또는 keyword matching candidate |
| confirmed | 27 | 0 | threshold 분류 상태 (승격 결정) |
| proposal | 56 | 18 | threshold 분류 상태 (초안 유지) |
| proposed | 0 | 0 | 미사용 |
| policy | 293 | 31 | 5+ 컨텍스트 다의어 |
| record | 190 | 0 | 보존 기록 또는 일반 동사 |
| review | 135 | 8 | gate type 또는 lifecycle status |
| profile | 241 | 34 | 도메인 catalog (ee-agent specific) |
| instance | 110 | 4 | 실제 rule 데이터 |
| schema | 244 | 30 | ee-agent rule schema 또는 외부 JSON Schema |
| threshold | 86 | 27 | threshold_proposals 4종 |
| mandatory | 2 | 0 | gate_metrics 미승격 어휘 |
| optional | 9 | 0 | rule schema 필드 |
| advisory | 0 | 0 | 미사용 |
| deferred | 36 | 0 | threshold 상태 또는 decision doc deferred items |
| review_later | 52 | 2 | L7 policy 분류 상태 |
| accepted | 10 | 0 | review gate 결과 |
| rejected | 9 | 0 | review gate 결과 |
| superseded | 0 | 0 | 미사용 (lessons protocol 후보) |

### 3.2 명확한 의미가 확립된 사례

- schema/profile/instance 3 자산의 정의가 `ai_agent_curriculum_mapping_record_v0.1.md` §0 및 `profile_catalog_boost_design_v0.2.md`에 일관 진술
- `_draft.json` 파일명 suffix 의미: pre-stable, 변경 가능 자산
- `v0.x-draft` 버전 라벨 의미: SemVer pre-release 의미
- threshold 3 상태 (`confirmed / proposal / deferred`)는 `threshold_confirmation_decision_v0.1.md`에 명확 등록
- L7 3 상태 (`allowed / review_later / disallowed`)는 `l7_policy_decision_v0.1.md`에 명확 등록
- `decision / rationale / deferred items` 형식이 `schema_validator_implementation_decisions_v0.1.md`에 패턴 확립

### 3.3 의미가 충돌하는 사례

CF1. `policy` 다의어 (5+ 컨텍스트):
- ee-agent 아키텍처 Policy Layer (`ee_agent_development_spec_v0.1.md` §5.2)
- L7·L8 policy decision gate 산출물
- policy_change_governance design rule (R1~R12)
- hard_check policy mode
- turning point policy 초안 (`development_turning_point_policy_v0.1.md`)
- curriculum mapping의 "정책 아님" 진술

CF2. `draft` 4 가지 의미:
- 버전 라벨 suffix (`0.1-draft`, `0.2-draft`)
- 파일명 suffix (`*_draft.json`)
- 외부 JSON Schema spec name (`JSON Schema draft-07`)
- profile_metadata `status: "draft"` (자산 lifecycle 상태)

CF3. `schema` 2 가지 의미:
- ee-agent rule schema (`rule_schema_v0.1_draft.schema.json` 본 게이트가 정의한 form)
- 외부 JSON Schema 표준 (`$schema`, `draft-07`)

CF4. `review` 2 가지 의미:
- gate type ("Review Gate" 패턴: 작성 → review → commit → push)
- schema_metadata.status enum 값 (`["draft", "review", "approved", "deprecated"]`)

CF5. `deferred` 2 가지 도메인:
- threshold 분류 상태 (proposal 4종 중 T4 결정)
- decision document의 `deferred items` (본 게이트 범위 외, 다음 gate로 이월)

CF6. `candidate` 2 가지 도메인:
- gate 후보 옵션 표기 ("후보 P-naming", "후보 T-review")
- keyword matching candidate (`split_design_adjustment.md` 14 candidate, 242 hits)

CF7. JSON `status` 필드 3 가지 컨텍스트:
- schema_metadata / profile_metadata: lifecycle (`draft / review / approved / deprecated`)
- threshold_proposals: classification (`proposal` const)
- args (D-3 runtime data): runtime state (`CLEAN / GAP / NEEDS_REVIEW`)

### 3.4 같은 의미를 다른 어휘로 부르는 사례

- `proposed` (0 hits) vs `proposal` (74 hits md+json) — `proposed`는 사실상 미사용, `proposal`로 단일화
- "후보" (한글) vs `candidate` (영문) — gate 후보 의미에서 두 어휘가 동일 의미로 혼용

### 3.5 같은 어휘가 서로 다른 의미로 쓰이는 사례

CF1·CF2·CF3·CF4·CF5·CF6·CF7과 동일. 위 7건이 본 항목의 전체이다.

### 3.6 확정 상태 vs 초안 상태가 애매한 사례

- `development_turning_point_policy_v0.1.md` 파일명에 `policy` 포함되지만 내용은 "초안" 진술 (§0)
- `ai_agent_curriculum_mapping_record_v0.1.md` 파일명에 `record` 포함되어 정책 아님이 명확
- `hard_check_policy_design.md`는 `policy` + `design` 결합, 즉 "policy의 design" 의미 (실 적용 0)

→ 이 3 사례는 본 게이트가 R6 (문서 접미사 구분 룰)로 해소한다.

## 4. Term Collision Findings

| # | 충돌 | 분류 | 조치 |
|---|---|---|---|
| CF1 | `policy` 다의어 (5+ 컨텍스트) | CLARIFY | 사용 시 컨텍스트 prefix 또는 파일명에서 `policy / design / record / decision` 접미사로 구분 |
| CF2 | `draft` 4 가지 의미 | CLARIFY | 외부 JSON Schema 표기 시 `JSON Schema draft-07` 정확 인용. 내부 `0.x-draft`는 SemVer pre-release 의미 일관 유지 |
| CF3 | `schema` 2 가지 의미 | CLARIFY | 내부 = "ee-agent rule schema" 또는 "rule schema". 외부 = "JSON Schema" 표기 |
| CF4 | `review` 2 가지 의미 | CLARIFY + PROMOTE_LATER | 즉시 RENAME 없음. Schema v0.2 진입 시 schema_metadata.status enum의 `"review"` → `"under_review"` RENAME 검토 후보 등재 |
| CF5 | `deferred` 2 가지 도메인 | CLARIFY | threshold = 4종 분류 상태 중 하나. decision doc `deferred items` = 본 gate 범위 외 항목. 두 도메인 분리 명시 |
| CF6 | `candidate` 2 가지 도메인 | CLARIFY | gate 후보 (governance) vs keyword matching candidate (D-3 data). 두 도메인 분리 |
| CF7 | JSON `status` 3 가지 컨텍스트 | CLARIFY | metadata.status (자산 lifecycle) / threshold_proposals.status (분류) / args.status (runtime data). 도메인별 분리. 본 게이트는 schema 파일 변경 0이므로 RENAME 없음 |
| CF8 | `proposed` 0 hits | DO_NOT_USE | `proposal`로 단일화. 새 글에서 `proposed` 도입 금지 |
| CF9 | `advisory` 0 hits | PROMOTE_LATER | policy/record 중간 등급 어휘 후보. 즉시 도입 0 |
| CF10 | `superseded` 0 hits | PROMOTE_LATER | lessons protocol 후보. 즉시 도입 0 |
| CF11 | `mandatory` 2 hits | PROMOTE_LATER | turning point policy §5.1 미승격 어휘. 즉시 도입 0 |

OK 분류 (현재 의미 유지 가능):

- `profile / instance / schema` 3 자산 분리 정의는 일관성 통과 (CF3 외부 충돌은 CLARIFY로 해소)
- `confirmed / proposal / deferred` (threshold) 분류 어휘
- `allowed / review_later / disallowed` (L7) 분류 어휘
- `accepted / rejected` (review gate 결과) 어휘
- `_draft.json` 파일 suffix
- `<topic>_v0.x.md` 보고/결정 문서 suffix
- `decision / rationale / deferred items` 형식

RENAME 분류:

- 본 게이트에서 즉시 RENAME 박지 않는다 (사용자 명시 금지: schema/profile/instance 자체 변경 0).

DEMOTE 분류:

- 본 게이트에서 즉시 DEMOTE 박지 않는다.

## 5. Profile Scope Definition (Gate 내부 섹션)

본 단원은 별도 Profile Scope Decision Gate로 분리하지 않는다. 본 게이트의 어휘 정리 범위 안에서만 정의한다.

### 5.1 schema의 책임 영역

- 정의: rule을 어떤 형태로 적을 수 있는지의 form definition
- 현재 자산: `rule_schema_v0.1_draft.schema.json`
- domain-neutral 여부: 부분적. `SchemaMetadata`, `ProfileContract`, `Rule`, `ChangeReportContract` 구조는 domain-neutral 후보. 단, 일부 const (예: `schema_version` const `"0.1-draft"`) 및 일부 필드는 ee-agent 운영 가정에 묶여 있어 완전 domain-neutral 주장은 본 게이트 범위 외
- 본 게이트는 schema의 domain-neutral 비율을 측정하지 않는다.

### 5.2 profile의 책임 영역

- 정의: 해당 도메인에서 허용되는 catalog (category_enum, predicate_library, check_library, threshold_proposals, HumanReviewGuideline)
- 현재 자산: `ee_agent_rule_profile_v0.1_draft.json`, `ee_agent_rule_profile_v0.2_draft.json`
- domain 여부: ee-agent specific
- 다른 도메인 이식 시: 새 profile 파일을 도메인 prefix와 함께 신규 작성 (예: `<도메인>_rule_profile_v0.x_draft.json`)

### 5.3 instance의 책임 영역

- 정의: 실제 rule 데이터 객체 (v0.2 기준 12 rules)
- 현재 자산: `policy_change_rules_v0.1_draft_instance.json`, `policy_change_rules_v0.2_draft_instance.json`
- domain 여부: ee-agent specific
- 다른 도메인 이식 시: 새 instance 파일을 도메인 prefix와 함께 신규 작성

### 5.4 v0.x가 schema / profile / instance / validator 중 어느 것의 버전인가

본 게이트의 결정:

- v0.x 버전 라벨은 **자산 단위로 독립**한다.
- 현재 시점:
  - schema = `0.1-draft` (유지)
  - profile = `0.2-draft` (boost 후)
  - instance = `0.2-draft` (boost 후)
  - validator = `0.1.0`
- 자산 간 호환성은 schema_metadata.compatible_with_instance_versions 및 profile_metadata.compatible_schema_version 필드로 표기한다.
- 본 게이트는 이 호환성 필드를 수정하지 않는다.

### 5.5 다른 도메인 이식 시 명명 변환

- schema: `rule_schema_v0.x_draft.schema.json` 형식 재사용 가능 (domain-neutral 부분만)
- profile: `<도메인>_rule_profile_v0.x_draft.json` (도메인 prefix 필수)
- instance: `<도메인>_rules_v0.x_draft_instance.json` 또는 도메인 특화 명명
- 이식 결정 자체는 본 게이트 범위 외 — 향후 별도 Multi-Domain Profile Cross-Check Gate 영역

## 6. Naming Rules (Decision)

### R1. 파일 자산 명명 패턴

- `<topic>_v<major>.<minor>_draft.<ext>` = pre-stable 자산
  - 예: `ee_agent_rule_profile_v0.2_draft.json`, `policy_change_rules_v0.2_draft_instance.json`, `rule_schema_v0.1_draft.schema.json`
- `<topic>_v<major>.<minor>.md` = 보고/결정/정책/설계/기록 문서
  - 예: `l7_policy_decision_v0.1.md`, `threshold_confirmation_decision_v0.1.md`, `development_turning_point_policy_v0.1.md`, `profile_naming_revision_v0.1.md`
- `<date>_<topic>.md` = decision_records/ 폴더의 phase decision/handoff/policy 문서
  - 예: `2026-05-27_d3_power_item_policy_promotion.md`

### R2. 버전 라벨 의미

- `v<major>.<minor>-draft` = pre-stable SemVer pre-release. 변경 가능 자산
- `v<major>.<minor>` (suffix `-draft` 0) = stable 승격 시 사용 (현재 ee-agent에 stable 자산 0)
- 외부 JSON Schema 표기는 항상 `JSON Schema draft-07` 형식으로 정확 인용. 내부 `0.1-draft`와 혼용 금지

### R3. 자산 lifecycle status enum

- 현재 정의 (`rule_schema_v0.1_draft.schema.json`): `["draft", "review", "approved", "deprecated"]`
- 본 게이트는 enum 자체를 변경하지 않는다.
- PROMOTE_LATER 후보: Schema v0.2 진입 시 `"review"` → `"under_review"` RENAME 검토. 본 게이트에서 결정 아님

### R4. 분류 상태 어휘 (도메인별 분리)

- threshold 분류: `confirmed / proposal / deferred` (3 상태)
- L7 policy 분류: `allowed / review_later / disallowed` (3 상태)
- review gate 결과: `accepted / rejected` (필요 시 사용)
- runtime data state (D-3 도메인): `CLEAN / GAP / NEEDS_REVIEW` (governance와 분리)

각 도메인의 상태 어휘를 다른 도메인에 직접 차용하지 않는다.

### R5. Decision/Gate 결과 문서 어휘 패턴

- `decision / rationale / deferred items` 형식 유지
- `deferred items` = 본 게이트 범위 외, 다음 gate로 이월되는 항목
- "후보 <식별자>: <Gate name>" = 다음 권장 gate 표기. `candidate` 영문도 동일 의미. keyword matching candidate와 도메인 분리

### R6. 문서 접미사 구분

| 접미사 | 의미 | 예시 |
|---|---|---|
| `_policy` | 조직적 구속력 또는 governance rule layer | `development_turning_point_policy_v0.1.md`, `hard_check_policy_design.md` |
| `_record` | 보존 기록 (정책 아님) | `ai_agent_curriculum_mapping_record_v0.1.md` |
| `_design` | 설계 문서 (구현 0) | `profile_catalog_boost_design_v0.2.md`, `schema_validator_design_v0.1.md` |
| `_decision` | 1회성 판정 | `l7_policy_decision_v0.1.md`, `threshold_confirmation_decision_v0.1.md` |
| `_report` | 실행 결과 보고 | `schema_validator_run_report_v0.1.md` |
| `_review` | read-only 검토 결과 | `ee_agent_srs_multilayer_review_v0.1.md`, `item_split_manifest_shift_review.md` |
| `_revision` | 어휘/구조 정리 (본 문서) | `profile_naming_revision_v0.1.md`, `rule_schema_revision_notes.md` |
| `_spec` | 기준 문서 | `ee_agent_development_spec_v0.1.md` |

이 접미사 룰은 신규 문서 작성 시 권장이며, 기존 문서를 본 게이트가 RENAME 박지 않는다.

### R7. proposed → proposal 단일화

- `proposed` 어휘 신규 도입 금지
- 기존 0 hits이므로 즉시 RENAME 작업 0
- 새 문서/JSON에서는 `proposal`로 일관

### R8. PROMOTE_LATER 어휘 (mandatory / advisory / superseded)

- 본 게이트에서 즉시 도입 0
- 향후 필요 시 별도 gate에서 도입 결정. 도입 전 본 문서 갱신 (`profile_naming_revision_v0.2.md` 신규)

### R9. 본 게이트가 schema/profile/instance 자체를 수정하지 않는다

- naming 룰은 governance docs 일관성만 책임
- schema_metadata.status enum 값, threshold_proposals.status const, 파일명 등 모든 JSON 자산은 본 게이트 변경 0
- 향후 Schema v0.2 / Profile v0.3 / Instance v0.3 진입 시 본 문서의 PROMOTE_LATER 후보들을 입력 자료로 사용

## 7. Decision

본 게이트의 핵심 결정:

D1. 어휘 충돌 11건 (CF1~CF11)을 식별하고 분류했다. CLARIFY 7건 / PROMOTE_LATER 3건 / DO_NOT_USE 1건.

D2. schema / profile / instance 3 자산의 책임 영역을 §5에 명시했다.

D3. 자산별 v0.x 버전이 독립 운영됨을 §5.4에 명시했다.

D4. 파일 자산 명명 패턴 R1을 권장으로 등재했다. 기존 파일 RENAME 0.

D5. 버전 라벨 의미 R2를 명시했다. 외부 `JSON Schema draft-07`과 내부 `0.x-draft` 분리.

D6. 자산 lifecycle status enum (R3)에 PROMOTE_LATER 후보 1건 (`"review"` → `"under_review"`) 등재. 즉시 RENAME 0.

D7. 분류 상태 어휘 R4를 도메인별 분리로 확정.

D8. 문서 접미사 R6 (`_policy / _record / _design / _decision / _report / _review / _revision / _spec`) 권장 등재.

D9. `proposed` DO_NOT_USE (R7).

D10. `mandatory / advisory / superseded` PROMOTE_LATER (R8).

D11. 본 게이트는 schema/profile/instance 자산 파일 변경 0 (R9).

## 8. Claim Boundary

본 문서가 주장하는 것:

- 본 게이트 시점의 어휘 사용 빈도와 충돌 사례 (§3, §4)
- schema/profile/instance 3 자산의 책임 영역 (§5)
- naming/state vocabulary 권장 룰 R1~R9 (§6)

본 문서가 주장하지 않는 것:

- MVP Roadmap이 결정되었다는 주장
- Threshold가 confirmed로 profile에 반영되었다는 주장
- Instance v0.2가 구현되었다는 주장
- curriculum mapping이 정책으로 승격되었다는 주장
- gate_metrics가 mandatory가 되었다는 주장
- 전기자기학이 제외되었다는 주장
- L7 enforcement가 도입되었다는 주장
- harness/ontology engineering이 완성되었다는 주장
- schema/profile/instance JSON 자산 파일이 변경되었다는 주장
- 기존 문서들의 파일명이 본 게이트로 RENAME되었다는 주장
- `"review"` → `"under_review"` RENAME이 적용되었다는 주장 (PROMOTE_LATER 후보 등재만)
- mandatory/advisory/superseded 어휘가 도입되었다는 주장 (PROMOTE_LATER 후보 등재만)
- Profile Scope가 별도 gate로 분리되었다는 주장 (본 게이트 §5 내부 단원으로 처리)
- 본 게이트가 다른 도메인 이식을 결정했다는 주장 (Multi-Domain Cross-Check Gate 범위 외)

## 9. Follow-up Gates

| 후보 | 단일 목적 |
|---|---|
| 후보 N-review: Profile Naming Revision Review Gate | 본 문서가 commit 가능한지 read-only 검토 |
| 후보 N-commit: Profile Naming Revision Commit Gate | review 통과 후 본 문서 1건만 commit |
| 후보 N-push: Profile Naming Revision Push Gate | commit 후 원격 보존 |
| 후보 I-impl: Instance v0.2 Implementation Gate | `policy_change_rules_v0.2_draft_instance.json` 신규 작성 (R1 명명 패턴 적용 사례) |
| 후보 T-extra: Threshold Confirm Extension Gate | 다중 사례 누적 후 4종 재검토 (현재 confirmed 0) |
| 후보 M-mvp: MVP Roadmap Decision Gate | development spec §3.1 기반 3과목 결정 |
| 후보 S-promote: Schema v0.2 Status Enum Rename Gate | `"review"` → `"under_review"` 등 lifecycle 어휘 PROMOTE 결정 (PROMOTE_LATER 해소) |
| 후보 V-revision: Validator Boundary Revision Gate | L7 enforcement 도입 (별도 gate) |
| 후보 R-multi-domain: Multi-Domain Profile Cross-Check Gate | profile/instance 이식 시 명명 변환 (현재 ee-agent 1 도메인) |

자연 후속: 후보 N-review.

## 10. Success Criteria

본 게이트의 성공 판정:

- §1 Scope 명시
- §2 Non-goals 명시
- §3 Vocabulary Inventory Summary 완성 (20 어휘 빈도 + 충돌/OK 사례 분류)
- §4 Term Collision Findings 11건 분류
- §5 Profile Scope Definition 5 하위 단원 완성, 별도 gate 분리 없음
- §6 Naming Rules R1~R9 등재
- §7 Decision D1~D11 명시
- §8 Claim Boundary 본 게이트 금지 claim 명시
- §9 Follow-up Gates 9 후보 목록
- §10 Success Criteria (본 단원)
- 본 게이트가 schema/profile/instance JSON 자산 파일 수정 0
- 본 게이트가 scripts/ 수정 0
- 본 게이트가 validator 실행 0
- 본 게이트가 threshold profile 반영 0
- 본 게이트가 L7 enforcement 도입 0
- 본 게이트가 DEVLOG/Vault/MEMORY/decision JSONL 작성 0
- 본 게이트가 MVP Roadmap / Threshold Confirm / Instance v0.2 / curriculum mapping policy 승격 / gate_metrics mandatory / 전기자기학 제외 / harness completion claim 0
- 어휘 규칙 위반 0 (V1~V5 비표준 결합 미사용)

다음 자연 gate: 후보 N-review (Profile Naming Revision Review Gate).
