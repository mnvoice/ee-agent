# Answer-Selection Pedagogy — Cleanup-Dependency PA Apply + PA-V Verification (2026-05-21)

Verification report for PA — the pedagogy `solution` / `steps` apply of the
6 cleanup-completed cleanup-dependency items — and the PA-V post-apply
verification.

This document records an apply that **has been performed** on `app/data`.
The change is uncommitted (working-tree only); commit/push are NOT done.

- Base commit: `6772786` (HEAD; both target files tracked)
- CL-3/CL-4 apply: `docs/audit/answer_selection_pedagogy_cleanup_dependency_cl3_apply_verification_2026-05-21.md`
  (the 6 items' `choices` cleanup, already applied to the working tree)
- pedagogy `solution` source: the dry-run document fenced blocks
  (`..._expansion_dryrun_2026-05-21.md`) — `2016_1회_44` is the
  correction-pass 491-char version; `steps` from the reviewed drafts.

## 1. Scope applied

The 6 cleanup-completed items only. `2006_1회_7` (`hold-Type-S`) and
`2001_3회_43` (`hold-source`) were NOT touched. Fields written: `solution`
and `steps` only — the CL-3 cleaned `choices` were left intact; `answer` /
`text` not modified. Target files (both modified):
`app/data/questions.json`, `app/data/questions.v2.json`.

## 2. Applied — `solution` before / after

| key | answer | solution chars (before → after) | steps |
| --- | ---: | --- | --- |
| `2015_2회_29` | 2 | 520 → 405 | v2.1 인식/변환/계산 |
| `2002_3회_4` | 4 | 652 → 447 | v2.1 인식/변환/계산 |
| `2016_1회_71` | 3 | 133 → 417 | v2.1 인식/변환/계산 |
| `2015_1회_22` | 1 | 212 → 452 | v2.1 인식/변환/계산 |
| `2015_3회_27` | 3 | 160 → 456 | v2.1 인식/변환/계산 |
| `2016_1회_44` | 4 | 804 → 491 | v2.1 인식/변환/계산 |

`answer` is shown for reference only — it was NOT modified. The applied
`solution` text equals the dry-run document's reviewed fenced block for each
item (`2016_1회_44` = the correction-pass 491-char trim); `steps` equals the
reviewed `인식`/`변환`/`계산` drafts. Confirmed by pre-apply extraction check
and re-confirmed in PA-V check [4].

## 3. PA-V verification

Method: compare the post-apply files against (a) `HEAD` `6772786` and (b) the
pre-PA snapshot (post-CL-3 working tree), deep-comparing all 5331 records.

| # | check | `questions.json` | `questions.v2.json` |
| --- | --- | --- | --- |
| 1 | changed records vs HEAD == the 6 PA targets | PASS (6/6) | PASS (6/6) |
| 2 | changed fields within targets limited to `choices`+`solution`+`steps` | PASS (no violation) | PASS (no violation) |
| 3 | `answer` / `text` invariant vs HEAD | PASS | PASS |
| — | PA-isolation: vs pre-PA snapshot, PA changed only `solution`/`steps` (`choices` untouched) | PASS | PASS |
| 4 | applied `solution` == dry-run doc / `steps` == reviewed drafts | PASS | PASS |
| 5 | `solution` is v2.1 (6 labels in order) | PASS (6/6) | PASS (6/6) |
| 6 | `정답:` is the last line | PASS (6/6) | PASS (6/6) |
| 7 | `보기 판단` references [1]-[4] ↔ 4 stored (cleaned) choices | PASS (6/6) | PASS (6/6) |
| 8 | JSON valid; `questions.json`/`questions.v2.json` synced (solution+steps+choices, 6/6) | PASS | PASS |

`git diff --stat app/data/` (cumulative CL-3 + PA, vs HEAD `6772786`):

```
 app/data/questions.json    | 62 +++++++++++++++++++++++-----------------------
 app/data/questions.v2.json |  2 +-
```

The 6 records show `choices` (CL-3) + `solution` + `steps` (PA) changed; no
non-target record changed; `answer`/`text` invariant.

PA-V overall: **PASS**.

## 4. Record-count note (no anomaly)

The corpus has **5331 records**; `git show HEAD` and the post-apply file both
have list length 5331 (confirmed — unchanged). Of these, 5283 carry a `q_no`
field and 48 do not. The `(year, session, q_no)` key is **unique for all
5283** `q_no`-bearing records — there are **0 duplicate keys**. The 48
`q_no`-less records (non-question / malformed entries) collapse under the
keying function (some intermediate verification output showed "5314 unique
keys" — this is 5283 + the collapsed `q_no`-less set, a display artifact, not
a data change). All 16 records modified across this whole track (10
apply-ready + 6 cleanup-dependency) are uniquely keyed; each was modified
exactly once.

## 5. Cumulative state of the 6 cleanup-dependency records

Vs `HEAD` `6772786`, each of the 6 now carries: the CL-3 cleaned `choices`,
the v2.1 pedagogy `solution`, and the v2.1 `steps`. The displayed choices now
match the pedagogy `보기 판단` (the cleanup-dependency mismatch is resolved).
The 10 `apply-ready` items were already applied in commit `6772786`.

## 6. Not done in this step

- `2006_1회_7` (`hold-Type-S`) — not modified.
- `2001_3회_43` (`hold-source`) — not modified.
- No `answer` / `text` / `choices` modification (CL-3 `choices` left intact).
- App code / schema — not modified.
- No commit; no push; no local server; no paid API call.

## 7. Status

- PA complete and verified: 6 cleanup-completed items' pedagogy
  `solution`/`steps` applied to `app/data/questions.json` and
  `app/data/questions.v2.json`. PA-V verification PASS — exactly 6 records
  changed vs HEAD, fields limited to `choices`+`solution`+`steps`,
  `answer`/`text` invariant, `solution`/`steps` match the reviewed drafts,
  v2.1 format and choice mapping confirmed, files synced.
- Working tree: `questions.json` + `questions.v2.json` modified (uncommitted)
  — cumulative CL-3 + PA changes for the 6 cleanup-dependency records.
- Next (separate approval): commit/push; the `2006_1회_7` Type S
  correction-review track; `2001_3회_43` textbook source check.
