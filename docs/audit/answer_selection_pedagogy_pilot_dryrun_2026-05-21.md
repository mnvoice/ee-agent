# Answer-Selection Pedagogy Pilot — Solution Dry-run (2026-05-21)

Solution dry-run for the 7 answer-selection pedagogy pilot items. For each
item this document drafts a "reason-toward-the-answer" `solution` / `steps`
and checks the draft against the quality gate. The purpose is to validate
that the pedagogy structure fits real questions before any apply.

This is a **dry-run document only**. It does NOT modify `app/data` and is not
an approval to apply. `apply_status` = `not_applied` for every item.

- Base commit: `0ff1f31` (docs: design answer selection pedagogy track)
- Design parent: `docs/audit/answer_selection_pedagogy_track_design_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## Choice-OCR observation (surfaced before the drafts)

The pedagogy design assumed the 7 pilot items had "intact choices". On a
direct read, 4 of the 7 carry minor `choices` OCR residue / typos. None is
answer-corrupting — the answer-relevant meaning is readable — but they are
real choice-text defects:

- `2001_3회_41` choice [3]: `운도가 상승한다` → evidently `온도가 상승한다`.
- `2006_2회_27` choice [2]: `충수위를 낮추기` → evidently `홍수위를 낮추기`;
  choice [3]: `모래를 베제하기` → evidently `모래를 배제하기`.
- `2016_3회_21` choice [4]: trailing LaTeX residue
  (`… \begin{table}\captionsetup{labelformat=empty}\caption{`).
- `2015_3회_22` choice [4]: trailing page-footer residue (`… D-60 전기기사`).

The drafts below reference the actual stored choices and describe the
evident meaning. `choices` are NOT modified here. Recommendation in the
summary: a small choice-cleanup pass for these 4 items before the pedagogy
apply, OR proceed with evident-meaning description — a supervisor decision.

---

## Item 1 — `2007_1회_9`

- subject: 전기자기학 / current_answer: 4 → wait — current_answer: **2**
- current choices: [1] -2 / [2] -1/3 / [3] 0 / [4] 1/2
- existing solution/steps status: C20-2 corrected (4→2); `solution` /
  `steps` already conclude (2)번; `solution_svg` is an illustrative vector
  diagram.

### pedagogical solution draft

- 핵심 개념: 두 벡터가 수직이면 내적(dot product)이 0이다.
- 문제에서 봐야 할 단서: "수직이 되기 위한" — 내적 = 0 조건을 세우라는 신호.
- 보기 판단 / 오답 제거: A·B = 1+3a. [1] a=−2 → 1−6=−5≠0. [2] a=−1/3 →
  1−1=0 ✓. [3] a=0 → 1≠0. [4] a=1/2 → 1+1.5≠0. 0을 만드는 것은 [2]뿐.
- 정식 근거 또는 계산: A=(1,−1,3), B=(1,0,a). A·B = AxBx+AyBy+AzBz =
  1·1 + (−1)·0 + 3·a = 1+3a = 0 → a = −1/3.
- 흔한 함정: j 성분의 −1에 끌려 부호를 잘못 곱하기 쉽다. B의 j 성분이 0이라
  y항(−1·0)은 기여가 없다.
- 다른 과목 연결: 제어/신호의 직교성 판정도 내적 = 0으로 같다.
- 시험장 빠른 판별법: 1+3a=0만 풀면 끝. 분수 답(−1/3)이 유력 후보.
- 최종 정답: 2번 (a = −1/3).

### proposed steps draft

- 인식: 두 벡터의 수직 여부를 묻는 내적 문제.
- 변환: A⊥B ⇔ A·B = 0. A=(1,−1,3), B=(1,0,a).
- 계산: A·B = 1·1 + (−1)·0 + 3·a = 1+3a = 0 → a = −1/3. 정답 ②.

### quality checks

- answer matches q.answer: YES (2). ✓
- every choice explanation maps to actual choices: YES ([1]-[4] all). ✓
- no invented source/article/statute: YES (pure vector algebra). ✓
- no unsupported cross-subject claim: YES (직교성 link is standard). ✓
- no contradiction with source answer: YES. ✓
- concise enough for UI: YES (each element 1-2 lines). ✓

### risk note

Low. Clean computation item; choices [1]-[4] intact.

`apply_status`: not_applied.

---

## Item 2 — `2007_2회_64`

- subject: 회로이론 / current_answer: 1
- current choices: [1] 안정 / [2] 불안정 / [3] 조건부 안정 / [4] 임계 상태
- existing solution/steps status: C20-2 corrected (2→1); C20-2 solution
  cleanup completed the truncated steps; `solution` / `steps` conclude (1)번.

### pedagogical solution draft

- 핵심 개념: Hurwitz 안정 판별 — 모든 계수가 양수이고 모든 Hurwitz
  행렬식이 양수이면 안정.
- 문제에서 봐야 할 단서: "훌비쯔의 안정 조건으로 판별" — Hurwitz 행렬식을
  구성하라는 직접 지시.
- 보기 판단 / 오답 제거: 계수 a₀=1,a₁=2,a₂=5,a₃=4,a₄=2 모두 양수;
  D₁=2, D₂=6, D₃=16, D₄=32 모두 양수 → [1] 안정. [2] 불안정은 행렬식에
  음수가 있을 때, [4] 임계 상태는 행렬식에 0이 있을 때 — 여기엔 둘 다 없다.
  [3] 조건부 안정은 Hurwitz 판별의 결과 범주가 아니다.
- 정식 근거 또는 계산: D₁=a₁=2. D₂=a₁a₂−a₀a₃=10−4=6. D₃=16.
  D₄=a₄·D₃=32. 전부 > 0.
- 흔한 함정: 계수가 모두 양수인 것만 보고 끝내면 안 된다 — 그것은 필요조건일
  뿐, 행렬식까지 확인해야 충분조건이 된다.
- 다른 과목 연결: 제어공학의 Routh-Hurwitz 안정 판별과 동일한 방법 —
  회로이론·제어공학 공통.
- 시험장 빠른 판별법: 계수가 전부 양수이면 일단 안정 후보. 4차는
  D₂=a₁a₂−a₀a₃만 빠르게 확인해 양수이면 대체로 안정.
- 최종 정답: 1번 (안정).

### proposed steps draft

- 인식: 특성방정식 + Hurwitz → 안정 판별 문제.
- 변환: 안정 조건 = 모든 계수 > 0 AND 모든 Hurwitz 행렬식 Dₖ > 0.
- 계산: a₀~a₄ 전부 양수; D₁=2, D₂=10−4=6, D₃=16, D₄=32 전부 양수 →
  안정. 정답 ①.

### quality checks

- answer matches q.answer: YES (1). ✓
- every choice explanation maps to actual choices: YES. ✓
- no invented source/article/statute: YES (standard Hurwitz criterion). ✓
- no unsupported cross-subject claim: YES (Routh-Hurwitz link is standard). ✓
- no contradiction with source answer: YES. ✓
- concise enough for UI: YES. ✓

### risk note

Low. Choices [1]-[4] intact. The cross-subject link is a genuine identity.

`apply_status`: not_applied.

---

## Item 3 — `2001_3회_41`

- subject: 전기기기 / current_answer: 4
- current choices: [1] 동손이 증가한다. / [2] 여자 전류는 변함없다. /
  [3] `운도가 상승한다.` (OCR typo for `온도가 상승한다.`) /
  [4] 철손이 증가한다.
- existing solution/steps status: C20-1 corrected (2→4); `solution` /
  `steps` already conclude (4)번; no `solution_svg`.

### pedagogical solution draft

- 핵심 개념: 변압기 손실 분리 — 동손은 부하손(I²R, 부하전류²에 비례),
  철손은 무부하손(1차 전압·주파수에만 의존).
- 문제에서 봐야 할 단서: "부하가 증가할 때" + "옳지 않은 것" — 부하에 따라
  변하는 것과 변하지 않는 것을 구분하라는 신호.
- 보기 판단 / 오답 제거: [1] 동손은 부하전류²에 비례 → 부하↑면 증가:
  옳은 설명. [2] 여자 전류는 1차 전압·주파수로 정해져 부하와 무관 → 변함
  없음: 옳은 설명. [3] 온도는 손실 증가로 상승: 옳은 설명. [4] 철손은
  무부하손이라 부하와 무관하게 일정 → "증가한다"는 틀린 설명: 정답.
- 정식 근거 또는 계산: 철손 = 히스테리시스손 + 와류손이며 1차 전압·주파수의
  함수일 뿐 부하전류 항이 없다. 동손 = I²R로 부하전류에 의존.
- 흔한 함정: "부하 증가 → 모든 손실 증가"로 뭉뚱그리면 철손까지 증가한다고
  오해한다. 철손은 무부하손이다.
- 다른 과목 연결: 전력공학 변압기 효율 계산에서도 철손=무부하손 /
  동손=부하손 구분이 그대로 쓰인다.
- 시험장 빠른 판별법: "부하와 무관한 것"을 먼저 찾는다 — 철손과 여자 전류.
  [2](여자 전류 불변)는 옳은 설명이므로, "틀린 것"은 [4](철손 증가).
- 최종 정답: 4번 (철손은 부하와 무관 — "증가한다"가 틀림).

### proposed steps draft

- 인식: "부하 증가" 시 변압기 손실·특성 변화를 묻는, 옳지 않은 보기 찾기.
- 변환: 동손 ∝ 부하전류² (부하손) / 철손 = 무부하손 (전압·주파수 의존) /
  여자 전류 = 1차 전압·주파수 의존 / 온도 ∝ 총손실.
- 계산: [1] 동손↑ 참, [2] 여자 전류 불변 참, [3] 온도↑ 참, [4] 철손↑
  거짓(무부하손, 부하 무관). 옳지 않은 것 = ④.

### quality checks

- answer matches q.answer: YES (4). ✓
- every choice explanation maps to actual choices: YES — choice [3] is
  referenced as its evident meaning 온도 상승 (stored text has the OCR typo
  "운도"). ✓ (see risk note)
- no invented source/article/statute: YES (standard transformer loss
  theory). ✓
- no unsupported cross-subject claim: YES. ✓
- no contradiction with source answer: YES. ✓
- concise enough for UI: YES. ✓

### risk note

Low-medium. Choice [3] stored text has a minor OCR typo ("운도" → "온도");
the meaning is unambiguous and does not affect answer reasoning. Flagged for
the choice-cleanup decision (Summary). `choices` not modified here.

`apply_status`: not_applied.

---

## Item 4 — `2006_2회_27`

- subject: 전력공학 / current_answer: 4
- current choices: [1] 낙차를 높이기 위하여 / [2] `충수위를 낮추기 위하여`
  (OCR typo for `홍수위`) / [3] `모래를 베제하기 위하여` (OCR typo for
  `배제`) / [4] 유량을 조정하기 위하여
- existing solution/steps status: C20-2 corrected (3→4); C20-2 solution
  cleanup removed a fabricated "정답 없음" claim; `solution` / `steps`
  conclude ④; no `solution_svg`.

### pedagogical solution draft

- 핵심 개념: 수력발전 취수설비의 기능 구분 — 제수문(취수문)은 취수구에서
  물의 유입량(유량)을 조절·차단하는 수문.
- 문제에서 봐야 할 단서: "제수문" + "주된 목적" — 다른 취수설비와 기능을
  구별하라는 신호.
- 보기 판단 / 오답 제거: [1] 낙차는 댐 높이로 정해지며 제수문과 무관:
  오답. [2] 홍수위 조절은 방수로(spillway)의 역할: 오답. [3] 모래 배제는
  침사지·모래제거 설비의 역할: 오답. [4] 제수문은 물의 유입량(유량)을
  조절·차단: 정답.
- 정식 근거 또는 계산: 제수문 = 취수구 수로를 여닫아 취수량을 조절하거나
  물의 유입을 차단하는 수문. (계산 없는 개념 문항.)
- 흔한 함정: 취수구 주변 여러 설비(방수로·침사지)의 기능을 제수문 하나에
  혼동한다 — 각 설비는 역할이 다르다.
- 다른 과목 연결: (강한 교차 연결 없음 — 생략.)
- 시험장 빠른 판별법: 제수문의 "문(門)"은 물길을 여닫는 것 → 유량 조정.
  나머지 보기는 각각 다른 설비가 담당.
- 최종 정답: 4번 (유량을 조정하기 위하여).

### proposed steps draft

- 인식: 취수설비 "제수문"의 기능을 다른 설비와 구별하는 개념 문항.
- 변환: 제수문 = 유량 조절·유입 차단 / 방수로 = 홍수 시 과잉수 배출 /
  침사지 = 모래 배제 / 낙차 = 댐 높이로 결정.
- 계산: [1] 낙차·[2] 홍수위·[3] 모래 배제는 각각 다른 설비의 역할 →
  오답. [4] 유량 조정 = 제수문의 주목적 → 정답 ④.

### quality checks

- answer matches q.answer: YES (4). ✓
- every choice explanation maps to actual choices: YES — choices [2]/[3]
  referenced as evident meaning (홍수위 / 배제); stored text has OCR typos. ✓
  (see risk note)
- no invented source/article/statute: YES. ✓
- no unsupported cross-subject claim: YES (cross-subject element omitted as
  none is genuinely strong). ✓
- no contradiction with source answer: YES. ✓
- concise enough for UI: YES. ✓

### risk note

Low-medium. Choices [2] ("충수위"→"홍수위") and [3] ("베제"→"배제") have
minor OCR typos; meaning is unambiguous and does not affect answer reasoning.
Flagged for the choice-cleanup decision (Summary). `choices` not modified.

`apply_status`: not_applied.

---

## Item 5 — `2016_1회_70`

- subject: 제어공학 / current_answer: 4
- current choices: [1] 1[dB], 0° / [2] 0[dB], -90° / [3] 0[dB], 90° /
  [4] 0[dB], -180°
- existing solution/steps status: C20-4 corrected (2→4); C20-4 solution
  cleanup removed stale hedges and made the conclusion explicit ④; no
  `solution_svg`.

### pedagogical solution draft

- 핵심 개념: 복소수를 극형식으로 — 점 −1은 크기 1, 위상 ±180°. 보드선도의
  이득 = 20log|G|, 위상 = ∠G.
- 문제에서 봐야 할 단서: "임계점 (−1, j0)" — 복소평면의 점 −1을 크기와
  위상으로 바꾸라는 신호.
- 보기 판단 / 오답 제거: |−1| = 1 → 이득 = 20log₁₀(1) = 0[dB].
  ∠(−1) = ±180°. [1] 이득이 1dB라 틀림. [2] 위상 −90°(= −j)라 틀림.
  [3] 위상 90°(= +j)라 틀림. [4] 0[dB], −180° — 크기·위상 모두 일치:
  정답.
- 정식 근거 또는 계산: −1 = 1∠180° = 1∠−180°. Gain[dB] = 20log₁₀(1) = 0,
  Phase = ±180°.
- 흔한 함정: |−1|을 −1로 보고 이득을 음수로 계산하거나, 위상을 ±90°와
  혼동한다.
- 다른 과목 연결: Nyquist 안정 판별의 임계점이 곧 보드선도의 0dB·−180°
  지점 — 두 선도가 같은 안정 한계를 표현한다.
- 시험장 빠른 판별법: −1 → 크기 1(= 0dB)은 즉시. 위상은 실수축 음의 방향
  → ±180°. "0dB, −180°" 보기를 고른다.
- 최종 정답: 4번 (0[dB], −180°).

### proposed steps draft

- 인식: Nyquist 임계점 (−1,j0)을 보드선도의 이득·위상으로 변환하는 문제.
- 변환: 점 −1을 극형식으로 — |−1|=1, ∠(−1)=±180°.
  Gain[dB]=20log₁₀|G|, Phase=∠G.
- 계산: Gain = 20log₁₀(1) = 0[dB], Phase = ±180°. 정답 ④ (0[dB], −180°).

### quality checks

- answer matches q.answer: YES (4). ✓
- every choice explanation maps to actual choices: YES. ✓
- no invented source/article/statute: YES (complex-number / Bode
  definitions). ✓
- no unsupported cross-subject claim: YES (Nyquist↔Bode is the same
  control-theory topic). ✓
- no contradiction with source answer: YES. ✓
- concise enough for UI: YES. ✓

### risk note

Low. Choices [1]-[4] intact.

`apply_status`: not_applied.

---

## Item 6 — `2016_3회_21`

- subject: 전력공학 / current_answer: 4
- current choices: [1] 전류에 비례한다. / [2] 전류에 반비례한다. /
  [3] 전압의 제곱에 비례한다. / [4] `전압의 제곱에 반비례한다.` (stored
  text has trailing LaTeX residue after the sentence)
- existing solution/steps status: C20-4 corrected (1→4); C20-4 solution
  cleanup fixed the steps' wrong conclusion to ④; no `solution_svg`.

### pedagogical solution draft

- 핵심 개념: 두 일정 조건을 연립한다 — 전력 일정 → I ∝ 1/V; 손실 일정 →
  I²R 일정 → R ∝ V²; 전선 단면적 A ∝ 1/R.
- 문제에서 봐야 할 단서: "전력, 손실률 … 일정" — 두 일정 조건을 동시에
  쓰라는 신호.
- 보기 판단 / 오답 제거: P=√3·V·I·cosθ 일정 → I ∝ 1/V. 손실 3I²R 일정 →
  R ∝ 1/I² ∝ V². A = ρl/R → A ∝ 1/R ∝ 1/V². [3] 전압² 비례는 부호가
  반대라 오답. [1]/[2] 전류 비례·반비례는 A ∝ I²이지 A ∝ I가 아니며,
  물음의 기준은 전압이므로 오답. [4] 전압² 반비례: 정답.
- 정식 근거 또는 계산: I ∝ 1/V (전력 일정), R ∝ V² (손실 일정),
  A ∝ 1/R ∝ 1/V².
- 흔한 함정: A ∝ I²까지 구하고 "전류에 비례"라고 답하기 쉽다 — I²를 I로
  착각하고, 물음의 기준이 전압임을 놓치는 것이다.
- 다른 과목 연결: 송전 전압을 높이면 전선이 가늘어진다 — 고전압 송전의
  경제성 근거.
- 시험장 빠른 판별법: "전압을 올리면 전류가 줄고 전선이 가늘어진다"는 정성
  결론을 떠올리면 → 전압의 제곱에 반비례.
- 최종 정답: 4번 (전압의 제곱에 반비례).

### proposed steps draft

- 인식: 송전 조건(거리·전력·손실률·역률)이 일정할 때 전선 굵기를 구하는
  문제.
- 변환: P=√3·V·I·cosθ 일정 → I ∝ 1/V. 손실 3I²R 일정 → R ∝ V².
  A=ρl/A 관계에서 A ∝ 1/R.
- 계산: A ∝ 1/R ∝ 1/V². 전선의 굵기는 전압의 제곱에 반비례 → 정답 ④.

### quality checks

- answer matches q.answer: YES (4). ✓
- every choice explanation maps to actual choices: YES — choice [4]
  referenced by its sentence ("전압의 제곱에 반비례한다"); the trailing LaTeX
  residue is ignored. ✓ (see risk note)
- no invented source/article/statute: YES (derivation from given
  relations). ✓
- no unsupported cross-subject claim: YES. ✓
- no contradiction with source answer: YES. ✓
- concise enough for UI: YES. ✓

### risk note

Low-medium. Choice [4] stored text carries trailing LaTeX residue
(`\begin{table}\captionsetup…`) after the sentence; the choice sentence
itself is intact. Flagged for the choice-cleanup decision (Summary).
`choices` not modified.

`apply_status`: not_applied.

---

## Item 7 — `2015_3회_22`

- subject: 전력공학 / current_answer: 1
- current choices: [1] 변압기를 △ 결선한다. / [2] 동기조상기를 설치한다. /
  [3] 직렬 리액터를 설치한다. / [4] `전력용 콘덴서를 설치한다.` (stored
  text has trailing footer residue `D-60 전기기사`)
- existing solution/steps status: C20-3 corrected (4→1); `solution` /
  `steps` already conclude (1)번; `solution_svg` is an illustrative
  △-connection diagram.

### pedagogical solution draft

- 핵심 개념: 제3고조파(및 3의 배수 고조파)는 영상분(zero-sequence)으로 3상이
  동위상이다. △결선 폐회로 안에서 순환·상쇄되어 외부 선로로 나가지 않는다.
- 문제에서 봐야 할 단서: "제3고조파 제거" + "변압기" — 변압기 결선 방식으로
  답을 찾으라는 신호.
- 보기 판단 / 오답 제거: [1] △결선: 3고조파가 △ 폐회로 내 순환·상쇄 →
  제거: 정답. [2] 동기조상기: 무효전력 보상(역률 개선)용 — 고조파 제거가
  아님: 오답. [3] 직렬 리액터: 제5고조파 제거용(전력용 콘덴서와 함께 씀) —
  제3고조파용이 아님: 오답. [4] 전력용 콘덴서: 역률 개선용: 오답.
- 정식 근거 또는 계산: 3의 배수 고조파 = 영상분, 3상 동위상 → △ 폐회로에서
  합 = 0. (계산 없는 개념 문항.)
- 흔한 함정: "직렬 리액터 = 고조파 제거"로 외워두고 제3고조파에도 적용한다 —
  직렬 리액터는 제5고조파용이다.
- 다른 과목 연결: 전기기기의 변압기 Y/△ 결선 고조파 특성과 같은 원리 —
  △결선이 3고조파의 순환 통로.
- 시험장 빠른 판별법: "제3고조파 = △결선", "제5고조파 = 직렬 리액터"로 짝을
  외운다. 변압기 + 제3고조파 → △결선.
- 최종 정답: 1번 (변압기를 △ 결선한다).

### proposed steps draft

- 인식: 변압기 유기기전력의 제3고조파 제거 방법을 묻는 개념 문항.
- 변환: 제3고조파 = 영상분(3상 동위상). △결선 폐회로 내 순환·상쇄 /
  동기조상기·전력용 콘덴서 = 역률 개선 / 직렬 리액터 = 제5고조파용.
- 계산: [1] △결선만이 3고조파를 폐회로에서 상쇄 → 정답 ①. [2]/[3]/[4]는
  고조파(특히 3고조파) 제거 수단이 아님.

### quality checks

- answer matches q.answer: YES (1). ✓
- every choice explanation maps to actual choices: YES — choice [4]
  referenced by its sentence ("전력용 콘덴서를 설치한다"); trailing footer
  residue ignored. ✓ (see risk note)
- no invented source/article/statute: YES (harmonic / connection theory). ✓
- no unsupported cross-subject claim: YES (Y/△ harmonic link is standard). ✓
- no contradiction with source answer: YES. ✓
- concise enough for UI: YES. ✓

### risk note

Low-medium. Choice [4] stored text carries trailing footer residue
("D-60 전기기사"); the choice sentence itself is intact. Flagged for the
choice-cleanup decision (Summary). `choices` not modified.

`apply_status`: not_applied.

---

## Summary

| key | subject | answer | quality gate | choice-OCR flag | apply_status |
| --- | --- | ---: | --- | --- | --- |
| `2007_1회_9` | 전기자기학 | 2 | pass | none | not_applied |
| `2007_2회_64` | 회로이론 | 1 | pass | none | not_applied |
| `2001_3회_41` | 전기기기 | 4 | pass | [3] "운도"→"온도" | not_applied |
| `2006_2회_27` | 전력공학 | 4 | pass | [2] "충수위"→"홍수위", [3] "베제"→"배제" | not_applied |
| `2016_1회_70` | 제어공학 | 4 | pass | none | not_applied |
| `2016_3회_21` | 전력공학 | 4 | pass | [4] trailing LaTeX residue | not_applied |
| `2015_3회_22` | 전력공학 | 1 | pass | [4] trailing footer residue | not_applied |

- The pedagogy structure (8 elements + `인식`/`변환`/`계산` steps) fits all 7
  items: every item produced a complete, concise, answer-locked draft.
- All 7 drafts pass the quality gate (answer match, choice mapping, no
  invented source, no unsupported cross-subject claim, no source
  contradiction, UI-concise).
- 4 of 7 items carry minor `choices` OCR residue / typos (not
  answer-corrupting). Recommendation — a supervisor decision: either (a) run
  a small choice-cleanup pass for `2001_3회_41`, `2006_2회_27`,
  `2016_3회_21`, `2015_3회_22` (choices-only, like the R3 choice-OCR
  recovery) before the pedagogy apply, or (b) accept the choices as-is and
  let the pedagogy `solution` describe the evident meaning. Option (a) is
  cleaner; option (b) is faster.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `solution` / `steps` apply.
- No `answer` / `choices` modification.
- No app code or schema modification.
- No paid API call.
- No push.

## Status

- Pilot solution dry-run complete for all 7 candidates; the pedagogy
  structure is validated against real questions.
- No `app/data` modification.
- Next (separate approval): a supervisor decision on the choice-OCR cleanup,
  then a limited pedagogy `solution` / `steps` apply with its own approval.
