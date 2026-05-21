# Answer-Selection Pedagogy — Expansion Dry-run Review (2026-05-21)

Read-only review of the 18-item expansion solution dry-run. It checks v2.1
format compliance, answer/choice mapping accuracy, the 6 OCR flags, the
`2001_3회_43` content risk, and the 5 over-target lengths, then classifies
each item for limited apply.

This is a **read-only review document**. It does NOT modify `app/data`, does
NOT apply any `solution` / `steps`, and is not an approval to apply.

- Base commit: `f09b97e`
- Reviewed: `docs/audit/answer_selection_pedagogy_expansion_dryrun_2026-05-21.md`
- Template: `docs/audit/answer_selection_pedagogy_template_v2_1_plaintext_2026-05-21.md`
- Pilot review precedent: `docs/audit/answer_selection_pedagogy_pilot_review_2026-05-21.md`

## 0. Review independence note

The dry-run and this review were produced by the same instance — this is a
self-review, not an independent audit (builder-auditor are not separated
here). What this review CAN verify independently: (a) format, mechanically,
by re-running the length/label measurement script; (b) the calculation-type
physics, re-derived from scratch this turn; (c) answers cross-checked against
the source 【답】 markers in `old_answer_conflict_correction_manifest`. What
it canNOT substitute: an independent reviewer, and — for `2001_3회_43` — a
textbook (see Section 4). Treat Section 4 as the one item this review cannot
close on its own.

## 1. v2.1 format compliance

Mechanically re-measured (script over the 18 solution/steps strings):

- All 18 `solution` drafts carry the 6 required plain-text labels in order:
  `핵심 단서:` / `보기 판단:` / `근거/계산:` / `함정:` / `시험장 판별:` /
  `정답:`. Elements separated by one blank line.
- All 18 end with `정답:` as the last line.
- No markdown bold / heading / table in any draft. Unicode (`→ ↑ ↓ ∝ ²` …)
  and `[1]`-`[4]` only — renders safely under `escapeHC` + `pre-wrap`.
- All 18 `steps` keep the `인식` / `변환` / `계산` dict (keys exact, in
  order).
- `다른 과목 연결:` omitted for all 18 — v2.1-compliant (the element is
  conditional; forced links are prohibited; no link in this pool is as
  strong as the pilot's `2007_2회_64`).

Verdict: format compliant for all 18.

Minor observation (non-blocking): 2 items put a formula in `핵심 단서:`,
which v2.1 nominally reserves for `근거/계산:` — `2006_1회_7`
(`div E = ∂Ex/∂x+…`) and `2015_1회_71` (`τ=L/R`). `2002_3회_4` and
`2001_1회_68` are borderline (a proportionality / a quoted stem formula).
This is a light-polish item for apply-prep, not a blocker.

## 2. Answer / choice mapping accuracy

All 18 `정답:` lines match the stored `q.answer`. Per-choice `보기 판단`
references all 4 actual stored choices in every item.

Calculation-type items re-derived independently this turn:

- `2006_1회_7` div E at origin = ∂Ex/∂x + ∂Ey/∂y + ∂Ez/∂z = 0+0+3 = 3 →
  choice [2]. ✓
- `2015_1회_13` S = |E|²/η₀ = 25×10⁻⁴/377 = 6.631×10⁻⁶ → choice [1]. ✓
- `1998_4회_10` H2x = μR1·2/μR2 = 1; B₂/μ0 = (4, −8, 8) → choice [4]. ✓
- `2015_1회_71` L = N·φ/I = 12 H; τ = L/R = 1 s → choice [1]. ✓
- `2006_1회_6` Q[cal] = 0.24·CV²t/(ερ) (1 J = 0.239 cal) → choice [3]. ✓
- `2001_1회_21` L = 0.4605 log₁₀(D/r) + 0.05 → choice [2]. ✓
- `2015_2회_23` π-circuit Is = C·Er + D·Ir = Y(1+ZY/4)Er + (1+ZY/2)Ir →
  choice [4]. ✓
- `2002_3회_4` surface-charge potential U = (1/4πε)∬ρs/r dS → choice [4]. ✓

Concept/memory items cross-checked against the source 【답】 markers
(`old_answer_conflict_correction_manifest`, pack source-fill commits) and
standard theory: `2015_1회_22`/`2015_3회_27` (안정도, X 반비례),
`2015_2회_29` (피뢰기), `2015_3회_25` (반한시-정한시), `2016_1회_69`
(고유주파수), `2016_3회_44` (무부하시험), `2016_1회_44` (전기자 반작용 ≠
[4]), `2016_1회_71` (△ E_l=E_p), `2001_1회_68` (가속도 오차 상수) — all
consistent.

Verdict: answer/choice mapping correct for all 18. One item (`2001_3회_43`)
has a correct *answer* but an inference-based *reason* — see Section 4.

## 3. OCR flags (6) — blocking judgment

Flagged: `2015_1회_22` [2] (`직접`→`적게`), `2015_3회_27` [4] (`자단`→
`차단`), `2015_2회_29` [4] (trailing footer residue), `2002_3회_4` [4]
(trailing footer residue), `2016_1회_71` [4] (LaTeX residue `rac{`→`\frac{`),
`2006_1회_7` `text` z-component (`\overline`, and `3 Z`→`3z` capitalization).

Do they block the apply? **No** — the pedagogy apply modifies `solution` /
`steps` only; the OCR residue lives in `choices` / `text`, which the apply
does not touch. The answer-relevant meaning is readable in all 6, and each
draft references the evident meaning.

But: a learner sees the displayed `choices` / `text` next to the solution. A
solution that says "전압 변동을 줄이면 …" beside a choice displaying
"전압변동을 직접 한다" reads as an inconsistency. The pilot handled exactly
this — it ran a choice-cleanup pass (`35f422e`) before the pedagogy apply
(`2aadbe5`).

Judgment: the 6 OCR flags are **non-blocking for the solution/steps apply**,
but per the pilot precedent a companion `choices` / `text` cleanup pass
should land before or bundled with the pedagogy apply for these 6, so the
displayed text matches the solution's `보기 판단`. That cleanup is a separate
track (it modifies `choices`/`text`, needs its own approval) and does not
hold up the solution/steps dry-run → apply pipeline; it is a sequencing
dependency, not a gate.

Latent (not in the dry-run's flag list): `2016_1회_44` choices [2]/[3]
contain "굽은 회전방향", which reads as OCR noise (the standard wording is
plain "회전방향"). Non-answer-affecting, non-blocking — fold into the same
companion cleanup if that item's choices are touched.

## 4. `2001_3회_43` content risk — source spot-check

**Required, and broader than a spot-check.** The answer (②) is verified by
the source 【답】 marker (`old_answer_conflict_correction_manifest`, pack1
`4317aea`). But the dry-run's `보기 판단` / `근거/계산` for choice [2] states
the *reason* it is wrong as: "표준은 1차·조정권선이 고정자, 2차가 회전자".

That reason is a (c) inference, not an (a) source: it was derived by negating
choice [2] (if [2] is wrong and [2] says rotor for 1차·조정 / stator for 2차,
then "correct" = the reverse). The source confirms [2] is the wrong choice;
it does NOT confirm that the rotor/stator swap is *the* error — the error in
[2] could instead lie in the winding count or naming. 정류자형 주파수
변환기 is an infrequently-tested special machine, so this cannot be closed by
self-review.

Verdict: `2001_3회_43` is **held from apply** until a textbook source
confirms the actual error in choice [2]. After the source check, the
`보기 판단` / `근거/계산` for [2] must be re-drafted to state the
source-confirmed error (and the over-length trimmed at the same time).

## 5. Length — 5 over-target items

Target (v2.1): `solution` 350-500 chars. 13/18 within target. 5 over:
`2016_1회_69` 501, `2001_1회_68` 505, `2006_1회_6` 511, `2001_3회_43` 530,
`2016_1회_44` 548. All `steps` (101-154) are within 100-180.

- `2016_1회_69` 501, `2001_1회_68` 505, `2006_1회_6` 511 — over by 1-11
  chars (≤2.2%). On a ~500-char Korean target this is measurement noise; all
  three are well below the pilot's applied range (512-678, `2aadbe5`, review
  7/7 `keep`). **No trim needed** — treat as at-target.
- `2001_3회_43` 530, `2016_1회_44` 548 — over by 30/48 chars. Still below the
  pilot's 678 max, but a real margin over the v2.1 target the project
  deliberately tightened to after the pilot. **Light trim recommended** to
  ≤500; achievable by tightening `함정` / `시험장 판별` without cutting the
  per-choice `보기 판단` substance. For `2001_3회_43` the trim happens
  together with the Section 4 re-draft; for `2016_1회_44` it is a standalone
  light trim.

Verdict: length is not a blocker for any item. `2016_1회_44` carries a
needs-trim note; `2001_3회_43`'s trim is absorbed into its source-check
re-draft.

## 6. Classification (18)

| # | key | format | mapping | length | classification |
| --- | --- | --- | --- | ---: | --- |
| 1 | `2001_1회_21` | ok | ✓ | 453 | pass |
| 2 | `2015_1회_22` | ok | ✓ | 452 | pass (+choice-cleanup) |
| 3 | `2015_3회_27` | ok | ✓ | 456 | pass (+choice-cleanup) |
| 4 | `2015_2회_23` | ok | ✓ | 461 | pass |
| 5 | `2015_2회_29` | ok | ✓ | 405 | pass (+choice-cleanup) |
| 6 | `2015_3회_25` | ok | ✓ | 468 | pass |
| 7 | `2016_1회_69` | ok | ✓ | 501 | pass |
| 8 | `2006_1회_7` | 핵심단서 formula | ✓ | 465 | pass (+text-cleanup) |
| 9 | `2015_1회_13` | ok | ✓ | 465 | pass |
| 10 | `1998_4회_10` | ok | ✓ | 493 | pass |
| 11 | `2002_3회_4` | ok | ✓ | 447 | pass (+choice-cleanup) |
| 12 | `2006_1회_6` | ok | ✓ | 511 | pass |
| 13 | `2015_1회_71` | 핵심단서 formula | ✓ | 442 | pass |
| 14 | `2016_3회_44` | ok | ✓ | 409 | pass |
| 15 | `2001_3회_43` | ok | answer ✓ / reason inferred | 530 | needs-source-check |
| 16 | `2016_1회_44` | ok | ✓ | 548 | needs-trim (+minor choice OCR) |
| 17 | `2016_1회_71` | ok | ✓ | 417 | pass (+choice-cleanup) |
| 18 | `2001_1회_68` | ok | ✓ | 505 | pass |

Tally: **pass 16** (of which 6 carry a companion `choices`/`text` cleanup —
items 2, 3, 5, 8, 11, 17), **needs-trim 1** (`2016_1회_44`),
**needs-source-check 1** (`2001_3회_43`), **hold 0**.

No item is a `hold` — every answer and per-choice mapping is correct; the two
non-pass items are resolvable (a trim, a source check).

## 7. Judgment — recommended apply sequencing

- **16 pass items** — solution/steps drafts are apply-ready. For the 6 with a
  companion cleanup, sequence a `choices` / `text` cleanup pass (separate
  approval, like the pilot's `35f422e`) before or bundled with their pedagogy
  apply, so the displayed text matches the solution. The other 10 pass items
  have no dependency.
- **`2016_1회_44` (needs-trim)** — light trim 548 → ≤500 before apply
  (tighten `함정` / `시험장 판별`); then it joins the pass set.
- **`2001_3회_43` (needs-source-check)** — hold from apply. Confirm the error
  in choice [2] from a 전기기기 textbook, re-draft `보기 판단` / `근거/계산`,
  trim 530 → ≤500, then re-review.
- All applies remain gated by supervisor approval and the iPad / browser
  viewport check (the limited-apply quality gate per the 2026-05-21
  supervisor decision). No bulk apply; dry-run → review → limited apply →
  closeout.
- Optional polish (non-blocking): move the `핵심 단서:` formulas in
  `2006_1회_7` / `2015_1회_71` into `근거/계산:`; add `다른 과목 연결:` to the
  2 borderline items (`2016_1회_71` △/Y, `2015_1회_71` 시정수) if wanted.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `solution` / `steps` apply.
- No `answer` / `choices` / `text` modification.
- No app code or schema modification.
- No trim or re-draft applied (recommendations only).
- No local server run.
- No paid API call.
- No commit; no push.

## Status

- Expansion dry-run review complete: 18 items checked on format, mapping,
  OCR flags, content risk, and length.
- Format compliant 18/18; answer/mapping correct 18/18; physics re-derived.
- Classification: pass 16 (6 with companion cleanup), needs-trim 1
  (`2016_1회_44`), needs-source-check 1 (`2001_3회_43`), hold 0.
- The 6 OCR flags do not block the solution/steps apply; a companion
  choices/text cleanup is recommended per pilot precedent.
- Next (separate approval): `2016_1회_44` trim, `2001_3회_43` textbook source
  check + re-draft, the choices/text cleanup decision, then a limited
  pedagogy apply behind the iPad viewport gate.
