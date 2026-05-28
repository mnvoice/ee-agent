# Dynamic Binding Spec v0.1

작성일: 2026-05-28
Gate: Dynamic Binding Spec Gate
분류: **Spec 문서 (의미 계약 정의)**. Enforcement 문서가 아니다.

## 1. Meta

- 본 문서는 `$dynamic` 바인딩의 **의미 계약(meaning contract)**을 정의하는 Dynamic Binding Spec v0.1이다.
- 본 문서는 Spec only이다. validator 동작 규정, 도구 측 runtime 해소 구현, schema/profile/instance 반영은 본 문서의 책임이 아니다.
- 본 문서는 신규 markdown 1건 추가에 한정한다. 기존 schema/profile/instance/naming 문서는 수정하지 않는다.
- 본 문서는 token rename, R9 instance token 교체, F2/F5 Naming Drift 해결, Threshold/L7 결정을 수행하지 않는다. 해당 항목은 §8 Routed Follow-ups로 후속 gate에 위임한다.
- 감독관 보정안(Claude Web 외부 검토 + 감독관 보정) 반영: `$dynamic`을 flat token registry가 아닌 **source-scoped binding contract**로 정의한다.

근거 출처:
- (a) `policy_change_rules_v0.2_draft_instance.json` (rules_count 12, `$dynamic` 실사용 3건)
- (a) `ee_agent_rule_profile_v0.2_draft.json` (wrapper parameters_schema, line 420 `$dynamic` 키 패턴 세부를 not_validated로 명시)
- (a) `rule_schema_v0.1_draft.schema.json` (AutomatedCheckCall.parameters를 `type: object`로만 강제, `$dynamic` 키 형식 미강제)
- (a) `policy_change_rules_v0.2_acceptance_review.md` (F3/F4 → 본 gate routing)
- (a) `schema_validator_run_report_v0.2.md` C2/C3 (형식 차원만 cross-check, runtime 해소·semantic correctness 유보)

## 2. Scope / Non-goals

### Scope (본 문서가 정의하는 것)

- `$dynamic` 바인딩의 source 모델 (source classes)
- R6 / R9 / R11 각 바인딩의 source-scoped contract (source, context, referent, type, cardinality, domain scope, failure mode)
- 전역 failure mode 정책 (token-specific 예외 이전의 default)
- token name(도메인 종속) vs source mechanism(도메인 무관)의 domain scope split

### Non-goals (본 문서가 하지 않는 것)

- schema 수정 — 금지
- profile 수정 — 금지
- instance 수정 — 금지
- validator 실행 / 구현 / 수정 — 금지
- profile `parameters_schema`에 `$dynamic` 패턴 반영 — 금지
- token rename — 금지
- R9 instance token 교체 — 금지
- F2/F5 Naming Drift 해결 — 금지
- Threshold / MVP / L7 결정 — 금지
- DEVLOG / Vault / MEMORY / decision JSONL 작성 — 금지
- commit / push — 금지

## 3. Problem Statement

### 3.1 현 상태 (a) 사실

v0.2 instance가 `$dynamic` 객체 3건에 의존한다.

| rule | 위치 | 사용 형태 |
|---|---|---|
| R6 | instance:284 | `automated_check.parameters.item = {"$dynamic": "predicate_dominant_item"}` |
| R9 | instance:408 | `automated_check.parameters.item = {"$dynamic": "predicate_dominant_item"}` |
| R11 | instance:491 | `automated_check.parameters.pid = {"$dynamic": "current_pid"}` |

- schema는 `AutomatedCheckCall.parameters`를 `type: object`로만 강제하고 `$dynamic` 키 형식을 강제하지 않는다 (cross-check는 validator gate 책임).
- profile은 wrapper의 `item`/`pid` type을 `[string, object]`로 완화해 객체 전달을 허용하나, line 420에서 "dynamic binding 객체 형식(`$dynamic` 키 패턴 등) 세부 정의"를 `not_validated_in_this_gate`로 명시한다.
- validator v0.2는 U4/U7/U8(R6/R9/R11 객체)의 **형식 차원**만 L6 pass로 확정했고, C2로 "runtime 정확 해소는 도구 측 책임", C3로 "semantic correctness는 검증 범위 밖"을 명시했다.

즉 **형식은 이미 닫혀 있고, 의미 계약이 비어 있다.** 본 gate가 채우는 것은 형식이 아니라 의미다.

### 3.2 flat token registry가 위험한 이유

`$dynamic` 토큰을 "전역 이름 → 값"의 flat dictionary로 정의하면 다음 문제가 발생한다.

- 같은 토큰 이름 `predicate_dominant_item`이 R6와 R9에서 공유되나, 두 rule의 predicate가 다르다. R6의 predicate는 `item_concentration_pct`(dominant item을 산출), R9의 predicate는 `zero_hit_items`(dominant item을 자연스럽게 산출하지 않음).
- flat registry는 "이 토큰의 의미는 무엇인가"를 토큰 이름만으로 답하려 한다. 그러나 R9에서는 그 이름이 가리키는 referent가 source context와 어긋난다 (F4).
- 따라서 의미를 토큰 이름이 아니라 **source context에 종속**시켜야 한다. 이것이 source-scoped binding contract의 핵심이다.

## 4. Source Model

`$dynamic` 바인딩 값의 출처(source)를 class로 구분한다. binding의 의미는 토큰 이름이 아니라 source class + context로 결정된다.

### 4.1 predicate-sourced binding

- predicate evaluation의 결과가 binding 값을 산출한다.
- 예: R6의 `item_concentration_pct`는 평가 과정에서 dominant item을 산출할 수 있다. 그 dominant item이 binding 값이 된다.
- 적합 조건: predicate가 해당 referent를 자연스럽게 산출할 때만 predicate-sourced로 정합하다.

### 4.2 invocation-sourced binding

- check invocation context가 binding 값을 제공한다. predicate 결과가 아니라 호출 시점의 context에서 온다.
- 예: R11의 `current_pid`는 `inspect_recovery_path_origin` 호출 시점의 pid context에서 온다.

### 4.3 source-scoped contract 원칙

- 모든 `$dynamic` 바인딩은 (source class, source context, referent, type, cardinality, domain scope, failure mode)의 7요소 계약으로 기술된다.
- 동일 토큰 이름이라도 source context가 다르면 별개의 계약으로 본다.
- source mechanism(predicate-sourced / invocation-sourced)은 도메인 무관이다. token name은 도메인 종속이다 (§7 참조).

## 5. Binding Inventory

각 바인딩을 source-scoped contract로 기술한다.

### 5.1 R6 binding

| 요소 | 값 |
|---|---|
| current use | `{"$dynamic": "predicate_dominant_item"}` (parameters.item) |
| source class | predicate-sourced |
| predicate context | `item_concentration_pct` (args min_pct: 60) |
| check context | `list_top_matching_keywords_for_item` (top_n: 10) |
| referent | concentration evaluation에서 산출된 dominant item |
| type | item identifier |
| cardinality | single |
| domain scope | token name `predicate_dominant_item`은 ee-agent/item-policy 종속. source mechanism(predicate-sourced)은 도메인 무관 |
| 적합성 | 정합. predicate가 dominant item을 자연스럽게 산출하므로 predicate-sourced + single referent가 일치 |

### 5.2 R9 binding

| 요소 | 값 |
|---|---|
| current use | `{"$dynamic": "predicate_dominant_item"}` (parameters.item) |
| source class | 현 토큰 이름은 predicate-sourced를 시사하나, predicate context가 산출 의미와 어긋남 |
| predicate context | `zero_hit_items` (args at_least: 1) |
| check context | `diagnose_data_debt_origin` (item dynamic 허용) |
| referent (현 토큰 기준) | single dominant item — **부적합** |
| referent (본 spec 계약) | **zero-hit item의 list/set** (단일 dominant item이 아님) |
| type | item identifier 집합 |
| cardinality | **list/set** (단일 아님) |
| domain scope | token name `predicate_dominant_item`은 ee-agent/D-3 종속. source mechanism은 도메인 무관 |
| 적합성 | **부적합 (F4 확정)**. `zero_hit_items` predicate는 dominant item을 자연스럽게 산출하지 않는다. 현 토큰 이름은 semantic misfit 가능성이 높다 |

R9 결정 경계:
- **본 spec에서 허용하는 결정**: R9의 referent는 single dominant item이 아니라 **list/set referent**여야 한다는 의미 계약을 확정한다.
- **본 spec에서 허용하지 않는 결정**: token rename, R9 instance token 교체, profile/schema 반영. → §8로 라우팅 (Naming Drift Gate / Enforcement Gate).

### 5.3 R11 binding

| 요소 | 값 |
|---|---|
| current use | `{"$dynamic": "current_pid"}` (parameters.pid) |
| source class | invocation-sourced |
| predicate context | `status_movement` (from GAP, to [CLEAN, NEEDS_REVIEW]) — 단 binding 값의 출처는 아님 |
| check context | `inspect_recovery_path_origin` (pid dynamic 허용) |
| referent | check invocation 시점의 current pid |
| type | pid identifier |
| cardinality | single |
| domain scope | token name `current_pid`은 ee-agent/D-3 종속. source mechanism(invocation-sourced)은 도메인 무관 |
| 적합성 | 정합 (조건부). 후속 validator 설계가 predicate-sourced임을 증명하기 전까지는 invocation-sourced로 본다 |

R11 추가 계약:
- pid context가 없을 때(missing)는 **binding resolution error / invalid invocation**으로 처리한다. **silent skip 금지** (§6 정책과 일치).

## 6. Global Failure Mode Policy

token-specific 예외 이전에 전역 default를 먼저 정의한다. 핵심 원칙: **skip / human_review를 default failure mode로 쓰지 않는다.** 이들은 rule/spec 결함을 은폐한다.

| 실패 상황 | 전역 default 처리 |
|---|---|
| unknown dynamic token (정의되지 않은 토큰) | `invalid_rule` |
| cardinality mismatch — single 기대 위치에 list 산출 | `invalid_rule` |
| ambiguous value — single 기대 위치에 모호한 다수 값 | `invalid_rule` |
| missing required invocation context | `invalid_invocation` 또는 `binding_resolution_error` |
| missing optional binding | spec이 해당 토큰을 명시적으로 optional로 표기한 경우에만 허용 |

- 위 처리는 의미 계약 차원의 분류이며, 도구/validator의 실제 동작 규정이 아니다 (Enforcement 아님).
- optional 표기가 없는 binding의 missing은 optional이 아니다 — required로 간주하고 위 표의 missing required 행을 적용한다.

## 7. Decisions

본 gate가 확정하는 의미 계약 결정.

1. **Flat token registry 금지.** `$dynamic` 토큰은 전역 이름만으로 의미가 결정되지 않는다. binding 의미는 source context에 종속된다.
2. **source-scoped binding 채택.** 모든 binding은 (source class, source context, referent, type, cardinality, domain scope, failure mode) 계약으로 기술된다.
3. **source classes 최소 2종으로 시작.** predicate-sourced, invocation-sourced.
4. **R6**: predicate-sourced, single dominant item contract. 정합.
5. **R9**: referent는 **list/set**여야 한다 (single dominant item 아님). 현 토큰 이름은 semantic misfit. token rename / instance 교체는 본 gate 밖.
6. **R11**: invocation-sourced, single current_pid. pid missing은 binding resolution error / invalid invocation (silent skip 아님).
7. **domain scope split**: token name(`predicate_dominant_item`, `current_pid`)은 ee-agent/D-3 종속. source mechanism(predicate-sourced, invocation-sourced)은 도메인 무관. 이 split은 후속 Naming Revision v0.2 Drift Gate의 입력이 된다.
8. **failure mode default**: skip/human_review를 default로 쓰지 않는다 (결함 은폐 방지).

## 8. Observations / Routed Follow-ups

본 gate는 아래 항목을 해결하지 않고 후속 gate로 라우팅한다.

| 항목 | routing |
|---|---|
| R9 token name misfit (`predicate_dominant_item` → 적합 이름) | Naming Drift Gate (Naming Revision v0.2) |
| R9 instance token 교체 (instance 실제 변경) | Enforcement Gate |
| token name vs source mechanism domain scope split | Naming Revision v0.2 Drift Gate (F2/F5 입력) |
| `$dynamic` 형식의 profile/schema 형식화 (parameters_schema 반영) | Profile / Schema Promotion Gate |
| validator의 `$dynamic` 의미 검증 동작 | Validator Boundary / Run Gate |
| Threshold / L7 / MVP 결정 | 각 Threshold 확정 Gate / L7 Policy Decision Gate |

## 9. Claim Boundary

본 문서가 주장하는 것:
- `$dynamic`의 의미 계약(source-scoped binding contract)을 정의한다.
- R6/R9/R11 각 binding의 source, referent, cardinality, failure mode를 기술한다.
- 전역 failure mode default 정책을 정의한다.
- token name(도메인 종속) vs source mechanism(도메인 무관) split을 명시한다.

본 문서가 주장하지 않는 것:
- asset(schema/profile/instance) 변경 — 0건.
- validator 지원 / runtime 해소 정확성 — 주장 안 함 (도구 측 책임, C2/C3와 정합).
- token rename / R9 instance token 교체 — 수행 안 함.
- F2/F5 / L7 / Threshold 해소 — 수행 안 함.
- rules semantic correctness 보장 — 본 문서는 binding 의미 계약만 정의, rule 전체의 의미 정합 보장 아님.

## 10. Success Criteria Self-check

- 신규 markdown 1건만 추가: 본 문서 (`dynamic_binding_spec_v0.1.md`).
- 기존 파일 수정: 0.
- staged: 0.
- commit / push: 0.
- forbidden actions (schema·profile·instance·validator·naming 수정, profile에 `$dynamic` 반영, token rename, R9 instance token 교체, F2/F5/L7/Threshold 결정, DEVLOG/Vault/MEMORY/decision JSONL 작성, commit/push): 0.

다음 자연 후보: 사용자 승인 시 §8 routing 중 1건. 본 gate는 spec 정의만 완료하고 후속 gate는 시작하지 않는다.
