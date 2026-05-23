# Trap-Map B-Priority — 기기-18 Redryrun After Correction (2026-05-23)

correction plan(`d1ca5b2`) Step 4 — Commit A(`6218d85`)·B(`753a9b2`)로 정정한
기기-18 대표 기출 `2010_2회_47`을 redryrun으로 재검증한다. 본 단계는 검증
문서만 — 학습 패키지·closeout/errata·questions.json 추가 수정 없음.

본 단계는 redryrun 검증 문서 작성까지 — app/data·questions.json 미수정.
solution/steps 미적용. answer/choices/text 미수정. 학습 패키지 문서 미수정.
유료 API 미호출. local server 미실행. amend/rebase/reset 없음.

- 검증 대상: 기기-18 변압기 등가회로 / 대표 기출 `2010_2회_47`
- 참조:
  - correction plan (`docs/audit/trap_map_B_priority_gigi_18_correction_plan_2026-05-23.md`)
  - Commit A evidence supplement (`docs/audit/trap_map_B_priority_gigi_18_commitA_evidence_supplement_2026-05-23.md`)
  - Commit B evidence supplement (`docs/audit/trap_map_B_priority_gigi_18_commitB_evidence_supplement_2026-05-23.md`)
  - official answer verification (`docs/audit/trap_map_B_priority_gigi_18_official_answer_verification_2026-05-22.md`)
  - 원래 1차 redryrun (`docs/audit/trap_map_B_priority_10_item_representative_redryrun_2026-05-22.md`)
  - 원본 PDF: `data/문제_2010_2회_20260316.pdf` page 8, 문제 47

---

## 결론: **ready_with_note** — 데이터 정합 PASS, 학습 패키지 정정(Step 5) 후 blocked 해제

정정된 `2010_2회_47` 레코드는 text·choices·answer·solution 모두 원본 PDF
문제 47과 정합한다. trap alignment는 **adjacent** 유지(1차 redryrun과 동일).
판정 **ready_with_note** — 데이터 부분에서 redryrun PASS. 단 학습 패키지 문서
(study set v1·day plan·learning log v1.1)가 아직 구 정답 (2) 기준이므로 기기-18
**blocked는 Step 5 이후로 해제** 보류한다.

steps 필드는 여전히 유도전동기(문제 48) 내용으로 오염된 상태 — Commit A/B
범위 외였고(plan §3.2), 별도 cleanup 트랙으로 logging만.

---

## 1. questions.json 현재 상태 (직접 조회)

`app/data/questions.json`의 `2010_2회_47` 레코드 — `python3 json.load` 후 출력:

| 필드 | 값 | 정정 여부 |
|---|---|---|
| year / session / q_no | 2010 / "2회" / 47 | 미변경 |
| subject | "전기기기" | 미변경 |
| tag | "변압기의 등가회로" | 미변경 |
| q_type | "개념형" | 미변경 |
| difficulty | 3 | 미변경 |
| quality | "complete" | 미변경 |
| text | "변압기의 무부하시험，단락시험에서 구할 수 없는 것은？" | 미변경 |
| choices[0] | "철손" | 미변경 |
| choices[1] | "전압 변동률" | 미변경 |
| choices[2] | "동손" | 미변경 |
| choices[3] | **"절연내력"** | **Commit A 정정** ("철손내력"→"절연내력") |
| answer | **4** | **Commit A 정정** (2→4) |
| solution | (아래 §1.1 전문) | **Commit B 정정** (Part 2 제거 + OCR 미세 정리) |
| steps | 유도전동기 내용 (인식·변환·계산 3 sub-key 전부) | **미정정 — 별도 트랙** |
| solution_svg | "정답: ④ 절연내력" 표시·"무부하 시험"·"절연 내력" 키워드 포함 (3243 자) | 미변경 — 이미 정답 (4) 정합 |

### 1.1 solution 전문

```
변압기의 시험
（1）개방 회로 시험（무부하 시험）으로 측정할 수 있는 항목
－무부하 전류－히스테리시스손－와류손
－여자 어드미턴스－철손
（2）단락 시험으로 측정할 수 있는 항목
－임피던스 와트（전부하 동손）－임피던스 전압（전압 강하）

그러나，절연내력은 절연재의 종류에 따라 정해지는 것으로서 무부하 시험과 단락시험으로는 구할 수 없다．
［답］（4）
```

길이 194자. 문제 47 풀이만 포함, 문제 48 혼입 0건 확인.

### 1.2 Part 2 markers 확인 (전부 0 hits)

| 마커 | solution 내 존재? |
|---|---|
| `483000` | False |
| `유도 전동기` | False |
| `회전수는` | False |
| `문제 \(` | False |

### 1.3 PDF keywords / OCR garbles

| PDF keyword | 존재? |
|---|---|
| `변압기의 시험` | True |
| `히스테리시스손` | True |
| `철손` | True |
| `절연내력` | True |
| `[답](4)` (전각 표기) | True |
| `무부하 시험` | True |

| OCR garble (이전 결함) | 존재? |
|---|---|
| `시혐` | False (정정됨) |
| `히스태리시스솜` | False |
| `철솜` | False |
| `무부 하 시험` | False |

→ solution 정합 ✅, OCR garble 모두 제거 ✅.

### 1.4 미정정 결함 — steps 필드

`steps` 필드는 Commit A/B 범위 외였고(plan §3.2), 정정되지 않았다. 현재 내용:

| sub-key | 첫 200자 |
|---|---|
| 인식 | "문제는 \"유도 전동기의 전부하 회전수\"를 구하는 것으로, 변압기 문제가 아닌 유도 전동기 문제입니다. 핵심 키워드는 \"3상 유도 전동기\", \"전부하 동손\", \"기계손\"이며 ..." |
| 변환 | "유도 전동기의 에너지 평형식을 이용합니다.\n\n**동기속도**: $N_s = \\frac{120f}{P} = \\frac{120 \\times 60}{8} = 900 \\text{ [rpm]}$ ..." |
| 계산 | "$N_s = 900$ [rpm]\n\n$P_2 = 100 - 3 - 2 = 95$ [kW]\n\n$s = \\frac{P_{cu2}}{P_2} = \\frac{3}{95} = 0.0316$ ... **정답: (4) 약 874[rpm]**" |

→ steps 3개 sub-key 전부 유도전동기(문제 48) 내용. **별도 cleanup 트랙 필요**.
text·choices·answer·solution의 정답 (4) 절연내력과 steps의 (4) 약 874[rpm]은
번호는 같으나 내용이 어긋남(steps의 (4)는 유도전동기 회전수 답안).

---

## 2. 원본 PDF와 정합 (재대조)

| 항목 | 원본 PDF 문제 47 | questions.json 현재 | 정합 |
|---|---|---|---|
| text | "변압기의 무부하시험, 단락시험에서 구할 수 없는 것은?" | "변압기의 무부하시험，단락시험에서 구할 수 없는 것은？" | ✅ (괄호 폭 차이만, 의미 동일) |
| choice [1] | "철손" | "철손" | ✅ |
| choice [2] | "전압 변동률" | "전압 변동률" | ✅ |
| choice [3] | "동손" | "동손" | ✅ |
| choice [4] | "절연내력" | "절연내력" | ✅ (정정 후) |
| 정답 | ④ | 4 | ✅ (정정 후) |
| 풀이 | 무부하시험 측정 항목(철손 등) + 단락시험 측정 항목(동손 등) + 절연내력 별도시험 + [답] ④ | (§1.1 solution 전문) | ✅ (정정 후, 절별 1:1 매핑) |

→ text·choices·answer·solution 4 필드 모두 원본 PDF와 정합.

---

## 3. trap alignment 재판정

### 3.1 입력

- **v3.2 기기-18 카드 원래 함정**: "1차 환산값과 2차 실제값을 혼동하는 보기" (1차/2차 환산 혼동).
- **대표 기출이 검증하는 함정 (정정 후)**: "무부하시험·단락시험에서 구할 수 없는 것" → 정답 (4) 절연내력. 변압기 시험-측정 항목 매핑 + 절연내력은 별도 시험이라는 인식 검증.

### 3.2 두 함정의 관계

| 측면 | 원래 카드 함정 | 대표 기출이 검증하는 함정 |
|---|---|---|
| 주제 | 변압기 등가회로 (1차↔2차 환산 일관성) | 변압기 시험 (어떤 시험으로 무엇을 구하는가) |
| 검증 메커니즘 | 환산값과 실제값을 혼동하는 보기 식별 | 시험 범위 밖 항목(절연내력) 식별 |
| 같은 광역 주제? | 둘 다 변압기 등가회로 단원 | 같은 단원의 인접 하위 함정 |

→ 정정 전 1차 redryrun의 판정(**adjacent** — "이 기출은 시험-파라미터 식별을
검증, v3.2 환산 혼동 함정은 별도")이 정정 후에도 그대로 유지된다. 정답이 (2)
전압변동률에서 (4) 절연내력으로 바뀌어도 *검증 메커니즘의 축*은 동일하게
"시험-측정 항목 매핑" — adjacent로 같은 분류.

### 3.3 trap alignment 판정: **adjacent** (유지)

- exact 아님: v3.2 카드의 *대표 보기 함정*(1차/2차 환산 혼동)을 직접 검증하지 않음.
- adjacent: 같은 변압기 등가회로·시험 영역의 인접 하위 함정 검증.
- mismatch 아님: 같은 광역 주제 내, 검증 축이 다를 뿐.

(정정 전 정답 (2) 전압변동률 기준에서는 "어떤 시험으로 무엇을 구하는가" 식별 →
adjacent. 정정 후 정답 (4) 절연내력 기준에서는 "시험 범위 밖 항목 식별" → 같은
adjacent 영역. 분류 변동 없음.)

---

## 4. Redryrun 판정: **ready_with_note**

| 평가 축 | 결과 | 사유 |
|---|---|---|
| text·choices·answer·solution PDF 정합 | ✅ PASS | §2 참조 |
| OCR garble 제거 | ✅ PASS | §1.3 4종 모두 제거 |
| Part 2 혼입 제거 | ✅ PASS | §1.2 4 마커 모두 0 |
| 정답 ↔ solution 내적 일관성 | ✅ PASS | answer=4 + solution [답](4) 일치 |
| solution_svg 정답 정합 (참고) | ✅ 이미 (4) 정합 | 정정 전부터 "정답: ④ 절연내력" |
| trap alignment | adjacent | §3 — 1차 redryrun과 동일 분류 |
| **steps 필드 정합** | **❌ FAIL** | §1.4 — 유도전동기 내용 잔존, **별도 cleanup 트랙 필요** |

### 판정 사유

- text·choices·answer·solution은 정정으로 PDF 정합·내적 일관성 모두 PASS →
  데이터 부분의 source-clean 충족.
- trap alignment adjacent → 학습 카드에서 "원래 카드 함정 ≠ 기출 함정" 분리 표기
  필요. 이는 1차 redryrun에서도 부여한 ready_with_note 사유.
- steps 필드 잔존 결함 → ready_with_note의 두 번째 사유. 학습 패키지 카드는
  questions.json의 steps를 직접 노출하지 않으므로 학습 자체 영향 없으나, 데이터
  무결성 차원에서 별도 cleanup 트랙 필요.

→ **판정: ready_with_note**. needs_replacement 아님 (대표 기출은 source-clean·
정답 정합·trap alignment 모두 사용 가능). defer 아님 (이미 검증 완료, 후속 작업
경로 명확).

---

## 5. B-pilot 영향

### 5.1 blocked 해제 조건

post-closeout errata(`0045ce4`)에서 기기-18을 blocked로 분류한 사유는:
- `answer`(2)와 공식 정답(4) 충돌
- choice[4] OCR garble
- 학습 패키지가 정답 (2)로 가르치는 상태

| 사유 | 정정 후 상태 |
|---|---|
| answer ↔ 공식 정답 충돌 | ✅ 해소 (Commit A, answer=4) |
| choice[4] OCR | ✅ 해소 (Commit A, "절연내력") |
| 학습 패키지가 정답 (2)로 가르침 | **❌ 미해소** — study set v1·day plan·learning log v1.1 모두 구 정답 (2) 기준 |

→ **questions.json 데이터 부분의 blocked 사유는 모두 해소**되었으나, **학습
패키지 정정(Step 5) 전에는 blocked 유지** — 학습자가 학습 패키지를 따르면 여전히
정답 (2)로 학습하므로 사용 보류 사유가 살아 있음.

### 5.2 본 redryrun에서 blocked 해제 행사하지 않음

본 문서는 데이터 redryrun 검증만 — clean count·blocked 해제는 Step 7
(closeout/errata 후속 erratum)에서 학습 패키지 정정 완료 확인 후 일괄 갱신.
post-closeout errata `0045ce4`의 count(확정 클린 35/40 / 기기-18 blocked 1/1)는
본 redryrun 시점에 그대로 유지.

---

## 6. 다음 조치

| 우선순위 | Step | 작업 | 상태 |
|---|---|---|---|
| 1 | Step 5 | study set v1·day plan·learning log v1.1의 **기기-18 카드 정답·외울 핵심·체크 질문·예상 오답 패턴·라벨을 (4) 절연내력 기준으로 재작성** (별도 명시 승인 필요) | 대기 |
| 2 | Step 6 | 학습 패키지 정정본 review | 대기 |
| 3 | Step 7 | closeout/post-closeout errata 후속 erratum + clean count 갱신(기기-18 blocked → ready_with_note·clean 전환 결정) | 대기 |
| (별도) | steps 필드 cleanup 트랙 | `2010_2회_47.steps`를 문제 47 기준으로 재작성 (또는 비워두기). Commit A/B 범위 외였음 | 대기 |
| (별도) | 추출 파이프라인 회귀 | 인접 문항 혼입 재발 방지(steps·solution 모두) | 대기 |

### 6.1 Step 5 학습 카드 정정 시 주의

- alignment(**adjacent**)·판정(**ready_with_note**)은 본 redryrun과 동일하게 유지.
- "원래 카드 함정"(1차/2차 환산 혼동) 라인은 동일하게 유지.
- "대표 기출이 검증하는 함정" 라인을 (2) 전압변동률 → (4) 절연내력 식별 기준으로
  재작성:
  - 변경 전: "시험-파라미터 식별 — 전압변동률은 직접 측정 항목이 아님"
  - 변경 후 후보: "시험 범위 밖 항목 식별 — 절연내력은 별도 절연내력시험 필요"
- 외울 핵심 문장·3회독 체크·예상 오답 패턴 라벨([원카드]/[기출]/[core])을 (4)
  기준으로 재작성.
- adjacent 함정 분리 원칙(G-2) 유지.

---

## 7. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. questions.json 현재 상태 (answer/choices/solution/Part 2 제거) | ✅ §1 |
| 1. steps 잔존 결함 logging | ✅ §1.4 |
| 2. 원본 PDF 정합 (text/choices/answer/solution) | ✅ §2 |
| 3. trap alignment 재판정 (adjacent 유지) | ✅ §3 |
| 4. redryrun 판정 (ready_with_note) | ✅ §4 |
| 5. B-pilot 영향 — blocked 해제 조건/실행 | ✅ §5 — 데이터 해소 / 학습 패키지 정정 전까지 보류 |
| 6. 다음 조치 (Step 5 / 6 / 7 + steps cleanup) | ✅ §6 |
| 학습 패키지 미수정 | ✅ docs/audit/ 신규 1건만 |
| closeout/errata 미수정 | ✅ Step 7 보류 |
| questions.json 추가 수정 없음 | ✅ 본 단계 검증만 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-18 `2010_2회_47` 정정 후 redryrun 검증 완료 — 데이터 부분 정합 PASS.
- text·choices·answer·solution 모두 원본 PDF 문제 47과 정합. OCR garble 4종·
  Part 2 혼입 마커 4종 전부 0 hits. answer(4) ↔ solution [답](4) 내적 일관성
  확보.
- trap alignment: **adjacent** 유지(1차 redryrun과 동일 분류). 정답 (2)→(4) 변경이
  검증 축(시험-측정 항목 매핑)을 바꾸지 않음.
- 판정: **ready_with_note** — 사유 (a) adjacent 함정 분리 필요, (b) steps 필드
  잔존 결함(별도 cleanup 트랙).
- B-pilot blocked 해제 조건 중 데이터 부분은 모두 해소, 학습 패키지(구 정답 (2)
  기준)는 미정정 — **blocked는 Step 5 학습 카드 정정 후 해제** 보류. 본 redryrun
  시점에 clean count 갱신 없음(Step 7 일괄).
- 잔존 트랙: Step 5 학습 카드 정정 / Step 6 review / Step 7 errata 갱신 + steps
  cleanup 별도 트랙.
- 이 문서는 redryrun 검증 문서다. questions.json·학습 패키지·closeout 미수정.
