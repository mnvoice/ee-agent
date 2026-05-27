# Rule Schema Design — v0.1 Draft

| 항목 | 값 |
|---|---|
| 상태 | DESIGN_ONLY |
| 작성일 | 2026-05-27 |
| 본 문서 단계 | Rule Schema Artifact Revision Gate 산출물 |
| 후속 단계 후보 | READY_FOR_RULE_SCHEMA_REVIEW_GATE |
| schema_version | `0.1-draft` |
| profile_version | `0.1-draft` |

---

## 0. 본 게이트의 단일 목적과 범위

Claude Web 초안 3종(`rule_schema_design.md`, `rule_schema_v0.3_draft.json`, `policy_change_rules.json`)을 검토 입력으로 사용하여 repo 내부에 정돈된 rule schema 산출물을 신규로 생성한다. 본 게이트는 원천 파일을 그대로 복사하지 않는다. 정정 사항을 적용한 신규 산출물만 만든다.

### 0.1 본 게이트에서 변경하지 않는 것

- `scripts/` 하위 어떤 파일도 수정하지 않는다.
- 기존 `policy_change_rules.json`은 수정하지 않는다.
- v0.2 → v0.3 마이그레이션을 실행하지 않는다.
- validator를 구현하지 않는다.
- governance 적용 도구를 작성하지 않는다.
- D-4 automation을 실행하지 않는다.
- input 재생성·generation 재실행·audit 재실행을 진행하지 않는다.
- commit·push를 진행하지 않는다.

### 0.2 원천 3종 반영 방식

| 원천 | 활용 방식 |
|---|---|
| `/private/tmp/ee_agent_rule_schema_sources/rule_schema_design.md` | 설계 원천 (조항·원칙 참고) |
| `/private/tmp/ee_agent_rule_schema_sources/rule_schema_v0.3_draft.json` | 구조 원천 (definitions·필드 참고) |
| `/private/tmp/ee_agent_rule_schema_sources/policy_change_rules.json` | v0.2 인스턴스 예시 (predicate·check 카탈로그 역추출 근거) |

세 원천 중 어느 것도 직접 복사하지 않았다. 본 산출물은 원천 구조를 재배치·재명명·재분할한 결과이다.

---

## 1. 설계 원칙

### 1.1 Schema First

규칙 인스턴스(v0.1·v0.2)를 추가로 작성하기 전에 형식 자체를 정의한다. 스키마 없이 인스턴스를 늘리면 형식 일관성이 ad-hoc 누적되어 도구가 추측에 의존하게 된다.

### 1.2 Schema 파일과 Profile 파일 분리

본 게이트는 단일 JSON 파일에 schema와 ee-agent profile을 함께 둔 원천 구조를 두 개의 파일로 분리한다.

| 파일 | 역할 | 도메인 의존성 |
|---|---|---|
| `rule_schema_v0.1_draft.schema.json` | domain-neutral contract만 정의. 형식 검증용 JSON Schema. | 무관 |
| `ee_agent_rule_profile_v0.1_draft.json` | ee-agent 도메인 값과 카탈로그 초안. status·category·predicate·check·threshold 실제 값. | ee-agent 의존 |

분리 이유:

- schema 파일이 ee-agent 카탈로그를 실제 값으로 포함하면 다른 도메인(react-confidence·추천시스템 등)이 동일 schema를 재사용하기 어렵다.
- profile 파일은 도메인 어휘를 자유롭게 갱신해도 schema 파일은 영향이 없다.
- validator는 (schema, profile) 두 입력을 cross-check한다.

### 1.3 Core + Profile 경계

`schema` 파일 내부는 `core`(도메인 무관 enum·인터페이스)와 `profile_contract`(profile 파일이 따라야 할 형식)로 다시 나뉜다. profile 파일은 `profile_contract`를 준수한다.

| 구분 | 정의 대상 | 위치 |
|---|---|---|
| core | priority_group·severity·auto_action·aggregation_method·criteria_combinator·verification_status enum / predicate·check 인터페이스 / multi-match report 형식 | schema 파일의 `core` 필드 |
| profile_contract | profile 파일이 가져야 할 root 키와 필드 형식 | schema 파일의 `profile_contract` 필드 |
| profile 실제 값 | status taxonomy·category enum·predicate 카탈로그·check 카탈로그·threshold 값·aggregation 선택 | profile 파일 |

### 1.4 Priority와 Severity 분리

| 차원 | 소속 | 어휘 | 의미 |
|---|---|---|---|
| priority_group | Rule 속성 | critical / major / standard / minor | 다중 매칭 정렬·final_action 산출 기준 |
| severity | Verdict 속성 | IMPROVEMENT / SOFT_ALERT / INVESTIGATE / SUSPECT / HARD_ALERT | 변동 심각도 라벨, 사람에게 표시 |

같은 규칙이 `priority_group=critical`이면서 `severity=IMPROVEMENT`일 수 있다. 예: GAP→CLEAN 회수 규칙은 잘못된 회수일 때 critical, 정합한 회수일 때 IMPROVEMENT.

### 1.5 다중 매칭 모두 보고 + Aggregation 분리

한 변동이 여러 규칙에 매칭되면 모든 verdict를 `all_matched_rules` 배열로 보고한다. 단, 도구가 자동 실행할 `final_action`은 `aggregation_method`로 1개 산출한다. 단일 verdict 압축은 보고 단계에서 수행하지 않는다.

### 1.6 Threshold Proposal 정책

profile 파일의 threshold 값은 모두 `status: proposal`로 표기한다. 본 게이트는 어떤 값도 확정하지 않는다. 확정은 별도 게이트의 책임이다.

---

## 2. Rule Contract

```
Rule:
  id                    # 고유 식별자, 패턴 ^R\d+(_[a-z]+)*$
  name                  # 사람 읽기용 이름
  scope                 # 적용 컨텍스트 (applicable_to·tested_in·domain_agnostic)
  priority_group        # core enum 4종
  metadata              # 출처·근거·검증 상태·폐기 신호
  criteria              # Predicate 배열 + combinator (AND/OR)
  verdict               # 4필드 (severity/category/auto_action/rationale)
  automated_check       # function_id + parameters + expected_return_type
  human_review_guidelines  # condition + action 배열
  examples              # 적용 사례 (선택)
```

### 2.1 ID 패턴

- `^R\d+(_[a-z]+)*$` (예: `R1`, `R11_recovery`)
- ID uniqueness는 JSON Schema의 패턴 매칭만으로는 보장되지 않는다. validator gate에서 인스턴스 배열 전수 검사로 별도 검증한다.

### 2.2 Scope

```
scope:
  applicable_to: ["item_policy_based_selector", ...]
  tested_in: ["ee-agent D-3", ...]
  domain_agnostic: boolean
```

domain_agnostic=true인 규칙은 core 후보 (현재 단계에서는 표기만, 자동 승격 없음).

---

## 3. Verdict Contract

```
Verdict:
  severity      # core enum (5종)
  category      # profile category_enum 중 1 (cross-check)
  auto_action   # core enum (4종)
  rationale     # 자유 텍스트
```

### 3.1 severity (core enum, 5종)

| 값 | 의미 |
|---|---|
| IMPROVEMENT | 정합한 개선 신호 |
| SOFT_ALERT | 경미한 변동, 모니터링만 |
| INVESTIGATE | 원인 분석 필요 |
| SUSPECT | 회귀 가능성 의심 |
| HARD_ALERT | 자동 차단, 즉시 검토 |

### 3.2 auto_action (core enum, 4종)

| 값 | 의미 |
|---|---|
| log_only | 기록만 |
| trigger_check | 자동 체크 트리거 |
| human_review | 사람 검토 요구 |
| block | 자동 진행 차단 |

### 3.3 category (profile enum)

profile 파일의 `domain_taxonomy.category_enum`에 정의된 값 중 하나여야 한다. cross-check는 validator gate의 책임이다.

### 3.4 rationale

자유 텍스트. 왜 이 verdict인가를 설명. 형식 검증 없음.

---

## 4. Predicate Contract

### 4.1 인터페이스 (core)

```
predicate_interface:
  id_pattern: ^[a-z][a-z0-9_]*$
  args_must_be_schema: true
  return_type: boolean
```

### 4.2 PredicateCall (Rule.criteria 내부)

```
PredicateCall:
  predicate_id: string  # profile.predicate_library에 정의된 id 중 1
  args: object          # 해당 predicate의 args_schema 준수
```

### 4.3 카탈로그 위치

predicate 카탈로그 실제 값은 profile 파일의 `predicate_library`에 있다. schema 파일에는 인터페이스만 있다.

### 4.4 cross-check 의무

- `PredicateCall.predicate_id`가 `profile.predicate_library[*].predicate_id` 안에 있는지 확인
- `PredicateCall.args`가 해당 predicate의 `args_schema`를 따르는지 확인

두 항목 모두 JSON Schema 기본 검증으로는 보장되지 않는다. validator gate에서 구현한다.

---

## 5. Automated Check Contract

### 5.1 인터페이스 (core)

```
check_interface:
  id_pattern: ^[a-z][a-z0-9_]*$
  parameters_must_be_schema: true
  return_type_required: true
```

### 5.2 AutomatedCheckCall (Rule 내부)

```
AutomatedCheckCall:
  function_id: string                # profile.check_library에 정의된 id 중 1
  parameters: object                 # 해당 check의 parameters_schema 준수
  expected_return_type: string       # 선택, 명시 권장
```

### 5.3 cross-check 의무

- `function_id`가 `profile.check_library[*].function_id` 안에 있는지 확인
- `parameters`가 해당 check의 `parameters_schema`를 따르는지 확인

JSON Schema 기본 검증으로 보장되지 않는다. validator gate에서 구현한다.

---

## 6. Human Review Contract

```
HumanReviewGuideline:
  id: string         # 패턴 ^G\d+$
  condition: string  # 자유 텍스트
  action: string     # 자유 텍스트
```

Rule.human_review_guidelines는 위 객체의 배열. 비어 있을 수 있다.

---

## 7. Multi-Match Report Contract

```
ChangeReport:
  change_id: uuid
  context:
    before_hash: string
    after_hash: string
    tool_hash: string
    policy_hash: string
  all_matched_rules:
    - rule_id
      verdict (4필드 전체)
      priority_group
      matched_criteria_evidence  # object
  final_action: auto_action enum
  aggregation_method_used: aggregation_method enum
```

### 7.1 보고 원칙

- 매칭된 모든 규칙의 verdict를 압축 없이 그대로 포함한다.
- final_action만 aggregation 결과 1개를 별도로 둔다.

---

## 8. Aggregation Policy

### 8.1 core 측 enum (3종)

| method | 동작 |
|---|---|
| highest_priority_wins | priority_group 최상위 규칙의 auto_action 사용 (기본 권장) |
| most_severe_wins | severity 최상위 규칙의 auto_action 사용 |
| conservative_combine | 가장 보수적 action 선택 (block > human_review > trigger_check > log_only) |

### 8.2 profile 측 선택

profile 파일의 `aggregation_policy.method`에서 위 3종 중 하나를 선택한다. ee-agent profile은 `highest_priority_wins`를 1차 선택으로 둔다. 단, 본 게이트에서 영구 확정으로 표기하지 않는다.

---

## 9. Threshold Proposal Policy

### 9.1 형식 (profile 파일)

```
ThresholdProposal:
  value: number | integer | string
  status: "proposal"             # 본 게이트에서는 고정값
  rationale: string              # 관찰 근거 또는 초기 추측 출처
  proposal_source: string        # 누가 어떤 맥락에서 제안했는가
```

### 9.2 본 게이트의 proposal 4종

| 이름 | 값 | 출처 |
|---|---|---|
| broad_item_concentration_pct | 60 | D-3 단일 item 흡수 패턴 관찰 (확정 검증 없음) |
| soft_alert_max_delta_pct | 5 | 초기 임계값 (전수 검증 없음) |
| hard_alert_min_delta_pct | 10 | 초기 임계값 (전수 검증 없음) |
| multi_word_min_length | 2 | D-3 split 정책 기반 (전수 검증 없음) |

위 4개 값은 모두 `status: proposal`이다. 본 게이트에서 확정으로 사용해서는 안 된다.

---

## 10. JSON Schema 한계와 Validator Gate 필요성

본 게이트의 JSON Schema(`rule_schema_v0.1_draft.schema.json`)는 형식 검증만 책임진다. 다음 항목은 JSON Schema 기본 검증으로는 보장되지 않는다.

| # | 한계 항목 | 필요한 cross-check |
|---|---|---|
| L1 | Rule.id uniqueness | 인스턴스 배열 전수 순회로 중복 ID 탐지 |
| L2 | PredicateCall.predicate_id ↔ profile.predicate_library 카탈로그 일치 | 카탈로그 외 predicate_id 거부 |
| L3 | PredicateCall.args ↔ 해당 predicate의 args_schema | predicate별 args_schema로 args 재검증 |
| L4 | Verdict.category ↔ profile.domain_taxonomy.category_enum 일치 | 카탈로그 외 category 거부 |
| L5 | AutomatedCheckCall.function_id ↔ profile.check_library 카탈로그 일치 | 카탈로그 외 function_id 거부 |
| L6 | AutomatedCheckCall.parameters ↔ 해당 check의 parameters_schema | check별 parameters_schema로 재검증 |
| L7 | Rule.priority_group과 Verdict.severity 조합 정합성 | 도메인 규약에 따른 조합 화이트리스트 (현재 미정의) |
| L8 | RuleMetadata.deprecation_signal과 verification_status 일관성 | well_tested 상태에서 deprecation_signal 채워졌는지 등 정책 검사 |

위 8개 한계는 후속 **Schema Validator Gate**에서 구현한다. 본 게이트의 schema 파일은 한계 항목을 인지한 상태로 발행한다.

---

## 11. 10개 질문 답변 매핑

| # | 질문 | 답변 위치 |
|---|---|---|
| 1 | 무엇이 하나의 rule인가 | §2 Rule Contract (9필드) |
| 2 | rule id·name 고유성 보장 | §2.1 id 패턴 + §10 L1 validator gate 의무 |
| 3 | criteria 표현 언어 | §4 Predicate Contract. core 인터페이스 + profile 카탈로그 |
| 4 | verdict 구조 | §3 Verdict Contract (4필드) |
| 5 | 다중 matching 보고 | §7 Multi-Match Report Contract |
| 6 | priority와 severity 분리 | §1.4 priority=Rule 속성, severity=Verdict 속성 |
| 7 | automated_check와 human_review 분리 | §5·§6 별도 contract |
| 8 | schema version과 migration | §12 schema_metadata.schema_version + migration_paths |
| 9 | core vs profile 경계 | §1.2·§1.3 schema 파일 내부 core/profile_contract, profile 파일 분리 |
| 10 | threshold proposal 위치 | §9 profile 파일의 threshold_proposals |

---

## 12. Schema Versioning

```
schema_metadata:
  schema_version: "0.1-draft"
  status: "draft"
  compatible_with_instance_versions: ["0.1.x"]
  migration_paths:
    - from_version: "0.2-instance"
      migration_notes: "v0.2 인스턴스(policy_change_rules.json) → v0.1-draft schema 형식 변환은 별도 migration gate의 책임. 본 게이트에서는 실행하지 않음."
      breaking_changes:
        - "rules 배열 항목이 verdict_1st 단일 문자열 대신 4필드 verdict 객체"
        - "criteria 객체가 predicate_id + args 배열 형식"
        - "priority가 문자열 수식 대신 priority_group enum"
```

### 12.1 schema_version 명명 정책

- 본 게이트는 schema 자체의 1차 정돈이므로 `0.1-draft`로 시작한다.
- 원천 파일에 표기된 `0.3-draft`는 rules 인스턴스 버전과 혼동 가능성이 있어 사용하지 않는다.
- v0.2 → v0.3 인스턴스 마이그레이션 의도는 본 schema 파일의 버전과 무관하다.

---

## 13. Profile 파일 구조

`ee_agent_rule_profile_v0.1_draft.json`의 root 키:

| 키 | 내용 |
|---|---|
| profile_metadata | profile_version·domain_id·status·source_notes |
| domain_taxonomy | status_values·status_movement_notes·category_enum |
| predicate_library | predicate 카탈로그 배열 (1차 7종) |
| check_library | automated check 카탈로그 배열 (1차 10종) |
| threshold_proposals | threshold 값 4종, 모두 status: proposal |
| aggregation_policy | method 선택 (highest_priority_wins 1차) |
| claim_boundary | profile 내용의 검증 수준 명시 (직접 정의 / 초안 / proposal) |

### 13.1 predicate_library 카탈로그 (1차 초안)

다음 7종은 `policy_change_rules.json` v0.2 인스턴스에서 역추출한 초안이다. 실측 검증은 없다.

| predicate_id | 의미 (요약) |
|---|---|
| status_movement | from→to status 이동 건수 검사 |
| delta_status_count | 특정 status 증감 방향·최소 변동량 |
| item_concentration_pct | 한 item 집중도 비율 |
| hash_changed | questions·tool·policy hash 변경 여부 |
| abs_delta_pct | 절대 변동률 범위 |
| zero_hit_items | 0 hit item 수 임계 |
| item_changed | 같은 entry의 매칭 item 변경 여부 |

### 13.2 check_library 카탈로그 (1차 초안)

다음 10종도 v0.2 인스턴스에서 역추출한 초안이다.

| function_id |
|---|
| multi_word_keyword_recovery_test |
| list_competing_items_per_pid |
| list_before_after_items_per_pid |
| compare_keyword_lists_for_new_broad |
| diff_input_data_hash |
| diff_tool_version_metadata |
| list_top_matching_keywords_for_item |
| search_synonyms_in_corpus |
| trace_responsible_keyword |
| verify_no_keyword_overreach |

---

## 14. 본 게이트에서 확정된 것과 미확정인 것

### 14.1 확정 사항

- schema first 원칙
- schema 파일·profile 파일 2개 파일 분리
- schema 파일 내부 core / profile_contract 경계
- priority_group 4단계 (critical·major·standard·minor)
- severity 5종 (IMPROVEMENT·SOFT_ALERT·INVESTIGATE·SUSPECT·HARD_ALERT)
- auto_action 4종 (log_only·trigger_check·human_review·block)
- aggregation_method 3종 enum
- Verdict 4필드 (severity·category·auto_action·rationale)
- Rule 9필드 (id·name·scope·priority_group·metadata·criteria·verdict·automated_check·human_review_guidelines + 선택 examples)
- 다중 매칭 모두 보고 + final_action을 aggregation으로 분리
- threshold는 profile 파일에서 `status: proposal`로 표기

### 14.2 미확정 사항

- threshold 4종 확정값
- v0.2 인스턴스(`policy_change_rules.json` 12 규칙) → v0.1-draft schema 형식 변환
- JSON Schema cross-check 8종 (§10 L1~L8) 구현
- governance 적용 도구 구현
- D-4 automation 구조 확정
- aggregation_method를 highest_priority_wins로 영구 확정 (현재는 ee-agent profile의 1차 선택)
- domain_agnostic=true 규칙의 core 자동 승격 정책

---

## 15. Claim Boundary

| 단계 | 내용 |
|---|---|
| (a) 직접 정의 | Rule 9필드, Verdict 4필드, core enum 5+4+3+2종, predicate·check 인터페이스 형식, multi-match report shape |
| (b) 초안 산출 | predicate_library 7종, check_library 10종 — v0.2 규칙에서 역추출. 실측 검증 없음 |
| (c) Proposal | threshold 4값 — D-3 관찰 또는 초기 추측 |

---

## 16. 후속 게이트 후보

| 후보 | 단일 목적 |
|---|---|
| 후보 A | Schema Validator Gate — §10의 L1~L8 cross-check 구현 |
| 후보 B | Instance Migration Gate — v0.2 12 규칙을 v0.1-draft schema 형식으로 변환 |
| 후보 C | Threshold 확정 Gate — proposal → confirmed |
| 후보 D | Schema 실측 적용 Gate — D-3·D-4 실제 변동에 schema 적용 검증 |
| 후보 E | Core 재사용 Gate — react-confidence·추천시스템 등 다른 verify-agent 프로젝트에 core 시범 적용 |

각 후보는 독립이다. 순서·병행은 사용자 결정 영역이다.

---

## 17. 최종 상태

`READY_FOR_RULE_SCHEMA_REVIEW_GATE`
