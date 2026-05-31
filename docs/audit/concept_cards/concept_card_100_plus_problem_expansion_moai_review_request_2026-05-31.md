# MOAI Review Request - 100+ Problem Expansion Validation Gate

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Request

Please independently review the proposed 100+ problem expansion validation gate.

The user proposed:

```text
30문제 갖고는 어렵고 문제를 확정을 해서 한 100문제 이상을 한 번 확대를 해서 재차 검증해보면 어떻겠느냐.
```

Codex supervisor preliminary verdict:

```yaml
supervisor_verdict: feasible_with_gate
recommended_next_step: independent_moai_advisory_on_100_plus_validation_design
yaml_mutation_authorized: false
gold_set_claim_authorized: false
semantic_gain_claim_authorized: false
expansion_pilot_promotion_authorized: false
pr_merge_authorized: false
```

Please evaluate whether this verdict is conservative enough and whether the proposed gate design is safe.

## 2. Current Locked State

Assume the following current state:

- PR #1 is draft, open, and unmerged.
- Imported governance artifacts are under `docs/audit/concept_cards/`.
- Codex concept-card YAML files: 33.
- Codex YAML structure: OK.
- Codex risk levels: LOW 19 / MEDIUM 14.
- MOAI entries: 30.
- MOAI risk levels: LOW 18 / MEDIUM 12.
- MOAI previous optional-notes verdict: `PASS_WITH_NOTES`.
- MOAI YAML mutation recommendation: `false`.
- Codex supervisor decision: no YAML patch authorized.
- No gold-set claim.
- No corpus-grounding-complete claim.
- No semantic-gain-proof claim.
- No `expansion_pilot` promotion to baseline.

## 3. Proposed Gate

Gate name:

```text
100+ Problem Expansion Validation Gate
```

Purpose:

- Expand validation beyond the current 30-problem/card scale.
- Test whether the concept-card governance structure remains useful at larger scale.
- Identify missing, partial, risky, or over-broad coverage.
- Identify future patch-gate candidates.
- Identify future `expansion_pilot` promotion-gate candidates.
- Prepare evidence for a later semantic-gain evaluation without claiming semantic gain now.

## 4. Proposed Scope

Allowed:

- define a candidate 100+ problem validation set
- record source/path for each problem
- map each problem to one or more concept cards
- classify coverage as `covered`, `partial`, `missing`, `over_broad`, or `not_applicable`
- identify optional-note pressure points
- identify `expansion_pilot` pressure points
- identify future patch-gate or promotion-gate candidates
- prepare evidence tables and review records

Not allowed:

- patch YAML
- claim a gold set
- claim corpus grounding completion
- claim semantic gain proof
- promote `expansion_pilot` cards to baseline
- merge PR #1
- move PR #1 out of draft
- treat MOAI advisory as authorization

## 5. Specific Questions For MOAI

Please answer these questions:

1. Is it structurally safe to expand validation to 100+ problems under a gate, while keeping PR #1 draft and YAML unchanged?
2. Does this create any hidden overclaim risk, such as implying gold-set status or semantic-gain proof?
3. What human decisions must be made before the 100+ validation gate is actually opened?
4. Should the first 100+ validation run use local corpus only, external sources, or both?
5. Should the gate target all 33 cards, only 30 baseline reviewed draft cards, or include the 3 `expansion_pilot` cards as non-baseline candidates?
6. What minimum fields should each problem row include to make later patch/promotion decisions auditable?
7. What would be signs that this gate is drifting into unauthorized YAML mutation, baseline promotion, or gold-set claim?
8. What verdict should Codex use now: `PASS`, `PASS_WITH_NOTES`, `DEFER`, or `BLOCK`?

## 6. Expected MOAI Output Format

Please return:

```yaml
overall_verdict: PASS | PASS_WITH_NOTES | DEFER | BLOCK
structural_safety: ...
yaml_mutation_recommended: false
pr_state_change_recommended: false
gold_set_claim_authorized: false
semantic_gain_claim_authorized: false
expansion_pilot_promotion_authorized: false
required_human_decisions:
  - ...
recommended_problem_set_scope: ...
recommended_evaluation_fields:
  - ...
overclaim_risks:
  - ...
automation_overreach_risks:
  - ...
```

## 7. Claim Boundary

This request is advisory only.

It does not authorize:

- YAML mutation
- PR #1 merge
- PR #1 ready-for-review transition
- corpus-grounding gate open
- 100+ validation gate open
- gold-set claim
- semantic-gain claim
- `expansion_pilot` promotion
