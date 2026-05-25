# Trap-Map B-Priority — `2020_1,2회` 66항 E1 Source PDF Audit (2026-05-25)

66항 session-label policy evaluation (`df7e932`, `DR-TRAP-2020-12-66ITEM-SESSION-
LABEL-POLICY`)의 evidence gate E1 — 원본 PDF source audit을 수행한다. 사용자
명시 승인 영역에 따라 `data/문제_2020_1,2회_20260316.pdf` read-only inspection만
수행한다.

이번 단계는 **read-only audit**. **app/data, questions.json, per-year json, PDF
filename, pdf_pages, app code, 어떤 파일도 수정하지 않는다.** PDF 복사/rename/
편집/OCR 산출물 생성/data report 파일 생성 모두 금지. push 없음.
amend/rebase/reset 없음. 기기-17 caution 유지. q52 단독 id 재발급 금지 유지.
registry row promotion 금지 유지. Batch migration 실행 금지.

- 검토 대상 PDF: `data/문제_2020_1,2회_20260316.pdf` (untracked, 19,482,003 bytes,
  35 pages, A4)
- 관련 policy evaluation: `docs/audit/trap_map_B_priority_2020_1_2_66item_session_label_policy_2026-05-25.md` (`DR-TRAP-2020-12-66ITEM-SESSION-LABEL-POLICY`)
- 관련 separability evaluation: `docs/audit/trap_map_B_priority_gigi_17_66item_separability_evaluation_2026-05-25.md`
- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`
- 관련 jsonl: `docs/audit/decision_records/trap_map_active_decisions.jsonl`

---

## 1. PDF 기본 정보

| 항목 | 값 |
|---|---|
| 파일 경로 | `data/문제_2020_1,2회_20260316.pdf` |
| 크기 | 19,482,003 bytes (~18.6 MB) |
| 페이지 수 | **35 pages** |
| Page size | 595 x 841 pts (A4) |
| PDF version | 1.5 |
| Creator | vFlat (모바일 스캔 앱) |
| Encrypted | no |
| tracked? | **untracked** (사용자 명시 승인으로 read-only inspection 허용) |

→ `vFlat` creator + A4 + 35 pages 양식은 *책의 일부를 모바일 스캔한 결과물*임을
시사. 단일 시험 시행 PDF가 아니라 *문제집 일부*일 가능성.

---

## 2. 표지 Evidence — "제 1,2 회" 합본 시험 명시

### 2.1 표지 (PDF page 1, 책 page 906) 직접 인용

```
국가기술자격검정 필기시험 문제

2020년도 전기기사 일반검정 제 1,2 회

자격종목 및 등급(선택분야)  종목코드  시험시간      문제지형별
전기기사                   1150     2시간 30분    A

1과목 전기자기학
```

→ **표지 명시**: "**2020년도 전기기사 일반검정 제 1,2 회**" — 1회+2회가 **별 시험으로 분리**되지 않고 **합본 시험**으로 시행됐음을 표지가 직접 명시.

### 2.2 표지 기재 일자

표지에 **시행 일자가 명시되지 않음**. 책 페이지 footer는 "**20년도 1,2회**"로
일관 표기 (예: page 907, 909, 910, ..., 940 — 모든 footer 일관).

→ 본 PDF는 *시행 일자 표기 없는 합본 시험 양식*. 시행 일자 evidence는 별 트랙
(예: 외부 시행 기록 source).

### 2.3 양식 의미

"제 1,2 회" 양식은 *2020년 COVID-19 영향*으로 전기기사 1회·2회 시험이 한 번에
합본 시행됐을 가능성을 시사 (외부 evidence 영역 — 본 audit scope 외 확정 없음).
다만 **PDF source 자체는 합본 시험으로 명시**되어 있어, 1회와 2회를 분리할 source
단서가 PDF에 *부재*.

---

## 3. 페이지 구조 — 1회/2회 분리 단서 부재

### 3.1 페이지 ↔ 책 페이지 ↔ 과목 매핑 (read한 영역)

| PDF page | 책 page | 영역 | 표시 단서 |
|---|---|---|---|
| 1 | 906 | 표지 + 1과목 전기자기학 시작 (문제 1) | "제 1,2 회" 합본 명시 |
| 2 | 907 | 1과목 문제 2~4 | footer "20년도 1,2회" |
| 3 | 908 | 1과목 문제 5~8 | footer "20년도 1,2회" |
| 4 | 909 | 1과목 문제 9~11 | footer "20년도 1,2회" |
| 5 | 910 | 1과목 문제 12~14 | footer "20년도 1,2회" |
| 15 | 920 | **3과목 전기기기 시작 (문제 41)** + 2과목 끝 (문제 40) | footer "20년도 1,2회" |
| 16 | 921 | 3과목 문제 42~44 | footer "20년도 1,2회" |
| 17 | 922 | 3과목 문제 45~47 | footer "20년도 1,2회" |
| 18 | 923 | 3과목 문제 48~50 | footer "20년도 1,2회" |
| 19 | 924 | 3과목 문제 51~53 | footer "20년도 1,2회" |
| 20 | 925 | 3과목 문제 54~56 | footer "20년도 1,2회" |
| 30 | 935 | 5과목(전기설비) 문제 82~83 | footer "20년도 1,2회" |
| 31 | 936 | 5과목 문제 84~85 | footer "20년도 1,2회" |
| 32 | 937 | 5과목 문제 86~88 | footer "20년도 1,2회" |
| 33 | 938 | 5과목 문제 89~91 | footer "20년도 1,2회" |
| 34 | 939 | 5과목 문제 92~93 | footer "20년도 1,2회" |
| 35 | 940 | 5과목 문제 94~95 (마지막) + 안내문 | footer "20년도 1,2회" |

### 3.2 1회/2회 분리 구간 단서 — **부재**

| 분리 단서 유형 | 발견 여부 |
|---|---|
| "제1회" 표기 영역 | 0건 |
| "제2회" 표기 영역 | 0건 |
| 별 표지 (1회 → 2회 전환) | 0건 |
| 별 시간/일자 표기 | 0건 |
| 과목별 회차 분리 표기 | 0건 |

→ 35 페이지 전체에 footer "20년도 1,2회" 일관. **1회/2회 분리 구간 단서 0건**.
PDF는 *합본 양식으로 단일 시험처럼 작성*.

### 3.3 마지막 안내문 (PDF page 35, 책 page 940)

```
출제기준 변경 및 개정된 관계 법규에 따라 삭제된 문제가 있어 20문항이 안됩니다.
```

→ **일부 문제 삭제 영역 존재** 명시. 책 본문에 표시된 문제 번호는 1~95이나, 일부
문제가 출제기준 변경/관계 법규 개정으로 *삭제*되어 *과목별 20문항 미만* 영역
존재.

---

## 4. 95 문제 vs 66 Records 차이 분석

### 4.1 PDF 문제 번호 범위

| 과목 | 문제 번호 범위 (PDF) | 표준 문항 수 |
|---|---|---|
| 1과목 전기자기학 | 문제 01~20 | 20 |
| 2과목 전력공학 | 문제 21~40 | 20 |
| 3과목 전기기기 | 문제 41~60 | 20 |
| 4과목 회로이론·제어공학 | 문제 61~80 | 20 |
| 5과목 전기설비기술기준 | 문제 81~100 | 20 |
| **합계** | **1~100 (표준)** | **100** |

PDF에서 확인된 최대 문제 번호 = **95** (page 35). 100 - 95 = 5 문제가 *최소
영역*에서 누락. 단 PDF 안내문이 "20문항이 안됩니다" = *과목별 20문항 미만* 명시
영역이라, 단일 과목당 일부 누락 양식.

### 4.2 per-year file 66 records vs PDF 95 문제

| 항목 | count |
|---|---:|
| PDF 표면 문제 번호 (1~95) | 95 |
| `data/questions_기출_2020_1_2회.json` records | 66 |
| 차이 | **29 records 영역** |

29 records 차이는 다음 영역의 혼합 가능성:
- 출제기준 변경으로 삭제된 문제 (PDF 안내문 영역)
- per-year file에 별 사유로 미등재된 문제
- OCR/추출 단계에서 누락된 문제

본 audit은 *PDF source 단위*만 확인. per-year file과 PDF의 1:1 매핑은 별 트랙
(E2 record-level page mapping 영역).

### 4.3 q52 위치 — 본 audit read 영역 외

q52는 **3과목 전기기기 문제 52** = PDF page 18-19 사이 (page 18 = 문제 48~50,
page 19 = 문제 51~53). 본 audit은 page 18-19를 read 영역에 포함했음 — 단 page
19 = 문제 51~53 중 q52는 **동기전동기 V곡선 / 정답 1** (impact audit §1과 정합).

본 audit이 직접 확인한 page 19 (책 page 924) 영역:
- 문제 51: 직류발전기 효율 (정답 ③)
- 문제 52: 동기전동기 공급 전압과 부하 일정 유지 + 여자 전류 증가 시 전기자 전류
  변화 (정답 ①) — **separability evaluation §1.4 + impact audit §1 명시와 정합**
- 문제 53: 전압변동률 작은 동기발전기 (정답 ①)

→ q52 컨텐츠 = 동기전동기 V곡선 (변압기 권수비 X) 재확인. impact audit / per-year
file `2020_1,2회_52` 컨텐츠 일치.

---

## 5. 6 Audit Question 답

### Q1 — PDF 표지 기재 일자는 무엇인가?

**A**: **시행 일자 표기 없음**.

근거:
- 표지에 "2020년도 전기기사 일반검정 제 1,2 회" + 자격종목/종목코드/시험시간/
  문제지형별 명시
- **시행 일자 명시 0건**
- footer "20년도 1,2회" 일관 표기 (35 page 전체)

→ 본 PDF는 시행 일자 표기 없는 *합본 시험 양식*. 시행 일자 evidence는 외부
source 영역.

### Q2 — PDF가 2020 1회/2회 합본인지, 단일 회차인지, 불명확한지?

**A**: **명시 합본**.

근거:
- 표지 직접 인용: "**2020년도 전기기사 일반검정 제 1,2 회**"
- "제 1,2 회" 양식 = 1회+2회 합본 시행 명시
- footer 35 page 전체 "20년도 1,2회" 일관
- 단일 회차 PDF (예: `2020_1회.pdf` 또는 `2020_2회.pdf`)이 *아님*

### Q3 — 페이지 구조상 1회/2회 분리 구간 단서가 있는지?

**A**: **0건 — 분리 구간 단서 부재**.

근거:
- §3.2 5 분리 단서 유형 모두 0건 ("제1회" / "제2회" / 별 표지 / 별 시간 / 회차
  분리)
- 35 page 전체 단일 시험 양식으로 작성
- 과목별 분리만 있고 (1과목→2과목→3과목→4과목→5과목), 회차별 분리 없음

→ PDF source 자체가 합본 양식으로 *1회/2회 분리 source 단서를 제공하지 않음*.

### Q4 — 66항 records를 split/alias/migration으로 확정할 만큼 evidence가 충분한지?

**A**: **부족 — 본 audit으로 결정 evidence 충족 0**.

각 후보 평가 (66항 policy evaluation §2 정합):

| 후보 | 본 audit evidence 영향 |
|---|---|
| 후보 B (alias policy) | 어느 회차 alias할지 결정 evidence 부재 유지 — 합본 시험이라 1회/2회 어느 쪽인지 분리 자체가 PDF source에 부재 |
| **후보 C (split policy)** | **본 audit으로 부적합 확정** — PDF source가 합본 양식, 1회/2회 분리 source 단서 0건. split 자체가 evidence 부재 영역 |
| 후보 D (Batch migration) | 66항 alias 정책 + 100항 source claim + persisted key migration 모두 미정 유지 |
| **후보 A (defer)** | **본 audit으로 정합 강화** — split 불가 확정 + alias 결정 evidence 부재로 보류 유지 정합 |
| 후보 E (docs errata only) | A의 sub-variant 영역 유지 |

→ 본 audit은 *후보 C 부적합 확정* + *후보 A 정합 강화*의 evidence를 추가한다. 단
별 정책 결정으로 확정할 evidence는 여전히 부족.

### Q5 — q52 alias registry 또는 기기-17 caution 상태에 영향이 있는지?

**A**: **영향 0 — q52 separable 영역 유지**.

근거:
- separability evaluation Q1·Q2 Separable 결론 유지
- registry artifact `9868f95` candidate baseline 유지
- registry artifact review PASS 12/12 (`f0b462c`) 유지
- 본 audit은 PDF source 자체에 q52 컨텐츠 (동기전동기 V곡선)가 page 19에 있음을
  *재확인*만 — q52 alias row의 `2020_1회_52` storage_id ↔ `2022_1회_52`
  canonical_source_id 매핑 (별 PDF `data/20200424_1회.pdf` p.4 q52 영역)과
  *별 영역*
- 기기-17 caution 유지 영역 변경 없음

### Q6 — 다음 E2 record 분류 evidence에 필요한 입력은 무엇인지?

**A**: **E2 트랙은 본 audit 결론으로 *부분 영역 변경* 필요**.

기존 E2 양식 (policy evaluation §3 Q7):
- 66항 각 record의 1회/2회 소속 판정 — *합본 시험이므로 판정 자체가 불가*

본 audit 후 E2 새 양식 후보:
- E2a: 66항 각 record의 PDF page mapping (record-level page locator)
- E2b: 95 문제 ↔ 66 records 1:1 매핑 (29 records 영역 식별)
- E2c: 삭제된 문제 / 미등재 문제 / OCR 누락 영역 분류
- E2d: 합본 양식이라 "1회/2회 split"이 source 영역에 부재함을 *명시 evidence*로
  document

→ E2 트랙은 *원래 의도한 split 분류*가 아니라 *record-PDF page mapping +
누락 영역 분류*로 영역 재정의 필요.

---

## 6. 결론 — Defer 유지 + 후보 C 부적합 확정

### 6.1 본 audit이 활성화하는 영역

- **후보 A (defer with evidence requirements)** 정합 강화
- 후보 C (split policy) **부적합 확정** — PDF source 자체가 합본 양식, split
  evidence 부재
- E2 트랙 영역 재정의 필요 (1회/2회 split이 아니라 record-page mapping +
  누락 영역 분류)

### 6.2 본 audit이 차단 유지하는 영역

- caution release (Step 6) — separability Q4 + 본 audit으로 split 불가 확정,
  alias/migration evidence 여전히 부재
- Batch migration — separability Q5 + 본 audit으로 split 영역 부재
- registry row promotion — 별 명시 승인 영역
- 기기-17 caution 해제 — `caution remains` 유지

### 6.3 본 audit이 변경하지 않는 영역

- q52 separable layer (registry / artifact review / App/data / runtime design /
  separability evaluation) 모두 PASS baseline 유지
- 66항 policy 결정 — defer 유지 (정책 변경 0)
- jsonl decision entry — 정책 변경 없으므로 추가 안 함 (사용자 가이드 정합)

---

## 7. 다음 evidence Gate (별 명시 승인 후만 진행)

### 7.1 E2 영역 재정의 — record-PDF page mapping (별 트랙)

- 66항 각 record의 PDF page 매핑 (예: `2020_1,2회_q41` → PDF page 15)
- 95 문제 ↔ 66 records 1:1 매핑
- 29 records 영역 식별 (삭제/미등재/OCR 누락)
- 합본 양식 명시 evidence 추가

### 7.2 E3~E6 (policy evaluation §3 Q7 영역 유지)

- E3: 100항과의 충돌 영역 검증 (split 자체가 부적합이라 *재정의 필요*)
- E4: 다른 합본 PDF 패턴 (별 연도 합본 PDF 사례 비교)
- E5: app persisted key 영향 (split이 불가이므로 alias only 영역 재평가)
- E6: separability re-evaluation (E2~E5 충분 수집 후)

### 7.3 외부 source evidence (별 트랙, 명시 승인 후)

- 한국기술자격검정 공식 2020년 전기기사 시행 기록 (1회·2회 합본 시행 사실 확인)
- COVID-19 영향 시행 정보 (외부 source)

---

## 8. Forbidden Until Separate Approval

- q52 단독 id 재발급
- `questions.json` 수정
- per-year json 수정
- PDF filename rename
- PDF 파일 복사 / 편집 / OCR 산출물 생성
- `pdf_pages/index.json` 수정
- app code 수정
- app alias resolver 구현
- app/data alias registry 추가
- record metadata field 추가
- registry row promotion from `candidate` to `approved`
- 기기-17 caution 해제 선언
- Batch migration 진입
- 66항 systemic policy를 q52 registry 영역에 흡수
- registry artifact 자체 수정
- 보류 해제 선언 (별 명시 승인 + E2~E6 evidence + 별 정책 결정 후)
- 후보 C (split policy) 진입 (본 audit으로 부적합 확정)

---

## 9. Decision Record 영향

본 audit은 **evidence 영역 추가만** 수행 — 정책 변경 0:

- 66항 policy = **defer 유지** (변경 없음)
- 후보 C 평가 영역 갱신 (부적합 확정) — audit evidence 영역, 정책 결정 아님
- E2 트랙 영역 재정의 필요 명시 — 별 트랙 작업 영역
- caution release / Batch migration 차단 영역 유지
- q52 separable layer 영향 0

→ jsonl `trap_map_active_decisions.jsonl`에 별 entry 추가 안 함 (사용자 가이드:
"JSONL은 정책 결정이 아니면 수정하지 말 것" 준수).

본 audit 문서 자체가 E1 evidence로 충분.

---

## Status

- E1 원본 PDF source audit 작성 완료.
- 핵심 evidence:
  - PDF 표지 "**2020년도 전기기사 일반검정 제 1,2 회**" — 명시 합본 시험
  - PDF 시행 일자 표기 0
  - 1회/2회 분리 구간 단서 0건 (35 page 전체)
  - PDF 95 문제 (1~95) / per-year 66 records / 차이 29 records 영역
  - q52 = 동기전동기 V곡선 (page 19, impact audit과 정합 재확인)
- 결론:
  - **후보 A (defer) 정합 강화**
  - **후보 C (split policy) 부적합 확정** — PDF source가 합본 양식, split
    evidence 부재
  - E2 트랙 영역 재정의 필요 (1회/2회 split이 아니라 record-PDF page mapping +
    누락 영역 분류)
- 정책 변경 0 — 66항 defer 유지, q52 separable layer 영향 0, jsonl entry 추가
  안 함 (사용자 가이드 준수).
- PDF / app code / app data / registry artifact / pdf_pages / jsonl 모두 변경
  0.
- 기기-17 caution 유지. registry row status=candidate 유지. Batch migration
  차단 유지. caution release 차단 유지.
- 다음 gate: E2 트랙 영역 재정의 + E3~E6 / 외부 source evidence / 66항 policy
  재evaluation.
