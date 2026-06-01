# MOAI Second Review Request — Concept Card Expansion Pilot Gate

작성일: 2026-05-30 KST
작성자: Codex supervisor

## 1. Role

MOAI는 generator가 아니라 independent advisory reviewer로 응답한다.

Do not create new concept cards.
Do not rewrite the full card set.
Do not claim gold set, corpus grounding completion, or semantic gain proof.

## 2. Current State To Assume

Codex-side verified state:

- `concept_cards/*.yaml`: 33 files
- YAML structure: OK
- Codex risk levels: LOW 19 / MEDIUM 14
- MOAI preserved draft: 30 entries
- MOAI preserved draft risk levels: LOW 18 / MEDIUM 12

Card status:

- 30 baseline reviewed draft cards are preserved.
- 3 expansion_pilot cards exist:
  - `q_bandwidth.yaml`
  - `power_factor_correction.yaml`
  - `initial_final_value_theorems.yaml`

Recent Codex gate:

- `concept_card_expansion_pilot_review_2026-05-30.md`
- `concept_card_33_consistency_audit_2026-05-30.md`

## 3. Review Target

Review these 7 files only:

1. `concept_cards/q_bandwidth.yaml`
2. `concept_cards/power_factor_correction.yaml`
3. `concept_cards/initial_final_value_theorems.yaml`
4. `concept_cards/thevenin_equivalent.yaml`
5. `concept_cards/balanced_three_phase.yaml`
6. `concept_cards/second_order_response.yaml`
7. `concept_cards/symmetrical_components.yaml`

## 4. Specific Questions

For each target card, answer:

| question | expected answer shape |
|---|---|
| Is the static boundary narrow enough? | yes/no + one sentence |
| Are formula conditions explicit enough? | yes/no + exact field name |
| Is `extension_risk.level` under- or over-estimated? | keep/raise/lower + reason |
| Does any dynamic destination overclaim transfer? | yes/no + target phrase |
| Does the risk/caution block prevent common misuse? | yes/no + missing caution if any |
| Should Codex patch wording be changed? | no / exact replacement suggestion |

## 5. Codex Patches To Review

Codex made only three narrow patches after pre-change review:

1. `power_factor_correction.yaml`
   - formula changed to `single-phase or per-phase basis: C = Q_C / (omega V^2)`
   - condition/caution now mentions voltage basis and Y/Delta connection basis

2. `initial_final_value_theorems.yaml`
   - condition/caution now mentions impulse boundary for initial value theorem

3. `second_order_response.yaml`
   - `alpha = R / (2 L)` is now labeled `series RLC only`

Please judge whether these are:

- sufficient,
- too broad,
- too narrow,
- or potentially misleading.

## 6. Forbidden Output

Do not output:

- new YAML cards,
- a replacement 33-card set,
- claims that the set is gold/final,
- claims that corpus grounding has been completed,
- claims that semantic gain has been proven.

## 7. Desired Output Format

Use this format:

```text
# MOAI Second Review — Expansion Pilot Gate

## Summary Verdict

| item | verdict |
|---|---|
| 7-card review | PASS / PASS_WITH_NOTES / REVISE_NEEDED |
| Codex 3 narrow patches | sufficient / needs adjustment |
| new card generation | not recommended |

## Per-card Review

| file | verdict | risk level stance | required change | forbidden claim to preserve |
|---|---|---|---|---|

## Patch Review

| Codex patch | verdict | reason | replacement wording if needed |
|---|---|---|---|

## Advisory Notes

- Keep notes short.
- Mark corpus-grounding needs as future work only.
- Do not treat advisory notes as direct authorization to patch.
```
