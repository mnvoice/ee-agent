# Trap-Map B-Priority — 기기-17 Correction Plan (2026-05-23)

기기-17 record identity targeted audit(`13edae5`)에서 변압기 Δ-Y 권수비 문제의
true source를 확정한 뒤, 데이터·학습 패키지 수정 *전 단계*로 작성하는 correction
plan 문서다. 본 plan은 수정 범위·승인 범위·실행 순서·후속 문서 재작성 범위·
위험 관리를 명문화한다.

이번 단계는 plan 작성만 — **app/data·questions.json·id·학습 패키지 문서 미수정**.
solution/steps 미적용. answer/choices/text 미수정. 유료 API 미호출. local server
미실행. 데이터·학습 패키지 수정은 본 plan 승인 후 별도 트랙·별도 commit으로
진행. 기존 commit amend/rebase/reset 없음.

- 검토 대상: 기기-17 변압기 Δ-Y 권수비 / 대표 기출 `2020_1회_52`
- 참조:
  - record identity targeted audit (`docs/audit/trap_map_B_priority_gigi_17_record_identity_targeted_audit_2026-05-23.md`, `13edae5`)
  - record identity normalization plan (`docs/audit/trap_map_B_priority_gigi_17_record_identity_normalization_plan_2026-05-23.md`, `538c9c6`)
  - cleanup feasibility review (`docs/audit/trap_map_B_priority_gigi_17_cleanup_feasibility_2026-05-23.md`, `2bfc065`)
  - 기기-18 correction plan 양식 참조 (`docs/audit/trap_map_B_priority_gigi_18_correction_plan_2026-05-23.md`)
  - 원본 PDF (true source): `data/20200424_1회.pdf` (파일명 ↔ 표지 기재 일자 불일치, 강한 가설: 1자 typo; 표지 기재 일자 = 2022-04-24) page 4 문제 52

### 표현 정책 (본 plan 전반 적용)

본 plan은 N1 audit이 직접 확인한 사실과 강한 가설을 다음과 같이 분리 표기한다:

| 사실 등급 | 표기 | 적용 대상 |
|---|---|---|
| (a) 직접 확인 | 단정 표기 ("확정", "정합") | PDF p.4 q52 본문·choices·정답 ↔ questions.json `2020_1회_52` 일치 |
| 강한 가설 | "강한 가설" 라벨 | PDF 파일명 `20200424` ↔ 표지 기재 일자 `2022-04-24`의 1자 typo 해석 |
| (c) 추정 | "가능성"·"확인 필요" 라벨 | per-year 100항이 모두 2022 1회 컨텐츠라는 확장 (q41·q52 sanity check 외 미검증) |

PDF 날짜는 "표지 기재 일자"로 표기한다 (PDF 표지가 "2022년 04월 24일 필기
기출문제"로 인쇄되어 있다는 (a) 사실. 시행 일자가 실제로 2022-04-24인지는 외부
일자 정합 별도 검증 영역).

---

## 0. 개념 혼동 방지 라벨 (G-4)

본 plan이 다루는 학습 내용의 영역을 다음과 같이 명시 한정한다. 검색·grep·매칭·
정정 작업에서 다음 영역을 혼동하지 않는다.

| 라벨 | 영역 | 본 plan 대상? |
|---|---|---|
| **변압기 Δ-Y 결선 / 권수비** | 단상변압기 3대 1차 △ · 2차 Y 결선의 권수비 계산 (V·I 변환) — 기기-17 본 케이스 | ✅ **본 plan 대상** |
| 유도전동기 Y-Δ 기동 | 유도전동기 기동 시 권선을 Y로 시작 → 운전 시 Δ로 전환하는 기동 방식 | ❌ 본 plan 대상 아님 |
| 동기전동기 V곡선 | 동기전동기 여자전류 변화에 따른 전기자전류 변화 곡선 (`2020_1,2회_52`의 별 컨텐츠) | ❌ 본 plan 대상 아님 |

핵심 구분:
- "Δ-Y"가 동일 표기로 등장해도 **변압기 결선 (정상상태 권수비)** 과 **유도전동기
  기동 방식 (과도상태 전류 제한)** 은 별 영역.
- 기기-17은 **정상상태 변압기 결선 / 권수비 / 정답 ①** 영역만 다룬다.
- 동기전동기 V곡선은 별 record(`2020_1,2회_52`)의 컨텐츠로, 본 plan의 정정 대상
  아님 — A-track·B-track 어느 쪽도 동기전동기 V곡선 record를 건드리지 않는다.

검색·매칭 시 위 라벨 외 영역(`기동`, `V곡선`, `여자전류` 등)이 hit으로 잡히면 본
plan 범위 외로 분류한다.

---

## 1. 현재 문제 요약

### 1.1 결함 표

| 결함 ID | 위치 | 현재 값 | 원본 PDF 기준 | 분류 |
|---|---|---|---|---|
| D-1 | `2020_1회_52` `choices[0]` (보기 [1]) | 잉여 `\sqrt{3}` 포함 LaTeX (`\sqrt{3}\frac{aV}{\sqrt{3}}…`) | `aV/√3 (V), √3I/a (A)` | choice OCR artifact |
| D-2 | `2020_1회_52` `solution` | 전류식 `I/(√3a)` 형태 오기 | `√3I/a` (정답 ① 선택지와 정합) | solution 전류식 오류 |
| D-3 | `2020_1회_52` `year`·`session` 메타 | `year=2020, session="1회"` | 원본 PDF 표지 기재 일자 = 2022-04-24 (시행 시기 강한 가설: 2022년 1회) | record meta/source identity mismatch |
| D-4 | per-year 파일 `data/questions_기출_2020_1회.json` (100 records) | 전수가 같은 PDF에서 추출됐을 가능성 (N1 audit §4 q41 sanity check) | 모두 2022 1회 컨텐츠일 가능성 (확정은 N3b 전수 sanity check 후) | systemic mis-attribution (D-3 상위 원인) |
| D-5 | PDF 파일 `data/20200424_1회.pdf` | 파일명에 "20200424" | PDF 표지 기재 일자 "2022년 04월 24일 필기 기출문제" | filename ↔ 표지 기재 일자 불일치 (강한 가설: 1자 typo, D-3·D-4 상위 원인) |

### 1.2 caution 상태 — 본 결함이 유지시키는 영역

trap-map 기기-17은 현재 **caution 1항/1문제 단독**(blocked 0). 학습 내용 (변압기
Δ-Y 권수비 / 정답 ① / aV/√3·√3I/a) 자체는 valid — D-1 + D-2가 정정되면 보기·풀이
표기가 PDF와 정합, D-3 또는 D-4·D-5가 정정되면 record identity가 PDF와 정합.
즉 caution 사유 3개가 정정 가능하다는 것이 N1 audit으로 확정된 상태.

### 1.3 학습 패키지 영향

B-pilot 학습 패키지(study set v1·day plan·learning log v1.1·closeout·post-closeout
errata·관련 review)는 기기-17 카드를 "대표 기출 `2020_1회_52`"로 표기하고, 정답 ①
변압기 Δ-Y 권수비를 학습 내용으로 함. 학습 내용의 trap alignment·판정·외울 항목은
PDF와 정합이지만, **대표 기출 표기와 보기 [1] 잉여 √3 / solution 전류식 표기**가
PDF 원본과 어긋남. 카드의 trap alignment·핵심 학습 문장은 유지하되, 대표 기출 id·
보기 [1] 표기·solution 표기를 정정해야 한다.

---

## 2. N1 Audit Evidence 요약

본 plan이 기반으로 하는 N1 audit(`13edae5`) 핵심 evidence:

### 2.1 True source 확정 evidence

| 단계 | 출처 | 결과 |
|---|---|---|
| corpus exact match | questions.json 5,331 + per-year 74 + mathpix 65 OCR PDFs | 1 hit (`2020_1회_52` 자체), 다른 PDF 후보 0건 |
| `data/문제_2020_1,2회_20260316.pdf` (실제 2020 1·2회 합본) q52 | direct mathpix | 동기전동기 V곡선 — 다른 문제 |
| `data/20200424_1회.pdf` p.4 q52 | direct Read | **본문·choices·정답 questions.json `2020_1회_52`와 직접 일치** |
| PDF 표지 기재 일자 | direct Read | "2022년 04월 24일 필기 기출문제" — 파일명 "20200424"는 강한 가설로 typo |

→ **확정 (a)**: 기기-17 변압기 Δ-Y 권수비 문제 본문·choices·정답이 PDF
`data/20200424_1회.pdf` p.4 q52와 일치. 정답 ①, choice ① text = `aV/√3 (V),
√3I/a (A)`. PDF 표지 기재 일자 = "2022년 04월 24일".

→ **강한 가설**: PDF 파일명 "20200424"가 표지 기재 일자 "2022-04-24"의 1자
typo이며, 시행 시험 = 전기기사 2022년 1회. (시행 일자 외부 정합 검증은 별
트랙. 본 plan 범위 외.)

### 2.2 100항 mis-attribution 가능성 evidence (D-4)

q52 외 q41 spot check:
- PDF `data/20200424_1회.pdf` p.4 문제 41 (3과목 전기기기 첫 문제 — 비정현파 무부하손)
- questions.json `2020_1회_41` text·정답 동일 → PDF에서 추출 일치

같은 PDF에서 추출된 연속 100항이므로 `data/questions_기출_2020_1회.json` 100
records 전수가 2022 1회 컨텐츠일 가능성 매우 높음 (완전 전수 검증은 N3b 트랙으로
분리).

### 2.3 `2020_1회_52` vs `2020_1,2회_52` 관계

`2020_1,2회_52`(동기전동기 V곡선)는 별 출처 PDF(`문제_2020_1,2회_20260316.pdf` —
실제 2020 1·2회 합본)에서 추출 — 같은 q_no 슬롯에 다른 PDF의 다른 문제가 들어간
구조. duplicate 식별자 아님. 본 plan의 정정 범위와 충돌 없음.

### 2.4 2022 1회 슬롯 비어 있음 — 재attribution 안전

questions.json 전수 grep 결과 `year=2022, session="1회"` record 0건. 즉 D-3 메타
정정 시 record id 재attribution(`2020_1회_*` → `2022_1회_*`) 충돌 없음 — id 정정의
산술적 안전성 확보. (단 app routing/storage key 영향은 별 검증 필요. 본 plan §6.4
참조.)

---

## 2A. G-1 — Identity Claim Evidence (5축 stand-alone)

§2 evidence 요약을 5축 stand-alone 첨부로 보강한다. 본 §2A는 N1 audit
(`13edae5`)에서 직접 측정한 evidence를 plan 본문에 (a) 출처로 박아 두기 위한
섹션이다. 후속 트랙(N3a~N5)에서 evidence 재참조 시 본 섹션이 stand-alone 인용
근거가 된다.

### 2A.1 축 ① — questions.json `2020_1회_52` 본문 발췌

**출처**: `app/data/questions.json` (master, 5,331 records)
**record key**: `2020_1회_52` (year=2020, session="1회", q_no=52)

본문 (text):
```
권수비가 a인 단상변압기 3대가 있다. 이것을 1차에 △, 2 차에 Y로 결선하여
3상 교류 평형회로에 접속할 때 2차측의 단자전압을 V(V), 전류를 I(A)라고
하면 1차측의 단자전압 및 선전류는 얼마인가? (단, 변압기의 저항,
누설리액턴스, 여자전류는 무시한다.)
```

선택지 (choices):
- [1] `\sqrt{3}\frac{aV}{\sqrt{3}}\text{(V)}, \frac{\sqrt{3}I}{a}\text{(A)}` (잉여 `\sqrt{3}` artifact 포함)
- [2] `\sqrt{3}aV\text{(V)}, \frac{I}{\sqrt{3}a}\text{(A)}`
- [3] `\frac{\sqrt{3}V}{a}\text{(V)}, \frac{aI}{\sqrt{3}}\text{(A)}`
- [4] `\frac{V}{\sqrt{3}a}\text{(V)}, \sqrt{3}aI\text{(A)}`

정답 (answer): `1`

solution (인용 — 결함 D-2 포함):
> 전류식이 `I/(√3a)` 형태로 작성됨 — 정답 ① 선택지 `√3I/a`와 어긋남.

### 2A.2 축 ② — 원본 PDF page 4 q52 발췌

**출처**: `data/20200424_1회.pdf` (파일명 ↔ 표지 기재 일자 불일치, 강한 가설:
typo) page 4, 3과목 전기기기 영역

```
52. 권수비가 a인 단상변압기 3대가 있다. 이것을 1차에 △, 2 차에 Y로 결선하여
    3상 교류 평형회로에 접속할 때 2차측의 단자전압을 V(V), 전류를 I(A)라고
    하면 1차측의 단자전압 및 선전류는 얼마인가? (단, 변압기의 저항,
    누설리액턴스, 여자전류는 무시한다.)

  ❶ aV/√3 (V), √3I/a (A)
  ② √3aV(V), I/(√3a)(A)
  ③ √3V/a (V), aI/√3 (A)
  ④ V/(√3a)(V), √3aI(A)
```

표기 convention: `❶` = 전자문제집 CBT(www.comcbt.com) 정답 표기. 정답 = ①.

### 2A.3 축 ③ — PDF 표지 "2022년 04월 24일" 발췌

**출처**: `data/20200424_1회.pdf` 모든 페이지 상단 footer (직접 Read)

```
전기기사    ◐ 2022년 04월 24일 필기 기출문제 ◑    전자문제집 CBT : www.comcbt.com
```

- 표지 기재 일자 = **2022년 04월 24일** (a) 직접 확인
- 파일명 `20200424` ↔ 표지 기재 일자 `20220424` (강한 가설: 1자 typo)
- 시행 시험 시기 외부 일자 정합은 별 트랙 (본 plan 범위 외)

### 2A.4 축 ④ — q41 sanity check 결과

**출처**: `data/20200424_1회.pdf` p.4 문제 41 (3과목 전기기기 첫 문제) ↔
questions.json `2020_1회_41` 비교

PDF p.4 문제 41 인용:
```
41. 단상 변압기의 무부하 상태에서 V1 = 200sin(ωt+30°)(V) 의 전압이 인가되었을
    때 I0 = 3sin(ωt+60°) + 0.7sin(3ωt+180°)(A) 의 전류가 흘렀다. 이때 무부하손은
    약 몇 W인가?  ❷ 259.8
```

questions.json `2020_1회_41`:
- tag: '비정현파의 소비전력 계산'
- text: "단상 변압기의 무부하 상태에서 V1 = 200sin(ωt+30°)(V)의 전압이 인가되었을
  때 Io = 3sin(ωt+60°) + 0.7sin(3ωt+180°)(A) 의 전류가 흘렀다. 이때 무부하손은 약
  몇 W..."

→ 본문·정답 동일. 같은 PDF 출처임이 확정. 단 N1 audit이 검증한 record는 q41·q52
2건뿐 — `data/questions_기출_2020_1회.json` 전체 100항이 모두 2022 1회 컨텐츠라는
것은 (c) 추정 (강한 추정이나 미확정).

### 2A.5 축 ⑤ — questions.json year=2022, session="1회" count = 0 측정

**측정 명령** (jq):
```bash
jq '[.[] | select(.year == 2022 and .session == "1회")] | length' \
   app/data/questions.json
```

**N1 audit 측정 결과**: `0`

**해석**:
- `year=2022, session="1회"` 슬롯이 questions.json에 비어 있음
- D-3 메타 정정 시 record id 재attribution(`2020_1회_N` → `2022_1회_N`) 산술적
  충돌 0건
- 단 storage key·app routing 영향은 별 차원 (G-2 측정 영역, §6.4 + §9)

**재측정 요구**: B-track 진입 전 본 측정을 다시 실행하여 (a) 출처로 재확인 후
G-5 식별 키 정책 결정.

### 2A.6 G-1 통과 기준

위 5축이 모두 (a) 출처로 기록되어 있고 강한 가설(파일명 typo)이 (a) 사실과 분리
표기되어야 G-1 통과. G-1 미통과 시 A-track·B-track 어느 쪽도 진입 금지.

---

## 3. Correction Path 분리 (A-track / B-track)

기기-17 결함은 **표기 차원**과 **데이터 메타 차원**으로 분리됨. 두 차원은 위험도·
범위·승인 단위가 달라 별 트랙으로 처리한다.

### 3.1 A-track — 학습 패키지 표기 정정 (즉시 실행 권장, 위험 낮음)

**대상**:
- 학습 패키지 문서 한정 — questions.json 미수정
- 기기-17 카드 "대표 기출" 표기와 보기 [1] / solution 표기 정정

**대상 파일 후보** (실제 정정 시 파일별 grep로 확정):

| 문서 | 정정 후보 위치 |
|---|---|
| `docs/audit/trap_map_B_priority_pilot_study_set_v1_2026-05-22.md` | 기기-17 카드 "대표 기출 `2020_1회_52`" + 보기 [1] 표기 + solution 인용 |
| `docs/audit/trap_map_B_priority_pilot_day_plan_2026-05-22.md` | Day N 기기-17 카드 — 대표 기출 표기 + 외울 핵심 문장 |
| `docs/audit/trap_map_B_priority_pilot_learning_log_v1_1_2026-05-22.md` | Day N 기기-17 카드 — 대표 기출 표기 + 학습 라벨 |
| `docs/audit/trap_map_B_priority_pilot_learning_package_closeout_2026-05-22.md` | clean count·caution 항 갱신 (A-track 적용 후) |
| `docs/audit/trap_map_B_priority_post_closeout_errata_2026-05-22.md` | 후속 erratum으로 정정 trail 기록 |
| 관련 review/errata 문서 | 기기-17 언급 시 동일 정정 — grep로 식별 |

**변경 내용 후보**:

| 항목 | 변경 전 | 변경 후 |
|---|---|---|
| 대표 기출 id | `2020_1회_52` | `2022_1회_52 (시행 2022-04-24)` — 단, 본 표기는 학습 표기 차원이며 data id는 D-3 미정정 상태에서는 여전히 `2020_1회_52` |
| 보기 [1] 표기 (학습 카드 내 인용 시) | `\sqrt{3}\frac{aV}{\sqrt{3}}\text{(V)}, \frac{\sqrt{3}I}{a}\text{(A)}` (잉여 √3) | `aV/√3 (V), √3I/a (A)` — PDF 원본 정합 |
| solution 인용 (학습 카드 내) | 전류식 `I/(√3a)` 형태 | `√3I/a` — PDF 보기 ①과 정합 |
| 학습 카드 trap alignment·판정·외울 문장 | (유지) | (변경 없음) |

**A-track의 분리 commit 권고** — §6.3 참조.

#### 3.1.1 G-3 — A-track 정정 범위 whitelist

A-track 실행 시 다음 whitelist 외 어떤 파일도 수정 금지. 본 whitelist는 N3a
실행 권한 부여 시 명시 동결한다.

**수정 허용 파일 (학습 패키지 문서 3종 + 부속)**:

| 파일 (Whitelist W-1) | 정정 위치 (grep 후 확정) |
|---|---|
| `docs/audit/trap_map_B_priority_pilot_study_set_v1_2026-05-22.md` | 기기-17 카드 "대표 기출" id 표기 + 보기 [1] LaTeX 인용 + solution 전류식 인용 |
| `docs/audit/trap_map_B_priority_pilot_day_plan_2026-05-22.md` | Day N 기기-17 카드 — 대표 기출 표기 + 외울 핵심 문장 |
| `docs/audit/trap_map_B_priority_pilot_learning_log_v1_1_2026-05-22.md` | Day N 기기-17 카드 6칸 + 라벨 — 대표 기출 표기 |

**수정 허용 부속 문서**:

| 파일 (Whitelist W-2) | 정정 위치 |
|---|---|
| `docs/audit/trap_map_B_priority_pilot_learning_package_closeout_2026-05-22.md` | clean count·caution 항 갱신 (A-track 적용 후) |
| `docs/audit/trap_map_B_priority_post_closeout_errata_2026-05-22.md` | 후속 erratum으로 정정 trail 기록 |
| 관련 review 문서 (기기-17 언급 위치) | grep로 식별 후 동일 표기 정정 |

**대표 기출 표기 변경 범위**:
- 변경 전: `2020_1회_52`
- 변경 후: `2022_1회_52 (시행 시기 강한 가설; PDF 표지 기재 일자 2022-04-24)`
- 한정: 학습 카드의 *대표 기출 표기 문자열만* 변경. data record id(storage key)는
  A-track에서 변경하지 않는다 (B-track 영역).

**보기 [1] artifact 정정 범위**:
- 변경 전 (학습 카드 내 인용): `\sqrt{3}\frac{aV}{\sqrt{3}}\text{(V)}, \frac{\sqrt{3}I}{a}\text{(A)}` (잉여 `\sqrt{3}`)
- 변경 후 (학습 카드 내 인용): `aV/√3 (V), √3I/a (A)` (PDF 원본 표기 정합)
- 한정: 학습 카드 본문의 *인용 영역만* 변경. questions.json `choices[0]` 원본 필드는
  A-track에서 변경하지 않는다 (B-track·별 cleanup 트랙 영역).

**A-track 절대 금지 (G-3 violation)**:

| 영역 | 금지 사유 |
|---|---|
| `app/data/questions.json` 어떤 필드든 수정 | data 영역 — B-track 또는 별 cleanup 트랙 |
| `data/questions_기출_*.json` per-year 파일 수정 | data 영역 — B-track |
| record id / year / session / q_no | data identity — B-track + G-5 결정 필요 |
| `app/` 코드 어떤 파일 수정 | app routing 영역 — N3c 통과 후만 |
| PDF 파일 / `data/pdf_pages/*` 디렉토리 rename | B-track 영역 |
| 기기-17 외 다른 trap-map 카드 정정 | A-track scope 외 — 별 트랙 |

**A-track 산출물 버전명**:
- study set v1·day plan·learning log v1.1은 모두 PASS review 완료 — 정정 시 *별
  버전 발행* 또는 *erratum 부착* 양식 사용.
- 권장: **patch 양식 (v1.1 → v1.1.1, study set v1 → v1.0.1)** 또는 **명시 v1.2
  발행** 중 1택. N3a 실행 권한 부여 시 동결.
- 부속 후속 erratum은 별 신규 문서로 기록한다 (기존 closeout/post-closeout errata에
  trail entry 추가 또는 신규 erratum 문서).

### 3.2 B-track — questions.json 메타 normalization (app 영향 검증 후, 위험 중)

**대상**:
- `app/data/questions.json` `2020_1회_*` 100 records 메타 일괄 정정
- per-year 파일 `data/questions_기출_2020_1회.json` (100 records) 메타 일괄 정정
- PDF 파일 `data/20200424_1회.pdf` rename → `data/20220424_1회.pdf`
- 관련 pdf_pages cache 디렉토리 `data/pdf_pages/2020_1회/` → `data/pdf_pages/2022_1회/`

**변경 내용 후보** (각 record당):

| 필드 | 변경 전 | 변경 후 |
|---|---|---|
| `year` | `2020` | `2022` |
| `session` | `"1회"` | `"1회"` (변경 없음) |
| `q_no` | (변경 없음) | (변경 없음) |
| record id (storage key) | `2020_1회_N` (N=1..100) | `2022_1회_N` |

**B-track의 사전 검증 필수** — §6.4 참조. app routing/storage key/외부 reference
영향 사전 확인 안 한 채 일괄 정정 금지.

#### 3.2.1 G-5 — B-track 식별 키 정책 (3 후보, G-2 결과 후 결정)

B-track 메타 정정에서 record 식별 키(storage key)를 어떻게 처리할지 결정해야
한다. **본 plan에서는 후보 3개를 나열만 하고 결정하지 않는다.** G-2 측정 결과
(§6.4 + §9)가 보고된 후 별 명시 결정으로 1택 동결한다.

| 후보 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **K1 — id 유지 + year/session/q_no만 정정** | record id storage key는 `2020_1회_N`으로 유지하고 내부 필드 `year=2020→2022`만 정정. session/q_no는 변경 없음 | app routing·외부 reference 영향 0. 가장 안전 | id와 메타가 영구 불일치 — id가 자체 신뢰성 잃음. 향후 모든 query가 (id, year) 조합 검증 필요 |
| **K2 — id 재발급** | record id storage key를 `2020_1회_N` → `2022_1회_N`로 일괄 재발급 + year/session/q_no 메타 정정 | id와 메타 정합 회복. data 무결성 최고 | app routing·cache·외부 reference 영향 큼. N3c 영향 조사에서 변경 범위 큰 곳이 다수 나오면 마이그레이션 비용 큼 |
| **K3 — 신규 record 추가 + 기존 deprecate** | `2022_1회_N` record 100건 신규 추가, 기존 `2020_1회_N` 100건은 `deprecated: true` 플래그로 보존 | 외부 reference 호환성 유지하면서 신규 정합 record 제공. rollback 안전 | record 총수 +100 (5,331 → 5,431). 학습 진도·통계 집계 시 중복 회피 룰 필요. UI 노출 시 deprecated record 숨김 룰 필요 |

**G-5 동결 룰**:
1. 본 plan 단계에서는 K1·K2·K3 중 결정 금지.
2. G-2(§6.4) 측정 결과 보고 후, 별 명시 결정으로 1택 동결한다.
3. **G-5 결정 전 B-track 실행 진입 금지.**
4. G-5 결정은 supervisor decision log(§8)에 추가 entry로 기록.

**G-5 결정 가이드** (참고):
- N3c 측정에서 app 코드의 `2020_1회` 또는 `year=2020 AND session="1회"` 참조가
  소수 + 변경 범위 한정적이면 K2 (id 재발급) 우세.
- 참조가 다수 + 외부 학습 패키지·캐시·통계에 광범위하게 기록되어 있으면 K1 (id 유지)
  또는 K3 (신규 추가) 우세.
- K3는 데이터 양 증가 부담이 있으나 rollback 안전성이 가장 높음 — 사용자가
  보수적 선택 시 권장.

### 3.3 Option C(alias errata) / Option D(representative 교체) — A·B 결과 후 fallback 보류

N1 audit §7.4·§8 권고에 따라 본 plan은 A-track + B-track 두 갈래로 집중한다.
Option C/D는 폐기하지 않고 **fallback으로 보류**한다 — A·B 실행 결과에 따라 재
활성화 가능성이 남는다.

| 옵션 | 본 plan 상태 | 재활성화 조건 (참고) |
|---|---|---|
| **Option C (메타 정정 없이 docs에 mismatch alias 명시)** | fallback 보류 | G-5 결정에서 K1·K2·K3 모두 부적격으로 판정되면 B-track 미실행 + Option C로 docs에 alias 표기만 추가하는 보수 경로 |
| **Option D (대표 기출을 다른 회차 q로 교체)** | fallback 보류 | A-track 실행 후에도 학습 카드가 source-clean으로 수렴 안 하거나, B-track의 G-2 측정에서 100항 sanity가 폐기 수준으로 깨지면 대표 기출 자체를 별 회차 q로 교체 |

본 plan은 A-track + B-track을 우선 트랙으로 동결하되, Option C/D를 fallback
영역에 유지한다. fallback 진입 조건은 별 트랙 결정 사항.

---

## 4. 권장 실행 순서

| Step | 작업 | 산출물·검증 | 가드 |
|---|---|---|---|
| **N3a** | A-track 학습 표기 정정 plan 작성 → 승인 후 실행 (study set/day plan/learning log/관련 review·errata의 기기-17 카드 표기 정정) | 학습 패키지 정정 commit (별도) + grep 측정으로 정정 범위 확인 | 학습 표기 한정·questions.json 미수정·다른 카드 미수정 |
| **N3b** | per-year 파일 `data/questions_기출_2020_1회.json` 100 records 전수 sanity audit (각 record가 PDF `data/20200424_1회.pdf` 컨텐츠와 정합한지 sampling 또는 record별 cross-check) | sanity audit 보고서 (docs/audit/) | read-only, 데이터 미수정. 100% 정합 확인되어야 B-track 진행 |
| **N3c** | app id 참조 영향 조사 — `2020_1회_*` storage key가 app routing/cache/외부 reference에서 어떻게 사용되는지 grep | 영향 보고서 (docs/audit/) | read-only, 코드 변경 없음 |
| **N3d** | B-track questions.json 메타 normalization plan 작성 → 승인 후 실행 (questions.json + per-year + PDF + pdf_pages 일괄 정정) | B-track 실행 plan 문서 + 실행 commit 묶음 (별도) | N3b·N3c 통과 후만 실행. amend/rebase/reset 없음 |
| **N4** | 기기-17 representative redryrun — 정정 후 데이터·학습 패키지 정합 재검증 (read-only) | redryrun 문서 — (4) source-clean·정답 ① 정합·메타 정합 재확인 | 추론 금지·questions.json 미수정 |
| **N5** | clean count 갱신 판단 — 기기-17 caution 해제 가능 여부 | follow-up erratum — 사용 가능 36/41 / 완전 클린 36/41(현재 35/40 + 기기-17) 도달 가능성 검토 | 정정 trail 확인 후만 갱신 |

각 step은 별 명시 승인 후 수행. 본 plan 승인이 N3a~N5 자동 승인 아님.

### 4.1 N3a와 N3b 분리 사유

- N3a(학습 표기 정정)는 questions.json·데이터 미수정 트랙이라 위험 최소, 즉시
  학습 자료 신뢰성 회복 가능. caution의 학습 노출 영향 우선 차단.
- N3b(100항 sanity audit)는 read-only이나 시간 비용 있음. A-track 실행과 병행 가능.

A-track(N3a)을 B-track(N3b·N3c·N3d)보다 먼저 진행하는 이유: A는 단독으로 학습
영향 차단, B는 데이터 무결성 복원 트랙으로 N3b·N3c 통과를 전제로 한다.

---

## 5. 후속 학습 패키지 재작성 범위 (본 plan 단계에서는 미작성)

A-track 또는 B-track이 승인·실행되면 아래 문서들의 기기-17 항목을 정정해야 한다 —
**본 plan 단계에서는 작성하지 않는다**(plan만 정의). A-track / B-track 별 영향 범위
구분:

| 문서 | A-track 영향 | B-track 영향 |
|---|---|---|
| study set v1 | 기기-17 카드 대표 기출 표기·보기 [1]·solution 인용 정정 | (없음 — 데이터 id가 바뀌어도 학습 표기는 A에서 이미 갱신됨) |
| day plan | 기기-17 카드 표기 정정 | (없음) |
| learning log v1.1 | 기기-17 카드 6칸 + 라벨 — 표기 정정 | record id가 변경되면 학습 로그의 record 참조도 정정 가능 |
| closeout | clean count·caution 갱신 (A-track 적용 후 caution 부분 해제 가능 여부) | clean count·caution 완전 해제 가능 여부 |
| post-closeout errata | A-track 정정 trail 후속 erratum | B-track 정정 trail 후속 erratum |
| 관련 review 문서들 | 기기-17 언급 위치 grep로 식별 후 표기 정정 | (메타 정정 시) record id 참조 위치 grep로 식별 후 정정 |

학습 카드 재작성 시 alignment·판정 유지 후보:
- alignment: **N1 audit §1 + cleanup feasibility 기반 — 유지**. PDF 원본의 변압기
  Δ-Y 권수비 정답 ① 학습 내용은 그대로 valid.
- 판정: A-track 적용 후 **ready 또는 ready_with_note 재평가** — 표기 정합 회복 후
  source-clean이 되면 ready 승격 검토 가능. B-track 적용 후 ready 승격 가능성
  더 강해짐.

---

## 6. 위험 관리

### 6.1 추론 금지·최소 수정 원칙

- A-track에서 학습 카드 표기를 새로 작성하지 않는다. PDF 원본 표기 문구만 근거로
  사용하며, 그 외 새로운 학습 표현·예시·식을 *추가하지 않는다*.
- B-track에서 questions.json 메타 외의 필드(text·choices·answer·solution·subject·
  tag 등)를 정정에 포함하지 않는다. 메타 정정은 year 1 필드(또는 record id storage
  key) 변경에 한정.
- N1 audit이 확정하지 않은 영역(예: 100항 중 q41·q52 외 record가 정말 모두 2022
  1회인가)은 N3b 통과 전엔 결정 근거로 사용하지 않는다.

### 6.2 A-track 옵션 비교

| 옵션 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **A1 (최소)** | 대표 기출 id 표기만 정정 (`2020_1회_52` → `2022_1회_52 (시행 2022-04-24)`). 보기 [1]·solution 인용 그대로 | 변경 폭 최소 | 보기 [1] 잉여 √3·solution 전류식 오기 잔존 |
| **A2 (PDF 정합 — 권장)** | A1 + 학습 카드 내 보기 [1] 인용을 PDF 원본 `aV/√3` / solution 전류식 인용을 `√3I/a`로 정정 | 학습 카드 = PDF 원본 정합. 학습 노출 시 가독성·정확성 향상 | 변경 폭 약간 증가 (단 모든 변경이 PDF 원본 텍스트로부터 source-grounded) |
| A3 (전면 재작성) | 학습 카드 자체를 새로 작성 | — | **금지** — 추론 위험, §6.1 위반 |

권장: **A2** — 모든 글자 정정이 PDF 원본에서 직접 가져온 것이므로 추론 없음, 표기·
정합 회복.

### 6.3 commit 분리 권고

#### A-track commit 분리

- 권장: **2 commit 분리** (또는 학습 패키지 파일 수에 따라 더 세분).
  - Commit A1: 대표 기출 id 표기 정정 (의미·식별자 변경).
  - Commit A2: 보기 [1]·solution 인용 정정 (텍스트 정리 — A2 옵션 적용 시).
- 사유: 식별자 변경(A1)은 학습 카드의 source 추적 영향. 텍스트 정리(A2)는
  표기 정합. 두 변경을 분리하면 (a) 회귀 시 부분 롤백 가능, (b) review에서 두
  성격의 변경을 별도 평가 가능, (c) git blame 명확.

#### B-track commit 분리

- 권장: **3 commit 분리**.
  - Commit B1: PDF 파일 + pdf_pages 디렉토리 rename (`20200424` → `20220424`).
  - Commit B2: per-year 파일 `data/questions_기출_2020_1회.json` 100 records 메타
    정정 + 파일 rename.
  - Commit B3: `app/data/questions.json` 100 records 메타 정정.
- 사유: 데이터 무결성의 backward chain(PDF → per-year → master)을 거꾸로 추적
  가능하도록 분리. 각 commit 후 diff 검증 + N3b·N3c 결과 재확인 가능.

#### commit 분리 가드

각 commit 사이에 diff 검증 step. 다음 commit 진입 전 즉시 검증·승인.

### 6.4 B-track 사전 검증 의무 — G-2 측정 패키지

questions.json 메타 일괄 정정 전 다음 사전 검증 필수. 본 §6.4는 release gate
**G-2**(§9)의 측정 항목 정의이기도 하다. **G-2 측정 결과가 사용자에게 보고되고
승인되기 전까지 B-track(N3d) 진입 금지.**

#### G-2 측정 항목 (M-1 ~ M-5)

| 측정 ID | 항목 | 측정 명령 후보 | 통과 기준 |
|---|---|---|---|
| **M-1** | `2020_1회` 관련 레코드 수 | `jq '[.[] \| select(.year == 2020 and .session == "1회")] \| length' app/data/questions.json` | 100 (N1 audit 가정과 일치) |
| **M-2** | `data/questions_기출_2020_1회.json` 레코드 수 | `jq 'length' data/questions_기출_2020_1회.json` | 100 |
| **M-3** | 두 set 간 1:1 매핑 검증 | per-year 100 records의 (q_no, text 첫 30자) ↔ questions.json `2020_1회_N` 동일 record 매칭 (jq join 또는 python script) | 100/100 매칭, 누락·중복 0 |
| **M-4** | app 코드에서 `2020_1회` / `year=2020` / `session="1회"` 참조 grep | `grep -rn "2020_1회\\|year.*2020\\|session.*\"1회\"" app/ src/ scripts/` (경로는 실제 디렉토리 구조에 맞춰 조정) | hit 위치 전체 목록화 + 각 hit의 영향 분류(route key·cache key·UI label·통계·테스트) |
| **M-5** | 다른 회차 sanity check (mis-attribution 패턴이 다른 회차에도 있는가) | `data/문제_*_20260316.pdf` 중 1·2건 sampling — 파일명 표기 일자 ↔ PDF 표지 기재 일자 cross-check (예: `data/문제_2020_3회_20260316.pdf` 표지 vs `data/20220305_2회.pdf` 표지) | mis-attribution이 `data/20200424_1회.pdf` 1건에 국한되는지 또는 다른 PDF에도 동일 패턴이 있는지 분류 |

#### 보조 측정 (N1 audit에서 이미 확인된 항목 재측정)

| 측정 ID | 항목 | 측정 명령 후보 | 통과 기준 |
|---|---|---|---|
| M-6 | `year=2022, session="1회"` 슬롯 비어 있음 재확인 | `jq '[.[] \| select(.year == 2022 and .session == "1회")] \| length' app/data/questions.json` | 0 (G-1 §2A.5와 일치) |
| M-7 | `data/pdf_pages/2020_1회/` ↔ `data/20200424_1회.pdf` 매핑 확인 | 페이지 PNG 수 = PDF 페이지 수, 첫 페이지 시각 정합 | 동일 PDF 출처 확정 |
| M-8 | 100항 PDF 정합 (N3b 본 트랙) | per-year file 100 records 각각이 `data/20200424_1회.pdf` 컨텐츠와 정합 (record별 cross-check 또는 통계적 sampling 30+ records) | sampling 통과율 ≥ 95% (95% 미만 시 record별 전수 검증으로 진입) |

#### G-2 통과 룰

1. M-1 ~ M-5 다섯 항목 + 보조 M-6 ~ M-8 세 항목 모두 측정 완료.
2. 측정 결과 docs/audit/ 별 보고서로 기록 (예:
   `docs/audit/trap_map_B_priority_gigi_17_btrack_g2_measurement_<date>.md`).
3. 사용자 승인 후 G-5(§3.2.1) 식별 키 정책 1택 동결.
4. G-2 통과 + G-5 동결 후만 B-track 실행 진입.

#### G-2 미통과 시 차단

- M-1 ≠ 100 또는 M-2 ≠ 100: per-year ↔ master 일치성 깨짐 → B-track 보류, 별
  진단 트랙으로 분기.
- M-3 매칭 < 100/100: 두 source 간 record 누락·중복 발견 → B-track 보류, data 정리
  트랙 선행.
- M-4 영향 범위가 N3c plan 범위 초과: B-track 보류, app 마이그레이션 plan 별도
  수립.
- M-5에서 다른 PDF에도 동일 mis-attribution 발견: 본 plan scope 확장 또는 별
  systemic correction 트랙으로 분기.

**B-track 보고 전 금지 동결**: G-2 측정 결과 보고서가 작성·승인되기 전까지
`app/data/questions.json`·`data/questions_기출_*.json`·PDF·pdf_pages 디렉토리에
대한 어떤 수정도 금지.

### 6.5 다른 영역 회귀 차단

- A-track: 학습 패키지 문서 외 어떤 파일도 변경 금지. git diff에서 변경 범위가
  학습 패키지 문서로 한정됨을 매 commit 후 확인.
- B-track: `2020_1회` 식별자 100 records 외 어떤 record도 변경 금지. git diff에서
  변경 범위가 100 records + PDF·디렉토리 rename으로 한정됨을 매 commit 후 확인.
- A-track·B-track 어느 쪽도 `2010_2회_47`(기기-18) 같은 다른 trap-map record 미수정.
- steps·solution_svg 필드는 본 correction 범위 외 — 향후 별도 트랙.

### 6.6 app/data 수정은 별도 명시 승인 후만

본 plan은 plan 작성까지. N3a(A-track 실행), N3d(B-track 실행)는 사용자의 *명시적
추가 승인* 후에만 실행. plan 승인 ≠ 데이터·문서 수정 승인. plan 승인 시 다음 step의
권한 범위(N3a만, N3a+N3b 모두, A-track 어느 commit까지, 등)를 명시하도록 한다.

### 6.7 학습 패키지 문서 수정도 별도 승인

N3a 학습 카드 정정도 별도 승인 필요. 현 체인의 학습 패키지 문서(study set v1·day
plan·learning log v1.1)는 모두 PASS review 완료 — 정정은 v1.2 등 새 버전 발행
또는 별도 erratum 부착으로 안전하게 처리.

---

## 7. 금지사항 명시 (본 plan 단계 한정)

이번 N2 plan 작성 단계에서 다음은 모두 금지:

- app/data 수정 금지
- `app/data/questions.json` 수정 금지
- `data/questions_기출_*.json` per-year 파일 수정 금지
- record id / year / session / q_no 수정 금지
- answer / choices / text / solution / steps / solution_svg 수정 금지
- subject / tag / q_type / difficulty / quality 수정 금지
- 학습 패키지 문서(study set / day plan / learning log / closeout / errata / 관련
  review) 수정 금지
- PDF 파일 / pdf_pages 디렉토리 rename 금지
- 유료 API 호출 금지
- local server 실행 금지
- 기존 commit amend / rebase / reset 금지

본 plan은 docs/audit/ 신규 1건만 추가한다.

---

## 8. Supervisor Decision Log

| 시점 | 결정 | 근거 commit |
|---|---|---|
| 2026-05-23 | cleanup feasibility review에서 기기-17 record identity mismatch escalation | `2bfc065` |
| 2026-05-23 | record identity normalization plan 작성 (audit 직전 plan) | `538c9c6` |
| 2026-05-23 | record identity targeted audit 완료 — true source 확정 (PDF `data/20200424_1회.pdf` p.4 q52 / 정답 ① / 표지 기재 일자 2022-04-24 / 파일명 ↔ 표지 기재 일자 불일치 강한 가설: 1자 typo) | `13edae5` |
| 2026-05-23 | 사용자 결정: **기기-17 correction track 확정** — A-track(학습 표기 정정) → B-track(메타 normalization) 분리, B-track은 N3b·N3c 통과 후만. **correction plan 먼저 작성 후 별도 승인 받아 데이터·학습 패키지 수정** | 본 plan v1 (`docs: plan 기기-17 correction after source audit`, `16bf8f1`) |
| 2026-05-23 | 사용자 결정: **release gate G-1 ~ G-5 동결** — 본 plan v1을 보강하여 5 gate(identity evidence stand-alone / B-track 영향 측정 / A-track whitelist / 개념 혼동 라벨 / 식별 키 정책 3 후보) 정의·통과 기준·차단 룰 명문화. C/D는 fallback 보류. 표현 정책 (사실/강한 가설/추정 분리) 동결 | 본 plan v2 보강 (`docs: strengthen 기기-17 correction plan guardrails`) |
| (대기) | plan 승인 + N3a A-track 학습 표기 정정 권한 부여 (G-3 + G-4 + G-1 통과 필요) | 대기 중 |
| (대기) | N3b 100항 sanity audit 권한 부여 (G-2 M-8 측정 영역, G-1 + G-4 통과 필요) | 대기 중 |
| (대기) | N3c app id 참조 영향 조사 권한 부여 (G-2 M-4 측정 영역, G-1 + G-4 통과 필요) | 대기 중 |
| (대기) | G-2 측정 보고서 작성·승인 (M-1 ~ M-5 + M-6 ~ M-8) | 대기 중 |
| (대기) | G-5 식별 키 정책 결정 (K1·K2·K3 중 1택 동결, G-2 통과 전제) | 대기 중 |
| (대기) | N3d B-track 메타 normalization 실행 권한 부여 (G-1·G-2·G-4·G-5 모두 통과 전제) | 대기 중 |
| (대기) | N4 redryrun + N5 clean count 갱신 권한 부여 | 대기 중 |

본 plan 승인 후 진행 가능한 작업: N3a~N5. 각 step은 명시 승인 후 수행.

---

## 9. Release Gates G-1 ~ G-5 (요약)

본 plan은 5개 release gate를 정의한다. 각 gate는 다음 트랙·step 진입의 전제
조건이며, 모든 gate를 통과한 후만 정정 작업이 완료된 것으로 본다.

### Gate 매트릭스

| Gate | 영역 | 본문 위치 | 통과 기준 (요약) | 차단 (미통과 시) |
|---|---|---|---|---|
| **G-1** | Identity claim evidence 5축 stand-alone | §2A | 5축(축 ①~⑤) 모두 (a) 출처로 본문에 기록됨 + 강한 가설(파일명 typo)이 (a)와 분리 표기 | A-track·B-track 어느 쪽도 진입 금지 |
| **G-2** | B-track 영향 범위 측정 + 보고 | §6.4 | M-1~M-5 + M-6~M-8 측정 완료 + 별 보고서 작성 + 사용자 승인 | B-track(N3d) 진입 금지. 측정 결과 보고 전까지 questions.json·per-year·PDF·pdf_pages 어떤 수정도 금지 |
| **G-3** | A-track 정정 범위 whitelist | §3.1.1 | W-1·W-2 파일 외 수정 금지 + 대표 기출 표기·보기 [1]·solution 인용만 정정 + 산출물 버전명 동결 | A-track(N3a) 진입 시 whitelist 위반 차단 |
| **G-4** | 개념 혼동 방지 라벨 | §0 | 변압기 Δ-Y 결선/권수비 영역만 본 plan 대상 + 유도전동기 Y-Δ 기동 / 동기전동기 V곡선은 본 plan 대상 아님 | A-track·B-track의 grep·매칭·정정 작업에서 비대상 영역 hit 차단 |
| **G-5** | B-track 식별 키 정책 (K1·K2·K3) | §3.2.1 | G-2 측정 결과 보고 후 K1·K2·K3 중 1택 동결 + supervisor decision log entry 추가 | G-5 결정 전 B-track(N3d) 실행 진입 금지 |

### Gate 적용 흐름

```
plan 승인
   ↓
 G-1 검증 (§2A) — evidence 5축 기록 확인
   ↓ (G-1 통과)
 ┌─────────────────┬─────────────────┐
 ↓                 ↓                 ↓
 A-track:          B-track 사전 검증:    (G-4는 항상 적용)
 G-3 + G-4 통과    G-2 + G-4 통과       grep·매칭·정정 시
   ↓ N3a            ↓ N3b·N3c·G-2 보고
 학습 표기 정정      ↓ (사용자 승인)
                    G-5 결정 (K1/K2/K3)
                     ↓ N3d
                    B-track 실행
                     ↓
                    N4 redryrun
                     ↓
                    N5 clean count 갱신
```

### Gate ↔ Step 매핑

| Step | 필수 통과 gate |
|---|---|
| N3a (A-track 실행) | G-1, G-3, G-4 |
| N3b (100항 sanity) | G-1, G-4 (read-only이지만 측정 영역 한정) |
| N3c (app 영향) | G-1, G-4 (read-only) |
| G-2 측정 보고 | G-1 (evidence 기반) |
| G-5 결정 | G-2 통과 |
| N3d (B-track 실행) | G-1, G-2, G-4, G-5 |
| N4 (redryrun) | 적용된 트랙(A·B)에 따라 통과한 gate 확인 |
| N5 (clean count 갱신) | N4 통과 |

### Gate 동결 룰

- 본 plan에서는 5개 gate의 *정의·통과 기준·차단 룰*만 동결한다.
- 각 gate의 *실제 측정·결정*은 본 plan 승인 후 별 step에서 수행.
- gate 통과 보고는 별 docs/audit/ 보고서로 기록한다 — plan 본문에 결과를
  사후 갱신하지 않는다 (plan은 동결).

---

## 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 0. 개념 혼동 방지 라벨 (G-4 — 변압기 Δ-Y / 유도 Y-Δ / 동기 V곡선 구분) | ✅ §0 |
| 0a. 표현 정책 (사실 / 강한 가설 / 추정 분리) | ✅ 머리 표현 정책 표 |
| 1. 현재 결함 요약 (D-1 보기 [1] / D-2 solution / D-3 메타 / D-4 100항 / D-5 PDF 파일명 강한 가설 + caution 상태 + 학습 패키지 영향) | ✅ §1 |
| 2. N1 audit evidence 요약 (true source + 100항 가능성 + 1·2회 관계 + 2022 슬롯 안전) | ✅ §2 |
| **2A. G-1 identity claim evidence 5축 stand-alone** (questions.json 본문 / PDF p.4 / PDF 표지 / q41 sanity / 2022 1회 count 0 측정 명령) | ✅ §2A |
| 3. correction path 분리 (A-track 학습 표기 / B-track 메타 / C·D fallback 보류) | ✅ §3 |
| **3.1.1 G-3 A-track whitelist** (W-1·W-2 + 변경 범위 + 금지 영역 + 산출물 버전명) | ✅ §3.1.1 |
| **3.2.1 G-5 B-track 식별 키 정책** (K1·K2·K3 3 후보 + G-2 결과 후 결정 + 결정 전 진입 금지) | ✅ §3.2.1 |
| 4. 권장 실행 순서 (N3a~N5 + A·B 분리 사유) | ✅ §4 |
| 5. 후속 학습 패키지 재작성 범위 (plan 단계 미작성 명시) | ✅ §5 |
| **6.4 G-2 B-track 사전 검증 측정 패키지** (M-1~M-5 + M-6~M-8 + 측정 결과 보고 전 B-track 금지 동결) | ✅ §6.4 |
| 6. 위험 관리 (추론 금지·옵션 비교·commit 분리·B-track 사전 검증·승인 분리) | ✅ §6 |
| 7. 금지사항 명시 | ✅ §7 |
| 8. supervisor decision log | ✅ §8 |
| **9. release gates G-1 ~ G-5 요약 + 적용 흐름 + step 매핑 + 동결 룰** | ✅ §9 |
| plan만 작성, 데이터·학습 패키지·기존 commit 미수정 | ✅ docs/audit/ 본 문서 1건만 변경 |
| 금지사항 준수 | ✅ app/data·questions.json·id·answer/choices/text·solution/steps·학습 패키지·PDF 파일·디렉토리 미수정 / API·server 미실행 / amend·rebase·reset 없음 |
| 표현 점검 (typo 단정 → 강한 가설) | ✅ §1.1 D-5 + §2.1 + 머리 표현 정책 |
| 표현 점검 (PDF 일자 → 표지 기재 일자) | ✅ §1.1 D-5 + §2.1 + §2A.3 |
| C/D 폐기 → fallback 보류 | ✅ §3.3 |

---

## Status

- 기기-17 correction plan 작성 완료 + release gate G-1~G-5 보강 동결 —
  데이터·학습 패키지 수정 전 단계.
- 대상: 학습 패키지 문서(A-track) + `app/data/questions.json` `2020_1회_*` 100
  records 메타 + per-year 파일 + PDF·디렉토리 rename(B-track).
- True source (a) 사실: 본문·choices·정답이 PDF `data/20200424_1회.pdf` p.4
  q52와 일치 (N1 audit `13edae5` 직접 인용). 정답 ① choice text = `aV/√3 (V),
  √3I/a (A)`. PDF 표지 기재 일자 = "2022년 04월 24일".
- 강한 가설: PDF 파일명 "20200424" ↔ 표지 기재 일자 "2022-04-24"의 1자 typo —
  실제 시행 시기 외부 일자 정합은 별 트랙.
- 권장 옵션:
  - A-track **A2** (PDF 정합 — 대표 기출 표기 + 보기 [1]·solution 인용 정정).
  - B-track은 G-2 측정 보고 + G-5 식별 키 결정 통과 후 실행.
  - commit 분리 — A-track 2건(A1·A2), B-track 3건(B1·B2·B3), 각 commit 사이 diff
    검증.
- **Release gates 동결**: G-1(evidence 5축) / G-2(B-track 영향 측정) /
  G-3(A-track whitelist) / G-4(개념 혼동 라벨) / G-5(식별 키 정책 K1·K2·K3).
  각 gate 통과 전 해당 트랙 진입 금지.
- C/D fallback: A·B 결과에 따라 재활성화 가능성 보류 (폐기 아님).
- 후속 학습 패키지 재작성(study set/day plan/learning log/closeout/errata/관련
  review)은 본 plan 범위 밖 — N3a·N3d 별도 승인 후.
- supervisor decision log: correction track 확정 / A·B 분리 / G-1~G-5 동결 /
  plan 후 승인 대기. plan 승인 ≠ 데이터·학습 패키지 수정 승인. G-5 결정·G-2
  측정·N3a·N3b·N3c·N3d·N4·N5 모두 별 명시 승인.
- 이 문서는 correction plan + release gate 동결 문서다. questions.json·per-year·
  학습 패키지·PDF·디렉토리 미수정.
