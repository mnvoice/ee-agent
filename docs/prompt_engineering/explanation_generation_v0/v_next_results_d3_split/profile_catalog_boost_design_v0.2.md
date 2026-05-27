# Profile Catalog Boost Design — v0.2 (Draft)

| 항목 | 값 |
|---|---|
| 상태 | DESIGN_ONLY |
| 작성일 | 2026-05-28 |
| 본 문서 단계 | Profile Catalog Boost Gate 산출물 |
| 후속 단계 후보 | READY_FOR_PROFILE_CATALOG_BOOST_REVIEW_GATE |
| 대상 unresolved | U1·U2·U3·U4·U5·U6·U7·U8·U11 (9건, migration_log §8) |
| 입력 schema | `rule_schema_v0.1_draft.schema.json` (commit `ee2e515`) |
| 입력 profile | `ee_agent_rule_profile_v0.1_draft.json` (commit `ee2e515`) |
| 입력 instance | `policy_change_rules_v0.1_draft_instance.json` (commit `411912a`) |
| 입력 validator | `scripts/schema_validator.py` (commit `202b7a4`) |

---

## 0. 본 게이트의 단일 목적과 범위

migration_log §8의 unresolved 11건 중 profile 표현력 부족이 직접 원인인 U1·U2·U3·U4·U5·U6·U7·U8·U11 (9건) 처리를 위한 catalog boost 설계를 작성한다. 본 문서는 **설계 문서**이며 어떤 파일도 수정하지 않는다.

### 0.1 본 게이트가 다루는 unresolved 9건

| ID | 원인 영역 | 본 게이트 처리 |
|---|---|---|
| U1 | R7 category 임시 (magnitude-only category 부재) | category_enum 보강 |
| U2 | R8 category 임시 (위와 동일) | category_enum 보강 |
| U3 | R5 automated_check nuance 손실 (data+tool 동시) | wrapper check 보강 |
| U4 | R6 item placeholder parameter binding | runtime binding 정책 |
| U5 | R7 automated_check 임시 매핑 (monitor only) | wrapper check 보강 또는 schema optional |
| U6 | R8 automated_check 임시 매핑 (multi-trigger) | wrapper check 보강 |
| U7 | R9 automated_check nuance 손실 (synonyms+hit count) | wrapper check 보강 |
| U8 | R11 automated_check nuance 손실 (trace+broad check) | wrapper check 보강 |
| U11 | HumanReviewGuideline.id 미부여 | instance revision 권장 (schema 수정 불요) |

### 0.2 본 게이트가 다루지 않는 unresolved

- U9 (L7 정책 미정의): L7 Policy Decision Gate 책임. 본 게이트와 독립
- U10 (threshold 확정): Threshold 확정 Gate 책임

### 0.3 본 게이트에서 변경하지 않는 것

- `ee_agent_rule_profile_v0.1_draft.json`을 수정하지 않는다.
- `rule_schema_v0.1_draft.schema.json`을 수정하지 않는다.
- `policy_change_rules_v0.1_draft_instance.json`을 수정하지 않는다.
- `scripts/schema_validator.py`를 수정하지 않는다.
- validator를 재실행하지 않는다.
- threshold를 확정하지 않는다.
- governance·D-4 automation을 진행하지 않는다.
- commit·push를 진행하지 않는다.

---

## 1. U1·U2 — Magnitude Category 보강 (category_enum)

### 1.1 현재 상태

profile.domain_taxonomy.category_enum 9종은 모두 "변동 유형" 카테고리:

```
RECOVERABILITY · AMBIGUITY · ROUTING · POLICY_RELAXATION · DATA_OR_TOOL_DRIFT
BROAD_KEYWORD · DATA_DEBT · TOOL_CHANGE · SUBJECT_CHANGE
```

R7 (soft alert, 변동 ≤ 5%)과 R8 (hard alert, 변동 ≥ 10%)은 "변동 크기" 기준 rule. 9 category 어느 것도 magnitude를 직접 표현하지 않으므로 instance에서 DATA_OR_TOOL_DRIFT로 임시 매핑.

### 1.2 후보 매핑 전략

| 전략 | 옵션 | 장점 | 단점 |
|---|---|---|---|
| A | 단일 magnitude category 추가 (예: `MAGNITUDE_DELTA`) | 9 → 10 category, 변경 폭 작음 | R7·R8 등급 차이를 category로 표현 불가 |
| B | 2 magnitude category 추가 (`SOFT_ALERT_VOLUME` + `HARD_ALERT_VOLUME`) | R7·R8 분리 표현 | 9 → 11 category, severity와 의미 중복 |
| C | 단일 통합 category 추가 (`POLICY_SHIFT_SCALE`) + R7·R8 severity로 등급 표현 | severity·category 역할 분리 유지 | "scale" 어휘가 magnitude 의미를 명확히 전달하지 못함 |
| D | category는 그대로 (DATA_OR_TOOL_DRIFT 임시 유지) + `metadata.deprecation_signal`로만 명시 | profile 수정 없음 | unresolved 영구 잔존 |

### 1.3 권장 (본 설계의 v0.2 안)

**전략 A (`MAGNITUDE_DELTA` 단일 추가)**

근거:
- severity가 이미 SOFT_ALERT·HARD_ALERT로 등급을 표현 (전략 B와 의미 중복 회피)
- 단일 category가 변경 폭 최소화
- `MAGNITUDE_DELTA`는 "변동 크기"라는 의미를 직접 전달
- 후속 도메인에서도 재사용 가능 (recsys·react-confidence에서도 변동 크기 기준 rule 가능)

### 1.4 적용 시 instance 변경 예시 (구현 gate 작업, 본 게이트는 표기만)

```
R7.verdict.category: DATA_OR_TOOL_DRIFT → MAGNITUDE_DELTA
R8.verdict.category: DATA_OR_TOOL_DRIFT → MAGNITUDE_DELTA
R7·R8.metadata.deprecation_signal: 매핑 임시 명시 제거 (확정 매핑으로 갱신)
```

### 1.5 결정 영역

| 항목 | 본 게이트 결정 |
|---|---|
| profile category_enum에 `MAGNITUDE_DELTA` 추가 | 제안 (실제 수정은 구현 gate) |
| `MAGNITUDE_DELTA`의 description | "변동 크기 기반 rule. severity와 결합하여 magnitude 분류" |
| L7 매트릭스 영향 | (priority, severity) 조합과 무관. L7 정책은 별도 |
| backward compatibility | DATA_OR_TOOL_DRIFT는 유지 (R5 등에서 계속 사용) |

---

## 2. U3·U5·U6·U7·U8 — Wrapper Check 보강 (check_library)

### 2.1 현재 상태

profile.check_library 10종은 단일 동작 함수만 정의:

```
multi_word_keyword_recovery_test · list_competing_items_per_pid · list_before_after_items_per_pid
compare_keyword_lists_for_new_broad · diff_input_data_hash · diff_tool_version_metadata
list_top_matching_keywords_for_item · search_synonyms_in_corpus
trace_responsible_keyword · verify_no_keyword_overreach
```

v0.2 원천 5 rule (R5·R7·R8·R9·R11)은 다음 의도를 가지나 단일 함수로 충분히 표현되지 않음:

| Rule | 원천 의도 | v0.1 매핑 | nuance 손실 |
|---|---|---|---|
| R5 | data hash + tool hash 동시 검사 | `diff_input_data_hash` (data만) | tool hash 분리 |
| R7 | monitor only (automated_check 부재) | `diff_input_data_hash` (임시) | 의미 충돌 (monitor ≠ diff) |
| R8 | trigger full diff report (multi-함수 wrapper) | `diff_input_data_hash` (임시) | multi-함수 부재 |
| R9 | search_synonyms + before_hit_count_check | `search_synonyms_in_corpus` (전자만) | before_hit_count 분리 |
| R11 | trace_responsible_keyword + check_if_new_broad | `trace_responsible_keyword` (전자만) | broad check 분리 |

### 2.2 후보 wrapper check 5종 제안

| 신규 function_id | 의도 | parameters_schema 권장 |
|---|---|---|
| `evaluate_drift_origin` | data hash + tool hash 동시 검사 (R5) | `{}` (parameters 없음, 두 hash 모두 자동 확인) |
| `monitor_delta_no_action` | monitor only — 어떤 변경도 수행하지 않고 단순 기록 (R7) | `{}` |
| `trigger_full_diff_report` | data·tool·policy hash 모두 검사 + diff report 산출 (R8) | `{}` |
| `diagnose_data_debt_origin` | synonyms 검사 + before/after hit count 비교 (R9) | `{"item": "<runtime_resolved>"}` |
| `inspect_recovery_path_origin` | responsible keyword 추적 + broad check 통합 (R11) | `{"pid": "<runtime_resolved>"}` |

### 2.3 적용 시 instance 변경 예시

```
R5.automated_check.function_id: diff_input_data_hash → evaluate_drift_origin
R7.automated_check.function_id: diff_input_data_hash → monitor_delta_no_action
R8.automated_check.function_id: diff_input_data_hash → trigger_full_diff_report
R9.automated_check.function_id: search_synonyms_in_corpus → diagnose_data_debt_origin
R11.automated_check.function_id: trace_responsible_keyword → inspect_recovery_path_origin
```

instance 변경 후 R5·R7·R8·R9·R11 metadata.deprecation_signal에서 "nuance 손실"·"임시 매핑" 표기 제거 가능.

### 2.4 backward compatibility

기존 10 단일 함수는 유지 (다른 rule이 직접 사용 중). 신규 5 wrapper는 catalog 추가만이며 기존 함수 대체 아님.

### 2.5 결정 영역

| 항목 | 본 게이트 결정 |
|---|---|
| 신규 5 wrapper 추가 | 제안 (실제 수정은 구현 gate) |
| 기존 10 함수 보존 | 유지 |
| validator L5 영향 | 새 5 function_id가 catalog에 등록되면 자동 통과 (현재 validator는 catalog 멤버십만 검사) |
| 도구 측 실제 구현 | profile catalog 추가는 도구 측 함수 구현과 분리. 도구 구현은 별도 트랙 (본 설계 범위 외) |

---

## 3. U4 — Runtime Parameter Binding 정책

### 3.1 현재 상태

R6.automated_check.parameters = `{"item": "<runtime_resolved>", "top_n": 10}`

`<runtime_resolved>`는 string placeholder. validator의 L6 검사는 minimum check (required + top-level type)만 수행하므로 string 값이 들어있으면 통과. 단, 의미 차원에서 "runtime 해소가 필요한 binding"임이 schema·profile에서 명시되지 않음.

### 3.2 후보 처리 전략

| 전략 | 옵션 | profile 수정 | schema 수정 | validator 수정 |
|---|---|---|---|---|
| A | 현 상태 유지 (`<runtime_resolved>` string placeholder + deprecation_signal 표기) | 불요 | 불요 | 불요 |
| B | profile parameters_schema에 dynamic binding 명세 추가 (예: `{"$dynamic": "predicate_dominant_item"}` 형식) | 필요 (`parameters_schema`에 메타 필드 추가) | 불요 (schema가 parameters_schema 내부 형식 강제 안 함) | 불요 (validator는 minimum check만) |
| C | schema에 runtime_binding 영역 신설 (PredicateCall·AutomatedCheckCall에 `runtime_binding` 필드 추가) | 불요 | 필요 (PredicateCall·AutomatedCheckCall schema 보강) | 필요 (L3·L6 검사에 binding 검증 추가) |

### 3.3 권장

**전략 B (`profile parameters_schema`에 dynamic binding 메타 명세)**

근거:
- schema·validator 수정 0 → 변경 폭 최소화
- profile에서 도메인별 dynamic binding 정책을 자유 정의 가능 (다른 도메인은 별도 정책)
- `<runtime_resolved>` 자리에 `{"$dynamic": "predicate_dominant_item"}` 형식 객체를 두면 도구 측 runtime 해소 로직이 메타를 읽어 처리
- 본 시점 validator는 string 검사만 하므로 dict 값도 minimum check 우회 가능 (단, parameters_schema의 type이 string이면 dict는 reject — 후속 검토)

### 3.4 추가 검토 (parameters_schema의 type 강제)

R6의 `list_top_matching_keywords_for_item.parameters_schema`:

```
{
  "type": "object",
  "required": ["item"],
  "properties": {
    "item": {"type": "string"},
    "top_n": {"type": "integer", "minimum": 1}
  }
}
```

`item.type = string`이므로 dict 값을 넣으면 L6 fail. 전략 B 적용 시:
- 옵션 B1: parameters_schema의 `item.type`을 `["string", "object"]`로 완화
- 옵션 B2: parameters_schema에 별도 `dynamic_binding_allowed` 메타 추가, validator가 이 메타를 읽어 type 검사 우회

본 설계는 **옵션 B1을 1차 권장**. 단 dynamic binding의 형식(`$dynamic` 패턴 등)은 별도 검토 영역.

### 3.5 결정 영역

| 항목 | 본 게이트 결정 |
|---|---|
| schema 수정 | 불요 (전략 B 채택) |
| profile parameters_schema 수정 | 필요 (R6의 list_top_matching_keywords_for_item, R9의 diagnose_data_debt_origin, R11의 inspect_recovery_path_origin 등) |
| validator 수정 | 잠재적 필요 (옵션 B2 채택 시). 옵션 B1 채택 시 불요 |
| 본 게이트 권장 | 옵션 B1 (validator 수정 회피, parameters_schema type 완화) |

---

## 4. U11 — HumanReviewGuideline.id 처리

### 4.1 현재 상태

instance의 모든 HumanReviewGuideline 객체에 `id` 필드 부재. schema 정의:

```
HumanReviewGuideline:
  id: pattern "^G\d+$" (선택)
  condition: string (필수)
  action: string (필수)
```

id가 선택이므로 schema·validator 통과. 단, 동일 rule 안에서 guideline 식별이 어려움.

### 4.2 후보 처리

| 전략 | 옵션 | 영향 |
|---|---|---|
| A | id 부재 유지 (현 상태) | 변경 없음. 외부 reference 불가 |
| B | instance revision에서 id 부여 (G1·G2·G3...) | instance 수정 1건. schema·profile·validator 0 |
| C | instance + schema 양쪽 수정 (id를 required로 승급) | 영향 폭 큼 |

### 4.3 권장

**전략 B (instance revision에서 id 부여)**

근거:
- schema·validator 수정 0 → 변경 폭 최소
- instance 갱신 후 G1·G2·G3 같은 식별자로 외부 reference 가능
- v0.2 instance가 자연스럽게 id를 포함하도록 정책 변경

### 4.4 적용 시 instance 변경 예시

각 rule의 human_review_guidelines 배열의 각 항목에 id 추가:

```
"human_review_guidelines": [
  {"id": "G1", "condition": "...", "action": "..."},
  {"id": "G2", "condition": "...", "action": "..."},
  ...
]
```

id는 rule 내부에서만 unique. 다른 rule의 G1과 충돌 가능 (schema pattern `^G\d+$`만 강제). cross-rule uniqueness는 v0.2 정책에서 결정 영역.

### 4.5 결정 영역

| 항목 | 본 게이트 결정 |
|---|---|
| HumanReviewGuideline.id를 schema에서 required로 승급 | 불요 (전략 B 채택, schema 무변동) |
| instance revision에서 39 guideline 모두 id 부여 | 제안 (실제 수정은 instance revision gate) |
| id uniqueness scope | rule-local 권장 (cross-rule은 v0.3 검토) |

---

## 5. Versioning Plan

### 5.1 본 boost 적용 시 권장 version 변화

| 파일 | 현재 | 본 boost 적용 후 |
|---|---|---|
| `rule_schema_v0.1_draft.schema.json` | 0.1-draft | **0.1-draft 유지** (전략 B로 schema 무변동) |
| `ee_agent_rule_profile_v0.1_draft.json` | 0.1-draft | **0.2-draft 승급** (category_enum + check_library + parameters_schema 보강) |
| `policy_change_rules_v0.1_draft_instance.json` | 0.1-draft | **0.2-draft 승급** (R6·R7·R8·R9·R11 category·check 재배정 + HumanReviewGuideline.id 부여) |
| `scripts/schema_validator.py` | 0.1.0 | **0.1.0 유지** (전략 B로 validator 무변동) |

### 5.2 파일명 권장

| 파일 | v0.2 파일명 권장 |
|---|---|
| profile | `ee_agent_rule_profile_v0.2_draft.json` (신규 파일, v0.1은 history 보존) |
| instance | `policy_change_rules_v0.2_draft_instance.json` (신규 파일) |
| schema | 변경 없음 (`rule_schema_v0.1_draft.schema.json` 유지) |

### 5.3 schema.SchemaMetadata.compatible_with_instance_versions

본 boost는 schema 자체를 수정하지 않으므로 `SchemaMetadata.schema_version` const("0.1-draft") 유지. 단, profile_version·instance_version은 schema와 독립적으로 0.2-draft 승급 가능.

후속 검토: schema_version과 profile·instance version의 분리·연동 정책. 본 설계는 분리 유지 권장.

---

## 6. 영향 범위 종합

| 영역 | 본 boost 적용 시 변경 | 본 게이트 진행 |
|---|---|---|
| profile | 필요 (category_enum +1, check_library +5, parameters_schema 일부) | 변경 없음 (설계만) |
| instance | 필요 (R6·R7·R8·R9·R11 매핑 갱신 + HumanReviewGuideline.id 부여 39건) | 변경 없음 (설계만) |
| schema | 불요 (전략 B 채택) | 변경 없음 |
| validator | 불요 (전략 B 채택) | 변경 없음 |
| validator 재실행 | 보강 후 검증 시 1회 (별도 gate) | 0회 |

---

## 7. Recommended Next Gates

| 후보 | 단일 목적 |
|---|---|
| 후보 B-review: Profile Catalog Boost Review Gate | 본 설계 문서가 commit 가능한지 read-only 검토 |
| 후보 B-commit: Profile Catalog Boost Commit Gate | review 통과 후 본 설계 문서 1건만 commit |
| 후보 B-push: Profile Catalog Boost Push Gate | commit 후 원격 보존 |
| 후보 B-impl-profile: Profile v0.2 Implementation Gate | `ee_agent_rule_profile_v0.2_draft.json` 신규 생성 |
| 후보 B-impl-instance: Instance v0.2 Implementation Gate | `policy_change_rules_v0.2_draft_instance.json` 신규 생성 |
| 후보 B-impl-run: Validator Run Gate (v0.2) | 신규 profile + instance로 validator 1회 실행 |

직전 흐름(작성 → review → commit → push) 패턴을 이어가면 후보 B-review가 가장 가까운 자연 후속.

본 설계 적용 순서 권장:
1. 본 설계 문서 review → commit → push (B-review·B-commit·B-push)
2. Profile v0.2 작성 (B-impl-profile)
3. Instance v0.2 작성 (B-impl-instance)
4. validator 1회 실행 검증 (B-impl-run)
5. 각 단계마다 review·commit·push

---

## 8. 아직 말하면 안 되는 claim

| # | 주장 (금지) |
|---|---|
| C1 | profile이 본 게이트에서 수정되었다는 주장 — 설계만, 0건 |
| C2 | schema가 본 게이트에서 수정되었다는 주장 — 0건 |
| C3 | instance가 본 게이트에서 수정되었다는 주장 — 0건 |
| C4 | validator가 본 게이트에서 수정되었다는 주장 — 0건 |
| C5 | validator가 v0.2 instance·profile로 통과한다는 주장 — 본 시점 v0.2 인스턴스 부재 |
| C6 | threshold 4종이 확정되었다는 주장 — Threshold 확정 Gate 별도 |
| C7 | L7 정책이 본 게이트로 결정되었다는 주장 — L7 Policy Decision Gate에서 부분 해소 (U9), 본 게이트와 독립 |
| C8 | governance·D-4 automation·input·generation·audit 중 어느 것이 본 게이트에서 진행되었다는 주장 — 0건 |
| C9 | `MAGNITUDE_DELTA` category가 모든 도메인에 적용 가능하다는 주장 — ee-agent profile 권장값, 다른 도메인은 별도 정책 |
| C10 | 신규 5 wrapper check가 도구 측에서 실제 구현되었다는 주장 — catalog 등록과 도구 구현은 분리 |
| C11 | U1·U2·U3·U4·U5·U6·U7·U8·U11이 본 게이트로 해소되었다는 주장 — 설계만, 적용은 별도 implementation gate |
| C12 | U9·U10이 본 게이트와 관련 있다는 주장 — 본 게이트 범위 외 (각각 L7 Policy·Threshold Gate 책임) |
| C13 | semantic correctness가 보장된다는 주장 — 본 설계는 형식·표현력 보강만, semantic 검증 아님 |
| C14 | 본 설계의 versioning plan(profile·instance 0.2-draft, schema 0.1-draft 유지)이 다른 도메인에도 적용된다는 주장 — ee-agent 권장값 |

---

## 9. Claim Boundary

| 단계 | 본 게이트가 주장 가능한 것 |
|---|---|
| (a) 직접 정의 | U1·U2 처리 전략(전략 A, MAGNITUDE_DELTA), U3·U5·U6·U7·U8 wrapper 5종 후보 명세, U4 runtime binding 전략(전략 B 옵션 B1), U11 instance revision 전략(전략 B), versioning plan, 영향 범위 |
| (b) 권장 초안 | wrapper 5종 parameters_schema, instance 갱신 예시, 신규 파일명 |
| (c) 미확정 | dynamic binding 객체 형식(`$dynamic` 키 등)의 세부 schema, cross-rule HumanReviewGuideline.id uniqueness, 도구 측 wrapper 실제 구현, magnitude category의 다른 도메인 적용 |

본 게이트는 (a)에 대해서만 설계 차원 정합성을 주장한다. (b)는 implementation gate가 별도 결정, (c)는 후속 단계.

---

## 10. 본 게이트에서 확정된 것과 미확정인 것

### 10.1 확정 사항

- U1·U2 → MAGNITUDE_DELTA category 추가 권장
- U3·U5·U6·U7·U8 → wrapper check 5종 추가 권장 (`evaluate_drift_origin`·`monitor_delta_no_action`·`trigger_full_diff_report`·`diagnose_data_debt_origin`·`inspect_recovery_path_origin`)
- U4 → profile parameters_schema 일부 type 완화 (전략 B 옵션 B1)
- U11 → instance revision에서 G1·G2·... id 부여 (rule-local uniqueness)
- versioning: profile·instance 0.2-draft 승급, schema 0.1-draft 유지, validator 0.1.0 유지
- 영향 범위: profile·instance 수정 / schema·validator 무변동

### 10.2 미확정 사항

- dynamic binding 객체 형식 (`$dynamic` 키 패턴 등) 세부
- cross-rule HumanReviewGuideline.id uniqueness 정책
- 도구 측 5 wrapper 실제 구현
- v0.2 profile·instance 실제 파일 작성 (별도 implementation gate)
- v0.2 validator 1회 실행 검증
- magnitude category의 다른 도메인 적용 (ee-agent 외)

---

## 11. 최종 상태

`READY_FOR_PROFILE_CATALOG_BOOST_REVIEW_GATE`
