# Answer-Selection Pedagogy Pilot — iPad-Viewport Readability Check (2026-05-21)

Readability check of the 7 applied pedagogy pilot items for use on an iPad
screen. The intended check was a desktop-browser iPad-viewport emulation; that
could not run (see Limitations), so this is a **structural fallback
assessment** — based on the app's render code, CSS, and the measured solution
text — not a live render.

This is a **read-only check document**. It does NOT modify `app/data`.

- Base commits: `2aadbe5` (pilot apply), `1316bca` (pilot review),
  `38ff584` (v2 template refinement)
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Limitations

- `gstack browse` (the headless-browser tool) requires the `bun` runtime;
  `bun` is not installed on this machine.
- No new runtime was installed — by supervisor decision, `bun` is not
  installed and no new tool is added.
- Therefore an actual iPad / desktop-browser viewport render was NOT
  performed. The actual iPad / browser viewport check is deferred to an
  optional later spot check.
- This assessment is structural: it reads the app render code
  (`js/render.js`, `js/main.js`), the CSS (`css/style.css`), and the stored
  `solution` / `steps` text, and reasons about iPad-viewport behavior from
  those facts. It cannot confirm the live rendered scroll length or visual
  layout.

## Check environment (intended vs actual)

- app URL: `http://localhost:8771/index.html` (local static server; started
  and then stopped — no longer running).
- intended: desktop browser with iPad-viewport emulation — iPad portrait
  ~820×1180, iPad landscape ~1180×820.
- actual: not rendered (see Limitations). The local server was stopped.

## App render facts (read-only, from source)

- `solution` is rendered as `escapeHtml(solution)` inside
  `<div class="solution-text">` (`js/render.js:176`, `js/main.js:377`).
- `.solution-text` CSS: `font-size: 0.95rem` (≈15px), `line-height: 1.7`,
  `white-space: pre-wrap` (`css/style.css:605`).
- `.solution-body` padding `14px 16px`; the question view is full-width
  (`max-width: 100%`), so on iPad portrait the content column is roughly
  viewport width minus padding.
- `steps` content is inserted raw (not escaped) into `.step-content`
  (`js/render.js:170`, `js/main.js:373`); `.step-content` CSS matches
  `.solution-text` (0.95rem / 1.7 / pre-wrap).
- KaTeX renders `\(...\)` / `\[...\]` math (`js/render.js`,
  katex 0.16.11). Markdown is NOT processed — there is no `marked` /
  markdown library loaded.

### Finding A — `**bold**` headers render literally

The app does NOT parse markdown. `solution` is HTML-escaped and placed in a
`pre-wrap` div; `**` is not converted to bold. The pilot solutions' eight
`**핵심 단서**`-style headers therefore display with literal `**` asterisks
around each header.

This is **pre-existing, corpus-wide** behavior — the existing 5331-item
corpus solutions also use `**` and render it literally. The pilot 7 are
consistent with the corpus; this is NOT a pilot regression. But for the
pedagogy goal (readability) the literal `**` is a minor visual detractor.
Fixing it would require either an app-level markdown renderer (app-code
change, out of scope) or a header format that renders cleanly under
`escapeHtml` + `pre-wrap`. Surfaced for a supervisor / app-level decision.

### Finding B — no LaTeX in the pilot solution/steps (a plus)

The pilot `solution` and `steps` text contains no `\(...\)` / `\[...\]` /
`$` math — only plain Unicode (`∝`, `²`, `∠`, `√`, `→`, `±`, subscripts).
So there is no KaTeX dependency or KaTeX-failure risk in the pilot
solution/steps bodies. (The question `text` and `choices` may still contain
LaTeX — pre-existing, app-handled.)

### Finding C — steps inserted raw

`steps` content is inserted as raw innerHTML. The pilot steps contain a few
`>` characters (e.g. "Dₖ > 0") but no `<` — a bare `>` renders fine in HTML.
No breakage for the pilot 7. Noted as a latent fragility for future items
(a `<` in a steps string would be unsafe); pre-existing app pattern.

## Per-item check

`white-space: pre-wrap` preserves the solution's `\n\n` element separators,
so each item renders as 7-8 labelled blocks. Estimated rendered height uses
≈0.95rem / line-height 1.7 (≈26px line box) and an iPad-portrait content
column (~780px usable → ≈40-48 Korean chars/line).

| key | solution chars | blocks | longest para | est. iPad-portrait scroll | verdict |
| --- | ---: | ---: | ---: | --- | --- |
| `2007_1회_9` | 512 | 8 | 124 | shortest; ≈1 screen + minor scroll | structurally_ok |
| `2007_2회_64` | 628 | 8 | 191 | ≈1-2 screens | structurally_ok |
| `2001_3회_41` | 678 | 8 | 176 | longest; ≈2 screens | structurally_ok |
| `2006_2회_27` | 522 | 7 | 148 | ≈1 screen + minor scroll | structurally_ok |
| `2016_1회_70` | 636 | 8 | 166 | ≈1-2 screens | structurally_ok |
| `2016_3회_21` | 638 | 8 | 199 | ≈1-2 screens | structurally_ok |
| `2015_3회_22` | 654 | 8 | 181 | ≈1-2 screens | structurally_ok |

Per dimension (all 7):

- length / readability: medium. 512-678 chars, ≈2× the corpus median (306).
  The 8-block structure with labelled headers keeps it scannable; the cost is
  length.
- scroll burden: estimated ≈1-2 iPad-portrait screens for the solution body
  (the question + choices sit above it). Landscape (1180 wide, full-width
  column) wraps fewer lines but the viewport is shorter (820 tall) — net
  scroll is similar. This estimate needs a live render to confirm.
- markdown / KaTeX render: `**` headers show literally (Finding A); no LaTeX
  in the pilot solution/steps so no KaTeX risk (Finding B).
- choice ↔ explanation mapping: the 보기 판단 element references "[1]-[4]";
  the app shows choices as numbered buttons above the solution. The mapping
  is by number, and it works — but on iPad the choices scroll off-screen
  while reading 보기 판단, so the learner may scroll up to cross-reference.
  A real friction point, best confirmed by a live render.
- answer-selection usefulness: high (unchanged from the pilot review
  `1316bca`).

## Aggregate

| verdict | count |
| --- | ---: |
| `structurally_ok` | 7 |
| `needs_v2_rewrite` | 0 |
| `needs_actual_viewport_check` | 0 (see note) |

All 7 are structurally well-formed and render-safe (no KaTeX risk, no HTML
breakage). No item has a per-item defect requiring a v2 rewrite. The two
open questions — the literal `**` rendering and the real scroll burden —
are not per-item issues:

- the `**` rendering is corpus-wide and app-level;
- the scroll-burden judgment genuinely needs a live iPad render.

Both are recorded as deferred / surfaced rather than as a per-item
`needs_actual_viewport_check` verdict.

## Decision proposal

- Keep the pilot 7 items as applied (`2aadbe5`) — no rewrite now. They are
  well-formed, render-safe, and consistent with the corpus.
- The pilot-7 v2-rewrite decision remains deferred — it was to be decided
  after a browser check, and the browser check could not run.
- Surface to the supervisor: the app renders `**` literally for every
  solution (corpus-wide). If clean bold headers are wanted for the pedagogy
  solutions, that is an app-level decision (add a markdown renderer) or a
  header-format change — both outside this pilot's scope.
- Expansion: hold the expansion batch until an actual iPad / browser
  viewport spot check is done (optional, later). The v2 template
  (`38ff584`) should additionally note Finding A — its `**`-header
  assumption renders literally under the current app.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `solution` / `steps` modification.
- No `answer` / `choices` modification.
- No app code or schema modification.
- No `bun` install; no new tool installed.
- No actual iPad / browser viewport render.
- No expansion batch started.
- No paid API call.
- No push.

## Status

- Structural iPad-readability fallback check complete: 7/7
  `structurally_ok`.
- Open: literal `**` rendering (app-level, surfaced); actual iPad viewport
  scroll check (deferred to an optional later spot check).
- Recommendation: keep the pilot 7 as-is; hold the expansion batch until the
  actual viewport spot check.
