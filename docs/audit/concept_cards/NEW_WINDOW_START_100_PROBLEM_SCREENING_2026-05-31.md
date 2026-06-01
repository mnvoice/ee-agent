# New Window Start - 100 Problem Screening

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Start Here

This handoff preserves the current supervisor state before continuing the 100 Problem Expansion Validation Gate in a new Codex window.

Recommended next window task:

```text
Continue from `NEW_WINDOW_START_100_PROBLEM_SCREENING_2026-05-31.md`.
Run the 20-row stratified calibration setup for the open 100 Problem Expansion Validation Gate.
Do not patch YAML. Do not merge PR #1. Keep PR #1 draft.
```

## 2. Current PR State

Repository:

```text
mnvoice/ee-agent
```

PR:

```text
https://github.com/mnvoice/ee-agent/pull/1
```

Branch:

```text
codex/concept-card-governance-import-2026-05-31
```

Current locked state:

- PR #1 is draft.
- PR #1 is open and unmerged.
- Imported artifacts are under `docs/audit/concept_cards/`.
- YAML mutation is not authorized.
- Gold-set claim is not authorized.
- Benchmark claim is not authorized.
- Semantic-gain proof claim is not authorized.
- `expansion_pilot` promotion is not authorized.
- PR ready-for-review transition is not authorized.
- PR merge is not authorized.

## 3. Concept Card State

Known verification state from prior closeout:

| check | state |
|---|---:|
| Codex concept-card YAML files | 33 |
| Codex YAML structure | OK |
| Codex risk levels | LOW 19 / MEDIUM 14 |
| MOAI entries | 30 |
| MOAI risk levels | LOW 18 / MEDIUM 12 |

Current card status remains:

- 30 baseline reviewed draft cards
- 3 `expansion_pilot` cards
- optional notes deferred
- no YAML patch authorized

## 4. Open Gate

Gate now open:

```yaml
gate_name: 100 Problem Expansion Validation Gate
gate_status: open
target_count: 100
source_file: app/data/questions.json
source_pool_filter: subject == "회로이론" and q_no is present
sort_order: year asc, session numeric asc, q_no asc
selected_rows: first 100 rows after sorting
source_pool_count_for_subject: 375
selected_rows_count: 100
```

Gate-open record:

```text
docs/audit/concept_cards/concept_card_100_problem_gate_open_decision_2026-05-31.md
```

Frozen source inventory:

```text
docs/audit/concept_cards/concept_card_100_problem_source_inventory_2026-05-31.md
```

## 5. Adopted Screening Model

Supervisor accepted the Claude Web advisory with revisions.

Accepted:

- Separate `card_survivability_issue`, `source_data_issue`, and `domain_boundary_issue`.
- These categories are not mutually exclusive.
- Tags are signals, not source of truth.
- `회로이론` is an exam/admin label and may include broad boundary overlap.
- Full 100-row classification must not proceed before 20-row stratified calibration.

Rejected/modified:

- Numeric score fields are rejected.
- Percentages and rankings are rejected.
- Full 4-party review is optional, not mandatory for every row.
- Keep five core `coverage_status` values and add auxiliary axes instead of expanding `coverage_status`.

Supervisor decision record:

```text
docs/audit/concept_cards/concept_card_100_problem_claude_web_advisory_supervisor_decision_2026-05-31.md
```

Schema revision:

```text
docs/audit/concept_cards/concept_card_100_problem_schema_revision_2026-05-31.md
```

## 6. Revised Row Fields

Use these fields for calibration and later screening:

- `problem_id`
- `source`
- `source_provenance`
- `problem_text_or_ref`
- `tag_signal`
- `source_condition`
- `domain_classification`
- `concept_card_mapping`
- `card_role`
- `coverage_status`
- `card_fit_issue`
- `coverage_rationale`
- `pressure_point_flag`
- `pressure_rationale`
- `is_pilot_row`
- `requires_human_review`
- `multi_failure_flag`
- `gold_set_disclaimer`
- `review_status`
- `timestamp_utc`
- `notes`

Do not add score fields.

## 7. Allowed Values Summary

`source_condition`:

- `usable`
- `metadata_only`
- `ocr_damage`
- `figure_missing`
- `tag_text_mismatch`
- `insufficient_text`
- `source_conflict`

`domain_classification`:

- `pure_circuit_theory`
- `broad_scope_exam_circuit`
- `cross_subject_control_signal`
- `cross_subject_power_three_phase`
- `logic_or_digital`
- `contamination_or_out_of_scope`
- `uncertain`

`coverage_status`:

- `covered`
- `partial`
- `missing`
- `over_broad`
- `not_applicable`

`card_fit_issue`:

- `none`
- `under_coverage`
- `over_extension`
- `wrong_card_family`
- `needs_card_combination`
- `pilot_only_fit`
- `uncertain`

`pressure_point_flag`:

- `none`
- `optional_note`
- `patch_candidate`
- `promotion_candidate`
- `new_card_candidate`

## 8. Next Required Work

Next step:

```yaml
next_step: select_20_row_stratified_calibration_set
full_100_row_classification_authorized_before_calibration: false
```

Calibration plan:

```text
docs/audit/concept_cards/concept_card_100_problem_calibration_plan_2026-05-31.md
```

Required calibration strata:

| stratum | count | purpose |
|---|---:|---|
| clean anchor rows | 5 | source/domain/card fit relatively clean |
| source-data suspect rows | 5 | metadata-only, OCR damage, tag/text mismatch, figure-needed, insufficient text |
| domain-boundary suspect rows | 5 | control/signal/system, 4-terminal, transform, 3-phase, power, digital/logic boundary |
| card-coverage boundary rows | 5 | card combination, pilot-only fit, possible under/over coverage |

## 9. Important Interpretation Rule

Do not treat a failed row as card failure until source and domain axes are checked.

A row can fail because:

1. the card is weak or missing
2. the source data is damaged
3. the row is a domain-boundary case
4. more than one of these is true

This gate is a cause-classification system, not a correctness score.

## 10. Human-Friendly Explanation

The purpose of this system:

```text
100 problems are used to pressure-test the concept cards.
When something does not work, the system must identify whether the problem is the card, the source data, or the subject/domain boundary.
```

Example:

```yaml
problem_id: 2001_1회_64
looks_like: control/block-diagram problem
source_subject: 회로이론
supervisor_reading: do not stretch existing circuit cards to cover this
possible_future_signal: new_card_candidate
current_action: no YAML mutation
```

## 11. Storage Model

Do not mix screening results directly into concept-card YAML.

Use separate layers:

```yaml
concept_cards_yaml:
  role: knowledge body
  key: card_id

screening_records_jsonl:
  role: fast machine-readable screening records
  key: problem_id + card_id

supervisor_logs_md:
  role: human-readable rationale and decisions

gate_decisions_md:
  role: authorization boundaries and next-step decisions
```

Former concept-card YAML format remains useful as the knowledge-card DB.

Example card body remains separate:

```yaml
concept: RLC resonance
static_boundary: 회로이론에서 L과 C 리액턴스가 상쇄되는 조건
formula_core:
  - omega0 = 1/sqrt(LC)
  - Q = omega0 / BW
```

Machine screening records should link by `card_id`, not embed problem histories into YAML cards.

## 12. Forbidden Actions

Do not:

- patch YAML
- create new YAML cards
- promote `expansion_pilot` cards
- claim gold set
- claim benchmark status
- claim corpus grounding completion
- claim semantic gain proof
- move PR #1 out of draft
- merge PR #1
- convert pressure flags into patch lists
- use percentages, scores, or rankings

## 13. Recommended First Command In New Window

Inspect these files first:

```text
docs/audit/concept_cards/README.md
docs/audit/concept_cards/concept_card_100_problem_gate_open_decision_2026-05-31.md
docs/audit/concept_cards/concept_card_100_problem_source_inventory_2026-05-31.md
docs/audit/concept_cards/concept_card_100_problem_calibration_plan_2026-05-31.md
docs/audit/concept_cards/concept_card_100_problem_schema_revision_2026-05-31.md
```

Then produce:

```text
docs/audit/concept_cards/concept_card_100_problem_calibration_set_2026-05-31.md
```

This next output should select 20 calibration rows only. It should not classify all 100 rows.

## 14. Claim Boundary

This handoff does not claim:

- calibration completion
- full 100-row classification completion
- card pass/fail outcome
- gold set completion
- benchmark status
- corpus grounding completion
- semantic gain proof
- YAML patch authorization
- `expansion_pilot` promotion
- PR #1 ready-for-review approval
- PR #1 merge approval
