# MOAI Advisory Record - Next Corpus-Grounding Gate Plan

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Input

Source:

- User pasted MOAI independent advisory response in the Codex thread.
- Subject under review: PR #1 draft-maintenance decision, next corpus-grounding gate preparation document, and YAML patch prohibition.

MOAI stated scope limits:

- MOAI used the decision structure provided by the user as its single input.
- MOAI did not directly read the PR #1 body, gate-preparation document body, or supervisor records in this channel.
- MOAI's review is therefore a structural-pattern assessment, not a wording-level audit.
- MOAI explicitly stated that the advisory is not patch authorization.

## 2. MOAI Verdict

```yaml
overall_verdict: PASS_WITH_NOTES
structural_pattern_assessment: sound_conservative
```

MOAI conclusion:

- Keeping PR #1 as draft is structurally conservative.
- Adding a gate-preparation document is not itself a gate-open decision.
- Prohibiting YAML patching blocks unverified claims from becoming baseline content.
- No structural-level overclaim or automation overreach was detected within MOAI's input scope.

## 3. Four-Axis Review Summary

| axis | MOAI status | supervisor reading |
|---|---|---|
| claim boundary | `respected_in_structure` | The current structure preserves draft state, preparation-only status, and no YAML mutation. |
| overclaim audit | no structural-level overclaim detected | Wording-level audit remains out of MOAI scope unless document text is supplied. |
| missing human decisions | gaps identified | Human decision records are needed before gate open, PR ready transition, optional-note priority selection, or merge. |
| automation authority overreach | none detected at described-pattern level | Automation remains limited to verification, documentation, and comments. |

## 4. High-Risk Phrases To Avoid

MOAI recommended avoiding wording that implies completed grounding, patch authorization, or merge readiness.

High-risk phrases include:

- `corpus grounding is now complete`
- `external textbook evidence collected`
- `optional notes are ready for patch`
- `gate has been opened`
- `PR #1 is effectively ready`
- `MOAI advisory authorizes the patch`
- `semantic gain demonstrated`
- `gold reference established`

Acceptable wording includes:

- `preparation for a future corpus-grounding gate`
- `candidate sources identified, not yet verified`
- `no YAML mutation authorized at this time`
- `human supervisor decision required to open the gate`

## 5. Required Safety Sentence

MOAI recommended that the preparation document explicitly preserve this boundary:

```text
This document prepares a future gate; it does not open one, does not ground any optional note, and does not authorize any YAML mutation.
```

Supervisor note:

- The existing gate-plan document already states that it is a preparation and evidence gate and not a YAML mutation gate.
- A future wording pass may add the exact sentence above if a wording-level hardening patch is opened.

## 6. Human Decisions Still Required

MOAI identified four human-only decisions that must not be automated:

1. Gate-open authority
   - Opening the corpus-grounding gate requires an explicit human supervisor decision and a separate record.
2. Draft-to-ready transition
   - Moving PR #1 from draft to ready-for-review requires human approval and preconditions.
3. Optional-note grounding priority
   - Choosing which optional note to ground first requires human priority judgment.
4. Merge authority
   - PR #1 merge approval belongs to a human reviewer/account.

## 7. Supervisor Decision

Codex supervisor accepts this MOAI advisory as independent structural review input.

No operational status is changed by this advisory.

Specifically:

- PR #1 remains draft.
- PR #1 remains unmerged.
- The next corpus-grounding gate remains prepared, not opened.
- No YAML patch is authorized.
- No `expansion_pilot` promotion is authorized.
- No gold-set, corpus-grounding-complete, or semantic-gain claim is made.

## 8. Next Governance Action

Allowed next documentation action:

- Add a human-decision checklist that separates gate-open authority, draft-promotion preconditions, optional-note priority, and merge approval.

This action is documentation-only and does not authorize YAML mutation, PR ready transition, or merge.

## 9. Claim Boundary

This record does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- `expansion_pilot` promotion to baseline
- YAML patch authorization
- corpus-grounding gate open approval
- PR #1 ready-for-review approval
- PR #1 merge approval
