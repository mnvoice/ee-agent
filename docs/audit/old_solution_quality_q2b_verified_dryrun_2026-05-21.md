# Old Solution Quality — Q2-B Verified Dry-Run Sheet (2026-05-21)

Answer-locked regenerated solution **drafts** for the 4 `source_answer_verified`
items from the first manual source review. This is a review sheet only.
`app/data/questions.json` and `app/data/questions.v2.json` were NOT modified.
No paid API was used. Nothing was auto-applied. Q2 apply remains BLOCKED.

## Reference commits

- `4317aea` — docs: fill source answers for first 10 review-pack items
- `33c8fcf` — docs: record first source review routing

## Inputs

- Review pack: `docs/audit/old_answer_manual_source_review_pack_2026-05-21.md`
- Routing summary: `docs/audit/old_answer_manual_source_review_routing_2026-05-21.md`
- Q2-A dry-run (reused drafts): `docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`

## Scope — 4 verified items only

| key | subject | q.answer | source_answer | source verdict | Q2-A draft |
| --- | --- | ---: | ---: | --- | --- |
| `2001_1회_21` | 전력공학 | 2 | 2 | `source_answer_verified` | reused (A1) |
| `2002_1회_32` | 전력공학 | 1 | 1 | `source_answer_verified` | new (was Q2-A Part B) |
| `2005_3회_83` | 전기설비기술기준 | 4 | 4 | `source_answer_verified` | reused (A2) |
| `2006_1회_7` | 전기자기학 | 2 | 2 | `source_answer_verified` | reused (A3) |

The 6 `source_answer_conflict` items are out of scope for this sheet and are not
touched here.

Premise for every item below: `source_answer == q.answer`, confirmed by the
PDF 【답】 marker during manual source review. The drafts are answer-locked to
this verified answer.

---

## Drafts

### 1. `2001_1회_21`

- key: `2001_1회_21`
- q.answer: **2**
- source_answer: **2**
- source_page: 2
- source verdict: `source_answer_verified`
- old solution issue: Q2-A dry-run A1 기록 — 구해설 결론이 "(1)번으로 추정"으로
  보기번호를 잘못 적었다 (detected_answer_mentions=[1]). 공식 전개 자체는 2번을
  가리킨다. Q2-A 시점에는 q.answer가 PDF 미검증 상태였으나, source review에서
  PDF p.2 풀이의 【답】②로 q.answer=2가 확정되었다.
- proposed solution draft: 가공 송전선 1상당 작용 인덕턴스는 내부 인덕턴스와
  외부 인덕턴스의 합이다. 내부 인덕턴스는 도체 내부 자속에 의한 것으로 상수
  0.05[mH/km], 외부 인덕턴스는 선간거리 D와 도체 반지름 r의 비에 따라
  0.4605 log₁₀(D/r)[mH/km]이다. 따라서 L = 0.05 + 0.4605 log₁₀(D/r)[mH/km].
  로그 인수는 D/r(선간거리÷반지름), 상수항은 0.05이다.
- proposed steps draft:
  - 인식: 가공 송전선로 1상 작용 인덕턴스 공식을 묻는 문제.
  - 변환: 작용 인덕턴스 = 내부 인덕턴스(상수 0.05) + 외부 인덕턴스(0.4605 log₁₀(D/r)).
  - 계산: L = 0.05 + 0.4605 log₁₀(D/r) [mH/km]. → 정답: 2번.
- answer-lock checks:
  - conclusion matches q.answer: PASS — 결론이 2번(q.answer=2)을 가리킨다.
  - no figure dependency: PASS — 공식 전개만으로 해결, 도면 의존 없음.
  - no invented source/article claim: PASS — 조항번호·외부 출처 인용 없음.
- risk note: **low** — source review가 PDF p.2 【답】②를 직접 확인하여 Q2-A A1
  draft가 source-confirmed로 승격되었다.

### 2. `2002_1회_32`

- key: `2002_1회_32`
- q.answer: **1**
- source_answer: **1**
- source_page: 3-4
- source verdict: `source_answer_verified`
- old solution issue: Q2-A dry-run에서 DB 저장 보기 1이 OCR 손상(`} \end{table}`
  잔류)으로 평가 불가 판정되어 Part B(`needs_source_answer_check`)로 제외되었다.
  source review에서 원문 PDF(p.3 문제, p.4 풀이)를 직접 판독한 결과 보기는
  깨끗하며, 풀이의 고장별 대칭분 표가 【답】①을 명시한다. 따라서 Q2-A에서
  작성하지 못한 proposed solution을 본 시트에서 새로 작성한다.
- proposed solution draft: 대칭좌표법에서 송전선 고장은 영상·정상·역상의 세
  대칭분으로 분해하여 해석한다. 고장 종류별로 필요한 대칭분이 다르다 — 3상
  단락은 정상분만, 선간 단락은 정상분과 역상분, 1선 지락은 정상·역상·영상분
  모두가 필요하다. 문제는 "정상 및 역상 임피던스가 필요한 경우"(정상분과
  역상분만 필요하고 영상분은 불필요한 경우)를 묻는다. 이는 선간 단락 고장에
  해당한다.
- proposed steps draft:
  - 인식: 대칭좌표법 고장 해석에서 정상·역상 임피던스만 필요한 고장 종류를 묻는 문제.
  - 변환: 고장별 필요 대칭분 — 3상 단락=정상분, 선간 단락=정상분+역상분,
    1선 지락=정상분+역상분+영상분.
  - 계산(판정): 정상분과 역상분만 필요하고 영상분은 불필요 = 선간 단락 고장.
    → 정답: 1번.
- answer-lock checks:
  - conclusion matches q.answer: PASS — 결론이 1번(q.answer=1)을 가리킨다.
  - no figure dependency: PASS — 고장별 대칭분 관계만으로 해결, 도면 의존 없음.
  - no invented source/article claim: PASS — 조항번호·외부 출처 인용 없음.
- risk note: **low** — Q2-A에서 OCR 손상으로 제외됐던 항목이 source review로
  복구되었다. PDF p.4 풀이의 고장별 대칭분 표가 【답】①을 직접 확인한다.

### 3. `2005_3회_83`

- key: `2005_3회_83`
- q.answer: **4**
- source_answer: **4**
- source_page: 8
- source verdict: `source_answer_verified`
- old solution issue: Q2-A dry-run A2 기록 — 구해설 결론이 "정답 4번 (…내용상
  (2)번이며 정정 필요)"로 결론과 보기번호 진술이 자가당착이다
  (detected_answer_mentions=[2]). source review에서 PDF p.8 풀이의 【답】④로
  q.answer=4가 확정되었다.
- proposed solution draft: 금속관의 절단면(단구)은 날카로워, 전선이 직접 닿으면
  절연 피복이 쓸려 손상될 수 있다. 절연 부싱은 이 관 단구에 끼워 전선 피복을
  보호하는 부품이다. 따라서 절연 부싱의 가장 주된 목적은 관의 단구에서 전선
  피복의 손상을 방지하는 것이다.
- proposed steps draft:
  - 인식: 금속관공사에서 절연 부싱의 주된 목적을 묻는 문제.
  - 변환: 금속관 단구는 날카로워 전선 피복이 손상되기 쉽다. 절연 부싱은 단구에
    끼우는 보호 부품이다.
  - 계산(판정): 절연 부싱의 주된 목적 = 관 단구에서 전선 피복 손상 방지.
    → 정답: 4번.
- answer-lock checks:
  - conclusion matches q.answer: PASS — 결론이 4번(q.answer=4)을 가리킨다.
  - no figure dependency: PASS — 개념 설명만으로 해결, 도면 의존 없음.
  - no invented source/article claim: PASS — 원문 PDF p.8 풀이는 `232.12`
    조항을 인용하나 본 draft는 개념 설명만 사용하고 조항번호를 인용하지 않는다.
- risk note: **low** — source review가 PDF p.8 풀이 【답】④를 확인했다. 원문
  풀이는 `232.12` 조항(관 끝 부분 전선 피복 손상 방지용 부싱 사용)을 명시하여
  A2 draft의 개념 설명과 정합한다.

### 4. `2006_1회_7`

- key: `2006_1회_7`
- q.answer: **2**
- source_answer: **2**
- source_page: 2
- source verdict: `source_answer_verified`
- old solution issue: Q2-A dry-run A3 기록 — 구해설이 발산 계산값 "3"과 보기번호
  "3"을 혼동하여 결론을 "(3)번"으로 적었다 (detected_answer_mentions=[3]).
  계산값 3에 해당하는 보기는 2번이다. source review에서 PDF p.2 풀이의
  "div E=3 → 【답】②"로 q.answer=2가 확정되었다.
- proposed solution draft: 발산 div E = ∂Eₓ/∂x + ∂E_y/∂y + ∂E_z/∂z.
  ∂Eₓ/∂x = 6e³ˣsin5y, ∂E_y/∂y = 5e³ˣsin5y이며 원점에서 sin0 = 0이므로 두 항
  모두 0. ∂E_z/∂z = 3e⁴ᶻ(1+4z)이며 z=0에서 3. 따라서 원점의 발산 값은
  0+0+3 = 3이다. 보기 중 값 "3"은 2번이다.
- proposed steps draft:
  - 인식: 주어진 전계 벡터의 발산을 원점에서 구하는 문제.
  - 변환: div E = ∂Eₓ/∂x + ∂E_y/∂y + ∂E_z/∂z. 각 성분을 해당 변수로 편미분한다.
  - 계산: 원점에서 x·y 성분 미분값은 sin0=0으로 0, z 성분 미분값 3e⁴ᶻ(1+4z)는 3.
    합 = 3. 보기에서 값 3은 2번. → 정답: 2번.
- answer-lock checks:
  - conclusion matches q.answer: PASS — 결론이 2번(q.answer=2)을 가리킨다.
  - no figure dependency: PASS — 벡터 미분 계산만으로 해결, 도면 의존 없음.
  - no invented source/article claim: PASS — 조항번호·외부 출처 인용 없음.
- risk note: **low** — source review가 PDF p.2 풀이 "div E=3 → 【답】②"를
  확인했다. 구해설의 계산값-보기번호 혼동을 source가 정정한다.

---

## Status

- Q2 apply remains **BLOCKED**.
- This sheet is a dry-run draft. It is NOT applied to `app/data`.
- All 4 drafts: answer-lock 3-check PASS, risk **low**.
- verified 4 items remain regeneration **candidates only** — not apply-approved.
  Regeneration apply requires separate approval.
- `source_answer_conflict` 6 items: not touched; separate answer correction
  design required (no `app/data` edit authorized).

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No answer correction.
- No solution apply.
- No regeneration apply.
- No paid API call.
