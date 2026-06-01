# 100 Problem Classification Criteria

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Purpose

This document freezes row-level classification criteria for the open 100 Problem Expansion Validation Gate.

It prevents classifier drift while preserving claim boundaries.

This document does not classify any row by itself.

## 2. Coverage Status Definitions

| status | definition |
|---|---|
| `covered` | The selected problem can be handled by one or more existing baseline reviewed draft concept cards without requiring new formula scope, new caution scope, or pilot-card promotion. |
| `partial` | An existing card is relevant but incomplete for the problem; a learner would likely need an additional condition, caveat, example type, or source-grounded note. |
| `missing` | No existing baseline reviewed draft card reasonably covers the core concept needed by the problem. |
| `over_broad` | A card appears applicable only by stretching its scope beyond the card's stated boundaries or risk controls. |
| `not_applicable` | The problem is outside the concept-card target domain, too damaged to classify, duplicate/noise, or otherwise not suitable for this gate. |

## 3. Card Role Definitions

| role | definition |
|---|---|
| `primary` | The card describes the main concept needed for the problem. |
| `supporting` | The card supports the solution but is not the main concept. |
| `partial` | The card overlaps with the problem but lacks required bounded detail. |
| `mis_fit` | The card seems tempting but would mislead or overextend the card. |

## 4. Pressure Point Flags

| flag | meaning |
|---|---|
| `none` | No downstream signal. |
| `optional_note` | A deferred optional note appears relevant, but no patch is authorized. |
| `patch_candidate` | The row may justify a future patch gate after human review. |
| `promotion_candidate` | The row may support future `expansion_pilot` review, but no promotion is authorized. |
| `new_card_candidate` | The row may reveal a missing concept, but no new YAML card is authorized. |

A pressure point flag is evidence only. It is never authorization.

## 5. Pilot Handling

The three `expansion_pilot` cards may be mapped only as pilot candidates:

- `q_bandwidth.yaml`
- `power_factor_correction.yaml`
- `initial_final_value_theorems.yaml`

Rules:

- Set `is_pilot_row: true` if any pilot card is mapped.
- Keep pilot observations in a separate output section.
- Do not include pilot rows in baseline coverage counts.
- Do not claim pilot promotion from row counts.

## 6. Damaged Or Ambiguous Rows

Rows with damaged text, missing choices, obvious metadata contamination, or unresolved source conflict should be classified as one of:

- `not_applicable`, if the problem cannot support concept-card screening
- `partial`, if the concept is visible but evidence is incomplete

Damaged rows are useful as data-quality pressure signals, not as card-quality proof.

## 7. Count And Language Rules

Allowed:

- absolute counts
- row-level rationales
- candidate signals
- excluded-row list

Forbidden:

- percentages
- scores
- rankings
- benchmark wording
- gold-set wording
- semantic-gain wording
- ready-for-patch wording
- ready-for-promotion wording

## 8. Claim Boundary

This criteria record does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- YAML patch authorization
- `expansion_pilot` promotion to baseline
- 100-row classification completion
