# 100 Problem Full Classification

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This record classifies the frozen 100 rows from the open 100 Problem Expansion Validation Gate using the calibrated workflow.

It is an evidence table only. It does not patch YAML, authorize card promotion, claim a gold set, claim benchmark status, or claim semantic-gain proof.

## 2. Run Boundary

```yaml
gate_name: 100 Problem Expansion Validation Gate
run_scope: frozen_100_rows
source_file: app/data/questions.json
source_inventory: docs/audit/concept_cards/concept_card_100_problem_source_inventory_2026-05-31.md
source_provenance: local_app_exam_data
review_status: codex_classified
timestamp_utc: 2026-05-31T12:04:37Z
gold_set_disclaimer: not_gold_not_benchmark
yaml_mutation_authorized: false
pr_state_change_authorized: false
```

## 3. Classification Table

| row | problem_id | source_condition | domain_classification | concept_card_mapping | card_role | coverage_status | card_fit_issue | pressure_point_flag | requires_human_review | multi_failure_flag | rationale |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `1998_2회_61` | figure_missing | broad_scope_exam_circuit | `second_order_response` | primary | partial | none | none | true | true | s-plane root response is in the 2nd-order/pole family, but the missing figure prevents clean evidence use. |
| 2 | `1998_2회_62` | figure_missing | pure_circuit_theory | `s_domain_circuit_analysis`, `rc_transient` | primary | partial | none | none | true | true | RC transfer-function setup is the right family, but the circuit figure is needed for exact mapping. |
| 3 | `1998_2회_63` | figure_missing | pure_circuit_theory | `laplace_transform`, `rc_transient` | primary | partial | none | none | true | true | Exponential-source RC response fits Laplace/RC transient, with figure dependency. |
| 4 | `1998_2회_64` | source_conflict | uncertain | none | none | not_applicable | uncertain | none | true | true | Cross-reference-like text and unrelated choices make it unusable as card evidence. |
| 5 | `1998_2회_67` | usable | logic_or_digital | none | none | not_applicable | none | none | false | false | Boolean simplification is outside the concept-card target domain. |
| 6 | `1998_4회_61` | usable | pure_circuit_theory | `phasor`, `impedance` | primary | covered | none | none | false | false | Phase relation between complex voltage and current fits phasor/impedance. |
| 7 | `1998_4회_63` | usable | pure_circuit_theory | `initial_final_value_theorems`, `laplace_transform` | primary | partial | pilot_only_fit | promotion_candidate | true | false | Direct final-value theorem use; best fit involves an expansion-pilot card. |
| 8 | `1998_4회_65` | usable | broad_scope_exam_circuit | `laplace_transform` | partial | partial | under_coverage | optional_note | true | false | Impulse-response wording is related to Laplace but not fully explicit in card scope. |
| 9 | `1998_4회_66` | usable | broad_scope_exam_circuit | none | none | missing | under_coverage | new_card_candidate | true | false | Filter taxonomy is not covered by current baseline cards. |
| 10 | `1998_4회_67` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 11 | `1998_4회_68` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 12 | `1998_4회_69` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Cross-reference-like text has no usable problem body. |
| 13 | `1998_4회_70` | figure_missing | logic_or_digital | none | none | not_applicable | none | none | true | true | Logic-device equivalence is a digital boundary row and needs a figure. |
| 14 | `1998_6회_64` | figure_missing | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | true | Signal-flow graph transfer is a control/signal boundary outside baseline cards. |
| 15 | `1998_6회_66` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 16 | `1998_6회_67` | figure_missing | pure_circuit_theory | `rc_transient`, `s_domain_circuit_analysis` | primary | partial | needs_card_combination | none | true | true | Switching initial-condition row fits transient analysis but needs circuit context. |
| 17 | `1998_6회_68` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 18 | `1998_6회_69` | usable | broad_scope_exam_circuit | none | none | missing | under_coverage | new_card_candidate | true | false | Half-wave rectified average value is not represented in current cards. |
| 19 | `1998_6회_70` | usable | broad_scope_exam_circuit | `harmonics`, `fourier_series` | primary | partial | under_coverage | optional_note | true | false | Harmonic components are covered conceptually, but RMS/combined-value calculation detail is thin. |
| 20 | `1999_3회_61` | usable | broad_scope_exam_circuit | `laplace_transform`, `second_order_response` | primary | covered | none | none | false | false | Transfer-function natural frequency fits pole/2nd-order interpretation. |
| 21 | `1999_3회_62` | usable | pure_circuit_theory | `laplace_transform` | primary | covered | none | none | false | false | Integral Laplace transform falls directly under Laplace transform. |
| 22 | `1999_3회_63` | figure_missing | pure_circuit_theory | `rl_transient`, `s_domain_circuit_analysis` | primary | partial | none | none | true | true | RL switching transient is the right family, but exact circuit is figure-dependent. |
| 23 | `1999_3회_65` | tag_text_mismatch | broad_scope_exam_circuit | `bode_plot` | primary | partial | under_coverage | optional_note | true | true | Text is Bode stability judgment under a resonance tag; Bode card lacks stability-margin detail. |
| 24 | `1999_4회_61` | usable | cross_subject_power_three_phase | `symmetrical_components` | primary | covered | none | none | true | false | Symmetrical-components formula maps directly, with power-system boundary noted. |
| 25 | `1999_4회_63` | usable | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | false | Routh stability count is not covered by current concept cards. |
| 26 | `1999_4회_64` | figure_missing | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | true | Block-diagram transfer-function reduction is not covered by baseline cards. |
| 27 | `1999_4회_65` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 28 | `1999_4회_66` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 29 | `1999_4회_67` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 30 | `1999_4회_68` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 31 | `1999_4회_69` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 32 | `1999_6회_61` | figure_missing | cross_subject_power_three_phase | `three_phase_power` | primary | partial | none | none | true | true | Three-phase power family is right, but the circuit figure is needed. |
| 33 | `1999_6회_62` | usable | pure_circuit_theory | `series_parallel_circuits`, `ohms_law` | partial | partial | under_coverage | optional_note | true | false | Series resistance and Ohm's-law scaling are relevant, but meter-range detail is not explicit. |
| 34 | `1999_6회_66` | usable | broad_scope_exam_circuit | `harmonics`, `complex_power` | primary | partial | under_coverage | optional_note | true | false | Non-sinusoidal power uses harmonic power reasoning beyond current formula detail. |
| 35 | `1999_6회_69` | figure_missing | pure_circuit_theory | `two_port_network` | primary | partial | none | none | true | true | ABCD/two-port family is correct, but exact L-network parameters depend on the figure. |
| 36 | `2000_2회_61` | usable | pure_circuit_theory | `rl_transient` | primary | covered | none | none | false | false | Relay timing follows standard RL first-order transient behavior. |
| 37 | `2000_2회_62` | figure_missing | broad_scope_exam_circuit | `fourier_series` | primary | partial | none | none | true | true | Triangle-wave Fourier expansion matches Fourier-series concept, with waveform figure dependency. |
| 38 | `2000_2회_64` | usable | broad_scope_exam_circuit | `laplace_transform`, `s_domain_circuit_analysis` | primary | covered | none | none | false | false | Differential-equation-to-transfer-function conversion is covered. |
| 39 | `2000_2회_65` | figure_missing | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | true | Overall block-diagram transfer function needs control-block algebra not in current cards. |
| 40 | `2000_2회_67` | usable | contamination_or_out_of_scope | none | none | not_applicable | none | none | true | false | Displacement-pressure device is source-pool contamination for this gate. |
| 41 | `2000_2회_70` | tag_text_mismatch | cross_subject_control_signal | none | none | missing | wrong_card_family | new_card_candidate | true | true | State-variable system matrix is not apparent power and is outside baseline cards. |
| 42 | `2000_4회_61` | figure_missing | pure_circuit_theory | `impedance`, `two_port_network` | partial | partial | under_coverage | patch_candidate | true | true | Image-impedance condition relates to impedance/two-port but needs bounded detail and figure. |
| 43 | `2000_4회_62` | figure_missing | broad_scope_exam_circuit | `impedance`, `s_domain_circuit_analysis` | primary | partial | under_coverage | optional_note | true | true | Driving-point impedance from pole/zero distribution is related but not fully covered. |
| 44 | `2000_4회_65` | figure_missing | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | true | Disturbance block-diagram output is control-block algebra. |
| 45 | `2000_4회_66` | usable | cross_subject_control_signal | `laplace_transform` | partial | partial | under_coverage | optional_note | true | false | Root-location stability is touched by pole language but needs explicit stability criterion. |
| 46 | `2000_4회_67` | usable | broad_scope_exam_circuit | `harmonics`, `complex_power` | primary | partial | under_coverage | optional_note | true | false | Harmonic current power needs non-sinusoidal power detail beyond current cards. |
| 47 | `2000_6회_61` | source_conflict | pure_circuit_theory | `mutual_inductance` | primary | partial | uncertain | none | true | true | Text supports mutual inductance, but choices are corrupted or from another row. |
| 48 | `2000_6회_65` | usable | pure_circuit_theory | `thevenin_equivalent` | primary | covered | none | none | false | false | Open-circuit voltage, equivalent impedance, and load current match Thevenin formula. |
| 49 | `2000_6회_66` | usable | broad_scope_exam_circuit | `z_transform` | primary | covered | none | none | false | false | z-transform card directly covers the signal-transform concept. |
| 50 | `2000_6회_68` | usable | broad_scope_exam_circuit | `bode_plot` | primary | covered | none | none | false | false | Frequency-response gain and phase fit Bode/frequency-response card. |
| 51 | `2000_6회_69` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 52 | `2000_6회_70` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 53 | `2000_6회_74` | tag_text_mismatch | pure_circuit_theory | `two_port_network` | primary | partial | wrong_card_family | none | true | true | Text is 4-terminal parameters under a Thevenin tag; two-port is correct family. |
| 54 | `2000_6회_78` | tag_text_mismatch | pure_circuit_theory | `laplace_transform` | primary | partial | wrong_card_family | none | true | true | Text asks Laplace transform under a Thevenin tag. |
| 55 | `2001_1회_62` | usable | broad_scope_exam_circuit | `bode_plot` | primary | covered | none | none | false | false | Bode gain curve is directly in Bode-plot scope. |
| 56 | `2001_1회_63` | figure_missing | pure_circuit_theory | `thevenin_equivalent` | primary | partial | none | none | true | true | Linear network terminal behavior fits Thevenin, but circuit figure is needed. |
| 57 | `2001_1회_64` | figure_missing | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | true | Block-diagram comparison is control/signal-flow territory. |
| 58 | `2001_1회_67` | figure_missing | pure_circuit_theory | `two_port_network` | primary | partial | none | none | true | true | 4-terminal constant A maps to two-port, but figure is needed. |
| 59 | `2001_1회_69` | figure_missing | pure_circuit_theory | `rlc_resonance`, `second_order_response` | partial | partial | under_coverage | optional_note | true | true | RLC energy/time problem is related but current cards lack this energy-window detail. |
| 60 | `2001_1회_70` | usable | pure_circuit_theory | `second_order_response`, `rlc_resonance` | primary | partial | under_coverage | optional_note | true | false | RLC transient calculation fits 2nd-order response but needs more calculation detail. |
| 61 | `2001_1회_74` | usable | cross_subject_power_three_phase | `symmetrical_components` | primary | covered | none | none | true | false | Zero-sequence current is covered by symmetrical-components card, with power-boundary noted. |
| 62 | `2001_2회_63` | figure_missing | pure_circuit_theory | `rc_transient`, `s_domain_circuit_analysis` | primary | partial | needs_card_combination | none | true | true | Switching initial condition maps to transient analysis but depends on circuit figure. |
| 63 | `2001_2회_64` | figure_missing | broad_scope_exam_circuit | none | none | missing | under_coverage | new_card_candidate | true | true | Half-wave average-value computation is not currently covered. |
| 64 | `2001_2회_65` | usable | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | false | Routh-Hurwitz sign-change interpretation is not covered. |
| 65 | `2001_2회_68` | usable | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | false | State-equation construction is control/state-space territory. |
| 66 | `2001_2회_70` | tag_text_mismatch | cross_subject_control_signal | none | none | missing | wrong_card_family | new_card_candidate | true | true | Stability condition row is mislabeled as non-sinusoidal RMS. |
| 67 | `2001_3회_61` | tag_text_mismatch | pure_circuit_theory | `impedance`, `phasor` | primary | partial | wrong_card_family | none | true | true | Text is RC AC current, not apparent power; impedance/phasor family is usable. |
| 68 | `2001_3회_62` | figure_missing | pure_circuit_theory | `two_port_network` | primary | partial | none | none | true | true | 4-terminal constant A maps to two-port, but figure is needed. |
| 69 | `2001_3회_63` | source_conflict | pure_circuit_theory | `source_transformation` | partial | partial | under_coverage | optional_note | true | true | Text asks ideal source properties, but choices appear unrelated. |
| 70 | `2001_3회_65` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 71 | `2001_3회_66` | usable | cross_subject_power_three_phase | `three_phase_power`, `power_factor` | primary | covered | none | none | true | false | Balanced 3-phase load power and line current are covered. |
| 72 | `2001_3회_71` | usable | broad_scope_exam_circuit | `rlc_resonance`, `harmonics` | primary | partial | needs_card_combination | patch_candidate | true | false | Third-harmonic resonance needs a combination of resonance and harmonics. |
| 73 | `2001_3회_72` | figure_missing | broad_scope_exam_circuit | `laplace_transform`, `fourier_series` | partial | partial | under_coverage | optional_note | true | true | Square-wave Laplace transform bridges waveform and Laplace cards; figure needed. |
| 74 | `2002_1회_64` | usable | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | false | State-transition matrix is state-space/control content. |
| 75 | `2002_1회_65` | figure_missing | pure_circuit_theory | `rl_transient` | primary | partial | none | none | true | true | RL time constant behavior is covered, but exact circuit context is figure-dependent. |
| 76 | `2002_1회_69` | usable | broad_scope_exam_circuit | `complex_power`, `power_factor` | primary | covered | none | none | false | false | Apparent power and power factor from P/Q are covered by power cards. |
| 77 | `2002_1회_70` | usable | broad_scope_exam_circuit | `complex_power`, `power_factor` | primary | covered | none | none | false | false | Power factor from V/I/P fits existing power cards. |
| 78 | `2002_3회_63` | figure_missing | pure_circuit_theory | `impedance`, `two_port_network` | partial | partial | under_coverage | patch_candidate | true | true | Image-impedance calculation is related but needs dedicated boundary/detail. |
| 79 | `2002_3회_65` | figure_missing | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | true | Block-diagram equivalent transformation is not covered. |
| 80 | `2002_3회_67` | figure_missing | pure_circuit_theory | `superposition_theorem` | primary | partial | none | none | true | true | Superposition concept fits, but circuit figure is needed for evidence. |
| 81 | `2002_3회_68` | usable | broad_scope_exam_circuit | none | none | missing | under_coverage | new_card_candidate | true | false | Ideal op-amp operator output is not represented in current cards. |
| 82 | `2002_3회_69` | usable | pure_circuit_theory | `impedance`, `phasor` | primary | partial | under_coverage | optional_note | true | false | RL frequency locus uses impedance/phasor reasoning but locus detail is not explicit. |
| 83 | `2002_3회_70` | usable | cross_subject_control_signal | `laplace_transform`, `second_order_response` | partial | partial | under_coverage | optional_note | true | false | Step response of transfer function is related but control-response detail is thin. |
| 84 | `2003_1회_63` | usable | cross_subject_power_three_phase | `three_phase_power`, `power_factor` | primary | covered | none | none | true | false | Two-wattmeter balanced-load power factor fits 3-phase/power-factor family. |
| 85 | `2003_1회_64` | figure_missing | broad_scope_exam_circuit | none | none | missing | under_coverage | new_card_candidate | true | true | Op-amp circuit output is outside current concept-card coverage. |
| 86 | `2003_1회_66` | figure_missing | pure_circuit_theory | `rlc_resonance`, `q_bandwidth` | primary | partial | needs_card_combination | patch_candidate | true | true | Antiresonance needs bounded resonance/detail beyond current core card. |
| 87 | `2003_1회_67` | usable | broad_scope_exam_circuit | `bode_plot` | primary | partial | under_coverage | optional_note | true | false | First-order closed-loop bandwidth fits frequency-response family but formula detail is thin. |
| 88 | `2003_1회_70` | figure_missing | broad_scope_exam_circuit | `laplace_transform`, `fourier_series` | partial | partial | under_coverage | optional_note | true | true | Square-wave Laplace transform bridges waveform and Laplace; figure needed. |
| 89 | `2003_3회_63` | figure_missing | pure_circuit_theory | `s_domain_circuit_analysis`, `rc_transient`, `rl_transient` | partial | partial | needs_card_combination | none | true | true | Switching initial current needs the circuit figure and transient family selection. |
| 90 | `2003_3회_65` | usable | pure_circuit_theory | `impedance`, `power_factor` | primary | covered | none | none | false | false | RL AC power factor fits impedance and power-factor cards. |
| 91 | `2003_3회_70` | usable | pure_circuit_theory | `laplace_transform` | primary | covered | none | none | false | false | Unit-step Laplace transform is directly covered. |
| 92 | `2003_3회_75` | tag_text_mismatch | pure_circuit_theory | `two_port_network`, `impedance` | primary | partial | wrong_card_family | patch_candidate | true | true | Text is 4-terminal image impedance under a symmetrical-components tag. |
| 93 | `2004_1회_28` | figure_missing | pure_circuit_theory | `two_port_network` | primary | partial | none | none | true | true | 4-terminal constants map to two-port but require the figure. |
| 94 | `2004_1회_63` | figure_missing | logic_or_digital | none | none | not_applicable | none | none | true | true | Gate-name identification is digital/logic boundary and figure-dependent. |
| 95 | `2004_1회_66` | figure_missing | pure_circuit_theory | `source_transformation` | primary | partial | none | none | true | true | Equivalent current-source conversion maps to source transformation but requires figures. |
| 96 | `2004_1회_68` | figure_missing | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | true | Signal-flow graph simplification is not covered. |
| 97 | `2004_1회_70` | metadata_only | uncertain | none | none | not_applicable | none | none | true | true | Publisher-style cross-reference/metadata row; exclude from card evidence. |
| 98 | `2004_1회_73` | tag_text_mismatch | pure_circuit_theory | `laplace_transform` | primary | partial | wrong_card_family | none | true | true | Tag says symmetrical components while text asks a Laplace transform. |
| 99 | `2004_1회_78` | usable | broad_scope_exam_circuit | `harmonics`, `complex_power` | primary | partial | under_coverage | optional_note | true | false | Non-sinusoidal average power is related to harmonics/power but needs more formula detail. |
| 100 | `2004_1회_79` | tag_text_mismatch | pure_circuit_theory | `two_port_network` | primary | partial | wrong_card_family | patch_candidate | true | true | Text is 4-terminal/transfer constants under a Laplace-inverse tag. |

## 4. Absolute Counts

These are descriptive counts for this evidence table only.

| field | values |
|---|---|
| `source_condition` | usable 39; figure_missing 35; metadata_only 14; tag_text_mismatch 9; source_conflict 3 |
| `domain_classification` | pure_circuit_theory 36; broad_scope_exam_circuit 25; uncertain 15; cross_subject_control_signal 15; cross_subject_power_three_phase 5; logic_or_digital 3; contamination_or_out_of_scope 1 |
| `coverage_status` | partial 46; not_applicable 19; missing 18; covered 17 |
| `pressure_point_flag` | none 58; new_card_candidate 18; optional_note 17; patch_candidate 6; promotion_candidate 1 |
| `requires_human_review` | true 86; false 14 |
| `multi_failure_flag` | true 61; false 39 |

## 5. Main Readout

The 100 rows do not support a simple "card passed/failed" reading.

Observed groups:

- Clean baseline coverage exists for ordinary phasor, Thevenin, RL transient, Laplace, z-transform, Bode, complex-power, and power-factor rows.
- Many rows are excluded or human-review rows because the source is a publisher cross-reference placeholder, a figure-dependent row, or tag/text mismatch.
- Several `회로이론` rows are broad exam-scope or cross-subject control/signal rows: block diagrams, signal-flow graphs, Routh/state-space, op-amp, and logic.
- The most useful future pressure signals are not YAML authorization. They are candidates for a later human gate.

## 6. Pressure Signals For Later Human Gate

| signal | rows | interpretation |
|---|---|---|
| `new_card_candidate` | `1998_4회_66`, `1998_6회_64`, `1998_6회_69`, `1999_4회_63`, `1999_4회_64`, `2000_2회_65`, `2000_2회_70`, `2000_4회_65`, `2001_1회_64`, `2001_2회_64`, `2001_2회_65`, `2001_2회_68`, `2001_2회_70`, `2002_1회_64`, `2002_3회_65`, `2002_3회_68`, `2003_1회_64`, `2004_1회_68` | Mostly control/signal, Routh/state-space, op-amp, filter taxonomy, waveform average, and signal-flow areas. |
| `patch_candidate` | `2000_4회_61`, `2001_3회_71`, `2002_3회_63`, `2003_1회_66`, `2003_3회_75`, `2004_1회_79` | Mostly image impedance, antiresonance, harmonic resonance, and 4-terminal/transfer constants. |
| `promotion_candidate` | `1998_4회_63` | Initial/final value theorem pilot fit is strong but still not promotion authorization. |
| `optional_note` | multiple rows | Mostly non-sinusoidal power, Bode bandwidth/stability, meter scaling, waveform-Laplace, RLC energy, and RL frequency locus. |

## 7. Workflow Notes Before Any Patch Discussion

- Do not use excluded publisher cross-reference rows as card evidence.
- Do not stretch baseline circuit cards to cover control-block algebra or state-space rows.
- Do not count expansion-pilot matches as baseline coverage.
- Figure-dependent rows should be reviewed with the source figure before becoming hard evidence.
- Pressure signals should be reviewed by a human supervisor before any YAML patch or new-card gate.

## 8. Claim Boundary

This full classification record does not claim:

- gold set completion
- benchmark status
- corpus grounding completion
- semantic-gain proof
- YAML patch authorization
- `expansion_pilot` promotion
- PR #1 ready-for-review approval
- PR #1 merge approval
