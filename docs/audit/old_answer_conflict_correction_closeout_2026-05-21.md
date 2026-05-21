# Old Answer Conflict Correction — Closeout (2026-05-21)

Closeout record for the C20 answer correction track. Of the 20
`source_answer_conflict` items from the 1998-2016 old C1 pilot, the 19 items
with a single 1-4 `source_answer` have had their `q.answer` corrected and
their `solution` / `steps` reconciled. This document closes that track.

This is a closeout record only. No `app/data` modification is made here.

## 1. Purpose

After the 30-item C1 pilot source review, the `source_answer_conflict` items
were routed to an answer correction track. This closeout records the
completion of that track for the 19 items whose `source_answer` is a single
1-4 value: their `q.answer` was corrected to the source PDF 【답】 marker, and
their `solution` / `steps` were reconciled with the corrected answer. The 2
non-single-answer items (DQ-1) remain deferred.

## 2. Reference documents / commits

| step | commit |
| --- | --- |
| design | `614826b` |
| manifest | `0e6804d` |
| C20-1 answer correction | `13036de` |
| C20-1 solution cleanup | `8f4bdf0` |
| C20-2 answer correction | `c7390e4` |
| C20-2 solution cleanup | `8ad2689` |
| C20-3 answer correction | `8a6a961` |
| C20-3 solution cleanup | `5f80afa` |
| C20-4 answer correction | `c9ea03c` |
| C20-4 solution cleanup | `de0c6ab` |

Supporting audit documents (per step): the design, manifest, per-batch apply
records, and per-batch solution dry-run / apply records under `docs/audit/`
(`old_answer_conflict_correction_*` and `old_answer_manual_source_review_*`).

## 3. Final tally

| Metric | Count |
| --- | ---: |
| original pilot total | 30 |
| `source_answer_verified` apply track (already applied earlier) | 9 |
| single-answer `source_answer_conflict` corrected (C20) | 19 |
| DQ-1 deferred | 2 |
| C20 `answer_corrected_solution_pending` (open) | 0 |
| C20 `solution_svg` pending audit | 19 |

`30 = 9 (verified) + 19 (C20 conflict) + 2 (DQ-1 deferred)`.

DQ-1 deferred items:

- `2014_2회_50` — source marker 【답】①,② (double marker; not a single
  1-4 answer).
- `2014_3회_62` — source marker 【답】전항정답 (all-choice / defective
  question; no single source answer).

## 4. Corrected 19 items

`final status` = `answer_and_solution_closed` for all 19.

| key | old_answer | corrected_answer | source_page | answer commit | solution commit | notes / flags |
| --- | ---: | ---: | --- | --- | --- | --- |
| `1998_4회_10` | 1 | 4 | p.2 | `13036de` | `8f4bdf0` | solution edited (stale-ref cleanup) |
| `2001_1회_68` | 1 | 3 | p.6 | `13036de` | `8f4bdf0` | solution edited (steps typo fix) |
| `2001_3회_41` | 2 | 4 | p.3 | `13036de` | `8f4bdf0` | no-op (already consistent) |
| `2001_3회_43` | 1 | 2 | p.4 | `13036de` | `8f4bdf0` | solution edited; choice-OCR flag |
| `2002_3회_4` | 2 | 4 | p.2 | `13036de` | `8f4bdf0` | no-op (already consistent) |
| `2006_1회_6` | 4 | 3 | p.2 | `c7390e4` | `8ad2689` | solution edited (steps defect fix) |
| `2006_2회_27` | 3 | 4 | p.4 | `c7390e4` | `8ad2689` | solution edited (fabricated-claim fix) |
| `2007_1회_9` | 4 | 2 | p.2 | `c7390e4` | `8ad2689` | no-op (already consistent) |
| `2007_2회_64` | 2 | 1 | p.6 | `c7390e4` | `8ad2689` | no-op (already consistent) |
| `2015_1회_71` | 4 | 1 | p.24 | `c7390e4` | `8ad2689` | solution edited (stale-ref cleanup) |
| `2015_1회_87` | 3 | 2 | p.29 | `8a6a961` | `5f80afa` | no-op (already consistent) |
| `2015_2회_23` | 3 | 4 | p.9 | `8a6a961` | `5f80afa` | solution edited (steps defect fix) |
| `2015_2회_29` | 1 | 2 | p.10 | `8a6a961` | `5f80afa` | no-op (already consistent) |
| `2015_3회_22` | 4 | 1 | p.9 | `8a6a961` | `5f80afa` | no-op (already consistent) |
| `2015_3회_25` | 1 | 4 | p.9 | `8a6a961` | `5f80afa` | no-op; choice-OCR flag |
| `2016_1회_44` | 2 | 4 | p.15 | `c9ea03c` | `de0c6ab` | solution edited (hedge cleanup); deep-review flag |
| `2016_1회_69` | 1 | 4 | p.23 | `c9ea03c` | `de0c6ab` | solution edited (steps hedge removal) |
| `2016_1회_70` | 2 | 4 | p.23 | `c9ea03c` | `de0c6ab` | solution edited (steps hedge removal) |
| `2016_3회_21` | 1 | 4 | p.7 | `c9ea03c` | `de0c6ab` | solution edited (steps wrong-conclusion fix) |

All 19: `answer` corrected to the verified `source_answer`; `solution` /
`steps` reconciled (edited or confirmed no-op). `solution_svg` not modified —
pending the SVG-AUDIT track.

## 5. Batch summary

| batch | answer corrected | solution edited | no-op |
| --- | ---: | ---: | ---: |
| C20-1 | 5 | 3 | 2 |
| C20-2 | 5 | 3 | 2 |
| C20-3 | 5 | 1 | 4 |
| C20-4 | 4 | 4 | 0 |
| total | 19 | 11 | 8 |

Observation: the conflict set was C1 `conclusion_mismatch`, so in many items
the `solution` body already concluded the source-correct answer and only
stale old-answer references needed cleanup (8 no-op). Where the existing
`solution` / `steps` carried a genuine defect — `2006_1회_6` (erroneous step),
`2006_2회_27` (fabricated "no valid answer" claim), `2015_2회_23` (truncated
steps), `2016_3회_21` (wrong conclusion) — the fix was a bounded,
source-grounded correction, never a from-scratch regeneration.

## 6. Remaining flags

- **DQ-1 (defective / multi-answer policy)**:
  - `2014_2회_50` — multi-answer policy (source marker ①,②).
  - `2014_3회_62` — all-answer / defective-question policy (source marker
    전항정답).
- **choice-OCR recovery**:
  - `2001_3회_43` — DB-stored choice [2] text OCR-damaged.
  - `2015_3회_25` — DB-stored choice [4] text is page-footer residue; choices
    [1]-[3] carry a stray leading "：".
- **deep reasoning review**:
  - `2016_1회_44` — conclusion (4번) is source-locked, but the `solution` /
    `steps` reasoning body enumerates effects that do not map to the actual
    choice texts; a reasoning rewrite was out of scope for the cleanup.
- **SVG-AUDIT**:
  - `solution_svg` consistency audit for the C20 19 corrected items.
  - Optionally, `solution_svg` audit for the 9 earlier `source_answer_verified`
    apply-track items.

## 7. Policy conclusions

- For 1998-2016 old questions, `source_answer` verification against the
  source PDF 【답】 marker is required before any answer-lock or correction.
  "`q.answer` is the SoT" is NOT auto-extended for this period.
- A single-`source_answer` conflict is handled by: an itemized manifest, a
  per-batch apply, and a post-apply `solution` / `steps` cleanup.
- Answer correction and solution cleanup are closed within the same batch, so
  `answer_corrected_solution_pending` state is not allowed to accumulate.
- Multi-answer / 전항정답 source markers are NOT force-mapped onto the single
  `answer` field; they route to the DQ-1 policy track.
- Q2 bulk apply remains BLOCKED. Apply stays item-by-item, verified-only,
  with per-batch approval.

## 8. Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No additional answer correction.
- No `solution` / `steps` apply.
- No `solution_svg` modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
