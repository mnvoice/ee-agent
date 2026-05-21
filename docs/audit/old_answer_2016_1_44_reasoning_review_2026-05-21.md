# Old Answer — `2016_1회_44` Deep Reasoning Review (2026-05-21)

Read-only deep review of `2016_1회_44`. The C20-4 closeout flagged this item:
its `q.answer` is corrected (4) and its `solution` / `steps` had a minimal
hedge cleanup, but the reasoning body was suspected to enumerate effects that
do not match the actual choice texts. This review compares the current
`app/data` record (question / choices / answer / solution / steps) and
judges whether the reasoning is logically consistent with the actual choices
and the source answer 4.

This is a **read-only review document**. It does NOT modify `app/data`,
`choices`, `solution` / `steps`, `answer`, `solution_svg`, app code, or the
schema. It proposes a follow-up route only.

- Base commits: `c9ea03c` (C20-4 answer correction), `de0c6ab` (C20-4
  solution cleanup), `10d8901` (SVG audit)
- Source review pack: `old_answer_manual_source_review_pack3_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Record snapshot (read-only)

- key: `2016_1회_44`
- answer: `4` (corrected; source marker 【답】④, pack3 p.15)
- subject: 전기기기 / q_type: 암기형

Question text:

> 직류기의 전기자 반작용에 의한 영향이 아닌 것은?

Choices (as stored in `app/data`, readable, not OCR-corrupt):

| # | choice text |
| --- | --- |
| [1] | 자속이 감소하므로 유기기전력이 감소한다. |
| [2] | 발전기의 굽은 회전방향으로 기하학적 중성축이 형성된다. |
| [3] | 전동기의 굽은 회전방향과 반대방향으로 기하학적 중성축이 형성된다. |
| [4] | 브러시에 의해 단락된 코일에는 기전력이 발생하므로 브러시 사이의 유기기전력이 증가한다. |

`solution` summary: lists "전기자 반작용의 영향" as four items —
(1) 전기적 중성축 이동, (2) 주자속 감소 및 유기기전력 감소, (3) 정류자
편간 섬락, (4) 발전기 출력감소 — then states "정답: 4번" and the reason
"모든 선택지가 전기자 반작용의 실제 영향이며, 보기 (4)는 (2)의 결과이므로
별도의 영향이 아니다."

`steps` summary: `인식` / `변환` classify armature-reaction effects into
direct / indirect. `계산` maps "1번: 중성축 이동 / 2번: 주자속 감소 /
3번: 섬락 / 4번: 출력감소" and concludes "정답: 4번 — 가장 간접적인 2차
영향인 4번이 별도의 독립적 영향이 아님."

## Review questions

### Q1. Does answer 4 match the source marker?

YES. The source review pack 3 records 【답】④ (p.15). Standard DC-machine
theory also confirms it: choice [4] describes a commutation phenomenon, not
an armature-reaction effect (see Q3). Answer 4 is correct.

### Q2. Does the choice [4] text match the solution's conclusion?

PARTIALLY. The solution prints "정답: 4번", which matches `q.answer` = 4 as a
number. But the solution never addresses the actual content of choice [4]
("브러시에 의해 단락된 코일에는 기전력이 발생하므로 브러시 사이의
유기기전력이 증가한다"). The solution's item "(4) 발전기 출력감소" is not
choice [4]. The conclusion number is right; the solution's treatment of
choice [4] is about a different statement.

### Q3. Does the solution body enumerate the actual choices, or describe other options?

It describes other options. The solution body and `steps` enumerate a
generic list of armature-reaction effects —
중성축 이동 / 주자속 감소 / 섬락 / 출력감소 — and label them (1)-(4) /
1번-4번. That enumeration does NOT correspond to the actual choices:

| solution / steps item | actual choice |
| --- | --- |
| "(1) 중성축 이동" | choice [1] is 자속 감소 → 유기기전력 감소 |
| "(2) 주자속 감소" | choice [2] is 발전기 기하학적 중성축 |
| "(3) 섬락" | choice [3] is 전동기 기하학적 중성축 |
| "(4) 발전기 출력감소" | choice [4] is 브러시 단락 코일 기전력 |

The mapping is wrong at every position. The solution also asserts "모든
선택지가 전기자 반작용의 실제 영향" — which is false: choice [4] is NOT an
armature-reaction effect, which is precisely why it is the answer.

Correct reasoning (standard DC-machine theory, for the future cleanup —
not applied here):

- Choice [1] — armature reaction causes demagnetization (감자작용); the main
  flux decreases and the induced EMF decreases. This IS an armature-reaction
  effect. (True statement.)
- Choices [2], [3] — armature reaction shifts the neutral axis (generator: in
  the rotation direction; motor: opposite). These describe the neutral-axis
  shift, an armature-reaction effect. (True statements; note the choices say
  "기하학적 중성축", a loose wording — see Q5.)
- Choice [4] — a coil short-circuited by the brush and the EMF in it is a
  commutation (정류) phenomenon (reactance voltage during commutation), not
  an armature-reaction effect. Moreover armature reaction DECREASES the brush
  EMF (via demagnetization), so "유기기전력이 증가한다" is doubly wrong.
  Therefore choice [4] is "NOT an armature-reaction effect" → the answer.

The current solution's stated reason ("(4)는 (2)의 결과이므로 별도의 영향이
아니다") is wrong both in content (choice [4] is not 출력감소) and in logic
(the item is the answer because it is a commutation phenomenon, not because
it is a "secondary effect").

### Q4. Do the `steps` connect choices and answer consistently?

NO. `steps.계산` maps "1번-4번" onto the same wrong enumeration as the
solution body. The per-choice verification does not correspond to the actual
choices, so the steps do not consistently connect the choices to the answer.
The conclusion "정답: 4번" is correct only by coincidence of the number.

### Q5. Is the remaining risk a choice-OCR problem, a reasoning problem, or a wording problem?

It is a **reasoning problem**.

- NOT choice-OCR: choices [1]-[4] are stored as readable, well-formed
  sentences. There is no OCR corruption. (Unlike `2001_3회_43` /
  `2015_3회_25`, which had genuine choice-OCR damage.)
- A minor wording quirk exists in the source question: choices [2]/[3] say
  "기하학적 중성축" where standard theory would say "전기적(자기적) 중성축"
  shifts. This is a source-question wording quirk; it does not change the
  answer and is not the solution's defect.
- The actual defect is in the `solution` / `steps`: the reasoning body was
  written against a generic armature-reaction effect list rather than the
  actual choice texts, and it gives a wrong reason for why choice [4] is the
  answer. The conclusion number (4) is correct; the reasoning is mismatched.

## Verdict

`needs_solution_cleanup`

The `q.answer` (4) is correct and source-locked. The `choices` are intact
(no OCR recovery needed). The `solution` and `steps` reasoning body, however,
enumerates the wrong items as choices and gives a wrong rationale. The
conclusion is right but the reasoning does not match the actual choices.

## Follow-up route

- Route: `needs_solution_cleanup` → a separate `solution` / `steps` cleanup
  dry-run for `2016_1회_44`, following the C20 dry-run → apply pattern.
- Scope of that future cleanup: rewrite the `solution` / `steps` reasoning so
  that the per-choice analysis matches the actual choice texts [1]-[4] and
  states the correct reason choice [4] is the answer (choice [4] describes a
  commutation phenomenon, not an armature-reaction effect; choices [1]-[3]
  are genuine armature-reaction effects). The `q.answer` (4), `choices`, and
  `solution_svg` (this item has no `solution_svg` — confirmed by the SVG
  audit) are not touched.
- This review does NOT perform that cleanup. It only records the verdict and
  the route.

## Status

- `2016_1회_44`: `q.answer` = 4 (closed). `choices` intact. `solution` /
  `steps` reasoning flagged `needs_solution_cleanup`.
- No choice-OCR recovery needed for this item.
- Q2 bulk apply remains BLOCKED.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `choices` modification.
- No `solution` / `steps` modification.
- No `answer` modification.
- No `solution_svg` modification.
- No app code or schema modification.
- No paid API call.
- No push.
