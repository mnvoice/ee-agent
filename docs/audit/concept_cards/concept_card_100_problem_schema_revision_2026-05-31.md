# 100 Problem Screening Schema Revision

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This document revises the screening schema for the 100 Problem Expansion Validation Gate after review of the Claude Web advisory.

It supplements, rather than deletes, the earlier screening table template.

## 2. Accepted Schema Change

The prior schema treated `coverage_status` as the main classification field.

Supervisor decision:

- Keep `coverage_status` for continuity.
- Add separate axes for source/data condition, domain classification, and card fit.
- Do not use numeric score fields.

## 3. Revised Required Fields

| field | required values / rule |
|---|---|
| `problem_id` | frozen source inventory ID |
| `source` | `app/data/questions.json:<problem_id>` |
| `source_provenance` | `local_app_exam_data` |
| `problem_text_or_ref` | short text preview or source pointer |
| `tag_signal` | original `tag` value, signal only |
| `source_condition` | `usable`, `metadata_only`, `ocr_damage`, `figure_missing`, `tag_text_mismatch`, `insufficient_text`, `source_conflict` |
| `domain_classification` | `pure_circuit_theory`, `broad_scope_exam_circuit`, `cross_subject_control_signal`, `cross_subject_power_three_phase`, `logic_or_digital`, `contamination_or_out_of_scope`, `uncertain` |
| `concept_card_mapping` | list of card IDs or `none` |
| `card_role` | `primary`, `supporting`, `partial`, `mis_fit`, or `none` |
| `coverage_status` | `covered`, `partial`, `missing`, `over_broad`, or `not_applicable` |
| `card_fit_issue` | `none`, `under_coverage`, `over_extension`, `wrong_card_family`, `needs_card_combination`, `pilot_only_fit`, `uncertain` |
| `coverage_rationale` | one-line rationale |
| `pressure_point_flag` | `none`, `optional_note`, `patch_candidate`, `promotion_candidate`, or `new_card_candidate` |
| `pressure_rationale` | required when flagged |
| `is_pilot_row` | `true` if mapped to `q_bandwidth`, `power_factor_correction`, or `initial_final_value_theorems`; otherwise `false` |
| `requires_human_review` | `true` or `false` |
| `multi_failure_flag` | `true` or `false` |
| `gold_set_disclaimer` | constant: `not_gold_not_benchmark` |
| `review_status` | `codex_calibration`, `codex_classified`, `moai_advised`, or `human_signed` |
| `timestamp_utc` | ISO timestamp |
| `notes` | free-form, no score language |

## 4. Rejected Fields

Do not add:

- `data_integrity_score`
- `card_failure_score`
- `source_failure_score`
- `domain_boundary_score`
- percentages
- rankings
- aggregate score fields

Reason:

- Score fields create false precision.
- Score fields invite benchmark or semantic-gain framing.
- MOAI already warned against percentage and score language.

## 5. Claim Boundary

This schema revision does not claim:

- any row has been classified
- any card passed or failed screening
- gold set completion
- benchmark status
- semantic gain proof
- YAML patch authorization
- `expansion_pilot` promotion to baseline
