# Answer Mismatch / Old Solution Quality Track

Date: 2026-05-21
Branch: `feat/phase-b-migration`

## Context

G5 is closed and the figure-dependent hold track is resolved. The next large track is no
longer "fix answers"; it is "find old or weak explanations whose conclusion, evidence, or
rendered learning value is unsafe."

Current source of truth:

- `q.answer` remains the answer SoT.
- Answer-locked regeneration must explain the fixed answer, not choose an answer.
- Figure-dependent items must not be regenerated without original figure evidence.
- G2 remains a smell test, not expert answer verification.

## Baseline Snapshot

Read-only scan of `app/data/questions.v2.json` after `48a36b9`:

| Metric | Count | Meaning |
| --- | ---: | --- |
| Total entries | 5,331 | Full app dataset |
| `tool_name=null` old synthesized solutions | 4,563 | Main old-solution quality surface |
| Missing solution metadata / empty solution | 693 | Separate empty-solution track |
| Answer-locked T3.5 solutions | 74 | G5 closed/pass set |
| H2 local-crop answer-locked solution | 1 | `2025_3회_79` |
| Regex-detected explicit answer mentions | 1,225 | Candidate pool for conclusion checks |
| Explicit answer mention mismatches | 190 | High-priority review candidates |
| Placeholder-like solution text | 261 | High-priority review candidates |
| PUA characters in solution | 204 | Rendering/content-risk candidates |
| `figure_svg` / `stem_figure` present | 340 | Needs figure-aware routing |

These are triage signals, not final defect counts.

## Track Goal

Build a repeatable quality pipeline for old explanations:

1. Find deterministic high-risk candidates.
2. Split them into repairable, figure-dependent, source-answer-needed, and defer groups.
3. Regenerate only repairable candidates with answer-locking.
4. Verify with the same data/render gates that closed G5.
5. Keep paid API use as a later budget decision, not the default path.

## Non-Goals

- Do not re-open the 74 G5-closed answer-locked items unless regression evidence appears.
- Do not treat every regex mismatch as a wrong answer.
- Do not bulk overwrite old solutions without candidate classification and drift checks.
- Do not use generated `figure_svg` or `solution_svg` as source evidence.
- Do not commit `data/pdf_pages/index.json` or broad page-image artifacts as part of this track.

## Candidate Classes

| Class | Signal | Default Action |
| --- | --- | --- |
| C1 conclusion mismatch | Solution says `정답: N번` where `N != q.answer` | High-priority answer-locked regen candidate |
| C2 placeholder / non-substantive | "정보 부족", "분석 불가", "재제출", TODO-like text | Regen or empty-solution track |
| C3 empty solution / empty steps | `solution` or `steps` empty | Separate fill track; answer-lock required |
| C4 PUA / corrupted glyphs | PUA chars or obvious OCR residue in solution | OCR/source review before regen |
| C5 figure-dependent | Text or asset requires original diagram/crop | Hold until source crop exists |
| C6 law/regulation specificity risk | Invented law article or unsupported KEC number | Human/source review, then regen |
| C7 already verified | `tool_name` starts with `answer-locked-regen-T3.5` | Exclude by default |

## Proposed Pipeline

### Phase Q0: Inventory

Read-only scripts only.

- Generate a stable candidate manifest keyed by `year/session/q_no`.
- Record trigger classes and current hashes for `solution` and `steps`.
- Exclude verified answer-locked items by metadata.
- Keep output under `app/reports/` or `output/`; commit only the design or a reviewed manifest.

Exit criteria:

- Candidate manifest is reproducible.
- Counts reconcile with `verify_questions_quality.py`.
- No app/data mutation.

### Phase Q1: Deterministic Triage

Rank candidates:

1. Explicit answer mention mismatch.
2. Placeholder/non-substantive solution.
3. Empty solution or steps.
4. PUA/corrupted solution.
5. Figure-dependent or source-evidence-dependent cases.

For each candidate, assign one route:

- `regen_text_only`: enough text/choices/answer to rewrite without paid API.
- `needs_source_answer_check`: answer SoT confidence is insufficient.
- `needs_source_crop`: figure/circuit/graph/table is required.
- `defer_policy`: answer sentinel or domain decision needed.

Exit criteria:

- First batch is small, preferably 20 to 50 items.
- No `needs_source_crop` item enters text-only regeneration.

### Phase Q2: Answer-Locked Regeneration Batch

Apply only to `regen_text_only`.

Required invariant:

- `q.answer` unchanged.
- Generated conclusion matches `q.answer`.
- `solution_source.tool_name = "answer-locked-regen-old-quality-Q2"`.
- `verified_at` set only after automatic validation passes.

Recommended fields:

- `app/data/questions.json`: `solution`, `steps`.
- `app/data/questions.v2.json`: `solution`, `steps`, `solution_source`, `steps_source`.

Exit criteria:

- Drift check passes before writing.
- Patch scope exactly equals approved candidate set.

### Phase Q3: Validation Gates

Automatic gates:

- JSON parse and Pydantic validation.
- `q.answer` unchanged for every patched item.
- Conclusion-number recheck equals `q.answer`.
- No placeholder-like solution text.
- No U+FFFD.
- No PUA in new solution unless explicitly justified.
- KaTeX/render smoke test for patched items.

Human / reviewer gates:

- G2 smell test sample, category-balanced.
- Extra review for regulations and figure-adjacent items.

Exit criteria:

- Automatic gates 100% pass.
- G2 has 0 FAIL and acceptable suspicious count.

### Phase Q4: Browser Verification

Use the G5 pattern, but scoped to patched items:

- Clean browser state when doing final verdict.
- Open each patched item or representative batches.
- Confirm no stale old solution is being judged.
- Confirm console error 0 and `.katex-error` 0.

Exit criteria:

- Batch marked CLOSED/PASS only after data and browser layers agree.

## Budget Policy

Default is no paid API.

Use paid multimodal API only when all are true:

- Candidate is high-value or high-risk.
- Original source image/crop is required.
- Local crop/source extraction is insufficient for confident reasoning.
- User explicitly approves budget and scope.

This leaves priority 4 as a separate budget decision instead of mixing it into priority 3.

## First Implementation Step

Add a read-only extractor for this track, likely:

`scripts/extract_old_solution_quality_candidates.py`

Minimum output columns:

- `key`
- `year`
- `session`
- `subject`
- `q_no`
- `answer`
- `solution_source.tool_name`
- `triggers`
- `detected_answer_mentions`
- `route`
- `solution_hash`
- `steps_hash`
- `text_preview`
- `solution_preview`

Recommended first report:

`app/reports/old_solution_quality_candidates_<timestamp>.json`

Do not mutate app data in the extractor.

## Open Decisions

- Whether to include `answer=0` sentinel items in this track or keep them separate.
- Whether 2025_2회_60 should remain a future enhancement candidate or enter Q1 as
  `needs_source_crop`.
- Whether to make the first Q2 batch conclusion-mismatch-only, or include placeholders too.
- Whether Web Claude or another independent reviewer should review the first G2 sample.

## Suggested Next Move

Implement the read-only extractor and produce the first manifest. Then choose a small Q2
pilot batch from `C1 conclusion mismatch` candidates, excluding figure-dependent and
source-answer-uncertain items.
