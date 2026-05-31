# 100 Problem Gate Close Criteria

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This document defines when the open 100 Problem Expansion Validation Gate may be closed.

It does not close the gate by itself.

## 2. Required Close Conditions

The gate may close only after all required outputs exist:

| output | required condition |
|---|---|
| problem inventory | 100 selected rows identified by stable source rule |
| row-level table | all 100 rows classified or explicitly marked `not_applicable` |
| baseline section | 30 baseline reviewed draft cards reported separately |
| pilot section | 3 `expansion_pilot` cards reported separately as `pilot_candidate_only` |
| excluded-row section | damaged, duplicate, noisy, or out-of-domain rows listed |
| pressure-point section | optional-note, patch, promotion, or new-card candidate signals listed as signals only |
| MOAI review request | completed table prepared for independent advisory |
| supervisor closeout | human-readable closeout record preserving claim boundaries |

## 3. Required Human Close Decision

A human supervisor must approve gate close.

Gate close must not be inferred automatically from row count, coverage count, or MOAI advisory.

## 4. Closeout Must Preserve These Non-Authorizations

A gate closeout must state:

```yaml
yaml_mutation_authorized: false
gold_set_claim_authorized: false
semantic_gain_claim_authorized: false
expansion_pilot_promotion_authorized: false
pr_state_change_authorized: false
```

If the human supervisor wants any downstream action, that action must open a separate gate.

## 5. Forbidden Closeout Claims

The closeout must not claim:

- 100 rows are a gold set
- 100 rows are a benchmark
- semantic gain was proven
- corpus grounding is complete
- any card is promoted
- any YAML patch is approved
- PR #1 is ready to merge

## 6. Claim Boundary

This close-criteria record does not claim:

- gate completion
- gold set completion
- corpus grounding completion
- semantic gain proof
- YAML patch authorization
- `expansion_pilot` promotion to baseline
- PR #1 ready-for-review approval
- PR #1 merge approval
