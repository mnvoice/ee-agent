# Old Answer — Defective / Multi-answer Schema Probe (DQ-2) (2026-05-21)

Read-only investigation (DQ-2) into whether the current `app/data` schema and
the app's scoring / rendering logic can represent a multi-answer or
defective ("전항정답") question. This determines which DQ-1 policy options are
feasible.

This is a **read-only investigation document**. It does NOT modify `app/data`,
the schema, app code, or any `q.answer`.

- Base commit: `37ccaa2` (docs: design defective multi-answer policy)
- Policy parent: `docs/audit/old_answer_defective_multi_answer_policy_2026-05-21.md`
- DQ-1 items: `2014_2회_50` (multi_answer_marker), `2014_3회_62` (all_answer_defective)

## 1. Investigation scope and commands

Read-only scans performed:

- `app/data/questions.json`, `app/data/questions.v2.json` — full field
  inventory, `answer` field type and value distribution, search for
  multi-answer / status / defective / disabled fields (Python `json` scan).
- `app/js/*.js` (8 files, 5532 LOC) and `app/index.html` — `grep` for
  `answer`, `quality`, `incomplete`, `disabl`, `defect`, `exclude`, `전항정답`.
- `docs/` — `grep` for schema descriptions.

## 2. Data schema findings

`questions.json` and `questions.v2.json` both hold 5331 records.

- `answer` field: type is **`int` for all 5331 records** in both files.
  Value distribution (identical in both files):
  `0`: 154, `1`: 1282, `2`: 1423, `3`: 1302, `4`: 1170.
- There is **no multi-answer field** (no `answers`, no `all_answers`, no
  list-typed answer field).
- There is **no `answer_status`, no `defective`, no `disabled`, no
  `excluded` field**.
- `questions.json` fields: `answer, choices, difficulty, figure_svg, number,
  q_no, q_type, quality, session, solution, solution_svg, steps, subject,
  tag, text, year`.
- `questions.v2.json` adds provenance fields (`answer_source`,
  `choices_source`, `solution_source`, `steps_source`, `text_source`),
  `stem_figure`, and a dict-typed `figure_svg` / `solution_svg`. None of
  these expresses a multi-answer or defective state — `answer_source` is
  provenance metadata (`source` / `tool_name` / `verified_at`), not an
  answer value.
- `quality` field: values are `complete` (5144) and `incomplete` (187).
  This is the closest existing field to a "question state", but it expresses
  data-completeness, not answer multiplicity or defectiveness.
- The `answer = 0` sentinel: 154 records carry `answer = 0`, outside the
  1-4 choice range. Choices are numbered 1-4, so a learner's `userAnswer`
  is always 1-4 and can never equal 0 — an `answer = 0` record is therefore
  effectively "never scoreable as correct". This is a de-facto
  unknown-answer sentinel, NOT a usable representation for
  "either ① or ②" or "all choices accepted".

Conclusion: the schema supports **single answer only**. It has no field for
multiple answers, all-answers, defective, or disabled / excluded states.

## 3. App logic findings

`q.answer` is consumed as a single integer compared by strict equality
(`===`) at multiple, scattered sites. There is no central scoring function.

| location | usage |
| --- | --- |
| `app/js/study.js:159` | `isCorrect: choiceNum === q.answer` |
| `app/js/main.js:335-336` | `isCorrect = answered && userAnswer === answer`; `isWrong = answered && userAnswer !== null && userAnswer !== answer` |
| `app/js/main.js:357` | result indicator text `'정답: ' + answer + '번'` |
| `app/js/main.js:1332` | mock-exam scoring `if (state.mockAnswers[i] === q.answer) results[subj].correct++` |
| `app/js/main.js:1375` | `isCorrect = state.mockAnswers[i] === q.answer` |
| `app/js/main.js:1528` | `isCorrect: choiceNum === q.answer` |
| `app/index.html`, `app/js/bundle.js`, `app/js/render.js` | duplicated choice-render / answer-compare logic (bundle.js is a bundled copy) |

- Every comparison is `userAnswer === q.answer` (or `!==`) — a single-value
  match.
- The correct-answer display (`main.js:357`) prints a single number:
  `정답: N번`.
- `disabled` appears only as the per-choice button disabled state after the
  learner answers — there is **no question-level disable / exclude logic**.
- The `quality` field (`incomplete` for 187 records) is **not read by any
  app code** — no filtering, hiding, or special handling keys off it.
- No code path handles a defective / all-answer / multi-answer question.

Conclusion: the app logic supports **single answer only**. It does not
support multiple answers, all-answers, defective questions, or
disabled / excluded questions. Scoring logic is duplicated across
`main.js`, `study.js`, `index.html`, and `bundle.js`.

## 4. Support matrix

| Representation | Schema support | App logic support |
| --- | --- | --- |
| single answer | YES (`answer: int`) | YES (`=== ` compare) |
| multiple answers | NO | NO |
| all answers (전항정답) | NO | NO |
| defective / deferred question | NO | NO |
| disabled / excluded question | NO | NO |

## 5. Risk assessment

- The scoring comparison is **scattered across 3+ files** (`main.js`,
  `study.js`, `index.html`) plus a bundled copy (`bundle.js`). Any change to
  the answer representation must be applied consistently at every site, or
  scoring diverges between the normal mode, study mode, and mock-exam mode.
- There is **no central scoring function** to change in one place — this
  raises the regression risk of any multi-answer / defective change.
- The correct-answer display assumes a single number (`정답: N번`); a
  multi-answer or defective item would render incorrectly without a display
  change too.
- The `answer = 0` sentinel cannot be reused for DQ-1: setting a DQ item to
  `answer = 0` marks every learner wrong, which is the opposite of
  "all answers accepted" and wrong for "either ① or ②".
- `questions.json` and `questions.v2.json` must stay consistent — any schema
  change is a two-file migration.

## 6. DQ-1 option — implementation difficulty / risk

| Option | Schema work | App work | Difficulty | Risk |
| --- | --- | --- | --- | --- |
| A — keep `defer` | none | none | none | none — status quo preserved |
| B — metadata / flag field | add a field to both JSON files | app must read the new field to change behavior; otherwise the flag is inert | medium | low if app-inert (no behavior change); medium if app reads it |
| D — disabled / excluded | add a field to both JSON files | add question-level filtering at load time (no such logic exists today) | medium-high | medium — new filtering path, scoring/stats affected |
| E — multi-answer schema | add `answers` / `all_answers` to both JSON files | change every `===` compare site (≥6, across `main.js`/`study.js`/`index.html`/`bundle.js`) + the `정답: N번` display | high | high — touches scoring core in 3 modes; no central function; regression-prone |
| C — force single `q.answer` | — | — | — | prohibited — source distortion, scoring distortion |

## 7. Recommendation

- Do NOT modify `app/data` now.
- Without a schema change AND a coordinated app-logic change, the DQ-1 items
  cannot be represented faithfully. Keep both DQ-1 items `defer` /
  `not_applied`.
- Do NOT force-map a single `q.answer` onto the DQ-1 items (Option C) and do
  NOT reuse the `answer = 0` sentinel — both distort scoring.
- A DQ-1 apply requires a separate, approved migration design covering:
  both JSON files, all scattered `===` scoring sites, the `정답: N번`
  display, mock-exam scoring, stats aggregation, and a browser verification
  plan (per the Section 6 gate of the DQ-1 policy document).
- Option A (keep defer) is the safe state until that migration is designed.
  Among the active options, B (app-inert metadata flag) is the lowest-risk
  way to at least record the source truth without changing scoring — but
  even B should be deferred to an explicit, approved design step.

## 8. Not done in this step

- No file modification.
- No schema change.
- No app logic change.
- No `q.answer` modification.
- No `solution` / `steps` modification.
- No `solution_svg` modification.
- No paid API call.
- No push.

## 9. Status

- The 2 DQ-1 items remain `defer` / `not_applied`.
- Q2 bulk apply remains BLOCKED.
- Schema and app logic confirmed single-answer-only. A DQ-1 apply is blocked
  until a migration design is produced and approved.
