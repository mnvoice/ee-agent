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
  - 원본 PDF (true source): `data/20200424_1회.pdf` (파일명 mis-named, 실제 표지 일자 2022-04-24) page 4 문제 52

---

## 1. 현재 문제 요약

### 1.1 결함 표

| 결함 ID | 위치 | 현재 값 | 원본 PDF 기준 | 분류 |
|---|---|---|---|---|
| D-1 | `2020_1회_52` `choices[0]` (보기 [1]) | 잉여 `\sqrt{3}` 포함 LaTeX (`\sqrt{3}\frac{aV}{\sqrt{3}}…`) | `aV/√3 (V), √3I/a (A)` | choice OCR artifact |
| D-2 | `2020_1회_52` `solution` | 전류식 `I/(√3a)` 형태 오기 | `√3I/a` (정답 ① 선택지와 정합) | solution 전류식 오류 |
| D-3 | `2020_1회_52` `year`·`session` 메타 | `year=2020, session="1회"` | 원본 PDF 표지 일자 = 2022-04-24 (시행 2022년 1회) | record meta/source identity mismatch |
| D-4 | per-year 파일 `data/questions_기출_2020_1회.json` (100 records) | 전수가 같은 PDF에서 추출됐을 가능성 (N1 audit §4 q41 sanity check) | 모두 2022 1회 컨텐츠일 가능성 (확정은 N3b 전수 sanity check 후) | systemic mis-attribution (D-3 상위 원인) |
| D-5 | PDF 파일 `data/20200424_1회.pdf` | 파일명에 "20200424" | PDF 표지 "2022년 04월 24일 필기 기출문제" | filename 1자 typo (D-3·D-4 상위 원인) |

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
| PDF 표지 일자 | direct Read | "2022년 04월 24일 필기 기출문제" — 파일명 "20200424"는 typo |

→ **확정**: 기기-17 변압기 Δ-Y 권수비 문제의 true source = 전기기사 2022년 1회
시행(2022-04-24) 문제 52, 정답 ①, choice ① text = `aV/√3 (V), √3I/a (A)`.

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

### 3.3 Option C(alias errata) / Option D(representative 교체) 불요 판정

N1 audit §7.4·§8 권고대로:

- Option C(메타 정정 없이 docs에 mismatch alias 명시)는 옵션 A·B 둘 다 실행
  가능해진 시점에서 잔류 결함만 남기는 임시방편 — **불요**.
- Option D(대표 기출을 다른 회차 q로 교체)는 true source가 확정됐고 학습 내용이
  valid하므로 — **불요**.

본 plan은 A-track + B-track 두 갈래로 집중한다.

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

### 6.4 B-track 사전 검증 의무

questions.json 메타 일괄 정정 전 다음 사전 검증 필수:

| 검증 항목 | 측정 방법 | 통과 기준 |
|---|---|---|
| 100항 PDF 정합 (N3b) | per-year file 100 records 각각이 `data/20200424_1회.pdf` 컨텐츠와 정합 (sampling 또는 record별 cross-check) | 100% 정합 |
| storage key 영향 (N3c) | `2020_1회` 패턴 grep — app routing, cache, frontend reference, 외부 학습 패키지 reference | 영향 범위 확정 + 마이그레이션 plan 수립 가능 |
| 2022_1회 슬롯 비어 있음 재확인 | grep `year=2022 AND session="1회"` in questions.json | 0 hits 유지 |
| pdf_pages 디렉토리 정합 | `data/pdf_pages/2020_1회/` ↔ `data/20200424_1회.pdf` 매핑 확인 | 동일 PDF 출처 확정 |

위 4개 모두 통과해야 B-track 실행. 한 건이라도 미통과면 B-track 보류, plan 재설계.

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
| 2026-05-23 | record identity targeted audit 완료 — true source 확정 (2022 1회 q52 / 정답 ① / PDF `data/20200424_1회.pdf` filename mis-named) | `13edae5` |
| 2026-05-23 | 사용자 결정: **기기-17 correction track 확정** — A-track(학습 표기 정정) → B-track(메타 normalization) 분리, B-track은 N3b·N3c 통과 후만. **correction plan 먼저 작성 후 별도 승인 받아 데이터·학습 패키지 수정** | 본 plan (`docs: plan 기기-17 correction after source audit`) |
| (대기) | plan 승인 + N3a A-track 학습 표기 정정 권한 부여 | 대기 중 |
| (대기) | N3b 100항 sanity audit 권한 부여 | 대기 중 |
| (대기) | N3c app id 참조 영향 조사 권한 부여 | 대기 중 |
| (대기) | N3d B-track 메타 normalization 실행 권한 부여 (N3b·N3c 통과 전제) | 대기 중 |
| (대기) | N4 redryrun + N5 clean count 갱신 권한 부여 | 대기 중 |

본 plan 승인 후 진행 가능한 작업: N3a~N5. 각 step은 명시 승인 후 수행.

---

## 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. 현재 결함 요약 (D-1 보기 [1] / D-2 solution / D-3 메타 / D-4 100항 / D-5 PDF 파일명 + caution 상태 + 학습 패키지 영향) | ✅ §1 |
| 2. N1 audit evidence 요약 (true source + 100항 가능성 + 1·2회 관계 + 2022 슬롯 안전) | ✅ §2 |
| 3. correction path 분리 (A-track 학습 표기 / B-track 메타 / C·D 불요) | ✅ §3 |
| 4. 권장 실행 순서 (N3a~N5 + A·B 분리 사유) | ✅ §4 |
| 5. 후속 학습 패키지 재작성 범위 (plan 단계 미작성 명시) | ✅ §5 |
| 6. 위험 관리 (추론 금지·옵션 비교·commit 분리·B-track 사전 검증·승인 분리) | ✅ §6 |
| 7. 금지사항 명시 | ✅ §7 |
| 8. supervisor decision log | ✅ §8 |
| plan만 작성, 데이터·학습 패키지·기존 commit 미수정 | ✅ docs/audit/ 신규 문서 1건만 |
| 금지사항 준수 | ✅ app/data·questions.json·id·answer/choices/text·solution/steps·학습 패키지·PDF 파일·디렉토리 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-17 correction plan 작성 완료 — 데이터·학습 패키지 수정 전 단계.
- 대상: 학습 패키지 문서(A-track) + `app/data/questions.json` `2020_1회_*` 100
  records 메타 + per-year 파일 + PDF·디렉토리 rename(B-track).
- True source = 전기기사 2022년 1회(시행 2022-04-24) 문제 52, 정답 ① choice text
  `aV/√3 (V), √3I/a (A)` — N1 audit(`13edae5`)에서 PDF `data/20200424_1회.pdf` p.4
  직접 인용으로 확정.
- 권장 옵션:
  - A-track **A2** (PDF 정합 — 대표 기출 표기 + 보기 [1]·solution 인용 정정).
  - B-track은 N3b·N3c 사전 검증 통과 후 실행.
  - commit 분리 — A-track 2건(A1·A2), B-track 3건(B1·B2·B3), 각 commit 사이 diff
    검증.
- 후속 학습 패키지 재작성(study set/day plan/learning log/closeout/errata/관련
  review)은 본 plan 범위 밖 — N3a·N3d 별도 승인 후.
- supervisor decision log: correction track 확정 / A·B 분리 / plan 후 승인 대기.
  plan 승인 ≠ 데이터·학습 패키지 수정 승인.
- 이 문서는 correction plan이다. questions.json·per-year·학습 패키지·PDF·디렉토리
  미수정.
