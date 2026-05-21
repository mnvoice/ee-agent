# Old Answer Conflict Correction — C20-1 Apply Result (2026-05-21)

Correction result log for batch C20-1. The `q.answer` field of 5
single-`source_answer` conflict items was corrected to the source PDF 【답】
marker value, in both `app/data/questions.json` and
`app/data/questions.v2.json`. Only the `answer` field was changed.

This is an apply-result record. The apply was authorized for batch C20-1 only.

- Base manifest commit: `0e6804d` (docs: draft old answer correction manifest)
- Design parent: `docs/audit/old_answer_conflict_correction_design_2026-05-21.md`
- Manifest: `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`
- Source review pack: `old_answer_manual_source_review_pack_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Apply target — C20-1 (5 items)

| key | old_answer | new_answer | source_page | evidence (summary) | source ref |
| --- | ---: | ---: | --- | --- | --- |
| `1998_4회_10` | 1 | 4 | p.2 | 문제 10 풀이 box ends 【답】④ | pack1 / `4317aea` |
| `2001_1회_68` | 1 | 3 | p.6 | 풀이 (가속도편차상수 Kₐ) ends 【답】③ | pack1 / `4317aea` |
| `2001_3회_41` | 2 | 4 | p.3 | 풀이 (철손은 무부하손) ends 【답】④ | pack1 / `4317aea` |
| `2001_3회_43` | 1 | 2 | p.4 | 풀이 box ends 【답】②; PDF choices readable | pack1 / `4317aea` |
| `2002_3회_4` | 2 | 4 | p.2 | 풀이 (potential-form surface integral) ends 【답】④ | pack1 / `4317aea` |

`new_answer` equals the verified `source_answer` for every row.

## Changed files

- `app/data/questions.json` — 5 `answer` fields updated.
- `app/data/questions.v2.json` — 5 `answer` fields updated.

## Changed field

- `answer` only. For every changed item the field-level diff is exactly
  `['answer']`. `choices`, `text`, `subject`, `q_no`, `q_type`, `difficulty`,
  `quality`, `tag`, `solution`, `steps`, and `solution_svg` are unchanged.

## Downstream status — answer_corrected_solution_pending

[IMPORTANT] These 5 items are in state `answer_corrected_solution_pending`:

- The `answer` field is now consistent with the source PDF 【답】 marker.
- The existing `solution` and `steps` were NOT modified and may still describe
  or conclude the **old** answer. They can be inconsistent with the corrected
  `answer`.
- `solution_svg` was NOT modified and is pending audit.
- A following step must regenerate `solution` / `steps` against the
  source-corrected `answer` before these 5 items are treated as resolved.

| key | answer | solution/steps | solution_svg |
| --- | --- | --- | --- |
| `1998_4회_10` | corrected | pending regeneration | pending audit |
| `2001_1회_68` | corrected | pending regeneration | pending audit |
| `2001_3회_41` | corrected | pending regeneration | pending audit |
| `2001_3회_43` | corrected | pending regeneration | pending audit |
| `2002_3회_4` | corrected | pending regeneration | pending audit |

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- All 5 C20-1 targets exist exactly once in both files.
- All 5 targets: post `answer` == `source_answer`.
- Exactly 5 items changed in each file; no other item changed.
- For each changed item, the field-level diff is exactly `['answer']`.
- `choices` / `text` / `solution` / `steps` / metadata / `solution_svg`
  unchanged for all items.
- C20-2 / C20-3 / C20-4 items (14 keys) unchanged.
- DQ-1 items (`2014_2회_50`, `2014_3회_62`) unchanged.
- `git diff --check` — no whitespace errors.
- Serialization preserved: both files round-trip byte-identically under their
  original formatting (`questions.json`: indent=2, ensure_ascii=False, trailing
  newline; `questions.v2.json`: compact separators, no trailing newline). The
  diff is confined to the 5 changed integer values — no mass reformatting.

## Status

- Q2 bulk apply remains BLOCKED.
- Apply authorization covered batch C20-1 only. C20-2 / C20-3 / C20-4 are not
  applied and require separate per-batch approval.
- DQ-1 items remain sealed pending the defective / multi-answer policy.

## Not done in this step

- No `solution` / `steps` apply or regeneration.
- No `solution_svg` modification.
- No `choices` / question text / metadata modification.
- No C20-2 / C20-3 / C20-4 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
