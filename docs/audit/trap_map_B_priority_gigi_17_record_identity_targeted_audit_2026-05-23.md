# Trap-Map B-Priority — 기기-17 Record Identity Targeted Audit (2026-05-23)

기기-17 record identity normalization plan(`538c9c6`)의 N1 audit — 변압기 Δ-Y
권수비 문제의 true source 회차/번호 추적. corpus 내부 + 로컬 PDF로 한정해 수행.

본 단계는 audit 문서 작성까지 — **app/data·questions.json·id·학습 패키지·closeout/
errata 미수정**. solution/steps 미적용. answer/choices/text 미수정. 유료 API 미호출.
local server 미실행. 외부 웹 검색 미사용. amend/rebase/reset 없음.

- 검토 대상: 기기-17 대표 기출 `2020_1회_52` (변압기 Δ-Y 권수비 문제)
- 개념 분류 제한: **변압기 Δ-Y 결선/권수비**만 매칭 대상. 유도전동기 Y-Δ 기동·
  동기전동기 V곡선은 별 주제로 제외.
- 참조:
  - normalization plan (`docs/audit/trap_map_B_priority_gigi_17_record_identity_normalization_plan_2026-05-23.md`)
  - 기기-17 cleanup feasibility (`docs/audit/trap_map_B_priority_gigi_17_cleanup_feasibility_2026-05-23.md`)
  - 원본 PDF 후보: `data/20200424_1회.pdf` (✅ 본 audit에서 true source로 식별)

---

## 결론: **TRUE SOURCE 확정 — 2022년 4월 24일 시행 시험(전기기사) 문제 52번**

본 audit이 식별한 변압기 Δ-Y 권수비 문제의 출처:
- **PDF**: `data/20200424_1회.pdf` (전자문제집 CBT, www.comcbt.com 제공)
- **표지 일자**: PDF 본문 상단 "**2022년 04월 24일** 필기 기출문제"
- **문제 번호**: 52번
- **공식 정답**: ① (PDF에 ❶로 표기, choice text = `aV/√3 (V), √3I/a (A)`)

**파일명 ↔ 실제 일자 불일치 (mis-naming)**: 파일명 `20200424`는 "2020-04-24"로
해석되어 questions.json에 year=2020 / session="1회"로 저장됐으나, PDF 표지의
실제 일자는 **2022-04-24** — 파일명이 1자 오기(2020 → 2022)된 것.

**Mis-attribution 범위 — 100항 전수 가능성 (NOT isolated)**: per-year 파일
`data/questions_기출_2020_1회.json`의 100개 레코드가 모두 같은 PDF에서 추출된
2022년 1회 컨텐츠일 가능성이 높음 (q41 sanity check로 확인 — 본 audit §4). 즉
**기기-17 q52는 100항 전체 mis-labeling의 한 사례**.

→ 본 audit의 의의: 기기-17 case 식별이 **upstream 단일 PDF 파일명 오기**라는
근본 원인을 드러냄. 정정 트랙은 q52 개별 대응이 아닌 **per-year 파일 전체 +
PDF 파일명** 차원에서 설계해야 한다.

---

## 1. Audit Scope & Method

본 audit이 따른 검색 절차:

1. questions.json `2020_1회_52` 본문에서 unique phrases 추출:
   - "권수비가 a인 단상변압기 3대"
   - "1차에 △, 2 차에 Y로 결선"
   - "단자전압을 V(V), 전류를 I(A)"
   - "1차측의 단자전압 및 선전류"
2. corpus 내부 grep:
   - `app/data/questions.json` (5,331 records)
   - `data/questions_기출_*.json` (74 per-year files)
   - `data/mathpix_기출_*.json` (65 OCR'd PDF files, 1998~2020 covering 1·2·3·4·6회)
3. 로컬 PDF directory 탐색:
   - `data/문제_*.pdf` (연도·회차별 표준 PDF)
   - `data/20200424_1회.pdf` (filename 의심 — 2020/4/24 vs 2022/4/24)
   - `data/pdf_pages/*` (페이지 PNG 캐시)
4. 후보 PDF 직접 페이지 확인 (Read with pages=N): `data/20200424_1회.pdf` page 1-5.

**개념 혼동 방지**: 검색·매칭 시 다음 영역은 명시적으로 배제:
- 유도전동기 Y-Δ 기동 (motor starting method)
- 동기전동기 V곡선 (excitation control)

---

## 2. Step 1 — Corpus Internal Search

### 2.1 questions.json (master)

- "권수비가 a인 단상변압기 3대" 정확 매칭: **1 hit** — `2020_1회_52` 자체 (다른
  record에 동일 본문 0건).

### 2.2 per-year files (`data/questions_기출_*.json`, 74개)

- 정확 매칭: **1 hit** — `data/questions_기출_2020_1회.json` q_no=52 (questions.json의
  source per-year file).
- looser 매칭 "단상변압기 3대" or "단상 변압기 3대": 6 hits:
  - 1998_6회_21 (정상·역상·영상 임피던스 — 별 주제)
  - 2018_1회_27 (V결선 동손 비교 — 별 주제)
  - 2018_1회_55 (△-Y 결선 각변위/위상차 — 같은 영역이나 다른 문제)
  - **2020_1회_52** (본 target)
  - 2021_2회_31 (Δ-Δ 최대부하 — 별 주제)
  - 2026_1회_53 (Δ-Δ → V-V 사용가능 부하 — 별 주제)
- → exact 권수비 a 단상변압기 3대 1차△·2차Y 본문은 다른 회차에 부재.

### 2.3 mathpix files (`data/mathpix_기출_*.json`, 65 OCR'd PDFs)

- 정확 매칭: **0 hit**.
- 정규식 `권수비.{0,10}단상.?변압기.{0,10}3.?대`: 0 hit.
- 정규식 `1차에 △.*2.?차에 Y`: 0 hit.
- 정규식 `1차측의 단자전압.{0,30}선전류`: 0 hit.
- 정규식 `단자전압을 V` (broad): 1 hit (2013_1회) — 다른 문제.

→ **mathpix-OCR된 65개 PDF 어느 곳에도 변압기 Δ-Y 권수비 본 문제는 부재**.

### 2.4 `data/mathpix_기출_2020_1_2회.json` (PDF `문제_2020_1,2회_20260316.pdf`의 OCR)

- "문제 52" 추출 = "동기전동기의 공급 전압과 부하를 일정하게 유지하면서 ... 여자
  전류를 증가시키면 전기자 전류는?" → V곡선 / 정답 ①.
- PDF 2020년 1회 52 = V곡선 문제. **questions.json `2020_1회_52` (변압기 권수비)는
  PDF 2020 1회 52가 아님 — 다시 확정.**

### 2.5 두 pipeline 공존 — 데이터 입력 분기

| pipeline | 입력 file | 출력 | 본 audit 시점 q_no=52 컨텐츠 |
|---|---|---|---|
| Pipeline A (per-year) | `data/questions_기출_YYYY_N회.json` (74 files) | per-year per-session 100항씩 | `2020_1회_52` = 변압기 권수비 △-Y |
| Pipeline B (mathpix-derived) | `data/mathpix_기출_YYYY_N회.json` (65 files) → `data/questions_기출_YYYY_1_2회.json` 등 | combined-session 묶음 (66항 등) | `2020_1,2회_52` = 동기전동기 V곡선 (PDF 정합) |

두 pipeline 결과가 `app/data/questions.json`에 모두 ingestion됨 → 같은
(year=2020, q_no=52)에 두 record 공존 (session = "1회" vs "1,2회").

---

## 3. Step 2 — Local PDF 후보 식별 및 직접 확인

### 3.1 후보 PDF 탐색

- `data/문제_2020_*.pdf` 3건 검토:
  - `문제_2020_1,2회_20260316.pdf` — q52 = V곡선 (mathpix와 정합, 본 target 아님)
  - `문제_2020_3회_20260316.pdf` — out of scope
  - `문제_2020_4회_20260316.pdf` — out of scope
- **`data/20200424_1회.pdf`** — 파일명 의심 (filename에 "20200424" 포함). 본
  audit에서 직접 확인.

### 3.2 `data/20200424_1회.pdf` 표지 / 내용 인용

**PDF 표지 (모든 페이지 상단 footer)**:
```
전기기사    ◐ 2022년 04월 24일 필기 기출문제 ◑    전자문제집 CBT : www.comcbt.com
```

→ **파일명 "20200424"는 "2022-04-24"의 typo (2020 → 2022)**. PDF 실제 내용은
**2022년 04월 24일 시행 전기기사 필기 기출문제**.

### 3.3 PDF page 4 (3과목 전기기기 q41~q53) — 문제 52 직접 인용

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

(`❶` = 전자문제집 CBT 정답 표기 convention; 정답 ①.)

### 3.4 PDF ↔ questions.json `2020_1회_52` 본문 정합 확인

| 항목 | PDF (`data/20200424_1회.pdf` p.4 문제 52) | questions.json `2020_1회_52` | 정합 |
|---|---|---|---|
| text | "권수비가 a인 단상변압기 3대가 있다. 이것을 1차에 △, 2 차에 Y로 결선하여..." | 동일 | ✅ |
| choice ① | `aV/√3 (V), √3I/a (A)` | `\sqrt{3}\frac{aV}{\sqrt{3}}\text{(V)}, \frac{\sqrt{3}I}{a}\text{(A)}` | ✅ (단 questions.json 보기 [1]은 잉여 `\sqrt{3}` OCR artifact 포함 — PDF는 `aV/√3` 깨끗) |
| choice ② | `√3aV(V), I/(√3a)(A)` | `\sqrt{3}aV\text{(V)}, \frac{I}{\sqrt{3}a}\text{(A)}` | ✅ |
| choice ③ | `√3V/a (V), aI/√3 (A)` | `\frac{\sqrt{3}V}{a}\text{(V)}, \frac{aI}{\sqrt{3}}\text{(A)}` | ✅ |
| choice ④ | `V/(√3a)(V), √3aI(A)` | `\frac{V}{\sqrt{3}a}\text{(V)}, \sqrt{3}aI\text{(A)}` | ✅ |
| 정답 | ① | answer=1 | ✅ |

→ **본문·정답 일치 — questions.json의 변압기 권수비 문제는 본 PDF에서 추출된 것
확정**. 단지 메타(year=2020·session="1회")가 잘못 부여됨.

---

## 4. Sanity Check — Mis-Attribution이 q52에 국한되는가?

PDF `data/20200424_1회.pdf`는 2022 1회 100개 문제의 PDF. per-year 파일
`data/questions_기출_2020_1회.json`은 100항 전수를 담음. 두 데이터가 같은 PDF
출처라면 100항 전체가 mis-attribute됨을 의미.

### Spot check — 문제 41 (3과목 전기기기 첫 문제)

PDF p.4 문제 41 인용:
> 41. 단상 변압기의 무부하 상태에서 V1 = 200sin(ωt+30°)(V) 의 전압이 인가되었을
>     때 I0 = 3sin(ωt+60°) + 0.7sin(3ωt+180°)(A) 의 전류가 흘렀다. 이때 무부하손은
>     약 몇 W인가?  ❷ 259.8

questions.json `2020_1회_41`:
- tag: '비정현파의 소비전력 계산'
- text: "단상 변압기의 무부하 상태에서 V1 = 200sin(ωt+30°)(V)의 전압이 인가되었을
  때 Io = 3sin(ωt+60°) + 0.7sin(3ωt+180°)(A) 의 전류가 흘렀다. 이때 무부하손은 약 몇 W..."

→ **동일** (텍스트 일치, 정답 동일).

### 결론

**`data/questions_기출_2020_1회.json` 100 records가 모두 2022 1회 컨텐츠일 가능성이
매우 높다.** 본 audit은 q52·q41 2개만 검증했으나, 같은 PDF 출처로부터 추출된
연속 100항이므로 동일 mis-attribution이 전수 적용된다고 보는 것이 자연스럽다.
(완전 전수 검증은 별도 트랙.)

또한 `data/pdf_pages/2020_1회/` 디렉토리에는 9개 페이지 PNG만 존재(`page_1~page_9`)
— `data/20200424_1회.pdf`도 9 페이지 — 같은 PDF의 페이지 캐시일 가능성. 즉
"2020_1회" 라벨이 부여된 모든 pipeline A 산출물이 동일 mis-named PDF에서 비롯됨.

---

## 5. `2020_1회_52` vs `2020_1,2회_52` 관계 정리

| 식별자 | 실제 출처 PDF | 컨텐츠 | 정합 |
|---|---|---|---|
| **`2020_1회_52`** | **`data/20200424_1회.pdf`** (filename mis-named; 실제 2022-04-24 시행) | 변압기 권수비 △-Y / 정답 ① | PDF 정합 ✅ / **메타 라벨 (year=2020) ❌** |
| **`2020_1,2회_52`** | **`data/문제_2020_1,2회_20260316.pdf`** (실제 2020 1회+2회 합본) | 동기전동기 V곡선 / 정답 ① | PDF 정합 ✅ / **메타 라벨 (session="1,2회") 부분 정합** (실제 "1회"여야) |

→ 두 record는 **서로 다른 PDF 출처에서 추출된 별개 컨텐츠**. duplicate 식별자
아님 — duplicate처럼 보였으나 실은 *두 PDF가 같은 q_no=52에 다른 문제를 담은 것*.

`2020_1,2회_52`는 PDF 2020년 1회 52(V곡선)와 정합 — session 라벨이 정확히 "1회"였으면
`2020_1회_52`로 저장됐을 데이터. 그 자리(`2020_1회_52`)에 2022 1회 변압기 권수비
문제가 들어가는 바람에 V곡선 record는 "1,2회" 라벨로 우회 저장된 것으로 보임.

---

## 6. 신규 발견 종합

| 발견 | 의미 | 영향 범위 |
|---|---|---|
| **F1. 변압기 Δ-Y 권수비 문제 true source 확정** | `data/20200424_1회.pdf` p.4 문제 52 = 2022년 4월 24일 시행 전기기사 필기 기출문제 | 기기-17 정정 가능 |
| **F2. PDF 파일명 1자 오기** | "20200424" → 실제 "20220424". 파일 표지가 명확히 "2022년 04월 24일" | 파일 rename 필요 |
| **F3. mis-attribution 100항 추정** | `data/questions_기출_2020_1회.json` 100항이 전부 2022 1회 컨텐츠 (q41·q52 sanity check 일치) | per-year 파일 전체 정정 + questions.json 100 record meta 정정 |
| **F4. 2022 1회 슬롯 비어 있음** | questions.json에 year=2022·session="1회" record 0건 | id 재attribution 충돌 없음 (안전) |
| **F5. mathpix corpus에 본 PDF OCR 부재** | `data/mathpix_기출_2020_1회.json` 미존재 (file inventory에 부재). per-year 파일은 별 pipeline 산출 | pipeline A vs B 분리 명확 |
| **F6. PDF 정답 ① choice = aV/√3, √3I/a — 물리 정답 직접 일치** | questions.json 보기 [1]의 잉여 `\sqrt{3}` artifact는 OCR 추가분 — PDF 원본은 깨끗 | choice [1] cleanup 가능 (정정값 = `aV/√3 (V), √3I/a (A)`) |
| **F7. solution 필드 전류식 오류는 PDF와 무관** | PDF는 풀이/해설 없음 (CBT 형식). solution의 `I/(√3a)`는 LLM/agent 생성 시점의 별도 오류 | solution cleanup 가능 (정정값 = `√3I/a`) |

---

## 7. 판정

### 7.1 True Source 후보 — **확정**

- **PDF**: `data/20200424_1회.pdf` (filename mis-named, 실제 표지 일자 2022-04-24)
- **시험**: 전기기사 2022년 1회 (시행 2022-04-24)
- **문제 번호**: 52
- **공식 정답**: ① — choice text `aV/√3 (V), √3I/a (A)`

### 7.2 evidence

| 단계 | 출처 | 결과 |
|---|---|---|
| corpus exact match | questions.json + per-year files | 1 hit (`2020_1회_52` 자체) |
| corpus loose match | questions.json + per-year files | 6 hits 모두 별 문제 |
| mathpix 65 PDFs | regex search | 0 hit |
| 2020 1,2회 mathpix q52 | direct grep | 동기전동기 V곡선 (다른 문제) |
| **PDF `data/20200424_1회.pdf` p.4 q52** | **direct read** | **본문·choices·정답 questions.json `2020_1회_52`와 정합** |

→ **확정 판정**. 다른 PDF 후보는 모두 배제됨 (corpus 어디에도 같은 본문 없음, 본
PDF만 일치).

### 7.3 학습 패키지 표기 정정 방향

study set v1 / day plan / learning log v1.1의 기기-17 카드 "대표 기출" 표기를:
- **변경 전**: `2020_1회_52`
- **변경 후 후보**: `2022_1회_52` (시행 2022-04-24)

선택지 [1] 표기 OCR artifact를 동시에 표기 정정할 수 있음 (`aV/√3 (V), √3I/a (A)`로).

### 7.4 Data id 정정 필요 여부

| 옵션 | 내용 | 권장 |
|---|---|---|
| 학습 패키지만 정정 (plan §4 옵션 A) | docs의 대표 기출 id를 `2022_1회_52`로 정정. questions.json은 그대로 | 임시·저위험. data 무결성은 회복 안 됨 |
| **questions.json 메타 정정 (plan §4 옵션 B)** | `2020_1회_*` 100 records의 year=2020 → 2022 일괄 정정. + per-year 파일 rename + PDF rename | 본질 정정. 단 app routing/storage key 영향 사전 확인 필수 |
| alias errata (plan §4 옵션 C) | 메타 정정 없이 docs로 mismatch 명시 | 잔류 결함, 임시방편 |

→ True source 확정으로 옵션 A·B가 모두 실행 가능. **권장 순서**: A를 먼저 실행
(즉시 학습 패키지 신뢰성 회복) → app id 참조 영향 검증 후 B 실행 (data 무결성
회복).

---

## 8. 다음 Step 권고

본 audit은 audit 문서 작성까지 — 후속 작업은 별도 명시 승인 후 진행.

| 단계 | 작업 | 산출물 |
|---|---|---|
| N2 — correction plan | A(학습 표기) → app 영향 검증 → B(메타 정정) 분리 plan. F3 100항 전수 검증 포함 | correction plan 문서 |
| N3a — 학습 패키지 정정 (옵션 A) | study set/day plan/learning log 기기-17 카드의 "대표 기출 2020_1회_52" → "2022_1회_52 (시행 2022-04-24)"로 정정. 보기 [1] LaTeX 잉여 √3 정정도 같이 가능 | learning materials correction commit |
| N3b — 100항 전수 sanity check + per-year 파일 rename | `data/questions_기출_2020_1회.json` 100항이 모두 2022 1회 컨텐츠인지 record별 PDF cross-check (또는 sampling) | audit report |
| N3c — questions.json 메타 정정 (옵션 B) | year=2020,session="1회" → year=2022,session="1회" 일괄 정정. PDF 파일도 `data/20200424_1회.pdf` → `data/20220424_1회.pdf` rename. app id 참조 영향 사전 확인 | 별도 commit + evidence supplement |
| N4 — 기기-17 redryrun | 정정 후 데이터·학습 패키지 정합 재검증 | redryrun 문서 |
| N5 — clean count 갱신 | 기기-17 caution 해제 가능 여부 결정. 완전 클린 36/41 / caution 0/0 도달 가능성 | follow-up erratum |
| 별도 — 추출 파이프라인 회귀 트랙 | 본 case의 filename typo 양상 + 기기-18 인접 혼입 양상 통합 회귀 방지 | 별도 트랙 |

---

## 9. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. 변압기 Δ-Y 권수비 unique phrase 추출 | ✅ §1 |
| 2. corpus 내부 grep (questions.json / per-year 74 / mathpix 65) | ✅ §2 |
| 3. 로컬 PDF 후보 식별 + 직접 확인 | ✅ §3 — `data/20200424_1회.pdf` p.4 q52 인용 |
| 4. 두 레코드 관계 정리 (`2020_1회_52` vs `2020_1,2회_52`) | ✅ §5 |
| 5. 학습 패키지 표기 정정 방향 제안 | ✅ §7.3 |
| 6. data id 정정 필요 여부 옵션 비교 | ✅ §7.4 |
| 7. 다음 step 권고 | ✅ §8 |
| 개념 혼동 금지 (Y-Δ 기동 / V곡선 매칭 안 함) | ✅ §1 (배제 명시) + §2.4 (V곡선 record 명확히 기기-17 대상 아님) |
| 추론으로 정정 확정 금지 — PDF source-grounded | ✅ §3.3 PDF 직접 인용 후 §7 판정 |
| 본 단계 데이터·학습 패키지·closeout/errata 미수정 | ✅ docs/audit/ 신규 1건만 |
| 외부 웹 검색 미사용 | ✅ corpus + local PDF만 |
| 금지사항 준수 | ✅ app/data·questions.json·id·answer/choices/text·solution/steps·학습 패키지·closeout/errata 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-17 record identity targeted audit 완료 — **true source 확정**.
- 출처: `data/20200424_1회.pdf` (filename mis-named "20200424" → 실제 PDF 표지
  "2022년 04월 24일") page 4 문제 52. 시험 = 전기기사 2022년 1회. 정답 ① choice
  text `aV/√3 (V), √3I/a (A)` — 물리 정답·questions.json answer 정합.
- evidence: corpus 65 mathpix OCR + 74 per-year files + questions.json 5,331
  records grep 결과 PDF `data/20200424_1회.pdf` 외 다른 출처 후보 0건. 본 PDF
  본문·choices·정답 questions.json `2020_1회_52`와 직접 일치.
- 신규 major 발견 — **`data/questions_기출_2020_1회.json` 100 records 전체가
  2022 1회 컨텐츠일 가능성** (q41·q52 sanity check 일치). filename typo 기인
  systemic mis-attribution.
- 학습 패키지 정정 방향: "대표 기출 `2020_1회_52`" → "`2022_1회_52` (시행
  2022-04-24)". 보기 [1] 잉여 √3 artifact도 PDF 원본대로 `aV/√3`로 정정.
- data id 정정: 옵션 A(학습 표기만) 즉시 실행 가능. 옵션 B(questions.json
  메타 일괄 정정 + per-year 파일 rename + PDF rename)는 app id 참조 영향 사전
  검증 후 실행.
- 다음 권고: N2 correction plan → N3a 학습 표기 → N3b 100항 sanity → N3c 메타
  정정 → N4 redryrun → N5 clean count 갱신.
- 이 문서는 audit 보고서다. 데이터·학습 패키지·closeout/errata·id 미수정.
