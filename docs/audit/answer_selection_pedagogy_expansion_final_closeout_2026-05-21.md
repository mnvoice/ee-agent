# Answer-Selection Pedagogy — Expansion Track Final Closeout (2026-05-21)

Final closeout of the answer-selection pedagogy expansion track. It registers
`2001_3회_43` as a deferred item, summarizes the track outcome and the
held/excluded items, records the residual risks, and recommends follow-ups.

This is a **closeout summary document**. It does NOT modify `app/data`.

- Latest pushed commit: `a5e6d78` (branch `feat/phase-b-migration`,
  origin-synced, tracked working tree clean)
- Track commits: `2aadbe5` (pilot apply, prior), `6772786` (expansion
  apply-ready batch), `8f6d4c6` (cleanup-dependency batch), `a5e6d78` (Type-S
  correction)

## 1. Deferred item registration — `2001_3회_43`

`2001_3회_43` (전기기기 / 정류자형 주파수 변환기 / "설명 중 틀린 것") is
registered as **`hold-source-external-textbook-needed`** — deferred, not
applied.

Deferral basis:

- **`answer` ② is source-verified** — the source PDF 풀이 box (mathpix OCR,
  `data/mathpix_기출_2001_3회.json`) ends with `【답】(2)`, corroborated by
  `old_answer_manual_source_review_pack_2026-05-21.md` (pack1).
- **Choice [2]'s error mechanism is NOT confirmable from any repo-internal
  source.** The 풀이 box confirms choices (1), (3), (4) as correct
  descriptions but says nothing about where the 1차 / 2차 / 조정 권선 are
  placed — it never addresses choice [2]'s claim. The repo holds no 전기기기
  textbook / study material describing the machine's winding arrangement.
- A pedagogy `보기 판단` for choice [2] must state *why* [2] is wrong;
  without a source for the error mechanism, that cannot be written.
- **No estimation-based `solution`/`steps` apply** is permitted — drafting a
  `보기 판단` for [2] from inference would violate the source-verification
  discipline (the dry-run's [2] reasoning was already flagged as an
  inference, not a sourced fact).

Resolution condition: obtain an external 전기기기 textbook that confirms the
정류자형 주파수 변환기 winding arrangement / the specific error in choice
[2]. Then re-draft the `보기 판단`, trim to the v2.1 length target, and apply
as a single-item track. Until then `2001_3회_43` stays held.

## 2. Track outcome — 24 items applied and pushed

| sub-batch | items | commit |
| --- | ---: | --- |
| pilot | 7 | `2aadbe5` (prior) |
| expansion — apply-ready (clean) | 10 | `6772786` |
| expansion — cleanup-dependency | 6 | `8f6d4c6` |
| expansion — Type-S (`2006_1회_7`) | 1 | `a5e6d78` |
| **total applied & pushed** | **24** | — |

Applied keys:

- pilot (7): `2007_1회_9`, `2007_2회_64`, `2001_3회_41`, `2006_2회_27`,
  `2016_1회_70`, `2016_3회_21`, `2015_3회_22`
- apply-ready (10): `2001_1회_21`, `2015_2회_23`, `2015_3회_25`,
  `2016_1회_69`, `2015_1회_13`, `1998_4회_10`, `2006_1회_6`, `2015_1회_71`,
  `2016_3회_44`, `2001_1회_68`
- cleanup-dependency (6): `2015_2회_29`, `2002_3회_4`, `2016_1회_71`,
  `2015_1회_22`, `2015_3회_27`, `2016_1회_44`
- Type-S (1): `2006_1회_7`

All 24 carry a v2.1 plain-text-label `solution` (6 elements:
`핵심 단서`/`보기 판단`/`근거/계산`/`함정`/`시험장 판별`/`정답`) and an
`인식`/`변환`/`계산` `steps` dict. Every apply was verified — exact changed-
record count, field-scope limits, `answer` invariance, `questions.json` ↔
`questions.v2.json` sync.

## 3. Held / excluded items

| item | status | route |
| --- | --- | --- |
| `2001_3회_43` | `hold-source-external-textbook-needed` | deferred — external 전기기기 textbook (Section 1) |
| `2005_3회_83` | excluded (전기설비기술기준 statute) | a separate statute-safe track |
| `2015_1회_87` | excluded (전기설비기술기준 statute) | a separate statute-safe track |
| `2002_1회_32` | excluded (corrupted answer choice [1] = `} \end{table}`) | a separate DQ / data-quality track |

The 3 excluded items (`2005_3회_83`, `2015_1회_87`, `2002_1회_32`) were
removed at the expansion scoping stage — statute items carry an
article-fabrication risk and the corrupted item cannot have its answer choice
mapped. `2001_3회_43` reached the dry-run/review but could not be closed.

Source pool accounting: the old-answer track resolved 28 source-verified
items (9 verified + 19 corrected). pilot used 7; the 21 non-pilot →
18 expansion candidates (17 applied + 1 deferred) + 3 excluded at scoping.
`7 + 17 = 24` applied; `1` deferred; `3` routed elsewhere.

## 4. Residual risks

- **iPad / browser viewport — never live-rendered.** Both the pilot and the
  expansion viewport checks were structural fallback assessments (`bun` not
  installed; the app has no question-deep-link routing; no browser-automation
  tool available). The structural estimate is low-medium readability risk,
  but the pixel-accurate scroll burden and the choice cross-reference
  friction are unconfirmed. Mitigation: a supervisor can open
  `app/index.html` on a real iPad / desktop Chrome at iPad viewport.
- **`2001_3회_43` deferred** — depends on an external textbook source; until
  then this item keeps its pre-pedagogy `solution`/`steps`.
- **Statute track / DQ track not yet designed** — `2005_3회_83`,
  `2015_1회_87` (statute) and `2002_1회_32` (corrupted choice) await their
  own tracks; they currently keep their original data.
- **Length** — 5 of the applied solutions are slightly over the v2.1 350-500
  target (501-511 chars); judged acceptable (within the pilot's applied
  range) and not trimmed.
- **`2015_2회_29` choices** — the stored `choices` array holds the source
  풀이 lines (`설비 : 기능` format), not the source's bare question choices.
  The pedagogy `solution` is consistent with the stored format; re-sourcing
  the choices is a separate data-quality question, recorded but not actioned.

## 5. Follow-up recommendations

- **Recommended next: a learning-priority 100-item track.** The expansion
  validated the v2.1 pedagogy template against 24 source-verified items
  across 5 subjects with a stable dry-run → review → limited apply →
  closeout rhythm. Scaling to a ~100-item batch prioritized by learning
  value (high-frequency / high-miss-rate questions) is the natural next step.
  It needs a source-verification pass to widen the eligible pool beyond the
  old-answer track's 28 items (the expansion exhausted the non-pilot
  source-verified pool).
- **Single-item: `2001_3회_43`** — once an external 전기기기 textbook source
  is obtained, process `2001_3회_43` on its own (re-draft the [2]
  `보기 판단`, trim, apply, verify). Small and independent of the 100-item
  track.
- Statute and DQ items (`2005_3회_83`, `2015_1회_87`, `2002_1회_32`) — design
  the statute-safe and DQ tracks when those item classes are taken up.

## 6. Audit trail

Expansion-track audit documents (`docs/audit/`):

- expansion: `..._expansion_dryrun_`, `..._expansion_dryrun_review_`,
  `..._expansion_correction_`, `..._expansion_apply_verification_`,
  `..._expansion_apply_viewport_check_` (commit `6772786`)
- cleanup-dependency: `..._cleanup_dependency_batch_design_`,
  `..._cleanup_dependency_dryrun_`, `..._cleanup_dependency_cl2_review_`,
  `..._cleanup_dependency_cl3_apply_verification_`,
  `..._cleanup_dependency_pa_apply_verification_`,
  `..._expansion_content_preservation_review_` (commit `8f6d4c6`)
- Type-S: `..._residual_2_closeout_review_`,
  `..._2006_1_7_type_s_apply_verification_` (commit `a5e6d78`)
- this document: `..._expansion_final_closeout_2026-05-21.md`

## Not done in this step

- No `app/data/questions.json` / `questions.v2.json` modification.
- No `solution` / `steps` apply.
- No `answer` / `choices` / `text` modification.
- No `2001_3회_43` apply (deferred).
- No commit; no push (this document's commit/push is a separate approval).

## Status

- Answer-selection pedagogy expansion track closed: **24 items applied and
  pushed** (pilot 7 + apply-ready 10 + cleanup-dependency 6 + Type-S 1) across
  commits `2aadbe5` / `6772786` / `8f6d4c6` / `a5e6d78`.
- **1 deferred**: `2001_3회_43` (`hold-source-external-textbook-needed`).
- **3 routed elsewhere**: `2005_3회_83`, `2015_1회_87` (statute-safe track),
  `2002_1회_32` (DQ track).
- Recommended follow-up: a learning-priority ~100-item track (after a
  source-verification pass), and a single-item resolution of `2001_3회_43`
  once an external textbook source is available.
- This closeout document's commit/push awaits separate approval.
