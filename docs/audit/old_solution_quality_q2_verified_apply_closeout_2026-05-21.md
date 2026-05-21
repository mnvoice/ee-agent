# Old Solution Quality — Q2 Verified Apply Closeout (2026-05-21)

## Purpose

This document closes out the verified-apply track for the 1998-2016 old C1
pilot. For the 30-item C1 (`conclusion_mismatch`) pilot, each item's `q.answer`
was verified against the source PDF 【답】 marker by manual multimodal review.
Only `source_answer_verified` items — those whose source answer equals
`q.answer` — were applied (answer-locked regenerated solution + steps). Every
`source_answer_conflict` and `defer` item was left untouched in `app/data`.

This is a closeout record only. No `app/data` modification is made here.

## Key commits (track timeline)

| commit | step |
| --- | --- |
| `4317aea` | first source review (pack 1, items 1-10) |
| `33c8fcf` | first routing summary |
| `bce99f6` | Q2-B dry-run (4 verified items) |
| `fec4bbc` | Q2-B apply (4 verified items) |
| `041b83f` | second source review (pack 2, items 11-20) |
| `cff0e6d` | second routing summary |
| `5578c22` | Q2-C dry-run (2 verified items) |
| `fbeffef` | Q2-C apply (2 verified items) |
| `d4462c1` | third source review (pack 3, items 21-30) |
| `feed96a` | third routing summary |
| `44d84ac` | Q2-D dry-run (3 verified items) |
| `8354bee` | Q2-D apply (3 verified items) |

## Final tally

| Metric | Count |
| --- | ---: |
| pilot total | 30 |
| `source_answer_verified` | 9 |
| applied verified | 9 |
| `source_answer_conflict` | 20 |
| `defer` | 1 |
| `source_choice_ocr_corrupt` | 0 |
| `needs_better_scan` | 0 |

All 9 verified items were applied. The verified set is fully closed: verified
count (9) equals applied count (9).

## Applied verified items (9)

These 9 items had a source PDF 【답】 marker equal to `q.answer`. Their
`solution` and `steps` were replaced with answer-locked regenerated drafts in
both `app/data/questions.json` and `app/data/questions.v2.json`. `q.answer`,
`choices`, question text, metadata, and `solution_svg` were not modified.

| key | subject | q.answer | apply commit |
| --- | --- | ---: | --- |
| `2001_1회_21` | 전력공학 | 2 | `fec4bbc` (Q2-B) |
| `2002_1회_32` | 전력공학 | 1 | `fec4bbc` (Q2-B) |
| `2005_3회_83` | 전기설비기술기준 | 4 | `fec4bbc` (Q2-B) |
| `2006_1회_7` | 전기자기학 | 2 | `fec4bbc` (Q2-B) |
| `2015_1회_13` | 전기자기학 | 1 | `fbeffef` (Q2-C) |
| `2015_1회_22` | 전력공학 | 1 | `fbeffef` (Q2-C) |
| `2015_3회_27` | 전력공학 | 3 | `8354bee` (Q2-D) |
| `2016_1회_71` | 제어공학 | 3 | `8354bee` (Q2-D) |
| `2016_3회_44` | 전기기기 | 4 | `8354bee` (Q2-D) |

## Conflict items (20) — answer correction track

These 20 items had a source PDF 【답】 marker that differs from `q.answer`.
Route: answer correction track. They remain in a no-modify state for `app/data`
until a separate answer correction design exists.

| key | subject | q_no | current_q_answer | source_answer |
| --- | --- | ---: | ---: | ---: |
| `1998_4회_10` | 전기자기학 | 10 | 1 | 4 |
| `2001_1회_68` | 제어공학 | 68 | 1 | 3 |
| `2001_3회_41` | 전기기기 | 41 | 2 | 4 |
| `2001_3회_43` | 전기기기 | 43 | 1 | 2 |
| `2002_3회_4` | 전기자기학 | 4 | 2 | 4 |
| `2006_1회_6` | 전기자기학 | 6 | 4 | 3 |
| `2006_2회_27` | 전력공학 | 27 | 3 | 4 |
| `2007_1회_9` | 전기자기학 | 9 | 4 | 2 |
| `2007_2회_64` | 회로이론 | 64 | 2 | 1 |
| `2014_2회_50` | 전기기기 | 50 | 3 | 1, 2 |
| `2015_1회_71` | 전기자기학 | 71 | 4 | 1 |
| `2015_1회_87` | 전기설비기술기준 | 87 | 3 | 2 |
| `2015_2회_23` | 전력공학 | 23 | 3 | 4 |
| `2015_2회_29` | 전력공학 | 29 | 1 | 2 |
| `2015_3회_22` | 전력공학 | 22 | 4 | 1 |
| `2015_3회_25` | 전력공학 | 25 | 1 | 4 |
| `2016_1회_44` | 전기기기 | 44 | 2 | 4 |
| `2016_1회_69` | 전력공학 | 69 | 1 | 4 |
| `2016_1회_70` | 제어공학 | 70 | 2 | 4 |
| `2016_3회_21` | 전력공학 | 21 | 1 | 4 |

## Defer item (1) — defective-question policy needed

| key | subject | q_no | current_q_answer | reason |
| --- | --- | ---: | ---: | --- |
| `2014_3회_62` | 회로이론 | 62 | 4 | 원문 마커가 【답】전항정답 (defective question, all choices accepted). The source 풀이 table gives F(s)=1/s and F(z)=z/(z-1), which no single choice matches. There is no single source answer to lock against. |

Route: defer. Held until a defective-question ("전항정답") policy is defined.

## Policy conclusions

- For 1998-2016 old items, "`q.answer` is the SoT" is NOT auto-extended. The
  C1 pilot established that a conclusion mismatch on an unverified old item
  does not by itself mean the old solution is wrong — `q.answer` itself may be
  unverified.
- Only `source_answer_verified` items (source PDF 【답】 == `q.answer`) are
  eligible for answer-locked regeneration and apply.
- `source_answer_conflict` items: `app/data` modification is prohibited until a
  dedicated answer correction track is designed and approved.
- Defective ("전항정답") questions are deferred until a separate
  defective-question policy is defined.
- Q2 bulk apply remains prohibited. Apply is item-by-item, verified-only, with
  per-batch approval.

## Remaining follow-up tracks

- Answer correction design for the 20 `source_answer_conflict` items.
- Defective-question policy for `2014_3회_62`.
- Optional `solution_svg` consistency audit for the 9 applied items
  (the apply track did not touch `solution_svg`).

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No answer correction.
- No solution apply.
- No regeneration apply.
- No `solution_svg` modification.
- No paid API call.
