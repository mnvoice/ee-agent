# MOAI Advisory Record - 100+ Problem Expansion Validation Gate

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Input

Source:

- User pasted MOAI independent advisory response in the Codex thread.
- Subject under review: proposed `100+ Problem Expansion Validation Gate`.
- Prior request: `concept_card_100_plus_problem_expansion_moai_review_request_2026-05-31.md`.

MOAI stated scope limits:

- MOAI used the gate proposal, supervisor preliminary verdict, and current locked state as a single input.
- MOAI did not directly read PR #1, `docs/audit/concept_cards/`, or prior review records in this channel.
- MOAI's review is a gate-design-pattern assessment.
- MOAI explicitly stated that it does not open the gate and does not authorize patch, merge, promotion, or claims.

## 2. MOAI Verdict

```yaml
overall_verdict: PASS_WITH_NOTES
structural_safety: structurally_safe_if_bounded
yaml_mutation_recommended: false
pr_state_change_recommended: false
gold_set_claim_authorized: false
semantic_gain_claim_authorized: false
expansion_pilot_promotion_authorized: false
```

MOAI conclusion:

- Expanding to 100+ problems under a draft-PR and YAML-frozen gate is structurally safer than staying at the 30-problem scale if the gate is tightly bounded.
- Codex's preliminary verdict, `feasible_with_gate`, is conservative enough at the authorization layer.
- The design needs supplementary safeguards before the gate can be opened.

## 3. Required Human Decisions

MOAI identified these human-required decisions before any 100+ validation gate can open:

| decision | reason |
|---|---|
| problem-set selection authority | Problem selection is the largest hidden gold-set risk and must be owned by a named human supervisor. |
| problem-set provenance policy | Source classes must be declared and labeled per row. |
| target-count freeze | `100+` is proposal language only; the active gate must freeze a single integer target count. |
| coverage-classification criteria | Definitions for `covered`, `partial`, `missing`, `over_broad`, and `not_applicable` must be frozen before classification. |
| gate-open decision | A separate human-signed record must convert preparation into an open gate. |
| gate-close decision | Exit criteria and a human-signed close record are required. |
| output-use authority | Pressure-point flags must not automatically trigger patch, promotion, or new-card work. |

## 4. Recommended Scope

MOAI recommended:

- Target all 33 cards.
- Draw the problem set independently of the card list.
- Do not construct the problem set by walking the cards and writing one problem per card.
- Prefer a fixed, declared local exam-source range for the first run.
- Map each problem to zero, one, or many cards after problem selection.
- Report the 30 baseline reviewed draft cards separately from the 3 `expansion_pilot` cards.
- Tag pilot rows as `pilot_candidate_only`.
- Exclude pilot rows from baseline coverage counts.

## 5. Recommended Evaluation Fields

MOAI recommended these row fields:

- `problem_id`
- `source`
- `source_provenance`
- `problem_text_or_ref`
- `domain`
- `concept_card_mapping`
- `card_role`
- `coverage_status`
- `coverage_rationale`
- `pressure_point_flag`
- `pressure_rationale`
- `is_pilot_row`
- `gold_set_disclaimer`
- `review_status`
- `timestamp_utc`
- `notes`

Supervisor note:

- `gold_set_disclaimer` should be a constant statement such as: `this row is not a gold standard, this row is not a benchmark`.
- `notes` must avoid score language.

## 6. Overclaim Risks

MOAI identified these overclaim risks:

- percentage or score language implying semantic-gain measurement
- benchmark, gold set, reference set, or evaluation suite framing
- baseline-vs-pilot comparisons that imply promotion
- pressure-point flags being treated as authorization
- unilateral classifier authority without spot-checking
- corpus-grounding creep from mixing external textbook material into the first run

## 7. Automation Overreach Risks

MOAI identified these automation-overreach risks:

- auto-triggering YAML edits from `patch_candidate` flags
- auto-generating new YAML card stubs from `missing` rows
- auto-promoting pilot cards from covered counts
- moving PR #1 from draft to ready through automation
- silently changing labels, milestones, or project-board status
- recasting MOAI advisory as approval
- adding rows beyond the frozen target count mid-run

## 8. Supervisor Decision

Codex supervisor accepts MOAI's advisory as independent gate-design input.

No operational status is changed by this advisory.

Specifically:

- PR #1 remains draft.
- PR #1 remains unmerged.
- The 100+ validation gate remains proposed, not opened.
- No problem set is approved.
- No target count is frozen.
- No YAML patch is authorized.
- No card promotion is authorized.
- No gold-set, corpus-grounding-complete, or semantic-gain claim is made.

## 9. Required Follow-Up Before Gate Open

Before opening the 100+ validation gate, create or obtain human approval for:

1. problem-set selection authority
2. provenance policy
3. target-count freeze
4. coverage-classification criteria
5. gate-open record
6. gate-close criteria
7. output-use authority

## 10. Claim Boundary

This record does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- `expansion_pilot` promotion to baseline
- YAML patch authorization
- 100+ problem-set approval
- 100+ validation gate open approval
- PR #1 ready-for-review approval
- PR #1 merge approval
