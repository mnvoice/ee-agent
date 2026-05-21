# Old Answer Manual Source Review Routing (2026-05-21)

Routing summary for the first 10 items of the manual source review. This is a
route-recording step only: no answer, choice, or solution is applied here.

- Source review commit: `4317aea` (docs: fill source answers for first 10 review-pack items)
- Review pack: `docs/audit/old_answer_manual_source_review_pack_2026-05-21.md`
- Pilot source: `docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Verdict tally (first 10)

| Verdict | Count |
| --- | ---: |
| `source_answer_verified` | 4 |
| `source_answer_conflict` | 6 |
| `source_choice_ocr_corrupt` | 0 |
| `needs_better_scan` | 0 |
| `defer` | 0 |

## verified — answer-locked regeneration candidate

These 4 items have a source answer found in the PDF that equals `q.answer`.
Next route: answer-locked regeneration candidate.

| key | subject | q_no | source_answer |
| --- | --- | ---: | ---: |
| `2001_1회_21` | 전력공학 | 21 | 2 |
| `2002_1회_32` | 전력공학 | 32 | 1 |
| `2005_3회_83` | 전기설비기술기준 | 83 | 4 |
| `2006_1회_7` | 전기자기학 | 7 | 2 |

Note: these 4 items are NOT yet approved for apply. They return to the pool as
regeneration candidates only. Regeneration apply requires separate approval.

## conflict — answer correction track

These 6 items have a source answer found in the PDF that differs from
`q.answer`. Next route: answer correction track.

| key | subject | q_no | current_q_answer | source_answer |
| --- | --- | ---: | ---: | ---: |
| `1998_4회_10` | 전기자기학 | 10 | 1 | 4 |
| `2001_1회_68` | 제어공학 | 68 | 1 | 3 |
| `2001_3회_41` | 전기기기 | 41 | 2 | 4 |
| `2001_3회_43` | 전기기기 | 43 | 1 | 2 |
| `2002_3회_4` | 전기자기학 | 4 | 2 | 4 |
| `2006_1회_6` | 전기자기학 | 6 | 4 | 3 |

Note: these 6 items remain in a no-modify state for `app/data`. A separate
answer correction design is required before any change. No `app/data` edit is
authorized by this routing record.

## Status constraints

- Q2 apply remains BLOCKED.
- verified 4 items: regeneration candidates only — not apply-approved.
- conflict 6 items: `app/data` modification prohibited; separate answer
  correction design required.
- `source_choice_ocr_corrupt` / `needs_better_scan` / `defer`: 0 items, no
  recovery or hold track is opened.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No answer correction.
- No solution apply.
- No regeneration apply.
