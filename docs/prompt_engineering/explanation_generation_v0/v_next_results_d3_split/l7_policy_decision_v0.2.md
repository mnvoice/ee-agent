# L7 Policy Decision — v0.2

| 항목 | 값 |
|---|---|
| 상태 | DECISION_ONLY |
| 작성일 | 2026-05-28 |
| 본 문서 단계 | L7 Policy Decision Gate v0.2 산출물 |
| 후속 단계 후보 | READY_FOR_L7_POLICY_V0_2_REVIEW_GATE |
| 적용 schema | `rule_schema_v0.1_draft.schema.json` (commit `ee2e515`) |
| 적용 profile | `ee_agent_rule_profile_v0.2_draft.json` (commit `0799544`) |
| 적용 instance | `policy_change_rules_v0.2_draft_instance.json` (commit `bfcdd67`) |
| 적용 validator | `scripts/schema_validator.py` v0.1.0 (commit `202b7a4`) |
| 관찰 입력 | `schema_validator_run_report_v0.2.json` (commit `9c7b6ae`) |
| 직전 정책 | `l7_policy_decision_v0.1.md` (commit `9e73be4`) |

---

## 0. 본 게이트의 단일 목적과 범위

`scripts/schema_validator.py`의 L7 검사(`Rule.priority_group` × `Verdict.severity` 조합)에 대한 v0.2 정책을 결정한다. v0.1 정책(`l7_policy_decision_v0.1.md`, commit `9e73be4`)의 결정 8 조합 분류 (6 allowed + 2 review_later)를 v0.2 validator run 결과 (commit `9c7b6ae`)에 비추어 재확인한다.

본 문서는 **정책 결정 문서**이며, validator·schema·profile·instance 어떤 파일도 수정하지 않는다.

### 0.1 본 게이트가 결정하는 것

- v0.2에서 L7 등급 유지 또는 변경 여부
- review_later 2 조합의 v0.2 처리 결정
- priority_group·severity 재배정 권고 여부
- disallowed 조합 신설 여부
- validator enforcement 도입 시점
- instance·profile·schema 수정 요구 여부
- U9 해소·부분 해소 결정

### 0.2 본 게이트가 변경하지 않는 것

- `scripts/schema_validator.py` 변경 없음
- `rule_schema_v0.1_draft.schema.json` / `ee_agent_rule_profile_v0.1_draft.json` / `ee_agent_rule_profile_v0.2_draft.json` / `policy_change_rules_v0.1_draft_instance.json` / `policy_change_rules_v0.2_draft_instance.json` 변경 없음
- validator 재실행 0회
- threshold 확정 0건
- governance·D-4 automation 진행 0건
- commit·push 진행 0건

---

## 1. v0.1 정책 (직전) 재요약

v0.1 L7 Policy Decision (`l7_policy_decision_v0.1.md`, commit `9e73be4`)의 결정:

- L7 등급: report_only (validator hard fail 금지)
- 8 조합 분류: **6 allowed + 2 review_later + 0 disallowed**
- review_later 2 조합:
  - (critical, INVESTIGATE) [R12]
  - (minor, INVESTIGATE) [R5·R9]
- 비공식 원칙 H1~H5 (profile 미등재)
- U9 부분 해소 (review_later 후속 결정 대기)

---

## 2. v0.2 validator run 관찰 정합

`schema_validator_run_report_v0.2.json` (commit `9c7b6ae`)의 L7 report_only 12건 분포:

| # | priority_group | severity | 매칭 rule (v0.2 instance) | rule 수 | v0.1 분류 |
|---|---|---|---|---|---|
| 1 | critical | HARD_ALERT | R8 | 1 | allowed |
| 2 | critical | INVESTIGATE | R12 | 1 | review_later |
| 3 | major | SUSPECT | R4, R6 | 2 | allowed |
| 4 | standard | INVESTIGATE | R1, R2 | 2 | allowed |
| 5 | standard | SOFT_ALERT | R3 | 1 | allowed |
| 6 | standard | IMPROVEMENT | R10, R11 | 2 | allowed |
| 7 | minor | INVESTIGATE | R5, R9 | 2 | review_later |
| 8 | minor | SOFT_ALERT | R7 | 1 | allowed |

8 조합 분포가 v0.1 정책과 100% 정합. priority_group·severity가 v0.1 instance → v0.2 instance 사이에 변경되지 않았음을 의미. v0.2 catalog 보강(MAGNITUDE_DELTA·wrapper 5종)은 category·function_id만 변경했고 priority·severity는 그대로 유지됨.

---

## 3. v0.2 결정 매트릭스

### 3.1 8 조합 결정 (v0.1과 비교)

| # | priority_group | severity | v0.1 분류 | v0.2 결정 | v0.1 → v0.2 변화 |
|---|---|---|---|---|---|
| 1 | critical | HARD_ALERT | allowed | **allowed** (유지) | 변화 없음 |
| 2 | critical | INVESTIGATE | review_later | **review_later** (유지) | 변화 없음 |
| 3 | major | SUSPECT | allowed | **allowed** (유지) | 변화 없음 |
| 4 | standard | INVESTIGATE | allowed | **allowed** (유지) | 변화 없음 |
| 5 | standard | SOFT_ALERT | allowed | **allowed** (유지) | 변화 없음 |
| 6 | standard | IMPROVEMENT | allowed | **allowed** (유지) | 변화 없음 |
| 7 | minor | INVESTIGATE | review_later | **review_later** (유지) | 변화 없음 |
| 8 | minor | SOFT_ALERT | allowed | **allowed** (유지) | 변화 없음 |

### 3.2 v0.2 결정 요약

- 8 조합 분류: **6 allowed + 2 review_later + 0 disallowed** (v0.1과 동일)
- review_later 2 조합 → **allowed 승격 안 함**
- review_later 2 조합 → **disallowed 신설 안 함**
- priority_group·severity 재배정 권고 → **권고하지 않음**

### 3.3 결정 사유

v0.2 validator run 1회 실행이 v0.1 정책 결정 시점의 관찰(L7 Policy Decision Gate v0.1, commit `9e73be4`)에 1회 운영 데이터를 추가했다. 그러나 다음 이유로 v0.1 결정을 변경하지 않는다.

- v0.2 validator run의 L7 12건은 v0.1 instance (12 rules) → v0.2 instance (12 rules) 사이 priority_group·severity 변경 0건임을 확인. 즉 v0.2 catalog 보강이 L7 관찰에 영향 0
- 1회 추가 관찰로 분류 변경의 다중 사례 누적 부족
- review_later 2 조합 (R12·R5·R9)의 의도성 검토는 도메인 정책 결정이며 본 게이트는 결정 권한 보류

---

## 4. v0.2 L7 Enforcement Decision

| 결정 항목 | v0.2 결정 |
|---|---|
| L7 등급 (v0.2) | **report_only** 유지 (v0.1과 동일) |
| validator hard fail 처리 | **금지** 유지 (v0.1과 동일) |
| review_later 조합 (#2, #7) 차단 | **차단하지 않음**. report_only로 관찰만 (v0.1과 동일) |
| allowed 조합 (6건) 처리 | report_only로 관찰만 (v0.1과 동일) |
| disallowed 조합 신설 | **하지 않음** (관찰 0건, v0.1과 동일) |
| validator enforcement 도입 시점 | **본 게이트 도입 안 함**. 별도 Validator Boundary Revision Gate 책임 |

### 4.1 사유

- v0.2 validator run으로 1회 운영 관찰이 누적되었으나 enforcement 도입 기준(다중 사례·도메인 정책 결정)에 미달
- enforcement는 scripts/schema_validator.py 코드 수정 필요 영역이며, 본 게이트는 정책 결정 문서만 작성하는 범위
- v0.1 정책 결정과 동일 원칙 유지로 schema-first 흐름의 일관성 보장

### 4.2 enforcement 후속 게이트 후보

- **Validator Boundary Revision Gate (v0.2)**: review_later 2 조합 영구 정책 확정 후 validator enforcement (warning·error 등급) 도입
- 진입 전 결정 영역: review_later 2 조합의 영구 분류, enforcement 등급 매트릭스, 도메인별 policy 매트릭스 등재 여부

---

## 5. Instance·Profile·Schema 수정 요구 여부

| 항목 | v0.2 결정 |
|---|---|
| `policy_change_rules_v0.2_draft_instance.json` 본 게이트 수정 | **수행하지 않음** |
| R12·R5·R9 priority_group 재배정 | **본 게이트 변경 없음** |
| `ee_agent_rule_profile_v0.2_draft.json` 본 게이트 수정 | **수행하지 않음** |
| `rule_schema_v0.1_draft.schema.json` 본 게이트 수정 | **수행하지 않음** |
| `scripts/schema_validator.py` 본 게이트 수정 | **수행하지 않음** |

### 5.1 instance 수정을 미루는 사유 (v0.1과 동일)

- review_later 분류는 "정합성 의문 있음 + 후속 결정 대기"이지 "즉시 수정 요구"가 아님
- instance 수정은 본 게이트의 변경 가능 영역 외 (decision 문서 1건만)
- v0.2 instance가 validator run cross-check를 통과한 시점에 priority·severity 재배정은 catalog와 무관한 영역

---

## 6. U9 해소 정도

| 항목 | v0.2 결정 |
|---|---|
| migration_log U9 (L7 정책 미정의) | **부분 해소 유지** (v0.1과 동일) |
| 완전 해소 시점 | 다중 도메인 사례 누적 또는 review_later 2 조합 영구 정책 결정 시 |
| 본 게이트 추가 진전 | v0.1 결정의 v0.2 validator run 정합 확인 (관찰 1라운드 누적) |

### 6.1 v0.1 → v0.2 부분 해소 진전

| 단계 | 누적 |
|---|---|
| v0.1 Policy Decision Gate (commit `9e73be4`) | 8 조합 1차 분류 (단일 사례, v0.2 12 rules 기반) |
| v0.2 Validator Run Gate (commit `9c7b6ae`) | 8 조합 form-level cross-check 확정 (validator audit으로 분포 재확인) |
| **본 게이트 (v0.2 Policy Decision)** | **8 조합 분류 1라운드 재확인** (변경 0건). U9 부분 해소 유지 |

---

## 7. U10 (Threshold 확정)과의 독립성

| 항목 | 상태 |
|---|---|
| U10 (threshold 4종 확정) | **본 게이트와 무관**. Threshold 확정 Gate 책임 |
| 본 게이트의 U10 관련 결정 | **0건** |
| L7 정책과 threshold의 영향 관계 | 독립. L7은 priority·severity 조합 분류, threshold는 magnitude 임계값. 분리 영역 |

본 게이트는 U10을 다루지 않는다.

---

## 8. v0.1 정책과 v0.2 정책의 차이

| 항목 | v0.1 정책 | v0.2 정책 | 차이 |
|---|---|---|---|
| L7 등급 | report_only | report_only | 동일 |
| hard fail 금지 | 명시 | 명시 | 동일 |
| 8 조합 분류 | 6 allowed + 2 review_later | 6 allowed + 2 review_later | 동일 |
| review_later 2 조합 | (critical, INVESTIGATE) [R12], (minor, INVESTIGATE) [R5·R9] | 동일 | 동일 |
| 비공식 원칙 H1~H5 | 명시, profile 미등재 | 본 게이트 추가 정의·등재 없음 (v0.1 가이드라인 유지) | 동일 |
| 누적 운영 관찰 | 0회 (정책 결정 시점) | 1회 (v0.2 validator run, commit `9c7b6ae`) | **v0.2에서 +1회 관찰 누적** |
| validator enforcement | 미도입 | 미도입 | 동일 |
| instance·schema·profile·validator 수정 | 0건 | 0건 | 동일 |

### 8.1 본질적 차이 1개

**v0.2의 새로운 점**: v0.2 catalog 보강 후에도 priority_group·severity 분포가 v0.1과 동일함을 validator run으로 form-level 확인. 즉 catalog 보강이 L7 정책 결정에 영향이 없음을 실측 확인.

이는 v0.1 정책 결정이 catalog 변경에 강건(robust)함을 1회 운영 관찰로 부분 확인한 셈이다. 단, 1회 관찰로 강건성을 결론짓지 않는다 (다중 사례 누적 영역).

---

## 9. Claim Boundary

| 단계 | 본 게이트가 주장 가능한 것 |
|---|---|
| (a) 직접 정의 | v0.2 L7 등급 (report_only 유지), 8 조합 분류 (v0.1과 동일 유지), v0.2 enforcement 결정 (도입 안 함), instance·schema·profile·validator 수정 결정 (없음), U9 부분 해소 유지 |
| (b) 비공식 가이드라인 | v0.1 정책의 비공식 원칙 H1~H5 그대로 유지 (재정의·재등재 없음) |
| (c) 미확정 | review_later 영구 정책, enforcement 도입 시점, profile 매트릭스 등재, 다중 사례 누적 후 재검토 |

본 게이트는 (a)에 대해서만 v0.2 정책 효력을 주장한다.

---

## 10. 아직 말하면 안 되는 claim

| # | 주장 (금지) |
|---|---|
| C1 | validator enforcement가 도입되었다는 주장 — 본 게이트 미도입 |
| C2 | scripts/schema_validator.py가 수정되었다는 주장 — 본 게이트 0건 |
| C3 | L7 정책이 운영 검증되었다는 주장 — 1회 validator run으로 부분 확인만 |
| C4 | semantic correctness가 본 결정으로 보장된다는 주장 — L7은 형식 분류, semantic 차원 아님 |
| C5 | threshold가 확정되었다는 주장 — 본 게이트 0건 |
| C6 | U10이 본 게이트로 해소되었다는 주장 — Threshold 확정 Gate 책임 |
| C7 | review_later 2 조합이 disallowed로 확정될 가능성이 결정되었다는 주장 — 후속 게이트 판단 영역 |
| C8 | 비공식 원칙 H1~H5가 본 게이트로 profile에 등재되었다는 주장 — 등재 0건 |
| C9 | instance·profile·schema가 본 결정으로 수정 필요하다는 주장 — 본 게이트 수정 없음 결정 |
| C10 | governance verdict·D-4 automation·input·generation·audit이 본 게이트에서 진행되었다는 주장 — 0건 |
| C11 | U9가 본 게이트로 완전 해소되었다는 주장 — 부분 해소 유지 (다중 사례 누적 필요) |
| C12 | 본 게이트가 후속 review·commit·push·revision gate를 자동 통과시킨다는 주장 — 각 후속 게이트의 독립 판단 |
| C13 | v0.2 정책이 다른 도메인(react-confidence·추천시스템)에 적용 가능하다는 주장 — ee-agent profile 한정 |

---

## 11. 본 게이트에서 확정된 것과 미확정인 것

### 11.1 확정 사항 (v0.2 한정)

- L7 등급 report_only 유지 (validator hard fail 금지)
- 8 조합 분류 v0.1과 동일 (6 allowed + 2 review_later + 0 disallowed)
- review_later 2 조합 즉시 disallowed 확정 안 함
- enforcement 본 게이트 미도입 (별도 Validator Boundary Revision Gate)
- instance·schema·profile·validator 본 게이트 수정 없음
- U9 부분 해소 유지 (v0.1과 동일)
- U10 본 게이트와 독립 (Threshold 확정 Gate 책임)
- 비공식 원칙 H1~H5 v0.1 가이드라인 그대로 유지

### 11.2 미확정 사항

- review_later 2 조합 영구 정책 (allowed 승격·priority/severity 재배정·disallowed 신설 중 어느 쪽인지)
- enforcement 도입 시점 (v0.3 또는 후속)
- profile에 priority×severity 허용 매트릭스 등록 여부
- 비공식 원칙 H1~H5의 영구 채택·등재 여부
- 다중 도메인 사례 누적 후 재검토 결과
- L7 정책의 다른 도메인 적용

---

## 12. 후속 게이트 후보

본 결정 문서가 review·승인되면 다음 후보가 자연 후속:

| 후보 | 단일 목적 |
|---|---|
| 후보 P-review v0.2: L7 Policy Decision v0.2 Review Gate | 본 결정 문서가 commit 가능한지 read-only 검토 |
| 후보 P-commit v0.2: L7 Policy Decision v0.2 Commit Gate | review 통과 후 본 결정 문서 1건 commit |
| 후보 P-push v0.2: L7 Policy Decision v0.2 Push Gate | commit 후 원격 보존 |
| 후보 T-confirm: Threshold 확정 Gate | U10 해소 (본 게이트와 독립) |
| 후보 V-revision: Validator Boundary Revision Gate (v0.2) | review_later 2 조합 영구 정책 확정 후 enforcement 도입 |
| 후보 R-multi-domain: Multi-Domain Profile Cross-Check Gate | L7 정책의 다른 도메인 적용 가능성 검토 |

직전 흐름(작성 → review → commit → push) 패턴을 이어가면 후보 P-review v0.2가 가장 가까운 자연 후속.

---

## 13. 최종 상태

`READY_FOR_L7_POLICY_V0_2_REVIEW_GATE`
