# Concept Card Optional Note Backlog Decision

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Gate

Gate name:

**Optional Note Backlog / Corpus Grounding Gate**

Purpose:

- Decide whether the three deferred MOAI optional notes deserve immediate YAML patching.
- Preserve claim boundaries from the MOAI second review supervisor record.
- Avoid treating advisory notes as patch authorization.

## 2. Pre-decision Verification

Codex re-ran the required verification before making this decision.

| check | expected | actual | status |
|---|---:|---:|---|
| Codex concept card YAML files | 33 | 33 | OK |
| Codex YAML structure | OK | OK | OK |
| Codex extension risk levels | LOW 19 / MEDIUM 14 | LOW 19 / MEDIUM 14 | OK |
| MOAI entries | 30 | 30 | OK |
| MOAI extension risk levels | LOW 18 / MEDIUM 12 | LOW 18 / MEDIUM 12 | OK |

Path note:

- Requested workspace path uses `/Users/jeong-ujin_1/...`.
- Shell `pwd` resolves the accessible workspace as `/Users/jeong-ujin/...`.
- No content drift was observed in the required counts or YAML checks.

## 3. Inputs Reviewed

Required handoff and review files were read before this decision:

- `NEW_WINDOW_START_HERE_2026-05-30.md`
- `NEW_WINDOW_START_CHECKLIST_2026-05-30.md`
- `concept_card_review_summary_2026-05-30.md`
- `concept_card_expansion_pilot_review_2026-05-30.md`
- `concept_card_33_consistency_audit_2026-05-30.md`
- `moai_artifacts/circuit_theory_moai_second_review_2026-05-31.md`
- `concept_card_moai_second_review_supervisor_record_2026-05-31.md`

The three target YAML files were also inspected:

- `concept_cards/power_factor_correction.yaml`
- `concept_cards/initial_final_value_theorems.yaml`
- `concept_cards/second_order_response.yaml`

## 4. Optional Notes

| file | optional note | current YAML status | decision |
|---|---|---|---|
| `power_factor_correction.yaml` | Add optional 3-phase per-phase voltage note. | Formula already states `single-phase or per-phase basis`; `extension_risk.condition` already requires voltage basis and Y/Delta connection basis. | Backlog only; corpus grounding recommended before any formula expansion. |
| `initial_final_value_theorems.yaml` | Mirror no-impulse condition in `formula_core`. | `extension_risk.condition` and `caution` already include the impulse boundary. | Backlog only; low urgency wording refinement. |
| `second_order_response.yaml` | Add optional parallel RLC alpha formula. | Current formula explicitly labels series RLC alpha and zeta formulas. | Backlog only; patching now may broaden scope without corpus grounding. |

## 5. Supervisor Decision

No YAML patch is authorized in this gate.

Rationale:

- MOAI second review judged the existing Codex narrow patches sufficient.
- All three remaining notes were explicitly optional.
- The active YAML cards already preserve the relevant misuse boundaries.
- Adding optional formulas now could broaden scope or introduce convention choices without corpus grounding.
- A future patch gate should start from a corpus-grounded source check, not from advisory preference alone.

## 6. Backlog Status

The three optional notes remain deferred.

Recommended future handling:

1. Open a dedicated corpus grounding gate if these notes become important for learner-facing precision.
2. Before patching, create a pre-change review record with source/corpus evidence.
3. Keep any patch narrow and condition-prefixed.
4. Re-run the 33-card YAML structure and risk distribution checks after any patch.

## 7. Claim Boundary

This decision does not claim:

- 33-card gold set completion
- corpus grounding completion
- semantic gain proof
- expansion_pilot promotion to baseline
- MOAI advisory as direct patch authorization
- new card creation

Current status remains:

- 30 baseline reviewed draft cards
- 3 expansion_pilot cards
- 33 Codex YAML files
- Codex risk distribution LOW 19 / MEDIUM 14
- MOAI preserved draft 30 entries with LOW 18 / MEDIUM 12

