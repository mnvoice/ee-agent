# Old Answer Manual Source Review Routing 2 (2026-05-21)

Routing summary for the second 10 items of the manual source review (pilot
items 11-20). This is a route-recording step only: no answer, choice, or
solution is applied here.

- Source review commit: `041b83f` (docs: fill source answers for second review-pack items)
- Second pack commit: `e5dc08a` (docs: prepare second source review pack)
- Review pack: `docs/audit/old_answer_manual_source_review_pack2_2026-05-21.md`
- First routing summary: `docs/audit/old_answer_manual_source_review_routing_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Scope

- Target range: pilot items 11-20 of the 30-item C1 pilot.

## Verdict tally (pilot 11-20)

| Verdict | Count |
| --- | ---: |
| `source_answer_verified` | 2 |
| `source_answer_conflict` | 7 |
| `defer` | 1 |
| `source_choice_ocr_corrupt` | 0 |
| `needs_better_scan` | 0 |

## verified — answer-locked regeneration candidate

These 2 items have a source answer found in the PDF that equals `q.answer`.
Next route: answer-locked regeneration candidate.

| key | subject | q_no | source_answer |
| --- | --- | ---: | ---: |
| `2015_1회_13` | 전기자기학 | 13 | 1 |
| `2015_1회_22` | 전력공학 | 22 | 1 |

Note: these 2 items are NOT yet approved for apply. They return to the pool as
regeneration candidates only. Regeneration apply requires separate approval.

## conflict — answer correction track

These 7 items have a source answer found in the PDF that differs from
`q.answer`. Next route: answer correction track.

| key | subject | q_no | current_q_answer | source_answer |
| --- | --- | ---: | ---: | ---: |
| `2006_2회_27` | 전력공학 | 27 | 3 | 4 |
| `2007_1회_9` | 전기자기학 | 9 | 4 | 2 |
| `2007_2회_64` | 회로이론 | 64 | 2 | 1 |
| `2014_2회_50` | 전기기기 | 50 | 3 | 1, 2 |
| `2015_1회_71` | 전기자기학 | 71 | 4 | 1 |
| `2015_1회_87` | 전기설비기술기준 | 87 | 3 | 2 |
| `2015_2회_23` | 전력공학 | 23 | 3 | 4 |

Note: these 7 items remain in a no-modify state for `app/data`. A separate
answer correction design is required before any change. No `app/data` edit is
authorized by this routing record.

## defer — defective-question policy needed

This 1 item has no single source answer to lock against.

| key | subject | q_no | current_q_answer | reason |
| --- | --- | ---: | ---: | --- |
| `2014_3회_62` | 회로이론 | 62 | 4 | 원문 【답】전항정답 / defective question. The source 풀이 table gives F(s)=1/s and F(z)=z/(z-1), which no single choice matches; the official marker accepts all choices. No single source answer exists. |

Next route: defer / defective-question policy needed. This item is held until a
policy for defective ("전항정답") questions is defined. It is not classified as
`source_answer_verified` or `source_answer_conflict` by a simple branch.

## Special cases

- `2014_2회_50`: the source carries a double marker 【답】①,②. Because
  `q.answer=3` matches neither, it is routed as `source_answer_conflict`, not
  as a partial match.
- `2014_3회_62`: the source marker is 【답】전항정답 (defective question).
  Do NOT branch it into `source_answer_verified` / `source_answer_conflict`;
  it is routed as `defer` pending a defective-question policy.

## Status constraints

- Q2 full apply remains BLOCKED.
- verified 2 items: regeneration candidates only — not apply-approved.
- conflict 7 items: `app/data` modification prohibited; sealed until a separate
  answer correction design exists.
- defer 1 item: sealed until a defective-question policy is defined.
- The earlier Q2-B apply (`fec4bbc`) was a limited exception for 4
  `source_answer_verified` items only and does not extend to this batch.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No answer correction.
- No solution apply.
- No regeneration apply.
- No modification of the 4 earlier-applied (`fec4bbc`) items.
- No modification of the conflict / defer items.
- No `solution_svg` modification.
