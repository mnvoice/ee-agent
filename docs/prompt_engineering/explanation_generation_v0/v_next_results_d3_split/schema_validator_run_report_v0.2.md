# Schema Validator Run Report — v0.2

| 항목 | 값 |
|---|---|
| 상태 | RUN_AUDIT_ONLY |
| 작성일 | 2026-05-28 |
| 본 문서 단계 | Validator Run Gate v0.2 산출물 |
| validator 버전 | `0.1.0` (`scripts/schema_validator.py`, commit `202b7a4`) |
| 실행 횟수 | 1회 (본 게이트는 재실행 금지) |
| JSON report 위치 | `docs/.../v_next_results_d3_split/schema_validator_run_report_v0.2.json` |
| 후속 단계 후보 | READY_FOR_VALIDATOR_RUN_V0_2_REVIEW_GATE |

---

## 1. 실행 목적

profile v0.2 + instance v0.2를 입력으로 `scripts/schema_validator.py` v0.1.0을 1회 실행한다. 본 실행의 목표:

- profile v0.2 (MAGNITUDE_DELTA + wrapper 5종 + parameters_schema 완화)와 instance v0.2 (R7·R8 category 갱신 + R5·R7·R8·R9·R11 wrapper 적용 + R6·R9·R11 dynamic binding + HumanReviewGuideline G1~Gn id) 사이 cross-check 실측
- L1~L6 catalog 멤버십·args/parameters 검증을 통해 U1·U2·U3·U4·U5·U6·U7·U8 적용의 cross-check 확정
- L7·L8 동작 재확인
- audit 산출물(stdout + JSON report) 보존

본 실행은 U9 (L7 정책)·U10 (threshold 확정)을 다루지 않는다.

---

## 2. 실행 명령

```
python3 scripts/schema_validator.py \
  --schema docs/.../v_next_results_d3_split/rule_schema_v0.1_draft.schema.json \
  --profile docs/.../v_next_results_d3_split/ee_agent_rule_profile_v0.2_draft.json \
  --rules docs/.../v_next_results_d3_split/policy_change_rules_v0.2_draft_instance.json \
  --report-json docs/.../v_next_results_d3_split/schema_validator_run_report_v0.2.json
```

| flag | 값 | 비고 |
|---|---|---|
| `--schema` | `rule_schema_v0.1_draft.schema.json` | I1 (v0.1 schema, 무변동) |
| `--profile` | `ee_agent_rule_profile_v0.2_draft.json` | I2 (v0.2 profile, MAGNITUDE_DELTA + wrapper 5종) |
| `--rules` | `policy_change_rules_v0.2_draft_instance.json` | I3 (v0.2 instance, 12 rules) |
| `--change-report` | (미지정) | I4 부재 |
| `--report-json` | `schema_validator_run_report_v0.2.json` | 본 게이트 JSON 산출물 경로 |

---

## 3. 입력 파일

| ID | 파일 | 존재 | SHA-256 (선두 12자) |
|---|---|---|---|
| I1 | `rule_schema_v0.1_draft.schema.json` | 통과 | `74d02d6dce4c` |
| I2 | `ee_agent_rule_profile_v0.2_draft.json` | 통과 | `6372d512a33a` |
| I3 | `policy_change_rules_v0.2_draft_instance.json` | 통과 | `a010c1a8bab0` |
| I4 | (미지정) | 부재 | (해당 없음) |

I1·I2·I3 3종 모두 제공. I4 부재.

### 3.1 v0.1 audit과의 hash 비교

| 입력 | v0.1 audit | v0.2 audit | 변화 |
|---|---|---|---|
| schema | `74d02d6dce4c` | `74d02d6dce4c` | 동일 (schema 무변동, design 결정과 정합) |
| profile | `67875d9e1287` (v0.1) | `6372d512a33a` (v0.2) | 변경 (v0.1 → v0.2 catalog 보강) |
| rules | 부재 (v0.1 audit에서 미제공) | `a010c1a8bab0` (v0.2) | 신규 제공 |

---

## 4. stdout Summary 핵심 수치

```
errors:                          0
warnings:                        0
report_only items:               12
unresolved_policy_questions:     1
skipped checks:                  0
exit_decision:                   pass_with_report_only
exit code:                       0
```

---

## 5. JSON Report 핵심 수치

### 5.1 summary

| 키 | 값 |
|---|---|
| total_checks | 12 |
| passed | 11 |
| failed | 0 |
| warned | 0 |
| report_only | 1 (검사 단위) |
| skipped | 0 |
| exit_decision | `pass_with_report_only` |
| errors_count | 0 |
| report_only_items_count | 12 (L7 항목 12개) |
| unresolved_policy_questions_count | 1 |

### 5.2 check_outcomes

| 검사 ID | 결과 | 비고 |
|---|---|---|
| schema_root_required | pass | schema 5 required root 모두 존재 |
| profile_root_required | pass | profile v0.2 6 required root 모두 존재 |
| version_alignment | pass | schema_version_const = compatible_schema_version = `0.1-draft` |
| threshold_status | pass | profile v0.2 threshold_proposals 4종 모두 `status=proposal` |
| L1 Rule.id uniqueness | pass | 12 rules R1~R12 모두 unique |
| L2 PredicateCall.predicate_id catalog | pass | 사용 predicate 7종 모두 profile v0.2 predicate_library 멤버 |
| L3 PredicateCall.args args_schema | pass | required + type 모두 충족 |
| L4 Verdict.category profile enum | pass | 사용 category 9종 (RECOVERABILITY·AMBIGUITY·ROUTING·POLICY_RELAXATION·DATA_OR_TOOL_DRIFT·BROAD_KEYWORD·DATA_DEBT·TOOL_CHANGE·**MAGNITUDE_DELTA**) 모두 profile v0.2 category_enum 멤버 |
| L5 AutomatedCheckCall.function_id catalog | pass | 사용 function_id 12종 (wrapper 5종 포함) 모두 profile v0.2 check_library 멤버 |
| L6 AutomatedCheckCall.parameters parameters_schema | pass | required + type 모두 충족 (dynamic binding dict 값 포함, profile v0.2 type 완화로 통과) |
| L7 priority_group ↔ severity 조합 | report_only | 12 rules 각각 1건, 정책 미정의 |
| L8 deprecation_signal ↔ verification_status | pass | verification_status가 모두 `single_case` (L8 trigger 조건 `well_tested` 미충족) |

### 5.3 metadata

| 키 | 값 |
|---|---|
| validator_version | `0.1.0` |
| schema_version_const | `0.1-draft` |
| profile_version | `0.2-draft` |
| change_report_skipped | true |

---

## 6. U1~U8/U11 cross-check 확정 결과

본 실행으로 U1·U2·U3·U4·U5·U6·U7·U8 적용이 cross-check 차원에서 확정되었다. U11도 schema 차원에서 정합 확인.

| Unresolved | instance v0.2 적용 | validator cross-check 결과 | 확정 여부 |
|---|---|---|---|
| U1 (R7 category 임시) | R7.verdict.category = MAGNITUDE_DELTA | L4 pass | **확정** |
| U2 (R8 category 임시) | R8.verdict.category = MAGNITUDE_DELTA | L4 pass | **확정** |
| U3 (R5 wrapper) | R5.automated_check.function_id = evaluate_drift_origin | L5 pass | **확정** |
| U4 (R6 runtime binding) | R6.parameters.item = `{"$dynamic": "predicate_dominant_item"}` | L6 pass (profile v0.2 type 완화) | **확정** |
| U5 (R7 wrapper) | R7.function_id = monitor_delta_no_action | L5 pass | **확정** |
| U6 (R8 wrapper) | R8.function_id = trigger_full_diff_report | L5 pass | **확정** |
| U7 (R9 wrapper) | R9.function_id = diagnose_data_debt_origin + parameters.item dict | L5·L6 pass | **확정** |
| U8 (R11 wrapper) | R11.function_id = inspect_recovery_path_origin + parameters.pid dict | L5·L6 pass | **확정** |
| U11 (HumanReviewGuideline.id) | 31개 모두 G1~Gn 부여 | schema validation 통과 (HumanReviewGuideline 형식 정합) | **확정** |

본 게이트는 **9건 unresolved의 form-level cross-check 확정**을 보고한다. semantic correctness 보장이나 도구 측 wrapper 실제 구현 완료는 별도 영역.

---

## 7. U9·U10 미해소 유지

| Unresolved | 본 게이트 상태 | 책임 gate |
|---|---|---|
| U9 (L7 정책 미정의) | **미해소 유지**. 본 실행에서 L7 report_only 12건 발현 + unresolved_policy_questions 1건 누적 | L7 Policy Decision Gate v0.2 |
| U10 (threshold 4종 확정) | **미해소 유지**. threshold_proposals 4종 모두 `status=proposal`로 통과 (확정 아님) | Threshold 확정 Gate |

본 게이트는 U9·U10을 다루지 않는다.

---

## 8. v0.1 audit과 v0.2 audit 비교

| 항목 | v0.1 audit (commit `157baae`) | v0.2 audit (본 게이트) |
|---|---|---|
| rules instance | 미제공 (L1~L8 skip) | 제공 (L1~L8 실행) |
| L1~L6 결과 | skip (8건) | **pass** (실측 확정) |
| L7 결과 | skip | **report_only 12건** |
| L8 결과 | skip | pass |
| exit_decision | `pass` | `pass_with_report_only` |
| skipped_checks | 8 (L1~L8) | 0 |
| unresolved_policy_questions | 0 | 1 (L7) |

v0.2 audit이 v0.1 audit 대비 L1~L8 실측 cross-check를 확정. v0.2 instance·profile catalog가 v0.1 schema와 정합함을 처음으로 실측 확인.

---

## 9. L7 report_only 분포 (12 rules)

본 실행의 L7 report_only 12 항목 분포 (priority_group × severity):

| # | priority_group | severity | 매칭 rule | rule 수 |
|---|---|---|---|---|
| 1 | critical | HARD_ALERT | R8 | 1 |
| 2 | critical | INVESTIGATE | R12 | 1 |
| 3 | major | SUSPECT | R4, R6 | 2 |
| 4 | standard | INVESTIGATE | R1, R2 | 2 |
| 5 | standard | SOFT_ALERT | R3 | 1 |
| 6 | standard | IMPROVEMENT | R10, R11 | 2 |
| 7 | minor | INVESTIGATE | R5, R9 | 2 |
| 8 | minor | SOFT_ALERT | R7 | 1 |

L7 Policy Decision Gate v0.1 (commit `9e73be4`)의 8 조합 매핑과 동일. v0.2 instance에서도 priority_group·severity가 v0.1 instance와 동일하게 유지되었음을 의미.

L7 Policy Decision v0.1에서는 6 allowed + 2 review_later (critical·INVESTIGATE / minor·INVESTIGATE)로 분류. 본 게이트는 정책 재결정 없이 관찰만 기록.

---

## 10. 아직 말하면 안 되는 claim

본 실행 결과가 `pass_with_report_only`라고 해서 다음 항목이 결정되었다고 주장해서는 안 된다.

| # | 주장 (금지) |
|---|---|
| C1 | wrapper 5종 (evaluate_drift_origin·monitor_delta_no_action·trigger_full_diff_report·diagnose_data_debt_origin·inspect_recovery_path_origin)이 도구 측에서 실제 구현되었다는 주장 — catalog 멤버십만 cross-check 통과. 도구 측 실제 구현은 별도 트랙 |
| C2 | dynamic binding 객체 `{"$dynamic": "..."}`이 runtime에서 정확히 해소된다는 주장 — schema·profile 차원 형식 정합만 cross-check. runtime 해소 로직은 도구 측 책임 |
| C3 | semantic correctness가 보장된다는 주장 — validator는 형식·catalog 멤버십 cross-check만 수행. 의미 차원 검증 아님 |
| C4 | threshold 4종이 확정되었다는 주장 — `threshold_status` pass는 `status=proposal` 표기 정합만 의미 |
| C5 | L7 review_later 2 조합이 본 게이트로 해소되었다는 주장 — L7 report_only 12건 누적, unresolved_policy_questions 1건. **U9 미해소 유지** |
| C6 | L7 정책이 본 게이트로 결정되었다는 주장 — 본 게이트는 정책 결정 아님 |
| C7 | governance·D-4 automation이 본 게이트에서 진행되었다는 주장 — 0건 |
| C8 | MAGNITUDE_DELTA category가 다른 도메인에 적용 가능하다는 주장 — ee-agent profile v0.2 한정 적용 |
| C9 | 본 audit 산출물이 commit·push 되었다는 주장 — 본 게이트는 audit 생성만 |
| C10 | U11 부여된 HumanReviewGuideline id의 cross-rule uniqueness가 보장된다는 주장 — rule-local uniqueness만 명시 |
| C11 | v0.1 instance·v0.1 profile이 본 audit으로 deprecated 처리되었다는 주장 — 두 v0.1 파일은 history 보존, 본 게이트와 무관 |

---

## 11. 본 게이트에서 확정된 것과 미확정인 것

### 11.1 확정 사항

- validator v0.1.0이 v0.2 profile + v0.2 instance와 호환 (exit 0, exit_decision `pass_with_report_only`)
- L1~L6 cross-check pass (U1·U2·U3·U4·U5·U6·U7·U8 form-level 확정)
- L8 pass (verification_status `single_case` 12 rules로 L8 trigger 조건 미충족)
- L7 report_only 12건 + unresolved_policy_questions 1건 (v0.1 audit 정합과 일관)
- profile v0.2 `MAGNITUDE_DELTA` category가 instance v0.2 R7·R8에서 정상 작동
- profile v0.2 wrapper 5종이 instance v0.2 R5·R7·R8·R9·R11에서 정상 작동
- profile v0.2 parameters_schema type 완화가 instance v0.2 R6·R9·R11 dynamic binding 객체 수용
- HumanReviewGuideline 31 id가 schema 형식과 정합
- schema·profile·instance·validator 본 게이트 무변동

### 11.2 미확정 사항

- 도구 측 wrapper 5종 실제 구현
- dynamic binding 객체의 runtime resolution 로직
- L7 review_later 2 조합 영구 정책 (U9, L7 Policy Decision Gate v0.2 책임)
- threshold 4종 확정값 (U10, Threshold 확정 Gate 책임)
- semantic correctness 차원 검증
- cross-rule HumanReviewGuideline.id uniqueness 정책
- v0.2 audit 산출물의 commit·push (별도 게이트)

---

## 12. 후속 게이트 후보

| 후보 | 단일 목적 |
|---|---|
| 후보 V-run-review: Validator Run v0.2 Review Gate | 본 audit 2건이 commit 가능한지 read-only 검토 |
| 후보 V-run-commit: Validator Run v0.2 Commit Gate | review 통과 후 audit 2건 commit |
| 후보 V-run-push: Validator Run v0.2 Push Gate | commit 후 원격 보존 |
| 후보 P-policy v0.2: L7 Policy Decision Gate v0.2 | U9 해소 (L7 review_later 2 조합 영구 정책) |
| 후보 T-confirm: Threshold 확정 Gate | U10 해소 |
| 후보 V-revision: Validator Boundary Revision Gate | L7 enforcement 도입 (U9 결정 후) |

직전 흐름(작성 → review → commit → push)을 이어가면 후보 V-run-review가 가장 가까운 자연 후속.

---

## 13. 최종 상태

`READY_FOR_VALIDATOR_RUN_V0_2_REVIEW_GATE`
