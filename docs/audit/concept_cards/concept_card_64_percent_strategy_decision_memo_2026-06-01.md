# 64 Percent Strategy Decision Memo

작성일: 2026-06-01 KST
작성자: Codex supervisor

## 1. Purpose

이 메모는 100 Problem Expansion Validation Gate 이후 드러난 `pure_circuit_theory` 바깥 64% 자리를 어떻게 해석하고 처리할지에 대한 정책 변화, 특이점, 선택 이유를 남긴다.

이 문서는 실행 기록이 아니라 판단 기록이다. 나중에 사람이 다시 읽고 "그때 이 선택이 좋았나?"를 검토할 수 있도록 자연어 설명을 포함한다.

## 2. Starting Point

100개 row 분류 결과:

| domain bucket | count | reading |
|---|---:|---|
| `pure_circuit_theory` | 36 | 좁은 의미의 회로이론 core |
| `broad_scope_exam_circuit` | 25 | 시험 안의 넓은 회로이론/회로 인접 영역 |
| `cross_subject_control_signal` | 15 | 제어/신호/상태공간/블록선도 자리 |
| `uncertain` | 15 | 데이터 또는 출판 구조 때문에 개념 판단이 어려운 자리 |
| `cross_subject_power_three_phase` | 5 | 3상/전력 경계 자리 |
| `logic_or_digital` | 3 | 디지털 논리 자리 |
| `contamination_or_out_of_scope` | 1 | 시험 pool 오염 또는 대상 밖 |

처음 보면 "36%만 순수 회로이론이고 64%가 안 된다"처럼 보인다.

하지만 이 해석은 위험하다. 64%는 하나의 실패 덩어리가 아니다. 그 안에는 서로 다른 처리 방식이 필요한 자리들이 섞여 있다.

## 3. Core Policy Shift

이번 판단의 핵심 변화:

```text
64% = 부족한 회로이론 카드 64%
```

가 아니다.

정확한 해석:

```text
64% = broad_scope 확장 자리 + cross_subject 별도 카드 자리 + uncertain 데이터 자리 + 제외/보류 자리
```

즉, 64%는 "회로이론 카드로 더 덮어야 할 양"이 아니라 "앞으로 처리 경로를 갈라야 하는 양"이다.

이 구분이 중요한 이유:

- broad_scope는 회로이론 카드 보강으로 처리할 수 있다.
- control/signal은 회로이론 카드로 억지 확장하면 안 된다.
- power/three-phase는 회로이론과 전력공학 경계에서 별도 보강이 필요하다.
- uncertain은 카드가 아니라 데이터/출판 구조 문제다.
- logic/contamination은 즉시 카드 확장의 대상이 아니다.

## 4. Natural-Language Reflection

이번 결과에서 가장 조심해야 할 유혹은 "시험에 나오니까 전부 회로이론 카드에 넣자"이다.

사장님 입장에서는 시험 문제를 풀어야 한다. 그러면 블록선도, Routh, 상태방정식, 3상 전력, 논리식도 결국 눈앞의 문제다. "시험에 나오니 다 처리해야 한다"는 말은 맞다.

하지만 시스템 입장에서는 이걸 전부 회로이론 카드에 넣는 순간 카드 체계가 무너진다. 회로이론 카드가 제어공학, 신호처리, 전력공학, 디지털 논리까지 다 설명하려고 하면, 각 카드의 경계가 흐려지고 나중에 어떤 근거로 무엇을 보강해야 하는지 알 수 없게 된다.

따라서 이번 선택은 이렇게 정리한다.

```text
시험에는 나온다.
그래서 버리면 안 된다.
하지만 회로이론으로 우겨넣으면 안 된다.
그러므로 시험용 지식 체계는 확장하되, 카드 분류 체계는 정직하게 분리한다.
```

이 선택은 느리다. 하지만 나중에 다시 볼 수 있다. "왜 이 문제를 회로이론 patch로 안 넣었지?"라고 물었을 때, 답이 남는다. "그 문제는 회로이론 시험지 안에 있었지만 실제 개념은 제어/상태공간이었기 때문"이라고 말할 수 있다.

## 5. Four Scenarios Reviewed

### Scenario 1: Fully Separated Handling

각 bucket을 서로 다른 트랙으로 처리한다.

| bucket | handling |
|---|---|
| broad_scope | 회로이론 확장/보강 |
| cross_subject_control_signal | 제어/신호 카드 신설 |
| cross_subject_power_three_phase | 3상/전력 카드 보강 |
| uncertain | 데이터/출판 구조 backlog |
| logic_or_digital | 디지털 논리 카드군 보류 또는 별도 트랙 |
| contamination | 제외 |

장점:

- 시스템 정직성이 가장 높다.
- 나중에 왜 특정 문제를 특정 카드에 넣지 않았는지 설명하기 쉽다.
- broad_scope와 cross_subject를 섞지 않는다.

단점:

- 일이 커진다.
- 사장님이 여러 트랙을 동시에 판단해야 한다.
- 빠른 시험 대비만 보면 답답할 수 있다.

### Scenario 2: ROI Priority Handling

효용이 큰 순서대로 처리한다.

1. broad_scope 25%
2. cross_subject_power_three_phase 5%
3. cross_subject_control_signal 15%
4. uncertain 15%
5. logic/contamination 4%

장점:

- 가장 빨리 진전이 보인다.
- 기존 회로이론 카드 자산을 활용할 수 있다.
- 시험 점수에 바로 연결될 가능성이 높다.

단점:

- 뒤로 밀린 uncertain/data 문제가 계속 쌓일 수 있다.
- control/signal이 중기 과제로 밀리면 실제 시험 약점이 남을 수 있다.

### Scenario 3: Cover + Defer

즉시 풀 수 있는 것만 덮고 나머지는 보류한다.

즉시 처리:

- pure circuit
- 일부 broad_scope
- 일부 power

보류:

- control/signal
- uncertain
- logic/contamination

장점:

- 가장 빠르다.
- 작업 부담이 낮다.

단점:

- 시험지에 실제로 나오는 control/signal 문제를 방치한다.
- "분류는 했지만 해결은 안 한" 상태가 길어질 수 있다.
- 시스템 정직성도 낮아질 수 있다. 보류 이유가 흐려지면 나중에 다시 같은 논의를 반복한다.

### Scenario 4: Exam Goal + System Goal Split

목적을 둘로 분리한다.

시험 목적:

- 문제에서 정답을 찾는다.
- 정답 근거를 잡는다.
- 근거가 어느 개념/과목으로 확장되는지 표시한다.

시스템 목적:

- 회로이론, broad_scope, 제어, 전력, 데이터 문제를 정직하게 분리한다.
- 카드 patch, 새 카드, 데이터 backlog, 제외를 혼동하지 않는다.

장점:

- 시험 목적과 시스템 정직성을 동시에 살린다.
- "시험에는 나오지만 회로이론 카드는 아니다"라는 말을 할 수 있다.
- 장기적으로 다른 과목 카드 체계로 확장하기 좋다.

단점:

- 실행 구조가 다층이다.
- 문서화 부담이 크다.
- 사장님이 1차 목적을 계속 확인해야 한다.

## 6. Chosen Strategy

선택:

```text
Scenario 2 + Scenario 4 결합
```

즉:

- 실행 순서는 ROI 우선으로 간다.
- 해석 체계는 시험 목적과 시스템 목적을 분리한다.

이 선택의 이유:

1. 사장님의 1차 목적은 "문제에서 정답 찾기 + 정답 근거 + 근거의 확장"이다.
2. 그러므로 broad_scope, power, control/signal을 버릴 수 없다.
3. 하지만 control/signal을 회로이론 카드로 억지 확장하면 시스템이 망가진다.
4. uncertain은 카드 문제가 아니라 데이터/출판 구조 문제다.
5. 따라서 빠른 진전을 위해 broad_scope부터 처리하되, cross_subject는 별도 카드군으로 분리해야 한다.

## 7. Policy Decisions Made

### Decision 1: 64%를 단일 실패율로 읽지 않는다

`pure_circuit_theory` 36% 바깥을 "카드가 실패한 64%"로 읽지 않는다.

이유:

- 64% 안에는 처리 방식이 다른 row가 섞여 있다.
- not_applicable과 missing과 partial을 같은 실패로 묶으면 다음 작업이 왜곡된다.

### Decision 2: broad_scope는 회로이론 확장 후보로 본다

`broad_scope_exam_circuit` 25%는 시험 안의 넓은 회로이론 자리다.

처리:

- 일부는 existing cards로 partial/covered 가능.
- 일부는 optional note 또는 patch candidate.
- 회로이론 카드 확장 gate의 1순위 후보.

단, "넓은 회로이론"이라는 이유만으로 무조건 patch하지 않는다. row별로 source/figure/tag 상태를 본다.

### Decision 3: control/signal은 회로이론 카드로 늘리지 않는다

`cross_subject_control_signal` 15%는 시험에 나오지만 회로이론 카드로 억지 처리하지 않는다.

예:

- 블록선도
- 신호흐름선도
- Routh-Hurwitz
- 상태방정식
- 상태천이행렬
- 안정도 판별

처리:

- 제어공학/신호 카드군 후보로 분리.
- 회로이론 카드 patch 후보로 세지 않는다.

### Decision 4: power/three-phase는 작은 별도 보강 트랙으로 둔다

`cross_subject_power_three_phase` 5%는 작지만 시험에 직접 의미가 있다.

이미 관련 카드가 있다:

- `three_phase_power`
- `power_factor`
- `symmetrical_components`
- `complex_power`

처리:

- 기존 카드 보강 또는 전력/3상 mini-track으로 처리.
- control/signal보다 빠르게 정리 가능하다.

### Decision 5: uncertain은 카드 문제가 아니다

`uncertain` 15%는 대부분 데이터/출판 구조 문제다.

처리:

- publisher cross-reference placeholder는 validation evidence에서 제외 가능.
- OCR/선택지 충돌/그림 누락은 데이터 정리 backlog로 둔다.
- card failure로 세지 않는다.

이번에 사장님이 제공한 설명이 중요했다:

```text
출판사가 같은 문제를 반복 인쇄하지 않고 "몇 년도 몇 회에 있음"처럼 표시하는 경우가 있다.
이 row는 문제 하나를 날려도 문제가 없는 상황이다.
```

이 설명 때문에 `metadata_only` row의 의미가 달라졌다. 단순 데이터 파손이 아니라 출판 편집 구조일 수 있다.

### Decision 6: pressure flag는 authorization이 아니다

`patch_candidate`, `promotion_candidate`, `new_card_candidate`, `optional_note`는 모두 증거 신호다.

아직 하지 않는 것:

- YAML patch
- expansion_pilot promotion
- new card creation
- PR ready-for-review
- PR merge

### Decision 7: pilot card는 baseline coverage로 세지 않는다

`initial_final_value_theorems`, `q_bandwidth`, `power_factor_correction`은 expansion_pilot 상태다.

따라서 pilot card가 잘 맞아도:

- evidence로 기록한다.
- promotion signal로는 둘 수 있다.
- baseline coverage로는 세지 않는다.

## 8. Recommended Execution Plan

### Phase 1: Broad-Scope Circuit Patch Planning

대상:

- `broad_scope_exam_circuit`
- `patch_candidate`
- `optional_note`
- 일부 `partial + under_coverage`

대표 주제:

- image impedance / transfer constants
- antiresonance
- harmonic resonance
- non-sinusoidal power
- Bode bandwidth/stability
- waveform-Laplace bridge
- RLC energy/time detail
- meter scaling / instrument range detail

산출물:

- broad_scope patch 후보 목록
- patch vs optional note 분리
- YAML patch 여부는 별도 human gate에서 결정

### Phase 2: Power/Three-Phase Mini-Track

대상:

- `cross_subject_power_three_phase`
- 이미 covered 또는 partial인 3상/전력 row

대표 주제:

- balanced 3-phase power
- two-wattmeter method
- symmetrical components boundary
- power factor / apparent power

산출물:

- 기존 카드 보강 필요 여부
- 전력공학 카드군으로 분리할 항목

### Phase 3: Control/Signal New-Card Planning

대상:

- `cross_subject_control_signal`
- `new_card_candidate`

대표 주제:

- block diagram algebra
- signal-flow graph
- Routh-Hurwitz
- state equation
- state transition matrix
- control stability

산출물:

- 제어공학 concept card seed list
- 회로이론 카드와의 연결 boundary
- "시험에는 나오지만 회로이론 core가 아님" 표시

### Phase 4: Data/Publication Backlog

대상:

- `uncertain`
- `metadata_only`
- `source_conflict`
- publisher cross-reference rows

처리:

- cross-reference placeholder는 evidence에서 제외.
- 실제 문제 복구가 필요한 row만 backlog.
- 복구 전에는 card failure로 세지 않는다.

### Phase 5: Logic/Contamination Hold

대상:

- `logic_or_digital`
- `contamination_or_out_of_scope`

처리:

- 지금은 보류 또는 제외.
- 디지털 논리 카드군이 필요해질 때 별도 gate.

## 9. Things To Revisit Later

나중에 다시 봐야 할 질문:

1. broad_scope patch를 먼저 한 것이 실제 시험 풀이에 도움이 되었나?
2. control/signal을 별도 카드군으로 뺀 선택이 너무 느렸나, 아니면 시스템을 살렸나?
3. publisher cross-reference row를 제외 처리한 것이 데이터 손실이었나, 아니면 적절한 정리였나?
4. pilot card를 baseline coverage로 세지 않은 것이 보수적이었나, 아니면 불필요하게 엄격했나?
5. `partial` 46개 중 실제로 학습 효과가 큰 보강은 몇 개였나?
6. `new_card_candidate` 18개 중 시험 ROI가 큰 카드군은 무엇이었나?
7. 이 분류 체계가 다른 과목에도 재사용 가능한가?

## 10. Final Recommendation

현재 선택은 다음 한 문장으로 요약한다.

```text
시험 문제는 풀어야 하므로 broad_scope, power, control을 버리지 않는다.
하지만 시스템을 망치지 않기 위해 회로이론, 제어, 전력, 데이터 문제를 끝까지 분리한다.
```

바로 다음 실행 권고:

1. broad_scope action plan 작성
2. patch_candidate 6건과 optional_note 17건 분리 검토
3. power/three-phase mini-track 정리
4. control/signal seed-card list 작성
5. uncertain/data backlog 별도 문서화

## 11. Claim Boundary

이 메모는 다음을 주장하지 않는다.

- YAML patch authorization
- new card creation authorization
- expansion_pilot promotion
- gold set completion
- benchmark status
- semantic-gain proof
- PR #1 ready-for-review approval
- PR #1 merge approval
