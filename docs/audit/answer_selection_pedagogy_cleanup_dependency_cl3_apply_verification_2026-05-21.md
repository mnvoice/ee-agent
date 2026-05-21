# Answer-Selection Pedagogy — Cleanup-Dependency CL-3a/CL-3b Apply + CL-4 Verification (2026-05-21)

Verification report for CL-3a / CL-3b — the `choices` cleanup apply of the 6
`pass-apply-ready` cleanup-dependency items — and the CL-4 post-apply
verification.

This document records an apply that **has been performed** on `app/data`.
The change is uncommitted (working-tree only); commit/push are NOT done.

- Base commit: `6772786` (both target files tracked and clean at this HEAD)
- CL-2 review: `docs/audit/answer_selection_pedagogy_cleanup_dependency_cl2_review_2026-05-21.md`
- CL-1 dry-run: `docs/audit/answer_selection_pedagogy_cleanup_dependency_dryrun_2026-05-21.md`

## 1. Scope applied

The 6 `pass-apply-ready` items only — 7 `choices` element corrections across
6 records. Target files (both modified): `app/data/questions.json` and
`app/data/questions.v2.json`. Field written: the named `choices[]` elements
only. `answer`, `text`, `solution`, `steps`, and every other field were not
modified. `2006_1회_7` (`hold-Type-S`) and `2001_3회_43` (`hold-source`) were
NOT touched; no pedagogy `solution`/`steps` apply was done.

## 2. Applied corrections — before / after

| key | choice | type | before | after |
| --- | --- | --- | --- | --- |
| `2015_2회_29` | [4] | R | `…단선 방지\n[답] 15년도 2회\n439\n전기기사 펄기 D－60 시리즈` | `아모 로드(Armour rod) : 전선의 진동에 의한 전선의 단선 방지` |
| `2002_3회_4` | [4] | R | `\(U=\frac{1}{4πε}\iint\frac{ρs}{r}ds\) 2-286\nD-60 전기기사` | `\(U=\frac{1}{4 \pi \epsilon} \iint \frac{\rho_{s}}{r} d s\)` |
| `2016_1회_71` | [4] | L | `\(E_l = ` + `<U+000C>` + `rac{1}{\sqrt{3}}E_p\)` | `\(E_l = \frac{1}{\sqrt{3}}E_p\)` |
| `2015_1회_22` | [2] | W | `전압변동을 직접 한다.` | `전압변동을 적게 한다.` |
| `2015_3회_27` | [4] | W | `…고속도 자단방식을 채용한다.` | `…고속도 차단방식을 채용한다.` |
| `2016_1회_44` | [2] | W | `발전기의 굽은 회전방향으로 …` | `발전기의 경우 회전방향으로 …` |
| `2016_1회_44` | [3] | W | `전동기의 굽은 회전방향과 반대방향으로 …` | `전동기의 경우 회전방향과 반대방향으로 …` |

The apply script asserted, per correction, that (a) `questions.json` and
`questions.v2.json` held the same pre-value (sync precondition), (b) the
transform result equals the CL-2-verified expected value, (c) the value
actually changed. All 7 assertions passed.

## 3. CL-4 verification

Method: `git show HEAD` (`6772786`) version of each file vs the post-apply
version; deep-compare all 5331 records.

| # | check | `questions.json` | `questions.v2.json` |
| --- | --- | --- | --- |
| 1 | changed records exactly 6 (= the 6 targets) | PASS | PASS |
| 2 | only `choices` field changed; within it only the named indices | PASS (no violation) | PASS (no violation) |
| 3 | `answer` / `text` / `solution` / `steps` invariant (6/6) | PASS | PASS |
| 3' | non-target records changed | none | none |
| 4 | JSON parses valid | PASS | PASS |
| 5 | the 6 records' `choices` synced `questions.json` == `questions.v2.json` | — | PASS (6/6) |
| 6 | corrected values equal the CL-2-verified expected values | PASS | PASS |
| 7 | record count 5331 unchanged | PASS | PASS |

`git diff --stat app/data/`:

```
 app/data/questions.json    | 14 +++++++-------
 app/data/questions.v2.json |  2 +-
 2 files changed, 8 insertions(+), 8 deletions(-)
```

`questions.json`: 7 changed lines (the 7 corrected `choices` strings).
`questions.v2.json`: single-line file, whole line rewritten; the structural
deep-compare confirms the content change is confined to the 6 records' named
`choices` elements.

CL-4 overall: **PASS**.

## 4. Observations

- `2016_1회_71` choice [4] previously contained a `U+000C` form-feed control
  character; it is removed by the `\frac` correction (a data-hygiene
  improvement alongside the LaTeX fix).
- The 6 corrections do not affect any `answer` and do not conflict with the
  cleanup-dependency items' pedagogy `보기 판단` (confirmed in CL-2). The
  pedagogy `solution`/`steps` for these 7 items are still NOT applied — that
  is the PA step.
- The working tree now has 2 modified tracked files; uncommitted.

## 5. Not done in this step

- `2006_1회_7` (`hold-Type-S`) — not modified; awaits the CL-3c Type S review.
- `2001_3회_43` (`hold-source`) — not modified.
- No `answer` / `text` / `solution` / `steps` modification.
- No pedagogy `solution` / `steps` apply (PA step, separate).
- App code / schema — not modified.
- No commit; no push; no local server; no paid API call.

## 6. Status

- CL-3a / CL-3b complete and verified: 6 `pass-apply-ready` choices
  corrections applied to `app/data/questions.json` and
  `app/data/questions.v2.json` (7 `choices` elements, 6 records). CL-4
  verification PASS — exactly 6 records changed, only the named `choices`
  elements, all other fields invariant, files synced, values match CL-2.
- Change is uncommitted (working-tree only).
- Next (separate approval): CL-3c — the `2006_1회_7` Type S correction
  review; then PA — the pedagogy `solution`/`steps` apply for the 7
  cleanup-dependency items; commit/push.
