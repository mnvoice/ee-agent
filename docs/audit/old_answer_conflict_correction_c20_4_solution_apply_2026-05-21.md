# Old Answer Conflict Correction — C20-4 Solution/Steps Apply Result (2026-05-21)

Apply-result log for the C20-4 solution/steps cleanup. The dry-run identified
all 4 C20-4 items as needing a `solution` / `steps` edit; this step applied
those 4 edits to `app/data/questions.json` and `app/data/questions.v2.json`.

C20-4 is the final batch of the 19-item single-answer correction set. With
this step, the C20 single-answer answer correction track is complete —
all 19 items have both `answer` corrected and `solution` / `steps`
reconciled.

This is an apply-result record. No `answer` field was modified here — the
C20-4 answer correction was already applied in `c9ea03c`.

- Base commits: `c9ea03c` (C20-4 answer correction apply), `e7c96c5`
  (C20-4 corrected-answer solution dry-run)
- Dry-run: `docs/audit/old_answer_conflict_correction_c20_4_solution_dryrun_2026-05-21.md`
- Apply result (answer): `docs/audit/old_answer_conflict_correction_c20_4_apply_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Edited items (4) — no no-op items

| key | corrected answer | change summary |
| --- | ---: | --- |
| `2016_1회_44` | 4 | `solution`: trailing hedge sentence "다만 문제 원문이 불완전하여 정확한 오답지를 특정하기 어렵습니다." (which contradicted the firm "정답: 4번") removed. `steps.계산`: hedge "(불완전한 보기이지만 개념상) " removed. Conclusion 4번 kept. |
| `2016_1회_69` | 4 | `steps.계산`: stale alternative-answer hedge "또는 선택지가 공진치인 경우 1번 (공진치)" removed. `solution` unchanged (already concluded (4)번). |
| `2016_1회_70` | 4 | `steps.계산`: stale "(선택지에 명시 필요)" parenthetical removed; final conclusion "정답: 0[dB], ±180° (표준 정답은 …)" replaced with explicit "정답: ④ 0[dB], -180°". `solution` unchanged (already concluded (4)번). |
| `2016_3회_21` | 4 | `steps.변환` + `steps.계산`: the wrong conclusion choice [1] ("전류에 비례") corrected. The fix completes the chain `A ∝ I²` and `I ∝ 1/V` ⇒ `A ∝ 1/V²`, concluding "정답: ④ 전압의 제곱에 반비례한다". `solution` unchanged (already derived `A ∝ 1/V²`). |

## No-op items

None. Unlike C20-3 (4 no-op items), all 4 C20-4 items required a
`solution` / `steps` edit.

## `2016_1회_44` — deeper review flag

For `2016_1회_44`, the applied edit was the minimal cleanup approved by the
dry-run: removal of the contradicting hedge sentences. The conclusion (4번)
is source-locked and now stands without contradiction.

A residual weakness remains and is NOT fixed by this step: the `solution`
body and `steps.계산` enumerate generic armature-reaction effects
("중성축 이동 / 주자속 감소 / 섬락 / 출력감소") that do not map to the actual
choice texts (choice [4] concerns EMF in brush-short-circuited coils — a
commutation phenomenon, which is why it is "not an armature reaction
effect"). A correct explanation would require rewriting the reasoning body,
which is beyond minimal cleanup and would risk overexpansion / fabrication.

- Flag: `2016_1회_44` `solution` / `steps` reasoning body needs a deeper
  review against the source 풀이 (the conclusion is correct; the reasoning
  is built on a mismatched enumeration).
- Scope: this flag is recorded in audit only. No further `solution` / `steps`
  rewrite was performed.

## Risk note — `2016_3회_21` was a genuine wrong-conclusion fix

`2016_3회_21` `steps.변환` and `steps.계산` previously concluded choice [1]
("전류에 비례") — the opposite of the corrected answer 4. The applied fix is
source-grounded: the `solution` body already holds the full derivation
(`I ∝ 1/V` from constant power, `R ∝ V²` from constant loss, `A ∝ 1/V²`).
The fix connects the `steps`' own `A ∝ I²` derivation with `I ∝ 1/V` to
reach `A ∝ 1/V²` = choice [4]. No physics was newly expanded; the missing
link joins pieces already present.

## Changed files

- `app/data/questions.json` — `solution` / `steps` of 4 items updated.
- `app/data/questions.v2.json` — `solution` / `steps` of 4 items updated.

`solution` / `steps` content strings are identical between the two files; the
files differ only in provenance metadata (`*_source`) and `solution_svg`
representation, neither of which was touched.

## Changed fields

- `2016_1회_44`: `solution`, `steps`.
- `2016_1회_69`: `steps`.
- `2016_1회_70`: `steps`.
- `2016_3회_21`: `steps`.
- No other field changed for any item. `answer`, `choices`, `text`,
  metadata, `*_source`, and `solution_svg` are unchanged.

## Verification (run against `git HEAD` pre-state)

- `app/data/questions.json` — JSON parse OK.
- `app/data/questions.v2.json` — JSON parse OK.
- Record count unchanged: 5331 in both files (pre == post).
- Exactly 4 items changed in each file; each change is confined to
  `solution` / `steps` only.
- C20-4 answers unchanged: all 4 items `answer` = 4.
- Edited items: all non-`solution`/`steps` fields unchanged.
- `2016_3회_21` `steps.계산` now concludes "정답: ④ 전압의 제곱에
  반비례한다"; the prior "정답: 1. 전류에 비례한다" is gone.
- `choices` / `text` / metadata / `solution_svg` unchanged for all items.
- C20-1 / C20-2 / C20-3 items (15 keys) and DQ-1 items
  (`2014_2회_50`, `2014_3회_62`) unchanged.
- `git diff --check` — no whitespace errors.
- Serialization preserved — diff confined to the edited string lines; no mass
  reformatting.

## Downstream status

- C20-4 `answer_corrected_solution_pending` state is RESOLVED for all 4 items.
- The C20 single-answer correction set (19 items) is now fully closed:
  every item has `answer` corrected and `solution` / `steps` reconciled.
  - C20-1 closed: `13036de` + `8f4bdf0`
  - C20-2 closed: `c7390e4` + `8ad2689`
  - C20-3 closed: `8a6a961` + `5f80afa`
  - C20-4 closed: `c9ea03c` + this step
- `solution_svg` for all C20 items is still pending the SVG-AUDIT track.
- Open follow-up flags: `2016_1회_44` deeper reasoning review;
  `2001_3회_43` and `2015_3회_25` choice-OCR recovery.

## Status

- Q2 bulk apply remains BLOCKED.
- The C20 single-answer answer correction track is complete.
- DQ-1 items (`2014_2회_50` double marker, `2014_3회_62` 전항정답) remain
  sealed pending the defective / multi-answer policy.

## Not done in this step

- No `answer` modification.
- No `choices` / question text / metadata modification.
- No `solution_svg` modification.
- No `2016_1회_44` reasoning-body rewrite (deeper review flagged only).
- No C20-1 / C20-2 / C20-3 modification.
- No DQ-1 item modification.
- No paid API call.
- No push.
