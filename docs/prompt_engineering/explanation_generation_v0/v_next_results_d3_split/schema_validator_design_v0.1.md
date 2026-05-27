# Schema Validator Design — v0.1 Draft

| 항목 | 값 |
|---|---|
| 상태 | DESIGN_ONLY |
| 작성일 | 2026-05-27 |
| 본 문서 단계 | Schema Validator Design Gate 산출물 |
| 후속 단계 후보 | READY_FOR_SCHEMA_VALIDATOR_DESIGN_REVIEW_GATE |
| 적용 대상 schema | `rule_schema_v0.1_draft.schema.json` |
| 적용 대상 profile | `ee_agent_rule_profile_v0.1_draft.json` |
| validator 구현 여부 | 본 문서 단계 없음 (별도 implementation gate 책임) |

---

## 0. 본 게이트의 단일 목적과 범위

`known_limits` L1~L8을 기준으로 validator가 수행할 검사 범위·판정 등급·입출력 명세를 설계한다. 본 문서는 **검사 설계 문서**이며, validator 구현·실행은 본 게이트에서 진행하지 않는다.

### 0.1 본 게이트에서 변경하지 않는 것

- validator 코드를 작성하지 않는다.
- `scripts/` 어떤 파일도 수정하지 않는다.
- `rule_schema_v0.1_draft.schema.json`·`ee_agent_rule_profile_v0.1_draft.json`을 수정하지 않는다.
- 기존 `policy_change_rules.json`을 수정하지 않는다.
- v0.2 → v0.1-draft 마이그레이션을 실행하지 않는다.
- governance verdict를 적용하지 않는다.
- threshold를 확정하지 않는다.
- D-4 automation을 실행하지 않는다.
- commit·push를 진행하지 않는다.

### 0.2 본 게이트가 정의하는 것

- validator의 입력 파일 4종
- validator의 출력 파일 5섹션
- L1~L8 각 검사의 입력·통과 기준·실패 시 등급
- 기본 판정 등급 매트릭스
- L7·L8 정책 미정의 처리 방식
- validator가 절대 수행하지 말아야 할 동작 7종
- 후속 implementation gate의 성공 판정 초안

---

## 1. Validator 입력 파일 명세

validator는 다음 입력 4종을 받는다. 각 파일은 read-only로 처리한다.

| # | 입력 파일 | 필수 여부 | 역할 | 본 게이트 단계에서의 위치 |
|---|---|---|---|---|
| I1 | `rule_schema_v0.1_draft.schema.json` | 필수 | 형식 contract. domain-neutral. | `docs/prompt_engineering/explanation_generation_v0/v_next_results_d3_split/` |
| I2 | `ee_agent_rule_profile_v0.1_draft.json` | 필수 | ee-agent 카탈로그·threshold proposal. | 위와 동일 |
| I3 | future rules instance file | 선택 | v0.1-draft schema에 정합하는 rule 인스턴스 배열. 본 게이트 단계에서는 부재. instance migration gate 산출물. | 미정 (별도 gate에서 결정) |
| I4 | optional change report file | 선택 | `ChangeReport` 형식의 측정 결과. governance 단계 입력. | 미정 (별도 gate에서 결정) |

### 1.1 입력 호환성 매트릭스

| 입력 조합 | validator 동작 |
|---|---|
| I1 only | schema 자체 형식 검증만 가능 (`$schema` draft-07 정합성, definitions 구조 일관성 등) |
| I1 + I2 | L2·L4·L5의 카탈로그 cross-check 가능. L1·L3·L6은 인스턴스가 없으므로 skip. |
| I1 + I2 + I3 | L1·L3·L6 포함 전체 L1~L6 검사 가능. L7·L8은 정책 미정의로 report-only 또는 warning. |
| I1 + I2 + I3 + I4 | 위 + change report shape 검증 (`change_report_contract` 정합성). |

### 1.2 입력 파싱 정책

- JSON parse 실패 = `error` (즉시 종료)
- 파일 부재 (필수 파일) = `error` (즉시 종료)
- 파일 부재 (선택 파일) = skip + 출력 `validation_summary.skipped` 항목에 기록
- 입력 파일 인코딩은 UTF-8로 고정한다.

---

## 2. Validator 출력 파일 명세

validator는 단일 JSON 출력 파일을 생성한다. 본 게이트는 파일 경로·파일명을 확정하지 않는다 (implementation gate 결정).

### 2.1 출력 root 구조

```
validator_output:
  validation_summary
  errors
  warnings
  report_only
  unresolved_policy_questions
  metadata
```

### 2.2 각 섹션 명세

| 섹션 | 역할 | 기록 항목 |
|---|---|---|
| validation_summary | 전체 결과 요약 | total_checks, passed, failed, warned, report_only, skipped, exit_decision |
| errors | hard fail 항목 배열 | check_id(L1~L6), input_locator, expected, actual, severity="error" |
| warnings | soft fail 항목 배열 | check_id, input_locator, observation, severity="warning" |
| report_only | 기록 전용 항목 배열 | check_id(L7·L8), input_locator, observation, severity="report_only" |
| unresolved_policy_questions | L7·L8 정책 미정의 결정 대기 항목 | check_id, decision_needed, suggested_options, context |
| metadata | 실행 컨텍스트 | schema_version, profile_version, input_file_hashes, validator_version, run_timestamp |

### 2.3 exit_decision 정책

| validation_summary.exit_decision | 의미 |
|---|---|
| pass | errors=0 + warnings=0 |
| pass_with_warnings | errors=0, warnings≥1 |
| pass_with_report_only | errors=0, warnings=0, report_only≥1 |
| fail | errors≥1 |

validator의 process exit code 매핑은 implementation gate에서 결정한다. 본 게이트는 결과 의미만 정의한다.

### 2.4 출력 형식 원칙

- 결과는 단일 JSON 객체로 발행한다.
- 결과 파일에 input 파일 자체를 inline 포함하지 않는다 (input_file_hashes로 참조).
- 사람이 읽는 보고용 텍스트 출력은 선택 (별도 reporter 도구가 JSON 출력을 가공). validator 자체는 JSON만 책임.

---

## 3. L1~L8 검사 명세

각 L별로 다음 구조로 정의한다.

```
검사 ID
  설명
  입력
  통과 기준
  실패 시 등급
  실패 시 보고 형식
  본 게이트 단계의 적용 가능성
```

### 3.1 L1 Rule.id uniqueness

| 항목 | 내용 |
|---|---|
| 설명 | rules 배열 내 `Rule.id`가 중복되지 않는지 검사 |
| 입력 | I3 (rules instance file) |
| 통과 기준 | rules[*].id 집합 크기 = rules 배열 길이 |
| 실패 시 등급 | error |
| 실패 시 보고 | check_id="L1", duplicate_ids=[...], occurrences=[{rule_index, rule_id, location}] |
| 본 게이트 단계 적용 가능성 | I3 부재로 skip 예정 |

### 3.2 L2 PredicateCall.predicate_id catalog 존재 여부

| 항목 | 내용 |
|---|---|
| 설명 | 모든 `Rule.criteria.predicates[*].predicate_id`가 profile.predicate_library의 `predicate_id` 집합에 포함되는지 검사 |
| 입력 | I1 + I2 + I3 |
| 통과 기준 | rules에 등장한 모든 predicate_id ⊆ profile.predicate_library[*].predicate_id |
| 실패 시 등급 | error |
| 실패 시 보고 | check_id="L2", unknown_predicate_id, rule_id, criteria_index, suggested_known_ids |
| 본 게이트 단계 적용 가능성 | I3 부재로 skip 예정. 단, profile.predicate_library 카탈로그 자체의 자체 일관성 검사(중복 predicate_id 등)는 사전 단계에서 수행 가능 |

### 3.3 L3 PredicateCall.args args_schema 준수

| 항목 | 내용 |
|---|---|
| 설명 | 각 `PredicateCall.args`가 해당 predicate의 `args_schema`를 만족하는지 검사 |
| 입력 | I1 + I2 + I3 |
| 통과 기준 | 모든 PredicateCall.args가 profile.predicate_library에서 매칭된 predicate의 args_schema 검증 통과 |
| 실패 시 등급 | error |
| 실패 시 보고 | check_id="L3", predicate_id, rule_id, criteria_index, args_received, args_schema, validation_errors |
| 본 게이트 단계 적용 가능성 | I3 부재로 skip 예정 |

### 3.4 L4 Verdict.category profile enum 포함 여부

| 항목 | 내용 |
|---|---|
| 설명 | 모든 `Rule.verdict.category` 값과 `MatchedRule.verdict.category` 값(I4 입력 시)이 `profile.domain_taxonomy.category_enum`에 포함되는지 검사 |
| 입력 | I1 + I2 + I3 (+ I4 선택) |
| 통과 기준 | 등장한 모든 category 값 ⊆ profile.domain_taxonomy.category_enum |
| 실패 시 등급 | error |
| 실패 시 보고 | check_id="L4", unknown_category, rule_id 또는 change_id, occurrence_path, suggested_known_categories |
| 본 게이트 단계 적용 가능성 | I3 부재로 skip 예정. profile.category_enum 자체의 자체 일관성(중복 값 등)은 사전 단계에서 수행 가능 |

### 3.5 L5 AutomatedCheckCall.function_id catalog 존재 여부

| 항목 | 내용 |
|---|---|
| 설명 | 모든 `Rule.automated_check.function_id`가 `profile.check_library`의 `function_id` 집합에 포함되는지 검사 |
| 입력 | I1 + I2 + I3 |
| 통과 기준 | rules에 등장한 모든 function_id ⊆ profile.check_library[*].function_id |
| 실패 시 등급 | error |
| 실패 시 보고 | check_id="L5", unknown_function_id, rule_id, suggested_known_function_ids |
| 본 게이트 단계 적용 가능성 | I3 부재로 skip 예정. profile.check_library 자체의 자체 일관성 검사는 사전 단계에서 수행 가능 |

### 3.6 L6 AutomatedCheckCall.parameters parameters_schema 준수

| 항목 | 내용 |
|---|---|
| 설명 | 각 `AutomatedCheckCall.parameters`가 해당 check의 `parameters_schema`를 만족하는지 검사 |
| 입력 | I1 + I2 + I3 |
| 통과 기준 | 모든 AutomatedCheckCall.parameters가 매칭된 check의 parameters_schema 검증 통과 |
| 실패 시 등급 | error |
| 실패 시 보고 | check_id="L6", function_id, rule_id, parameters_received, parameters_schema, validation_errors |
| 본 게이트 단계 적용 가능성 | I3 부재로 skip 예정 |

### 3.7 L7 Rule.priority_group ↔ Verdict.severity 조합 정합성

| 항목 | 내용 |
|---|---|
| 설명 | `Rule.priority_group`(4종)과 `Rule.verdict.severity`(5종) 조합이 도메인 규약에 따라 허용되는지 검사 |
| 입력 | I1 + I2 + I3 |
| 통과 기준 | 도메인 규약 미정의. v0.1에서는 통과 조건을 강제하지 않는다 |
| 실패 시 등급 | **report_only** (v0.1에서는 hard fail 금지) |
| 실패 시 보고 | check_id="L7", rule_id, priority_group, severity, combination_observed, policy_decision_status="undefined" |
| 본 게이트 단계 적용 가능성 | I3 부재로 skip. 정책 미정의 항목은 `unresolved_policy_questions`에 기록 |

### 3.8 L8 RuleMetadata.deprecation_signal ↔ verification_status 일관성

| 항목 | 내용 |
|---|---|
| 설명 | `verification_status`가 `well_tested`인 경우 `deprecation_signal`이 명시되었는지 등의 일관성 정책 검사 |
| 입력 | I1 + I2 + I3 |
| 통과 기준 | 도메인 규약 미정의. v0.1에서는 통과 조건을 강제하지 않는다 |
| 실패 시 등급 | **report_only** (v0.1에서는 hard fail 금지) |
| 실패 시 보고 | check_id="L8", rule_id, verification_status, deprecation_signal_present, observation, policy_decision_status="undefined" |
| 본 게이트 단계 적용 가능성 | I3 부재로 skip. 정책 미정의 항목은 `unresolved_policy_questions`에 기록 |

---

## 4. 기본 판정 등급 매트릭스

| 검사 ID | 등급 | exit_decision 영향 |
|---|---|---|
| L1 Rule.id uniqueness | error | fail |
| L2 predicate_id catalog 존재 | error | fail |
| L3 PredicateCall.args 정합 | error | fail |
| L4 Verdict.category profile enum 포함 | error | fail |
| L5 function_id catalog 존재 | error | fail |
| L6 AutomatedCheckCall.parameters 정합 | error | fail |
| L7 priority_group ↔ severity 조합 | report_only | pass_with_report_only |
| L8 deprecation_signal ↔ verification_status | report_only | pass_with_report_only |

### 4.1 등급 정의

| 등급 | 의미 | 후속 처리 |
|---|---|---|
| error | hard fail. 인스턴스가 schema·profile contract를 위반함 | implementation·migration·governance 진행 금지 |
| warning | soft fail. 형식은 통과하나 도메인 의도와 불일치 의심 | 사람 검토 권장. 자동 차단은 없음. v0.1에서는 명시적 검사 없음 (필요 시 후속 정책 결정 후 도입) |
| report_only | 정책 미정의 상태에서 관찰 기록만 수행 | unresolved_policy_questions에 기록 후 policy decision gate로 인계 |
| skip | 입력 부재로 검사 미수행 | validation_summary.skipped에 기록 |
| pass | 통과 | 추가 처리 없음 |

### 4.2 v0.1에서 warning 등급을 명시 검사로 도입하지 않는 이유

본 단계에서는 warning 트리거 정책이 정의되지 않았다. error(=형식 위반)와 report_only(=정책 미정의 관찰)만 명시한다. warning은 v0.2 이후 도메인 정책 결정과 함께 도입 가능 영역으로 남긴다.

---

## 5. L7·L8 정책 미정의 처리

L7·L8은 본 단계에서 도메인 규약이 정의되어 있지 않다. validator v0.1은 hard fail을 강제하지 않는다.

### 5.1 처리 절차

1. L7·L8 패턴이 관찰되면 `report_only` 섹션에 기록한다.
2. 동일 패턴을 `unresolved_policy_questions` 섹션에 별도 항목으로 누적한다.
3. validator process는 실패로 종료하지 않는다 (`exit_decision = pass_with_report_only`).

### 5.2 unresolved_policy_questions 항목 형식

```
unresolved_policy_questions[i]:
  check_id: "L7" | "L8"
  decision_needed: string  # 어떤 정책 결정이 필요한가
  suggested_options: array of string
  context: object          # 관찰된 인스턴스 위치·값
```

### 5.3 L7 예시 (관찰 시 기록될 형식)

```
{
  "check_id": "L7",
  "decision_needed": "priority_group=critical과 severity=IMPROVEMENT 조합 허용 여부",
  "suggested_options": [
    "허용 — 잘못된 IMPROVEMENT 신호가 critical priority로 분류 가능",
    "거부 — priority=critical은 IMPROVEMENT 외 severity만 허용",
    "도메인별 정책 — profile에 priority_group↔severity 허용 매트릭스 별도 정의"
  ],
  "context": {
    "rule_id": "...",
    "priority_group": "critical",
    "severity": "IMPROVEMENT"
  }
}
```

### 5.4 L8 예시 (관찰 시 기록될 형식)

```
{
  "check_id": "L8",
  "decision_needed": "verification_status=well_tested에서 deprecation_signal 필수 여부",
  "suggested_options": [
    "필수 — well_tested는 폐기 조건 명시 강제",
    "선택 — deprecation_signal은 자유 입력",
    "도메인별 정책 — profile에 verification_status별 metadata 필수 필드 별도 정의"
  ],
  "context": {
    "rule_id": "...",
    "verification_status": "well_tested",
    "deprecation_signal_present": false
  }
}
```

### 5.5 정책 결정 후 처리

- 정책이 확정되면 `unresolved_policy_questions` 해당 항목을 제거한다.
- L7·L8 등급을 `error`·`warning`·`report_only` 중 하나로 재배정한다.
- schema·profile에 정책 enforcement 메타를 반영하는 것은 본 validator design 게이트의 범위가 아니다. 별도 schema revision gate의 책임이다.

---

## 6. Validator가 절대 수행하지 말아야 할 동작

validator는 input 파일을 read-only로 검사한다. 다음 동작은 금지된다.

| # | 금지 동작 |
|---|---|
| F1 | threshold proposal 값을 confirmed로 변경 |
| F2 | v0.2 rules → v0.1-draft schema 형식으로 migration 자동 수행 |
| F3 | governance verdict를 인스턴스에 자동 적용 |
| F4 | rules instance 파일을 수정 |
| F5 | profile 파일을 수정 |
| F6 | schema 파일을 수정 |
| F7 | D-4 automation 또는 인접 input·generation·audit 도구 실행 |

위 7종은 후속 implementation gate의 성공 판정 조건에 포함된다.

---

## 7. Validator 구현 Gate 성공 판정 초안

validator 구현 gate는 본 design 문서가 review·승인된 이후 진입 가능하다. 다음은 그 게이트의 성공 판정 초안이다. 본 게이트에서 확정하지 않는다.

| 항목 | 초안 |
|---|---|
| 단일 목적 | 본 design 문서의 L1~L8 검사를 read-only로 수행하는 validator 작성 |
| 변경 가능 영역 | `scripts/` 하위 신규 validator 스크립트 1~N개 (구현 gate에서 명시) |
| 절대 금지 | F1~F7 모든 동작, 입력 파일 수정, 구현 외 design 변경, threshold 확정 |
| 성공 판정 | (a) input 파일 read-only / (b) JSON 출력 단일 파일 발행 / (c) L1~L6 error 등급 정상 작동 / (d) L7·L8 report_only 정상 작동 / (e) exit_decision 4종 정확 분기 / (f) 입력 파일 hash 재계산 가능 |
| 실패 시 동작 | 실패 처리 후 파일 수정 없이 종료 (input 파일·tracked 파일 어떤 것도 변경하지 않음) |
| 실패 시 보고 | validator 자체의 실행 실패와 검사 결과 fail은 분리. 전자는 stderr·exit code, 후자는 결과 JSON의 `exit_decision = fail`로 표기 |

### 7.1 validator 구현 gate 진입 전 필요한 결정 항목

다음은 implementation gate 진입 전에 design review gate 또는 별도 단계에서 결정해야 할 항목이다.

- 출력 JSON 파일의 경로·파일명
- exit code 매핑 (예: pass=0, pass_with_warnings=0, pass_with_report_only=0, fail=2)
- validator 자체의 언어·런타임 (Python·Node 등) — 본 design 문서에서는 명시하지 않음
- 결과 reporter(사람이 읽는 보고용 텍스트 출력)를 별도 도구로 분리할지 통합할지

---

## 8. Profile 파일에 대한 사전 자체 일관성 검사 (선택 영역)

I3 인스턴스 파일이 부재한 본 게이트 단계에서도 validator는 다음 사전 검사를 수행 가능하다. 본 design은 선택 영역으로 둔다.

| 사전 검사 ID | 설명 | 등급 |
|---|---|---|
| P1 | profile.predicate_library 내 predicate_id 중복 여부 | error |
| P2 | profile.check_library 내 function_id 중복 여부 | error |
| P3 | profile.domain_taxonomy.category_enum 내 중복 여부 | error |
| P4 | profile.threshold_proposals 각 항목의 `status` 값이 schema의 `ThresholdProposal.status` const("proposal")과 일치 | error |
| P5 | profile.aggregation_policy.method 값이 core.aggregation_method_enum 중 1 | error |
| P6 | profile root 키가 schema.profile_contract.required_root_keys 6종을 모두 포함 | error |

P1~P6은 validator implementation gate에서 도입할지 본 design 문서 후속 revision에서 결정한다.

---

## 9. Claim Boundary

| 단계 | 본 게이트가 주장 가능한 것 |
|---|---|
| (a) 직접 정의 | validator 입력 4종, 출력 5섹션, L1~L8 검사 구조, 기본 판정 등급 매트릭스, L7·L8 정책 미정의 처리 절차, validator 금지 동작 7종 |
| (b) 초안 권장 | implementation gate 성공 판정 7항, 출력 형식 원칙, 사전 자체 일관성 검사 P1~P6 |
| (c) 미확정 | warning 등급 트리거 정책, exit code 매핑, 출력 파일 경로·파일명, validator 언어·런타임, L7·L8 정책 결정 |

본 게이트는 (a)에 대해서만 design 차원 정합성을 주장한다. (b)·(c)는 후속 review·implementation gate의 판단을 전제로 한다.

---

## 10. 본 게이트에서 확정된 것과 미확정인 것

### 10.1 확정 사항

- validator 입력 4종 (I1·I2·I3·I4)
- validator 출력 5섹션 (validation_summary·errors·warnings·report_only·unresolved_policy_questions) + metadata
- L1~L6 기본 등급 = error
- L7·L8 기본 등급 = report_only (hard fail 금지)
- exit_decision 4종 (pass·pass_with_warnings·pass_with_report_only·fail)
- validator 금지 동작 7종 (F1~F7)
- unresolved_policy_questions 항목 형식

### 10.2 미확정 사항

- warning 등급 명시 검사 항목
- exit code 매핑
- 출력 파일 경로·파일명
- validator 언어·런타임
- 사전 자체 일관성 검사 P1~P6 도입 여부
- L7·L8 정책 (별도 policy decision gate)
- reporter 도구 분리 여부

---

## 11. 후속 게이트 후보

본 design 문서가 review·승인되면 다음 게이트가 자연 후속이다.

| 후보 | 단일 목적 |
|---|---|
| 후보 V1: Schema Validator Design Review Gate | 본 design 문서가 implementation gate 진입 가능한 설계인지 read-only review |
| 후보 V2: Schema Validator Implementation Gate | 본 design 문서를 기준으로 validator 스크립트 작성 |
| 후보 V3: Schema Validator Run Gate | 작성된 validator를 I1·I2에 1차 실행하여 사전 자체 일관성 결과 수집 |
| 후보 P1: L7·L8 Policy Decision Gate | unresolved_policy_questions의 정책 결정 |
| 후보 R1: Instance Migration Gate (design §16 후보 B) | I3 산출. validator 전체 검사 실행 가능 |

각 후보는 독립이다. 본 design 문서는 후보 V1·V2 진입의 입력 자료다.

---

## 12. 최종 상태

`READY_FOR_SCHEMA_VALIDATOR_DESIGN_REVIEW_GATE`
