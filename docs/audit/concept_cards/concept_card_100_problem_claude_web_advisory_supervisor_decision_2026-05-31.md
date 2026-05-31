# Claude Web Advisory Supervisor Decision - 100 Problem Screening

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Input

Source:

- User pasted Claude Web advisory text in the Codex thread.
- Subject: how to distinguish `card failure`, `source-data failure`, and `domain-boundary issue` before row-level screening.

The advisory is treated as external reasoning input, not authorization.

## 2. Supervisor Verdict

```yaml
overall_verdict: PASS_WITH_REVISIONS
accept_core_3_way_split: true
accept_multi_failure_flag: true
accept_stratified_calibration: true
accept_tag_not_sot_warning: true
accept_score_fields: false
accept_automatic_full_classification_without_calibration: false
yaml_mutation_authorized: false
gold_set_claim_authorized: false
semantic_gain_claim_authorized: false
expansion_pilot_promotion_authorized: false
pr_state_change_authorized: false
```

## 3. Accepted Points

Codex supervisor accepts these advisory points:

1. Three-way separation is necessary:
   - `card_survivability_issue`
   - `source_data_issue`
   - `domain_boundary_issue`
2. The three categories are not mutually exclusive.
3. A row may have multiple failure modes.
4. Tags are signals, not source of truth.
5. Subject label `회로이론` is an exam/admin label and may include control, signal/system, 4-terminal networks, transform methods, 3-phase, or power-related boundary material.
6. Damaged source rows must not be counted as card failure.
7. A calibration pass should precede full 100-row classification.
8. Calibration should be stratified rather than purely first-N or random.

## 4. Rejected Or Modified Points

Codex supervisor modifies these advisory points:

| advisory proposal | supervisor decision | reason |
|---|---|---|
| `data_integrity_score: 0..1` | reject score field | Score language conflicts with MOAI warning against scores/percentages and may imply benchmark measurement. Use enum flags instead. |
| `card_failure_score`, `source_failure_score`, `domain_boundary_score` | reject score fields | Numeric scoring invites false precision and semantic-gain style aggregation. |
| 4-way independent classification by user, Codex, Claude Web, MOAI for all calibration rows | reduce to optional advisory | Useful but too heavy as a gate prerequisite. Codex may prepare calibration rows; human review is required only for uncertain/boundary rows unless the user requests full multi-agent review. |
| `coverage_status` expansion to 8 values | partially accept | Preserve existing five primary statuses for comparability; add auxiliary fields for `domain_classification`, `card_fit_issue`, and `needs_card_combination` instead of overloading coverage status. |

## 5. Revised Classification Model

Each row should be evaluated on separate axes:

| axis | field | allowed values |
|---|---|---|
| source/data condition | `source_condition` | `usable`, `metadata_only`, `ocr_damage`, `figure_missing`, `tag_text_mismatch`, `insufficient_text`, `source_conflict` |
| domain boundary | `domain_classification` | `pure_circuit_theory`, `broad_scope_exam_circuit`, `cross_subject_control_signal`, `cross_subject_power_three_phase`, `logic_or_digital`, `contamination_or_out_of_scope`, `uncertain` |
| card survivability | `coverage_status` | `covered`, `partial`, `missing`, `over_broad`, `not_applicable` |
| card fit issue | `card_fit_issue` | `none`, `under_coverage`, `over_extension`, `wrong_card_family`, `needs_card_combination`, `pilot_only_fit`, `uncertain` |
| review need | `requires_human_review` | `true`, `false` |
| multi-failure | `multi_failure_flag` | `true`, `false` |

Rules:

- `coverage_status` is not enough by itself.
- `source_condition` must be checked before treating a row as card failure.
- `domain_classification` must be recorded before treating a row as missing coverage.
- `card_fit_issue` can be `none` even when `source_condition` or `domain_classification` is problematic.
- `multi_failure_flag` should be true when more than one axis has a non-clean value.

## 6. Calibration Decision

Before full 100-row classification, run a 20-row calibration pass.

Recommended stratification:

| stratum | count | source |
|---|---:|---|
| clean anchor rows | 5 | rows where text/tag appear coherent and baseline card mapping is likely |
| source-data suspect rows | 5 | metadata-only, OCR damage, tag/text mismatch, figure-needed, or insufficient text rows |
| domain-boundary suspect rows | 5 | control/signal/system, 4-terminal, transform, 3-phase, power, or digital/logic boundary rows |
| card-coverage boundary rows | 5 | rows likely requiring card combination, pilot-only fit, or possible under/over-coverage |

Calibration output should define practical examples for the revised fields.

## 7. Automation Decision

Allowed automation before full classification:

- detect candidate source-data issues
- detect tag/text mismatch candidates
- detect likely domain-boundary candidates using keywords
- propose card candidates
- prepare calibration table

Not allowed automatically:

- final full-row classification without calibration
- turning pressure flags into patch lists
- treating pilot-card matches as baseline coverage
- treating source-data failures as card failures
- using numeric scores or percentages

## 8. Claim Boundary

This supervisor decision does not claim:

- any row has been classified
- any card has passed or failed
- gold set completion
- benchmark status
- corpus grounding completion
- semantic gain proof
- YAML patch authorization
- `expansion_pilot` promotion to baseline
- PR #1 ready-for-review approval
- PR #1 merge approval
