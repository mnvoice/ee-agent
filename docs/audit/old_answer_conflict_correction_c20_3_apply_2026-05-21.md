# Old Answer Conflict Correction — C20-3 Apply Result (2026-05-21)

Correction result log for batch C20-3. The `q.answer` field of 5
single-`source_answer` conflict items was corrected to the source PDF 【답】
marker value, in both `app/data/questions.json` and
`app/data/questions.v2.json`. Only the `answer` field was changed.

This is an apply-result record. The apply was authorized for batch C20-3 only.

- Base manifest commit: `0e6804d` (docs: draft old answer correction manifest)
- Prior completed batches:
  - C20-1 closed: `13036de` (answer) + `8f4bdf0` (solution)
  - C20-2 closed: `c7390e4` (answer) + `8ad2689` (solution)
- Design parent: `docs/audit/old_answer_conflict_correction_design_2026-05-21.md`
- Manifest: `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`
- Source review pack: `old_answer_manual_source_review_pack3_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Apply target — C20-3 (5 items)

| key | old_answer | new_answer | source_page | evidence (summary) | source ref |
| --- | ---: | ---: | --- | --- | --- |
| `2015_1회_87` | 3 | 2 | p.29 | 풀이 (231.6 옥내전로 대지전압 300V 이하) ends 【답】② | pack3 / `d4462c1` |
| `2015_2회_23` | 3 | 4 | p.9 | 풀이 (π형 회로 I_s 보정항) ends 【답】④ | pack3 / `d4462c1` |
| `2015_2회_29` | 1 | 2 | p.10 | 풀이 (② 피뢰기=이상전압 파고치 저감) ends 【답】② | pack3 / `d4462c1` |
| `2015_3회_22` | 4 | 1 | p.9 | 풀이 (제3고조파 제거=변압기 △결선) ends 【답】① | pack3 / `d4462c1` |
| `2015_3회_25` | 1 | 4 | p.9 | 풀이 (④ 반한시-정한시 특성) ends 【답】④ | pack3 / `d4462c1` |

`new_answer` equals the verified `source_answer` for every row.

## Note — `2015_3회_25` choice-OCR status

`2015_3회_25` was flagged in the review prep sheet as a possible choice-OCR
concern. The source review (pack 3) resolved it: the source PDF choices are
readable and the source 【답】 marker is clear, so the item is a confirmed
`source_answer_conflict` (not `source_choice_ocr_corrupt`). The `choices`
field is NOT modified by this step; only `answer` is corrected.

## Changed files

- `app/data/questions.json` — 5 `answer` fields updated.
- `app/data/questions.v2.json` — 5 `answer` fields updated.

## Changed field

- `answer` only. For every changed item the field-level diff is exactly
  `['answer']`. `choices`, `text`, `subject`, `q_no`, `q_type`, `difficulty`,
  `quality`, `tag`, `solution`, `steps`, `solution_svg`, and the `*_source`
  provenance fields are unchanged.

## Downstream status — answer_corrected_solution_pending

[IMPORTANT] These 5 items are in state `answer_corrected_solution_pending`:

- The `answer` field is now consistent with the source PDF 【답】 marker.
- The existing `solution` and `steps` were NOT modified and may still describe
  or conclude the **old** answer. They can be inconsistent with the corrected
  `answer`.
- `solution_svg` was NOT modified and is pending audit.
- A following step (the C20-3 solution dry-run / cleanup, analogous to C20-1
  and C20-2) must reconcile `solution` / `steps` against the source-corrected
  `answer` before these 5 items are treated as resolved.

| key | answer | solution/steps | solution_svg |
| --- | --- | --- | --- |
| `2015_1회_87` | corrected | pending regeneration | pending audit |
| `2015_2회_23` | corrected | pending regeneration | pending audit |
| `2015_2회_29` | corrected | pending regeneration | pending audit |
| `2015_3회_22` | corrected | pending regeneration | pending audit |
| `2015_3회_25` | corrected | pending regeneration | pending audit |

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- All 5 C20-3 targets exist exactly once in both files.
- All 5 targets: post `answer` == `source_answer`.
- Exactly 5 items changed in each file; no other item changed.
- For each changed item, the field-level diff is exactly `['answer']`.
- `choices` / `text` / `solution` / `steps` / metadata / `solution_svg`
  unchanged for all items.
- C20-1 / C20-2 items (10 keys) unchanged.
- C20-4 items (4 keys) unchanged.
- DQ-1 items (`2014_2회_50`, `2014_3회_62`) unchanged.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the 5 changed integer values; no
  mass reformatting.

## Status

- Q2 bulk apply remains BLOCKED.
- Apply authorization covered batch C20-3 only. C20-4 is not applied and
  requires separate per-batch approval.
- C20-1 and C20-2 are closed (answer + solution).
- DQ-1 items remain sealed pending the defective / multi-answer policy.

## Not done in this step

- No `solution` / `steps` apply or regeneration.
- No `solution_svg` modification.
- No `choices` / question text / metadata modification.
- No C20-1 / C20-2 modification.
- No C20-4 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
