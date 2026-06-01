# Concept Card Governance Index

This folder preserves the concept-card governance import for PR #1.

It is an audit and review packet, not a content patch gate. The files here make the concept-card work easy to review from GitHub or iPad while keeping the current claim boundaries explicit.

## Open First On iPad

Start here:

1. [`concept_card_governance_import_closeout_2026-05-31.md`](concept_card_governance_import_closeout_2026-05-31.md) - final import closeout, verification counts, MOAI verdict, and PR-state recommendation.
2. [`concept_cards/index.md`](concept_cards/index.md) - list of the 33 Codex YAML concept cards.
3. [`IMPORT_MANIFEST_2026-05-31.md`](IMPORT_MANIFEST_2026-05-31.md) - import scope, source workspace, branch, and rollback notes.

For a quick review pass, read the closeout first, then the nested card index.

## Current Status

- PR #1 is draft and unmerged.
- Imported artifacts are confined to `docs/audit/concept_cards/`.
- MOAI reviewed the optional notes corpus-grounding gate.
- MOAI verdict: `PASS_WITH_NOTES`.
- MOAI recommended YAML mutation: `false`.
- Codex supervisor decision: no YAML patch authorized.
- Current semantic status: 30 baseline reviewed draft cards, 3 `expansion_pilot` cards, optional notes deferred.

Latest verification state:

| check | status |
|---|---:|
| Codex YAML files | 33 |
| Codex YAML structure | OK |
| Codex risk levels | LOW 19 / MEDIUM 14 |
| MOAI entries | 30 |
| MOAI risk levels | LOW 18 / MEDIUM 12 |

## Codex YAML Cards

The Codex-authored concept-card YAML files are in:

```text
docs/audit/concept_cards/concept_cards/
```

Use [`concept_cards/index.md`](concept_cards/index.md) as the card list. It identifies 30 baseline draft cards and 3 `expansion_pilot` cards.

## MOAI Artifacts

MOAI artifacts are in:

```text
docs/audit/concept_cards/moai_artifacts/
```

Key files:

- [`moai_artifacts/circuit_theory_concept_cards_independent_draft_v0.1.yaml`](moai_artifacts/circuit_theory_concept_cards_independent_draft_v0.1.yaml)
- [`moai_artifacts/circuit_theory_concept_cards_independent_draft_v0.1_review_table.md`](moai_artifacts/circuit_theory_concept_cards_independent_draft_v0.1_review_table.md)
- [`moai_artifacts/circuit_theory_concept_cards_codex_vs_moai_comparison_v0.1.md`](moai_artifacts/circuit_theory_concept_cards_codex_vs_moai_comparison_v0.1.md)
- [`moai_artifacts/circuit_theory_tierB_note_merge_and_pilot_advisory_v0.1.md`](moai_artifacts/circuit_theory_tierB_note_merge_and_pilot_advisory_v0.1.md)
- [`moai_artifacts/circuit_theory_moai_second_review_2026-05-31.md`](moai_artifacts/circuit_theory_moai_second_review_2026-05-31.md)

## Claim Boundaries

This folder does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- `expansion_pilot` promotion to baseline
- MOAI advisory as YAML patch authorization

Do not patch YAML from this packet unless a new gate explicitly authorizes it.

## Next Gates

Recommended next gates before any content promotion:

1. Decide whether PR #1 should remain a draft review container or become official repository history.
2. Run a corpus-grounding gate before any optional notes are merged into YAML.
3. Require a new explicit patch gate before mutating any YAML card.
4. Treat `initial_final_value_theorems.yaml` as the strongest future patch-gate candidate only if stronger source grounding is provided.
5. Keep `expansion_pilot` cards out of baseline unless a separate promotion gate approves them.

## PR Handling

Keep PR #1 as draft unless the user explicitly decides otherwise.

Do not merge PR #1 from this README task.
