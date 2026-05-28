# Threshold Confirmation Decision — v0.1

| 항목 | 값 |
|---|---|
| 상태 | DECISION_ONLY |
| 작성일 | 2026-05-28 |
| 본 문서 단계 | Threshold Confirmation Decision Gate 산출물 |
| 후속 단계 후보 | READY_FOR_THRESHOLD_CONFIRMATION_REVIEW_GATE |
| 적용 profile | `ee_agent_rule_profile_v0.2_draft.json` (commit `0799544`) |
| 적용 instance | `policy_change_rules_v0.2_draft_instance.json` (commit `bfcdd67`) |
| 관찰 validator audit | `schema_validator_run_report_v0.2.json` (commit `9c7b6ae`) |
| 대상 unresolved | U10 (threshold 4종 확정) |

---

## 0. 본 게이트의 단일 목적과 범위

profile v0.2의 `threshold_proposals` 4종 (값 60·5·10·2) 각각에 대해 **confirmed / proposal 유지 / deferred** 중 하나를 판정한다.

본 문서는 **정책 결정 문서**이며 profile·schema·instance·validator 어떤 파일도 수정하지 않는다.

### 0.1 본 게이트가 결정하는 것

- 4종 threshold 각각의 v0.1 판정 (confirmed / proposal / deferred)
- confirmed 판단 기준
- 단일 사례 기반 한계 명시
- 추가 관찰 필요 항목 식별
- profile v0.2 직접 수정 또는 v0.3 신규 작성 분리 결정
- U10 해소 정도

### 0.2 본 게이트가 변경하지 않는 것

- `ee_agent_rule_profile_v0.2_draft.json`을 수정하지 않는다.
- `rule_schema_v0.1_draft.schema.json`을 수정하지 않는다.
- `policy_change_rules_v0.2_draft_instance.json`을 수정하지 않는다.
- `scripts/schema_validator.py`를 수정하지 않는다.
- validator를 재실행하지 않는다.
- L7 enforcement를 도입하지 않는다.
- governance·D-4 automation을 진행하지 않는다.
- commit·push를 진행하지 않는다.

---

## 1. 명명 차이 사전 보고

본 게이트 인계 메시지의 threshold 명명과 profile v0.2 실제 명명이 다르다. **값(60·5·10·2)은 일치**하지만 **키 이름이 다르다**.

| 인계 메시지 명명 | profile v0.2 실제 명명 (정본) | 값 |
|---|---|---|
| `first_order_missing_item_delta_ratio` | `broad_item_concentration_pct` | 60 |
| `broad_keyword_min_count` | `soft_alert_max_delta_pct` | 5 |
| `excessive_predicate_count` | `hard_alert_min_delta_pct` | 10 |
| `recovery_path_min_count` | `multi_word_min_length` | 2 |

본 결정은 **profile v0.2 실제 명명을 정본**으로 사용한다. 인계 메시지의 명명 차이는 명명 재검토 필요성을 시사하나, 본 게이트의 단일 목적 (confirmed 판정) 범위 외이다. 명명 재정렬은 별도 Profile Naming Revision Gate의 책임으로 분리한다.

---

## 2. 4종 Threshold 현 상태 (profile v0.2 정본)

| ID | 이름 (정본) | 값 | rationale | proposal_source |
|---|---|---|---|---|
| T1 | `broad_item_concentration_pct` | 60 | D-3 단일 item 흡수 패턴 관찰값. 도메인 출제 비중 큰 영역이면 정합일 수 있음. 확정 검증 없음. | human suggestion, 2026-05-27 |
| T2 | `soft_alert_max_delta_pct` | 5 | 초기 임계값. 380 entry 풀 전수 검증 없음. | initial heuristic, 2026-05-27 |
| T3 | `hard_alert_min_delta_pct` | 10 | 초기 임계값. 380 entry 풀 전수 검증 없음. | initial heuristic, 2026-05-27 |
| T4 | `multi_word_min_length` | 2 | multi-word keyword 최소 단어 수. D-3 split 정책 기반. | D-3 policy observation, 2026-05-27 |

---

## 3. Confirmed 판단 기준

본 게이트는 다음 5 기준을 사용하여 confirmed 승격 가능 여부를 판정한다.

| 기준 ID | 기준 |
|---|---|
| K1 | 다중 사례 누적 (최소 3 도메인 또는 3 데이터셋에서 동일 임계값 관찰) |
| K2 | 정량 검증 (특정 임계값이 운영 환경에서 false positive·false negative 비율을 미리 정의된 한도 안에 유지) |
| K3 | 도메인 정의에 직접 연결 (의미 차원에서 자명한 정의이거나 외부 표준 참조) |
| K4 | 변동량 임계값의 경우: 운영 1라운드 이상의 측정 데이터로 임계값 적정성 확인 |
| K5 | confirmed 시 instance·profile downstream에 미치는 영향이 명확히 파악됨 |

본 게이트의 confirmed 승격은 **K1 또는 K3 충족 + K5 충족**을 최소 조건으로 한다.

---

## 4. 4종 Threshold 각각의 v0.1 판정

### 4.1 T1 `broad_item_concentration_pct = 60`

| 항목 | 평가 |
|---|---|
| 출처 | D-3 단일 item 흡수 패턴 1회 관찰 (가공전선 사례) |
| K1 다중 사례 | **미충족** (1회 관찰만) |
| K2 정량 검증 | **미충족** (false positive·false negative 측정 없음) |
| K3 도메인 정의 직접 연결 | **미충족** (단일 사례 기반 heuristic) |
| K4 운영 1라운드 측정 | **미충족** |
| K5 downstream 영향 | 부분 충족 (instance R6에서 사용 중, 단 명시적 영향 측정 없음) |
| **판정** | **proposal 유지** + 추가 관찰 필요 |
| 사유 | D-3 단일 사례만으로 60% 임계값을 confirmed로 승격하는 것은 over-fit 위험. 다른 도메인·데이터셋에서 동일 임계값이 정합인지 다중 사례 누적 필요 |

### 4.2 T2 `soft_alert_max_delta_pct = 5`

| 항목 | 평가 |
|---|---|
| 출처 | 초기 heuristic, 380 entry 풀 전수 검증 없음 |
| K1 다중 사례 | **미충족** |
| K2 정량 검증 | **미충족** (380 entry 검증 0회) |
| K3 도메인 정의 직접 연결 | **미충족** (초기 추측) |
| K4 운영 1라운드 측정 | **미충족** |
| K5 downstream 영향 | 부분 충족 (instance R7에서 사용 중) |
| **판정** | **proposal 유지** + 추가 관찰 필요 |
| 사유 | 초기 추측 단계의 5% 임계값을 confirmed로 승격하는 것은 검증 없는 확정으로 위험. 380 entry 전수 검증 또는 운영 1라운드 측정 필요 |

### 4.3 T3 `hard_alert_min_delta_pct = 10`

| 항목 | 평가 |
|---|---|
| 출처 | 초기 heuristic, 380 entry 풀 전수 검증 없음 |
| K1 다중 사례 | **미충족** |
| K2 정량 검증 | **미충족** |
| K3 도메인 정의 직접 연결 | **미충족** (초기 추측) |
| K4 운영 1라운드 측정 | **미충족** |
| K5 downstream 영향 | 부분 충족 (instance R8에서 사용 중, auto_action=block 트리거이므로 영향 큼) |
| **판정** | **proposal 유지** + 추가 관찰 우선 필요 |
| 사유 | hard_alert는 `auto_action=block`을 트리거하므로 false positive 영향이 가장 큰 임계값. 초기 추측으로 confirmed 승격은 가장 큰 위험. T2보다 더 엄격한 검증 필요 |

### 4.4 T4 `multi_word_min_length = 2`

| 항목 | 평가 |
|---|---|
| 출처 | D-3 split 정책 기반. multi-word keyword 최소 단어 수 |
| K1 다중 사례 | 미충족 (1 도메인) |
| K2 정량 검증 | 미충족 |
| K3 도메인 정의 직접 연결 | **충족** (multi-word의 의미상 자명한 정의: 2 단어 이상이 "multi-word") |
| K4 운영 1라운드 측정 | 부분 충족 (D-3 split 정책에서 사용) |
| K5 downstream 영향 | 충족 (R1 multi_word_keyword_recovery_test의 max_words 파라미터 등) |
| **판정** | **deferred** (의미상 자명 vs 도메인별 정의 가능성 사이 검토 필요) |
| 사유 | "multi-word"는 의미상 2 단어 이상이라는 정의가 자명하나, 도메인별 (예: bigram·trigram 분리 정책) 재정의 가능성도 있음. 본 게이트는 confirmed로 승격하지 않고 별도 정책 검토로 deferred 처리 |

### 4.5 v0.1 판정 요약

| ID | 이름 | 값 | v0.1 판정 |
|---|---|---|---|
| T1 | `broad_item_concentration_pct` | 60 | **proposal 유지** |
| T2 | `soft_alert_max_delta_pct` | 5 | **proposal 유지** |
| T3 | `hard_alert_min_delta_pct` | 10 | **proposal 유지** |
| T4 | `multi_word_min_length` | 2 | **deferred** |

**confirmed 승격: 0건 / proposal 유지: 3건 / deferred: 1건**

---

## 5. 단일 사례 기반 한계 명시

본 게이트의 판정 근거는 다음 단일 사례에 한정된다.

| 항목 | 범위 |
|---|---|
| 도메인 | ee-agent 한정 (1 도메인) |
| 데이터셋 | v0.2 instance 12 rules (1 데이터셋) |
| 운영 관찰 | v0.2 validator run 1회 (commit `9c7b6ae`) |
| 380 entry 검증 | 0회 |

다중 사례 누적이 부재하므로 본 결정의 4종 판정은 v0.1 한정 보수적 결정이다. 후속 게이트에서 다중 사례 누적 후 재검토 영역.

---

## 6. Profile v0.2 직접 수정 vs v0.3 신규 작성 분리

### 6.1 결정

| 항목 | v0.1 결정 |
|---|---|
| profile v0.2 직접 수정 | **수행하지 않음** |
| profile v0.3 신규 작성 | **본 게이트에서 수행하지 않음** |
| profile 수정 책임 영역 | **별도 Threshold Profile Revision Gate** |

### 6.2 사유

- 본 게이트는 decision 문서 1건 작성 범위. profile 수정은 별도 게이트의 변경 가능 영역
- 본 게이트의 4종 판정 중 confirmed 0건이므로 profile 변경 필요성 0
- 만약 confirmed 1건 이상이 향후 결정되면 profile v0.3 신규 작성 (v0.2 보존)으로 분리 권장

---

## 7. U10 해소 정도

| 항목 | v0.1 결정 |
|---|---|
| migration_log U10 (threshold 4종 확정) | **부분 해소** |
| 부분 해소 의미 | 본 게이트로 4종 각각의 v0.1 판정 결정. confirmed 0건, proposal 3건, deferred 1건 |
| 완전 해소 시점 | 다중 사례 누적 + 정량 검증 후 |
| 본 게이트 추가 진전 | proposal 4종 → proposal 3 + deferred 1로 분리 (proposal 일률 표기에서 deferred 1건 분리) |

### 7.1 v0.1 → v0.2 부분 해소 진전 (migration_log U10 관점)

| 단계 | 누적 |
|---|---|
| migration_log U10 (commit `411912a`) | threshold 4종 모두 `status=proposal` (일률 표기) |
| profile v0.2 (commit `0799544`) | threshold 4종 모두 `status=proposal` 유지 (변경 없음) |
| **본 게이트 (Threshold Confirmation Decision)** | **4종 분류: confirmed 0 / proposal 유지 3 / deferred 1**. U10 부분 해소 |

---

## 8. Claim Boundary

| 단계 | 본 게이트가 주장 가능한 것 |
|---|---|
| (a) 직접 정의 | 4종 threshold v0.1 판정 (confirmed 0 / proposal 유지 3 / deferred 1), confirmed 판단 기준 K1~K5, 명명 차이 사전 보고, profile 수정 결정 (없음), U10 부분 해소 |
| (b) 비공식 가이드라인 | K1~K5 confirmed 판단 기준의 v0.1 권고. 영구 규약 아님 |
| (c) 미확정 | 다중 사례 누적 후 4종 재검토, T4 deferred 영구 정책, 명명 재정렬 (Profile Naming Revision Gate), confirmed 승격 가능성 |

본 게이트는 (a)에 대해서만 v0.1 효력을 주장한다.

---

## 9. 아직 말하면 안 되는 claim

| # | 주장 (금지) |
|---|---|
| C1 | threshold 4종이 profile v0.2에 confirmed로 반영되었다는 주장 — 본 게이트 profile 수정 0건 |
| C2 | threshold가 운영 검증 완료되었다는 주장 — 1 도메인·1 데이터셋·운영 1회 관찰만 |
| C3 | profile v0.2가 수정되었다는 주장 — 변경 0건 |
| C4 | profile v0.3가 본 게이트에서 작성되었다는 주장 — 별도 게이트 책임 |
| C5 | validator가 본 게이트에서 재실행되었다는 주장 — 0회 |
| C6 | L7·U9가 본 게이트로 해소되었다는 주장 — L7 Policy Decision Gate v0.2 책임 |
| C7 | semantic correctness가 본 결정으로 보장된다는 주장 — threshold는 형식·임계값 영역 |
| C8 | 비공식 기준 K1~K5가 영구 규약이라는 주장 — v0.1 권고만 |
| C9 | T4 deferred가 disallowed 또는 영구 미확정으로 결정되었다는 주장 — 검토 대기 영역 |
| C10 | confirmed 0건이 다른 도메인에도 동일하게 적용된다는 주장 — ee-agent 한정 판정 |
| C11 | 명명 차이가 본 게이트로 정정되었다는 주장 — Profile Naming Revision Gate 책임 |
| C12 | governance·D-4 automation·input·generation·audit이 본 게이트에서 진행되었다는 주장 — 0건 |
| C13 | U10이 본 게이트로 완전 해소되었다는 주장 — 부분 해소 유지 |
| C14 | 본 게이트가 후속 review·commit·push·profile revision gate를 자동 통과시킨다는 주장 |

---

## 10. 본 게이트에서 확정된 것과 미확정인 것

### 10.1 확정 사항 (v0.1 한정)

- 4종 threshold v0.1 판정: T1 proposal 유지 / T2 proposal 유지 / T3 proposal 유지 / T4 deferred
- confirmed 0건, proposal 유지 3건, deferred 1건
- confirmed 판단 기준 K1~K5 (v0.1 권고)
- 단일 사례 기반 한계 명시 (1 도메인·1 데이터셋·1회 관찰)
- profile v0.2 직접 수정 없음 + profile v0.3 본 게이트 미작성
- U10 부분 해소 (proposal 4종 → proposal 3 + deferred 1로 분리)
- 명명 차이 사전 보고 (4종 인계 명명 vs profile 실제 명명)

### 10.2 미확정 사항

- 4종 confirmed 승격 가능성 (다중 사례 누적 후)
- T4 deferred 영구 정책 (도메인별 재정의 vs 자명한 정의)
- 명명 재정렬 (Profile Naming Revision Gate 별도)
- K1~K5의 영구 규약 채택 여부
- 운영 1라운드 측정 후 재검토 결과
- profile v0.3 작성 시점

---

## 11. 후속 게이트 후보

| 후보 | 단일 목적 |
|---|---|
| 후보 T-review: Threshold Confirmation Decision Review Gate | 본 결정 문서가 commit 가능한지 read-only 검토 |
| 후보 T-commit: Threshold Confirmation Decision Commit Gate | review 통과 후 commit |
| 후보 T-push: Threshold Confirmation Decision Push Gate | commit 후 원격 보존 |
| 후보 T-revision: Threshold Profile Revision Gate | confirmed 승격 시 profile v0.3 신규 작성 (현 시점 confirmed 0 → revision 불필요) |
| 후보 P-naming: Profile Naming Revision Gate | 인계 명명 vs profile 실제 명명 차이 정리 |
| 후보 V-revision: Validator Boundary Revision Gate (v0.2) | L7 enforcement 도입 (U9 결정 후) |
| 후보 R-multi-domain: Multi-Domain Profile Cross-Check Gate | threshold 4종 다중 도메인 재검토 |

직전 흐름(작성 → review → commit → push) 패턴을 이어가면 후보 T-review가 가장 가까운 자연 후속.

---

## 12. 최종 상태

`READY_FOR_THRESHOLD_CONFIRMATION_REVIEW_GATE`
