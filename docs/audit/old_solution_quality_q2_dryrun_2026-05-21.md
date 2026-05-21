# Old Solution Quality — Q2-A Dry-Run Sheet (2026-05-21)

Answer-locked regeneration **drafts** for the 30 C1 pilot candidates. This is a
review sheet only. `app/data/questions.json` and `app/data/questions.v2.json` were
NOT modified. No paid API was used. Nothing was auto-applied.

- Source pilot list: `docs/audit/old_solution_quality_pilot_2026-05-21.md`
- Extractor commit: `832e285`
- Inputs read: `app/data/questions.v2.json`, `app/data/questions.json`

## Critical finding — read before applying

The C1 pilot assumption ("old solution conclusion is wrong, `q.answer` is right")
was established on the **PDF-verified 2025-2026 set** (T3.5 G3). It does **not**
transfer to these pilot items, which are all **1998-2016** questions whose
`q.answer` was never verified against a PDF answer table.

Working each problem from physics/standard theory:

- **8 / 30** — `q.answer` agrees with standard theory; the old solution simply
  mis-concluded (often a value-vs-choice-index confusion). → proposed solution written.
- **22 / 30** — the worked result conflicts strongly with `q.answer` (or the choices
  are OCR-corrupted). For these, `q.answer` itself is suspect. Per the rule
  ("정말 q.answer와 문제/보기 사이 충돌이 강하게 의심되면 needs_source_answer_check"),
  **no proposed solution was written**; route = `needs_source_answer_check`.

Implication: a C1 conclusion mismatch on an unverified old item does NOT mean the
old solution is wrong. Q2 must not blindly answer-lock old items to `q.answer`.

## Summary

| Metric | Count |
| --- | ---: |
| Pilot items | 30 |
| Proposed solution written (`q.answer` confirmed) | 8 |
| `needs_source_answer_check` (excluded, strong conflict / OCR) | 22 |
| High risk | 0 of the 8 written (all low) |
| answer-lock FAIL | 0 of the 8 written |

Proposed-solution items: `2001_1회_21`, `2005_3회_83`, `2006_1회_7`,
`2015_1회_13`, `2015_1회_22`, `2015_3회_27`, `2016_1회_71`, `2016_3회_44`.

---

## Part A — Proposed solutions (8 items, q.answer confirmed)

### A1. `2001_1회_21`

- subject: 전력공학 | q.answer: **2**
- choices: 1) 0.4605 log(D/r)+0.5  2) 0.4605 log(D/r)+0.05  3) 0.4605 log(r/D)+0.5  4) 0.4605 log(r/D)+0.05
- old detected_answer_mentions: [1] | old conclusion: "(1)번으로 추정"
- proposed solution: 가공 송전선 1상당 작용 인덕턴스는 내부 인덕턴스와 외부 인덕턴스의 합이다. 내부 인덕턴스는 도체 내부 자속에 의한 것으로 상수 0.05[mH/km], 외부 인덕턴스는 선간거리 D와 도체 반지름 r의 비에 따라 0.4605 log₁₀(D/r)[mH/km]이다. 따라서 L = 0.05 + 0.4605 log₁₀(D/r)[mH/km]. 로그 인수는 D/r(선간거리÷반지름), 상수항은 0.05이다.
- proposed steps:
  - 인식: 가공 송전선로 1상 작용 인덕턴스 공식을 묻는 문제.
  - 변환: 작용 인덕턴스 = 내부 인덕턴스(상수 0.05) + 외부 인덕턴스(0.4605 log₁₀(D/r)).
  - 계산: L = 0.05 + 0.4605 log₁₀(D/r) [mH/km]. → 정답: 2번.
- answer-lock check: conclusion says q.answer(2) — PASS / no figure dependency — PASS / no invented article number — PASS
- risk note: **low**

### A2. `2005_3회_83`

- subject: 전기설비기술기준 | q.answer: **4**
- choices: 1) 관 끝 터짐 방지  2) 관 단구에서 조영제 접촉 방지  3) 관내 이물질 혼입 방지  4) 관 단구에서 전선 피복 손상 방지
- old detected_answer_mentions: [2] | old conclusion: "정답 4번 (…내용상 (2)번이며 정정 필요)"
- proposed solution: 금속관의 절단면(단구)은 날카로워, 전선이 직접 닿으면 절연 피복이 쓸려 손상될 수 있다. 절연 부싱은 이 관 단구에 끼워 전선 피복을 보호하는 부품이다. 따라서 절연 부싱의 가장 주된 목적은 관의 단구에서 전선 피복의 손상을 방지하는 것이다.
- proposed steps:
  - 인식: 금속관공사에서 절연 부싱의 주된 목적을 묻는 문제.
  - 변환: 금속관 단구는 날카로워 전선 피복이 손상되기 쉽다. 절연 부싱은 단구에 끼우는 보호 부품이다.
  - 계산(판정): 절연 부싱의 주된 목적 = 관 단구에서 전선 피복 손상 방지. → 정답: 4번.
- answer-lock check: conclusion says q.answer(4) — PASS / no figure dependency — PASS / no invented article number — PASS
- risk note: **low**

### A3. `2006_1회_7`

- subject: 전기자기학 | q.answer: **2**
- choices: 1) 0  2) 3  3) 6  4) 10
- old detected_answer_mentions: [3] | old conclusion: "값 3 … 정답 (3)번"
- proposed solution: 발산 div E = ∂Eₓ/∂x + ∂E_y/∂y + ∂E_z/∂z. ∂Eₓ/∂x = 6e³ˣsin5y, ∂E_y/∂y = 5e³ˣsin5y이며 원점에서 sin0 = 0이므로 두 항 모두 0. ∂E_z/∂z = 3e⁴ᶻ(1+4z)이며 z=0에서 3. 따라서 원점의 발산 값은 0+0+3 = 3이다. 보기 중 값 "3"은 2번이다.
- proposed steps:
  - 인식: 주어진 전계 벡터의 발산을 원점에서 구하는 문제.
  - 변환: div E = ∂Eₓ/∂x + ∂E_y/∂y + ∂E_z/∂z. 각 성분을 해당 변수로 편미분한다.
  - 계산: 원점에서 x·y 성분 미분값은 sin0=0으로 0, z 성분 미분값 3e⁴ᶻ(1+4z)는 3. 합 = 3. 보기에서 값 3은 2번. → 정답: 2번.
- answer-lock check: conclusion says q.answer(2) — PASS / no figure dependency — PASS / no invented article number — PASS
- risk note: **low** (구해설은 발산 값 3과 보기번호 3을 혼동했다 — 값 3은 2번 보기)

### A4. `2015_1회_13`

- subject: 전기자기학 | q.answer: **1**
- choices: 1) 6.63×10⁻⁶sin²ω(x-vt)  2) 6.63×10⁻⁶cos²ω(x-vt)  3) 6.63×10⁻⁴sinω(x-vt)  4) 6.63×10⁻⁴cosω(x-vt)
- old detected_answer_mentions: [2] | old conclusion: "정답 2번 (cos²…)"
- proposed solution: 두 직교 전계 성분이 만드는 합성 전계의 크기 제곱은 |E|² = E_y² + E_z² = (3×10⁻²)² + (4×10⁻²)² = 25×10⁻⁴·sin²ω(x-vt). 공기의 고유 임피던스 η₀ ≈ 377[Ω]를 쓰면 포인팅 벡터 크기 S = |E|²/η₀ = 25×10⁻⁴/377·sin²ω(x-vt) ≈ 6.63×10⁻⁶·sin²ω(x-vt)[W/m²]. 시간 함수는 원래 전계와 같은 sin² 형태로 유지된다.
- proposed steps:
  - 인식: 직교하는 두 전계 성분이 만드는 전자파의 포인팅 벡터 크기.
  - 변환: |E|² = E_y² + E_z². 포인팅 벡터 크기 S = |E|²/η₀, 공기 η₀ ≈ 377[Ω].
  - 계산: |E|² = (9+16)×10⁻⁴·sin²ω(x-vt) = 25×10⁻⁴·sin²ω(x-vt). S = 25×10⁻⁴/377·sin² ≈ 6.63×10⁻⁶ sin²ω(x-vt). → 정답: 1번.
- answer-lock check: conclusion says q.answer(1) — PASS / no figure dependency — PASS / no invented article number — PASS
- risk note: **low**

### A5. `2015_1회_22`

- subject: 전력공학 | q.answer: **1**
- choices: 1) 직렬리액턴스를 증가  2) 전압변동을 억제  3) 중간 조상방식 채용  4) 고장전류를 줄이고 고장구간 신속 차단
- old detected_answer_mentions: [4] | old conclusion: "정답 (4) (…1번이라 표기했으나 (4)번)"
- proposed solution: 정태 안정 극한 전력은 P_max = (V_s·V_r/X)·sinδ로, 직렬 리액턴스 X에 반비례한다. 안정도 향상책은 X를 줄이는 방향이다. "직렬 리액턴스를 증가시킨다"는 X를 키워 P_max를 낮추므로 안정도를 오히려 악화시킨다 — 안정도 향상 방법이 아니다. 나머지 보기(전압변동 억제, 중간 조상, 고속 차단)는 모두 표준적 향상책이다.
- proposed steps:
  - 인식: 송전계통 안정도 향상 방법이 "아닌 것"을 고르는 문제.
  - 변환: P_max = (V_s·V_r/X)·sinδ. 안정도는 직렬 리액턴스 X에 반비례.
  - 계산(판정): 직렬 리액턴스 증가 → X↑ → P_max↓ → 안정도 악화 → 향상 방법 아님. → 정답: 1번.
- answer-lock check: conclusion says q.answer(1) — PASS / no figure dependency — PASS / no invented article number — PASS
- risk note: **low**

### A6. `2015_3회_27`

- subject: 전력공학 | q.answer: **3**
- choices: 1) 속응 여자방식 채택  2) 고속도 재폐로 방식 채용  3) 발전기·변압기 리액턴스를 크게  4) 고장전류 줄이고 고속도 차단
- old detected_answer_mentions: [4] | old conclusion: "정답 4번"
- proposed solution: 안정 극한 전력은 계통의 직렬 리액턴스에 반비례한다. 발전기·변압기의 리액턴스를 크게 하면 직렬 리액턴스가 늘어 안정도가 나빠진다 — 안정도 증진 방법이 아니다. 속응 여자방식, 고속도 재폐로, 고속 차단은 모두 표준 증진책이다.
- proposed steps:
  - 인식: 송전계통 안정도 증진 방법이 "아닌 것"을 고르는 문제.
  - 변환: 안정 극한 전력은 직렬 리액턴스에 반비례. 증진책은 리액턴스를 줄이는 방향.
  - 계산(판정): 발전기·변압기 리액턴스를 크게 하면 안정도 악화 → 증진 방법 아님. → 정답: 3번.
- answer-lock check: conclusion says q.answer(3) — PASS / no figure dependency — PASS / no invented article number — PASS
- risk note: **low**

### A7. `2016_1회_71`

- subject: 제어공학(회로이론) | q.answer: **3**
- choices: 1) E_l = √3·E_p  2) E_l = 3E_p  3) E_l = E_p  4) E_l = E_p/√3
- old detected_answer_mentions: [1] | old conclusion: "E_l = E_p … 정답 (1)번"
- proposed solution: 평형 3상 Δ(삼각)결선에서는 세 상권선이 삼각형으로 닫혀 각 상권선이 두 선 사이에 직접 놓인다. 따라서 선간전압이 곧 상전압이며 E_l = E_p이다. (전류는 반대로 선전류 = √3 × 상전류.)
- proposed steps:
  - 인식: 평형 3상 Δ결선에서 선간전압과 상전압의 관계.
  - 변환: Δ결선은 상권선이 두 선 사이에 직접 연결된다.
  - 계산: E_l = E_p. → 정답: 3번.
- answer-lock check: conclusion says q.answer(3) — PASS / no figure dependency — PASS / no invented article number — PASS
- risk note: **low** (구해설은 E_l=E_p로 옳게 풀고도 보기번호를 "1번"으로 잘못 적었다 — E_l=E_p는 3번 보기)

### A8. `2016_3회_44`

- subject: 전기기기 | q.answer: **4**
- choices: 1) 유도시험  2) 단락시험  3) 부하시험  4) 무부하시험
- old detected_answer_mentions: [1] | old conclusion: "무부하 시험 … 정답 1번"
- proposed solution: 변압기 철손은 철심의 히스테리시스손과 와전류손으로, 전압·주파수에만 의존하고 부하와 무관한 무부하손이다. 정격전압을 걸고 2차를 개방한 무부하시험(개방회로시험)에서는 전류가 작아 동손이 무시되므로 입력전력이 곧 철손이 된다. (동손은 단락시험에서 측정.)
- proposed steps:
  - 인식: 변압기 철손을 측정하는 시험의 종류.
  - 변환: 철손은 무부하손으로 정격전압·무부하 상태에서 측정한다.
  - 계산(판정): 무부하시험(2차 개방, 정격전압 인가)의 입력전력 = 철손. → 정답: 4번.
- answer-lock check: conclusion says q.answer(4) — PASS / no figure dependency — PASS / no invented article number — PASS
- risk note: **low** (구해설은 "무부하 시험"으로 옳게 풀고도 보기번호를 "1번"으로 잘못 적었다 — 무부하시험은 4번 보기)

---

## Part B — needs_source_answer_check (22 items, no proposed solution)

For every item below, the worked result conflicts strongly with `q.answer`, or the
choices are OCR-corrupted. No proposed solution was written. Route =
`needs_source_answer_check`. These must NOT be answer-locked to `q.answer` without
a verified source answer (PDF answer table). All are excluded from the apply set.

| key | subject | q.answer | old mentions | conflict reason (worked result) |
| --- | --- | ---: | --- | --- |
| `1998_4회_10` | 전기자기학 | 1 | [4] | 경계조건(B 법선 연속·H 접선 연속) → B₂=μ₀(4aₓ-8a_y+8a_z) = 보기 4. q.answer=1 강한 충돌. |
| `2001_1회_68` | 제어공학 | 1 | [3] | 포물선 입력의 lim s²GH = 가속도 오차 상수 = 보기 3. q.answer=1(위치 오차 상수) 충돌. |
| `2001_3회_41` | 전기기기 | 2 | [4] | "옳지 않은 것" = 철손 증가(무부하손, 부하 무관) = 보기 4. q.answer=2(여자전류 불변=참) 충돌. |
| `2001_3회_43` | 전기기기 | 1 | [2] | 보기 본문이 OCR 심하게 손상("3자 권선","승압콘","3도분만 젬에") — 판정 불가. |
| `2002_1회_32` | 전력공학 | 1 | [2] | 보기 1이 OCR 깨짐("} \\end{table}") — q.answer가 판독 불가 보기를 가리킴. |
| `2002_3회_4` | 전기자기학 | 2 | [4] | 보기 2는 차원상 전위가 아닌 전계 형태. 점전하 중첩 전위형은 보기 4. q.answer=2 충돌. |
| `2006_1회_6` | 전기자기학 | 4 | [3] | 유전체 발열량 = 0.24·CV²t/(ρε)(V 제곱) = 보기 3. q.answer=4(CVt, V 1제곱) 차원 충돌. |
| `2006_2회_27` | 전력공학 | 3 | [4] | 제수문은 취수량/유량 조정·차단용 = 보기 4. 모래 배제는 침사지 기능. q.answer=3 충돌. |
| `2007_1회_9` | 전기자기학 | 4 | [2] | A·B = 1+3a = 0 → a = -1/3 = 보기 2. q.answer=4(1/2) 충돌. |
| `2007_2회_64` | 회로이론 | 2 | [1] | Routh 제1열(1,2,3,8/3,2) 전부 양수 → 안정 = 보기 1. q.answer=2(불안정) 충돌. |
| `2014_2회_50` | 전기기기 | 3 | [2] | V곡선 = 출력 일정 시 계자전류-전기자전류 관계(보기 1/2). q.answer=3(계자전류 일정)은 V곡선 정의와 반대. |
| `2014_3회_62` | 회로이론 | 4 | [1] | 단위계단함수 라플라스변환 = 1/s. q.answer=4는 라플라스변환을 s로 표기 — 오류. 보기 z변환부도 표준형(z/(z-1)) 불일치, OCR 손상 의심. |
| `2015_1회_71` | 전기자기학 | 4 | [1,1] | L=Nφ/I=2000·0.06/10=12H, τ=L/R=12/12=1s = 보기 1. q.answer=4(0.001) 충돌. |
| `2015_1회_87` | 전기설비기술기준 | 3 | [2] | 백열전등·방전등 옥내전로 대지전압 300V 이하 = 보기 2. q.answer=3(350) 충돌. |
| `2015_2회_23` | 전력공학 | 3 | [4] | π형 송전단전류 I_s = Y(1+ZY/4)E_r+(1+ZY/2)I_r = 보기 4. q.answer=3(보정항 누락) 충돌. |
| `2015_2회_29` | 전력공학 | 1 | [2] | 이상전압 파고치 저감·기기 보호 = 피뢰기 = 보기 2(보기 2가 "피뢰기" 명시). q.answer=1(직렬리액터) 충돌. |
| `2015_3회_22` | 전력공학 | 4 | [1] | 변압기 제3고조파 제거 = △결선 = 보기 1. q.answer=4(전력용 콘덴서) 충돌. |
| `2015_3회_25` | 전력공학 | 1 | [4] | 보기 4가 OCR 깨짐. "반한시·정한시 특성"을 묻는데 q.answer=1(반한시 단독) — 보기 손상으로 판정 불가. |
| `2016_1회_44` | 전기기기 | 2 | [4] | 보기 2·4 표현이 모호(OCR "굽은 회전방향", 전기적/기하학적 중성축 혼용) — 신뢰 판정 곤란. |
| `2016_1회_69` | 전력공학(제어) | 1 | [4] | 위상여유·이득여유는 직접 안정도 척도. 안정도와 가장 관계 적은 것은 고유주파수 = 보기 4. q.answer=1(공진치) 충돌. |
| `2016_1회_70` | 제어공학 | 2 | [4] | Nyquist 임계점 -1+j0 → 0dB, ±180° = 보기 4. q.answer=2(-90°) 충돌. |
| `2016_3회_21` | 전력공학 | 1 | [4] | 손실률 일정 시 전선 단면적 A ∝ 1/V²(전압 제곱 반비례) = 보기 4. q.answer=1(전류 비례) 충돌. |

risk note (Part B 공통): proposed solution 미작성, route `needs_source_answer_check`,
**apply 후보에서 제외**. q.answer 자체가 PDF 답안표 등 (a) 출처로 재검증되기 전에는
answer-lock 재생성 금지.

---

## Verdict

- 30건 중 proposed solution 작성 **8건** (전부 answer-lock 3-check PASS, risk low).
- `needs_source_answer_check` 제외 **22건** (강한 충돌 18건 + OCR 손상 4건).
- high risk **0건**, answer-lock FAIL **0건**.
- Q2 본적용 후보는 현재 **8건뿐**이며, 22건은 q.answer 소스 재검증(별도 트랙)이 선행되어야 한다.
- 본 시트 작성 중 `app/data/questions.json` / `questions.v2.json` 미수정 (read-only).
