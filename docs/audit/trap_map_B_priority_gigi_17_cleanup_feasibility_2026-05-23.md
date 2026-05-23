# Trap-Map B-Priority — 기기-17 Cleanup Feasibility / Review (2026-05-23)

기기-18 steps cleanup followup erratum(`54ccd63`)이 마지막 caution 사유로 식별한
기기-17 대표 기출 `2020_1회_52` cleanup feasibility/review다. 본 단계는 review만
— **app/data/questions.json·학습 패키지 미수정**.

본 단계는 feasibility 문서 작성까지 — app/data·questions.json·학습 패키지·
closeout/errata 미수정. solution/answer/choices/text 미수정. 유료 API 미호출.
local server 미실행. amend/rebase/reset 없음.

- 검토 대상: 기기-17 변압기 권수비 / 대표 기출 `2020_1회_52`
- 참조:
  - steps cleanup follow-up erratum (`docs/audit/trap_map_B_priority_gigi_18_steps_cleanup_followup_erratum_2026-05-23.md`)
  - 기기-17/18 cleanup feasibility 1차 (`docs/audit/trap_map_B_priority_cleanup_feasibility_review_2026-05-22.md`)
  - representative re-dryrun (`docs/audit/trap_map_B_priority_10_item_representative_redryrun_2026-05-22.md`)
  - study set v1 (`docs/audit/trap_map_B_priority_pilot_study_set_v1_2026-05-22.md`)
  - 원본 PDF `data/문제_2020_1,2회_20260316.pdf` page 19 문제 52

---

## 결론: **defer** — 신규 major 발견 (record 메타 식별 오류), upstream 조사 선행 필요

PDF 대조 결과 **questions.json `2020_1회_52` 레코드가 실제 PDF 2020년 1회 52번
문제와 다른 문제를 담고 있음**이 확인됐다(§2·§3). 이는 cleanup feasibility 1차
review(`1061a9f`)에서 식별된 "보기 [1] LaTeX 잉여 √3 / solution 전류식 오류"보다
**더 근본적인 결함** — 단순 표기/풀이 cleanup으로는 해소되지 않는 record 메타
식별(year·session·q_no ↔ 문제 본문) 불일치.

cleanup 옵션 4종(proceed_choice / proceed_solution / both / no_action) 모두
mis-attribution을 silence시킨 채 표면 정리만 수행 — 정직한 판정 아님. 본
feasibility는 **defer**를 권고하며, 우선 record 메타 식별 정상화 트랙(upstream
조사 + id 재attribution 또는 삭제·재이입)을 선행해야 한다.

기기-17은 caution 유지 — 사유가 "표기 cleanup 필요"에서 "record mis-attribution
escalation"으로 강화된다. clean count 36/41 사용 가능·완전 클린 35/40·caution 1/1
유지(본 cleanup으로는 변동 없음).

---

## 1. questions.json 현재 상태 (직접 조회)

`app/data/questions.json` `2020_1회_52` 레코드 — `python3 json.load` 후 출력:

| 필드 | 값 |
|---|---|
| year / session / q_no | 2020 / "1회" / 52 |
| subject | "전기기기" |
| tag | "변압기의 권수비 및 전압비" |
| q_type | "개념형" |
| difficulty | 4 |
| answer | **1** |
| text | "권수비가 a인 단상변압기 3대가 있다. 이것을 1차에 △, 2 차에 Y로 결선하여 3상 교류 평형회로에 접속할 때 2차측의 단자전압을 V(V), 전류를 I(A)라고 하면 1차측의 단자전압 및 선전류는 얼마인가?" |
| choices[0] (보기 [1]) | `\sqrt{3}\frac{aV}{\sqrt{3}}\text{(V)}, \frac{\sqrt{3}I}{a}\text{(A)}` |
| choices[1] (보기 [2]) | `\sqrt{3}aV\text{(V)}, \frac{I}{\sqrt{3}a}\text{(A)}` |
| choices[2] (보기 [3]) | `\frac{\sqrt{3}V}{a}\text{(V)}, \frac{aI}{\sqrt{3}}\text{(A)}` |
| choices[3] (보기 [4]) | `\frac{V}{\sqrt{3}a}\text{(V)}, \sqrt{3}aI\text{(A)}` |
| solution | (§4.2 참조) — V1 = aV/√3, **I1 = I/(√3a)** |
| steps | `{인식, 변환, 계산}` 3 sub-key 모두 △-Y 권수비 풀이 |
| solution_svg | 4,213자 (aV/√3 포함) |

---

## 2. 원본 PDF 대조 — **PDF 2020년 1회 문제 52 ≠ 위 레코드 내용**

### 2.1 원본 PDF 발췌 (`data/문제_2020_1,2회_20260316.pdf` PDF page 19)

```
문제 52  동기전동기의 공급 전압과 부하를 일정하게 유지하면서 역률을 1로
운전하고 있는 상태에서 여자 전류를 증가시키면 전기자 전류는?

 ① 앞선 무효전류가 증가
 ② 앞선 무효전류가 감소
 ③ 뒤진 무효전류가 증가
 ④ 뒤진 무효전류가 감소

풀이 (V곡선 그래프)
- I_f1: cos θ = 1
- I_f2 (여자 전류 증가): 진상의 전기자 전류가 흐르고, 전류는 증가한다.
- I_f3 (여자 전류 감소): 지상의 전기자 전류가 흐르고, 전류는 증가한다.
                                                                    [답] ①
```

지면 하단 footer: "20년도 1,2회 924" — 2020년 1회 q-range. PDF 페이지 18까지
q41~q50, 페이지 19에 q51~q53 — 문제 52 = 동기전동기 V곡선 / 여자전류 문제,
**정답 ①**.

### 2.2 questions.json `2020_1회_52`와의 대조

| 항목 | 원본 PDF 2020년 1회 문제 52 | questions.json `2020_1회_52` | 정합 |
|---|---|---|---|
| 주제 | 동기전동기 V곡선·여자전류 | 변압기 권수비·△-Y 결선 | **❌ 완전 불일치** |
| text | "동기전동기의 공급 전압과 부하를 일정하게 유지하면서 ... 여자 전류를 증가시키면 전기자 전류는?" | "권수비가 a인 단상변압기 3대... 1차 △, 2차 Y..." | **❌** |
| choices | 4지 무효전류 증감 분류 | 4지 LaTeX 전압·전류 식 | **❌** |
| 정답 | ① (앞선 무효전류가 증가) | 1 | (값은 같으나 의미 다름) |

→ **레코드 메타(`year=2020, session="1회", q_no=52`)와 본문 내용이 완전히
다르다.** 본문은 변압기 권수비 △-Y 문제이나, 그 id는 원본 PDF에서 동기전동기
V곡선 문제를 가리킨다.

### 2.3 원본 PDF 2020년 1회 문제 52와 정합한 레코드는 corpus 내 별도 존재

```
corpus 검색 — '여자 전류를 증가시키면 전기자 전류' 키워드:
  '2020_1,2회'_52  subj=전기기기  ans=1
  text: "동기전동기의 공급 전압과 부하를 일정하게 유지하면서 역률을 1로
        운전하고 있는 상태에서 여자 전류를 증가시키면 전기자 전류는?"
```

→ questions.json에는 PDF 2020년 1회 문제 52와 정합한 레코드가 **`2020_1,2회_52`
(session = "1,2회")** 로 별도 저장돼 있다. 즉 corpus 내에 동일한 PDF 출처에서
온 동기전동기 문제가 올바른 식별자로 한 번 저장되어 있고, 그와는 별개로 변압기
권수비 문제가 **`2020_1회_52` (session = "1회")** 라는 잘못된 식별자로 한 번 더
저장되어 있다.

---

## 3. 신규 발견: Record 메타 식별 오류 (Major)

### 3.1 발견 요약

| 발견 | 위치 | 영향 |
|---|---|---|
| `2020_1회_52` 레코드의 본문은 원본 PDF 2020년 1회 52번이 아님 | questions.json | record 메타 ↔ 본문 식별 불일치 (Major) |
| 본문은 변압기 권수비 △-Y 문제 — 유효한 기기-17 representative이나 *true source 미확정* | 본문 자체 | 학습 가치는 보존, 출처 추적 불가 |
| corpus에는 PDF 2020년 1회 52와 정합한 별도 레코드 `2020_1,2회_52`가 이미 존재 | questions.json | duplicate 식별자 (한 PDF 문제가 두 키로 저장) |
| 추출/세션 라벨링 파이프라인 오작동 가능성 | upstream | 다른 레코드에도 동일 패턴 가능 (전수 감사 필요) |

### 3.2 1차 cleanup feasibility review(`1061a9f`)의 식별 vs 본 발견

`1061a9f` §2가 식별한 기기-17 caution 사유:
- A. 보기 [1] LaTeX 잉여 √3 artifact
- B. solution 필드 전류식 오류 (I/(√3a), 물리값 √3I/a와 어긋남, 결선 라벨 오기)

본 review의 신규 발견:
- C. **레코드 메타 식별 오류 — record 자체가 2020 1회 52가 아님.**

A·B는 record 본문의 표기/풀이 결함이고, C는 record의 정체 결함이다. C가 해결되지
않은 상태에서 A·B만 cleanup하는 것은 *잘못된 식별자 아래의 텍스트*를 정리하는
일 — 실질적 무결성 회복이 아니다.

### 3.3 1차 redryrun(`6164d6f`) / 학습 패키지 영향 재평가

| 산출물 | 대상 식별 | 사용 데이터 | 영향 |
|---|---|---|---|
| 1차 redryrun(`6164d6f`) §검증표 | `2020_1회_52` | questions.json 본문 (권수비 △-Y) | 본문 기반 검증은 *내용상* 유효한 기기-17이나, 식별 라벨이 실제 PDF와 불일치라는 사실은 검출 못 함 (스코프 한계) |
| study set v1 기기-17 카드 | `2020_1회_52` 라벨 | questions.json 본문 | 본문은 유효한 권수비 △-Y 학습 자료. 단 "대표 기출: 2020_1회_52" 표기는 학습자가 원본 PDF로 cross-check 시 혼동 유발 |
| day plan / learning log v1.1 기기-17 카드 | 동일 | 동일 | 동일 |
| follow-up erratum (`c6d57d0`, `54ccd63`) — 기기-17 caution | 표기/풀이 cleanup만 caution 사유로 기록 | 메타 식별 오류 미반영 | caution 사유 underspecified — 본 review에서 escalate |

→ 학습 콘텐츠 자체는 유효 (권수비 △-Y는 실제 기기-17 representative 후보로
적합). 단 **인용 출처가 잘못됨** — 학습자가 "2020 1회 52를 풀자" 하고 원본 PDF
열면 V곡선 동기전동기 문제가 보임.

---

## 4. 알려진 caution 사항 — choice [1] LaTeX + solution 전류식 재정리

본 §은 record 본문 자체에 한정한 표기/풀이 결함 재확인. C(메타 식별 오류)와
분리해서 다룬다.

### 4.1 choice [1] LaTeX 잉여 √3 — 사실관계 재확인

choice [1] 원문: `\sqrt{3}\frac{aV}{\sqrt{3}}\text{(V)}, \frac{\sqrt{3}I}{a}\text{(A)}`
- 전압 항 문자 그대로: √3 · (aV/√3) = aV (잉여 √3 적용 시) **또는** aV/√3 (잉여
  √3 제거 시).
- 전류 항: √3I/a (정상).

물리 풀이 (1차△·2차Y, 권수비 a = N1/N2):
- 1차 단자전압 V1_line = aV/√3
- 1차 선전류 I1_line = √3I/a

→ **choice [1] (전압 잉여 √3 제거 시) = (aV/√3, √3I/a) = 물리 정답**. answer=1
정합 — **단 choice [1] 전압 LaTeX 표기 정리 필요** (artifact 1건).

### 4.2 solution 전류식 사실관계

solution 본문 전류 부분:
```
**전류 관계:**
Y-△ 변압기 결선에서 1차와 2차 선전류의 관계:
- 2차 Y결선 선전류: I
- 1차 △결선 선전류: I_1 = I/(√3a)

**정답:**
- 1차측 단자전압: aV/√3
- 1차측 선전류: I/(√3a)
```

- 전압: aV/√3 (정합, 1차△·2차Y 물리값과 일치).
- 전류: I/(√3a) — **물리값 √3I/a와 어긋남** (3배 차이). 또한 "Y-△ 변압기 결선"
  표기는 문제(1차△·2차Y, △-Y)와 반대 라벨.
- 즉 solution은 voltage는 맞고 current는 결선 라벨을 반대로 가정해 계산.

### 4.3 steps[계산] 사실관계

```
**1차측 선전류:**
I_1 = I/(a√3) = √3I/(3a)
```

steps도 solution과 동일하게 I/(a√3)로 계산 — solution과 같은 결선 라벨 오기로
인한 동일 오류.

### 4.4 solution_svg 사실관계

`solution_svg`는 aV/√3 표기를 포함하지만 √3I/a 또는 I/(√3a) 명시는 직접
확인되지 않음(grep). 본 review에서 svg 풀이 시각화 정합성 결론은 보류.

### 4.5 A·B 결함 자체는 cleanup 가능 — 단 C(메타 식별 오류) 해결 후에만 의미

- A (choice [1] LaTeX): 잉여 √3 제거하면 PDF/물리값 정합. 단순 1자 정정.
- B (solution + steps 전류식): "Y-△" → "△-Y", `I/(√3a)` → `√3I/a`로 정정. 복수
  위치(solution + steps[계산]) 동시 정정.
- C: 메타 식별 오류 — id 재attribution / duplicate 정리 / true source 식별.

C 해결 없이 A·B만 정정 시: "잘못된 id 아래의 텍스트를 정리"한 셈. 결과적으로
caution은 record-identity 차원에서 해소되지 않는다.

---

## 5. Cleanup 옵션 비교

본 review의 핵심: C(메타 식별 오류) 발견으로 인해 옵션 평가의 기준이 달라진다.

| 옵션 | 내용 | A·B 해소? | C 해소? | 권장 |
|---|---|---|---|---|
| proceed_choice_cleanup | choice [1] 잉여 √3 제거 | A 해소 | 아니오 | ✗ — C silence |
| proceed_solution_cleanup | solution/steps 전류식·결선 라벨 정정 | B 해소 | 아니오 | ✗ — C silence |
| proceed_choice_and_solution_cleanup | A + B 동시 | A·B 해소 | 아니오 | ✗ — C silence, 메타 식별 오류 잔존 |
| **defer** | record 메타 식별 정상화 트랙 선행 권고, A·B는 후속 | (대기) | (대기, upstream 조사 후) | ✅ |
| no_action | 영구 silence | — | — | ✗ |

### 권장: **defer** — 메타 식별 정상화 트랙 선행 필요

근거:
- C(메타 식별 오류)는 A·B와 다른 차원의 결함. 단순 텍스트 정정으로 해소 안 됨.
- A·B만 cleanup하면 "올바른 표기로 잘못된 식별자 아래에 저장"이라는 더 미묘한
  결함이 잔존.
- C 해결 후에야 A·B cleanup이 의미 있음 (또는 C 해결 과정에서 본문 자체가
  다른 처리(삭제·재이입)될 수 있음).
- defer는 추가 손상을 만들지 않고, 후속 트랙(upstream 조사)을 명확히 한다.

### Defer가 caution 해제와 충돌하지 않는 이유

기기-17 caution은 *record-level* 결함 잔존을 의미한다. C(메타 식별 오류)가
새로 추가됐으므로 caution 사유는 오히려 *강화*. caution 해제는 C+A+B 모두
해소된 후에만 가능. 단기 cleanup으로 해제 시도는 본 발견 이전 시나리오.

---

## 6. 영향 정리

### 6.1 학습 패키지 영향

- 학습 패키지 docs(study set v1 / day plan / learning log v1.1) 기기-17 카드는
  본문(권수비 △-Y) 기준으로 작성됨 — *학습 내용 자체는 유효한 기기-17
  representative*.
- 단 "대표 기출: `2020_1회_52`" 표기가 원본 PDF 2020년 1회 52와 불일치 — 학습자가
  원본 PDF로 cross-check 시 혼동 가능.
- 학습 패키지 정정 권고: 후속 트랙에서 record id가 재attribute되면 학습 패키지의
  "대표 기출" 표기도 동기 갱신 필요.

### 6.2 clean count 영향

| 분류 | 현재 (steps cleanup followup `54ccd63`) | 본 review 이후 |
|---|---|---|
| 사용 가능 | 36 / 41 | 36 / 41 (불변) |
| 완전 클린 | 35 / 40 | 35 / 40 (불변) |
| caution | 1 / 1 (기기-17) | **1 / 1 (기기-17, 사유 강화)** |
| blocked | 0 / 0 | 0 / 0 (불변) |

→ **clean count 수치 변동 없음**. 기기-17 caution 사유가 단순 표기 cleanup에서
record mis-attribution 포함으로 강화됨. follow-up erratum 차원의 별도 갱신이
필요한지는 본 review가 결정하지 않음(별도 트랙).

### 6.3 기기-17 caution 강화

post-closeout errata(`0045ce4`) 시점부터 기기-17은 다음 caution 사유로 분류:
- 보기 [1] LaTeX 잉여 √3 (A)
- solution 전류식 오류 (B — 1차 feasibility review `1061a9f`에서 식별)

본 review가 추가:
- **record 메타 식별 오류 (C — 신규)**

caution 강화 — 단순 cleanup 후속이 아닌 upstream record-identity 조사 트랙 필요.

### 6.4 추출 파이프라인 회귀 트랙과의 연결

기기-18 case에서 식별된 "추출 파이프라인 인접 문항 혼입"(steps cleanup followup
`54ccd63` §4)에 더해, 본 case는 "session 라벨링 오류" 또는 "duplicate record"
양상 — 같은 PDF 출처가 두 식별자(`2020_1회_52`, `2020_1,2회_52`)로 저장되며 한쪽
본문은 다른 문제로 대체된 것으로 보임. 회귀 트랙 범위가 확장되어야 함.

---

## 7. 다음 조치 권고

본 feasibility는 데이터·학습 패키지 변경 없음. 후속 작업은 별도 명시 승인 후
진행.

| 우선순위 | 트랙 | 내용 |
|---|---|---|
| 1 (선행) | **record 메타 식별 정상화 트랙** | (a) 권수비 △-Y 본문의 true source 식별 — 다른 연도/회차 PDF 조사, (b) `2020_1회_52` id 재attribution 또는 삭제, (c) 학습 패키지 "대표 기출" 표기 동기 갱신 검토. corpus 전수 감사로 동일 패턴 record 식별 |
| 2 (1 완료 후) | choice [1] LaTeX cleanup (A) | record id 정상화 후 `choices[0]` 잉여 √3 제거. 단순 1자 정정 |
| 3 (1 완료 후) | solution/steps 전류식·결선 라벨 cleanup (B) | `solution`·`steps[계산]` 전류식 `I/(√3a)` → `√3I/a`, 결선 라벨 "Y-△" → "△-Y" 정정 |
| 4 | 추출 파이프라인 회귀 트랙 (확장) | 기기-18 인접 문항 혼입 + 기기-17 session 라벨링·duplicate record 양상 모두 포함. 회귀 방지 |
| 5 | clean count 갱신 검토 | C+A+B 모두 해소 후 기기-17 caution → 완전 클린 전환 가능성 평가 (별도 follow-up erratum) |

본 review는 **defer 판정**까지 — 우선순위 1 트랙 착수는 별도 명시 승인 필요.

---

## 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. 원본 PDF 2020 1회 52 직접 조회 (PDF page 19) | ✅ §2.1 — V곡선 동기전동기 정답 ① |
| 2. questions.json `2020_1회_52` 현재 상태 직접 조회 | ✅ §1 |
| 3. 보기 [1] LaTeX artifact 사실 확인 | ✅ §4.1 — 잉여 √3 확인, 제거 시 물리 정합 |
| 4. solution 전류식 오류 사실 확인 | ✅ §4.2·4.3 — `I/(√3a)` ≠ 물리값 √3I/a, "Y-△" 결선 오기, steps[계산] 동일 오류 |
| 5. answer·학습 패키지 docs 정합 재확인 | ✅ §1·§3.3 — answer=1 정합(choice [1] artifact 제거 시), 학습 docs는 본문 기준 정확 |
| 5. **신규 발견: record 메타 식별 오류** | ✅ §2·§3 — PDF 2020 1회 52 ≠ questions.json `2020_1회_52` 본문 |
| 6. cleanup 필요 필드 후보 (choices/solution/steps/svg) | ✅ §4·§5 |
| 7. 수정 시 commit 분리안 제안 | ✅ §7 우선순위 1~3 |
| 8. 수정하지 않을 경우 caution 유지 영향 | ✅ §6 — caution 강화, clean count 불변 |
| 판정 (proceed_*/defer/no_action) | ✅ **defer** (§5 — 권고 근거 명시) |
| 데이터·학습 패키지·closeout/errata 미수정 | ✅ docs/audit/ 신규 1건만 |
| 추론으로 정정 확정 금지 — PDF source-grounded | ✅ PDF 발췌 직접 인용, 추정 결론 없음 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-17 `2020_1회_52` cleanup feasibility/review 완료 — **defer 판정**.
- 1차 review(`1061a9f`)가 식별한 caution 사유(보기 [1] LaTeX, solution 전류식)에
  더해 **신규 major 결함 발견 — record 메타 식별 오류**. PDF 2020년 1회 문제 52
  (동기전동기 V곡선, 정답 ①)와 questions.json `2020_1회_52` (변압기 권수비 △-Y,
  정답 1) 본문이 완전 불일치. corpus 내 `2020_1,2회_52`로 PDF 2020 1회 52 정합
  레코드 별도 존재 — duplicate 식별자 양상.
- 본 발견으로 cleanup 옵션 4종(proceed_choice / proceed_solution / both /
  no_action) 모두 메타 식별 오류를 silence시키는 표면 정리에 그침 — **defer**가
  유일한 정직한 판정.
- 기기-17 caution 사유 강화: 표기 cleanup에서 record mis-attribution 포함으로
  격상. caution 해제 불가, clean count 수치 변동 없음 (사용 가능 36/41 / 완전
  클린 35/40 / caution 1/1 / blocked 0/0 유지).
- 다음 권고: 1순위 record 메타 식별 정상화 트랙 (true source 식별 + id
  재attribution / duplicate 정리 + 학습 패키지 동기) → 2 choice cleanup → 3
  solution/steps cleanup → 4 추출 파이프라인 회귀 트랙 확장 → 5 clean count
  갱신 검토.
- 이 문서는 feasibility/review다. 데이터·학습 패키지·closeout/errata 미수정.
