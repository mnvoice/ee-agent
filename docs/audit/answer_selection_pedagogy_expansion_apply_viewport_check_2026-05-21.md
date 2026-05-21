# Answer-Selection Pedagogy — Expansion Post-apply Viewport Check (2026-05-21)

Post-apply viewport / readability check for the limited apply of the 10
`apply-ready` pedagogy items. It assesses the applied `solution` / `steps`
for iPad-viewport readability.

The intended check was a live desktop-browser iPad-viewport render. That
could not run here (see Limitations), so this is a **structural fallback
assessment** — based on the app's render code, CSS, and the now-applied
`solution`/`steps` text — not a live render. Same constraint as the prior
pilot iPad check (`answer_selection_pedagogy_ipad_viewport_readability_check_2026-05-21.md`).

This is a **read-only check document**. It does NOT modify `app/data`.

- Base: limited apply verified at
  `docs/audit/answer_selection_pedagogy_expansion_apply_verification_2026-05-21.md`
- App render code: `app/js/render.js`, CSS `app/css/style.css`

## Limitations

- `gstack`/`browse` (the headless-browser tooling) requires the `bun`
  runtime; `bun` is not installed (`which bun` → not found). No new runtime
  was installed.
- The app (`app/index.html`) has no hash/query routing to a specific
  question (`grep` for `location.hash` / `URLSearchParams` / `#q=` → none),
  so a one-shot headless screenshot cannot deep-link to a question's
  solution. The app renders questions dynamically via IndexedDB.
- No browser-automation tool is available in this step. Therefore an actual
  iPad / desktop-browser viewport render was NOT performed.
- This assessment is structural: it reads the render code, the CSS, and the
  applied `solution`/`steps`, and reasons about iPad-viewport behavior. It
  cannot confirm the pixel-accurate rendered scroll length.

## App render facts (from source, re-confirmed post-apply)

- `solution` is rendered as `escapeHtml(solution)` into
  `<div class="solution-text">` (`render.js:175-176`). `escapeHtml` escapes
  `& < > "` only.
- `steps[key]` is inserted **raw** (not escaped) into
  `<div class="step-content">` (`render.js:170`).
- `.solution-text` / `.step-content` CSS: `font-size: 0.95rem` (≈15.2px),
  `line-height: 1.7` (≈25.8px line box), `white-space: pre-wrap`
  (`style.css:597-611`).
- `.solution-body` padding `14px 16px`; `.step-block` margin-bottom 16px.
- Markdown is NOT processed (no `marked` library) — confirmed; the v2.1
  plain-text-label template was chosen precisely for this.

## Checked items (5)

3 longest of the applied 10, plus 2 representative samples (shortest + mid):

| key | solution chars | answer | role |
| --- | ---: | ---: | --- |
| `2006_1회_6` | 511 | 3 | longest applied |
| `2001_1회_68` | 505 | 3 | long |
| `2016_1회_69` | 501 | 4 | long |
| `2016_3회_44` | 409 | 4 | representative (shortest applied) |
| `2015_3회_25` | 468 | 4 | representative (mid) |

## Findings

### v2.1 plain-text label readability

All 5 `solution` drafts use the v2.1 plain-text labels (`핵심 단서:` /
`보기 판단:` / `근거/계산:` / `함정:` / `시험장 판별:` / `정답:`), 6 elements
each. Under `escapeHtml` + `pre-wrap`:

- The labels render as literal plain text — no markdown dependency, and no
  literal `**` artifact (v2.1 removed markdown bold; that was the pilot's
  Finding A). Readability: clean.
- The `\n\n` element separators are preserved by `pre-wrap`, so each
  solution renders as 6 labelled blocks with a blank line between — exactly
  the intended scannable structure.

### `정답:` last-line display

All 5 (and all 10 applied) have `정답:` as the last line of the `solution`
string (verified in the apply verification, 10/10). Under `pre-wrap` it
renders as the final line of the `.solution-text` block — the answer is the
last thing shown, as intended.

### 보기 판단 block / scroll burden (structural estimate)

Estimate assumptions: iPad-portrait content column ≈780px usable (viewport
~820px − `.solution-body` padding), ≈44 Korean-equivalent chars/line at
0.95rem, line box ≈25.8px.

| key | solution chars | elements | longest element | est. wrapped lines | est. `.solution-text` height |
| --- | ---: | ---: | ---: | ---: | ---: |
| `2006_1회_6` | 511 | 6 | 172 | ~17 | ~440px |
| `2001_1회_68` | 505 | 6 | 186 | ~17 | ~440px |
| `2016_1회_69` | 501 | 6 | 205 | ~17 | ~440px |
| `2016_3회_44` | 409 | 6 | 164 | ~17 | ~440px |
| `2015_3회_25` | 468 | 6 | 167 | ~18 | ~465px |

- The `.solution-text` block renders to ≈440-465px — roughly 0.37-0.39 of an
  iPad-portrait viewport (~1180px). The 6-element block count drives height
  more than the char count at this size, so the 409-511 char spread lands in
  a narrow ≈17-18 line band.
- The `보기 판단` element is the longest per item (164-205 chars → ≈4-5
  wrapped lines). It is scannable as a single labelled block.
- These solutions are **shorter than the pilot's applied range** (512-678,
  `2aadbe5`), which the pilot review judged `structurally_ok` 7/7. Scroll
  burden here is therefore ≤ the pilot's. The `steps` (인식/변환/계산, ≈24-55
  chars each) add ≈3 short step-blocks above the solution-text.
- Scroll-burden verdict: **low-medium**, same band as the pilot's accepted
  items.

### choices / text ↔ solution mapping

All 5 items' stored `choices` were read post-apply — all clean, no OCR
residue or LaTeX corruption (the `apply-ready` group had no OCR flags by
design; the 6 OCR-flagged items are all in the deferred `cleanup-dependency`
group and were NOT applied). Each solution's `보기 판단` references `[1]`-`[4]`
matching the actual stored choices:

- `2006_1회_6` — choices are 4 clean LaTeX formulas; `보기 판단` distinguishes
  them by the 4.2/0.24 coefficient and the V/V² power. No conflict.
- `2001_1회_68` — choices 위치/속도/가속도/평면 오차 상수; `보기 판단` maps
  s⁰/s¹/s² and flags [4] as a non-existent term. No conflict.
- `2016_1회_69` — choices 공진치/위상여유/이득여유/고유주파수; all mapped.
  No conflict.
- `2016_3회_44` — choices 유도/단락/부하/무부하시험; all mapped. No conflict.
- `2015_3회_25` — choices [1]-[4] (recovered clean at `fac4b8d`); `보기 판단`
  maps 반한시/순한시/정한시/결합. No conflict.

No `<` / `>` appears in any of the 5 solutions or steps, so the raw-inserted
`steps` and the escaped `solution` both render without HTML breakage.

### iPad readability risk

Low-medium for all 5 — the same band as the pilot's `structurally_ok`
verdict, and these are shorter than the pilot. No per-item readability
defect found.

## Residual (needs a live device render)

Unchanged from the prior pilot iPad check, two things a structural pass
cannot close:

- the pixel-accurate rendered scroll length;
- the choice cross-reference friction — while reading `보기 판단` on iPad, the
  numbered choice buttons sit above and scroll off-screen, so a learner may
  scroll up to cross-check `[1]`-`[4]`.

Both are best confirmed by opening `app/index.html` on a real iPad (or
desktop Chrome at iPad viewport) — trivial for the supervisor on the local
machine (Chrome is installed). This structural gate does not block; it
reports low-medium risk with no per-item defect.

## Verdict

- Structural viewport gate: **PASS** (low-medium readability risk, no
  per-item defect). The v2.1 plain-text labels render cleanly, `정답:` shows
  as the last line, the 6-element solutions are ≈440-465px tall (shorter
  than the accepted pilot), and choices↔solution mapping is conflict-free
  for all applied items.
- A live iPad/desktop-viewport render remains an optional confirmation step
  for the scroll-burden and cross-reference points above.

## Not done in this step

- No `app/data` modification.
- No `solution_source` / `steps_source` modification.
- No `cleanup-dependency` (7) apply.
- No live iPad / browser viewport render; no local server run.
- No commit; no push.

## Status

- Post-apply viewport check complete (structural fallback): 5 items checked
  (3 longest + 2 representative), gate PASS, iPad readability risk
  low-medium, no per-item defect.
- Pending separate decision: the `solution_source` / `steps_source`
  provenance-metadata update for the 10 applied records (raised in the apply
  verification report). This viewport check does not modify them.
- Next (separate approval): the `solution_source`/`steps_source` decision;
  commit/push; the `cleanup-dependency` batch (7); the `2001_3회_43` source
  check; an optional live device render.
