# Trap-Map B-Priority — 기기-17/기기-18 Cleanup Feasibility Review (2026-05-22)

B-priority pilot closeout(`3f2a840`)의 accepted residual 4·5(기기-17 LaTeX
artifact, 기기-18 cleanup 권장)에 대한 cleanup feasibility review다. 이번 단계는
feasibility 검토만 — app/data·questions.json 미수정.

검증을 위해 `questions.json`의 해당 2개 레코드를 **text·choices·answer·solution·
steps 전 필드** read-only 조회했다. solution/steps 미적용. answer/choices/text
미수정. 유료 API 미호출. local server 미실행.

- 검토 대상: 기기-17 `2020_1회_52` / 기기-18 `2010_2회_47`
- 참조:
  - B-priority closeout (`docs/audit/trap_map_B_priority_pilot_learning_package_closeout_2026-05-22.md`)
  - representative re-dryrun (`docs/audit/trap_map_B_priority_10_item_representative_redryrun_2026-05-22.md`)
  - study set v1 (`docs/audit/trap_map_B_priority_pilot_study_set_v1_2026-05-22.md`)

---

## 결론: **defer (양 항목)** + 기기-18 정답 충돌 escalation

closeout이 "단순 cleanup residual"로 분류했던 2건은, solution 필드까지 포함한
전 필드 조회 결과 **단순 표기 cleanup이 아니다.**

- **기기-17**: choice [1] √3 artifact 외에 **solution 필드의 전류식이 물리적으로
  오류**(결선 방향 반대). cleanup은 choices·solution 다필드 수정이며 원본 PDF
  대조 선행 필요 → **defer**.
- **기기-18**: choice [4] "철손내력"은 "절연내력" OCR 오류(solution이 확증) +
  **`answer` 필드(2)와 solution 필드 [답](4)이 충돌** + solution 필드에 다른
  문제(유도전동기) 혼입. 표준 풀이상 정답은 (4)로, `answer`(2)가 오류일 가능성이
  높다 → **defer + 정답 충돌 escalation**.

questions.json 수정은 양 항목 모두 **원본 PDF 공식 정답표 대조 검증을 선행**해야
하므로 현 단계 **no_action on questions.json**. 단 기기-18 정답 충돌은 B-pilot
학습 패키지(정답 2로 학습)에 영향을 주므로 별도 정정 트랙으로 escalate한다(§8).

---

## 1. 검증 방법

`questions.json`에서 2개 레코드를 전 필드 조회:
- text / choices(4지) / answer / solution / steps / solution_svg / quality.

1차 dryrun·redryrun은 명시 스코프가 **text·choices·answer**였고 solution·steps는
조회하지 않았다. 본 feasibility review가 solution·steps 필드를 처음 포함해 조회했고,
그 결과 아래 §2·§3의 신규 발견이 나왔다.

---

## 2. 기기-17 `2020_1회_52` 발견

- text: clean. answer: `1`.
- choices (questions.json 원문):
  - [1] `\n\sqrt{3}\frac{aV}{\sqrt{3}}\text{(V)}, \frac{\sqrt{3}I}{a}\text{(A)}`
  - [2] `\sqrt{3}aV\text{(V)}, \frac{I}{\sqrt{3}a}\text{(A)}`
  - [3] `\frac{\sqrt{3}V}{a}\text{(V)}, \frac{aI}{\sqrt{3}}\text{(A)}`
  - [4] `\frac{V}{\sqrt{3}a}\text{(V)}, \sqrt{3}aI\text{(A)}`

### 발견 2-A — choice [1] 전압 LaTeX 잉여 √3 (기지 artifact)
choice [1] 전압 항 `\sqrt{3}\frac{aV}{\sqrt{3}}` = 문자 그대로면 aV. 1차 △·2차 Y
물리 풀이상 1차 단자전압 = aV/√3. 잉여 `\sqrt{3}`를 제거하면 `\frac{aV}{\sqrt{3}}`
= 물리값과 정합. choice [1] 전류 항 `\frac{\sqrt{3}I}{a}` = √3I/a는 물리값과 정합
(이미 정상).

### 발견 2-B — solution 필드 전류식 오류 (신규)
solution 필드는 1차 단자전압 = aV/√3(정합)으로 적었으나, 1차 선전류를
**`I_1 = I/(√3a)`** 로 적고 "Y-△ 변압기 결선"이라 표기했다(문제는 △-Y).
- 1차 △ 결선에서 선전류 = √3 × 상전류 → 물리값 = √3I/a.
- solution의 I/(√3a)는 1차 Y·2차 △로 계산한 값 — 결선 방향을 반대로 적용한 오류.
- solution의 "**정답**" 단락도 "1차측 선전류 I/(√3a)"로 적어 — **choice [1] 전류
  (√3I/a)·answer 키(1)와 어긋난다.**
- 즉 solution 필드는 전압은 맞고 전류는 틀렸으며, 결선 라벨("Y-△")도 오기.

### 정합 정리
- 물리 정답: 1차 단자전압 aV/√3, 1차 선전류 √3I/a.
- choice [1]은 √3 artifact 제거 시 (aV/√3, √3I/a) = 물리 정답. **answer 키(1) 정확.**
- solution 필드만 전류·결선 라벨이 오류 — text·choices·answer는 (artifact 제외)
  정합.

---

## 3. 기기-18 `2010_2회_47` 발견

- text: clean. answer: `2`.
- choices: [1] 철손 / [2] 전압 변동률 / [3] 동손 / [4] **철손내력**.

### 발견 3-A — choice [4] "철손내력" = "절연내력" OCR 오류 (확증)
solution 필드가 "**절연내력**은 절연재의 종류에 따라 정해지는 것으로서 무부하
시험과 단락시험으로는 구할 수 없다"고 명시 — choice [4]의 의도 용어는 **절연내력**.
"철손내력"은 "절연내력"의 OCR 오류로 **확증**(solution 본문이 source).

### 발견 3-B — `answer` 필드(2)와 solution 필드 [답](4) 충돌 (신규·중대)
solution 필드는 무부하시험 측정 가능(철손 등)·단락시험 측정 가능(동손 등)을
나열한 뒤 "절연내력은 ... 구할 수 없다. **[답] (4)**"로 끝난다. 그러나 레코드의
`answer` 필드는 **2**.
- 표준 풀이: 철손[1]은 무부하시험, 동손[3]은 단락시험에서 측정 가능. 전압변동률[2]은
  단락시험 결과(%임피던스 강하)로 계산 가능. 절연내력[4]만 별도 절연내력시험이
  필요 — "구할 수 없는 것"의 정답은 **(4) 절연내력**.
- solution 필드의 [답](4)·표준 풀이가 일치 → **`answer` 필드(2)가 오류일 가능성이
  높다.** 최종 확정은 원본 PDF 공식 정답표 대조 필요.

### 발견 3-C — solution 필드에 다른 문제 혼입 (신규)
solution 필드 후반에 본 문제와 무관한 문제("483000V, 60Hz, 8극, 100kW 3상 유도
전동기 ... 전부하 회전수")와 그 풀이가 통째로 붙어 있다. steps 필드의 '인식'도
"변압기 문제가 아닌 유도 전동기 문제"라 적혀 — solution·steps가 다른 문제 기준으로
오염됨.

---

## 4. 항목별 평가

| 평가 항목 | 기기-17 `2020_1회_52` | 기기-18 `2010_2회_47` |
|---|---|---|
| cleanup 필요 여부 | 필요 — choice [1] artifact + solution 전류식 오류 | 필요 — choice [4] garble + answer 충돌 + solution 오염 |
| source-clean 영향 | text·choices·answer는 (artifact 제외) 정합. **solution 필드 비정합** | choices [4] garble. **answer↔solution 정답 충돌** — solution 포함 시 비정합 |
| 학습 패키지 영향 | **낮음** — study set·day plan·learning log는 물리 정답(√3I/a)·answer(1)을 정확히 사용. questions.json solution 필드만 오류(앱 풀이 표시에 영향) | **높음** — study set·day plan·learning log가 기기-18 정답을 (2) 전압변동률로 학습. 정답이 (4)이면 학습 카드가 오답을 가르침 |
| redryrun 판정과의 관계 | redryrun "정답·trap 정합"은 text·choices·answer 스코프 한정 — solution 오류는 미검출 | redryrun "ready_with_note, 정답 (2) 정합"은 answer 필드만 확인 — solution [답](4) 미검출 |

---

## 5. 수정 대상 필드 후보 (수정은 미실시 — 후보만 명시)

| 항목 | 필드 | 수정 후보 내용 |
|---|---|---|
| 기기-17 | `choices[0]` | 전압 항 `\sqrt{3}\frac{aV}{\sqrt{3}}` → `\frac{aV}{\sqrt{3}}` (잉여 √3 제거). 전류 항 √3I/a는 유지 |
| 기기-17 | `solution` | 전류 `I/(√3a)` → `√3I/a`, 결선 라벨 "Y-△" → "△-Y", "정답" 단락 전류 정정 |
| 기기-17 | `steps` | '변환'·'계산' 단계에 동일 전류 오류 잔존 여부 확인 후 정정 |
| 기기-18 | `choices[3]` | "철손내력" → "절연내력" |
| 기기-18 | `answer` | 공식 정답표 대조 후 (2)→(4) 정정 여부 확정 |
| 기기-18 | `solution` | 본 문제(절연내력) 풀이만 남기고 혼입된 유도전동기 문제·풀이 제거 |
| 기기-18 | `steps` | 유도전동기 기준으로 오염된 '인식'·'변환' 재작성 |

answer/choices/text 및 solution/steps는 본 review에서 **미수정** — 위는 후보 명세.

---

## 6. 수정 전 추가 검증 필요 여부 — **필요 (양 항목)**

1. **원본 PDF 대조** — `2020_1회` 52번·`2010_2회` 47번의 출제 원본 PDF에서 공식
   보기 텍스트·공식 정답을 확인. 특히:
   - 기기-17: choice [1]의 공식 표기가 `aV/√3`인지 확정(현 인용은 물리 추론 기반).
   - 기기-18: 공식 정답이 (4)인지 (2)인지 확정 — `answer`↔solution 충돌 해소.
2. **기기-17 steps 필드 점검** — '변환'·'계산'에 solution과 동일한 전류 오류가
   있는지 확인.
3. **기기-18 solution 출처 분리** — 혼입된 유도전동기 문제가 어느 레코드에서 왔는지
   식별(다른 레코드 solution 누락 가능성 점검).
4. **downstream 동기화** — solution_svg가 오류 풀이를 시각화했는지 확인(기기-17
   전류·기기-18 정답).

검증 전 questions.json 수정 금지 — 추론값으로 answer/choices/solution을 덮어쓰면
사례 8(측정-결론 비약)·사례 7(description을 source 취급) 위험.

---

## 7. 판정

| 항목 | 판정 | 사유 |
|---|---|---|
| 기기-17 | **defer** | cleanup 가능하나 choices+solution(+steps) 다필드 수정이며 원본 PDF 대조 선행 필요. 검증 전 no_action |
| 기기-18 | **defer** | choice [4] garble은 solution이 확증해 cleanup 가능하나, answer 충돌이 핵심 — 공식 정답표 대조 선행 필수. 검증 전 no_action |
| 종합 | **defer** | 양 항목 모두 원본 PDF 검증을 선행 트랙으로 두고, 검증 완료 후 cleanup 실행 트랙으로 진행. 현 단계 questions.json 수정 없음 |

proceed 아님(추론값 적용 위험), no_action 아님(artifact·오류 실재, 방치 불가) —
**defer**: 원본 PDF 검증 트랙을 선행한 뒤 cleanup.

---

## 8. B-Pilot 영향 및 권고

본 feasibility review는 closeout accepted-residual에 **미반영된 신규 결함**을
드러냈다 — closeout은 기기-17/18을 "표기 cleanup"으로 분류했으나 실제로는 더 깊다.

- **기기-17**: B-pilot 학습 패키지 docs는 물리 정답을 정확히 사용 — 학습 영향 낮음.
  questions.json solution 필드 오류는 DQ 트랙 cleanup 대상(앱 풀이 표시 한정).
- **기기-18**: B-pilot 학습 패키지는 정답을 **(2) 전압변동률**로 학습한다. 표준
  풀이·solution 필드는 정답을 **(4) 절연내력**으로 본다. 정답이 (4)로 확정되면
  study set v1·day plan·learning log v1.1의 기기-18 카드가 **오답을 가르치는**
  상태가 된다.

### 권고

1. **우선 — 기기-18 정답 충돌 해소 트랙**: 원본 `2010_2회` PDF 공식 정답표로
   기기-18 정답((2) vs (4))을 확정. (4)로 확정되면 B-pilot 기기-18 카드 정정 또는
   기기-18을 needs_replacement 재분류 후 대체 항목 재선정 필요. closeout의
   "학습자 사용 준비 완료"는 기기-18 한정으로 **정답 확정 시까지 보류** 권고.
2. **다음 — 기기-17/18 cleanup 실행 트랙**: 원본 PDF 검증 완료 후 §5 후보 필드를
   DQ 트랙으로 정정(별도 승인).
3. closeout 문서는 amend하지 않는다(금지). 본 review 문서가 신규 결함의 인계
   기록이며, 후속 트랙이 이를 근거로 진행한다.

---

## 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 검토 대상 2항 전 필드 조회 | ✅ text·choices·answer·solution·steps — questions.json read-only |
| cleanup 필요 여부 | ✅ §4 — 양 항목 필요 |
| source-clean 영향 | ✅ §4 — 기기-17 solution 비정합 / 기기-18 answer↔solution 충돌 |
| 학습 패키지 영향 | ✅ §4 — 기기-17 낮음 / 기기-18 높음 |
| 수정 대상 필드 후보 | ✅ §5 — 미수정, 후보만 명시 |
| 수정 전 추가 검증 필요 | ✅ §6 — 원본 PDF 대조 등 4건 |
| proceed/no_action/defer 판정 | ✅ §7 — 양 항목 defer |
| B-pilot 영향 escalation | ✅ §8 — 기기-18 정답 충돌, closeout 미반영 신규 결함 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-17/기기-18 cleanup feasibility review 완료 — questions.json 전 필드
  read-only 조회.
- 판정: 양 항목 **defer** — 원본 PDF 공식 정답표·보기 대조 검증을 선행해야
  cleanup 가능. 현 단계 questions.json 수정 없음.
- 신규 발견: 기기-17 solution 필드 전류식 오류(I/(√3a), 물리값 √3I/a) / 기기-18
  `answer`(2)↔solution [답](4) 정답 충돌 + choice [4] "철손내력"="절연내력" OCR
  오류 + solution 다른 문제 혼입.
- B-pilot 영향: 기기-17 낮음(docs 정확), 기기-18 **높음**(학습 패키지가 정답 (2)로
  학습 — 정답 (4) 확정 시 오답 학습). closeout accepted-residual 미반영 신규 결함.
- 권고: 1순위 기기-18 정답 충돌 해소 트랙(원본 PDF 대조), 2순위 cleanup 실행 트랙.
- 이 문서는 feasibility review다. questions.json·학습 패키지·closeout 미수정.
