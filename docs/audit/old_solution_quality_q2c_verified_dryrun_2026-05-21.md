# Old Solution Quality — Q2-C Verified Dry-Run Sheet (2026-05-21)

Answer-locked regenerated solution **drafts** for the 2 `source_answer_verified`
items from the second manual source review (pilot items 11-20). This is a
review sheet only. `app/data/questions.json` and `app/data/questions.v2.json`
were NOT modified. No paid API was used. Nothing was auto-applied. Q2 full
apply remains BLOCKED.

## Reference commits

- `e5dc08a` — docs: prepare second source review pack
- `041b83f` — docs: fill source answers for second review-pack items
- `cff0e6d` — docs: record second source review routing

## Inputs

- Second review pack: `docs/audit/old_answer_manual_source_review_pack2_2026-05-21.md`
- Second routing summary: `docs/audit/old_answer_manual_source_review_routing2_2026-05-21.md`
- Q2-A dry-run (reused drafts A4, A5): `docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`

## Scope — 2 verified items only

| key | subject | q.answer | source_answer | source_page | source verdict | Q2-A draft |
| --- | --- | ---: | ---: | ---: | --- | --- |
| `2015_1회_13` | 전기자기학 | 1 | 1 | 5 | `source_answer_verified` | reused (A4) |
| `2015_1회_22` | 전력공학 | 1 | 1 | 8 | `source_answer_verified` | reused (A5) |

The 7 `source_answer_conflict` items and the 1 `defer` item from the second
review are out of scope for this sheet and are not touched here. The 4 earlier
Q2-B applied items (`fec4bbc`) are also not touched.

Premise for both items below: `source_answer == q.answer`, confirmed by the
PDF 【답】 marker during the second manual source review. The drafts are
answer-locked to this verified answer.

---

## Drafts

### 1. `2015_1회_13`

- key: `2015_1회_13`
- q.answer: **1**
- source_answer: **1**
- source_page: 5
- source verdict: `source_answer_verified`
- old solution issue: Q2-A dry-run A4 기록 — 구해설 결론이 "정답 2번 (cos²…)"으로
  cos-제곱 형태인 보기 2를 가리켰다 (detected_answer_mentions=[2]). 그러나 두
  직교 전계 성분이 만드는 포인팅 벡터의 시간 함수는 원래 전계와 같은 sin-제곱
  형태로 유지되며, 이는 보기 1이다. Q2-A 시점에는 q.answer가 PDF 미검증
  상태였으나, 2차 source review에서 PDF p.5 풀이의 【답】①로 q.answer=1이
  확정되었다.
- proposed solution draft: 두 직교 전계 성분이 만드는 합성 전계의 크기 제곱은
  |E|² = E_y² + E_z² = (3×10⁻²)² + (4×10⁻²)² = 25×10⁻⁴·sin²ω(x-vt). 공기의
  고유 임피던스 η₀ ≈ 377[Ω]를 쓰면 포인팅 벡터 크기 S = |E|²/η₀ =
  25×10⁻⁴/377·sin²ω(x-vt) ≈ 6.63×10⁻⁶·sin²ω(x-vt)[W/m²]. 시간 함수는 원래
  전계와 같은 sin² 형태로 유지된다.
- proposed steps draft:
  - 인식: 직교하는 두 전계 성분이 만드는 전자파의 포인팅 벡터 크기.
  - 변환: |E|² = E_y² + E_z². 포인팅 벡터 크기 S = |E|²/η₀, 공기 η₀ ≈ 377[Ω].
  - 계산: |E|² = (9+16)×10⁻⁴·sin²ω(x-vt) = 25×10⁻⁴·sin²ω(x-vt).
    S = 25×10⁻⁴/377·sin² ≈ 6.63×10⁻⁶ sin²ω(x-vt). → 정답: 1번.
- answer-lock checks:
  - conclusion matches q.answer: PASS — 결론이 1번(q.answer=1)을 가리킨다.
  - no figure dependency: PASS — 벡터 합성·포인팅 벡터 계산만으로 해결, 도면 의존 없음.
  - no invented source/article claim: PASS — 조항번호·외부 출처 인용 없음.
- risk note: **low** — 2차 source review가 PDF p.5 풀이 【답】①를 직접 확인하여
  Q2-A A4 draft가 source-confirmed로 승격되었다. 구해설의 sin²/cos² 형태 혼동을
  source가 정정한다.

### 2. `2015_1회_22`

- key: `2015_1회_22`
- q.answer: **1**
- source_answer: **1**
- source_page: 8
- source verdict: `source_answer_verified`
- old solution issue: Q2-A dry-run A5 기록 — 구해설 결론이 "정답 (4) (…1번이라
  표기했으나 (4)번)"으로 결론과 보기번호 진술이 자가당착이다
  (detected_answer_mentions=[4]). 정태 안정 극한 전력 P_max는 직렬 리액턴스 X에
  반비례하므로, "직렬 리액턴스를 증가"시키는 보기 1은 안정도 향상 방법이 아니다
  — 즉 "아닌 것"을 묻는 문제의 답은 보기 1이다. 2차 source review에서 PDF p.8
  풀이의 【답】①로 q.answer=1이 확정되었다.
- proposed solution draft: 정태 안정 극한 전력은 P_max = (V_s·V_r/X)·sinδ로,
  직렬 리액턴스 X에 반비례한다. 안정도 향상책은 X를 줄이는 방향이다. "직렬
  리액턴스를 증가시킨다"는 X를 키워 P_max를 낮추므로 안정도를 오히려
  악화시킨다 — 안정도 향상 방법이 아니다. 나머지 보기(전압변동 억제, 중간
  조상, 고속 차단)는 모두 표준적 향상책이다.
- proposed steps draft:
  - 인식: 송전계통 안정도 향상 방법이 "아닌 것"을 고르는 문제.
  - 변환: P_max = (V_s·V_r/X)·sinδ. 안정도는 직렬 리액턴스 X에 반비례.
  - 계산(판정): 직렬 리액턴스 증가 → X↑ → P_max↓ → 안정도 악화 → 향상 방법
    아님. → 정답: 1번.
- answer-lock checks:
  - conclusion matches q.answer: PASS — 결론이 1번(q.answer=1)을 가리킨다.
  - no figure dependency: PASS — 안정 극한 전력 공식 전개만으로 해결, 도면 의존 없음.
  - no invented source/article claim: PASS — 조항번호·외부 출처 인용 없음.
- risk note: **low** — 2차 source review가 PDF p.8 풀이 【답】①를 직접 확인하여
  Q2-A A5 draft가 source-confirmed로 승격되었다. 구해설의 결론-보기번호
  자가당착을 source가 정정한다.

---

## Status

- Q2 apply remains **BLOCKED**.
- This sheet is a dry-run draft. It is NOT applied to `app/data`.
- Both drafts: answer-lock 3-check PASS, risk **low**.
- verified 2 items remain regeneration **candidates only** — not apply-approved.
  Regeneration apply requires separate approval.
- The 7 `source_answer_conflict` items: not touched; separate answer correction
  design required (no `app/data` edit authorized).
- The 1 `defer` item (`2014_3회_62`): not touched; a defective-question
  ("전항정답") policy is required before any handling.
- The 4 earlier Q2-B applied items (`fec4bbc`): not touched.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No answer correction.
- No solution apply.
- No regeneration apply.
- No modification of the conflict / defer items.
- No modification of the 4 earlier-applied (`fec4bbc`) items.
- No `solution_svg` modification.
- No paid API call.
