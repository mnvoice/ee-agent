# New Window Start Checklist

Use this as the first checklist in the new window.

## 1. Verify Location

- [x] Workspace is accessible via `/Users/jeong-ujin_1/Documents/Codex/2026-05-30/ee-agent-d-3-governance-repo`; shell `pwd` resolves it as `/Users/jeong-ujin/Documents/Codex/2026-05-30/ee-agent-d-3-governance-repo`
- [x] `concept_cards/` exists
- [x] `moai_artifacts/` exists

## 2. Verify Codex Cards

- [x] `find concept_cards -maxdepth 1 -type f -name '*.yaml' | wc -l` returns `33`
- [x] Ruby YAML structure check returns `structure=OK`
- [x] Risk distribution is `LOW 19 / MEDIUM 14`

## 3. Verify MOAI Artifacts

- [x] `moai_artifacts/circuit_theory_concept_cards_independent_draft_v0.1.yaml` exists
- [x] Python YAML load returns `30`
- [x] MOAI risk distribution is `LOW 18 / MEDIUM 12`
- [x] `moai_artifacts/circuit_theory_concept_cards_codex_vs_moai_comparison_v0.1.md` exists
- [x] `moai_artifacts/circuit_theory_tierB_note_merge_and_pilot_advisory_v0.1.md` exists

## 4. Verify Current Records

- [x] `concept_card_tierB_patch_record_2026-05-30.md` exists
- [x] `concept_card_supervisor_decision_memo_2026-05-30.md` exists
- [x] `concept_card_review_summary_2026-05-30.md` exists
- [x] `concept_card_expansion_backlog_2026-05-30.md` exists

## 5. Next Gate

- [x] Create `concept_card_expansion_pilot_review_2026-05-30.md` before editing.
- [x] Review 3 expansion pilots.
- [x] Review 4 note-merged cards.
- [x] Do not create new cards unless instructed.
- [x] Do not claim gold set.

## 6. If Drift Occurs

If any expected count or file is missing:

- [ ] Stop normal flow.
- [ ] Create a drift note.
- [ ] State actual vs expected.
- [ ] Recommend safe next action.
