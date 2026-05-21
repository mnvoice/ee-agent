# Answer-Selection Pedagogy — `2006_1회_7` Type-S Apply + Verification (2026-05-21)

Verification report for the Type-S apply of `2006_1회_7` — the question-stem
text correction plus the pedagogy `solution`/`steps` apply.

This document records an apply that **has been performed** on `app/data`.
The change is uncommitted (working-tree only); commit/push are NOT done.

- Base commit: `8f6d4c6` (`2006_1회_7` untouched by any prior commit — both
  target files tracked and clean at this HEAD)
- Decision basis: `docs/audit/answer_selection_pedagogy_residual_2_closeout_review_2026-05-21.md`
  (`2006_1회_7` ruled `apply-ready-Type-S`)
- pedagogy `solution` source: the expansion dry-run document, item #8 fenced
  block; `steps` from the reviewed draft.

## 1. Scope applied

`2006_1회_7` only — fields written: `text`, `solution`, `steps`.
`answer` and `choices` NOT modified. `2001_3회_43` and all other records NOT
touched. Target files (both modified): `app/data/questions.json`,
`app/data/questions.v2.json`.

## 2. Applied changes

### (a) `text` stem correction

- before (z-component): `… +k 3 Z e^{\overline{4 z}}`
- after (z-component): `… +k 3 z e^{4 z}`
- change: capital `Z` → lowercase coordinate `z`; the spurious `\overline`
  removed. The rest of `text` is unchanged.
- basis: the source PDF's own 풀이 region (mathpix OCR) writes
  `\frac{\partial}{\partial z}\left(3 z e^{4 z}\right)` and computes
  `div E = 3`; `answer`=2 (`choices[2]`=`3`) holds only for the z-component
  `3z·e^{4z}`. `e^{\overline{4z}}` is not valid notation — an OCR artifact
  of the source's stem region.

### (b) pedagogy `solution` / `steps`

- `solution`: the v2.1 plain-text-label draft (expansion dry-run item #8),
  465 chars — already uses the clean `3z·e^{4z}` form, so it is consistent
  with the corrected stem.
- `steps`: the reviewed `인식`/`변환`/`계산` draft.

## 3. Verification

Method: `git show HEAD` (`8f6d4c6`) vs the post-apply files; deep-compare all
5331 records.

| # | check | `questions.json` | `questions.v2.json` |
| --- | --- | --- | --- |
| 1 | changed records exactly 1 (`2006_1회_7`) | PASS | PASS |
| 2 | changed fields == {`text`, `solution`, `steps`} | PASS | PASS |
| 3 | `answer` / `choices` invariant | PASS | PASS |
| 4 | `text` corrected to `3 z e^{4 z}` (no `\overline`, no `3 Z`) | PASS | PASS |
| 5 | `solution`/`steps` consistent with the corrected `text` (clean `3z·e^{4z}`) | PASS | PASS |
| 6 | `solution` is v2.1 (6 labels in order) | PASS | PASS |
| 7 | `정답:` is the last line | PASS | PASS |
| 8 | `보기 판단` references [1]-[4] ↔ 4 stored choices | PASS | PASS |
| 9 | JSON valid; `steps` keys `인식`/`변환`/`계산`; `questions.json`/`questions.v2.json` synced (text+solution+steps) | PASS | PASS |

`git diff --stat app/data/`:

```
 app/data/questions.json    | 10 +++++-----
 app/data/questions.v2.json |  2 +-
```

`questions.json`: 5 changed lines for the one record (`text` 1 + `solution` 1
+ `steps` 3). `questions.v2.json`: single-line file, structural deep-compare
confirms the content change is confined to `2006_1회_7`'s `text`/`solution`/
`steps`. Record count 5331 unchanged.

Type-S apply verification: **PASS**.

## 4. Not done in this step

- `2001_3회_43` — not modified (remains `hold-source-external-textbook-needed`,
  deferred).
- No `answer` / `choices` modification.
- No other record modified; no app code / schema change.
- No commit; no push; no local server; no paid API call.

## 5. Status

- `2006_1회_7` Type-S apply complete and verified: the stem `text` corrected
  (`3 Z e^{\overline{4 z}}` → `3 z e^{4 z}`) and the v2.1 pedagogy
  `solution`/`steps` applied to `app/data/questions.json` and
  `app/data/questions.v2.json`. Exactly 1 record changed; fields limited to
  `text`+`solution`+`steps`; `answer`/`choices` invariant; files synced.
- Change is uncommitted (working-tree only).
- Track state: 24 expansion items now carry the v2.1 pedagogy
  `solution`/`steps` (10 apply-ready + 6 cleanup-dependency + `2006_1회_7`);
  `2001_3회_43` remains the sole deferred item (`hold-source`).
- Next (separate approval): commit/push; for `2001_3회_43`, an external
  전기기기 textbook source or a deferred-item record.
