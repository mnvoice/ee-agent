# Next Corpus-Grounding Gate Plan

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. User Decision

User-approved operating decision:

```text
PR #1은 지금 merge하지 말고 draft로 유지한다. 다음은 corpus-grounding gate 준비로 간다.
```

Supervisor interpretation:

- Keep PR #1 as a draft review container.
- Do not merge PR #1 in this step.
- Do not close or delete PR #1 in this step.
- Do not patch YAML in this step.
- Prepare the next corpus-grounding gate as a separate decision surface.

## 2. Current State

Current imported packet state remains:

- PR #1 is draft and unmerged.
- Imported artifacts are under `docs/audit/concept_cards/`.
- Codex concept-card YAML files: 33.
- Codex YAML structure: OK.
- Codex risk distribution: LOW 19 / MEDIUM 14.
- MOAI preserved draft entries: 30.
- MOAI risk distribution: LOW 18 / MEDIUM 12.
- MOAI optional-notes advisory verdict: `PASS_WITH_NOTES`.
- MOAI YAML mutation recommendation: `false`.
- Codex supervisor decision: no YAML patch authorized.

## 3. Gate Purpose

The next corpus-grounding gate should answer this narrow question:

```text
Which, if any, deferred optional notes or expansion candidates have enough source/corpus support to justify opening a future YAML patch gate?
```

This is a preparation and evidence gate. It is not itself a YAML mutation gate.

## 4. In Scope

The next gate may inspect and summarize evidence for:

- deferred optional notes from the MOAI advisory path
- `initial_final_value_theorems.yaml` as the strongest future patch-gate candidate
- any source/corpus passages that directly support or weaken a proposed card wording change
- whether evidence is local-corpus only or externally grounded
- whether any candidate should remain backlog-only

## 5. Out Of Scope

The next gate must not:

- patch YAML
- claim gold set completion
- claim corpus grounding completion
- claim semantic gain proof
- promote `expansion_pilot` cards to baseline
- treat MOAI advisory as patch authorization
- merge PR #1
- convert PR #1 out of draft

## 6. Required Inputs

Minimum inputs for the next gate:

- `concept_card_optional_note_backlog_decision_2026-05-31.md`
- `concept_card_optional_notes_corpus_grounding_gate_2026-05-31.md`
- `concept_card_optional_notes_moai_advisory_record_2026-05-31.md`
- `concept_cards/index.md`
- relevant target YAML files, read-only
- relevant local corpus/source files, read-only

If external grounding is used, it must be recorded separately from local-corpus evidence.

## 7. Required Output

The next gate should produce a review record with:

- candidate file
- proposed future change, if any
- evidence source path or citation
- evidence strength
- risks or convention dependencies
- supervisor decision: `open_patch_gate`, `defer`, or `reject`

Allowed decisions:

| decision | meaning |
|---|---|
| `open_patch_gate` | Evidence may justify a separate future YAML patch gate. This does not patch YAML by itself. |
| `defer` | Candidate remains in backlog pending stronger grounding. |
| `reject` | Candidate should not be pursued under current claim boundaries. |

## 8. Human-Required Decisions

A human must decide before any later promotion or mutation:

1. Whether PR #1 should ever be merged into official repository history.
2. Whether any corpus-grounding result is strong enough to open a YAML patch gate.
3. Whether external textbook-level grounding is required for a specific candidate.
4. Whether any `expansion_pilot` card may be considered for baseline promotion.

## 9. Automation-Allowed Work

Codex supervisor may automatically:

- verify PR #1 remains draft/open/unmerged
- verify changed paths remain under `docs/audit/concept_cards/`
- verify YAML count and structure remain unchanged
- prepare read-only evidence tables
- draft a future patch-gate request
- add PR comments documenting the current decision

Codex supervisor may not automatically merge, close, delete, promote, or mutate YAML without a new explicit user decision.

## 10. Claim Boundary

This plan does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- `expansion_pilot` promotion to baseline
- YAML patch authorization
- PR #1 merge approval
