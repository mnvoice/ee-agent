# Concept Card Optional Notes Corpus Grounding Gate

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Gate

Gate name:

**Optional Notes Corpus Grounding Gate**

Purpose:

- Check whether the three deferred MOAI optional notes have enough local corpus support to justify an immediate YAML patch.
- Keep advisory suggestions separate from patch authorization.
- Preserve the five original source YAML examples as seed snapshots.

This gate does not create new cards and does not patch YAML.

## 2. Pre-change Verification

| check | expected | actual | status |
|---|---:|---:|---|
| Codex concept-card YAML files | 33 | 33 | OK |
| Codex YAML structure | OK | OK | OK |
| Codex extension risk levels | LOW 19 / MEDIUM 14 | LOW 19 / MEDIUM 14 | OK |

## 3. Local Corpus Searched

Search scope:

- `data/knowledge_store_*.json`
- `docs/study/`
- `docs/prompt_engineering/explanation_generation_v0/`
- `docs/audit/concept_cards/`

Search was limited to local repository materials. This is therefore a local-corpus check, not a full external textbook grounding.

## 4. Findings

| target file | optional note | local corpus signal | supervisor decision |
|---|---|---|---|
| `power_factor_correction.yaml` | Add explicit 3-phase per-phase voltage note. | Local corpus strongly supports Y/Delta line/phase relations and 3-phase power formulas. It also contains an exam-style power factor correction item. | No immediate patch. The current card already says `single-phase or per-phase basis` and `extension_risk.condition` already requires voltage basis and Y/Delta connection basis. |
| `initial_final_value_theorems.yaml` | Mirror no-impulse condition in `formula_core`. | Local corpus supports the topic's presence and contains Laplace/impulse material, but this search did not find a direct local statement that the initial value theorem formula should be conditioned by no impulse at `t = 0`. | No immediate patch. Keep the condition in `extension_risk` only until a stronger source is available. |
| `second_order_response.yaml` | Add parallel RLC alpha formula. | Local corpus supports generic second-order damping language and contains separate serial/parallel RLC resonance material, but this search did not find a direct local statement of `alpha = 1/(2RC)` for parallel RLC. | No immediate patch. Adding the formula now could broaden the card without enough local grounding. |

## 5. Evidence Notes

Power factor and 3-phase basis:

- `data/knowledge_store_2.json` contains 3-phase line/phase relations: `V선간 = sqrt(3) V상` for Y connection and `V선간 = V상` for Delta connection.
- `data/knowledge_store_2.json` contains 3-phase power forms using line voltage/current and per-phase forms: `P = sqrt(3) VL IL cosphi`, `Q = sqrt(3) VL IL sinphi`, and `P = 3 Vp Ip cosphi`.
- `docs/prompt_engineering/explanation_generation_v0/v_next_inputs_d3/input_075.md` contains an exam-style power factor correction item using capacitor compensation.

Initial/final value theorem:

- `data/knowledge_store_3.json` lists `초기값 정리와 최종값 정리` as a high-frequency topic in the local circuit-theory index.
- `data/knowledge_store_3.json` contains Laplace-transform and unit impulse material.
- The local corpus search did not find a direct no-impulse applicability statement for the initial value theorem.

Second-order response:

- `data/knowledge_store_4.json` contains the standard second-order transfer function denominator `s^2 + 2 zeta omega_n s + omega_n^2`.
- `data/knowledge_store_4.json` states `zeta = alpha / omega_n` in second-order transient response material.
- `data/knowledge_store_2.json` contains separate serial and parallel RLC resonance material, including `Q = omega0 L / R` for series and `Q = omega0 R C` for parallel.
- The local corpus search did not find a direct parallel RLC damping formula `alpha = 1/(2RC)`.

## 6. Decision

No YAML patch is authorized.

Rationale:

- `power_factor_correction.yaml` already carries enough voltage-basis caution for the current reviewed-draft status.
- `initial_final_value_theorems.yaml` already carries the no-impulse warning in `extension_risk`; moving it into `formula_core` is a wording preference unless directly grounded.
- `second_order_response.yaml` already avoids overclaim by marking current alpha/zeta formulas as series RLC only.
- The two formula-expansion candidates would benefit from stronger source grounding before being promoted into `formula_core`.

## 7. Backlog Update

The three optional notes remain deferred.

Recommended future action:

1. Ask MOAI to review this local-corpus gate as an independent advisory check.
2. If MOAI finds a direct source-equivalent basis for any note, open a dedicated patch gate.
3. If no stronger evidence appears, keep the current YAML unchanged.

## 8. Claim Boundary

This gate does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- expansion_pilot promotion to baseline
- MOAI advisory as direct patch authorization
- external textbook-level grounding

