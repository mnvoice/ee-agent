# Old Answer Conflict Correction — Design (2026-05-21)

Design document for the answer correction track covering the 20
`source_answer_conflict` items from the 1998-2016 old C1 pilot. This is a
**design document only**. It defines policy, boundaries, verification gates,
and batching for a future correction. It does NOT modify `app/data`, does NOT
correct any `q.answer`, and does NOT apply any solution change.

- Closeout (track parent): `docs/audit/old_solution_quality_q2_verified_apply_closeout_2026-05-21.md`
- Source review packs: `old_answer_manual_source_review_pack{,2,3}_2026-05-21.md`
- Source review routings: `old_answer_manual_source_review_routing{,2,3}_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## 1. Background

- The old C1 (`conclusion_mismatch`) pilot covered 30 items from 1998-2016.
  Each item's `q.answer` was manually verified against the source PDF 【답】
  marker by multimodal review.
- Verdict tally: 9 `source_answer_verified`, 20 `source_answer_conflict`,
  1 `defer`.
- The 9 `source_answer_verified` items (source 【답】 == `q.answer`) were
  applied — answer-locked regenerated `solution` + `steps` only. `q.answer`,
  `choices`, question text, metadata, and `solution_svg` were not modified.
  Apply commits: `fec4bbc` (Q2-B 4), `fbeffef` (Q2-C 2), `8354bee` (Q2-D 3).
- The 20 `source_answer_conflict` items have a source PDF 【답】 marker that
  **differs** from the stored `q.answer`. They were routed to this answer
  correction track and remain in a no-modify state for `app/data`.
- The 1 `defer` item (`2014_3회_62`) carries a source marker 【답】전항정답
  (all-choice / defective question). It has no single source answer and is
  out of scope for this track (see Section 7).

## 2. Design Goals

- Define a policy and verification gate to perform `q.answer` correction for
  the 20 conflict items safely, item-by-item, with per-batch approval.
- Define the rule for modifying `app/data/questions.json` and
  `app/data/questions.v2.json` together so the two files never diverge.
- Establish before/after evidence traceability for every correction so each
  changed `q.answer` is auditable back to a specific source PDF page.
- Draw an explicit boundary between answer correction and any change to
  `solution` / `steps` / `solution_svg` — answer correction touches only the
  `answer` field.

## 3. Correction Target Table (20 conflict items)

`current_q_answer` = stored `q.answer`. `source_answer` = the 【답】 marker
read from the source PDF. All 20 items have `correction status: not_applied`.

Source-fill commits: pack 1 items → `4317aea`; pack 2 items → `041b83f`;
pack 3 items → `d4462c1`.

| # | key | current | source | src page | evidence note (summary) | source ref | route | status |
| ---: | --- | ---: | ---: | --- | --- | --- | --- | --- |
| 1 | `1998_4회_10` | 1 | 4 | p.2 | 문제 10 풀이 box ends 【답】④ | pack1 / `4317aea` | answer correction candidate | not_applied |
| 2 | `2001_1회_68` | 1 | 3 | p.6 | 풀이 (가속도편차상수 Kₐ) ends 【답】③ | pack1 / `4317aea` | answer correction candidate | not_applied |
| 3 | `2001_3회_41` | 2 | 4 | p.3 | 풀이 (철손은 무부하손) ends 【답】④ | pack1 / `4317aea` | answer correction candidate | not_applied |
| 4 | `2001_3회_43` | 1 | 2 | p.4 | 풀이 box ends 【답】②; PDF choices readable | pack1 / `4317aea` | answer correction candidate | not_applied |
| 5 | `2002_3회_4` | 2 | 4 | p.2 | 풀이 (potential-form surface integral) ends 【답】④ | pack1 / `4317aea` | answer correction candidate | not_applied |
| 6 | `2006_1회_6` | 4 | 3 | p.2 | 풀이 (Q=0.24·CV²t/(ερ)) ends 【답】③ | pack1 / `4317aea` | answer correction candidate | not_applied |
| 7 | `2006_2회_27` | 3 | 4 | p.4 | 풀이 (제수문=취수량 조절·물 유입 단절) ends 【답】④ | pack2 / `041b83f` | answer correction candidate | not_applied |
| 8 | `2007_1회_9` | 4 | 2 | p.2 | 풀이 (A·B=1+3a=0 → a=-1/3) ends 【답】② | pack2 / `041b83f` | answer correction candidate | not_applied |
| 9 | `2007_2회_64` | 2 | 1 | p.6 | 풀이 (Routh first column all positive → stable) ends 【답】① | pack2 / `041b83f` | answer correction candidate | not_applied |
| 10 | `2014_2회_50` | 3 | 1, 2 | p.17 | 풀이 (V곡선 정의) ends double marker 【답】①,② | pack2 / `041b83f` | **multi-answer / defective branch — excluded from single-answer correction** | not_applied |
| 11 | `2015_1회_71` | 4 | 1 | p.24 | 풀이 (L=Nφ/I=12H, τ=L/R=1s) ends 【답】① | pack2 / `041b83f` | answer correction candidate | not_applied |
| 12 | `2015_1회_87` | 3 | 2 | p.29 | 풀이 (231.6 옥내전로 대지전압 300V 이하) ends 【답】② | pack2 / `041b83f` | answer correction candidate | not_applied |
| 13 | `2015_2회_23` | 3 | 4 | p.9 | 풀이 (π형 회로 I_s 보정항) ends 【답】④ | pack2 / `041b83f` | answer correction candidate | not_applied |
| 14 | `2015_2회_29` | 1 | 2 | p.10 | 풀이 (② 피뢰기=이상전압 파고치 저감) ends 【답】② | pack3 / `d4462c1` | answer correction candidate | not_applied |
| 15 | `2015_3회_22` | 4 | 1 | p.9 | 풀이 (제3고조파 제거=변압기 △결선) ends 【답】① | pack3 / `d4462c1` | answer correction candidate | not_applied |
| 16 | `2015_3회_25` | 1 | 4 | p.9 | 풀이 (④ 반한시-정한시 특성) ends 【답】④; PDF choices readable | pack3 / `d4462c1` | answer correction candidate | not_applied |
| 17 | `2016_1회_44` | 2 | 4 | p.15 | 풀이 (전기자 반작용 영향 4종) ends 【답】④; PDF choices readable | pack3 / `d4462c1` | answer correction candidate | not_applied |
| 18 | `2016_1회_69` | 1 | 4 | p.23 | 풀이 (고유주파수는 안정도와 무관) ends 【답】④ | pack3 / `d4462c1` | answer correction candidate | not_applied |
| 19 | `2016_1회_70` | 2 | 4 | p.23 | 풀이 (Nyquist 임계점 -1+j0 → 0dB, ±180°) ends 【답】④ | pack3 / `d4462c1` | answer correction candidate | not_applied |
| 20 | `2016_3회_21` | 1 | 4 | p.7 | 풀이 (전선 단면적 A ∝ 1/V²) ends 【답】④ | pack3 / `d4462c1` | answer correction candidate | not_applied |

Source PDF paths (verbatim, including the space variant for 2015 files):
`data/문제_1998_4회_20260316.pdf`, `data/문제_2001_1회_20260316.pdf`,
`data/문제_2001_3회_20260316.pdf`, `data/문제_2002_3회_20260316.pdf`,
`data/문제_2006_1회_20260316.pdf`, `data/문제_2006_2회_20260316.pdf`,
`data/문제_2007_1회_20260316.pdf`, `data/문제_2007_2회_20260316.pdf`,
`data/문제_2014_2회_20260316.pdf`, `data/문제_2015_1회_20260316.pdf`,
`data/문제 _2015_2회_20260316.pdf`, `data/문제 _2015_3회_20260316.pdf`,
`data/문제_2016_1회_20260316.pdf`, `data/문제_2016_3회_20260316.pdf`.

### 3.1 Multi-answer flag — `2014_2회_50`

Of the 20 conflict items, 19 have a single 1-4 `source_answer`. Item
`2014_2회_50` (#10) is the exception: the source marker is a double 【답】①,②.
`current_q_answer=3` matches neither, so the routing docs recorded it as
`source_answer_conflict`. However, a double marker is **not a single
1-4 answer** and therefore cannot pass the single-answer correction gate in
Section 5. This design routes `2014_2회_50` to the defective / multi-answer
branch (Section 7) and **excludes it from the single-answer correction
batches** in Section 6. The single-answer correction set is **19 items**, not
20. This deviation from the literal "20-item correction" framing is
intentional and is flagged for explicit user confirmation before any apply.

## 4. Correction Boundary — Allowed / Prohibited

### Allowed (after separate per-batch approval)

- Modify only the `answer` field of a target item, setting it to the verified
  `source_answer`.
- Modify `app/data/questions.json` and `app/data/questions.v2.json` together,
  in the same correction unit, for the same item set.
- Write a correction manifest / audit record (before/after `answer`, source
  page, evidence note, source-fill commit) under `docs/audit/`.

### Prohibited

- Any `app/data` modification before explicit per-batch approval.
- Regenerating or modifying `solution` / `steps` in the same operation as an
  answer correction. Answer correction touches the `answer` field only.
- Modifying `choices`, question text, or any metadata field.
- Modifying `solution_svg`.
- Replacing `source_answer` with a theory-derived computation. The source of
  truth for correction is the PDF 【답】 marker, not a recomputed value.
- Bulk correction without a per-item target list and per-batch manifest.
- Correcting any item whose `source_answer` is not a single 1-4 value
  (multi-answer, 전항정답) — these route to Section 7.

## 5. Verification Gate

### 5.1 Pre-apply gate (per item)

An item is eligible for a correction batch only if all hold:

- `source_answer` is filled from a PDF 【답】 marker (a real source, not a
  recomputed value).
- `source_page` and `evidence_note` are present and non-empty.
- `current_q_answer != source_answer` (the item is genuinely a conflict).
- `source_answer` is a single integer in the 1-4 range.
- Exclusion: items with a multi-answer or 전항정답 source marker do NOT pass;
  they route to Section 7. (Current exclusions: `2014_2회_50` multi-answer,
  `2014_3회_62` 전항정답.)

### 5.2 Post-apply gate (per batch)

After a batch is applied, all of the following must verify:

- `app/data/questions.json` and `app/data/questions.v2.json` both parse as
  valid JSON.
- The two files have an identical record count.
- `git diff` shows changes confined to the batch's target items only — no
  other item is touched.
- For each target item, only the `answer` field changed. `choices`, question
  text, `solution`, `steps`, metadata, and `solution_svg` are byte-identical
  to their pre-apply state.
- For each target item, the post-correction `answer` equals the recorded
  `source_answer`.
- The batch manifest states whether this batch completes the full conflict
  list or is a partial batch (and, if partial, which items remain).
- `git diff --check` reports no whitespace errors.

## 6. Batching

- Do NOT correct all items in a single operation.
- Single-answer correction set = **19 items** (20 conflict items minus
  `2014_2회_50`, see Section 3.1).
- Batch size = 5 items. Proposed batches: C20-1 (5), C20-2 (5), C20-3 (5),
  C20-4 (4).
- Per batch, the sequence is:
  1. Write a correction dry-run manifest (before/after `answer` per item,
     source page, evidence note).
  2. Obtain supervisor approval for that specific batch.
  3. Apply to `app/data` (the two question files together).
  4. Run the Section 5.2 post-apply gate.
  5. Commit the batch with an evidence-linked message.
- `2014_3회_62` (전항정답) and `2014_2회_50` (multi-answer) are excluded from
  all C20 batches and handled in Section 7.

## 7. Defective / Multi-answer Branch

Two items cannot be corrected to a single 1-4 `q.answer`:

| key | source marker | reason |
| --- | --- | --- |
| `2014_3회_62` | 【답】전항정답 | All-choice / defective question. The source 풀이 table gives F(s)=1/s and F(z)=z/(z-1); no single choice matches the pair. No single source answer exists. |
| `2014_2회_50` | 【답】①,② | Double marker. The source 풀이 (V곡선 정의) accepts two choices; `current_q_answer=3` matches neither. No single source answer exists. |

- Both are out of scope for single-answer correction.
- Neither may have its `app/data` modified before a defective-question /
  multi-answer policy is defined and approved.
- A policy must decide how the system represents a question with no single
  correct answer (e.g., accept-all scoring, multi-answer field, or flag as
  defective and exclude from scoring). That decision is track DQ-1 below.

## 8. Follow-up Tasks

- **C20-A**: Write the conflict correction manifest / dry-run for the 19
  single-answer items (no `app/data` modification — manifest only).
- **C20-B**: Request approval for the first 5-item batch (C20-1) apply.
- **DQ-1**: Design the defective-question / multi-answer policy covering
  `2014_3회_62` (전항정답) and `2014_2회_50` (double marker).
- **SVG-AUDIT**: Read-only consistency audit of `solution_svg` for the 9
  already-applied verified items (the verified apply track did not touch
  `solution_svg`).

## 9. Not Done in This Step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No answer correction applied.
- No `solution` / `steps` apply.
- No `solution_svg` modification.
- No paid API call.
- No correction manifest written yet (C20-A is a separate, future step).
