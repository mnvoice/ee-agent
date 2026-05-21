# Old Answer — `2016_1회_44` Solution/Steps Cleanup Dry-run (2026-05-21)

Solution/steps cleanup dry-run for `2016_1회_44`. The reasoning review
(`fb3bb91`) verdict was `needs_solution_cleanup`: the `q.answer` (4) is
correct but the `solution` / `steps` reasoning body enumerates a generic
armature-reaction effect list that does not match the actual choice texts.
This document proposes an answer-locked `solution` / `steps` draft that
reasons about the actual choices.

This is a **dry-run document only**. It does NOT modify `app/data` and is not
an approval to apply.

- Base commits: `fb3bb91` (`2016_1회_44` reasoning review), `de0c6ab`
  (C20-4 solution cleanup)
- Reasoning review: `docs/audit/old_answer_2016_1_44_reasoning_review_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Current issue summary

- `q.answer` = 4 (corrected; source 【답】④, pack3 p.15). `choices` are
  intact (no OCR damage). The item has no `solution_svg`.
- The existing `solution` and `steps` enumerate a generic armature-reaction
  effect list — 중성축 이동 / 주자속 감소 / 섬락 / 출력감소 — and label it
  (1)-(4) / 1번-4번. That enumeration does not correspond to the actual
  choices.
- The existing reasoning never addresses the actual content of choice [4]
  ("브러시에 의해 단락된 코일에는 기전력이 발생하므로 브러시 사이의
  유기기전력이 증가한다"), and gives a wrong rationale ("(4)는 (2)의
  결과"). The conclusion number 4 is correct only by coincidence.

## Actual choices (read-only, from `app/data`)

| # | choice text |
| --- | --- |
| [1] | 자속이 감소하므로 유기기전력이 감소한다. |
| [2] | 발전기의 굽은 회전방향으로 기하학적 중성축이 형성된다. |
| [3] | 전동기의 굽은 회전방향과 반대방향으로 기하학적 중성축이 형성된다. |
| [4] | 브러시에 의해 단락된 코일에는 기전력이 발생하므로 브러시 사이의 유기기전력이 증가한다. |

## Corrected reasoning

Representative effects of armature reaction in a DC machine:

- 주자속 감소 / 감자 작용 — the armature-current flux weakens the main flux.
- 중성축 이동 — the flux distortion shifts the neutral axis (generator: in
  the rotation direction; motor: opposite to the rotation direction).
- 정류 악화 및 섬락 가능성 — with the neutral axis shifted, commutation at
  the brush position worsens and sparking can occur.

Applying this to the choices:

- Choices [1], [2], [3] each describe an armature-reaction effect:
  [1] = demagnetization (flux ↓ → induced EMF ↓), [2] = generator
  neutral-axis shift in the rotation direction, [3] = motor neutral-axis
  shift opposite to the rotation direction. All three ARE armature-reaction
  effects.
- Choice [4] — a coil short-circuited by the brush developing an EMF is a
  commutation-process phenomenon (the reactance voltage during commutation);
  it is not a direct effect of armature reaction. Furthermore, armature
  reaction reduces the induced EMF (via demagnetization), so the claim that
  "유기기전력이 증가한다" does not match an armature-reaction effect either.

Therefore the choice that is NOT an effect of armature reaction is [4].
This matches `q.answer` = 4 and the source marker 【답】④.

## Proposed solution draft

> 직류기의 전기자 반작용에 의한 영향이 아닌 것을 고르는 문제입니다.
>
> **전기자 반작용(Armature Reaction)의 대표적 영향:**
> - 주자속 감소(감자 작용): 전기자 전류가 만드는 자속이 주자속을 약화시킨다.
> - 중성축 이동: 자속 분포가 일그러져 중성축이 발전기는 회전 방향으로,
>   전동기는 회전 방향과 반대로 이동한다.
> - 정류 악화 및 섬락 가능성: 중성축이 이동하면 브러시 위치의 정류가
>   나빠져 불꽃(섬락)이 발생할 수 있다.
>
> **각 보기 검토:**
> - (1) 자속이 감소하므로 유기기전력이 감소한다 → 감자 작용으로 주자속이
>   줄고 유기기전력이 감소한다. **전기자 반작용의 영향이 맞다.**
> - (2) 발전기의 회전 방향으로 중성축이 형성(이동)된다 → 발전기에서
>   중성축은 회전 방향으로 이동한다. **전기자 반작용의 영향이 맞다.**
> - (3) 전동기의 회전 방향과 반대 방향으로 중성축이 형성(이동)된다 →
>   전동기에서 중성축은 회전 방향과 반대로 이동한다.
>   **전기자 반작용의 영향이 맞다.**
> - (4) 브러시에 의해 단락된 코일에 기전력이 발생하여 브러시 사이의
>   유기기전력이 증가한다 → 브러시로 단락된 코일에 기전력이 생기는 현상은
>   **정류(commutation) 과정의 리액턴스 전압** 문제로, 전기자 반작용의
>   직접적인 영향으로 보기 어렵다. 또한 전기자 반작용은 감자 작용으로
>   유기기전력을 **감소**시키므로 "유기기전력이 증가한다"는 서술과도 맞지
>   않는다.
>
> **정답: 4번**
>
> 전기자 반작용의 영향은 (1)·(2)·(3)이며, (4)는 정류 과정에 관한
> 설명이므로 전기자 반작용의 영향이 아니다.

## Proposed steps draft

`인식`:

> 직류기의 전기자 반작용이 미치는 영향을 묻는 문제다. 보기 중 전기자
> 반작용의 영향이 **아닌** 것을 골라야 하므로, 전기자 반작용의 대표
> 영향(감자 작용·중성축 이동·정류 악화)과 정류 과정의 현상을 구별하는
> 것이 핵심이다.

`변환`:

> 전기자 반작용의 대표 영향을 정리:
> - 감자 작용: 전기자 자속이 주자속을 약화 → 주자속 감소 → 유기기전력 감소
> - 중성축 이동: 발전기는 회전 방향, 전동기는 회전 방향과 반대로 이동
> - 정류 악화: 중성축 이동으로 브러시 위치의 정류가 나빠져 섬락 가능
>
> 한편 브러시로 단락된 코일에 생기는 기전력은 정류(commutation) 과정의
> 리액턴스 전압 현상으로, 전기자 반작용과 구분된다.

`계산`:

> 각 보기를 전기자 반작용의 영향 여부로 검증:
> - (1) 자속 감소 → 유기기전력 감소: 감자 작용의 결과 → 전기자 반작용의
>   영향 (O)
> - (2) 발전기 회전 방향으로 중성축 이동: 전기자 반작용의 영향 (O)
> - (3) 전동기 회전 방향과 반대로 중성축 이동: 전기자 반작용의 영향 (O)
> - (4) 브러시 단락 코일의 기전력 → 브러시 사이 유기기전력 증가: 정류
>   과정의 리액턴스 전압 문제이며, 전기자 반작용은 오히려 유기기전력을
>   감소시킨다 → 전기자 반작용의 영향이 아님 (X)
>
> **정답: 4번** (전기자 반작용의 영향이 아닌 것)

## Answer-lock checks

- conclusion matches `q.answer` = 4: YES — both the proposed `solution` and
  `steps` conclude 4번, and the per-choice analysis identifies [4] as the
  one that is NOT an armature-reaction effect.
- no figure dependency: YES — the item has no `solution_svg`; the proposed
  drafts are conceptual text with no figure reference.
- no invented source/article claim: YES — the drafts use standard DC-machine
  theory only; no statute number, article, or external source is cited or
  invented.
- choices text respected: YES — each (1)-(4) review line addresses the
  actual stored choice text, not a generic substitute.

## Risk note

- LOW-MEDIUM. The proposed drafts are standard DC-machine theory and the
  conclusion (4) is source-locked. The change replaces a mismatched
  reasoning body rather than a stale phrase, so it is a larger edit than a
  C20 hedge cleanup — but it is bounded to this single item's `solution` /
  `steps`.
- Wording nuance: choices [2]/[3] say "기하학적 중성축" whereas standard
  theory shifts the "전기적(자기적) 중성축". The proposed drafts phrase the
  effect as "중성축 이동" (the choice's intent) without contradicting the
  stored choice text and without rewriting the source-question wording. This
  nuance is noted but not "corrected" — `choices` are not modified.
- Recommend the apply replace the full `solution` string and the `변환` /
  `계산` (and optionally `인식`) `steps` sub-fields, since the reasoning body
  is rewritten rather than patched at a single anchor.

## apply_status

`not_applied`. This dry-run does not modify `app/data`. A separate apply step
with its own approval is required.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `answer` modification.
- No `choices` modification.
- No `solution` / `steps` apply.
- No `solution_svg` modification.
- No app code or schema modification.
- No paid API call.
- No push.
