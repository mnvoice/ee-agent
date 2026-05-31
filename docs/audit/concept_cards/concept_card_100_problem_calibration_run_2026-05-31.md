# 100 Problem Calibration Run

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This record classifies only the 20 selected calibration rows from `concept_card_100_problem_calibration_set_2026-05-31.md`.

It does not classify all 100 rows. It does not patch YAML. It does not authorize a patch, promotion, benchmark, gold-set claim, or semantic-gain claim.

## 2. Run Boundary

```yaml
gate_name: 100 Problem Expansion Validation Gate
run_scope: selected_20_calibration_rows_only
source_file: app/data/questions.json
source_provenance: local_app_exam_data
review_status: codex_calibration
timestamp_utc: 2026-05-31T11:57:29Z
gold_set_disclaimer: not_gold_not_benchmark
full_100_row_classification_completed: false
yaml_mutation_authorized: false
```

## 3. Calibration Classification Table

| problem_id | source_condition | domain_classification | concept_card_mapping | card_role | coverage_status | card_fit_issue | pressure_point_flag | requires_human_review | multi_failure_flag | coverage_rationale |
|---|---|---|---|---|---|---|---|---|---|---|
| `1998_4회_61` | usable | pure_circuit_theory | `phasor`, `impedance` | primary | covered | none | none | false | false | Phase relation between complex voltage and current is handled by phasor/impedance language without stretching a card. |
| `1999_6회_62` | usable | pure_circuit_theory | `series_parallel_circuits`, `ohms_law` | partial | partial | under_coverage | optional_note | true | false | Series resistance and Ohm's-law scaling are relevant, but meter-range conversion is not explicit in the current cards. |
| `2000_2회_61` | usable | pure_circuit_theory | `rl_transient` | primary | covered | none | none | false | false | Relay operation time follows standard RL first-order transient behavior. |
| `2000_6회_65` | usable | pure_circuit_theory | `thevenin_equivalent` | primary | covered | none | none | false | false | Open-circuit voltage, equivalent impedance, and load current match the Thevenin load-current formula. |
| `2001_3회_63` | source_conflict | pure_circuit_theory | `source_transformation` | partial | partial | under_coverage | optional_note | true | true | Text asks ideal source properties, but choices appear unrelated; source damage prevents using this as clean coverage proof. |
| `1998_2회_64` | source_conflict | uncertain | none | none | not_applicable | uncertain | none | true | true | Text is mostly cross-reference metadata and choices appear to belong to another concept. |
| `1998_4회_67` | metadata_only | uncertain | none | none | not_applicable | uncertain | none | true | true | Row contains only year/session metadata with blank choices. |
| `1998_6회_66` | metadata_only | uncertain | none | none | not_applicable | uncertain | none | true | true | Row contains only year/session metadata with blank choices despite a plausible tag. |
| `2000_6회_61` | source_conflict | pure_circuit_theory | `mutual_inductance` | primary | partial | uncertain | none | true | true | Text supports mutual inductance, but choices are visibly corrupted or from another row. |
| `2004_1회_73` | tag_text_mismatch | pure_circuit_theory | `laplace_transform` | primary | partial | wrong_card_family | none | true | true | Tag says symmetrical components while text asks a Laplace transform; choices also appear mismatched. |
| `1998_2회_67` | usable | logic_or_digital | none | none | not_applicable | none | none | false | false | Boolean simplification is a digital/logic boundary row, not a circuit concept-card failure. |
| `1998_6회_64` | figure_missing | cross_subject_control_signal | none | none | missing | under_coverage | new_card_candidate | true | true | Signal-flow graph transfer is a control/signal boundary and needs the figure; current baseline cards should not be stretched to cover it. |
| `2000_2회_67` | usable | contamination_or_out_of_scope | none | none | not_applicable | none | none | true | false | Displacement-pressure conversion device is source-pool contamination for this gate. |
| `2000_2회_70` | tag_text_mismatch | cross_subject_control_signal | none | none | missing | wrong_card_family | new_card_candidate | true | true | Tag says apparent power, but text is a state-variable system-matrix problem. |
| `2001_1회_74` | usable | cross_subject_power_three_phase | `symmetrical_components` | primary | covered | none | none | true | false | Zero-sequence current of unbalanced three-phase currents is covered by the existing symmetrical-components card, while remaining a power/three-phase boundary row. |
| `1998_4회_63` | usable | pure_circuit_theory | `initial_final_value_theorems`, `laplace_transform` | primary | partial | pilot_only_fit | promotion_candidate | true | false | The row is a direct final-value theorem use; current strongest fit is an expansion-pilot card, so it cannot count as baseline coverage. |
| `1999_3회_65` | tag_text_mismatch | broad_scope_exam_circuit | `bode_plot` | primary | partial | under_coverage | optional_note | true | true | Text is Bode stability judgment under a resonance tag; Bode card is relevant but stability-margin detail is thin. |
| `1999_6회_69` | figure_missing | pure_circuit_theory | `two_port_network` | primary | partial | none | none | true | true | ABCD/two-port card is the correct family, but the figure is needed to verify the exact parameter relation. |
| `2003_1회_66` | figure_missing | pure_circuit_theory | `rlc_resonance`, `q_bandwidth` | primary | partial | needs_card_combination | patch_candidate | true | true | Antiresonance uses the resonance family but may need bounded antiresonance/2-terminal-network detail beyond the current core card. |
| `2003_1회_67` | usable | broad_scope_exam_circuit | `bode_plot` | primary | partial | under_coverage | optional_note | true | false | Closed-loop first-order bandwidth is closer to Bode/frequency response than RLC Q; current card is relevant but formula detail is incomplete. |

## 4. Absolute Observations From The 20 Rows

| axis | observed values |
|---|---|
| `source_condition` | usable 9; source_conflict 3; metadata_only 2; tag_text_mismatch 3; figure_missing 3 |
| `coverage_status` | covered 4; partial 9; missing 2; not_applicable 5 |
| `requires_human_review` | true 15; false 5 |
| `multi_failure_flag` | true 10; false 10 |
| pilot-involved rows | 2 rows: `1998_4회_63`, `2003_1회_66` |

These are calibration observations only. They are not benchmark results and are not card pass/fail counts.

## 5. Calibration Findings

1. The revised schema is usable for separating source-data, domain-boundary, and card-fit causes.
2. `tag_text_mismatch` is necessary; several rows would be misclassified if the tag were treated as source of truth.
3. A row selected as a clean anchor can still fail source inspection. `2001_3회_63` is the clearest example.
4. `figure_missing` rows should remain eligible for calibration but should require human review before being used as card evidence.
5. Pilot-only fit needs to stay separate from baseline coverage. `1998_4회_63` is the cleanest example.
6. Some rows are legitimate source-pool boundary signals, not concept-card failures. `1998_2회_67` and `2000_2회_67` are examples.

## 6. Workflow Adjustment Before Full 100 Rows

Use the same schema for the full 100-row classification, with these execution rules:

- Inspect `text` and `choices` before mapping a card.
- If tag and text disagree, set `source_condition: tag_text_mismatch` and require human review.
- If text is only metadata or choices are blank, set `coverage_status: not_applicable` unless enough concept text remains.
- If text only points to another year/session/problem, treat it as a publisher cross-reference placeholder before treating it as OCR damage. These rows may be excluded from card evidence without counting as concept-card failure.
- If a figure is required, set `source_condition: figure_missing` and avoid treating the row as final card-quality proof.
- If an expansion-pilot card is the best fit, keep `coverage_status: partial`, set `card_fit_issue: pilot_only_fit` where appropriate, and do not count it as baseline coverage.
- Keep pressure flags as evidence only.

No new score field or percentage field is needed.

## 7. Human Clarification On Cross-Reference Rows

Human supervisor clarification after this calibration run:

```text
Some source rows are scanned from printed exam books where the publisher avoids repeating an identical problem and instead writes that the same problem appeared in another year/session. In that case, the row can be dropped from the validation evidence set; it is not necessarily OCR damage and should not be counted as a concept-card failure.
```

Interpretation for the full 100-row classification:

- Rows like `1998_4회_67` and `1998_6회_66` may represent publisher cross-reference placeholders.
- If no actual problem body is present, classify them as `not_applicable` for concept-card evidence.
- Record the reason as source/publication structure, not card coverage failure.
- Do not spend card-review effort trying to force a mapping from tag alone.

## 8. Next Allowed Step

```yaml
next_step: prepare_full_100_row_classification_table_using_calibrated_rules
full_100_row_classification_authorized_after_calibration: true
yaml_mutation_authorized: false
pr_state_change_authorized: false
```

The next step may classify the frozen 100 rows using this calibrated workflow. That still does not authorize any YAML patch, card promotion, PR ready-for-review transition, or merge.

## 9. Claim Boundary

This calibration run does not claim:

- full 100-row classification completion
- card pass/fail outcome
- gold set completion
- benchmark status
- corpus grounding completion
- semantic-gain proof
- YAML patch authorization
- `expansion_pilot` promotion
- PR #1 ready-for-review approval
- PR #1 merge approval
