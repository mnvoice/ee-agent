# Answer-Selection Pedagogy — Template v2.1 (Plain-Text Labels) (2026-05-21)

Template refinement v2.1. The iPad-viewport readability check found that the
app's solution renderer does not parse markdown, so the `**bold**` headers
used by v1/v2 render literally. v2.1 switches to plain-text labels so the
expansion batch does not depend on markdown rendering.

This is a **template refinement document only**. It does NOT modify
`app/data`, app code, or any `solution` / `steps`.

- Base commits: `38ff584` (template v2), `f28dc09` (iPad-viewport fallback
  check)
- Template v2: `docs/audit/answer_selection_pedagogy_template_refinement_2026-05-21.md`
- iPad check: `docs/audit/answer_selection_pedagogy_ipad_viewport_readability_check_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## 1. Problem

- The app's solution renderer (`js/render.js`, `js/main.js`) renders
  `solution` via `escapeHtml()` into a `white-space: pre-wrap` div. It does
  NOT parse markdown — no `marked` / markdown library is loaded.
- A `**핵심 단서**`-style header therefore renders with literal `**`
  asterisks around the label.
- This is corpus-wide, pre-existing behavior — the existing 5331-item corpus
  also uses `**` and renders it literally. The pilot 7 are structurally OK
  and consistent with the corpus; this is NOT a pilot regression.
- But for the pedagogy goal (readability), the literal `**` markers are a
  minor visual detractor, and there is no reason for the expansion batch to
  keep depending on a markdown feature the app does not have.

## 2. Decision

- The app-level Markdown renderer change is NOT made now. Reasons: the `**`
  literal rendering is whole-app behavior and not a pilot regression; adding
  a markdown renderer would change the display of all 5331 solutions and is
  a separate frontend track; the current goal is the safe expansion of the
  pedagogy solutions.
- From the expansion batch onward, the pedagogy template does NOT depend on
  markdown-bold. It uses plain-text labels.

## 3. v2.1 template — plain-text labels

Each element is a plain-text label followed by a colon, then the content.
No `**`. The `pre-wrap` renderer shows the label as plain text, and a blank
line separates elements — which is exactly how the structure should read.

Required elements (every item), in order:

1. `핵심 단서:` — the concept being tested and the textual clue in the stem,
   in one short paragraph (the v2 merged element — carries no formula).
2. `보기 판단:` — per-choice judgment; why each wrong choice is wrong, why
   the answer is right. Must map to the actual stored `choices`.
3. `근거/계산:` — the derivation / computation, or the rule it rests on.
   Carries the formula once (the `핵심 단서:` element does not restate it).
4. `함정:` — the common trap (plausible-but-wrong reasoning).
5. `시험장 판별:` — how to discriminate quickly under exam time pressure.
6. `정답:` — the final line; the answer stated explicitly, matching
   `q.answer`.

Conditional element:

- `다른 과목 연결:` — included only when a genuine, exam-relevant
  cross-subject link exists; placed before `정답:`. Omitted otherwise.

Concept/memory items may also carry a short concept explanation folded into
`핵심 단서:` (no separate element); derivation items do not.

### Format rules

- Label format: `라벨:` then a space then content; elements separated by one
  blank line. Example block:
  ```
  핵심 단서: 두 벡터가 수직이면 내적이 0이다. "수직"이 단서.

  보기 판단: [1] … [2] … [3] … [4] …
  ```
- `정답:` is the last line of the solution.
- `steps` keeps the `인식` / `변환` / `계산` dict (rendered by the app's
  step-block UI with its own labels — no change needed there).

## 4. Prohibited (until the UI renderer changes)

- No `**bold**` headers.
- No markdown tables.
- No markdown headings (`#`, `##`, …).
- No reliance on any markdown feature — the app renderer does not parse it.
- (LaTeX `\(...\)` / `\[...\]` is still rendered by KaTeX and remains
  allowed where a formula genuinely needs it — but the pilot showed plain
  Unicode (`∝`, `²`, `∠`) is usually enough and lower-risk.)

## 5. Pilot 7 items

- The pilot 7 (`2007_1회_9`, `2007_2회_64`, `2001_3회_41`, `2006_2회_27`,
  `2016_1회_70`, `2016_3회_21`, `2015_3회_22`) are NOT rewritten now. They
  stay as applied (`2aadbe5`) — structurally OK and corpus-consistent.
- The expansion batch uses v2.1 from its first dry-run.
- A pilot-7 rewrite to v2.1 (to drop their literal `**`) is possible later
  but requires separate approval; it is a cosmetic alignment, not a
  correctness fix, so it is low priority.

## 6. Expansion conditions

- The next expansion dry-run uses the v2.1 plain-text-label template.
- `solution` body target length: 350-500 chars (the v2 guideline holds; the
  plain-text labels are slightly shorter than `**…**` headers, which helps).
- `steps` length: 100-180 chars.
- The expansion still follows dry-run → review → limited apply → closeout,
  with no bulk apply, and remains held until the actual iPad / browser
  viewport spot check noted in `f28dc09`.

## 7. Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No app code modification (no markdown renderer added).
- No `solution` / `steps` modification.
- No pilot-7 rewrite.
- No expansion batch started.
- No paid API call.
- No push.

## 8. Status

- Template v2.1 fixed: plain-text labels (`핵심 단서:` / `보기 판단:` /
  `근거/계산:` / `함정:` / `시험장 판별:` / `다른 과목 연결:` / `정답:`),
  no markdown dependency.
- Pilot 7 unchanged. Expansion uses v2.1, still held pending the viewport
  spot check.
