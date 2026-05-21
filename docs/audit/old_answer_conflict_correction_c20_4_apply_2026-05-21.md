# Old Answer Conflict Correction — C20-4 Apply Result (2026-05-21)

Correction result log for batch C20-4. The `q.answer` field of 4
single-`source_answer` conflict items was corrected to the source PDF 【답】
marker value, in both `app/data/questions.json` and
`app/data/questions.v2.json`. Only the `answer` field was changed.

C20-4 is the final batch of the 19-item single-answer correction set.

This is an apply-result record. The apply was authorized for batch C20-4 only.

- Base manifest commit: `0e6804d` (docs: draft old answer correction manifest)
- Prior completed batches:
  - C20-1 closed: `13036de` (answer) + `8f4bdf0` (solution)
  - C20-2 closed: `c7390e4` (answer) + `8ad2689` (solution)
  - C20-3 closed: `8a6a961` (answer) + `5f80afa` (solution)
- Design parent: `docs/audit/old_answer_conflict_correction_design_2026-05-21.md`
- Manifest: `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`
- Source review pack: `old_answer_manual_source_review_pack3_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Apply target — C20-4 (4 items)

| key | old_answer | new_answer | source_page | evidence (summary) | source ref |
| --- | ---: | ---: | --- | --- | --- |
| `2016_1회_44` | 2 | 4 | p.15 | 풀이 (전기자 반작용 영향 4종) ends 【답】④ | pack3 / `d4462c1` |
| `2016_1회_69` | 1 | 4 | p.23 | 풀이 (고유주파수는 안정도와 무관) ends 【답】④ | pack3 / `d4462c1` |
| `2016_1회_70` | 2 | 4 | p.23 | 풀이 (Nyquist 임계점 -1+j0 → 0dB, ±180°) ends 【답】④ | pack3 / `d4462c1` |
| `2016_3회_21` | 1 | 4 | p.7 | 풀이 (전선 단면적 A ∝ 1/V²) ends 【답】④ | pack3 / `d4462c1` |

`new_answer` equals the verified `source_answer` for every row.

## Note — `2016_1회_44` choice-OCR status

`2016_1회_44` was flagged in the review prep sheet as a possible
choice / OCR / wording-ambiguity concern. The source review (pack 3) resolved
it: the source PDF choices are readable and the source 【답】 marker is clearly
④, so the item is a confirmed `source_answer_conflict` (not
`source_choice_ocr_corrupt`). The `choices` field is NOT modified by this
step; only `answer` is corrected.

## Changed files

- `app/data/questions.json` — 4 `answer` fields updated.
- `app/data/questions.v2.json` — 4 `answer` fields updated.

## Changed field

- `answer` only. For every changed item the field-level diff is exactly
  `['answer']`. `choices`, `text`, `subject`, `q_no`, `q_type`, `difficulty`,
  `quality`, `tag`, `solution`, `steps`, `solution_svg`, and the `*_source`
  provenance fields are unchanged.

## Downstream status — answer_corrected_solution_pending

[IMPORTANT] These 4 items are in state `answer_corrected_solution_pending`:

- The `answer` field is now consistent with the source PDF 【답】 marker.
- The existing `solution` and `steps` were NOT modified and may still describe
  or conclude the **old** answer. They can be inconsistent with the corrected
  `answer`.
- `solution_svg` was NOT modified and is pending audit.
- A following step (the C20-4 solution dry-run / cleanup, analogous to C20-1,
  C20-2, C20-3) must reconcile `solution` / `steps` against the
  source-corrected `answer` before these 4 items are treated as resolved.

| key | answer | solution/steps | solution_svg |
| --- | --- | --- | --- |
| `2016_1회_44` | corrected | pending regeneration | pending audit |
| `2016_1회_69` | corrected | pending regeneration | pending audit |
| `2016_1회_70` | corrected | pending regeneration | pending audit |
| `2016_3회_21` | corrected | pending regeneration | pending audit |

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- All 4 C20-4 targets exist exactly once in both files.
- All 4 targets: post `answer` == `source_answer`.
- Exactly 4 items changed in each file; no other item changed.
- For each changed item, the field-level diff is exactly `['answer']`.
- `choices` / `text` / `solution` / `steps` / metadata / `solution_svg`
  unchanged for all items.
- C20-1 / C20-2 / C20-3 items (15 keys) unchanged.
- DQ-1 items (`2014_2회_50`, `2014_3회_62`) unchanged.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the 4 changed integer values; no
  mass reformatting.

## Status

- Q2 bulk apply remains BLOCKED.
- C20-4 is the final batch of the 19-item single-answer correction set. With
  this step, all 19 single-`source_answer` conflict items have had their
  `q.answer` corrected.
- C20-1, C20-2, C20-3 are closed (answer + solution).
- C20-4 `answer` correction is complete; the C20-4 solution dry-run / cleanup
  is the remaining step before C20-4 closes.
- DQ-1 items remain sealed pending the defective / multi-answer policy.

## Not done in this step

- No `solution` / `steps` apply or regeneration.
- No `solution_svg` modification.
- No `choices` / question text / metadata modification.
- No C20-1 / C20-2 / C20-3 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
