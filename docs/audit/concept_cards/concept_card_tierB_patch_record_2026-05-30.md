# Concept Card Tier-B Patch Record

작성일: 2026-05-30 KST
근거:

- `concept_card_supervisor_decision_memo_2026-05-30.md`
- `moai_artifacts/circuit_theory_tierB_note_merge_and_pilot_advisory_v0.1.md`

## 1. Supervisor Decisions

### Part A — Note Merge

| item | decision |
|---|---|
| A-1 `thevenin_equivalent.yaml` word_roles `test_source_method` | accept |
| A-2 `thevenin_equivalent.yaml` risk 보강 | accept with concise wording |
| A-3 `balanced_three_phase.yaml` Y/Delta formula_core 추가 | accept |
| A-4 `balanced_three_phase.yaml` extension condition 보강 | accept |
| A-5 `second_order_response.yaml` series RLC zeta 식 추가 | accept |
| A-6 `symmetrical_components.yaml` I1/I2 분해식 추가 | accept |

### Part B — Expansion Pilot

| item | decision |
|---|---|
| B-1 `q_bandwidth.yaml` 생성 | accept as expansion_pilot |
| B-2 `q_bandwidth.yaml` risk level | MEDIUM |
| B-3 `q_bandwidth.yaml` parallel RLC Q 식 포함 | accept with explicit condition |
| B-4 `power_factor_correction.yaml` 생성 | accept as expansion_pilot |
| B-5 `power_factor_correction.yaml` risk level | MEDIUM |
| B-6 `series_reactor` word_roles key | accept |
| B-7 `initial_final_value_theorems.yaml` 생성 | accept as expansion_pilot |
| B-8 `initial_final_value_theorems.yaml` risk level | MEDIUM |
| B-9 formula notation | use `lim_{s -> ...}` style |

### Cross-cutting

| item | decision |
|---|---|
| C-1 batch vs staged | batch for this narrow gate |
| C-2 pilot status | keep `expansion_pilot` |
| C-3 Codex 30-card baseline | preserved; new files are expansion pilot, not baseline replacement |
| C-4 review summary update | update this gate |

## 2. Files To Modify

- `concept_cards/thevenin_equivalent.yaml`
- `concept_cards/balanced_three_phase.yaml`
- `concept_cards/second_order_response.yaml`
- `concept_cards/symmetrical_components.yaml`
- `concept_cards/index.md`
- `concept_card_review_summary_2026-05-30.md`

## 3. Files To Add

- `concept_cards/q_bandwidth.yaml`
- `concept_cards/power_factor_correction.yaml`
- `concept_cards/initial_final_value_theorems.yaml`

## 4. Claim Boundary

말할 수 있는 것:

- Tier-B note merge 4개와 expansion pilot 3개를 supervisor decision에 따라 적용한다.
- 신규 3개는 baseline 승격이 아니라 `expansion_pilot`이다.

아직 말하면 안 되는 것:

- 33-card gold set이 완성되었다.
- corpus grounding이 전수 검증되었다.
- semantic gain이 증명되었다.
- broad-scope deferred cards가 승인되었다.
