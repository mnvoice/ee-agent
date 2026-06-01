# 100+ Problem Expansion Gate-Open Preconditions

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This document records the preconditions that must be satisfied before the `100+ Problem Expansion Validation Gate` may be opened.

It implements the MOAI advisory safeguards without opening the gate.

This document is documentation-only.

It does not open the gate, approve a problem set, authorize YAML mutation, promote cards, claim semantic gain, claim gold-set status, move PR #1 out of draft, or approve merge.

## 2. Current State

Current state remains locked:

- PR #1 is draft.
- PR #1 is open and unmerged.
- The 100+ validation gate is proposed, not opened.
- No target count is frozen.
- No problem set is approved.
- No YAML patch is authorized.
- No `expansion_pilot` promotion is authorized.
- No gold-set, corpus-grounding-complete, or semantic-gain claim is made.

## 3. Required Human Decisions Before Gate Open

| # | decision | required before gate open | current status |
|---:|---|---|---|
| 1 | problem-set selection authority | Name the human supervisor who owns problem selection. | not decided |
| 2 | provenance policy | Decide allowed sources and row-level provenance labels. | not decided |
| 3 | target-count freeze | Replace proposal phrase `100+` with one fixed integer target count. | not decided |
| 4 | classification criteria | Freeze definitions for `covered`, `partial`, `missing`, `over_broad`, and `not_applicable`. | not decided |
| 5 | gate-open record | Create an explicit human-approved gate-open record. | not decided |
| 6 | gate-close criteria | Define exit criteria and required human close record. | not decided |
| 7 | output-use authority | Define who may convert evidence into later patch, promotion, or new-card gates. | not decided |

## 4. Recommended First-Run Defaults

These are recommendations only, not approvals:

- source scope: local exam-source only
- target scope: all 33 cards
- baseline reporting: 30 reviewed draft cards only
- pilot reporting: 3 `expansion_pilot` cards in a separate section
- pilot row tag: `pilot_candidate_only`
- output style: evidence tables only
- count style: absolute counts only, no percentages or scores
- downstream actions: none without separate human gate

## 5. Required Row Schema For Future Gate

A future gate-open record should either adopt or explicitly revise this schema:

| field | required meaning |
|---|---|
| `problem_id` | stable unique identifier |
| `source` | exam year and round, file path, or citation |
| `source_provenance` | source class such as `real_exam`, `generated`, `curated`, or `textbook_excerpt` |
| `problem_text_or_ref` | raw problem text or stable pointer |
| `domain` | domain/category tag |
| `concept_card_mapping` | list of card IDs or `none` |
| `card_role` | `primary`, `supporting`, `partial`, or `mis_fit` |
| `coverage_status` | `covered`, `partial`, `missing`, `over_broad`, or `not_applicable` |
| `coverage_rationale` | one-line rationale |
| `pressure_point_flag` | `optional_note`, `patch_candidate`, `promotion_candidate`, `new_card_candidate`, or `none` |
| `pressure_rationale` | required when flagged |
| `is_pilot_row` | true if mapped to an `expansion_pilot` card |
| `gold_set_disclaimer` | constant statement that the row is not a gold standard and not a benchmark |
| `review_status` | `codex_classified`, `moai_advised`, or `human_signed` |
| `timestamp_utc` | row timestamp |
| `notes` | free-form notes with no score language |

## 6. Forbidden Drift Patterns

The future gate must not drift into:

- percentage or score language
- benchmark, gold set, reference set, or evaluation suite framing
- baseline-vs-pilot promotion language
- treating pressure flags as patch authorization
- single-classifier final authority without spot-checking
- external textbook grounding unless separately authorized
- auto-patching YAML
- auto-generating new card YAML
- auto-promoting `expansion_pilot` cards
- auto-moving PR #1 out of draft
- auto-changing PR labels, milestones, or project status
- adding rows beyond the frozen target count mid-run

## 7. Gate-Open Record Template

A future human-approved gate-open record should include:

```yaml
gate_name: 100+ Problem Expansion Validation Gate
gate_status: open
human_supervisor: <name/account>
target_count: <fixed_integer>
problem_set_selection_authority: <name/account>
provenance_policy: <local_exam_only | local_corpus | external_sources | mixed_with_labels>
classification_criteria_record: <path>
gate_close_criteria: <path_or_summary>
output_use_authority: <name/account_or_policy>
yaml_mutation_authorized: false
gold_set_claim_authorized: false
semantic_gain_claim_authorized: false
expansion_pilot_promotion_authorized: false
pr_state_change_authorized: false
```

## 8. Claim Boundary

This precondition document does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- `expansion_pilot` promotion to baseline
- YAML patch authorization
- 100+ problem-set approval
- 100+ validation gate open approval
- PR #1 ready-for-review approval
- PR #1 merge approval
