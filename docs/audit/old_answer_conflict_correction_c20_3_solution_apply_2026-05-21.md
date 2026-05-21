# Old Answer Conflict Correction — C20-3 Solution/Steps Apply Result (2026-05-21)

Apply-result log for the C20-3 solution/steps cleanup. The dry-run identified
1 of the 5 C20-3 items as needing a real `steps` edit; this step applied that
edit to `app/data/questions.json` and `app/data/questions.v2.json`. The other
4 items were already consistent with the corrected `q.answer` and were left
unchanged.

This is an apply-result record. No `answer` field was modified here — the
C20-3 answer correction was already applied in `8a6a961`. No `solution` field
was modified — the dry-run confirmed the affected item's `solution` body was
already correct.

- Base commits: `8a6a961` (C20-3 answer correction apply), `4408155`
  (C20-3 corrected-answer solution dry-run)
- Dry-run: `docs/audit/old_answer_conflict_correction_c20_3_solution_dryrun_2026-05-21.md`
- Apply result (answer): `docs/audit/old_answer_conflict_correction_c20_3_apply_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Edited item (1)

| key | corrected answer | change summary |
| --- | ---: | --- |
| `2015_2회_23` | 4 | `steps.계산`: the defective tail — which carried the stale phrase "정답의 참고 풀이에 오류가 있으며" and ended truncated mid-sentence at "(선택지 중 정확한 답이" with no explicit conclusion — was replaced. The new tail adds a 선택지 4 review line (choice ④ matches the π-circuit sending-end current formula), keeps the boxed `I_s` formula, and ends with an explicit "정답: ④". `solution` unchanged (already concluded (4)번). 선택지 1/2/3 review unchanged. |

The replacement uses the formula already derived in the same item's
`solution` body and in `steps.변환`. No new article, source, or derivation
was introduced.

## No-op items (4)

| key | corrected answer | reason for no change |
| --- | ---: | --- |
| `2015_1회_87` | 2 | `solution` and `steps` already conclude 2번 (300V) — consistent. No `app/data` change. |
| `2015_2회_29` | 2 | `solution` and `steps` already conclude 2번 (피뢰기) — consistent. No `app/data` change. |
| `2015_3회_22` | 1 | `solution` and `steps` already conclude 1번 (변압기 △ 결선) — consistent. No `app/data` change. |
| `2015_3회_25` | 4 | `solution` and `steps` already conclude 4번 (반한시-정한시 특성) — consistent. No `app/data` change. See choice-OCR flag below. |

## `2015_3회_25` — choice-OCR recovery flag

The DB-stored `choices` field for `2015_3회_25` is OCR-corrupt: choice [4]
holds page-footer residue ("15년도 3회 / 473 / 전기기사 펄기 D-60 시리즈")
instead of the choice text "반한시-정한시 특성", and choices [1]-[3] carry a
stray leading "：". The `solution` / `steps` already state the intended
choice ④ meaning ("반한시-정한시 특성") correctly and conclude 4번, so no
`solution` / `steps` edit was needed.

- Flag: `2015_3회_25` `choices` field requires choice-OCR recovery.
- Scope: this flag is recorded in audit only. The `choices` field in
  `app/data` was NOT modified.
- Follow-up: choice-OCR recovery track (shared with `2001_3회_43` from C20-1).

## Changed files

- `app/data/questions.json` — `steps` of 1 item updated.
- `app/data/questions.v2.json` — `steps` of 1 item updated.

`solution` / `steps` content strings are identical between the two files; the
files differ only in provenance metadata (`*_source`) and `solution_svg`
representation, neither of which was touched.

## Changed fields

- `2015_2회_23`: `steps` only.
- No other field changed for any item. `answer`, `solution`, `choices`,
  `text`, metadata, `*_source`, and `solution_svg` are unchanged.

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- Exactly 1 item changed in each file; the change is confined to `steps` only.
- C20-3 answers unchanged: `2015_1회_87`=2, `2015_2회_23`=4, `2015_2회_29`=2,
  `2015_3회_22`=1, `2015_3회_25`=4.
- Edited item `2015_2회_23`: `solution` field byte-identical to pre-state;
  no non-`steps` field changed.
- `steps.계산` of `2015_2회_23` now ends with an explicit "**정답: ④**".
- No-op items (`2015_1회_87`, `2015_2회_29`, `2015_3회_22`, `2015_3회_25`)
  byte-identical to pre-state.
- `choices` / `text` / metadata / `solution_svg` unchanged for all items.
- C20-1 / C20-2 items (10 keys), C20-4 items (4 keys), and DQ-1 items
  (`2014_2회_50`, `2014_3회_62`) unchanged.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the edited string line; no mass
  reformatting.

## Downstream status

- C20-3 `answer_corrected_solution_pending` state is RESOLVED for all 5 items:
  1 had its `steps` corrected to match the corrected `q.answer`; 4 were
  already consistent.
- `solution_svg` is still pending the SVG-AUDIT track (not modified here).
- `2015_3회_25` carries a choice-OCR recovery flag (above).

## Status

- Q2 bulk apply remains BLOCKED.
- This step covered C20-3 only. C20-4 is not applied and requires separate
  per-batch approval.
- C20-1 closed (`13036de` + `8f4bdf0`). C20-2 closed (`c7390e4` + `8ad2689`).
  C20-3 is now closed (`8a6a961` + this step).
- DQ-1 items remain sealed pending the defective / multi-answer policy.

## Not done in this step

- No `answer` modification.
- No `solution` modification.
- No `choices` / question text / metadata modification (incl. `2015_3회_25`
  choice-OCR).
- No `solution_svg` modification.
- No modification of the 4 no-op items.
- No C20-1 / C20-2 / C20-4 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
