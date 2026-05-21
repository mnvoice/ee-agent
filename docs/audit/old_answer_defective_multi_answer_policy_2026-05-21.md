# Old Answer — Defective / Multi-answer Policy (DQ-1) Design (2026-05-21)

Policy design for the 2 DQ-1 items that the C20 single-answer correction
track could not safely handle: `2014_2회_50` (double marker) and
`2014_3회_62` (전항정답). Both have a source 【답】 marker that cannot be
represented as a single 1-4 `q.answer`.

This is a **policy design document only**. It does NOT modify `app/data`,
does NOT change any `q.answer`, does NOT change the schema, and does NOT
modify app code. It is not an approval to apply.

- C20 closeout: `docs/audit/old_answer_conflict_correction_closeout_2026-05-21.md`
- Source review pack: `old_answer_manual_source_review_pack2_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## 1. Background

- The 30-item C1 pilot was source-reviewed against the source PDF 【답】
  markers.
- 9 `source_answer_verified` items were applied earlier (answer-locked
  regenerated `solution` / `steps`).
- 19 single-`source_answer` `source_answer_conflict` items had their
  `q.answer` corrected and `solution` / `steps` reconciled (C20 track,
  closed at `5277967`).
- The remaining 2 items (DQ-1) cannot be safely handled by the single-answer
  `q.answer` structure. Their source markers are not a single 1-4 value.

## 2. DQ-1 target items (2)

`current route` = `defer`. `apply_status` = `not_applied` for both.

| key | current_q_answer | source_answer_marker | source_page | evidence_note | issue_type |
| --- | ---: | --- | --- | --- | --- |
| `2014_2회_50` | 3 | ①,② | p.17 | 문제 50 풀이 (V곡선 정의: 단자전압·부하 일정, 여자전류 변화) ends with a double marker 【답】①,②. `q.answer=3` matches neither. | `multi_answer_marker` |
| `2014_3회_62` | 4 | 전항정답 | p.19 | 문제 62 풀이 table gives F(s)=1/s and F(z)=z/(z-1); no single choice matches that pair, so the source marks 【답】전항정답 (all-choice / defective question). | `all_answer_defective` |

Both: `current route` = `defer`, `apply_status` = `not_applied`.

## 3. Policy problem

The `q.answer` field, as currently used, holds a single choice index. The
two DQ-1 items do not map onto that structure:

- `2014_2회_50` — the source accepts two choices (① and ②). A single
  `q.answer` cannot express "either ① or ② is correct".
- `2014_3회_62` — the source marks 전항정답 (all choices accepted /
  defective question). A single `q.answer` cannot express "all choices
  accepted" or "the item is defective".

Risks of force-mapping either item onto a single `q.answer`:

- **Scoring distortion** — a learner who picks the other valid choice
  (e.g. ② when `q.answer` is forced to ①) is wrongly marked incorrect.
- **Source evidence loss** — the source marker (①,② or 전항정답) is not
  recorded anywhere; the fact that the item is multi-answer / defective
  disappears.
- **UI / solution / answer-lock mismatch** — `solution` / `steps` that
  describe a multi-answer or defective situation would be inconsistent with
  a single forced `q.answer`.

Open question: whether the current `app/data` schema (`questions.json` /
`questions.v2.json`) and the app's scoring / rendering logic support a
multi-answer or defective-question representation at all. This is NOT
investigated in this document — it is deferred to DQ-2 (Section 5).

## 4. Processing options

| Option | Description | Assessment |
| --- | --- | --- |
| A — keep `defer` | No `app/data` modification. Manage via this audit document and a hold list. | Safe. Zero risk. Preserves source evidence in audit. No scoring fix. |
| B — add metadata / flag | Add fields such as `answer_status`, `source_answer_marker`, `defective_question`. | Records the source truth without changing `q.answer`. Needs schema + app + UI impact review. |
| C — force a single representative `q.answer` | Pick one choice arbitrarily as `q.answer`. | NOT RECOMMENDED / prohibited. Distorts the source; causes scoring distortion. |
| D — deactivate / exclude the item | Remove the item from scoring / exposure. | Needs a scoring / exposure policy. Loses the item from the bank. |
| E — introduce a multi-answer schema | E.g. `answers: [1,2]` or `all_answers: true`. | Most faithful representation. Needs app logic, validation, and migration work. |

## 5. Recommendation

- Do NOT modify `app/data` now.
- Keep the 2 DQ-1 items in `defer`.
- Answer correction for DQ-1 items is prohibited until a separate
  schema / policy is designed and approved.
- Open a follow-up track **DQ-2** to investigate schema impact, read-only:
  - Read-only scan: do `questions.json` / `questions.v2.json` already carry
    any field that could express a multi-answer or defective state?
  - Read-only scan: does the app's rendering / scoring logic assume a single
    `answer` value only?
  - After the scan, choose a policy option (B or E if a representation is
    feasible; A or D otherwise).

Rationale: Option C is excluded outright (source distortion). Options B, D,
and E all depend on facts about the schema and app logic that are not yet
known. The responsible next step is the DQ-2 read-only investigation, not a
premature policy commitment.

## 6. Gate — before any DQ item apply

A DQ item may be applied only after all of the following hold:

- The data-schema representation method is decided (which field(s) express a
  multi-answer / defective state).
- The impact on the app's scoring and rendering logic is confirmed.
- A migration strategy is decided (how existing records and the two DQ items
  move to the new representation).
- The source evidence (source marker, page, evidence note) is recorded.
- A browser / static verification plan exists (the change is checked in the
  running app, not only in the JSON).

## 7. Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `q.answer` modification.
- No `solution` / `steps` modification.
- No schema change.
- No app logic change.
- No `solution_svg` modification.
- No paid API call.
- No push.

## 8. Status

- The 2 DQ-1 items remain `defer` / `not_applied`.
- Q2 bulk apply remains BLOCKED.
- Next: DQ-2 read-only schema / app-logic investigation, then a policy
  decision among Options A / B / D / E.
