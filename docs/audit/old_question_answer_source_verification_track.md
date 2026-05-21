# Old Question Answer Source Verification Track

Date: 2026-05-21
Branch: `feat/phase-b-migration`

Design-only document. No app data is modified by this track's design phase.

## Why this track is needed

The Q2-A dry-run (`docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`) worked
all 30 C1 pilot candidates from standard theory. Result: **22 of 30** had a worked
result that conflicts strongly with the stored `q.answer`, or had OCR-corrupted
choices. Only 8 had a `q.answer` that matches standard theory.

The `q.answer is SoT` policy was established for the **2025-2026** set, where PDF
`[정답]` answer tables were extracted and matched `q.answer` 400/400 (T3.5 G3). That
verification does **not** cover **1998-2016** questions. For old questions, `q.answer`
is an unverified value.

Therefore a C1 `conclusion_mismatch` on an old question is ambiguous: it may mean the
old solution is wrong, OR that `q.answer` itself is wrong. Answer-locked regeneration
cannot proceed on old questions until each `q.answer` is verified against a real
source. This track defines that verification procedure.

Decision reference: `DR-T35-Q2A-ANSWER-SOT-001` (Q2 apply blocked).

## First verification scope

The 30 pilot items listed in `docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`
(C1 conclusion_mismatch ∩ regen_text_only, years 1998-2016). This is the first batch;
the procedure generalizes to other old candidate classes later.

## Routes

Each verified item is assigned exactly one route:

| Route | Meaning |
| --- | --- |
| `source_answer_verified` | A source answer was found and it equals the stored `q.answer`. |
| `source_answer_conflict` | A source answer was found and it differs from `q.answer`. |
| `source_choice_ocr_corrupt` | The stored choices are OCR-corrupted; answer cannot be mapped reliably. |
| `needs_pdf_page_crop` | The source answer or choices require a PDF page image/crop not yet available. |
| `defer` | Source is ambiguous or missing; needs a separate policy/manual decision. |

## Source priority

Verify `q.answer` against sources in this strict order. A lower-priority source is
used only when every higher-priority source is unavailable.

1. **Original PDF answer table** — the `[정답]` table in the source exam PDF
   (`data/문제_*.pdf`, `data/전기기사필기과년도*.pdf`). Highest authority.
2. **Original problem page choices (OCR / crop)** — the choice list on the original
   problem page, recovered by OCR or page crop, to confirm choice-to-number mapping.
3. **Existing Mathpix OCR** — `data/mathpix_기출_*.json` and related OCR artifacts.
4. **Theory calculation** — supporting evidence ONLY. A worked theoretical result may
   flag a suspected conflict but **must not replace a source answer**. An item is
   never marked `source_answer_verified` on theory alone.

## Manifest fields (proposed)

Read-only verification produces a manifest, one record per item:

| Field | Meaning |
| --- | --- |
| `key` | `{year}_{session}_{q_no}` |
| `current_q_answer` | `q.answer` currently stored in `questions.v2.json` |
| `source_answer` | answer found in the source (null if not found) |
| `source_answer_location` | where the source answer came from (PDF file + page, OCR file, etc.) |
| `source_choice_status` | `clean` / `ocr_corrupt` / `partial` — state of the choice list at the source |
| `verdict` | one of the 5 routes above |
| `evidence_note` | short note: what was checked and what was found |
| `next_action` | concrete follow-up for this item |

The manifest is written under `app/reports/` or `docs/audit/`; only a reviewed
manifest or this design is committed. The verifier never mutates app data.

## Apply gate

After verification, items split by route:

- `source_answer_verified` (source answer == `q.answer`) — **only these** are eligible
  for answer-locked regeneration. The Q2-A proposed solution (if any) may then be
  reconsidered for apply, still under supervisor approval.
- `source_answer_conflict` (source answer != `q.answer`) — routed to a separate
  **answer correction track**. `q.answer` itself is wrong and must be corrected at the
  data layer first; this is NOT a solution-quality fix.
- `source_choice_ocr_corrupt` — routed to a separate **choice recovery track**. The
  choice text must be repaired from the source before any answer judgment.
- `needs_pdf_page_crop` / `defer` — held until the required source asset or policy
  decision is available.

No answer-locked regeneration, and no answer correction, happens inside this track.
This track only produces the verified routing.

## Proposed pipeline

### Phase V0: Source inventory

- Confirm which source PDFs and OCR artifacts exist for the 30 pilot items'
  year/session.
- Identify which exams have a usable `[정답]` answer table.
- Read-only.

### Phase V1: Answer-table verification

- For each item, locate the source answer via the priority order above.
- Record `source_answer`, `source_answer_location`, `source_choice_status`.
- Assign a route.

### Phase V2: Manifest and split

- Emit the verification manifest.
- Split items into the four downstream groups defined in the Apply gate.

Exit criteria:

- Every pilot item has a route and an evidence note.
- No item is marked `source_answer_verified` on theory calculation alone.
- No app data mutation.

## Non-goals

- Do not modify `app/data/questions.json` or `app/data/questions.v2.json`.
- Do not correct any answer in this track (that is the answer correction track).
- Do not apply or regenerate any solution.
- Do not use paid API.
- Do not treat a theory calculation as a source answer.

## Budget policy

Default is no paid API. PDF answer-table reading and page crops are local operations.
A paid multimodal API call is considered only if a source page is unreadable by local
OCR/crop and the item is high-value — and only with explicit supervisor budget approval.

## Open decisions

- Whether the verification manifest lives under `app/reports/` (runtime) or
  `docs/audit/` (reviewed artifact).
- Whether `answer=0` sentinel items (if any reach this track) verify here or defer.
- Whether the answer correction track corrects `q.answer` in `questions.json` and
  `questions.v2.json` together, and how that interacts with the T3.5 verified set.

## Suggested next move

Implement Phase V0/V1 as a read-only verifier over the 30 pilot items, producing the
first verification manifest. Then route items and hand `source_answer_conflict` items
to the answer correction track.
