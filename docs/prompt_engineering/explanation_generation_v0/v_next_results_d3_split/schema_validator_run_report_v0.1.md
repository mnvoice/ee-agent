# Schema Validator Run Report — v0.1

| 항목 | 값 |
|---|---|
| 상태 | RUN_AUDIT_ONLY |
| 작성일 | 2026-05-28 |
| 본 문서 단계 | Validator Run Gate 산출물 |
| validator 버전 | `0.1.0` (`scripts/schema_validator.py`, commit `202b7a4`) |
| 실행 횟수 | 1회 (본 게이트는 재실행 금지) |
| JSON report 위치 | `docs/.../v_next_results_d3_split/schema_validator_run_report_v0.1.json` |
| 후속 단계 후보 | READY_FOR_VALIDATOR_RUN_REPORT_REVIEW_GATE |

---

## 1. 실행 목적

rules 인스턴스 없이 schema·profile 파일만을 대상으로 `scripts/schema_validator.py`를 v0.1 기준 1회 실행한다. 본 실행의 목표는 다음과 같다.

- v0.1 validator의 구조적 검사 4종(schema_root_required·profile_root_required·version_alignment·threshold_status)이 schema·profile 산출물에서 통과하는지 확인
- rules 미제공 시 L1~L8가 정상적으로 skipped로 보고되는지 확인
- audit 산출물(stdout summary + JSON report)을 후속 검토용으로 보존

본 실행은 rules 인스턴스 cross-check를 포함하지 않는다. L1~L6의 실측 검증은 별도 instance migration gate 이후 가능하다.

---

## 2. 실행 명령

```
python3 scripts/schema_validator.py \
  --schema docs/prompt_engineering/explanation_generation_v0/v_next_results_d3_split/rule_schema_v0.1_draft.schema.json \
  --profile docs/prompt_engineering/explanation_generation_v0/v_next_results_d3_split/ee_agent_rule_profile_v0.1_draft.json \
  --report-json docs/prompt_engineering/explanation_generation_v0/v_next_results_d3_split/schema_validator_run_report_v0.1.json
```

CLI flag 매핑:

| flag | 값 | 비고 |
|---|---|---|
| `--schema` (필수) | `rule_schema_v0.1_draft.schema.json` | I1 |
| `--profile` (필수) | `ee_agent_rule_profile_v0.1_draft.json` | I2 |
| `--rules` (선택) | (미지정) | I3 부재 → L1~L8 skip |
| `--change-report` (선택) | (미지정) | I4 부재 → change_report_skipped 표기 |
| `--report-json` (선택) | `schema_validator_run_report_v0.1.json` | 본 게이트 JSON 산출물 경로 |

---

## 3. 입력 파일

| ID | 파일 | 존재 | SHA-256 (선두 12자) |
|---|---|---|---|
| I1 | `docs/.../v_next_results_d3_split/rule_schema_v0.1_draft.schema.json` | 통과 | `74d02d6dce4c` |
| I2 | `docs/.../v_next_results_d3_split/ee_agent_rule_profile_v0.1_draft.json` | 통과 | `67875d9e1287` |
| I3 | (미지정) | 부재 | (해당 없음) |
| I4 | (미지정) | 부재 | (해당 없음) |

입력 파일 4종 중 2종만 제공. validator는 부재 입력을 자동 skip 처리.

---

## 4. 출력 JSON 파일

| 항목 | 값 |
|---|---|
| 경로 | `docs/.../v_next_results_d3_split/schema_validator_run_report_v0.1.json` |
| 파일 크기 | 1,681 bytes |
| JSON parse | 통과 |
| root 키 | `summary`, `errors`, `warnings`, `report_only`, `unresolved_policy_questions`, `skipped_checks`, `input_files`, `metadata` (총 8 키, decision D-5 7 키 + metadata) |

---

## 5. stdout Summary 핵심 수치

```
errors:                          0
warnings:                        0
report_only items:               0
unresolved_policy_questions:     0
skipped checks:                  8
exit_decision:                   pass
exit code:                       0
```

stdout 출력에는 다음이 함께 표기된다.

- `schema:` 입력 schema 경로
- `profile:` 입력 profile 경로
- `rules:` (not provided)
- `change_report:` (not provided)
- `report_json:` 본 게이트 JSON 산출물 경로

---

## 6. JSON Report 핵심 수치

### 6.1 summary

| 키 | 값 |
|---|---|
| total_checks | 12 |
| passed | 4 |
| failed | 0 |
| warned | 0 |
| report_only | 0 |
| skipped | 8 |
| exit_decision | `pass` |
| errors_count | 0 |
| report_only_items_count | 0 |
| unresolved_policy_questions_count | 0 |

### 6.2 check_outcomes (per-check)

| 검사 ID | 결과 |
|---|---|
| schema_root_required | pass |
| profile_root_required | pass |
| version_alignment | pass |
| threshold_status | pass |
| L1 Rule.id uniqueness | skip |
| L2 PredicateCall.predicate_id catalog | skip |
| L3 PredicateCall.args args_schema | skip |
| L4 Verdict.category profile enum | skip |
| L5 AutomatedCheckCall.function_id catalog | skip |
| L6 AutomatedCheckCall.parameters parameters_schema | skip |
| L7 priority_group ↔ severity 조합 | skip |
| L8 deprecation_signal ↔ verification_status | skip |

### 6.3 errors / warnings / report_only / unresolved_policy_questions

| 섹션 | 항목 수 |
|---|---|
| errors | 0 |
| warnings | 0 (v0.1 미도입, 항상 빈 배열) |
| report_only | 0 |
| unresolved_policy_questions | 0 |

### 6.4 metadata

| 키 | 값 |
|---|---|
| validator_version | `0.1.0` |
| schema_version_const | `0.1-draft` |
| profile_version | `0.1-draft` |
| change_report_skipped | true |

`schema_version_const`과 `profile_version`이 동일하게 `0.1-draft`로 표기됨 — version_alignment 통과 근거.

---

## 7. skipped_checks 8건 사유

L1~L8 8개 검사가 모두 skip된 사유는 동일하다: **`--rules` 인자가 제공되지 않음**.

| 검사 ID | skip 사유 |
|---|---|
| L1 Rule.id uniqueness | rules 배열 부재 → 중복 ID 검사 대상 없음 |
| L2 PredicateCall.predicate_id catalog 존재 | rules 부재 → PredicateCall 대상 없음 |
| L3 PredicateCall.args args_schema | rules 부재 → args 대상 없음 |
| L4 Verdict.category profile enum 포함 | rules 부재 → verdict 대상 없음 |
| L5 AutomatedCheckCall.function_id catalog 존재 | rules 부재 → automated_check 대상 없음 |
| L6 AutomatedCheckCall.parameters parameters_schema | rules 부재 → parameters 대상 없음 |
| L7 priority_group ↔ severity 조합 | rules 부재 → 조합 관찰 대상 없음 (report_only도 발생 없음) |
| L8 deprecation_signal ↔ verification_status | rules 부재 → RuleMetadata 대상 없음 (report_only도 발생 없음) |

skip은 validator 자체의 정상 동작이며, exit_decision = `pass`와 정합한다. skip은 검사 실패가 아니다.

---

## 8. 아직 말하면 안 되는 claim

본 실행 결과가 `pass`라고 해서 다음 항목이 검증되었다고 주장해서는 안 된다.

| # | 주장 (금지) |
|---|---|
| C1 | rules 인스턴스가 schema·profile contract와 정합하다는 주장 — rules 미제공으로 L1~L6 cross-check 미수행 |
| C2 | L1~L8 실측 cross-check가 완료되었다는 주장 — 8건 모두 skip |
| C3 | v0.2 → v0.1-draft 마이그레이션이 완료되었다는 주장 — 본 게이트 범위 외 |
| C4 | threshold 4종이 확정되었다는 주장 — `threshold_status` pass는 `status: "proposal"`이 올바르게 표기되었다는 의미일 뿐, 확정과 무관 |
| C5 | L7·L8 정책이 결정되었다는 주장 — 본 실행에서 L7·L8은 skip, unresolved_policy_questions도 0건 (rules 부재로 패턴 발현 없음) |
| C6 | validator가 모든 미확정 영역(warning 등급·P1~P6·exit code 세부 분기)을 결정했다는 주장 — decision 문서 §6.2 미확정 유지 |
| C7 | schema·profile이 모든 도메인 경계 조건에서 정합하다는 주장 — 본 실행은 structural 4종만 통과 확인. JSON Schema draft-07 full validation 미수행 |
| C8 | 본 audit 산출물이 commit·push 되었다는 주장 — 본 게이트는 audit 생성만, commit·push는 분리 게이트 |
| C9 | scripts/schema_validator.py 코드 수정이 필요 없음이 확정되었다는 주장 — N1(`--report-json` ↔ 입력 경로 충돌 방어) 비-blocker 후보 유지 |

---

## 9. 본 게이트에서 확정된 것과 미확정인 것

### 9.1 확정 사항

- validator v0.1.0이 schema·profile만으로 실행 가능 (exit 0)
- 구조적 검사 4종(schema_root_required·profile_root_required·version_alignment·threshold_status) 모두 pass
- rules 미제공 시 L1~L8 8건 모두 skip 보고
- JSON report root 8 키 모두 정상 발행
- `schema_version_const = profile_version = "0.1-draft"` (version_alignment pass 근거)
- input_files에 SHA-256 hash 정상 기록

### 9.2 미확정 사항

- rules 인스턴스 cross-check 결과 (L1~L6 실측)
- L7·L8 정책 결정 (validator는 옵션만 기록할 뿐 결정 권한 없음)
- threshold 확정값
- migration 가능 여부
- N1 (`--report-json` ↔ 입력 경로 충돌 방어)
- P1~P6 도입 여부

---

## 10. 다음 자연 gate

본 audit 산출물이 review·승인되면 자연 후속 후보:

| 후보 | 단일 목적 |
|---|---|
| 후보 V-run-review: Validator Run Report Review Gate | 본 audit 산출물(md + json)이 commit 가능한지 read-only 검토 |
| 후보 V-run-commit: Validator Run Report Commit Gate | review 통과 후 신규 audit 1~2건 commit |
| 후보 V-run-push: Validator Run Report Push Gate | commit 후 원격 보존 |
| **후보 R-migrate: Instance Migration Gate** | v0.2 `policy_change_rules.json` 12 규칙 → v0.1-draft schema 인스턴스 변환. **변환 완료 후 validator를 동일 명령에 `--rules`를 추가하여 L1~L6 실측 cross-check 가능** |
| 후보 P-policy: L7·L8 Policy Decision Gate | unresolved_policy_questions 정책 결정 |
| 후보 N1-revision: Validator Boundary Revision Gate | `--report-json` ↔ 입력 경로 충돌 방어 추가 |

본 게이트 인계 메시지의 "다음 자연 gate" 항목은 **후보 R-migrate (Instance Migration Gate)**를 명시함. validator가 v0.1.0으로 작동 가능함이 확인된 현 시점에서, validator의 실측 활용을 위해 가장 우선이 되는 자연 후속은 rules 인스턴스 입력 확보(R-migrate)이다. design·decision·implementation·run 4단계 흐름이 종결되었고, validator의 실측 능력은 rules 인스턴스 입력 유무에 의해 결정됨.

---

## 11. 최종 상태

`READY_FOR_VALIDATOR_RUN_REPORT_REVIEW_GATE`
