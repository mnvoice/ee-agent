# T3.5 Regeneration Decision Log

Date: 2026-05-20
Branch: `feat/phase-b-migration`

## Context

The project is migrating from answer-mismatch detection toward answer-locked solution regeneration.

Core finding:

- `q.answer` is the answer SoT.
- For 2025-2026, PDF `[정답]` answer tables were extracted and matched `q.answer` 400/400.
- Latest P1 answer mismatch cases were not answer errors. They were LLM-generated solution conclusion errors.
- Therefore the LLM should not choose the answer. It should explain the already-fixed answer.

## Gate Roles

Use different levels of strictness by gate:

| Gate | Role | Strictness |
| --- | --- | --- |
| G3 source answer check | Verify `q.answer` against PDF/source answer | precise |
| G1 automatic validation | Check conclusion number, answer choice text, PUA/FFFD, output shape | precise |
| G2 human QA | Spot check generated explanations for obvious quality problems | coarse |

G2 is not answer verification.

Human reviewers should not solve the problem again and should not compare every item against the textbook. G2 only asks whether the explanation is embarrassing or unsafe to show to a beginner.

## T3.5-F2 Decision

Proposed:

- Regenerate the 22-item QA review sheet with a simpler 4-item spot-check rubric.

Decision:

- Skip T3.5-F2 for the current batch.

Reason:

- Claude already evaluated the existing 22-item QA sheet.
- The result is actionable enough for this batch.
- Rebuilding the review sheet now would not change the decision materially.
- The simplified rubric should be used for the next batch, not retroactively for this one.

Carry forward:

- Add the simplified G2 policy to future review sheets.

## G2 Result Interpreted

Claude G2 review result:

- PASS: 21
- RETRY: 0
- FAIL: 1
- Automatic fail criteria: 0

Failed item:

- `2025_3회_79`
- Category: concept
- Cause: figure/block-diagram dependent problem.
- The generated explanation was too generic because figure-derived analysis is intentionally not available.

Interpretation:

- This is not a q.answer problem.
- This is not an answer-locked regeneration policy failure.
- This is a figure-dependent input limitation.

## Next Track

Run T3.5-G:

1. Hold `2025_3회_79` as `hold_figure_dependent`.
2. Sweep all 77 regenerated items for figure-dependent cases.
3. Split staging into:
   - apply candidates
   - hold candidates
4. Recompute G2 after hold exclusions.
5. Do not modify `questions.json`, `questions.v2.json`, `app/index.html`, or `data/pdf_pages` during this audit.

## T3.5-G Outcome

T3.5-G completed as a read-only audit.

Result:

- Apply candidates: 74
- Hold candidates: 3
- Data changes: 0

Hold candidates:

| Key | Reason |
| --- | --- |
| `2025_2회_60` | Figure-dependent DC machine winding identification. The regenerated explanation inferred the winding structure from `q.answer`. |
| `2025_3회_79` | Block-diagram comparison problem. This was the Claude G2 FAIL item. |
| `2026_1회_67` | Gate-circuit diagram identification. The regenerated explanation inferred the circuit structure from `q.answer`. |

One additional figure-keyword candidate, `2025_2회_45`, remains apply-eligible because the text states enough information without the figure (`가극성 변압기`) for the calculation to stand.

Updated G2 interpretation:

- Effective sample after hold exclusion: 21
- Effective sample PASS: 21/21
- Category effective pass rates:
  - calculation: 5/5
  - regulation: 5/5
  - concept: 11/11

Decision:

- Do not apply all 77 regenerated solutions.
- Treat the 3 figure-dependent cases as hold items for a separate figure/crop-backed track.
- The 74 apply candidates may proceed to G4 patch staging and user approval.

Policy carry-forward:

- Figure-dependent problems must be detected before answer-locked regeneration is applied.
- If the explanation only works by reverse-engineering `q.answer` without access to the figure, hold it.
- Regulation items should not invent KEC/article numbers. Missing article numbers are not a hard failure by themselves; invented article numbers are a failure.

## T3.5-H Dry-Run Outcome

T3.5-H completed as a read-only dry-run.

Result:

- Apply candidates: 74
- Missing keys in `questions.json`: 0
- Missing keys in `questions.v2.json`: 0
- Old hash drift: 0
- File changes made: 0

Dry-run change plan:

| File | Fields |
| --- | --- |
| `app/data/questions.json` | `solution`, `steps` |
| `app/data/questions.v2.json` | `solution`, `steps`, `solution_source`, `steps_source` |

Change count:

- `solution`: 74
- `steps`: 74
- `questions.v2.json` source metadata: 74 `solution_source` + 74 `steps_source`

Recommended v2 source metadata policy:

- Keep `source: "llm_synthesized"` because the regenerated explanation is still LLM-authored.
- Set `tool_name: "answer-locked-regen-T3.5"` to distinguish these from earlier free-form LLM solutions.
- Set `verified_at` to the apply timestamp because the batch passed source-answer locking, automatic validation, and G2 sampling QA.

Recommended apply procedure:

1. Re-run `/tmp/patch_apply_drift_check.py`.
2. Apply all 74 candidates to both JSON files in one operation.
3. Keep the 3 figure-dependent cases excluded.
4. Update `/tmp` staging only if needed for bookkeeping; repo data remains the actual patch target.
5. Run G5 app verification at `http://localhost:8001/`.

Decision pending:

- User approval for T3.5-I actual apply.
- Whether to use the recommended v2 source metadata policy above.

## Future G2 Rubric

Use a coarse 4-item spot check:

1. Does the explanation make sense?
2. Is the calculation or logic flow natural?
3. Does it avoid inventing evidence, law articles, or source facts?
4. Is it understandable for a beginner?

Per item:

- `OK`
- `suspicious`
- `NG`

Final item verdict:

- `PASS`: no `NG`, at most one `suspicious`
- `RETRY`: no `NG`, two or more `suspicious`
- `FAIL`: one or more `NG`

Batch pass guideline:

- FAIL: 0
- RETRY: 2 or fewer
- PASS: at least 20 of 22
- Category pass rates:
  - calculation: at least 4 of 5
  - regulation: at least 4 of 5
  - concept: at least 10 of 12

Important: G2 is a smell test, not expert answer verification.

## T3.5-I Apply Outcome

T3.5-I applied the 74 apply candidates to both data files after user approval.

Result:

- Drift check (`patch_apply_drift_check.py`): exit 0, 0 drift, 0 missing keys.
- Applied: 74/74 to `app/data/questions.json` and `app/data/questions.v2.json`.
- Post-apply hash verification: 0 mismatch on both files.
- `answer_mismatch` recheck on the 74 applied items: 0 remaining on both files.
- Hold items (`2025_2회_60`, `2025_3회_79`, `2026_1회_67`): unchanged, not applied.
- Apply timestamp: `2026-05-20T13:09:55+09:00`.

Format-preservation catch:

- The first apply pass wrote `questions.v2.json` with `json.dump(indent=2)`, but the
  original file is compact single-line. This reformatted the whole file (~294k line diff).
- Corrected: restored the original via `git show HEAD`, then re-applied the 74 items
  with compact serialization (`separators=(',',':')`), preserving the original format.
- `questions.json` was unaffected because its original format is already indent=2.

v2 source metadata applied:

- `solution_source` / `steps_source` for the 74 items set to
  `{source: "llm_synthesized", tool_name: "answer-locked-regen-T3.5", verified_at: <apply timestamp>}`.
- Hold items keep their previous `tool_name` (unchanged).

Final diff:

- `app/data/questions.json`: 535 line change (74 items, indent=2 preserved).
- `app/data/questions.v2.json`: compact single-line file (line-level diff not meaningful).

Gate status:

- G4 (data apply): complete.
- G5 (post-apply app verification): pending at `http://localhost:8001/`.
