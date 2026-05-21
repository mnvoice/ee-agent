# Old Answer Conflict Correction — C20-2 Apply Result (2026-05-21)

Correction result log for batch C20-2. The `q.answer` field of 5
single-`source_answer` conflict items was corrected to the source PDF 【답】
marker value, in both `app/data/questions.json` and
`app/data/questions.v2.json`. Only the `answer` field was changed.

This is an apply-result record. The apply was authorized for batch C20-2 only.

- Base manifest commit: `0e6804d` (docs: draft old answer correction manifest)
- Prior completed batch:
  - C20-1 answer correction — `13036de`
  - C20-1 solution cleanup — `8f4bdf0`
- Design parent: `docs/audit/old_answer_conflict_correction_design_2026-05-21.md`
- Manifest: `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`
- Source review packs: `old_answer_manual_source_review_pack{,2}_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Apply target — C20-2 (5 items)

| key | old_answer | new_answer | source_page | evidence (summary) | source ref |
| --- | ---: | ---: | --- | --- | --- |
| `2006_1회_6` | 4 | 3 | p.2 | 풀이 (Q=0.24·CV²t/(ερ)) ends 【답】③ | pack1 / `4317aea` |
| `2006_2회_27` | 3 | 4 | p.4 | 풀이 (제수문=취수량 조절·물 유입 단절) ends 【답】④ | pack2 / `041b83f` |
| `2007_1회_9` | 4 | 2 | p.2 | 풀이 (A·B=1+3a=0 → a=-1/3) ends 【답】② | pack2 / `041b83f` |
| `2007_2회_64` | 2 | 1 | p.6 | 풀이 (Routh first column all positive → stable) ends 【답】① | pack2 / `041b83f` |
| `2015_1회_71` | 4 | 1 | p.24 | 풀이 (L=Nφ/I=12H, τ=L/R=1s) ends 【답】① | pack2 / `041b83f` |

`new_answer` equals the verified `source_answer` for every row.

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
- A following step must reconcile `solution` / `steps` against the
  source-corrected `answer` before these 5 items are treated as resolved
  (the C20-2 solution dry-run / cleanup step, analogous to C20-1).

| key | answer | solution/steps | solution_svg |
| --- | --- | --- | --- |
| `2006_1회_6` | corrected | pending regeneration | pending audit |
| `2006_2회_27` | corrected | pending regeneration | pending audit |
| `2007_1회_9` | corrected | pending regeneration | pending audit |
| `2007_2회_64` | corrected | pending regeneration | pending audit |
| `2015_1회_71` | corrected | pending regeneration | pending audit |

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- All 5 C20-2 targets exist exactly once in both files.
- All 5 targets: post `answer` == `source_answer`.
- Exactly 5 items changed in each file; no other item changed.
- For each changed item, the field-level diff is exactly `['answer']`.
- `choices` / `text` / `solution` / `steps` / metadata / `solution_svg`
  unchanged for all items.
- C20-1 items (5 keys) unchanged.
- C20-3 / C20-4 items (9 keys) unchanged.
- DQ-1 items (`2014_2회_50`, `2014_3회_62`) unchanged.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the 5 changed integer values; no
  mass reformatting.

## Status

- Q2 bulk apply remains BLOCKED.
- Apply authorization covered batch C20-2 only. C20-3 / C20-4 are not applied
  and require separate per-batch approval.
- C20-1 is closed (answer correction `13036de` + solution cleanup `8f4bdf0`).
- DQ-1 items remain sealed pending the defective / multi-answer policy.

## Not done in this step

- No `solution` / `steps` apply or regeneration.
- No `solution_svg` modification.
- No `choices` / question text / metadata modification.
- No C20-1 modification.
- No C20-3 / C20-4 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
