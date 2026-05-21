# Supervisor Reflection — Old-Answer Track (2026-05-21)

A reflection on the old-answer verification / correction track and the
supervisor dialogue that drove it, written to prepare for the next
answer-selection pedagogy track.

This is a reflection document only. No `app/data`, app code, or schema is
modified.

## 1. Purpose

Review the old-answer verification / correction track, record the judgments
that worked and the ones that had to be corrected, and set the principles
for the upcoming answer-selection pedagogy track.

## 2. What we got wrong at the start

- We first assumed an "old solution mismatch" was simply a wrong old
  explanation — a `solution` quality problem.
- The pilot verification showed otherwise: the mismatches were a mix of
  genuinely wrong `q.answer` values, OCR-damaged `choices`, and
  multi-answer / 전항정답 (all-answer / defective) questions.
- "The solution is wrong" was the wrong frame. The stored `q.answer` itself
  could be wrong, the stored `choices` could be corrupt, and some questions
  had no single correct answer at all.

## 3. The turning points

- Deciding NOT to auto-extend "`q.answer` is the SoT" to the 1998-2016 old
  questions. For this period, the stored answer is itself unverified.
- Adopting the source PDF 【답】 marker as the verification criterion — a
  real external source, not a recomputed or assumed value.
- Switching from a bulk apply to a small-batch rhythm:
  design → manifest → per-batch dry-run → per-batch apply → closeout. Each
  batch closed `answer` and `solution` together so a pending state did not
  accumulate.

## 4. What we achieved

- `source_answer_verified` and applied — 9 items.
- single-answer `source_answer_conflict` corrected (answer + solution
  cleanup) — 19 items.
- choice-OCR recovery — 2 items (`2001_3회_43`, `2015_3회_25`).
- `solution_svg` consistency audit — `stale_svg` 0.
- DQ defer — 2 items (`2014_2회_50`, `2014_3회_62`).
- `2016_1회_44` reasoning cleanup closed.
- Branch `feat/phase-b-migration` pushed to origin (in sync, ahead 0).

## 5. What we learned

- An LLM is not an answer authority — it is closer to a contradiction
  detector. It is good at surfacing "the solution concludes X but the stored
  answer is Y", and weak at being the source of truth for X.
- Answer-locking without source evidence is dangerous. The conflict set was
  a `conclusion_mismatch` set, and in many items the stored answer — not the
  solution — was the wrong one.
- Four distinct problem types must be kept separate: a wrong answer, a wrong
  solution, an OCR-damaged choice, and a defective (multi-answer /
  전항정답) question. Conflating them produces wrong fixes.
- Accuracy without scalability is slow; scalability without accuracy is
  dangerous. The small-batch rhythm traded some speed for the ability to
  verify each step.

## 6. Principles going forward

- Only source-clean items are eligible for the pedagogy pilot — items whose
  `answer`, `choices`, `solution`, and `steps` are verified consistent.
- Any per-choice reasoning MUST match the actual stored `choices`, not a
  generic substitute list (the `2016_1회_44` lesson).
- Do not fabricate statute numbers, article references, or numeric values.
  Stay within the source and the actual question / choices.
- No bulk apply. Apply stays item-by-item / small-batch, with approval.
- Keep the rhythm: dry-run → review → limited apply → closeout.

## 7. Next goal

- Design an answer-selection pedagogy track — making each question a
  "good problem to reason toward the answer through", not just a stored
  answer key.
- The core of that pedagogy: the concept being tested, the textual clues,
  wrong-answer elimination, cross-subject connections, and the
  exam-room discrimination method (how to decide under time pressure).
- But verify with a small pilot first — do not roll it out broadly before a
  pilot confirms the approach.

## 8. Self-reflection

- A parallel-work conflict occurred earlier on this branch (the `8bf5db5`
  era). The single-git-executor principle — one session owns the git
  actions for a track — is necessary and was followed for this track.
- `.git/index.lock` recurred repeatedly during this track. The principle of
  NOT force-deleting the lock was kept: each time, the lock was investigated
  (no holding process found — a transient lock), and the commit was retried
  once the lock cleared. Force-removal was never used.
- Writing closeout documents at intermediate points was very effective. Each
  batch closeout / per-track closeout made the state auditable and let the
  supervisor approve incrementally instead of trusting one large diff.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No app code or schema modification.
- No paid API call.
- No push.

## Status

- Old-answer track closed (DQ-1 2 items excepted, deferred).
- This reflection prepares the answer-selection pedagogy track; that track
  starts with a small pilot.
