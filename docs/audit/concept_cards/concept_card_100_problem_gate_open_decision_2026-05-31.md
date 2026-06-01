# 100 Problem Expansion Validation Gate Open Decision

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Human Authorization

User instruction:

```text
go
```

Supervisor interpretation:

- Open the first bounded 100-problem expansion validation gate.
- Apply the conservative defaults recommended by MOAI unless they conflict with explicit claim boundaries.
- Keep PR #1 draft, open, and unmerged.
- Keep YAML frozen.

## 2. Gate Status

```yaml
gate_name: 100 Problem Expansion Validation Gate
gate_status: open
human_supervisor: user / mnvoice
problem_set_selection_authority: user / mnvoice
codex_role: execute deterministic selection and prepare evidence tables
target_count: 100
provenance_policy: local_app_exam_data_only
source_file: app/data/questions.json
selection_rule: subject == "회로이론", sort by year asc, session numeric asc, q_no asc, take first 100 rows
classification_criteria_record: docs/audit/concept_cards/concept_card_100_problem_classification_criteria_2026-05-31.md
gate_close_criteria_record: docs/audit/concept_cards/concept_card_100_problem_gate_close_criteria_2026-05-31.md
output_use_authority: human supervisor only
yaml_mutation_authorized: false
gold_set_claim_authorized: false
semantic_gain_claim_authorized: false
expansion_pilot_promotion_authorized: false
pr_state_change_authorized: false
```

## 3. Why This Selection Is Allowed

This source is repository-local app exam data, not external textbook material.

The problem set is selected independently of the concept-card list:

- Codex does not walk the 33 cards and invent one problem per card.
- Codex does not select examples to make specific cards look good.
- The first 100 rows are selected by a deterministic source-order rule from `app/data/questions.json`.
- Card mapping happens after selection.

## 4. Source Inventory Check

Local source inspection found:

| source | observed count | use in this gate |
|---|---:|---|
| `app/data/questions.json` total rows | 5331 | source pool |
| `app/data/questions.json` rows with `subject == "회로이론"` | 375 | selection pool |
| selected rows | 100 | fixed target |
| `docs/prompt_engineering/explanation_generation_v0/v_next_inputs_d3/input_*.md` | 94 | not used as primary target because target 100 cannot be met there alone |
| `docs/prompt_engineering/explanation_generation_v0/v_next_inputs_d3_b/input_*.md` | 94 | not used as primary target because target 100 cannot be met there alone |

## 5. Target Scope

Target concept-card scope:

- 30 baseline reviewed draft cards: evaluated as baseline coverage candidates.
- 3 `expansion_pilot` cards: evaluated separately as `pilot_candidate_only`.
- Pilot rows must not be counted as baseline coverage.

## 6. Output Form

Allowed output:

- problem inventory record
- row-level coverage screening table
- absolute counts only
- excluded-row list
- pressure-point list
- MOAI review request for the completed table

Forbidden output:

- percentage scores
- benchmark framing
- gold-set framing
- semantic-gain claim
- ready-for-patch list
- ready-for-promotion list
- YAML mutation

## 7. Gate Open Limits

Opening this gate authorizes only evidence-table preparation.

It does not authorize:

- YAML patch
- new YAML cards
- `expansion_pilot` promotion
- PR #1 ready-for-review transition
- PR #1 merge
- corpus-grounding-complete claim
- gold-set claim
- semantic-gain proof claim

## 8. Claim Boundary

This gate-open record does not claim:

- the selected 100 problems are a gold set
- the selected 100 problems are a benchmark
- coverage is good or bad before classification
- any concept card has passed or failed
- any patch is authorized
- any promotion is authorized
