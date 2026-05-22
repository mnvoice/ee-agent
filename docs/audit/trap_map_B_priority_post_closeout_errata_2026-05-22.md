# Trap-Map B-Priority Pilot — Post-Closeout Errata (2026-05-22)

cleanup feasibility review(`1061a9f`)에서 발견된 **기기-18 정답 충돌**이 B-priority
pilot closeout(`3f2a840`)의 "B-pilot 10항 전체 PASS" 및 "학습자 사용 준비 완료"
판정에 미치는 영향을 정리하는 post-closeout errata다.

closeout 문서는 amend하지 않는다(금지). 본 errata가 closeout 판정의 정정 기록이며,
후속 트랙은 본 문서를 근거로 진행한다. app/data·questions.json 미수정. solution/
steps 미적용. answer/choices/text 미수정. 유료 API 미호출. local server 미실행.

- 참조:
  - B-priority closeout (`docs/audit/trap_map_B_priority_pilot_learning_package_closeout_2026-05-22.md`)
  - cleanup feasibility review (`docs/audit/trap_map_B_priority_cleanup_feasibility_review_2026-05-22.md`)
  - representative re-dryrun (`docs/audit/trap_map_B_priority_10_item_representative_redryrun_2026-05-22.md`)
  - study set v1 / day plan / learning log v1.1 (B-pilot 학습 패키지)

---

## 결론

closeout의 **"B-pilot 10항 전체 PASS · 학습자 사용 준비 완료"** 판정을 정정한다.

- **기기-18 — 사용 보류(blocked)**: `answer` 필드(2)와 solution 필드/표준 풀이상
  정답(4)이 충돌. 학습 패키지가 정답 (2)로 가르치므로, 정답이 (4)로 확정되면
  오답 학습. 공식 정답표/원본 PDF 대조 전까지 **학습 사용 보류**.
- **기기-17 — caution 유지(사용 가능)**: choices √3 artifact·solution 전류식
  오류가 있으나 `answer`(1)·학습 패키지 docs는 물리 정답과 정합. 학습 사용은
  가능하되 caution(ready_with_note 유지). cleanup은 원본 PDF 대조 후 defer.
- closeout의 "10항 전체 PASS"는 **9항 사용 가능(8 클린 + 기기-17 caution) +
  기기-18 1항 보류**로 정정한다.

---

## 1. 기기-17 `2020_1회_52` — caution 유지

feasibility review(`1061a9f`) §2 발견:
- choice [1] 전압 LaTeX `\sqrt{3}\frac{aV}{\sqrt{3}}` — 잉여 √3 artifact.
- solution 필드 전류식 `I/(√3a)` — 물리값 `√3I/a`와 어긋남(결선 방향 반대 적용,
  "Y-△" 오기). solution "정답" 단락도 동일 오류.

정합 상태:
- `answer` 필드(1) — **정확**. choice [1]은 √3 artifact 제거 시 (aV/√3, √3I/a) =
  물리 정답.
- B-pilot 학습 패키지(study set v1·day plan·learning log v1.1) — 기기-17 카드는
  물리 정답(1차 선전류 √3I/a)·answer(1)을 정확히 사용. 학습 docs 정합.
- 비정합은 questions.json `solution` 필드(+steps 가능성)에 한정 — 앱 풀이 표시에만
  영향.

**판단 — 학습 사용 가능, caution 유지(ready_with_note)**:
- 학습 패키지 docs가 정확하므로 study set/learning log로 학습하면 문제 없음.
- caution 사유: 앱에서 이 문항의 solution을 열면 잘못된 전류식이 보일 수 있음 →
  학습자에게 "앱 풀이 표시의 전류식은 정정 대기" 주의 첨부.
- cleanup(choices[0] artifact 제거 + solution 정정)은 원본 `2020_1회` PDF 대조
  후 결정 — feasibility review 판정대로 **defer**.

→ 기기-17: **caution 1항/1문제** — 사용 가능, ready_with_note 유지.

---

## 2. 기기-18 `2010_2회_47` — 사용 보류(blocked)

feasibility review(`1061a9f`) §3 발견:
- choice [4] "철손내력" = "절연내력" OCR 오류 — solution 본문이 확증.
- **`answer` 필드(2) ↔ solution 필드 [답](4) 충돌.** 표준 풀이: 철손[1]은
  무부하시험, 동손[3]은 단락시험, 전압변동률[2]은 단락시험 결과로 계산 가능 —
  "구할 수 없는 것"의 정답은 (4) 절연내력. solution·표준 풀이가 (4)로 일치.
- solution 필드에 본 문제와 무관한 유도전동기 문제·풀이 혼입.

**B-pilot 학습 패키지 영향**:
- study set v1·day plan·learning log v1.1의 기기-18 카드는 정답을 **(2) 전압
  변동률**로 명시하고, 3회독 체크·외울 핵심 문장·오답 패턴을 (2) 기준으로 구성.
- 정답이 (4) 절연내력으로 확정되면 — **기기-18 학습 카드 전체가 오답을 가르치는
  상태**가 된다. (2) vs (4)는 trap·풀이·체크 질문이 모두 달라지는 충돌.

**판단 — 학습 사용 보류(blocked)**:
- 공식 정답표/원본 `2010_2회` PDF 대조로 정답((2) vs (4))을 확정하기 전까지
  기기-18 카드는 학습 사용 보류.
- 정답 (4) 확정 시: 기기-18 카드 정정(정답·trap·체크 재작성) 또는 기기-18을
  needs_replacement 재분류 후 대체 항목 재선정 필요.
- 정답 (2) 확정 시(가능성 낮음): `answer` 필드 정합, choice [4] garble만 cleanup.

→ 기기-18: **blocked 1항/1문제** — 정답 확정 전 사용 보류.

---

## 3. closeout 판정 정정

| closeout(`3f2a840`) 원 판정 | post-closeout 정정 |
|---|---|
| B-pilot 10항 전체 PASS | **9항 사용 가능 + 기기-18 1항 보류** (10항 일괄 PASS 아님) |
| 학습자 사용 준비 완료 | **9항 준비 완료** = 8항 클린 + 기기-17 1항 caution / 기기-18 1항 보류 |
| 기기-17·18 = accepted residual(표기 cleanup) | 기기-17 = caution residual / **기기-18 = blocked(정답 충돌, residual 아닌 미해결 결함)** |

closeout의 redryrun 10/10·study set/day plan/learning log review PASS 자체는
유효하다 — 그 게이트들은 text·choices·answer 스코프였고, solution 필드 결함은
feasibility review가 처음 검출했다. 본 errata는 그 신규 검출을 반영해 **사용
준비 판정만** 9항+1보류 체계로 낮춘다.

---

## 4. 전체 clean count 갱신

| 분류 | 항 | 문제 | 비고 |
|---|---|---|---|
| A-priority (유지) | 26 | 31 | A closeout 기준 — 변동 없음 |
| B-priority 클린 (caution·blocked 제외) | 8 | 8 | 기기-4·17·18 외 7 + … = B 10 − 기기-17 − 기기-18 = 8 |
| 기기-17 caution | 1 | 1 | 사용 가능, ready_with_note 유지 |
| 기기-18 blocked | 1 | 1 | 정답 충돌 — 사용 보류 |
| **합계** | **36** | **41** | A 26/31 + B 10/10 |

요약:
- **확정 클린(사용 가능, blocked 제외): 35항/40문제** = A 26/31 + B 9/9(기기-18
  제외). 이 중 기기-17 1항/1문제는 caution(사용 가능하나 주의).
- 완전 클린(caution·blocked 제외): 34항/39문제.
- **기기-17 caution: 1항/1문제** — 사용 가능.
- **기기-18 blocked: 1항/1문제** — 사용 보류.

A-priority 26항/31문제는 본 errata 범위 밖 — 변동 없이 유지.

---

## 5. 다음 우선 트랙

| 우선순위 | 트랙 | 내용 |
|---|---|---|
| 1 | 기기-18 공식 정답표/PDF 대조 | 원본 `2010_2회` 47번 공식 정답((2) vs (4)) 확정. (4) 확정 시 기기-18 카드 정정 또는 needs_replacement 재분류 + 대체 항목 재선정. choice [4] "절연내력" garble·solution 혼입도 동시 정리 |
| 2 | 기기-17 원본 PDF 대조 후 cleanup 여부 결정 | 원본 `2020_1회` 52번 보기 [1] 공식 표기 확인 → choices[0] √3 artifact 제거·solution 전류식(√3I/a)·결선 라벨 정정 여부 결정 |

두 트랙 모두 questions.json answer/choices/solution 수정을 수반하므로 원본 PDF
검증을 선행한다 — 추론값 적용 금지(feasibility review §6).

---

## 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 기기-17 — artifact+solution 오류, docs 정합, cleanup defer, caution 유지 판단 | ✅ §1 |
| 기기-18 — OCR 오류, answer(2)↔(4) 충돌, solution 혼입, 사용 보류, 오답 학습 가능성 명시 | ✅ §2 |
| closeout 영향 — 10항 일괄 PASS → 9항+기기-18 보류 정정 | ✅ §3 |
| "학습자 사용 준비 완료" → 9항(8 클린+기기-17 caution) 체계로 낮춤 | ✅ §3·§4 |
| 전체 clean count 갱신 | ✅ §4 — A 26/31 유지 / 확정 클린 35/40 / 기기-17 caution 1/1 / 기기-18 blocked 1/1 |
| 다음 우선 트랙 | ✅ §5 — 1 기기-18 정답표 대조 / 2 기기-17 PDF 대조 후 cleanup |
| closeout 미수정(amend 없음) | ✅ 별도 errata 문서로 정정 기록 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps 미수정 / API·server 미실행 |

---

## Status

- B-priority pilot post-closeout errata 작성 완료 — feasibility review(`1061a9f`)
  기기-18 정답 충돌의 closeout 영향 정리.
- 기기-17: caution 유지(사용 가능, ready_with_note) — docs 정합, cleanup defer.
- 기기-18: blocked(사용 보류) — `answer`(2)↔정답(4) 충돌, 학습 패키지가 오답(2)을
  가르칠 가능성. 공식 정답표/PDF 대조 전 보류.
- closeout 판정 정정: "10항 전체 PASS·사용 준비 완료" → **9항 사용 가능
  (8 클린 + 기기-17 caution) + 기기-18 1항 보류**.
- clean count: A 26항/31문제 유지 / 확정 클린(사용 가능) 35항/40문제 / 기기-17
  caution 1항/1문제 / 기기-18 blocked 1항/1문제 (총 36항/41문제).
- 다음 우선 트랙: 1 기기-18 공식 정답표/PDF 대조, 2 기기-17 원본 PDF 대조 후
  cleanup 결정.
- 이 문서는 post-closeout errata다. closeout·questions.json·학습 패키지 미수정.
