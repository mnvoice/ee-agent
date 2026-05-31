# 100 Problem Screening Table Template

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This template defines the row schema for the open 100 Problem Expansion Validation Gate.

It is ready for row-level classification, but it does not classify any row yet.

## 2. Source

Use the frozen inventory:

```text
docs/audit/concept_cards/concept_card_100_problem_source_inventory_2026-05-31.md
```

Selection rule:

```yaml
source_file: app/data/questions.json
source_pool_filter: subject == "회로이론" and q_no is present
sort_order: year asc, session numeric asc, q_no asc
target_count: 100
selected_rows: first 100 rows after sorting
```

## 3. Required Row Schema

| field | allowed values / rule |
|---|---|
| `problem_id` | frozen source inventory ID |
| `source` | `app/data/questions.json:<problem_id>` |
| `source_provenance` | `local_app_exam_data` |
| `problem_text_or_ref` | short text preview or source pointer |
| `domain` | usually `회로이론`; record visible cross-domain drift if any |
| `concept_card_mapping` | list of card IDs or `none` |
| `card_role` | `primary`, `supporting`, `partial`, `mis_fit`, or `none` |
| `coverage_status` | `covered`, `partial`, `missing`, `over_broad`, or `not_applicable` |
| `coverage_rationale` | one-line rationale |
| `pressure_point_flag` | `none`, `optional_note`, `patch_candidate`, `promotion_candidate`, or `new_card_candidate` |
| `pressure_rationale` | required when flagged |
| `is_pilot_row` | `true` if mapped to `q_bandwidth`, `power_factor_correction`, or `initial_final_value_theorems`; otherwise `false` |
| `gold_set_disclaimer` | constant: `not_gold_not_benchmark` |
| `review_status` | `codex_classified`, `moai_advised`, or `human_signed` |
| `timestamp_utc` | ISO timestamp |
| `notes` | free-form, no score language |

## 4. Blank Table

The actual classification table should be generated from this schema and the frozen 100-row inventory.

Do not fill coverage values unless the classifier has read the source row and relevant concept cards.

## 5. Claim Boundary

This template does not claim:

- any row is covered
- any row is missing
- any card passed screening
- any card failed screening
- gold set completion
- benchmark status
- semantic gain proof
- YAML patch authorization
- `expansion_pilot` promotion to baseline
