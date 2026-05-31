# Broad-Scope Circuit Action Plan

작성일: 2026-06-01 KST
작성자: Codex supervisor

## 1. Purpose

이 문서는 100 Problem Full Classification 이후 첫 실행 단계를 정리한다.

대상은 `pure_circuit_theory` 바깥 64% 전체가 아니다. 이번 단계는 그중 ROI가 높은 **broad_scope / 회로 인접 보강 자리**를 먼저 다룬다.

이 문서는 action plan이다. YAML patch를 수행하지 않는다. 새 concept card를 만들지 않는다. `expansion_pilot`을 승격하지 않는다.

## 2. Why This Comes First

64% 처리 전략 메모에서 선택한 방향은 `Scenario 2 + Scenario 4`였다.

즉:

- 실행은 ROI 순서로 한다.
- 해석은 시험 목적과 시스템 목적을 분리한다.

그 첫 단계가 broad_scope / 회로 인접 보강이다.

이유:

1. 시험에 직접 나온다.
2. 기존 회로이론 카드 자산을 가장 많이 활용할 수 있다.
3. 제어/상태공간처럼 새 과목 카드군을 만들기 전에도 진전이 가능하다.
4. 그래도 회로이론 카드 경계를 무너뜨리지 않도록 patch / optional note / new card / defer를 분리해야 한다.

## 3. Scope Boundary

이번 action plan에 포함:

- `broad_scope_exam_circuit` 중 회로/신호/파형/전력계산과 가까운 row
- `pure_circuit_theory` 중 patch signal이 강한 row
- `optional_note`로 처리 가능한 얇은 보강 row
- figure 확인이 필요한 회로 인접 row

이번 action plan에서 제외:

- `cross_subject_control_signal` 전체 카드군 설계
- `cross_subject_power_three_phase` mini-track 전체 설계
- `uncertain` 데이터 복구
- `logic_or_digital`
- `contamination_or_out_of_scope`

## 4. Candidate Split

### 4.1 Patch Gate Candidates

이들은 바로 YAML patch가 아니라, **다음 patch gate에서 원문/그림 확인 후 검토할 후보**다.

| priority | problem_id | topic | current mapping | reason | required before patch |
|---:|---|---|---|---|---|
| 1 | `2003_1회_66` | antiresonance | `rlc_resonance`, `q_bandwidth` | 반공진이 반복적으로 RLC 공진 카드 경계에 걸림 | 그림 확인, antiresonance가 기존 `rlc_resonance` 보강인지 별도 카드인지 결정 |
| 2 | `2001_3회_71` | third-harmonic resonance | `rlc_resonance`, `harmonics` | 공진과 고조파가 결합되는 시험형 | row 원문 확인, harmonic resonance를 optional note로 둘지 patch로 둘지 결정 |
| 3 | `2000_4회_61` | image impedance condition | `impedance`, `two_port_network` | 영상임피던스/전달정수 계열이 현 카드보다 세부적 | 그림 확인, `two_port_network` 보강 범위 결정 |
| 4 | `2002_3회_63` | image impedance calculation | `impedance`, `two_port_network` | 영상임피던스 계산형 | 그림 확인, formula note 후보 검토 |
| 5 | `2003_3회_75` | 4-terminal image impedance | `two_port_network`, `impedance` | tag mismatch가 있지만 실제 내용은 4단자/영상임피던스 | tag 오류 기록, 4단자 note 후보 검토 |
| 6 | `2004_1회_79` | 4-terminal / transfer constants | `two_port_network` | 전달정수/4단자 상수 세부가 반복됨 | tag 오류 기록, two-port convention note 후보 검토 |

해석:

- 이 6건은 “patch 후보”다.
- 아직 patch authorization은 아니다.
- 공통 축은 `RLC resonance` 확장과 `two_port / image impedance` 확장이다.

## 5. Optional Note Candidates

이들은 YAML 본문을 크게 바꾸기보다, 나중에 optional note 또는 설명 보강으로 처리할 가능성이 큰 row다.

| group | rows | suggested handling |
|---|---|---|
| Bode / bandwidth / stability | `1999_3회_65`, `2000_4회_66`, `2003_1회_67` | `bode_plot` 카드에 bandwidth/stability margin boundary를 보강할지 검토 |
| non-sinusoidal power | `1998_6회_70`, `1999_6회_66`, `2000_4회_67`, `2004_1회_78` | `harmonics`, `complex_power`, `power_factor` 사이의 비정현파 전력 boundary 정리 |
| waveform to Laplace | `1998_4회_65`, `2001_3회_72`, `2003_1회_70` | `laplace_transform` 카드에 impulse/square-wave bridge를 넣을지 검토 |
| RLC transient details | `2001_1회_69`, `2001_1회_70` | `second_order_response` / `rlc_resonance`에 energy/time calculation note 필요성 검토 |
| measurement / scaling | `1999_6회_62` | `series_parallel_circuits` 또는 `ohms_law`에 meter range example을 넣을지 검토 |
| frequency locus | `2002_3회_69` | `impedance` / `phasor`에 RL frequency locus를 넣을지 검토 |
| control-response bridge | `2002_3회_70` | 회로이론 보강이 아니라 control 카드군으로 넘길 가능성도 검토 |

해석:

- optional note는 patch보다 낮은 강도의 신호다.
- 시험 풀이에는 도움이 될 수 있지만, 카드 core를 바꿀 정도인지 별도 판단해야 한다.
- 특히 Bode/stability와 control-response는 회로이론 카드에 넣을지 제어 카드로 보낼지 조심해야 한다.

## 6. New Card Candidates Inside Broad-Scope-Like Area

일부 row는 broad_scope처럼 보이지만, 현재 카드에 억지로 붙이면 나쁜 카드가 된다.

| problem_id | topic | reason |
|---|---|---|
| `1998_4회_66` | filter taxonomy | 현재 `bode_plot` 또는 `rlc_resonance`로는 여파기 종류 판별을 안전하게 커버하지 못함 |
| `1998_6회_69` | half-wave rectified average | 비정현파/정류파 평균값은 현재 카드군에 없음 |
| `2001_2회_64` | half-wave average value | 같은 평균값/파형 계산 계열 |
| `2002_3회_68` | ideal op-amp operator | 회로 broad-scope 시험에는 나오지만 별도 op-amp 카드가 필요할 수 있음 |
| `2003_1회_64` | op-amp output | op-amp 회로 해석 자리 |

해석:

- 이들은 “회로이론 시험 안”에는 있을 수 있다.
- 하지만 기존 회로 concept card를 늘려서 억지로 cover하면 안 된다.
- 별도 mini-card 후보로 보되, 즉시 생성은 금지한다.

## 7. Immediate Recommended Work Order

### Step A: Source Figure Check Pack

먼저 그림이 필요한 patch 후보를 묶는다.

대상:

- `2003_1회_66`
- `2000_4회_61`
- `2002_3회_63`
- `2003_3회_75`
- `2004_1회_79`

목적:

- 실제 그림/원문 없이 카드 patch를 결정하지 않는다.
- figure_missing row를 hard evidence로 쓰지 않는다.

### Step B: RLC Resonance Extension Review

대상:

- `2003_1회_66` antiresonance
- `2001_3회_71` third-harmonic resonance
- `2001_1회_70` RLC transient detail
- `2001_1회_69` RLC energy/time detail

결정해야 할 것:

- 기존 `rlc_resonance`에 caution/note로 충분한가?
- `q_bandwidth` pilot과 연결해야 하는가?
- `second_order_response`와 역할을 나눠야 하는가?

### Step C: Two-Port / Image-Impedance Review

대상:

- `2000_4회_61`
- `2002_3회_63`
- `2003_3회_75`
- `2004_1회_79`

결정해야 할 것:

- `two_port_network` 카드에 image impedance / transfer constants note가 필요한가?
- convention 혼동 방지를 위해 caution을 보강해야 하는가?
- 별도 `image_impedance_transfer_constants` 카드가 필요한가?

### Step D: Non-Sinusoidal Power Review

대상:

- `1998_6회_70`
- `1999_6회_66`
- `2000_4회_67`
- `2004_1회_78`

결정해야 할 것:

- `harmonics`와 `complex_power` 사이의 boundary를 어떻게 둘 것인가?
- 평균전력/실효값/고조파 전력식을 card core에 넣을 것인가?
- broad_scope라서 optional note로만 둘 것인가?

### Step E: Bode / Bandwidth Boundary Review

대상:

- `1999_3회_65`
- `2000_4회_66`
- `2003_1회_67`

결정해야 할 것:

- `bode_plot`이 회로 주파수응답 카드인지, 제어 안정도 카드까지 일부 품을지 결정한다.
- 안정도 판별은 control 카드군으로 넘길 가능성이 높다.

## 8. Proposed Next Document

다음 문서는 아래 이름이 좋다.

```text
docs/audit/concept_cards/concept_card_broad_scope_patch_gate_precheck_2026-06-01.md
```

그 문서에서 할 일:

- patch_candidate 6건을 source/figure 필요성 기준으로 재검토
- optional_note 17건을 group별로 재분류
- YAML patch 가능성을 논하지 말고, patch gate를 열 수 있는지 판단
- 필요하면 MOAI/advisory request packet 준비

## 9. Decision Boundaries

이번 action plan에서 하지 않는 것:

- YAML patch
- 새 card 생성
- `expansion_pilot` 승격
- PR #1 ready-for-review 전환
- PR #1 merge
- gold set claim
- benchmark claim
- semantic-gain proof claim

## 10. Short Conclusion

이번 단계의 핵심은 이것이다.

```text
broad_scope를 먼저 보되, broad_scope 안에서도 patch / optional note / new card / figure-check를 갈라야 한다.
```

가장 먼저 볼 묶음은:

1. RLC resonance extension
2. two-port / image impedance
3. non-sinusoidal power
4. Bode / bandwidth boundary

이 네 묶음은 시험에 실제로 나오고, 기존 카드와 연결점도 있다. 따라서 control/signal 새 카드군보다 먼저 처리할 가치가 있다.