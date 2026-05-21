# Answer-Selection Pedagogy — Expansion Limited Apply Verification (2026-05-21)

Verification report for the limited apply of the answer-selection pedagogy
expansion — the 10 `apply-ready` items. It records what was applied, the
post-apply verification, and the residual observations.

This document records an apply that **has been performed** on `app/data`.
The change is uncommitted (working-tree only); commit/push are NOT done.

- Base commit: `f09b97e` (both target files tracked and clean at this HEAD)
- Correction pass: `docs/audit/answer_selection_pedagogy_expansion_correction_2026-05-21.md`
- Dry-run: `docs/audit/answer_selection_pedagogy_expansion_dryrun_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## 1. Scope applied

The `apply-ready` group only — 10 items. The 7 `apply-ready-with-cleanup-
dependency` items and the 1 `hold-source` item were NOT applied.

Target files (both modified): `app/data/questions.json` (indent=2,
ensure_ascii=False) and `app/data/questions.v2.json` (compact single-line,
ensure_ascii=False). Each file's serialization was verified to round-trip
byte-identically before the apply, so the re-dump changes only the 10
records.

Fields written: `solution` and `steps` only. `answer`, `choices`, `text`,
and every other field were not modified. In `questions.v2.json`,
`solution_source` / `steps_source` were also NOT modified (see Section 4).

## 2. Applied items — before / after `solution` length

| key | answer | solution chars (before → after) | steps |
| --- | ---: | --- | --- |
| `2001_1회_21` | 2 | 240 → 453 | v2.1 인식/변환/계산 |
| `2015_2회_23` | 4 | 943 → 461 | v2.1 인식/변환/계산 |
| `2015_3회_25` | 4 | 483 → 468 | v2.1 인식/변환/계산 |
| `2016_1회_69` | 4 | 676 → 501 | v2.1 인식/변환/계산 |
| `2015_1회_13` | 1 | 253 → 465 | v2.1 인식/변환/계산 |
| `1998_4회_10` | 4 | 990 → 493 | v2.1 인식/변환/계산 |
| `2006_1회_6` | 3 | 758 → 511 | v2.1 인식/변환/계산 |
| `2015_1회_71` | 1 | 626 → 442 | v2.1 인식/변환/계산 |
| `2016_3회_44` | 4 | 164 → 409 | v2.1 인식/변환/계산 |
| `2001_1회_68` | 3 | 642 → 505 | v2.1 인식/변환/계산 |

`answer` is shown for reference only — it was NOT modified; the before/after
columns are `solution` character counts. The applied `solution` text is
identical to the dry-run document's reviewed candidate (cross-checked
char-for-char before apply: all 10 doc ↔ apply-data matches).

## 3. Verification

Method: load the `HEAD` (`f09b97e`) version of each file via `git show` and
the post-apply version; deep-compare all 5331 records.

`app/data/questions.json`:

- record count: HEAD 5331 → now 5331 (unchanged).
- changed records: exactly 10 — and the set of changed records equals the 10
  target keys exactly.
- non-target records changed: none.
- target records — non-`solution`/`steps` field changes: none.
- per item: `answer` / `choices` / `text` invariant — YES (10/10).
- per item: `solution` is v2.1 (6 labels in order, `정답:` last line, choices
  [1]-[4] referenced) — YES (10/10).
- per item: `steps` keys exactly `인식` / `변환` / `계산` — YES (10/10).

`app/data/questions.v2.json`:

- record count: HEAD 5331 → now 5331 (unchanged).
- changed records: exactly 10 — equals the 10 target keys exactly.
- non-target records changed: none.
- target records — non-`solution`/`steps` field changes: none (incl.
  `solution_source` / `steps_source` unchanged).
- per item: `answer` / `choices` / `text` invariant — YES (10/10).
- per item: `solution` v2.1 / `steps` keys — YES (10/10).

`git diff --stat app/data/`:

```
 app/data/questions.json    | 80 +++++++++++++++++++++++-----------------------
 app/data/questions.v2.json |  2 +-
 2 files changed, 41 insertions(+), 41 deletions(-)
```

`questions.json` shows 80 changed lines confined to the 10 records'
`solution` + `steps` lines. `questions.v2.json` is a single-line file, so its
whole line is rewritten; the structural deep-compare above confirms the
content change is confined to the 10 records' `solution`/`steps`.

Both files parse as valid JSON after the apply.

Overall verification: **PASS**.

## 4. Observations

- **`solution_source` / `steps_source` not updated** — `questions.v2.json`
  carries provenance metadata fields `solution_source` and `steps_source`.
  Per the apply instruction ("`solution`/`steps`만 변경"), these were left
  untouched. (Correction, 2026-05-21: an earlier draft of this bullet called
  them "stale"; on reading the actual values they are
  `{"source":"llm_synthesized","tool_name":null,"verified_at":null}` — a
  generic marker that remains accurate for the new v2.1 pedagogy content,
  which is also LLM-synthesized. So they are NOT stale; no update is
  required. Confirmed in the viewport-check report.)
- **3 of 10 solutions are slightly over the v2.1 350-500 target** —
  `2016_1회_69` 501, `2001_1회_68` 505, `2006_1회_6` 511 (≤2.2% over, within
  the pilot's applied 512-678 range). The review judged these "no trim
  needed"; recorded here as carried-forward.
- **iPad / browser viewport check pending** — per the supervisor decision,
  the viewport check is a post-apply quality gate, to be run separately
  (local server / iPad not run in this step).
- The working tree now has 2 modified tracked files (`questions.json`,
  `questions.v2.json`). They are uncommitted; commit/push await separate
  approval.

## 5. Not done in this step

- The 7 `apply-ready-with-cleanup-dependency` items — NOT applied.
- The 1 `hold-source` item (`2001_3회_43`) — NOT applied.
- `answer` / `choices` / `text` — not modified.
- `solution_source` / `steps_source` — not modified.
- App code / schema — not modified.
- No local server run; no iPad / browser viewport check.
- No commit; no push.
- No paid API call.

## 6. Status

- Limited apply complete and verified: 10 `apply-ready` pedagogy
  `solution`/`steps` applied to `app/data/questions.json` and
  `app/data/questions.v2.json`. Exactly 10 records changed in each file;
  `answer`/`choices`/`text` invariant; v2.1 format confirmed.
- Change is uncommitted (working-tree only).
- Next (separate approval): the post-apply iPad / browser viewport check;
  a decision on the `solution_source`/`steps_source` provenance update;
  commit/push; then the cleanup-dependency batch (7) and the `2001_3회_43`
  source check.
