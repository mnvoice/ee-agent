# Old Answer — Verification / Correction Final Closeout (2026-05-21)

Final closeout for the old-answer verification and correction work on the
1998-2016 old C1 pilot. It summarizes the end state across source answer
verification, the verified apply, answer correction, solution cleanup, the
SVG audit, choice-OCR recovery, and the DQ defer.

This is a closeout summary only. No `app/data` modification is made here.

## 1. Purpose

Summarize the final state of the 30-item C1 pilot: source answer
verification, the `source_answer_verified` apply, the C20 single-answer
correction (answer + solution), the `solution_svg` consistency audit, the
`2016_1회_44` reasoning cleanup, the choice-OCR recovery, and the DQ defer.

## 2. Key closeout / summary commits

| step | commit |
| --- | --- |
| verified apply closeout | `4fed8a8` |
| C20 correction closeout | `5277967` |
| DQ defective/multi-answer policy | `37ccaa2` |
| DQ schema probe | `3894a38` |
| solution_svg consistency audit | `10d8901` |
| `2016_1회_44` reasoning cleanup apply | `4fbc820` |
| choice-OCR recovery apply | `fac4b8d` |

(Per-batch apply / dry-run commits are listed in the C20 closeout `5277967`
and the per-track audit documents under `docs/audit/`.)

## 3. Final-state tally

| Metric | Count |
| --- | ---: |
| pilot total | 30 |
| `source_answer_verified` and applied | 9 |
| single-answer `source_answer_conflict` corrected (C20) | 19 |
| DQ defer | 2 |
| `stale_svg` (SVG audit) | 0 |
| `choice_ocr_recovered` | 2 |

`30 = 9 (verified) + 19 (C20 corrected) + 2 (DQ defer)`.

DQ defer items:

- `2014_2회_50` — multi-answer marker 【답】①,②.
- `2014_3회_62` — all-answer / defective marker 【답】전항정답.

Unresolved in this track: the DQ migration only, intentionally deferred (see
Section 5).

## 4. Completed items

### `source_answer_verified` and applied (9)

`2001_1회_21`, `2002_1회_32`, `2005_3회_83`, `2006_1회_7`, `2015_1회_13`,
`2015_1회_22`, `2015_3회_27`, `2016_1회_71`, `2016_3회_44`.
(Answer-locked regenerated `solution` / `steps`; apply commits `fec4bbc` /
`fbeffef` / `8354bee`.)

### C20 single-answer `source_answer_conflict` corrected (19)

`q.answer` corrected to the source 【답】 marker and `solution` / `steps`
reconciled:

- C20-1: `1998_4회_10`, `2001_1회_68`, `2001_3회_41`, `2001_3회_43`,
  `2002_3회_4` (answer `13036de`, solution `8f4bdf0`)
- C20-2: `2006_1회_6`, `2006_2회_27`, `2007_1회_9`, `2007_2회_64`,
  `2015_1회_71` (answer `c7390e4`, solution `8ad2689`)
- C20-3: `2015_1회_87`, `2015_2회_23`, `2015_2회_29`, `2015_3회_22`,
  `2015_3회_25` (answer `8a6a961`, solution `5f80afa`)
- C20-4: `2016_1회_44`, `2016_1회_69`, `2016_1회_70`, `2016_3회_21`
  (answer `c9ea03c`, solution `de0c6ab`)

### choice-OCR recovered (2)

`2001_3회_43`, `2015_3회_25` — `choices` text recovered from the source PDF
(transcription R0-R3, apply `fac4b8d`). `answer` retained (2 / 4).

### `2016_1회_44` reasoning cleanup

`2016_1회_44` (a C20-4 item) carried a `needs_solution_cleanup` flag — the
`solution` / `steps` reasoning had been written against an enumeration that
did not match the actual choices. Reviewed (`fb3bb91`) and cleaned up
(`4fbc820`): the reasoning now matches the actual choice texts and correctly
explains why choice [4] is the answer. Status: `reasoning_cleanup_closed`.

### solution_svg consistency audit

28 items (9 verified + 19 C20) audited (`10d8901`): 13 have a `solution_svg`,
all text-consistent with the corrected answer; 15 have none. `stale_svg`: 0.
No SVG cleanup/rebuild track was opened.

## 5. Deferred items

DQ-1 — 2 items:

- `2014_2회_50` — source marker 【답】①,② (multi-answer).
- `2014_3회_62` — source marker 【답】전항정답 (all-answer / defective).

Reason for defer:

- The current `app/data` schema stores `answer` as a single integer, and the
  app's scoring / rendering logic compares it by strict `===` at scattered
  sites (DQ-2 probe `3894a38`). The schema and app cannot express a
  multi-answer or all-answer question.
- Coercing either item onto a single `q.answer` is forbidden — it distorts
  scoring and loses the source evidence.
- A DQ migration requires a coordinated schema + app scoring/rendering
  design, which is a separate large track.

## 6. Policy conclusions

- For 1998-2016 old questions, "`q.answer` is the SoT" is NOT inherited
  automatically.
- Source PDF 【답】 marker verification is mandatory before any answer-lock
  or correction.
- A single-answer conflict can be corrected with an itemized manifest +
  per-batch answer apply + post-apply solution cleanup.
- Answer correction and solution cleanup should close within the same batch,
  so `answer_corrected_solution_pending` state does not accumulate.
- Multi-answer / all-answer defects remain `defer` until a schema + app
  migration is designed and approved.
- Q2 bulk apply remains BLOCKED — apply stays item-by-item, verified-only,
  with per-batch approval.

## 7. Remaining optional tracks

- DQ migration design (large) — schema + app scoring/rendering, then a
  policy choice for the 2 DQ-1 items.
- An optional browser spot check of the corrected / recovered items, if a
  rendered visual confirmation is desired.
- A push decision — this branch (`feat/phase-b-migration`) is currently
  unpushed; pushing is a separate supervisor decision.

## 8. Not done

- DQ migration not implemented.
- Schema / app logic not changed.
- DQ-1 `app/data` not modified (the 2 DQ items remain `defer`).
- No push performed.

## 9. Status

- Old-answer verification / correction track: closed for the 28 resolvable
  items (9 verified + 19 corrected), with `2016_1회_44` reasoning cleanup and
  the 2 choice-OCR recoveries also closed.
- 2 DQ-1 items remain `defer` pending the DQ migration.
- Q2 bulk apply remains BLOCKED.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No app code / schema modification.
- No `answer` / `choices` / `solution` / `steps` / `solution_svg`
  modification.
- No paid API call.
- No push.
