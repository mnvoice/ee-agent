# 100 Problem Calibration Plan

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This plan adds a calibration step before full 100-row classification.

Reason:

- `회로이론` is not a clean conceptual boundary.
- Tags are signals, not source of truth.
- Source-data failure, domain-boundary issue, and card survivability issue can overlap.
- Full automation before calibration risks mislabeling why a row failed.

## 2. Calibration Verdict

```yaml
calibration_required_before_full_classification: true
calibration_target_count: 20
calibration_sampling: stratified
full_100_row_classification_authorized_before_calibration: false
numeric_scores_authorized: false
yaml_mutation_authorized: false
```

## 3. Stratified Calibration Set

Select 20 rows from the frozen 100-row inventory:

| stratum | count | purpose |
|---|---:|---|
| clean anchor rows | 5 | Establish examples where source, domain, and card fit are relatively clean. |
| source-data suspect rows | 5 | Test metadata-only, OCR damage, insufficient text, figure missing, and tag/text mismatch handling. |
| domain-boundary suspect rows | 5 | Test broad-scope exam circuit, control/signal, 4-terminal, transform, 3-phase, power, and logic/digital boundary rows. |
| card-coverage boundary rows | 5 | Test partial coverage, over-broad fit, card-combination need, and pilot-only fit. |

## 4. Revised Row Axes

Calibration rows must use these separate axes:

| axis | field | values |
|---|---|---|
| source/data | `source_condition` | `usable`, `metadata_only`, `ocr_damage`, `figure_missing`, `tag_text_mismatch`, `insufficient_text`, `source_conflict` |
| domain | `domain_classification` | `pure_circuit_theory`, `broad_scope_exam_circuit`, `cross_subject_control_signal`, `cross_subject_power_three_phase`, `logic_or_digital`, `contamination_or_out_of_scope`, `uncertain` |
| card survivability | `coverage_status` | `covered`, `partial`, `missing`, `over_broad`, `not_applicable` |
| card fit | `card_fit_issue` | `none`, `under_coverage`, `over_extension`, `wrong_card_family`, `needs_card_combination`, `pilot_only_fit`, `uncertain` |
| review control | `requires_human_review` | `true`, `false` |
| overlap control | `multi_failure_flag` | `true`, `false` |

## 5. Classification Order

For each calibration row:

1. Check source/data condition.
2. Check domain classification.
3. Propose card mapping only after source/domain notes are visible.
4. Assign coverage status.
5. Assign card fit issue.
6. Set `requires_human_review` when source/domain/card axes disagree or confidence is low.
7. Set `multi_failure_flag` when more than one axis is non-clean.

## 6. Source Of Truth Rule

The tag field is not source of truth.

Use tag only as an initial signal. If tag and problem text conflict, record `tag_text_mismatch` and require human review.

## 7. Human Review Rule

Human review is required for:

- all `tag_text_mismatch` rows
- all `metadata_only` rows before using them as evidence
- all `contamination_or_out_of_scope` rows
- all `wrong_card_family` rows
- all `pilot_only_fit` rows
- all `multi_failure_flag: true` rows

## 8. Calibration Output

Calibration output should include:

- 20-row calibration table
- examples of each revised field value used
- unresolved ambiguity list
- proposed changes to full-classification workflow, if any

## 9. Claim Boundary

This calibration plan does not claim:

- full 100-row classification completion
- any card pass/fail result
- gold set completion
- benchmark status
- semantic gain proof
- YAML patch authorization
- `expansion_pilot` promotion to baseline
