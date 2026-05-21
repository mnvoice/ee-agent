# Answer-Selection Pedagogy Pilot — Review (2026-05-21)

Read-only review of the 7 applied pedagogy pilot items. It assesses whether
the new `solution` / `steps` work as a "reason-toward-the-answer" solution —
on correctness, readability, UI load, and choice-judgment quality.

This is a **read-only review document**. It does NOT modify `app/data` and
does NOT start the expansion batch.

- Base commit: `2aadbe5` (data/docs: apply answer selection pedagogy pilot)
- Pilot apply: `docs/audit/answer_selection_pedagogy_pilot_apply_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Method

- Read-only inspection of the current `app/data` `solution` / `steps`.
- Text-level review first (this document). A browser render check is
  recommended as a follow-up (see Expansion recommendation).
- No modification.

## Length context

Corpus `solution` length: median 306, mean 335 chars (n=5331). The 7 pilot
solutions are 512-678 chars — roughly 2× the corpus median. This is an
inherent cost of the 8-element structure and is recorded as a UI/readability
observation (not a defect).

## Per-item review

### `2007_1회_9` — 전기자기학, answer 2

- solution length / density: 512 chars (shortest of the 7); 8 elements;
  steps 112 chars. Compact.
- choice-explanation quality: high — each of [1]-[4] is tested by
  substituting its `a` value into 1+3a. Directly teaches elimination.
- answer-selection usefulness: high — the learner sees exactly why only [2]
  gives 0.
- cross-subject connection quality: adequate — 직교성(orthogonality) link is
  brief and genuine.
- trap/hint usefulness: useful — the j-component sign trap is a real
  beginner error.
- UI/readability risk: low — shortest pilot solution.
- correctness risk: low — verified.
- verdict: `keep`.

### `2007_2회_64` — 회로이론, answer 1

- solution length / density: 628 chars; 8 elements; steps 131 chars.
- choice-explanation quality: high — [2]/[3]/[4] each explained by what
  condition they would require.
- answer-selection usefulness: high.
- cross-subject connection quality: strong — Routh-Hurwitz 회로↔제어 is a
  genuine, exam-relevant identity.
- trap/hint usefulness: high — the 필요조건 vs 충분조건 trap is a key
  Hurwitz misconception.
- UI/readability risk: low-medium.
- correctness risk: low — verified.
- verdict: `keep`.

### `2001_3회_41` — 전기기기, answer 4

- solution length / density: 678 chars (longest of the 7); 8 elements;
  steps 190 chars.
- choice-explanation quality: high — each of [1]-[4] judged 옳음/틀림.
- answer-selection usefulness: high — the "find what is load-independent"
  framing is a strong selection heuristic.
- cross-subject connection quality: adequate — 전력공학 효율 link is genuine.
- trap/hint usefulness: high — the "모든 손실 증가" lumping trap is the
  exact reason this item is missed.
- UI/readability risk: medium — longest solution; near the upper length
  bound.
- correctness risk: low — verified.
- verdict: `keep` (flagged as the length upper bound — see template notes).

### `2006_2회_27` — 전력공학, answer 4

- solution length / density: 522 chars; 7 elements (다른 과목 연결 omitted);
  steps 175 chars.
- choice-explanation quality: high — each device ([1] 낙차/[2] 방수로/[3]
  침사지/[4] 제수문) is distinguished by function.
- answer-selection usefulness: high — pure elimination teaching; good model
  for 암기형 items.
- cross-subject connection quality: n/a — element correctly omitted (no
  genuine link). This validates the 7-element variant.
- trap/hint usefulness: useful — the "confuse the surrounding facilities"
  trap is real.
- UI/readability risk: low.
- correctness risk: low — verified.
- verdict: `keep`.

### `2016_1회_70` — 제어공학, answer 4

- solution length / density: 636 chars; 8 elements; steps 170 chars.
- choice-explanation quality: high — [1]-[4] each checked on gain and phase.
- answer-selection usefulness: high.
- cross-subject connection quality: strong — Nyquist↔Bode is the same
  control-theory topic; the link is genuine.
- trap/hint usefulness: useful — the |−1| sign trap and ±90° confusion.
- UI/readability risk: low-medium.
- correctness risk: low — verified.
- verdict: `keep`.

### `2016_3회_21` — 전력공학, answer 4

- solution length / density: 638 chars; 8 elements; steps 153 chars.
- choice-explanation quality: high — all four choices addressed, including
  why [1]/[2] (전류 기준) are off-target.
- answer-selection usefulness: high — the derivation chain is the teaching
  point.
- cross-subject connection quality: adequate — high-voltage transmission
  economics link is genuine.
- trap/hint usefulness: high — the "A∝I² misread as A∝I" trap is the exact
  failure mode (this item's old steps had literally that error).
- UI/readability risk: low-medium. Minor: 핵심 개념 and 정식 근거 restate
  the same I∝1/V / R∝V² / A∝1/V² chain — slight redundancy (template note).
- correctness risk: low — verified; the apply also fixed the dry-run typo
  (`A=ρl/A` → `A=ρl/R`).
- verdict: `keep`.

### `2015_3회_22` — 전력공학, answer 1

- solution length / density: 654 chars; 8 elements; steps 181 chars.
- choice-explanation quality: high — each of [1]-[4] explained by function.
- answer-selection usefulness: high — the "3고조파=△, 5고조파=직렬리액터"
  pairing is a strong exam heuristic.
- cross-subject connection quality: adequate — 전기기기 Y/△ harmonic link
  is genuine.
- trap/hint usefulness: high — the "직렬 리액터=고조파 제거" overgeneral
  trap is real.
- UI/readability risk: low-medium.
- correctness risk: low — verified.
- verdict: `keep`.

## Aggregate

| verdict | count |
| --- | ---: |
| `keep` | 7 |
| `needs_shortening` | 0 |
| `needs_wording_cleanup` | 0 |
| `needs_logic_fix` | 0 |
| `defer` | 0 |

All 7 items work as answer-selection solutions: correct, with per-choice
elimination, traps, and (where genuine) cross-subject links. No item needs a
logic fix; none needs a wording cleanup. The only systemic observation is
length (see below).

## Template refinement proposals

Observations for the template, ahead of expansion:

- **Keep**: the per-choice 보기 판단 / 오답 제거 element, the 흔한 함정
  element, the 시험장 빠른 판별법 element, and the 최종 정답 element. These
  are the core of "reason toward the answer" and were consistently strong.
- **Keep, conditionally**: the 다른 과목 연결 element — valuable when a
  genuine link exists (`2007_2회_64`, `2016_1회_70`, `2015_3회_22`), correctly
  omitted when not (`2006_2회_27`). The 7-element variant is a valid form.
- **Possible over-element**: for derivation items (`2007_1회_9`,
  `2007_2회_64`, `2016_1회_70`, `2016_3회_21`) the 핵심 개념 and 정식 근거
  elements partly restate the same relations. Template refinement: for
  derivation items, keep 핵심 개념 to one line and let 정식 근거 carry the
  formula, to cut the ~2× length.
- **solution ↔ steps overlap**: the `steps` (`인식`/`변환`/`계산`) now
  partly duplicates the solution's 단서 / 정식 근거 / 계산 elements. A
  template decision is needed: keep `steps` as a terse skeleton (current
  state — 112-190 chars, acceptable) or fold it into the solution. Recommend
  keeping `steps` terse for now and revisiting after the browser check.
- **Subject adjustment**: 암기형 items (`2006_2회_27`) lean on
  elimination + traps and need no derivation; 계산형 items lean on 정식
  근거; both fit the structure. No subject needs a different element set —
  only the per-item emphasis shifts.

## Expansion recommendation

`expand_after_cleanup`

The pilot is correct and pedagogically sound (7/7 `keep`), so the approach is
validated. But two refinements should land first: (1) trim the
핵심 개념 / 정식 근거 overlap for derivation items to reduce the ~2× length,
and (2) a browser render check to confirm the UI load of a 500-680-char
structured solution is acceptable. After those, a 20-item batch can proceed
under the usual dry-run → review → limited apply → closeout rhythm. No bulk
apply.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `solution` / `steps` modification.
- No `answer` / `choices` modification.
- No app code or schema modification.
- No expansion batch started.
- No paid API call.
- No push.

## Status

- Pilot review complete: 7/7 `keep`. The pedagogy approach is validated.
- Recommendation: `expand_after_cleanup` — a template trim + a browser check
  before the expansion batch.
