# Old Solution Quality — Q2-D Verified Dry-Run Sheet (2026-05-21)

Answer-locked regenerated solution **drafts** for the 3 `source_answer_verified`
items from the third manual source review (pilot items 21-30). This is a
review sheet only. `app/data/questions.json` and `app/data/questions.v2.json`
were NOT modified. No paid API was used. Nothing was auto-applied. Q2 full
apply remains BLOCKED.

With the third pack, the full 30-item C1 pilot has been manually
source-reviewed.

## Reference commits

- `ee58aab` — docs: prepare third source review pack
- `d4462c1` — docs: fill source answers for third review-pack items
- `feed96a` — docs: record third source review routing

## Cumulative pilot-30 state

- `source_answer_verified`: 9
  - already applied (Q2-B `fec4bbc` 4 items + Q2-C `fbeffef` 2 items): 6
  - Q2-D dry-run target (this sheet, 3 items): 3
- `source_answer_conflict`: 20 — sealed until the answer correction track
- `defer`: 1 (`2014_3회_62`) — sealed until a defective-question policy is defined

## Inputs

- Third review pack: `docs/audit/old_answer_manual_source_review_pack3_2026-05-21.md`
- Third routing summary: `docs/audit/old_answer_manual_source_review_routing3_2026-05-21.md`
- Q2-A dry-run (reused drafts A6, A7, A8): `docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`

## Scope — 3 verified items only

| key | subject | q.answer | source_answer | source_page | source verdict | Q2-A draft |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `2015_3회_27` | 전력공학 | 3 | 3 | 10 | `source_answer_verified` | reused (A6) |
| `2016_1회_71` | 제어공학 | 3 | 3 | 23 | `source_answer_verified` | reused (A7) |
| `2016_3회_44` | 전기기기 | 4 | 4 | 15 | `source_answer_verified` | reused (A8) |

The 20 `source_answer_conflict` items and the 1 `defer` item are out of scope
for this sheet and are not touched here. The 6 earlier-applied items (Q2-B
`fec4bbc` + Q2-C `fbeffef`) are also not touched.

Premise for every item below: `source_answer == q.answer`, confirmed by the
PDF 【답】 marker during the third manual source review. The drafts are
answer-locked to this verified answer.

---

## Drafts

### 1. `2015_3회_27`

- key: `2015_3회_27`
- q.answer: **3**
- source_answer: **3**
- source_page: 10
- source verdict: `source_answer_verified`
- old solution issue: Q2-A dry-run A6 기록 — 구해설 결론이 "정답 4번"으로 보기 4를
  가리켰다 (detected_answer_mentions=[4]). 그러나 정태 안정 극한 전력은 계통의
  직렬 리액턴스에 반비례하므로, 발전기·변압기의 리액턴스를 크게 하면 안정도가
  나빠진다 — 즉 "증진 방법이 아닌 것"은 보기 3이다. 3차 source review에서 PDF
  p.10 풀이의 【답】③로 q.answer=3이 확정되었다.
- proposed solution draft: 정태 안정 극한 전력은 계통의 직렬 리액턴스에
  반비례한다. 발전기·변압기의 리액턴스를 크게 하면 직렬 리액턴스가 늘어
  안정도가 나빠진다 — 안정도 증진 방법이 아니다. 속응 여자방식, 고속도 재폐로,
  고장전류 저감·고속 차단은 모두 표준적인 증진책이다.
- proposed steps draft:
  - 인식: 송전계통 안정도 증진 방법이 "아닌 것"을 고르는 문제.
  - 변환: 안정 극한 전력은 직렬 리액턴스에 반비례. 증진책은 리액턴스를 줄이는 방향.
  - 계산(판정): 발전기·변압기 리액턴스를 크게 하면 직렬 리액턴스 증가 → 안정도
    악화 → 증진 방법 아님. → 정답: 3번.
- answer-lock checks:
  - conclusion matches q.answer: PASS — 결론이 3번(q.answer=3)을 가리킨다.
  - no figure dependency: PASS — 안정도 증진책 개념 비교만으로 해결, 도면 의존 없음.
  - no invented source/article claim: PASS — 조항번호·외부 출처 인용 없음.
- risk note: **low** — 3차 source review가 PDF p.10 풀이 【답】③를 직접 확인하여
  Q2-A A6 draft가 source-confirmed로 승격되었다. 구해설의 보기번호 오기를
  source가 정정한다.

### 2. `2016_1회_71`

- key: `2016_1회_71`
- q.answer: **3**
- source_answer: **3**
- source_page: 23
- source verdict: `source_answer_verified`
- old solution issue: Q2-A dry-run A7 기록 — 구해설이 E_l = E_p로 옳게 풀고도
  결론 보기번호를 "(1)번"으로 잘못 적었다 (detected_answer_mentions=[1]).
  E_l = E_p는 보기 3이다. 3차 source review에서 PDF p.23 풀이의 【답】③로
  q.answer=3이 확정되었다.
- proposed solution draft: 평형 3상 Δ(삼각)결선에서는 세 상권선이 삼각형으로
  닫혀 각 상권선이 두 선 사이에 직접 놓인다. 따라서 선간전압이 곧 상전압이며
  E_l = E_p이다. (전류는 반대로 선전류 = √3 × 상전류이다.)
- proposed steps draft:
  - 인식: 평형 3상 Δ결선에서 선간전압과 상전압의 관계.
  - 변환: Δ결선은 각 상권선이 두 선 사이에 직접 연결된다.
  - 계산(판정): 선간전압 = 상전압, 즉 E_l = E_p. → 정답: 3번.
- answer-lock checks:
  - conclusion matches q.answer: PASS — 결론이 3번(q.answer=3)을 가리킨다.
  - no figure dependency: PASS — Δ결선 구조 개념만으로 해결, 도면 의존 없음.
  - no invented source/article claim: PASS — 조항번호·외부 출처 인용 없음.
- risk note: **low** — 3차 source review가 PDF p.23 풀이 【답】③를 직접 확인하여
  Q2-A A7 draft가 source-confirmed로 승격되었다. 구해설은 E_l=E_p로 옳게 풀고도
  보기번호를 잘못 적었고, source가 이를 정정한다.

### 3. `2016_3회_44`

- key: `2016_3회_44`
- q.answer: **4**
- source_answer: **4**
- source_page: 15
- source verdict: `source_answer_verified`
- old solution issue: Q2-A dry-run A8 기록 — 구해설이 "무부하 시험"으로 옳게
  풀고도 결론 보기번호를 "1번"으로 잘못 적었다 (detected_answer_mentions=[1]).
  무부하시험은 보기 4이다. 3차 source review에서 PDF p.15 풀이의 【답】④로
  q.answer=4가 확정되었다.
- proposed solution draft: 변압기 철손은 철심의 히스테리시스손과 와전류손으로,
  전압·주파수에만 의존하고 부하와 무관한 무부하손이다. 정격전압을 걸고 2차를
  개방한 무부하시험(개방회로시험)에서는 전류가 작아 동손이 무시되므로 입력
  전력이 곧 철손이 된다. (동손은 단락시험에서 측정한다.)
- proposed steps draft:
  - 인식: 변압기 철손을 측정하는 시험의 종류.
  - 변환: 철손은 무부하손으로 정격전압·무부하 상태에서 측정한다.
  - 계산(판정): 무부하시험(2차 개방, 정격전압 인가)의 입력전력 = 철손.
    → 정답: 4번.
- answer-lock checks:
  - conclusion matches q.answer: PASS — 결론이 4번(q.answer=4)을 가리킨다.
  - no figure dependency: PASS — 변압기 시험 개념만으로 해결, 도면 의존 없음.
  - no invented source/article claim: PASS — 조항번호·외부 출처 인용 없음.
- risk note: **low** — 3차 source review가 PDF p.15 풀이 【답】④를 직접 확인하여
  Q2-A A8 draft가 source-confirmed로 승격되었다. 구해설은 무부하시험으로 옳게
  풀고도 보기번호를 잘못 적었고, source가 이를 정정한다.

---

## Status

- Q2 apply remains **BLOCKED**.
- This sheet is a dry-run draft. It is NOT applied to `app/data`.
- All 3 drafts: answer-lock 3-check PASS, risk **low**.
- verified 3 items remain regeneration **candidates only** — not apply-approved.
  Regeneration apply requires separate approval.
- The 20 `source_answer_conflict` items: not touched; separate answer
  correction design required (no `app/data` edit authorized).
- The 1 `defer` item (`2014_3회_62`): not touched; a defective-question
  ("전항정답") policy is required before any handling.
- The 6 earlier-applied items (Q2-B `fec4bbc` + Q2-C `fbeffef`): not touched.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No answer correction.
- No solution apply.
- No regeneration apply.
- No modification of the conflict / defer items.
- No modification of the 6 earlier-applied (`fec4bbc`, `fbeffef`) items.
- No `solution_svg` modification.
- No paid API call.
