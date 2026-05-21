# Answer-Selection Pedagogy — Template Refinement (v2) (2026-05-21)

Template refinement for the answer-selection pedagogy track. The pilot review
found the approach validated (7/7 `keep`) but flagged length and element
overlap. This document fixes the v2 template for the expansion batch.

This is a **design/refinement document only**. It does NOT modify `app/data`
and does NOT start the expansion batch.

- Base commits: `0ff1f31` (pedagogy track design), `2aadbe5` (pilot apply),
  `1316bca` (pilot review)
- Pilot review: `docs/audit/answer_selection_pedagogy_pilot_review_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## 1. Pilot review summary

- 7/7 `keep` — the answer-selection approach is validated; no item needed a
  logic fix or a wording cleanup.
- `solution` length 512-678 chars — roughly 2× the corpus median (306).
- UI / readability risk: medium (longer than typical; structured headers
  mitigate but mobile scroll is longer).
- For derivation items, 핵심 개념 and 정식 근거 partly restate the same
  relations — redundancy.
- `solution` and `steps` partly overlap (steps' 인식/변환/계산 ≈ solution's
  단서 / 근거 / 계산).

## 2. Refined template v2

### Required elements (every item)

1. **핵심 단서** — the concept being tested AND the textual clue in the
   stem, stated together in one short paragraph. (v1's separate 핵심 개념 +
   문제에서 봐야 할 단서 are merged; for derivation items this also absorbs
   the v1 핵심 개념 to remove the 핵심 개념 / 정식 근거 overlap.)
2. **보기 판단 / 오답 제거** — per-choice: why each wrong choice is wrong,
   why the answer is right. Must map to the actual stored `choices`.
3. **근거 또는 계산** — the derivation / computation, or the rule it rests
   on. Carries the formula (the 핵심 단서 element does NOT restate it).
4. **함정** — the common trap (plausible-but-wrong reasoning).
5. **시험장 판별법** — how to discriminate quickly under exam time pressure.
6. **최종 정답** — the answer, stated explicitly, matching `q.answer`.

### Conditional elements

- **다른 과목 연결** — included only when a genuine, exam-relevant
  cross-subject link exists; omitted otherwise (validated by `2006_2회_27`
  in the pilot).
- **확장 개념 설명** — a longer concept explanation, only for memory /
  concept items (암기형 / 개념형) where the concept itself is the content.
  Not used for derivation items (the derivation is the content there).

### Element count

- Derivation items: 6 required (no separate 핵심 개념 / 확장 개념 설명).
- Memory / concept items: 6 required + 확장 개념 설명 if the concept needs
  it.
- 다른 과목 연결 added only when genuine.
- Net: typically 6-7 elements (v1 was 7-8) — one element fewer, plus the
  merged 핵심 단서 removes the derivation-item redundancy.

## 3. Per-question-type templates

### 계산 / 도출형 (calculation / derivation)

- 핵심 단서: concept + clue in one short paragraph.
- 보기 판단 / 오답 제거: substitute / test each choice.
- 근거 또는 계산: the derivation, carrying the formula once.
- 함정 / 시험장 판별법 / 최종 정답.
- 다른 과목 연결: if genuine.
- No 확장 개념 설명.
- Pilot examples: `2007_1회_9`, `2007_2회_64`, `2016_1회_70`, `2016_3회_21`.

### 개념 / 암기형 (concept / memory)

- 핵심 단서: concept + clue.
- 확장 개념 설명: a few lines, if the concept needs unpacking.
- 보기 판단 / 오답 제거: per-choice function/property.
- 함정 / 시험장 판별법 / 최종 정답.
- 다른 과목 연결: if genuine.
- No 근거 또는 계산 derivation (replace with the rule statement).
- Pilot examples: `2001_3회_41`, `2015_3회_22`.

### 보기 비교형 (choice-comparison)

- A variant of 개념/암기형 where the whole task is distinguishing the
  choices. 보기 판단 / 오답 제거 is the largest element; 확장 개념 설명 is
  usually unnecessary; 다른 과목 연결 usually omitted.
- Pilot example: `2006_2회_27`.

### 교차과목 연결형 (cross-subject)

- Not a separate element set — any of the above types becomes this when the
  다른 과목 연결 element is genuinely strong. The element is then written
  with one concrete sentence, not a vague gesture.
- Pilot examples: `2007_2회_64` (회로↔제어), `2016_1회_70` (Nyquist↔Bode),
  `2015_3회_22` (전력↔기기).

### 법규 / 수치형 (statute / numeric)

- Handled by a conservative template, or excluded from the pedagogy batch.
- Statute: NO article-number fabrication — cite an article only if it is
  already in the verified source; otherwise state the rule without a number.
- Numeric: the 근거 또는 계산 element must show the derivation; no invented
  constants.
- The pilot deliberately excluded 전기설비기술기준 items; the expansion
  batch keeps statute items low priority pending this conservative template.

## 4. Target length guideline

- `solution` body: target 350-500 chars.
- complex derivation items: up to 600 chars maximum.
- `steps` (`인식`/`변환`/`계산`): keep 100-180 chars (terse skeleton).

The merged 핵심 단서 element and the removal of the derivation-item
redundancy are expected to bring most items into the 350-500 range; the
pilot's 512-678 is the v1 baseline to improve on.

## 5. Apply rule

- The 7 pilot items are NOT rewritten immediately. They stay as applied
  (`2aadbe5`).
- The v2 template applies from the next expansion dry-run onward.
- Whether to rewrite the 7 pilot items to v2 is decided AFTER the
  browser / readability check (Section 6) — if the check shows the v1 length
  is a real UI problem, the pilot 7 get a v2 rewrite; if acceptable, they
  stay as-is.

## 6. Browser / readability check (proposed follow-up)

A separate follow-up step, not done here:

- Open the 7 pilot items in the app and inspect the rendered `solution` /
  `steps`.
- Check on mobile and desktop: scroll length, the `**`-header structure,
  KaTeX / markdown rendering of formulas, and that the per-choice judgment
  visually maps to the displayed choices.
- The result feeds the Section 5 decision (rewrite the pilot 7 to v2, or
  keep) and confirms the Section 4 length guideline.

## 7. Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `solution` / `steps` modification.
- No `answer` / `choices` modification.
- No app code or schema modification.
- No expansion batch started.
- No browser check performed (proposed as a follow-up).
- No paid API call.
- No push.

## 8. Status

- v2 template fixed: 6 required elements (merged 핵심 단서), 2 conditional
  elements, per-question-type variants, target length 350-500 chars.
- Next: the browser / readability check, then a 20-item expansion dry-run
  under the v2 template — dry-run → review → limited apply → closeout, no
  bulk apply.
