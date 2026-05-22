# Trap-Map B-Priority — 기기-18 공식 정답 검증 (2026-05-22)

post-closeout errata(`0045ce4`)에서 blocked로 분류된 기기-18 대표 기출
`2010_2회_47`의 공식 정답을 source 대조로 확정한다. 이번 단계는 **정답·보기·
solution 충돌의 판정만** — 어떤 데이터도 수정하지 않는다.

app/data·questions.json 미수정. answer/choices/text 미수정. solution/steps
미적용. 유료 API 미호출. local server 미실행.

- 검증 대상: 기기-18 변압기 등가회로 / 대표 기출 `2010_2회_47`
- 참조:
  - post-closeout errata (`docs/audit/trap_map_B_priority_post_closeout_errata_2026-05-22.md`)
  - cleanup feasibility review (`docs/audit/trap_map_B_priority_cleanup_feasibility_review_2026-05-22.md`)

---

## 결론: **분기 2 — 공식 정답 (4) 절연내력**

원본 PDF 대조 결과 `2010_2회_47`의 공식 정답은 **④ 절연내력**이다.
questions.json `answer` 필드 (2)는 **오류 확정**.

- 원본 PDF 보기 ④ = **"절연내력"** (questions.json의 "철손내력"은 OCR 오류 확정).
- 원본 PDF 풀이 = "절연내력은 ... 무부하시험·단락시험으로는 구할 수 없다.
  **[답] ④**".
- B-pilot study set v1·day plan·learning log v1.1은 기기-18을 정답 (2)로 학습 —
  **오답을 가르친 상태 확정**.
- 기기-18 **blocked 유지** — questions.json 정정 승인 트랙 + 학습 패키지 기기-18
  카드 재작성 필요.

---

## 1. Source별 확인 결과

| Source | 접근 | 결과 |
|---|---|---|
| 원본 PDF — `data/문제_2010_2회_20260316.pdf` | ✅ 접근·조회 (PDF page 8, 지면 "2-29 / 10년도 2회") | 문제 47 문제·보기·풀이·정답 직접 확인 |
| 한국산업인력공단 공식 정답표(별도) | 미대조 | 원본 PDF(D-60 시리즈 2010년 2회 기출문제집)에 문제·보기·풀이·[답]이 인쇄돼 있어 별도 정답표 없이 확정 가능 |

원본 PDF는 "전기기사 필기 D-60 시리즈" 2010년 2회 기출문제집으로, 문제 47의
문제·보기 4지·풀이·[답]이 모두 인쇄돼 있다. 인쇄된 [답]·풀이 논리·보기 텍스트가
일관되고 표준 전기기사 지식과 부합 — 공식 정답 (4)로 판정.

### 원본 PDF 문제 47 (원문 그대로)

```
문제 47  변압기의 무부하시험, 단락시험에서 구할 수 없는 것은?
 ① 철손        ② 전압 변동률
 ③ 동손        ④ 절연내력

풀이
변압기의 시험
 (1) 개방 회로 시험(무부하 시험)으로 측정할 수 있는 항목
   · 무부하 전류 · 히스테리시스손 · 와류손 · 여자 어드미턴스 · 철손
 (2) 단락 시험으로 측정할 수 있는 항목
   · 임피던스 와트(전부하 동손) · 임피던스 전압(전압 강하)
 그러나, 절연내력은 절연재의 종류에 따라 정해지는 것으로서 무부하
 시험과 단락시험으로는 구할 수 없다.   [답] ④
```

---

## 2. 공식 정답 판정 — **(4) 절연내력**

- 원본 PDF 풀이가 명시: 철손[1]은 무부하시험, 동손[3]은 단락시험, 전압변동률[2]은
  단락시험 결과(임피던스 전압)로 도출 — 셋 다 두 시험에서 구할 수 있다. 절연내력만
  별도 절연내력시험이 필요 → "구할 수 없는 것"의 정답 = **④**.
- 원본 PDF [답] = **④**. 표준 전기기사 지식과도 부합.
- → 공식 정답 **(4) 절연내력**으로 확정.

---

## 3. 원본 PDF 보기 [4] 실제 문구

| 보기 | 원본 PDF | questions.json `choices` |
|---|---|---|
| [1] | 철손 | 철손 |
| [2] | 전압 변동률 | 전압 변동률 |
| [3] | 동손 | 동손 |
| [4] | **절연내력** | **철손내력** ← OCR 오류 |

원본 보기 [4] = **"절연내력"**. questions.json의 "철손내력"은 OCR 오류 확정
(절→철, 연→손). feasibility review §3-A의 추정(solution 본문 "절연내력")이 원본
PDF로 **확증**됨.

---

## 4. questions.json 현재 상태와의 차이

| 필드 | questions.json 현재 | 원본 PDF / 공식 | 판정 |
|---|---|---|---|
| `answer` | **2** (전압 변동률) | **4** (절연내력) | **오류 확정** |
| `choices[3]` | "철손내력" | "절연내력" | OCR 오류 확정 |
| `choices[0..2]` | 철손 / 전압 변동률 / 동손 | 동일 | 정합 |
| `text` | 변압기의 무부하시험, 단락시험에서 구할 수 없는 것은? | 동일 | 정합 |

핵심: `answer` 필드(2)가 공식 정답(4)과 어긋난다 — **answer 오류 확정**. 단,
questions.json의 `solution` 필드 본문은 "[답] (4)"로 적혀 있어 — `answer` 필드와
`solution` 필드가 서로 모순된 상태였고, 공식은 `solution` 쪽(4)이 맞다.

---

## 5. solution 혼입 여부 — 확인됨 (별도 결함, 정답 판정에 미사용)

questions.json `2010_2회_47` `solution` 필드 후반에 본 문제와 무관한
문제("3000V, 60Hz, 8극, 100kW 3상 유도전동기 ... 전부하 회전수")와 풀이가 혼입돼
있다. 원본 PDF 대조 결과 이는 **문제 48**(원본 PDF에서 문제 47 바로 다음 문항,
[답] ④)의 내용으로, 인접 문항이 47의 solution 필드에 함께 추출된 **추출 단계
오류**다.

- 본 혼입은 정답 판정 근거로 **사용하지 않았다** — 정답 판정은 원본 PDF의 문제
  47 문제·보기·풀이로만 수행.
- 혼입은 별도 데이터 결함으로 **logging**: `2010_2회_47` solution 필드에 문제 48
  (유도전동기 회전수) 내용 혼입 → cleanup 시 47 풀이만 남기고 48 내용 제거 대상.

---

## 6. 분기 판정 — **분기 2**

post-closeout errata가 제시한 4개 분기 중:

| 분기 | 조건 | 해당 |
|---|---|---|
| 1 | 공식 정답 (2) | ✗ |
| **2** | **공식 정답 (4)** | **✅ 해당** |
| 3 | (2)/(4) 둘 다 아님 | ✗ |
| 4 | source 접근 실패 | ✗ (원본 PDF 접근 성공) |

분기 2 — 공식 정답 (4):
- `answer` 필드(2) 오류 확정.
- study set v1·day plan·learning log v1.1이 기기-18을 정답 (2)로 학습 —
  **오답 학습 상태 확정**.
- 기기-18 **blocked 유지**.
- questions.json 수정 승인 요청 또는 needs_replacement 트랙 필요.

---

## 7. 다음 조치 권고

원본 PDF 대조 결과 **기출 문항 자체는 건전하다** — 문제·보기·풀이·정답이 원본에
명확히 인쇄돼 있고, 절연내력 정답은 표준이며, 기기-18(변압기 등가회로, adjacent —
시험-파라미터 식별) trap 검증에도 정답 (4) 기준으로 그대로 유효하다. 결함은
questions.json **추출 데이터**(answer 필드·choice[4] OCR·solution 혼입)에 한정된다.

→ **needs_replacement 불필요. questions.json 정정 트랙 권고.**

| 우선순위 | 조치 | 대상 (수정은 별도 승인) |
|---|---|---|
| 1 | questions.json `2010_2회_47` 정정 승인 요청 | `answer` 2→4 / `choices[3]` "철손내력"→"절연내력" / `solution` 문제 48 혼입 제거 |
| 2 | B-pilot 기기-18 학습 카드 재작성 | study set v1·day plan·learning log v1.1의 기기-18 카드를 정답 **(4) 절연내력** 기준으로 재작성 — 현재 (2) 전압변동률 기준 내용 전면 교체 |
| 3 | 재작성 후 기기-18 blocked 해제 | 카드 재작성·questions.json 정정 완료 후 redryrun 재검증 → blocked → 사용 가능 전환 |

본 검증 문서는 판정까지 — questions.json·학습 패키지 수정은 별도 승인 트랙.

---

## 8. B-Pilot Clean Count 영향

post-closeout errata의 count는 **변동 없음** — 기기-18은 errata 시점에 이미
blocked였고, 본 검증은 그 blocked를 "검증 대기"에서 **"정답 오류 확정"**으로
확정했을 뿐이다.

| 분류 | 항 / 문제 | 비고 |
|---|---|---|
| A-priority (유지) | 26 / 31 | 변동 없음 |
| 확정 클린 (사용 가능, blocked 제외) | 35 / 40 | 기기-17 caution 1/1 포함 |
| 기기-17 caution | 1 / 1 | 사용 가능 |
| 기기-18 blocked | 1 / 1 | **정답 오류 확정** — answer (2)→(4) |
| 합계 | 36 / 41 | — |

- B-pilot 사용 가능 = 9항 (8 클린 + 기기-17 caution). 기기-18 1항 보류 유지.
- 변경점: 기기-18 blocked의 성격이 "정답 충돌(미확정)" → **"공식 정답 (4) 확정,
  answer 필드 오류 확정"**. count 수치는 동일, 상태는 firming.
- closeout의 9항 체계 유지.

---

## 자체 점검

| 점검 항목 | 결과 |
|---|---|
| source별 확인 결과 | ✅ §1 — 원본 PDF 직접 조회, 별도 정답표 미대조 명시 |
| 공식 정답 판정 | ✅ §2 — (4) 절연내력 |
| 원본 PDF 보기 [4] 실제 문구 | ✅ §3 — "절연내력" (questions.json "철손내력" OCR 오류) |
| questions.json 현재 상태와의 차이 | ✅ §4 — answer 2 vs 4, choice[4] garble |
| solution 혼입 여부 | ✅ §5 — 문제 48 혼입 확인, 정답 판정에 미사용, 별도 logging |
| 4개 분기 중 판정 | ✅ §6 — 분기 2 (공식 정답 4) |
| 다음 조치 권고 | ✅ §7 — questions.json 정정 트랙 + 학습 카드 재작성, needs_replacement 불필요 |
| B-pilot clean count 영향 | ✅ §8 — count 불변, 기기-18 blocked 확정 |
| 추정 확정 회피 | ✅ 원본 PDF source 대조로 확정 — 추정 아님 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-18 `2010_2회_47` 공식 정답 검증 완료 — 원본 PDF `data/문제_2010_2회_
  20260316.pdf` 직접 대조.
- **공식 정답 = (4) 절연내력** (분기 2). questions.json `answer`(2) 오류 확정,
  `choices[3]` "철손내력"="절연내력" OCR 오류 확정.
- solution 필드 문제 48(유도전동기) 혼입 확인 — 정답 판정에 미사용, 별도 결함
  logging.
- B-pilot study set v1·day plan·learning log v1.1은 기기-18을 정답 (2)로 학습 —
  오답 학습 상태 확정.
- 권고: questions.json 정정 승인 트랙(answer 2→4 / choice[4] / solution 정리) +
  기기-18 학습 카드 (4) 기준 재작성. 기출 문항 자체는 건전 — needs_replacement
  불필요.
- clean count: A 26/31 유지, 확정 클린 35/40, 기기-17 caution 1/1, 기기-18
  blocked 1/1 — 수치 불변, 기기-18 상태 firming.
- 이 문서는 검증 문서다. questions.json·학습 패키지 미수정.
