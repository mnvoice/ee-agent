# 100+ Problem Expansion Validation Gate Plan

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. User Proposal

User proposed expanding validation beyond the current 30-problem/card scale:

```text
30문제 갖고는 어렵고 문제를 확정을 해서 한 100문제 이상을 한 번 확대를 해서 재차 검증해보면 어떻겠느냐.
```

Supervisor interpretation:

- The proposal is feasible as a validation-gate design.
- It is not itself approval to create a gold set.
- It is not itself approval to patch YAML.
- It is not itself approval to promote `expansion_pilot` cards to baseline.
- It is not itself approval to claim semantic gain proof.

## 2. Supervisor Verdict

```yaml
supervisor_verdict: feasible_with_gate
recommended_next_step: independent_moai_advisory_on_100_plus_validation_design
yaml_mutation_authorized: false
gold_set_claim_authorized: false
semantic_gain_claim_authorized: false
expansion_pilot_promotion_authorized: false
pr_merge_authorized: false
```

## 3. Purpose

The 100+ problem expansion validation gate should test whether the current concept-card governance structure remains useful at larger scale.

It should answer:

1. Do the 30 baseline reviewed draft cards cover enough recurring problem patterns?
2. Which concepts are missing, over-broad, or underspecified?
3. Which optional notes become important under repeated problem pressure?
4. Which `expansion_pilot` cards deserve future promotion-gate consideration?
5. Is there enough evidence to design a later semantic-gain evaluation?

This gate is evidence-gathering only. It does not mutate YAML.

## 4. In Scope

Allowed work:

- define a candidate 100+ problem validation set
- record source/path for each problem
- map each problem to one or more concept cards
- classify whether the current card set is sufficient, missing, risky, or over-broad
- identify patch-gate candidates
- identify promotion-gate candidates
- identify problems that should be excluded from future canonical/gold evaluation
- prepare a MOAI review request

## 5. Out Of Scope

Not allowed in this gate:

- patch YAML
- claim a gold set
- claim corpus grounding completion
- claim semantic gain proof
- promote `expansion_pilot` cards to baseline
- merge PR #1
- move PR #1 out of draft
- treat MOAI advisory as authorization

## 6. Proposed Problem-Set Requirements

A future 100+ problem set should have:

- at least 100 problems
- stable IDs
- source path or citation for each problem
- topic/category tag
- expected relevant concept-card IDs
- difficulty/complexity tag if available
- exclusion reason for problems that are ambiguous, duplicate, or out of scope

Problem sources should be separated by evidence class:

| evidence class | meaning |
|---|---|
| local corpus | repository-local study, prompt, or knowledge-store material |
| imported audit artifact | material preserved under `docs/audit/concept_cards/` |
| external source | textbook, exam, standard, or other non-repository source |

External sources require explicit human approval before use if licensing or citation scope is unclear.

## 7. Proposed Evaluation Fields

Each problem should produce a row with:

- problem ID
- source path/citation
- topic
- relevant card(s)
- baseline coverage status: `covered`, `partial`, `missing`, `over_broad`, or `not_applicable`
- risk observation
- optional-note relevance
- `expansion_pilot` relevance
- recommended next action: `none`, `evidence_needed`, `open_patch_gate_candidate`, `open_promotion_gate_candidate`, or `exclude`

## 8. Pass/Fail Boundary

This gate should avoid a single broad PASS/FAIL unless a human supervisor defines thresholds first.

Recommended outputs instead:

- coverage distribution
- top missing concepts
- top over-broad concepts
- top optional-note pressure points
- top `expansion_pilot` pressure points
- recommended future patch gates
- recommended future promotion gates
- problems excluded from future gold-set consideration

## 9. Human Decisions Required Before Execution

A human supervisor must decide:

1. Whether to open the 100+ problem expansion validation gate.
2. Whether the problem set uses local corpus only, external sources, or both.
3. Whether the first run targets all concept cards or only high-risk/pilot candidates.
4. Whether MOAI should review the gate design before any evidence collection.
5. Whether outputs may become inputs to later patch-gate or promotion-gate workflows.

## 10. Automation Allowed Before Human Decision

Codex may automatically:

- draft this gate plan
- draft a MOAI advisory request
- prepare a blank evaluation table template
- verify PR #1 remains draft/open/unmerged
- verify no YAML mutation was introduced
- add PR comments documenting the governance state

Codex may not automatically:

- open the gate as an active validation run
- select the final 100+ problems as canonical
- patch YAML
- promote cards
- claim semantic gain
- claim gold set
- merge PR #1

## 11. Claim Boundary

This plan does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- `expansion_pilot` promotion to baseline
- YAML patch authorization
- 100+ problem set approval
- 100+ validation gate open approval
- PR #1 merge approval
