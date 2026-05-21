# Old Answer Manual Source Review Routing 3 (2026-05-21)

Routing summary for the third 10 items of the manual source review (pilot
items 21-30). This is a route-recording step only: no answer, choice, or
solution is applied here.

- Third pack commit: `ee58aab` (docs: prepare third source review pack)
- Third source review commit: `d4462c1` (docs: fill source answers for third review-pack items)
- Review pack: `docs/audit/old_answer_manual_source_review_pack3_2026-05-21.md`
- First routing summary: `docs/audit/old_answer_manual_source_review_routing_2026-05-21.md`
- Second routing summary: `docs/audit/old_answer_manual_source_review_routing2_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Scope

- Target range: pilot items 21-30 of the 30-item C1 pilot. With this pack the
  full 30-item pilot has been manually source-reviewed.

## Verdict tally (pilot 21-30)

| Verdict | Count |
| --- | ---: |
| `source_answer_verified` | 3 |
| `source_answer_conflict` | 7 |
| `source_choice_ocr_corrupt` | 0 |
| `needs_better_scan` | 0 |
| `defer` | 0 |

## verified — answer-locked regeneration candidate

These 3 items have a source answer found in the PDF that equals `q.answer`.
Next route: answer-locked regeneration candidate.

| key | subject | q_no | source_answer |
| --- | --- | ---: | ---: |
| `2015_3회_27` | 전력공학 | 27 | 3 |
| `2016_1회_71` | 제어공학 | 71 | 3 |
| `2016_3회_44` | 전기기기 | 44 | 4 |

Note: these 3 items are NOT yet approved for apply, and no dry-run has been
written for them yet. They return to the pool as regeneration candidates only.
Regeneration dry-run and apply each require separate approval.

## conflict — answer correction track

These 7 items have a source answer found in the PDF that differs from
`q.answer`. Next route: answer correction track.

| key | subject | q_no | current_q_answer | source_answer |
| --- | --- | ---: | ---: | ---: |
| `2015_2회_29` | 전력공학 | 29 | 1 | 2 |
| `2015_3회_22` | 전력공학 | 22 | 4 | 1 |
| `2015_3회_25` | 전력공학 | 25 | 1 | 4 |
| `2016_1회_44` | 전기기기 | 44 | 2 | 4 |
| `2016_1회_69` | 전력공학 | 69 | 1 | 4 |
| `2016_1회_70` | 제어공학 | 70 | 2 | 4 |
| `2016_3회_21` | 전력공학 | 21 | 1 | 4 |

Note: these 7 items remain in a no-modify state for `app/data`. A separate
answer correction design is required before any change. No `app/data` edit is
authorized by this routing record.

## Special cases

- The 3 `proposed_solution_written` items (`2015_3회_27`, `2016_1회_71`,
  `2016_3회_44`) are all `source_answer_verified` — the source 【답】 marker
  equals `q.answer`.
- The 7 `needs_source_answer_check` items are all `source_answer_conflict`.
- `2015_3회_25` and `2016_1회_44` were flagged as possible choice-OCR concerns
  in the prep sheet, but the source PDF choices are readable and the 【답】
  marker is clear; both resolve to `source_answer_conflict`, not
  `source_choice_ocr_corrupt`.

## Cumulative tally — full 30-item pilot

With pack 3 complete, all 30 pilot items have been manually source-reviewed
(pack 1: items 1-10, pack 2: items 11-20, pack 3: items 21-30).

| Verdict | Pack 1 | Pack 2 | Pack 3 | Total |
| --- | ---: | ---: | ---: | ---: |
| `source_answer_verified` | 4 | 2 | 3 | 9 |
| `source_answer_conflict` | 6 | 7 | 7 | 20 |
| `defer` | 0 | 1 | 0 | 1 |
| `source_choice_ocr_corrupt` | 0 | 0 | 0 | 0 |
| `needs_better_scan` | 0 | 0 | 0 | 0 |
| Total | 10 | 10 | 10 | 30 |

verified breakdown:

- already applied (Q2-B `fec4bbc` 4 items + Q2-C `fbeffef` 2 items): 6
- verified, not yet dry-run / apply (this pack's 3 items): 3

## Status constraints

- Q2 full apply remains BLOCKED.
- The 3 pack-3 verified items: regeneration candidates only — not apply-approved,
  no dry-run written yet.
- conflict 20 items (cumulative): `app/data` modification prohibited; sealed
  until a separate answer correction design exists.
- defer 1 item (`2014_3회_62`): sealed until a defective-question policy is
  defined.
- The earlier Q2-B apply (`fec4bbc`) and Q2-C apply (`fbeffef`) were limited
  exceptions for the 6 `source_answer_verified` items only and do not extend to
  this batch.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No answer correction.
- No solution apply.
- No regeneration apply.
- No modification of the 6 earlier-applied (`fec4bbc`, `fbeffef`) items.
- No modification of the conflict / defer items.
- No `solution_svg` modification.
