# Old Answer — solution_svg Consistency Audit (2026-05-21)

Read-only audit of `solution_svg` consistency for the 28 items touched by the
old-answer tracks: the 9 `source_answer_verified` apply-track items and the
19 C20 single-answer corrected items. The audit checks whether the existing
`solution_svg` conflicts with the current `solution` / `steps` and the
corrected `q.answer`.

This is a **read-only audit document**. It does NOT modify `app/data`,
`solution_svg`, `solution` / `steps`, `answer`, app code, or the schema.

- Base commits: `4fed8a8` (verified apply closeout), `5277967` (C20 closeout),
  `3894a38` (DQ schema probe)
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Method

- Read-only scan only. No rendering, no image generation, no OCR, no API.
- For each item, the `solution_svg` content was read from
  `app/data/questions.json` (string field) or `app/data/questions.v2.json`
  (`solution_svg.svg_content`).
- The SVG `<text>` / `<tspan>` content was extracted and searched for:
  answer-number mentions (`정답` followed by a 1-4 / circled number),
  `N번` patterns, circled numbers ①-④, and stale cleanup-target phrases
  ("정답 없음", "선택지 미제시", "정정 주의", "보기 표시 누락",
  "제시되지 않은", "전항정답", "불완전").
- These `solution_svg` values are vector SVG with real `<text>` elements, so
  text extraction is reliable. The audit is text-extraction-based, not a
  rendered visual audit; an optional browser render check is noted as a
  follow-up.
- Where a verdict could not be reached from the text scan, the item is set to
  `needs_render_check`.

## Verdict definitions

- `ok` — `solution_svg` present and text-consistent with the current
  `solution` / `steps` and corrected `q.answer`; no stale content found.
- `stale_svg` — `solution_svg` contains an old answer number, old conclusion,
  stale formula, stale choice label, or a cleanup-target phrase.
- `no_svg` — the item has no `solution_svg`.
- `needs_render_check` — text scan inconclusive; a rendered visual check is
  required.
- `defer` — held.

## Audit table (28 items)

`solution`/`steps` status is `closed` for all 28 (verified-apply items had
answer-locked regenerated solutions; C20 items had answer + solution closed).

| key | current_answer | route | solution_svg | svg answer mention | svg stale-risk note | verdict |
| --- | ---: | --- | --- | --- | --- | --- |
| `2001_1회_21` | 2 | verified_apply | none | — | — | no_svg |
| `2002_1회_32` | 1 | verified_apply | none | — | — | no_svg |
| `2005_3회_83` | 4 | verified_apply | none | — | — | no_svg |
| `2006_1회_7` | 2 | verified_apply | present | none (derivation diagram; ∇·E=3 is a computed value, not a choice) | no answer label, no stale phrase | ok |
| `2015_1회_13` | 1 | verified_apply | present | none (Poynting-vector derivation) | no answer label, no stale phrase | ok |
| `2015_1회_22` | 1 | verified_apply | none | — | — | no_svg |
| `2015_3회_27` | 3 | verified_apply | none | — | — | no_svg |
| `2016_1회_71` | 3 | verified_apply | present | none (△/Y 결선 비교 diagram; E_l=E_p for △) | no answer label, no stale phrase | ok |
| `2016_3회_44` | 4 | verified_apply | present | none (무부하 시험 회로 diagram) | no answer label, no stale phrase | ok |
| `1998_4회_10` | 4 | c20_corrected | present | none (①② are 경계조건 원칙 enumeration, not choices) | derivation gives B₂=4μ₀ax−8μ₀ay+8μ₀az (= choice 4); no old answer ① | ok |
| `2001_1회_68` | 3 | c20_corrected | none | — | — | no_svg |
| `2001_3회_41` | 4 | c20_corrected | none | — | — | no_svg |
| `2001_3회_43` | 2 | c20_corrected | none | — | — | no_svg |
| `2002_3회_4` | 4 | c20_corrected | present | "∴ 정답: ④번" | SVG states ④ = current answer 4 — consistent | ok |
| `2006_1회_6` | 3 | c20_corrected | present | none (STEP 4 shows Q[cal]=0.24×V²Ct/(ρε)) | SVG uses 0.24 (correct), NOT the old erroneous 4.2; consistent with corrected answer 3 | ok |
| `2006_2회_27` | 4 | c20_corrected | none | — | — | no_svg |
| `2007_1회_9` | 2 | c20_corrected | present | none ("∴ a=-1/3" = choice 2 value) | no answer label, no stale phrase | ok |
| `2007_2회_64` | 1 | c20_corrected | present | none (Hurwitz D₁-D₄ all positive → 안정 = choice 1) | ①-④ are D₁-D₄ step labels, not choices; no stale phrase | ok |
| `2015_1회_71` | 1 | c20_corrected | present | none ("τ=1[sec]" = choice 1 value) | no answer label, no stale phrase | ok |
| `2015_1회_87` | 2 | c20_corrected | none | — | — | no_svg |
| `2015_2회_23` | 4 | c20_corrected | present | none (π형 등가회로 diagram only) | no answer label, no formula conclusion, no stale phrase | ok |
| `2015_2회_29` | 2 | c20_corrected | none | — | — | no_svg |
| `2015_3회_22` | 1 | c20_corrected | present | none (△ 결선 3고조파 제거 원리; "→ 고조파 제거 ✓") | △결선 = choice 1; no answer label, no stale phrase | ok |
| `2015_3회_25` | 4 | c20_corrected | none | — | — | no_svg |
| `2016_1회_44` | 4 | c20_corrected | none | — | — | no_svg |
| `2016_1회_69` | 4 | c20_corrected | present | "✗ 안정도 척도 아님 (정답)" on 고유주파수 | 고유주파수 = choice 4 = current answer — consistent | ok |
| `2016_1회_70` | 4 | c20_corrected | none | — | — | no_svg |
| `2016_3회_21` | 4 | c20_corrected | none | — | — | no_svg |

## Summary tally

| verdict | count |
| --- | ---: |
| `ok` | 13 |
| `stale_svg` | 0 |
| `no_svg` | 15 |
| `needs_render_check` | 0 |
| `defer` | 0 |
| total | 28 |

- 13 items have a `solution_svg`; all 13 are text-consistent with the current
  `solution` / `steps` and corrected `q.answer`. No stale answer number, old
  conclusion, stale formula, stale choice label, or cleanup-target phrase was
  found in any of them.
- The 2 SVGs that explicitly state an answer (`2002_3회_4` → ④,
  `2016_1회_69` → 고유주파수) both match the corrected `q.answer`.
- 15 items have no `solution_svg`.

Note: the conflict items were C1 `conclusion_mismatch` — the `solution` body
(and the `solution_svg` derivation, where present) already reflected the
source-correct reasoning; only the stored `q.answer` was wrong. The audit
confirms the `solution_svg` content did not carry the old stored answer.

## Follow-up routes

- `stale_svg` → SVG cleanup / rebuild track. **0 items — no action.**
- `no_svg` (15 items) → no action unless the app requires an SVG. The app
  renders questions without `solution_svg` (only 1900/5331 records have one),
  so no action is required.
- `needs_render_check` → browser / render audit. **0 items.**
- `ok` (13 items) → closed.

Optional: a rendered visual audit of the 13 `ok` SVGs could be run as a
separate browser-based check if a visual (not text-level) confirmation is
desired. The text-extraction audit found no inconsistency, so this is
optional, not required.

## Status

- `solution_svg` consistency audit complete for all 28 old-answer-track items.
- No `stale_svg` found; no SVG cleanup/rebuild track is opened.
- Q2 bulk apply remains BLOCKED.
- DQ-1 items (`2014_2회_50`, `2014_3회_62`) remain `defer` (not in this
  audit scope; their `q.answer` is unresolved pending the DQ migration).

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `solution_svg` modification.
- No `solution` / `steps` modification.
- No `answer` modification.
- No app code or schema modification.
- No rendering, OCR, or paid API call.
- No push.
