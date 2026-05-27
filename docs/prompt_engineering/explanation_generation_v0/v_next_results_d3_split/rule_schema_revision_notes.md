# Rule Schema Revision Notes — v0.1 Draft

| 항목 | 값 |
|---|---|
| 상태 | REVISION_LOG_ONLY |
| 작성일 | 2026-05-27 |
| 본 문서 단계 | Rule Schema Artifact Revision Gate 부속 |
| 다루는 범위 | 원천 3종 → 본 게이트 산출물 3종으로의 변경 추적 |

---

## 1. 본 문서의 목적과 범위

Claude Web 초안 3종을 본 게이트 산출물 3종으로 정돈하는 과정에서 적용한 정정 항목을 명세화한다. 본 문서는 revision log이며 새로운 규약을 정의하지 않는다.

### 1.1 본 문서가 다루지 않는 것

- 새 규약·새 enum·새 threshold 정의
- v0.2 → v0.1-draft 인스턴스 마이그레이션 결정
- validator 구현 결정
- governance 적용 도구 결정

---

## 2. 원천 3종과 산출물 3종 대응

| 원천 (검토 입력) | 본 게이트 산출물 |
|---|---|
| `/private/tmp/ee_agent_rule_schema_sources/rule_schema_design.md` | `rule_schema_design_v0.1.md` |
| `/private/tmp/ee_agent_rule_schema_sources/rule_schema_v0.3_draft.json` | `rule_schema_v0.1_draft.schema.json` + `ee_agent_rule_profile_v0.1_draft.json` (2분할) |
| `/private/tmp/ee_agent_rule_schema_sources/policy_change_rules.json` | profile 파일의 predicate·check 카탈로그 역추출 입력 (인스턴스 자체는 산출물에 포함 없음) |

세 원천 중 어느 파일도 그대로 cp 되지 않았다. 본 게이트 산출물은 원천 구조를 재배치·재명명·재분할한 결과이다.

---

## 3. 적용된 정정 항목

### 3.1 schema_version 정정

| 원천 표기 | 본 게이트 정정 |
|---|---|
| `schema_version: "0.3-draft"` | `schema_version: "0.1-draft"` |

이유:

- 본 게이트는 schema 자체의 1차 정돈이다. v0.2 인스턴스(`policy_change_rules.json`)와 무관한 별도 버전 체계이다.
- 원천의 `0.3-draft`는 인스턴스 마이그레이션 의도와 혼동될 수 있다.
- schema 파일은 자체 버전(`0.1-draft`)으로 시작하고, 인스턴스 마이그레이션은 별도 migration gate의 책임으로 분리한다.

### 3.2 profile_version 신설

| 원천 | 본 게이트 |
|---|---|
| profile에 별도 version 없음 (schema 안에 통합) | profile 파일 root에 `profile_version: "0.1-draft"` 신설 |

이유:

- 본 게이트가 schema 파일과 profile 파일을 분리한 결과, profile 파일도 독자적 버전 표기가 필요하다.
- schema_version과 profile_version은 독립적으로 진화 가능 (예: ee-agent 카탈로그 추가는 profile만 변경, schema는 무변동).

### 3.3 파일명 정정

| 원천 파일명 | 본 게이트 파일명 |
|---|---|
| `rule_schema_v0.3_draft.json` | `rule_schema_v0.1_draft.schema.json` (`.schema.json` 확장 명시) |
| (원천 없음) | `ee_agent_rule_profile_v0.1_draft.json` (도메인명 prefix + `profile` 명시) |
| `rule_schema_design.md` | `rule_schema_design_v0.1.md` (버전 명시) |

이유:

- `.schema.json` 확장은 JSON Schema 표준 관례에 정합.
- 도메인 prefix `ee_agent_`는 profile 파일이 도메인 의존임을 파일명에서 명시.
- 버전 suffix `_v0.1`은 동일 폴더 내에서 후속 버전과 공존 가능하도록 명시.

### 3.4 schema 파일과 profile 파일 분리

| 원천 구조 | 본 게이트 정정 |
|---|---|
| 단일 JSON Schema 파일 안에 `core`와 `profile`(ee-agent 카탈로그·threshold 포함)이 함께 있음. ee-agent predicate·check 카탈로그가 schema 파일에 실제 값으로 들어 있음. | schema 파일에는 domain-neutral contract만 (Core + ProfileContract). ee-agent 실제 카탈로그·threshold 값은 profile 파일로 분리. |

이유:

- schema 파일이 ee-agent 카탈로그를 실제 값으로 포함하면 다른 도메인(react-confidence·추천시스템 등) 재사용이 어렵다.
- profile 파일은 도메인 어휘를 자유롭게 갱신해도 schema 파일은 무변동.
- validator는 (schema, profile) 두 입력을 cross-check한다.

### 3.5 root naming 통일

schema 파일 root 키:

| 원천 | 본 게이트 |
|---|---|
| `schema_metadata` | `schema_metadata` (유지) |
| `core` | `core` (유지) |
| `profile` (안에 실제 ee-agent 값 포함) | `profile_contract` (profile 파일이 따라야 할 형식만, 실제 값 없음) |
| `Rule` definition만 존재 | `rule_contract` root 신설 (definitions의 Rule을 root에서 참조) |
| `ChangeReportShape` definition만 존재 | `change_report_contract` root 신설 (definitions의 ChangeReport를 root에서 참조) |

profile 파일 root 키 (원천에 없음, 본 게이트 신설):

- `profile_metadata`
- `domain_taxonomy`
- `predicate_library`
- `check_library`
- `threshold_proposals`
- `aggregation_policy`
- `claim_boundary` (역추출 초안임을 표기)

이유:

- root 키를 명사·`_contract` 접미사로 통일하여 schema와 profile 사이 매핑이 시각적으로 명확하다.
- 설계 문서(`rule_schema_design_v0.1.md`)의 chapter 구성과 root 키 이름이 1:1 대응한다.

### 3.6 JSON Schema 한계 명시

원천 schema 파일에는 cross-check 한계 항목이 명시되어 있지 않았다. 본 게이트는 schema 파일과 설계 문서 양쪽에 `known_limits` 8종(L1~L8)을 명시한다.

| 한계 | 검증 책임 |
|---|---|
| L1 Rule.id uniqueness | 후속 validator gate |
| L2 PredicateCall.predicate_id ↔ profile.predicate_library 일치 | 후속 validator gate |
| L3 PredicateCall.args ↔ predicate별 args_schema | 후속 validator gate |
| L4 Verdict.category ↔ profile.domain_taxonomy.category_enum 일치 | 후속 validator gate |
| L5 AutomatedCheckCall.function_id ↔ profile.check_library 일치 | 후속 validator gate |
| L6 AutomatedCheckCall.parameters ↔ check별 parameters_schema | 후속 validator gate |
| L7 Rule.priority_group과 Verdict.severity 조합 정합성 | 도메인 규약 미정의 (후속 검토) |
| L8 RuleMetadata.deprecation_signal과 verification_status 일관성 | 정책 검사 미정의 (후속 검토) |

이유:

- 본 게이트의 JSON Schema는 형식 검증만 책임진다. 도메인 cross-check는 별도 도구가 필요하다.
- 한계를 schema 자체에 메타로 명시하여 후속 validator gate 진입 시 누락 위험을 줄인다.

### 3.7 threshold proposal 유지

| 원천 표기 | 본 게이트 정정 |
|---|---|
| `policy_change_rules.json`의 `alert_thresholds`에 confirmed-looking 값 4종 존재 (5·10·60·15). | profile 파일의 `threshold_proposals`에 4종 (60·5·10·2). 모두 `status: "proposal"`. JSON Schema에서 `ThresholdProposal.status`를 `const: "proposal"`로 고정. |

이유:

- 60·5·10·2 값은 D-3 관찰·초기 추측 출처이며 380 entry 풀 전수 검증이 없다.
- proposal 표기 없이 사용하면 후속 게이트에서 확정값으로 오인될 가능성이 있다.
- 본 schema_version에서는 `status: "proposal"` 외 값을 schema 차원에서 거부한다.

### 3.8 명칭 변경 — verdict_1st → verdict 4필드 객체

| 원천(v0.2 인스턴스) | 본 게이트 |
|---|---|
| `verdict_1st: "INVESTIGATE_RECOVERABILITY"` (단일 문자열) | `verdict: {severity, category, auto_action, rationale}` 4필드 객체 |

본 게이트는 verdict 표현을 4차원으로 분리한다. 인스턴스 마이그레이션은 본 게이트가 수행하지 않으며, breaking change로 schema_metadata.migration_paths에 기록한다.

### 3.9 priority 정렬식 → priority_group enum

| 원천(v0.2 인스턴스) | 본 게이트 |
|---|---|
| `rule_priority: "R12 > R8 > R6 > R4 > R1/R2/R3/R10/R11 > R5 > R9 > R7"` (자연어 문자열) | `Rule.priority_group: "critical"|"major"|"standard"|"minor"` (core enum) |

이유:

- 자연어 정렬식은 도구가 파싱하기 어렵고 명세 외 규칙 추가 시 재작성이 필요하다.
- enum 기반 priority_group은 다중 매칭 정렬·aggregation 입력으로 직접 사용 가능하다.
- 정렬 ranking이 필요할 경우 enum 순서(critical → minor)가 우선순위로 사용된다.

### 3.10 어휘 정정

원천 표현 중 `pre_change_declaration_template.example.change_intent`의 "정밀화" 등은 유지. 본 게이트 산출물 전체에 한국어 표준 동사 정책을 적용했고, 비표준 결합 표현은 사용하지 않았다.

---

## 4. 본 게이트가 적용하지 않은 변경

다음 항목은 원천과의 차이가 있더라도 본 게이트에서 변경하지 않았다.

| 항목 | 사유 |
|---|---|
| v0.2 인스턴스 12 규칙의 본 schema 형식 변환 | 본 게이트의 단일 목적 범위 외. 별도 migration gate. |
| validator 도구 작성 | 별도 validator gate. |
| threshold 4종 확정 | 별도 confirmation gate. |
| governance 적용 도구 작성 | 별도 implementation gate. |
| `scripts/` 어떤 파일도 수정 안 함 | 본 게이트 hard 금지. |
| 기존 `policy_change_rules.json` 수정 안 함 | 본 게이트 hard 금지. |
| commit·push | 본 게이트 hard 금지. |
| DEVLOG·Vault·MEMORY·decision JSONL 작성 | 본 게이트 hard 금지. |

---

## 5. 본 게이트의 claim boundary

| 단계 | 본 게이트가 주장 가능한 것 |
|---|---|
| (a) 직접 정의 | schema·profile 파일 구조, root 키, core enum, predicate·check 인터페이스, Rule·Verdict·ChangeReport 형식 |
| (b) 초안 추출 | ee-agent predicate 7종·check 10종 카탈로그 (v0.2 인스턴스에서 역추출, 실측 검증 없음) |
| (c) Proposal | threshold 4값 (60·5·10·2). 모두 D-3 관찰 또는 초기 추측. 확정 표기 없음. |

본 게이트는 (a)에 대해서만 형식 정합성을 주장한다. (b)와 (c)는 후속 게이트의 검증을 전제로 한다.

---

## 6. 본 게이트 종료 후 자연스러운 다음 단계

후속 게이트 후보는 `rule_schema_design_v0.1.md` §16에 명시되어 있다. 순서·병행은 사용자 결정 영역이다.

---

## 7. 최종 상태

`READY_FOR_RULE_SCHEMA_REVIEW_GATE`
