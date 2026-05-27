# L7 Policy Decision — v0.1

| 항목 | 값 |
|---|---|
| 상태 | DECISION_ONLY |
| 작성일 | 2026-05-28 |
| 본 문서 단계 | L7 Policy Decision Gate 산출물 |
| 후속 단계 후보 | READY_FOR_L7_POLICY_DECISION_REVIEW_GATE |
| 적용 schema | `rule_schema_v0.1_draft.schema.json` (commit `ee2e515`) |
| 적용 profile | `ee_agent_rule_profile_v0.1_draft.json` (commit `ee2e515`) |
| 적용 validator | `scripts/schema_validator.py` v0.1.0 (commit `202b7a4`) |
| 관찰 입력 | `policy_change_rules_validation_report_v0.1.json` (commit `411912a`) |

---

## 0. 본 게이트의 단일 목적과 범위

`scripts/schema_validator.py` v0.1의 L7 검사(`Rule.priority_group` × `Verdict.severity` 조합 정합성)에 대한 v0.1 정책을 결정한다. 본 문서는 **정책 결정 문서**이며, validator 코드·schema·profile·instance 어떤 파일도 수정하지 않는다.

### 0.1 본 게이트가 결정하는 것

- 관찰된 8 조합 각각에 대한 분류 (allowed / review_later / disallowed)
- v0.1 validator의 L7 등급 유지 또는 승격 여부
- priority_group과 severity 조합의 기본 원칙
- 향후 validator revision의 enforcement 여부
- migrated instance 12 rules의 즉시 수정 필요 여부

### 0.2 본 게이트가 변경하지 않는 것

- `scripts/schema_validator.py` 코드를 수정하지 않는다.
- `rule_schema_v0.1_draft.schema.json` / `ee_agent_rule_profile_v0.1_draft.json` / `policy_change_rules_v0.1_draft_instance.json` 어떤 파일도 수정하지 않는다.
- validator를 재실행하지 않는다.
- threshold를 확정하지 않는다.
- governance verdict를 적용하지 않는다.
- D-4 automation·input·generation·audit 어떤 도구도 실행하지 않는다.
- commit·push를 진행하지 않는다.

---

## 1. L7 검사의 정의 (재진술)

L7은 `scripts/schema_validator.py`의 `check_L7_L8`이 산출하는 검사 단위이다.

- 검사 대상: 각 rule의 (`priority_group`, `severity`) 조합
- 검사 방식: 도메인 규약 미정의이므로 통과 조건 강제 없음. 패턴 관찰 시 `report_only` 등급으로 기록
- 출력: `report_only` 배열의 `check_id=L7` 항목 + `unresolved_policy_questions` 배열의 L7 1건
- exit code 영향: `pass_with_report_only` (= exit code 0)

본 검사는 design 문서 §3.7과 implementation decision §1.10 (D-10)에 의해 hard fail이 금지된다.

---

## 2. v0.1-draft instance 관찰: 8 조합 12 보고

`policy_change_rules_validation_report_v0.1.json`이 기록한 12건의 L7 report_only 항목 분포:

| # | priority_group | severity | 매칭 rule | rule 수 | 의미 (rule 본질) |
|---|---|---|---|---|---|
| 1 | critical | HARD_ALERT | R8 | 1 | 변동 ≥ 10% → 자동 차단 |
| 2 | critical | INVESTIGATE | R12 | 1 | 도구 변경 → trigger_check |
| 3 | major | SUSPECT | R4, R6 | 2 | 정책 완화 의심 / broad keyword 의심 |
| 4 | standard | INVESTIGATE | R1, R2 | 2 | CLEAN→GAP / CLEAN→NEEDS_REVIEW 이동 |
| 5 | standard | SOFT_ALERT | R3 | 1 | CLEAN→CLEAN 라우팅 변화 |
| 6 | standard | IMPROVEMENT | R10, R11 | 2 | ambiguity 해소 / 회수 |
| 7 | minor | INVESTIGATE | R5, R9 | 2 | drift / data debt |
| 8 | minor | SOFT_ALERT | R7 | 1 | 변동 ≤ 5% → log_only |

총 12 보고 / 8 조합.

---

## 3. 각 조합별 v0.1 Decision

각 조합을 다음 3 분류 중 하나에 배정한다.

- **allowed**: v0.1에서 정합 조합으로 인정. validator가 report_only로만 기록하며 추가 행동 없음
- **review_later**: 정합성 의문 있음. v0.1에서는 차단·경고 없이 관찰 유지. 후속 게이트에서 재검토
- **disallowed**: 정합 위반. v0.1 또는 v0.2 enforcement 후보

### 3.1 결정 매트릭스

| # | priority_group | severity | decision | 사유 |
|---|---|---|---|---|
| 1 | critical | HARD_ALERT | allowed | priority와 severity가 모두 최고 단계. 자동 차단의 의도와 일관 |
| 2 | critical | INVESTIGATE | **review_later** | priority는 critical인데 severity는 중간 단계. 차단이 아닌 trigger_check로 분기되는 부분이 의도적인지 후속 검토 필요 |
| 3 | major | SUSPECT | allowed | 의심 단계의 일반적 조합. major priority + SUSPECT severity는 정합 |
| 4 | standard | INVESTIGATE | allowed | 정상 status 이동에서 INVESTIGATE는 정합 |
| 5 | standard | SOFT_ALERT | allowed | 라우팅 변화는 분류 유지이므로 SOFT_ALERT 정합 |
| 6 | standard | IMPROVEMENT | allowed | 정합한 개선 신호. log_only 처리 정합 |
| 7 | minor | INVESTIGATE | **review_later** | priority는 minor인데 severity는 중간 단계. 우선순위 낮은 영역에서 INVESTIGATE가 적절한지 후속 검토 필요 |
| 8 | minor | SOFT_ALERT | allowed | minor priority + SOFT_ALERT는 정합 |

### 3.2 review_later 2 조합 사유 상세

#### 3.2.1 (critical, INVESTIGATE) — R12

R12 (도구 자체 변경 감지)는 정책 변경과 도구 변경을 분리 추적해야 한다는 의도. priority가 critical인 이유는 "도구 변경은 정책 영향 측정 정확성을 좌우하므로 즉시 인지가 필요"하기 때문. 그러나 severity가 INVESTIGATE인 이유는 "도구 변경 자체는 잘못이 아니며 원인 분석이 필요할 뿐"이라는 것.

후속 검토 영역:
- critical은 본래 차단·즉시 검토 단계인데, INVESTIGATE는 차단을 의미하지 않음
- 본 조합이 의도적 분기(우선순위는 높지만 차단은 아님)인지, 또는 priority를 major로 강등해야 하는지 결정 필요

#### 3.2.2 (minor, INVESTIGATE) — R5·R9

R5 (GAP만 증가, drift)와 R9 (data debt)은 minor priority에 INVESTIGATE severity. minor는 본래 후순위 처리 영역인데, INVESTIGATE는 원인 분석 필요를 의미.

후속 검토 영역:
- minor 영역에서 INVESTIGATE가 발생하면 후순위 처리와 충돌
- priority를 standard로 승격할지, severity를 SOFT_ALERT로 강등할지 결정 필요
- 또는 정합 분기로 유지하되 처리 우선순위 명시 필요

### 3.3 disallowed 조합 0

본 시점 관찰된 8 조합 중 disallowed로 분류되는 조합은 없다. v0.2 12 rules에 disallowed 패턴이 부재함을 의미.

---

## 4. v0.1 Enforcement Decision

| 결정 항목 | v0.1 결정 |
|---|---|
| L7 등급 | **report_only** 유지 (변경 없음) |
| validator hard fail 처리 | **금지** 유지 |
| review_later 조합 (#2, #7) 차단 | **차단하지 않음**. report_only로 관찰만 |
| allowed 조합 (6건) 처리 | report_only로 관찰만 |
| disallowed 조합 등급 | 본 시점 0건 (미적용) |

### 4.1 사유

- v0.1은 schema-first 흐름의 첫 정착 단계이며, L7 정책이 운영 검증되지 않음
- 본 결정의 6 allowed + 2 review_later는 단일 사례(v0.2 12 rules)에서 도출된 관찰이며 다중 사례 누적 없음
- 본 시점에 enforcement(warning·error)로 승격하면 후속 변경 시 false fail 위험
- v0.1은 관찰·기록 단계로 유지하고, 다중 사례 누적 후 v0.2 이상에서 enforcement 결정 권장

---

## 5. Future Validator Revision 여부

| 항목 | 결정 |
|---|---|
| 본 게이트에서 validator 코드 수정 | **수행하지 않음** |
| 본 게이트에서 schema·profile 수정 | **수행하지 않음** |
| v0.1 validator의 L7 동작 변경 | **없음** (report_only 유지) |
| 후속 validator revision (v0.2 이후) 가능 영역 | (a) review_later 2 조합의 정책 확정 시 enforcement 도입 / (b) disallowed 패턴 추가 시 error 등급 부여 / (c) priority×severity 허용 매트릭스를 profile에 별도 필드로 등록 |

본 게이트는 후속 validator revision의 입력 자료를 생성한다. 구현·수정은 별도 게이트(예: Validator Boundary Revision Gate v0.2)의 책임이다.

---

## 6. Migrated Instance 수정 여부

| 항목 | 결정 |
|---|---|
| `policy_change_rules_v0.1_draft_instance.json` 본 게이트 수정 | **수행하지 않음** |
| review_later 조합을 가진 R12·R5·R9의 priority_group 변경 | **본 게이트 변경 없음** |
| review_later 조합 해소 책임 | 후속 review·decision 게이트 또는 v0.2 rules instance |
| migration_log unresolved U9 (L7 정책 미정의) 해소 여부 | **부분 해소** (8 조합의 v0.1 분류 결정) / **완전 해소 아님** (review_later 2건은 후속 결정 대기) |

### 6.1 instance 수정을 미루는 사유

- 본 게이트의 review_later 분류는 "정합성 의문 있음 + 후속 결정 대기"이지 "즉시 수정 요구"가 아니다.
- migrated instance를 수정하면 본 게이트가 instance·schema·validator 어느 한 쪽의 변경을 강제하게 되며, 이는 본 게이트의 변경 가능 영역(decision 문서 1건) 외부의 작업.
- 후속 게이트에서 review_later 정책 결정이 확정되면, 그 결과를 반영하는 별도 instance revision 게이트가 진입 가능.

---

## 7. priority_group × severity 조합의 기본 원칙 (참고)

본 게이트의 분류 결정을 도출하기 위해 다음 비공식 원칙을 사용했다. 이 원칙들은 v0.1 권고이며 profile·schema에 등재되지 않는다.

| 원칙 ID | 내용 |
|---|---|
| H1 | priority_group과 severity가 모두 최고 단계(`critical` + `HARD_ALERT`)이면 자동 차단 의도 정합 |
| H2 | priority_group과 severity가 한 단계 차이는 일반적으로 정합 (예: standard+INVESTIGATE) |
| H3 | priority_group과 severity의 차이가 2단계 이상이면 의도성 검토 필요 (예: critical+INVESTIGATE, minor+INVESTIGATE는 review_later) |
| H4 | severity=IMPROVEMENT는 어떤 priority_group과도 결합 가능 (정합 신호이므로) |
| H5 | severity=HARD_ALERT는 priority_group=critical과만 결합 권장 (자동 차단 단계 일치) |

### 7.1 본 원칙의 한계

- H1~H5는 본 게이트에서 도출된 비공식 원칙. 본 게이트는 이를 schema·profile에 enforcement 항목으로 등록하지 않는다.
- 다중 사례 누적 없이는 원칙 자체가 over-fit 위험. 본 원칙은 v0.1 시점 1차 가이드라인이지 영구 규약이 아니다.
- 향후 enforcement 도입 시 본 원칙을 그대로 채택할지 별도 결정 영역.

---

## 8. 본 게이트에서 확정된 것과 미확정인 것

### 8.1 확정 사항 (v0.1 한정)

- L7 등급은 v0.1에서 `report_only` 유지
- 관찰 8 조합 중 6 allowed + 2 review_later + 0 disallowed
- review_later 2 조합: (critical, INVESTIGATE) [R12], (minor, INVESTIGATE) [R5·R9]
- 본 결정으로 validator·schema·profile·instance 수정 없음
- migration_log unresolved U9 부분 해소 (전체 해소 아님)
- 비공식 원칙 H1~H5 (v0.1 가이드라인, profile 미등재)

### 8.2 미확정 사항

- review_later 2 조합의 영구 정책 (allowed 승격·priority_group 재배정·severity 재배정 중 어느 쪽인지)
- enforcement 도입 시점 (v0.2 또는 후속)
- profile에 priority×severity 허용 매트릭스 등록 여부
- 비공식 원칙 H1~H5의 영구 채택 여부
- 다중 사례(v0.2 외 도메인) 누적 후 분류 재검토 결과

---

## 9. Claim Boundary

| 단계 | 본 게이트가 주장 가능한 것 |
|---|---|
| (a) 직접 정의 | v0.1 L7 등급(report_only 유지), 8 조합 분류(6 allowed + 2 review_later), v0.1 enforcement 결정(차단 없음), instance 수정 결정(없음), validator 수정 결정(없음) |
| (b) 비공식 가이드라인 | 원칙 H1~H5 (v0.1 시점 1차 가이드라인, profile 미등재) |
| (c) 미확정 | review_later 영구 정책, enforcement 도입 시점, profile 매트릭스 등록, 다중 사례 누적 후 재검토 결과 |

본 게이트는 (a)에 대해서만 v0.1 정책 효력을 주장한다. (b)는 권고 차원, (c)는 후속 게이트의 판단.

---

## 10. 아직 말하면 안 되는 claim

| # | 주장 (금지) |
|---|---|
| C1 | validator 수정이 완료되었다는 주장 — 본 게이트 0건 |
| C2 | scripts/schema_validator.py가 L7 enforcement로 승격되었다는 주장 — v0.1 report_only 유지 |
| C3 | schema·profile에 priority×severity 허용 매트릭스가 등록되었다는 주장 — 미등재 |
| C4 | profile catalog boost가 본 게이트에서 진행되었다는 주장 — Profile Catalog Boost Gate 별도 |
| C5 | threshold가 확정되었다는 주장 — 본 게이트 0건 |
| C6 | governance verdict가 인스턴스에 적용되었다는 주장 — 본 게이트 0건 |
| C7 | D-4 automation이 실행되었다는 주장 — 본 게이트 0건 |
| C8 | rules의 semantic correctness가 본 결정으로 보장된다는 주장 — L7은 형식 분류, semantic 차원 아님 |
| C9 | review_later 2 조합이 disallowed로 확정될 가능성이 있다는 주장 — 후속 게이트의 판단이며 현 시점 disallowed 0 |
| C10 | 비공식 원칙 H1~H5가 영구 규약이라는 주장 — v0.1 가이드라인, profile 미등재 |
| C11 | migrated instance가 본 결정으로 수정 필요하다는 주장 — 본 게이트는 instance 수정 없음으로 결정 |
| C12 | 본 게이트가 후속 review·commit·push gate를 자동 통과시킨다는 주장 — 각 후속 게이트의 독립 판단 |

---

## 11. 후속 게이트 후보

본 결정 문서가 review·승인되면 다음 후보가 자연 후속:

| 후보 | 단일 목적 |
|---|---|
| 후보 P-review: L7 Policy Decision Review Gate | 본 결정 문서가 commit 가능한 정책 문서인지 read-only 검토 |
| 후보 P-commit: L7 Policy Decision Commit Gate | review 통과 후 본 결정 문서 1건만 commit |
| 후보 P-push: L7 Policy Decision Push Gate | commit 후 원격 보존 |
| 후보 W-profile-boost: Profile Catalog Boost Gate | U3·U6·U7·U8 wrapper + magnitude category 보강 (본 게이트와 독립) |
| 후보 T-confirm: Threshold 확정 Gate | profile.threshold_proposals 4종 확정 (본 게이트와 독립) |
| 후보 V-revision: Validator Boundary Revision Gate (v0.2 후보) | review_later 2 조합 정책 확정 후 validator enforcement 도입 |

직전 흐름(작성 → review → commit → push) 패턴을 이어가면 후보 P-review가 가장 가까운 자연 후속.

---

## 12. 최종 상태

`READY_FOR_L7_POLICY_DECISION_REVIEW_GATE`
