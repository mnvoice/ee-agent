# Concept Card Human Decision Checklist

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This checklist separates actions Codex may prepare from decisions only a human supervisor may make.

It responds to the MOAI advisory on the PR #1 draft-maintenance and next corpus-grounding gate plan.

This checklist is documentation-only.

It does not open a corpus-grounding gate, does not authorize YAML mutation, does not move PR #1 out of draft, and does not approve merge.

## 2. Current Locked State

Current state remains:

- PR #1 is draft.
- PR #1 is open and unmerged.
- Imported artifacts remain under `docs/audit/concept_cards/`.
- No YAML patch is authorized.
- No `expansion_pilot` promotion is authorized.
- No gold-set, corpus-grounding-complete, or semantic-gain claim is made.

## 3. Human-Only Decisions

| decision | current status | human action required |
|---|---|---|
| Open corpus-grounding gate | not opened | Human must approve a separate gate-open decision record. |
| Select grounding priority | not selected | Human must choose whether to start with `initial_final_value_theorems.yaml`, another optional note, or a grouped review. |
| Decide evidence standard | not selected | Human must choose local-corpus-only, external textbook/source grounding, or both. |
| Move PR #1 from draft to ready | not approved | Human must approve after preconditions are met. |
| Merge PR #1 | not approved | Human must approve through PR review or explicit merge instruction. |
| Patch YAML | not approved | Human must approve a separate patch gate after evidence review. |
| Promote `expansion_pilot` to baseline | not approved | Human must approve a separate promotion gate. |

## 4. Draft-To-Ready Preconditions

Before PR #1 may move from draft to ready-for-review, a human should confirm:

- The purpose of PR #1 is still archival/governance import, not content promotion.
- The README/index is sufficient for iPad review.
- All claim boundaries are still explicit.
- No YAML mutation has been added without a patch gate.
- Any corpus-grounding work is clearly marked as preparation, advisory, or completed gate output.
- Merge remains a separate decision from ready-for-review.

## 5. Gate-Open Preconditions

Before opening the next corpus-grounding gate, a human should decide:

- target scope: one candidate or grouped optional notes
- evidence standard: local corpus, external sources, or both
- output format: evidence table, supervisor record, MOAI review packet, or all three
- success criterion: `open_patch_gate`, `defer`, or `reject`
- whether MOAI wording-level audit is required after Codex drafts the gate output

## 6. Optional-Note Priority Candidates

Known candidates from the current records:

| candidate | current advisory status | priority note |
|---|---|---|
| `initial_final_value_theorems.yaml` | strongest future patch-gate candidate | Consider first only if stronger source grounding is required and available. |
| `second_order_response.yaml` | deferred | Parallel RLC formula expansion needs stronger grounding and convention handling. |
| `power_factor_correction.yaml` | deferred | Current wording already carries voltage-basis caution; likely lower priority. |

This table does not select a priority. It only preserves the candidate set for human choice.

## 7. Automation Allowed Before Human Decision

Codex may prepare:

- read-only evidence tables
- source/citation inventories
- MOAI review request drafts
- PR comments documenting the current status
- verification that PR #1 remains draft/open/unmerged
- verification that YAML count and structure remain unchanged

Codex may not automatically:

- open the gate as a completed decision
- patch YAML
- move PR #1 out of draft
- merge PR #1
- close or delete PR #1
- promote `expansion_pilot` cards
- claim gold set, corpus grounding completion, or semantic gain proof

## 8. Claim Boundary

This checklist does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- `expansion_pilot` promotion to baseline
- YAML patch authorization
- gate-open approval
- draft-to-ready approval
- merge approval
