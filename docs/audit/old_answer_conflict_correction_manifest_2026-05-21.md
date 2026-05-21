# Old Answer Conflict Correction — Manifest / Dry-run (2026-05-21)

Correction dry-run manifest for the C20-A track. It enumerates the 19
single-`source_answer` conflict items eligible for `q.answer` correction,
their proposed new answers, source evidence, and batch assignment.

This manifest is a **dry-run record only**. It does NOT modify `app/data`,
does NOT correct any `q.answer`, and is **not an approval to apply**. Apply
requires separate per-batch supervisor approval (track C20-B).

- Base commit: `614826b` (docs: design old answer conflict correction track)
- Design parent: `docs/audit/old_answer_conflict_correction_design_2026-05-21.md`
- Closeout: `docs/audit/old_solution_quality_q2_verified_apply_closeout_2026-05-21.md`
- Source review packs: `old_answer_manual_source_review_pack{,2,3}_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Purpose

Provide a per-item correction dry-run for the 19 conflict items whose
`source_answer` is a single 1-4 value. Each row records the current stored
`q.answer`, the verified `source_answer` from the source PDF 【답】 marker,
and the proposed new answer. No row is applied here.

## Excluded items (routed to DQ-1)

| key | source marker | reason |
| --- | --- | --- |
| `2014_2회_50` | 【답】①,② | Double marker — `source_answer` is not a single 1-4 value. No single `q.answer` correction is possible. |
| `2014_3회_62` | 【답】전항정답 | All-choice / defective question — no single source answer exists. |

Both are out of scope for C20 answer correction. They route to the DQ-1
defective / multi-answer policy track. Their `app/data` MUST NOT be modified
before that policy is defined and approved.

## Confirmed scope criteria (user-approved, 2026-05-21)

- Only conflicts with a single 1-4 `source_answer` are answer-correction
  apply candidates.
- `2014_2회_50` (double marker) — single `q.answer` correction prohibited.
- `2014_3회_62` (전항정답) — single `q.answer` correction prohibited.
- The two items above route to DQ-1.
- The C20 single-answer correction set is therefore **19 items**.

## Correction target table (19 items)

`proposed_new_answer` equals the verified `source_answer` for every row.
`correction action` = update `q.answer` only. `apply_status` = `not_applied`
for every row. Source review doc/commit: pack 1 → `4317aea`, pack 2 →
`041b83f`, pack 3 → `d4462c1` (source-fill commits).

| batch | key | current_q_answer | source_answer | proposed_new_answer | source_page | evidence_note (summary) | source ref | correction action | apply_status |
| --- | --- | ---: | ---: | ---: | --- | --- | --- | --- | --- |
| C20-1 | `1998_4회_10` | 1 | 4 | 4 | p.2 | 문제 10 풀이 box ends 【답】④ | pack1 / `4317aea` | update q.answer only | not_applied |
| C20-1 | `2001_1회_68` | 1 | 3 | 3 | p.6 | 풀이 (가속도편차상수 Kₐ) ends 【답】③ | pack1 / `4317aea` | update q.answer only | not_applied |
| C20-1 | `2001_3회_41` | 2 | 4 | 4 | p.3 | 풀이 (철손은 무부하손) ends 【답】④ | pack1 / `4317aea` | update q.answer only | not_applied |
| C20-1 | `2001_3회_43` | 1 | 2 | 2 | p.4 | 풀이 box ends 【답】②; PDF choices readable | pack1 / `4317aea` | update q.answer only | not_applied |
| C20-1 | `2002_3회_4` | 2 | 4 | 4 | p.2 | 풀이 (potential-form surface integral) ends 【답】④ | pack1 / `4317aea` | update q.answer only | not_applied |
| C20-2 | `2006_1회_6` | 4 | 3 | 3 | p.2 | 풀이 (Q=0.24·CV²t/(ερ)) ends 【답】③ | pack1 / `4317aea` | update q.answer only | not_applied |
| C20-2 | `2006_2회_27` | 3 | 4 | 4 | p.4 | 풀이 (제수문=취수량 조절·물 유입 단절) ends 【답】④ | pack2 / `041b83f` | update q.answer only | not_applied |
| C20-2 | `2007_1회_9` | 4 | 2 | 2 | p.2 | 풀이 (A·B=1+3a=0 → a=-1/3) ends 【답】② | pack2 / `041b83f` | update q.answer only | not_applied |
| C20-2 | `2007_2회_64` | 2 | 1 | 1 | p.6 | 풀이 (Routh first column all positive → stable) ends 【답】① | pack2 / `041b83f` | update q.answer only | not_applied |
| C20-2 | `2015_1회_71` | 4 | 1 | 1 | p.24 | 풀이 (L=Nφ/I=12H, τ=L/R=1s) ends 【답】① | pack2 / `041b83f` | update q.answer only | not_applied |
| C20-3 | `2015_1회_87` | 3 | 2 | 2 | p.29 | 풀이 (231.6 옥내전로 대지전압 300V 이하) ends 【답】② | pack2 / `041b83f` | update q.answer only | not_applied |
| C20-3 | `2015_2회_23` | 3 | 4 | 4 | p.9 | 풀이 (π형 회로 I_s 보정항) ends 【답】④ | pack2 / `041b83f` | update q.answer only | not_applied |
| C20-3 | `2015_2회_29` | 1 | 2 | 2 | p.10 | 풀이 (② 피뢰기=이상전압 파고치 저감) ends 【답】② | pack3 / `d4462c1` | update q.answer only | not_applied |
| C20-3 | `2015_3회_22` | 4 | 1 | 1 | p.9 | 풀이 (제3고조파 제거=변압기 △결선) ends 【답】① | pack3 / `d4462c1` | update q.answer only | not_applied |
| C20-3 | `2015_3회_25` | 1 | 4 | 4 | p.9 | 풀이 (④ 반한시-정한시 특성) ends 【답】④; PDF choices readable | pack3 / `d4462c1` | update q.answer only | not_applied |
| C20-4 | `2016_1회_44` | 2 | 4 | 4 | p.15 | 풀이 (전기자 반작용 영향 4종) ends 【답】④; PDF choices readable | pack3 / `d4462c1` | update q.answer only | not_applied |
| C20-4 | `2016_1회_69` | 1 | 4 | 4 | p.23 | 풀이 (고유주파수는 안정도와 무관) ends 【답】④ | pack3 / `d4462c1` | update q.answer only | not_applied |
| C20-4 | `2016_1회_70` | 2 | 4 | 4 | p.23 | 풀이 (Nyquist 임계점 -1+j0 → 0dB, ±180°) ends 【답】④ | pack3 / `d4462c1` | update q.answer only | not_applied |
| C20-4 | `2016_3회_21` | 1 | 4 | 4 | p.7 | 풀이 (전선 단면적 A ∝ 1/V²) ends 【답】④ | pack3 / `d4462c1` | update q.answer only | not_applied |

## Batch composition

Batches are assigned by pilot order (the 30-item C1 pilot sequence), skipping
the two DQ-1 items.

| batch | item count | keys |
| --- | ---: | --- |
| C20-1 | 5 | `1998_4회_10`, `2001_1회_68`, `2001_3회_41`, `2001_3회_43`, `2002_3회_4` |
| C20-2 | 5 | `2006_1회_6`, `2006_2회_27`, `2007_1회_9`, `2007_2회_64`, `2015_1회_71` |
| C20-3 | 5 | `2015_1회_87`, `2015_2회_23`, `2015_2회_29`, `2015_3회_22`, `2015_3회_25` |
| C20-4 | 4 | `2016_1회_44`, `2016_1회_69`, `2016_1회_70`, `2016_3회_21` |

Total: 19 items.

## Pre-apply checks (per item — all hold for every row above)

- `current_q_answer != source_answer` — all 19 rows satisfy this (the item
  is a genuine conflict).
- `source_answer` is in 1..4 — all 19 rows satisfy this.
- `source_answer` is a single value (not multi-answer, not 전항정답) — all 19
  rows satisfy this; the two non-single items are excluded to DQ-1.
- `evidence_note` and `source_page` are present — all 19 rows satisfy this.
- Target `key` exists in both `app/data/questions.json` and
  `app/data/questions.v2.json` — to be confirmed at batch apply time
  (C20-B); this manifest does not read or modify `app/data`.

## Post-apply checks (to run later, per batch, at C20-B)

After a batch is applied, all of the following must verify:

- `app/data/questions.json` and `app/data/questions.v2.json` both parse as
  valid JSON.
- Record count unchanged in both files.
- `git diff` shows changes confined to that batch's target keys only.
- For each target, only the `answer` field changed.
- `choices`, question text, `solution`, `steps`, metadata, and `solution_svg`
  are byte-identical to their pre-apply state.
- For each target, the updated `answer` equals the recorded `source_answer`.
- `git diff --check` reports no whitespace errors.

## Status

- Q2 bulk apply remains BLOCKED.
- This manifest is NOT an approval to apply. Apply is per-batch, with
  separate supervisor approval (track C20-B).
- No `app/data` file was read or modified to produce this manifest; all
  values are sourced from the manual source review packs.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No answer correction applied.
- No `solution` / `steps` apply.
- No `solution_svg` modification.
- No modification of the DQ-1 items (`2014_2회_50`, `2014_3회_62`).
- No paid API call.
