# Answer-Selection Pedagogy — Cleanup-Dependency Batch Design (2026-05-21)

Design for the cleanup-dependency batch — the 7 expansion items deferred from
the limited apply because their displayed `choices` / `text` carry OCR
residue that would mismatch the pedagogy `보기 판단`.

This is a **design document only**. It does NOT modify `app/data`. The actual
`choices` / `text` cleanup and the pedagogy `solution` / `steps` apply each
require separate approval.

- Base commit: `6772786` (expansion batch — the 10 apply-ready items applied)
- Inputs: `docs/audit/answer_selection_pedagogy_expansion_correction_2026-05-21.md`
  (the 4-bucket classification), the dry-run draft
  (`..._expansion_dryrun_2026-05-21.md`)
- Pilot precedent: choice-cleanup `35f422e` ran **before** the pedagogy apply
  `2aadbe5`
- Source material confirmed present: `data/mathpix_기출_{2015_1회,2015_2회,
  2015_3회,2002_3회,2016_1회,2006_1회}.json` (mathpix OCR of the source PDFs)

## 1. Scope — 7 cleanup-dependency items

| # | key | OCR location | stored text (issue) | evident correct |
| --- | --- | --- | --- | --- |
| 1 | `2015_1회_22` | choice [2] | `전압변동을 직접 한다` | `직접` → `적게` (word) |
| 2 | `2015_3회_27` | choice [4] | `고속도 자단방식을 채용한다` | `자단` → `차단` (word) |
| 3 | `2015_2회_29` | choice [4] | `… 단선 방지 [답] 15년도 2회 / 439 / 전기기사 펄기 D－60 시리즈` | delete trailing page-footer residue |
| 4 | `2002_3회_4` | choice [4] | `\(U=\frac{1}{4πε}\iint\frac{ρs}{r}ds\) 2-286 / D-60 전기기사` | delete trailing page-footer residue |
| 5 | `2016_1회_71` | choice [4] | `\(E_l = rac{1}{\sqrt{3}}E_p\)` | LaTeX `rac{` → `\frac{` |
| 6 | `2006_1회_7` | `text` (z항) | `k 3 Z e^{\overline{4 z}}` | `3 Z`→`3z`, remove `\overline` |
| 7 | `2016_1회_44` | choice [2]/[3] | `… 굽은 회전방향으로 …` | remove spurious `굽은` |

All 7 have their v2.1 pedagogy `solution` / `steps` already drafted and
reviewed in the expansion dry-run. `2016_1회_44`'s `solution` was trimmed to
491 chars in the correction pass; the other 6 are unchanged from the dry-run.

## 2. Cleanup decision

The `choices` / `text` cleanup **precedes** the pedagogy `solution` / `steps`
apply for these 7 items. Reason: if the pedagogy `solution` is applied first,
the displayed choice/text (still carrying OCR residue) mismatches the
solution's `보기 판단`, which describes the evident meaning. Cleaning the
displayed text first removes the mismatch. This follows the pilot precedent
(`35f422e` choice-cleanup before `2aadbe5` pedagogy apply).

Constraint: the cleanup modifies `choices` / `text` — separate approval is
required for each modifying step (Section 4). This design does not execute
any modification.

## 3. Cleanup-type classification

All 7 corrections must be transcribed/confirmed against the source PDF
mathpix OCR (the old-answer choice-OCR recovery discipline, `fac4b8d`). The
sub-types differ by risk and by how much text changes:

- **Type R — residue deletion** (choice/text sentence intact; trailing junk
  removed): `2015_2회_29` [4], `2002_3회_4` [4]. Lowest risk.
- **Type L — LaTeX artifact fix** (single known artifact): `2016_1회_71` [4]
  (`rac{` → `\frac{`).
- **Type W — word-level change** (a content word substituted/removed —
  highest care, must match source): `2015_1회_22` [2] (`직접`→`적게`),
  `2015_3회_27` [4] (`자단`→`차단`), `2016_1회_44` [2]/[3] (remove `굽은`).
- **Type S — stem text fix** (`text`, the question stem — the most sensitive
  surface): `2006_1회_7` (`3 Z e^{\overline{4 z}}` → `3z e^{4z}`).

## 4. Small-step sequencing

The batch is broken into small steps; every `app/data`-modifying step is a
separate supervisor approval.

| step | action | modifies app/data | approval |
| --- | --- | --- | --- |
| CL-1 | choices/text cleanup dry-run — transcribe correct text from the mathpix source for all 7; per-item before/after + confidence | no | — |
| CL-2 | review the cleanup dry-run; checkpoint: after each correction, the item's pedagogy `보기 판단` still maps to the cleaned choice/text | no | — |
| CL-3a | cleanup apply — Type R + Type L (`2015_2회_29`, `2002_3회_4`, `2016_1회_71`) — lowest-risk sub-batch | yes (`choices`) | separate |
| CL-3b | cleanup apply — Type W (`2015_1회_22`, `2015_3회_27`, `2016_1회_44`) | yes (`choices`) | separate |
| CL-3c | cleanup apply — Type S (`2006_1회_7`, question `text`) — its own step | yes (`text`) | separate |
| CL-4 | post-cleanup verification — only target `choices`/`text` changed; record count, answer/solution/steps invariant | no | — |
| PA | pedagogy `solution`/`steps` apply for the 7 — same method as the 10-item apply (`questions.json` + `questions.v2.json`, `solution`/`steps` only) | yes (`solution`/`steps`) | separate |
| PA-V | post-apply verification + viewport check for the 7 | no | — |

Sequencing rationale:

- CL (cleanup) before PA (pedagogy apply) — Section 2.
- CL-3 is split a/b/c by risk type so the lowest-risk corrections can be
  approved/verified independently of the word-level and stem changes; CL-3c
  (`text`) is isolated because the question stem is the most sensitive
  surface.
- PA reuses the already-reviewed v2.1 drafts; no re-drafting — but CL-2 must
  confirm each `보기 판단` still maps after the cleaned text (the drafts
  already describe the evident meaning, so this is expected to hold, but it
  is an explicit checkpoint).

## 5. Pedagogy drafts for the 7 — status

The 7's v2.1 `solution`/`steps` exist and were reviewed in the expansion
dry-run / correction pass. They are NOT re-opened by this design. The PA step
applies them as-is, after CL. If CL-2 finds a `보기 판단` no longer matches a
cleaned choice, that item's draft returns to a small re-draft before PA
(not expected, but the checkpoint exists).

## 6. `2001_3회_43` — out of scope (hold-source, confirmed)

`2001_3회_43` is NOT part of this cleanup-dependency batch. It is
`hold-source`: the answer ② is source-verified, but the *reason* choice [2]
is wrong is not confirmed by the source 풀이 box (it does not state the
winding arrangement). Its hold is a content/source gap, not an OCR-residue
issue, so it does not belong in an OCR-cleanup batch.

Per the 2026-05-21 supervisor decision, `2001_3회_43` remains `hold-source`
and excluded from apply until a 전기기기 textbook (external source, not the
기출 해설) confirms the error mechanism in choice [2]. No external/textbook
basis is available in-repo, so it stays excluded.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `choices` / `text` cleanup executed (CL-1 dry-run not run here).
- No pedagogy `solution` / `steps` apply for the 7.
- No `2001_3회_43` change.
- No commit; no push.
- No paid API call.

## Status

- Cleanup-dependency batch design complete: 7 items scoped, cleanup decision
  set (cleanup precedes pedagogy apply, per pilot precedent), 4 cleanup
  sub-types classified, an 8-step small-step sequence defined with every
  modifying step as a separate approval.
- `2001_3회_43` confirmed `hold-source`, excluded.
- Next (separate approval): CL-1 — the choices/text cleanup dry-run,
  transcribing the 7 corrections from the mathpix source.
