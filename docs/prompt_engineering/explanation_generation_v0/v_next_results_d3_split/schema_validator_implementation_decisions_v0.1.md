# Schema Validator Implementation Decisions — v0.1

| 항목 | 값 |
|---|---|
| 상태 | DECISIONS_ONLY |
| 작성일 | 2026-05-28 |
| 본 문서 단계 | Schema Validator Implementation Pre-Decision Gate 산출물 |
| 후속 단계 후보 | READY_FOR_SCHEMA_VALIDATOR_IMPLEMENTATION_DECISION_REVIEW_GATE |
| 입력 design 문서 | `schema_validator_design_v0.1.md` (commit `a2f1240`) |

---

## 0. 본 게이트의 단일 목적과 범위

`schema_validator_design_v0.1.md`의 §10.2 미확정 사항과 §7.1 implementation gate 진입 전 결정 항목을 바탕으로, 후속 implementation gate가 임의로 결정해서는 안 되는 항목 13종을 확정하거나 명시적으로 보류한다.

본 문서는 **결정 문서**이며, validator 코드 작성·실행·구현 도입을 진행하지 않는다.

### 0.1 본 게이트에서 변경하지 않는 것

- validator 코드를 작성하지 않는다.
- `scripts/` 어떤 파일도 수정하지 않는다.
- 기존 schema·profile·design 4종 + validator design 1종 어떤 파일도 수정하지 않는다.
- 기존 `policy_change_rules.json`을 수정하지 않는다.
- v0.2 → v0.1-draft 마이그레이션을 실행하지 않는다.
- threshold를 확정하지 않는다.
- governance verdict를 적용하지 않는다.
- D-4 automation·input·generation·audit 어떤 도구도 실행하지 않는다.
- commit·push를 진행하지 않는다.

### 0.2 본 게이트가 결정하는 것

- 구현 언어
- validator 파일 경로 (생성은 별도 gate)
- 입력 파일 기본값
- 출력 방식
- 출력 JSON report 기본 구조
- exit decision 종류
- exit code mapping
- warning 등급 도입 여부
- P1~P6 도입 여부
- L7·L8 처리 방식 재명시
- reporter 분리 여부
- dependency 정책
- validator v0.1 검사 범위

---

## 1. 결정 항목 13종

각 항목은 `decision / rationale / deferred items` 형식으로 기록한다.

### 1.1 D-1 구현 언어

| 항목 | 내용 |
|---|---|
| decision | **Python** |
| rationale | repo `scripts/` 하위 도구가 Python 중심이며, JSON 검증·report 작성·CLI 인터페이스에 적합 |
| deferred items | Python 버전 하한선(예: `>=3.10`)은 implementation gate에서 repo 환경 확인 후 결정 |

### 1.2 D-2 validator 파일 경로

| 항목 | 내용 |
|---|---|
| decision | **`scripts/schema_validator.py`** |
| rationale | 기존 repo의 도구 위치 관례에 정합. 단일 파일로 시작하여 모듈 분할은 v0.2 이후 결정 |
| deferred items | 본 게이트에서 파일 생성하지 않음. validator implementation gate 산출물 |

### 1.3 D-3 입력 파일 기본값

| 입력 ID | 파일 | 필수 여부 | CLI flag (권장 초안) |
|---|---|---|---|
| I1 schema | `rule_schema_v0.1_draft.schema.json` (또는 동일 schema 파일) | 필수 | `--schema <path>` |
| I2 profile | `ee_agent_rule_profile_v0.1_draft.json` (또는 동일 profile 파일) | 필수 | `--profile <path>` |
| I3 rules instance | rules instance JSON (선택) | 선택 | `--rules <path>` |
| I4 change report | ChangeReport JSON (선택) | 선택 | `--change-report <path>` |

| 항목 | 내용 |
|---|---|
| decision | I1·I2 필수, I3·I4 선택 |
| rationale | design §1.1 호환성 매트릭스에 정합. I3·I4 부재 시 자동 skip |
| deferred items | CLI flag 이름(`--schema`·`--profile` 등)은 권장 초안. implementation gate에서 최종 명명 결정 |

### 1.4 D-4 출력 방식

| 항목 | 내용 |
|---|---|
| decision | **stdout summary + optional JSON report path** |
| rationale | 인간 가독 요약은 stdout, 도구 연동용 구조 결과는 선택 JSON 파일. design §2.4 "출력 형식 원칙"과 정합 |
| deferred items | stdout 포맷의 사람 가독 텍스트 구조는 implementation gate 결정 영역 |

### 1.5 D-5 출력 JSON report 기본 구조

| 항목 | 내용 |
|---|---|
| decision | root 7 키: `summary` / `errors` / `warnings` / `report_only` / `unresolved_policy_questions` / `skipped_checks` / `input_files` |
| rationale | design §2.1·§2.2 5섹션(+metadata)을 implementation 차원에서 확장. `skipped_checks`는 design §1.2·§2.1 skip 항목 명세. `input_files`는 design §2.4 input_file_hashes의 implementation 형식 |
| deferred items | 각 root 키의 세부 필드 schema(예: `errors[i]` 내부 필드)는 implementation gate에서 design §3 "실패 시 보고" 참고로 확정 |

#### 1.5.1 root 7 키 의미

| root 키 | 내용 |
|---|---|
| summary | total_checks·passed·failed·warned·report_only·skipped·exit_decision (design §2.2 validation_summary 매핑) |
| errors | L1~L6 error 항목 배열 |
| warnings | v0.1에서는 항상 빈 배열 (D-8 warning 미도입) |
| report_only | L7·L8 report_only 항목 배열 |
| unresolved_policy_questions | L7·L8 정책 미정의 항목 배열 (design §5.2 형식 준수) |
| skipped_checks | I3·I4 부재로 skip된 검사 ID 배열 |
| input_files | 각 입력 파일의 path + hash + 존재 여부 |

### 1.6 D-6 exit decision 종류

| 항목 | 내용 |
|---|---|
| decision | 4종: `pass` / `pass_with_warnings` / `pass_with_report_only` / `fail` (design §2.3 그대로) |
| rationale | design 명세를 implementation 차원에서 그대로 채택 |
| deferred items | v0.1에서는 `pass_with_warnings`가 실제 발생할 수 없음 (D-8 warning 0종). exit_decision 분기 자체는 유지하여 v0.2 호환 |

### 1.7 D-7 exit code mapping

| 항목 | 내용 |
|---|---|
| decision | `pass` / `pass_with_warnings` / `pass_with_report_only` → **0** / `fail` → **1** / tool·runtime error → **2** |
| rationale | UNIX 관례에 정합. report_only는 정책 미정의 관찰 기록이므로 종료 코드는 success. fail은 schema·profile contract 위반으로 1. validator 자체 실행 실패(JSON parse 실패·파일 부재 등)는 2로 분리하여 사용자가 "validator 실행 실패" 와 "검사 실패"를 구분 가능 |
| deferred items | tool error 세부 분기(예: file not found vs JSON parse error)는 implementation gate에서 결정. v0.1 단일 코드 2로 통합 |

### 1.8 D-8 warning 등급 도입 여부

| 항목 | 내용 |
|---|---|
| decision | **v0.1에서 도입하지 않음** |
| rationale | design §4.2에 "warning 등급을 명시 검사로 도입하지 않는 이유" 명시. v0.1은 error + report_only 중심. warning은 도메인 정책 결정 후 v0.2에서 도입 가능 영역 |
| deferred items | warning 트리거 조건·등급 매트릭스는 후속 도메인 정책 결정 gate에서 결정. v0.1 implementation의 `warnings` 배열은 항상 빈 배열로 발행 |

### 1.9 D-9 P1~P6 profile self-check 도입 여부

| 항목 | 내용 |
|---|---|
| decision | **v0.1 implementation에 도입하지 않음 (보류)** |
| rationale | design §8 "선택 영역으로 둔다" 명시. profile catalog 중복·required root 누락 등은 본 시점 profile 작성 단계에서 사람이 책임짐. P1~P6 도입은 별도 profile self-check gate로 분리 |
| 단 예외 | 다음 기본 검증은 v0.1 implementation의 사전 단계로 포함 가능 — (a) profile JSON parse 통과 / (b) profile root 키가 `ProfileContract.required_root_keys` 6종을 모두 포함 |
| deferred items | P1~P6 전체 도입은 별도 gate. 본 예외 2종은 implementation gate에서 도입 여부·등급 최종 결정 |

### 1.10 D-10 L7·L8 처리 방식

| 항목 | 내용 |
|---|---|
| decision | **v0.1에서 `report_only` 유지. hard fail 금지. `unresolved_policy_questions`에 기록** |
| rationale | design §3.7·§3.8·§4·§5·§10.1과 일관. L7·L8은 도메인 규약 미정의 상태로, validator가 결정을 강제하지 않음 |
| deferred items | L7·L8 정책 결정은 별도 L7·L8 Policy Decision Gate. validator 출력에는 옵션 후보(suggested_options) 형식으로 기록 |

### 1.11 D-11 reporter 분리 여부

| 항목 | 내용 |
|---|---|
| decision | **v0.1에서 단일 파일 구현. reporter 별도 분리 없음** |
| rationale | 도구 복잡도가 v0.1 단계에서 낮음. stdout summary 포맷과 JSON report 생성은 내부 헬퍼 함수로 분리하되, 별도 module·script로 분리하지 않음 |
| deferred items | reporter 분리는 v0.2 이후 필요 시 결정. v0.1 구현은 단일 `schema_validator.py`로 시작 |

### 1.12 D-12 dependency 정책

| 항목 | 내용 |
|---|---|
| decision | **Python standard library 우선. 외부 패키지 추가 금지. JSON Schema draft-07 full validation은 v0.1에서 직접 구현하지 않음** |
| rationale | v0.1은 최소 구조 검증 + cross-check 중심. `json`·`hashlib`·`argparse`·`pathlib`·`sys`·`typing` 등 stdlib만 사용. 외부 패키지(`jsonschema` 등) 추가는 dependency surface를 늘리고 v0.1 범위를 벗어남 |
| deferred items | (a) `jsonschema` 패키지가 repo에 이미 있더라도 본 게이트에서 dependency 추가 claim 금지. implementation gate에서 import 여부 결정. v0.1 권장은 미import. (b) JSON Schema draft-07 full validation은 v0.2 이후 도입 가능 영역. v0.1은 design §3에 명시된 cross-check만 수행 |

### 1.13 D-13 validator v0.1 검사 범위

| 영역 | 내용 |
|---|---|
| 포함 | (a) schema JSON parse / (b) profile JSON parse / (c) required root 존재 확인 (schema·profile 양쪽) / (d) `profile_metadata.compatible_schema_version`이 schema `schema_metadata.schema_version` const("0.1-draft")과 일치 / (e) profile `threshold_proposals.*.status`가 모두 "proposal" / (f) I3 rules instance가 주어진 경우 L1~L6 검사 / (g) L7·L8 report_only 생성 + unresolved_policy_questions 기록 |
| 제외 | (h) rules migration / (i) threshold 확정 / (j) governance verdict 적용 / (k) schema·profile·rules 파일 수정 / (l) D-4 automation 어떤 도구 실행 / (m) JSON Schema draft-07 full validation (D-12) / (n) P1·P2·P3 catalog 중복 검사 등 P1~P6 전체 (D-9) / (o) warning 등급 생성 (D-8) |

| 항목 | 내용 |
|---|---|
| decision | 위 포함 7종 + 제외 8종 |
| rationale | 포함 (a)·(b)·(c)는 input 파싱 단계. (d)·(e)는 profile-schema 일관성 기본 cross-check (P4·P5·P6 일부와 의도가 겹치지만 보안 차원 최소 검사로 분리). (f)는 design L1~L6의 정상 적용. (g)는 design L7·L8 처리 절차. 제외 항목은 D-8·D-9·D-12 결정과 design §6 F1~F7과 정합 |
| deferred items | 포함 (d)·(e)는 P4·P5·P6과 의도 중복. P1~P6 전체 도입 시 (d)·(e)를 P4·P5·P6으로 흡수할지는 별도 gate 결정 |

---

## 2. Implementation Gate 단일 목적 초안

본 결정 문서가 review·승인되면 후속 implementation gate가 다음 형식으로 진입 가능하다.

| 항목 | 초안 |
|---|---|
| 단일 목적 | `scripts/schema_validator.py` 1개 파일 작성. 본 결정 문서의 D-13 포함 7종 검사만 구현 |
| 변경 가능 영역 | `scripts/schema_validator.py` 신규 생성 1건만 |
| 절대 금지 | design 문서 §6의 F1~F7 7종 / D-13 제외 8종 / scripts 외 파일 수정 / 기존 schema·profile·design·decision 문서 수정 / dependency 추가 / D-4 automation 실행 / commit·push 본 단계에서 분리 결정 |
| 성공 판정 | (a) `scripts/schema_validator.py` 단일 파일 / (b) Python stdlib만 사용 / (c) D-13 포함 7종 검사 작동 / (d) D-6 exit decision 4종 / (e) D-7 exit code 매핑 (0·1·2) / (f) D-5 출력 JSON root 7 키 / (g) read-only 보장 (입력 파일·tracked 파일 변경 0) / (h) v0.1 implementation 단계에서 warning 0종·P1~P6 0종 |
| 실패 시 동작 | 입력 파일·tracked 파일 어떤 것도 수정하지 않고 종료. validator 자체 실행 실패는 exit code 2, 검사 fail은 결과 JSON의 `summary.exit_decision = fail` + exit code 1 |

### 2.1 Implementation Gate 금지 영역

| # | 금지 동작 | 근거 |
|---|---|---|
| F1 | threshold proposal 값 confirmed로 변경 | design §6 F1 |
| F2 | v0.2 rules → v0.1-draft migration 자동 수행 | design §6 F2 |
| F3 | governance verdict 인스턴스에 자동 적용 | design §6 F3 |
| F4 | rules instance 파일 수정 | design §6 F4 |
| F5 | profile 파일 수정 | design §6 F5 |
| F6 | schema 파일 수정 | design §6 F6 |
| F7 | D-4 automation 또는 인접 input·generation·audit 도구 실행 | design §6 F7 |
| D-13-제외 | (h)·(i)·(j)·(k)·(l)·(m)·(n)·(o) 8종 (본 결정 문서 §1.13) | 본 결정 문서 D-13 |

---

## 3. 재명시 (이전 단계와의 일관성 유지)

본 결정 문서는 다음 두 항목을 implementation gate에서 임의 변경 금지로 재명시한다.

### 3.1 L7·L8 hard fail 금지 재명시

- L7 priority_group ↔ severity 조합 정합성, L8 deprecation_signal ↔ verification_status 일관성은 v0.1에서 **report_only** 등급으로 유지한다.
- validator process는 L7·L8 발견 시 fail 종료하지 않는다.
- `unresolved_policy_questions`에 기록하여 후속 정책 결정 gate로 인계한다.
- design §3.7·§3.8·§4·§5·§10.1 + 본 결정 D-10과 일관.

### 3.2 P1~P6 v0.1 필수 구현 아님 재명시

- profile self-check P1~P6은 v0.1 implementation의 필수 범위가 아니다.
- design §8 "선택 영역" + 본 결정 D-9와 일관.
- 단 예외 2종 (a) profile JSON parse / (b) required root 6종 존재 확인은 D-13 포함 (c)에 흡수되어 사전 단계로 진행 가능.
- P1·P2·P3 catalog 중복 검사 등 전체 P1~P6 도입은 별도 profile self-check gate에서 결정.

---

## 4. 아직 말하면 안 되는 claim

본 결정 문서가 다음 주장을 포함하거나 implementation gate에서 발생시키면 안 된다.

| # | 주장 |
|---|---|
| C1 | validator가 작성·실행되었다는 주장 (본 게이트 구현 0) |
| C2 | threshold 4종이 본 게이트에서 확정되었다는 주장 (D-12·D-13 제외) |
| C3 | L7·L8 정책이 본 게이트에서 결정되었다는 주장 (D-10 유지) |
| C4 | v0.2 → v0.1-draft 마이그레이션이 본 게이트에서 진행되었다는 주장 (D-13 제외) |
| C5 | JSON Schema draft-07 full validation을 v0.1에서 보장한다는 주장 (D-12 제외) |
| C6 | P1~P6 전체가 v0.1에서 검증된다는 주장 (D-9 보류) |
| C7 | warning 등급으로 분류되는 항목이 v0.1에서 발생 가능하다는 주장 (D-8 도입 안 함) |
| C8 | implementation gate의 성공 판정이 본 문서로 확정되었다는 주장 (§2 초안만, 별도 review gate 필요) |
| C9 | validator가 D-4 automation 또는 governance 적용 기능을 가진다는 주장 (D-13 제외, design §6 F7) |
| C10 | `scripts/schema_validator.py`가 본 게이트에서 생성되었다는 주장 (D-2 path 명시만) |

---

## 5. Claim Boundary

| 단계 | 본 게이트가 주장 가능한 것 |
|---|---|
| (a) 직접 정의 | D-1 언어 (Python), D-4 출력 방식 (stdout + optional JSON), D-6 exit_decision 4종, D-7 exit code mapping, D-8 warning 미도입, D-9 P1~P6 보류, D-10 L7·L8 report_only 유지, D-11 단일 파일 구현, D-12 dependency 정책, D-13 포함 7종·제외 8종 |
| (b) 권장 초안 | D-2 파일 경로 (`scripts/schema_validator.py`), D-3 CLI flag 이름, D-5 root 7 키 |
| (c) 미확정 | Python 버전 하한선, stdout 포맷의 사람 가독 텍스트 구조, root 키 세부 필드 schema, P1~P6 도입 시 등급 매트릭스 |

본 게이트는 (a)에 대해서만 결정 효력을 주장한다. (b)는 implementation gate가 별도 결정 가능. (c)는 후속 단계에서 결정.

---

## 6. 본 게이트에서 확정된 것과 미확정인 것

### 6.1 확정 사항

- D-1 ~ D-13 13항 (각 항목의 decision 영역)
- L7·L8 hard fail 금지 재명시
- P1~P6 v0.1 필수 아님 재명시
- implementation gate 단일 목적 초안 + 금지 영역 F1~F7 + D-13 제외

### 6.2 미확정 사항

- Python 버전 하한선
- stdout 포맷의 사람 가독 텍스트 구조
- D-5 root 키 세부 필드 schema
- D-3 CLI flag 최종 명명
- D-7 tool·runtime error 세부 분기
- P1~P6 도입 시 등급 매트릭스
- L7·L8 정책 결정
- reporter 분리 (v0.2 이후)
- JSON Schema draft-07 full validation (v0.2 이후)
- warning 등급 트리거 정책 (v0.2 이후)

---

## 7. 후속 게이트 후보

| 후보 | 단일 목적 |
|---|---|
| 후보 D-review: Schema Validator Implementation Decision Review Gate | 본 결정 문서가 implementation gate 진입 가능한지 read-only review |
| 후보 D-commit: Schema Validator Implementation Decision Commit Gate | review 통과 후 본 결정 문서 1건만 commit |
| 후보 V-impl: Schema Validator Implementation Gate | `scripts/schema_validator.py` 작성 (review·commit 완료 후) |
| 후보 P-policy: L7·L8 Policy Decision Gate | unresolved_policy_questions 정책 결정 |
| 후보 R-migrate: Instance Migration Gate | v0.2 12 규칙 → v0.1-draft schema 인스턴스 변환 |

각 후보는 독립이다. 본 결정 문서는 후보 D-review·D-commit·V-impl 진입의 입력 자료다.

---

## 8. 최종 상태

`READY_FOR_SCHEMA_VALIDATOR_IMPLEMENTATION_DECISION_REVIEW_GATE`
