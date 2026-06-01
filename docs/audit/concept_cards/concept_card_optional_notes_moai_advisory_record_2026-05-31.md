# MOAI Advisory Record — Optional Notes Corpus Grounding Gate

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Input

Source:

- User pasted MOAI independent advisory response in the Codex thread.
- Requested review packet: `concept_card_optional_notes_moai_review_request_2026-05-31.md`
- Decision under review: `concept_card_optional_notes_corpus_grounding_gate_2026-05-31.md`

MOAI stated scope limits:

- It used the request text and supplied distribution summary as its input.
- It did not directly read the Codex workspace YAML files due to TCC/channel limits.
- It did not claim direct source-file audit completion.
- It treated its response as advisory input only, not patch authorization.

## 2. MOAI Verdict

```yaml
overall_verdict: PASS_WITH_NOTES
yaml_mutation_recommended: false
```

MOAI conclusion:

- Codex's no-immediate-YAML-patch decision is defensible for all three optional notes.
- Codex did not underestimate local corpus evidence.
- Codex did not overclaim local corpus grounding.
- The three optional notes should remain in backlog.
- No optional note reaches mandatory immediate patch level.

## 3. Per-note Advisory Summary

| file | MOAI verdict | required change | advisory meaning |
|---|---|---|---|
| `power_factor_correction.yaml` | `defer_reasonable` | none mandatory | Current `single-phase or per-phase basis` wording plus Y/Delta basis caveat is sufficient for now. A 3-phase example is polish-grade pedagogy, not a correctness gap. |
| `initial_final_value_theorems.yaml` | `defer_reasonable_but_weakest` | none mandatory | This is the strongest future patch candidate because learners may read only `formula_core`; however, no immediate patch is required while no-impulse already appears in `extension_risk.condition` and `caution`. |
| `second_order_response.yaml` | `defer_reasonable` | none mandatory | Current `series RLC only:` prefix is the right defensive structure. Parallel RLC `alpha = 1/(2RC)` should wait for stronger source grounding and ideally be paired with the corresponding zeta relation. |

## 4. Priority For Future Patch Gate

If a future patch gate is opened, MOAI recommended this priority order:

1. `initial_final_value_theorems.yaml`
   - strongest pedagogical case for mirroring no-impulse condition into `formula_core`
   - requires external textbook citation or equivalent strong source grounding
2. `second_order_response.yaml`
   - possible parallel RLC alpha + zeta paired patch
   - requires external textbook citation
3. `power_factor_correction.yaml`
   - optional 3-phase per-phase voltage example
   - lowest priority because current wording already constrains voltage basis

## 5. Claim Boundary Audit

MOAI audit result:

| claim | status |
|---|---|
| gold set completion | not made |
| corpus grounding completion | not made |
| semantic gain proof | not made |
| expansion_pilot promoted to baseline | not observed |
| MOAI advisory treated as patch authorization | not observed |

MOAI explicitly noted that Codex correctly distinguished local corpus check from external textbook-level grounding.

## 6. Supervisor Decision

Codex supervisor accepts MOAI's advisory as independent review input.

No YAML patch is authorized.

Rationale:

- MOAI agreed with Codex that immediate mutation is not justified.
- MOAI found no claim-boundary violation.
- MOAI identified `initial_final_value_theorems.yaml` as the strongest future candidate, but still did not recommend immediate YAML mutation.
- The current reviewed-draft status and backlog handling remain consistent with the workflow.

## 7. Current State

Current status remains:

- 30 baseline reviewed draft cards
- 3 expansion_pilot cards
- 33 Codex YAML files
- Codex risk distribution LOW 19 / MEDIUM 14
- MOAI preserved draft 30 entries with LOW 18 / MEDIUM 12
- optional notes deferred
- no gold set claim
- no corpus-grounding-complete claim
- no semantic-gain proof claim

