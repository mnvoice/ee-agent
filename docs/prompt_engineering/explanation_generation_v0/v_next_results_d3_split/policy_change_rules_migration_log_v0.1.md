# Policy Change Rules Migration Log — v0.2 to v0.1-draft

| 항목 | 값 |
|---|---|
| 상태 | MIGRATION_LOG_ONLY |
| 작성일 | 2026-05-28 |
| 본 문서 단계 | Instance Migration Gate 산출물 |
| 후속 단계 후보 | READY_FOR_INSTANCE_MIGRATION_REVIEW_GATE |
| 원천 v0.2 | `/private/tmp/ee_agent_rule_schema_sources/policy_change_rules.json` |
| 원천 sha256 | `0faa8e2f421570d48c774a9f144a604bcd67cdc0921db685fd3169d32c64a2af` |
| 대상 v0.1 instance | `policy_change_rules_v0.1_draft_instance.json` |
| validator 실행 결과 | `policy_change_rules_validation_report_v0.1.json` |

---

## 1. Migration 범위

| 항목 | 값 |
|---|---|
| 변환 대상 rule count | 12 (R1~R12) |
| 변환 완료 rule count | 12 |
| 누락 rule | 0 |
| validator L1~L6 error | 0 |
| validator L7 report_only | 12 (rule당 1, priority_group+severity 조합 정책 미정의) |
| validator L8 report_only | 0 (well_tested + deprecation_signal 부재 조건 미발현) |
| unresolved_policy_questions | 1 (L7 정책 미정의) |

---

## 2. verdict_1st → Verdict 4필드 매핑 기준

원천 v0.2의 verdict_1st 단일 문자열을 v0.1-draft `Verdict` 4필드(severity / category / auto_action / rationale)로 분해.

| R | verdict_1st | severity | category | auto_action |
|---|---|---|---|---|
| R1 | INVESTIGATE_RECOVERABILITY | INVESTIGATE | RECOVERABILITY | trigger_check |
| R2 | REVIEW_AMBIGUITY | INVESTIGATE | AMBIGUITY | human_review |
| R3 | ROUTING_CHANGE | SOFT_ALERT | ROUTING | log_only |
| R4 | SUSPECT_POLICY_RELAXATION | SUSPECT | POLICY_RELAXATION | human_review |
| R5 | INVESTIGATE_DATA_OR_TOOL_DRIFT | INVESTIGATE | DATA_OR_TOOL_DRIFT | trigger_check |
| R6 | SUSPECT_BROAD_KEYWORD | SUSPECT | BROAD_KEYWORD | human_review |
| R7 | SOFT_ALERT_MONITOR | SOFT_ALERT | DATA_OR_TOOL_DRIFT (임시) | log_only |
| R8 | HARD_ALERT_BLOCK | HARD_ALERT | DATA_OR_TOOL_DRIFT (임시) | block |
| R9 | DATA_DEBT_OR_KEYWORD_FAILURE | INVESTIGATE | DATA_DEBT | trigger_check |
| R10 | POTENTIAL_IMPROVEMENT | IMPROVEMENT | AMBIGUITY | log_only |
| R11 | POTENTIAL_IMPROVEMENT | IMPROVEMENT | RECOVERABILITY | log_only |
| R12 | SEPARATE_TOOL_CHANGE_FROM_POLICY | INVESTIGATE | TOOL_CHANGE | trigger_check |

### 2.1 R10·R11의 verdict_1st 동일·category 분리

R10·R11 모두 v0.2에서 `POTENTIAL_IMPROVEMENT`로 동일 verdict_1st를 사용. v0.1-draft 분해 시 category를 의도에 따라 분리:
- R10 (NEEDS_REVIEW → CLEAN): ambiguity 해소 → AMBIGUITY
- R11 (GAP → CLEAN/NEEDS_REVIEW): 회수 → RECOVERABILITY

### 2.2 R7·R8 category 매핑 unresolved

R7 (Soft alert, 변동 ≤ 5%)과 R8 (Hard alert, 변동 ≥ 10%)은 "변동 magnitude" 기준 rule이다. profile.category_enum 9종은 모두 "변동 유형" 카테고리(RECOVERABILITY·AMBIGUITY·ROUTING·POLICY_RELAXATION·DATA_OR_TOOL_DRIFT·BROAD_KEYWORD·DATA_DEBT·TOOL_CHANGE·SUBJECT_CHANGE). magnitude-based rule을 직접 표현할 카테고리 부재.

본 게이트는 두 rule의 category를 임시로 `DATA_OR_TOOL_DRIFT`로 매핑:
- 이유: magnitude-based rule이 정책 무변동에서도 발생 가능하므로 drift 카테고리가 가장 보편적.
- 임시 표기. profile.category_enum 보강 또는 magnitude-only 카테고리(`SOFT_ALERT_VOLUME`·`HARD_ALERT_VOLUME` 등) 추가 후 재배정 필요.
- 두 rule의 `metadata.deprecation_signal`에 매핑 임시성 명시.

---

## 3. criteria → PredicateCall 매핑 기준

원천 ad-hoc 형식을 profile.predicate_library 7종 카탈로그로 변환.

| R | 원천 criteria | predicates 매핑 | combinator |
|---|---|---|---|
| R1 | `movement: {from: "CLEAN", to: "GAP"}, min_count: 1` | `status_movement{from, to, min_count}` | AND |
| R2 | `movement: {from: "CLEAN", to: "NEEDS_REVIEW"}, min_count: 1` | `status_movement` | AND |
| R3 | `movement: {from_status: "CLEAN", to_status: "CLEAN", item_changed: true}` | `status_movement` + `item_changed{same_status: true}` | AND |
| R4 | `delta_clean: "positive", min_delta_count: 1` | `delta_status_count{status: "CLEAN", direction, min_count}` | AND |
| R5 | `delta_gap: "positive", delta_clean: 0, delta_review: 0` | `delta_status_count` × 3 (GAP positive + CLEAN zero + NEEDS_REVIEW zero) | AND |
| R6 | `item_concentration_pct_min: 60` | `item_concentration_pct{min_pct: 60}` | AND |
| R7 | `abs_delta_pct_max: 5` | `abs_delta_pct{max: 5}` | AND |
| R8 | `abs_delta_pct_min: 10` | `abs_delta_pct{min: 10}` | AND |
| R9 | `zero_hit_items_detected: true` | `zero_hit_items{at_least: 1}` | AND |
| R10 | `movement: {from: "NEEDS_REVIEW", to: "CLEAN"}, min_count: 1` | `status_movement` | AND |
| R11 | `movement: {from: "GAP", to: ["CLEAN", "NEEDS_REVIEW"]}, min_count: 1` | `status_movement` (to는 array) | AND |
| R12 | `tool_hash_changed: true` | `hash_changed{target: "tool"}` | AND |

### 3.1 R3 분해 사유

원천 R3은 `from_status`·`to_status`·`item_changed`를 한 객체에 포함. predicate_library는 `status_movement`(from/to)와 `item_changed`(same_status) 두 predicate로 분리되어 있어 AND 결합으로 표현.

### 3.2 R5 3-predicate AND 사유

원천 R5는 GAP 증가 + CLEAN 무변동 + REVIEW 무변동 3 조건의 AND. `delta_status_count`의 `direction` enum은 positive·negative·zero 3종이므로 zero direction으로 무변동 표현 가능.

### 3.3 R11 to-array 처리

원천 R11은 `to: ["CLEAN", "NEEDS_REVIEW"]` array 값. predicate `status_movement`의 args_schema는 `to: string | array<string>` 둘 다 수용. validator L3 PASS.

---

## 4. automated_check → AutomatedCheckCall 매핑 기준

원천 string을 profile.check_library 10종 카탈로그로 변환.

| R | 원천 automated_check | function_id | parameters | nuance 손실 |
|---|---|---|---|---|
| R1 | `multi_word_keyword_recovery_test` | 동일 | `{}` (max_words optional) | 없음 |
| R2 | `list_competing_items_per_pid` | 동일 | `{}` | 없음 |
| R3 | `list_before_after_items_per_pid` | 동일 | `{}` | 없음 |
| R4 | `compare_keyword_lists_for_new_broad` | 동일 | `{}` | 없음 |
| R5 | `diff_input_data_hash_and_tool_hash` | `diff_input_data_hash` | `{}` | **tool_hash 부분 분리, R12와의 boundary 의존** |
| R6 | `list_top_matching_keywords_for_item` | 동일 | `{item: "<runtime_resolved>", top_n: 10}` | item 값 runtime placeholder |
| R7 | `log_only` (action 명이지 함수 아님) | `diff_input_data_hash` (임시) | `{}` | **R7은 본래 automated_check 부재 rule. v0.1 schema가 required이므로 임시 매핑** |
| R8 | `trigger_full_diff_report` (profile 없음) | `diff_input_data_hash` (임시) | `{}` | **R8은 다중 함수 트리거 의도. v0.1 schema 단일 function_id로 압축** |
| R9 | `search_synonyms_in_corpus + before_hit_count_check` | `search_synonyms_in_corpus` | `{item: "<runtime_resolved>"}` | **before_hit_count_check 부분 분리** |
| R10 | `verify_no_keyword_overreach` | 동일 | `{}` | 없음 |
| R11 | `trace_responsible_keyword + check_if_new_broad` | `trace_responsible_keyword` | `{pid: "<runtime_resolved>"}` | **check_if_new_broad 부분 분리** |
| R12 | `diff_tool_version_metadata` | 동일 | `{}` | 없음 |

### 4.1 unresolved 항목 5건 (R5·R6·R7·R8·R9·R11)

| 항목 | 사유 | 후속 결정 영역 |
|---|---|---|
| R5 nuance 손실 | 원천이 data hash + tool hash 두 함수 동시 실행 의도. profile catalog는 분리 단일 함수만 제공. R12로 boundary 의존 | profile에 wrapper check 추가 또는 schema가 다중 function_id 수용 |
| R6 item placeholder | predicate의 dominant item을 runtime 해소. v0.1 schema는 static parameter 요구 | runtime parameter binding 기능 |
| R7 임시 매핑 | R7은 본래 monitor only, automated_check 부재 rule | schema가 `automated_check` optional 허용 또는 `no_op` placeholder function 등록 |
| R8 임시 매핑 + 다중 함수 | R8은 magnitude 기반 trigger. trigger_full_diff_report는 다중 함수 wrapper 의도 | profile에 trigger wrapper function 등록 |
| R9 nuance 손실 | search_synonyms_in_corpus + before_hit_count_check 두 함수 의도 | profile에 wrapper check 추가 |
| R11 nuance 손실 | trace_responsible_keyword + check_if_new_broad 두 함수 의도 | profile에 wrapper check 추가 |

---

## 5. priority_group 매핑

원천 v0.2: `rule_priority: "R12 > R8 > R6 > R4 > R1/R2/R3/R10/R11 > R5 > R9 > R7"`

v0.1-draft 4단계 enum으로 분배:

| priority_group | rules | 사유 |
|---|---|---|
| critical | R8, R12 | 자동 차단(R8) + 도구 변경 분리(R12) |
| major | R6, R4 | broad keyword 의심(R6) + 정책 완화 의심(R4) |
| standard | R1, R2, R3, R10, R11 | 정상 status 이동 분류 |
| minor | R5, R9, R7 | drift 모니터링(R5) + data debt(R9) + soft alert(R7) |

---

## 6. human_review → HumanReviewGuideline 매핑

원천 string array를 `condition` + `action` 객체 배열로 분해. `→` 또는 `—`로 split 가능한 항목은 그대로 분해. split 불가능한 항목은 condition+action 의미 유추 후 자연어 분해.

| R | guideline 수 | 분해 방식 |
|---|---|---|
| R1 | 3 | `→` split |
| R2 | 2 | `→` split |
| R3 | 2 | `→` split |
| R4 | 3 | `→` split |
| R5 | 3 | `→` split |
| R6 | 4 | `→` split 3 + `—` split 1 |
| R7 | 1 | "시" 시점 표현으로 분해 |
| R8 | 2 | 자연어 분해 |
| R9 | 3 | `→` split |
| R10 | 2 | `→` split |
| R11 | 3 | `→` split |
| R12 | 3 | 자연어 분해 |

HumanReviewGuideline.id는 본 인스턴스에서 생략 (schema에서 선택 필드).

---

## 7. metadata 기록 범위

각 rule의 `metadata` 필드 구성:

| 필드 | 값 |
|---|---|
| origin | `"v0.2 policy_change_rules.json {rule_id}, 2026-05-27"` (R6은 가공전선 패턴 명시) |
| evidence | `[]` (본 게이트에서 evidence ID 미생성) |
| verification_status | `single_case` (v0.2가 단일 사례 기반이므로 가장 보수적 표기) |
| deprecation_signal | R5·R7·R8에만 명시 (R5 측정 오류 가능성·R7·R8 category 임시 매핑) |
| created_at | `"2026-05-27"` (원천 v0.2 작성일) |
| last_reviewed_at | `"2026-05-28"` (본 migration gate 작성일) |

---

## 8. Unresolved 항목 종합

| ID | 항목 | 사유 | 후속 결정 영역 |
|---|---|---|---|
| U1 | R7 category 매핑 임시값 | profile.category_enum에 magnitude-only 카테고리 부재 | profile category_enum 보강 |
| U2 | R8 category 매핑 임시값 | 위와 동일 | 위와 동일 |
| U3 | R5 automated_check nuance 손실 | data+tool hash 동시 실행 의도, profile catalog 분리 | profile wrapper check 추가 |
| U4 | R6 automated_check item placeholder | dominant item runtime 해소, schema는 static | runtime parameter binding |
| U5 | R7 automated_check 임시 매핑 | R7은 본래 automated_check 부재 rule | schema의 automated_check optional 또는 no_op function |
| U6 | R8 automated_check 임시 매핑 + 다중 함수 | trigger_full_diff_report 다중 함수 wrapper 의도 | profile wrapper function |
| U7 | R9 automated_check nuance 손실 | search_synonyms + before_hit_count_check 두 함수 | profile wrapper check |
| U8 | R11 automated_check nuance 손실 | trace_responsible_keyword + check_if_new_broad 두 함수 | profile wrapper check |
| U9 | L7 정책 미정의 | priority_group + severity 조합 정합성 규약 부재 | L7 Policy Decision Gate |
| U10 | threshold 확정 | R6·R7·R8의 60·5·10 값이 profile.threshold_proposals 참조하나 본 게이트에서 확정 안 함 | Threshold 확정 Gate |
| U11 | HumanReviewGuideline.id 미부여 | schema에서 선택 필드, 본 게이트 생략 | 후속 revision에서 ID 부여 가능 |

---

## 9. Validator 실행 결과 요약

### 9.1 실행 명령

```
python3 scripts/schema_validator.py \
  --schema docs/.../v_next_results_d3_split/rule_schema_v0.1_draft.schema.json \
  --profile docs/.../v_next_results_d3_split/ee_agent_rule_profile_v0.1_draft.json \
  --rules docs/.../v_next_results_d3_split/policy_change_rules_v0.1_draft_instance.json \
  --report-json docs/.../v_next_results_d3_split/policy_change_rules_validation_report_v0.1.json
```

### 9.2 핵심 수치

| 항목 | 값 |
|---|---|
| exit code | 0 |
| exit_decision | `pass_with_report_only` |
| total_checks | 12 |
| passed | 11 |
| failed | 0 |
| warned | 0 |
| report_only | 1 (검사 단위; L7 검사 1개에 12 항목 누적) |
| skipped | 0 |
| errors_count | 0 |
| report_only_items_count | 12 (L7 항목 12개) |
| unresolved_policy_questions_count | 1 (L7 정책) |

### 9.3 check_outcomes

| 검사 ID | 결과 |
|---|---|
| schema_root_required | pass |
| profile_root_required | pass |
| version_alignment | pass |
| threshold_status | pass |
| L1 Rule.id uniqueness | pass (R1~R12 모두 고유) |
| L2 PredicateCall.predicate_id catalog | pass (사용 predicate 7종 모두 catalog 내) |
| L3 PredicateCall.args args_schema | pass (required + type 모두 충족) |
| L4 Verdict.category profile enum | pass (R7·R8 임시 DATA_OR_TOOL_DRIFT 포함 모두 enum 내) |
| L5 AutomatedCheckCall.function_id catalog | pass (사용 function_id 8종 모두 catalog 내) |
| L6 AutomatedCheckCall.parameters parameters_schema | pass (required + type 모두 충족) |
| L7 priority_group ↔ severity 조합 | report_only (12 rules 각각 1건, 정책 미정의) |
| L8 deprecation_signal ↔ verification_status | pass (verification_status가 모두 single_case이므로 L8 trigger 조건 well_tested 미충족) |

### 9.4 L7 보고 12건 분포

| priority_group | severity | rule 수 | 매칭 rule |
|---|---|---|---|
| critical | HARD_ALERT | 1 | R8 |
| critical | INVESTIGATE | 1 | R12 |
| major | SUSPECT | 2 | R4, R6 |
| standard | INVESTIGATE | 2 | R1, R2 |
| standard | SOFT_ALERT | 1 | R3 |
| standard | IMPROVEMENT | 2 | R10, R11 |
| minor | INVESTIGATE | 2 | R5, R9 |
| minor | SOFT_ALERT | 1 | R7 |

8 가지 조합. 본 게이트는 각 조합의 허용 여부를 결정하지 않는다. L7 Policy Decision Gate 책임.

---

## 10. 아직 말하면 안 되는 claim

| # | 주장 (금지) |
|---|---|
| C1 | threshold 4종이 확정되었다는 주장 — 60·5·10·2 값은 profile.threshold_proposals 참조이며 모두 status=proposal 유지 |
| C2 | L7 정책이 결정되었다는 주장 — 12 보고 누적, unresolved_policy_questions 1건. L7 Policy Decision Gate 대기 |
| C3 | governance verdict가 인스턴스에 적용되었다는 주장 — 본 게이트 범위 외 |
| C4 | D-4 automation이 실행되었다는 주장 — 본 게이트 진행 0건 |
| C5 | rules의 semantic correctness가 보장된다는 주장 — validator는 schema·profile contract 형식 정합만 검증. R5·R6·R7·R8·R9·R11의 nuance 손실 6건은 의미 차원에서 미해결 |
| C6 | R7·R8의 category 매핑이 확정된다는 주장 — DATA_OR_TOOL_DRIFT는 임시값 (U1·U2) |
| C7 | R6·R9·R11의 automated_check parameters에 정확한 값이 들어 있다는 주장 — `<runtime_resolved>` placeholder는 runtime resolution 필요 |
| C8 | 본 인스턴스가 v0.2 12 규칙의 1:1 완전 등가라는 주장 — automated_check nuance 손실 5건 (U3·U6·U7·U8·U11) |
| C9 | 본 게이트가 후속 review·commit·push gate를 통과시킨다는 주장 — 본 게이트는 instance 작성·validator 실행만, review는 별도 |
| C10 | scripts/schema_validator.py·기존 8종 산출물에 변경이 가해졌다는 주장 — 본 게이트 0건 |

---

## 11. 본 게이트에서 확정된 것과 미확정인 것

### 11.1 확정 사항

- v0.2 12 규칙이 v0.1-draft schema 형식의 인스턴스로 변환 완료
- L1~L6 cross-check 모두 PASS (error 0)
- 8 함수 catalog 사용, 7 predicate catalog 사용 모두 정합
- priority_group 4단계 분배 (critical·major·standard·minor)
- HumanReviewGuideline `condition` + `action` 분해 39건
- metadata 6필드 (origin·evidence·verification_status·created_at·last_reviewed_at + 일부 deprecation_signal) 모든 rule에 기록

### 11.2 미확정 사항

- U1~U11 11건 (§8 참조)
- L7 정책 (12 조합 허용 여부)
- threshold 확정값
- R7·R8 category 영구 매핑
- R5·R7·R8·R9·R11 automated_check nuance 복원
- R6·R9·R11 parameters runtime resolution 방식

---

## 12. 후속 게이트 후보

| 후보 | 단일 목적 |
|---|---|
| 후보 M-review: Instance Migration Review Gate | 본 인스턴스·migration_log·validation_report 3건이 commit 가능한지 read-only 검토 |
| 후보 M-commit: Instance Migration Commit Gate | review 통과 후 신규 3건 commit |
| 후보 M-push: Instance Migration Push Gate | commit 후 원격 보존 |
| 후보 P-policy: L7 Policy Decision Gate | L7 unresolved (12 조합 허용 매트릭스 결정) |
| 후보 T-confirm: Threshold 확정 Gate | profile.threshold_proposals 4종 확정 |
| 후보 W-profile-boost: Profile Catalog Boost Gate | U3·U6·U7·U8 wrapper check + magnitude-only category 추가 |
| 후보 N1-revision: Validator Boundary Revision Gate | `--report-json` 충돌 방어 |

직전 흐름(작성 → review → commit → push) 패턴을 이어가면 후보 M-review가 가장 가까운 자연 후속.

---

## 13. 최종 상태

`READY_FOR_INSTANCE_MIGRATION_REVIEW_GATE`
