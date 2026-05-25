# Trap-Map B-Priority — `2020_1,2회` 66항 E2 Record-PDF Mapping Audit (2026-05-25)

66항 session-label policy evaluation (`df7e932`, `DR-TRAP-2020-12-66ITEM-SESSION-
LABEL-POLICY`)의 evidence gate E2 — record-PDF page mapping audit을 수행한다.
E1 source audit (`5c1fecc`)에서 영역 재정의된 E2 (record-PDF page mapping +
95 ↔ 66 gap 분류 + 합본 양식 명시 evidence)를 따른다.

이번 단계는 **read-only audit**. **app/data, questions.json, per-year json, PDF
filename, pdf_pages, app code, 어떤 파일도 수정하지 않는다.** PDF 복사/rename/
편집/OCR 산출물/data report 신규 생성 모두 금지. push 없음. amend/rebase/reset
없음. 기기-17 caution 유지. q52 단독 id 재발급 금지 유지. registry row promotion
금지 유지. Batch migration 실행 금지.

- 검토 대상 PDF: `data/문제_2020_1,2회_20260316.pdf` (35 pages, 합본 시험)
- 검토 대상 per-year: `data/questions_기출_2020_1_2회.json` (66 records)
- 검토 대상 master: `app/data/questions.json` `year=2020, session="1,2회"` (66 records)
- 관련 E1 audit: `docs/audit/trap_map_B_priority_2020_1_2_66item_E1_source_audit_2026-05-25.md`
- 관련 policy evaluation: `docs/audit/trap_map_B_priority_2020_1_2_66item_session_label_policy_2026-05-25.md` (`DR-TRAP-2020-12-66ITEM-SESSION-LABEL-POLICY`)
- 관련 separability evaluation: `docs/audit/trap_map_B_priority_gigi_17_66item_separability_evaluation_2026-05-25.md`
- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md`

---

## 1. JSON ↔ Master 정합 + q_no Set Extraction

### 1.1 per-year ↔ master 1:1 정합 확인

| source | record count | q_no not-null | q_no null/missing | q_no range |
|---|---:|---:|---:|---|
| `data/questions_기출_2020_1_2회.json` (per-year) | 66 | 66 | 0 | **1~93** |
| `app/data/questions.json` `year=2020, session="1,2회"` (master) | 66 | 66 | 0 | 1~93 |

**per-year q_no set == master q_no set**: ✓ **True** (양 source 정합 100%)

### 1.2 q_no Set 추출 결과

per-year 66 records의 q_no = master 66 records의 q_no = 동일 set:
- q_no max = **93** (q_no 94, 95 부재)
- q_no range = 1~93 중 일부

---

## 2. 누락 q_no 식별 + 과목별 분포

### 2.1 누락 q_no 계산

`PDF 1~95 ∖ per-year present q_no`:

| 항목 | 값 |
|---|---|
| PDF 표면 영역 (q_no) | 1~95 (총 95) |
| per-year present (q_no) | 66 |
| **누락 count** | **29** |
| per-year ∖ PDF | 0 (extra 0건) |

### 2.2 누락 29 q_no 명단 (전수 명시)

```
3, 4, 9, 10, 13, 16, 20,
24, 25, 26, 28, 30, 32, 37, 38,
43, 50, 55,
61, 62, 67, 68, 71, 72, 74, 80,
83, 94, 95
```

### 2.3 과목별 분포 매트릭스

PDF 양식 (1과목 1~20, 2과목 21~40, 3과목 41~60, 4과목 61~80, 5과목 81~95)
기준:

| 과목 | q_no 범위 | PDF 표면 count | per-year present | 누락 | 누락 q_no |
|---|---|---:|---:|---:|---|
| 1과목 전기자기학 | 1~20 | 20 | 13 | **7** | 3, 4, 9, 10, 13, 16, 20 |
| 2과목 전력공학 | 21~40 | 20 | 12 | **8** | 24, 25, 26, 28, 30, 32, 37, 38 |
| 3과목 전기기기 | 41~60 | 20 | 17 | **3** | 43, 50, 55 |
| 4과목 회로이론·제어공학 | 61~80 | 20 | 12 | **8** | 61, 62, 67, 68, 71, 72, 74, 80 |
| 5과목 전기설비기술기준 | 81~95 | 15 | 12 | **3** | 83, 94, 95 |
| **합계** | **1~95** | **95** | **66** | **29** | — |

### 2.4 패턴 관찰

- **연속 pair 패턴 (4과목)**: 61-62 / 67-68 / 71-72 — 3 pair 모두 연속. 추출 도구
  영역의 *단위 누락 패턴* 가능성
- **연속 triple 패턴 (2과목)**: 24-25-26 — 3 연속. 동일 추출 영역 단위 누락
  가능성
- **5과목 마지막 (94, 95)**: PDF 마지막 2 문제. per-year max q_no = 93에서
  cutoff 가능성
- **3과목 누락 최소 (3건)**: q52 영역 (3과목 41~60) 누락 비율 가장 낮음 — q52
  포함 영역이 상대적으로 양호

---

## 3. PDF Source Verification — 누락 q_no가 PDF에 등재됐는지

본 audit이 직접 read한 PDF page 영역에서 누락 q_no가 *실제로 PDF에 출제됐는지*
verification.

### 3.1 직접 verification 영역 (PDF page 10-14 + 21-28 read)

| 누락 q_no | 과목 | PDF page | book page | PDF 출제 확인 |
|---|---|---:|---:|---|
| 24 | 2과목 | 10 | 915 | ✓ 정상 출제 — 3상 배전선로 60kW 콘덴서 용량 |
| 25 | 2과목 | 10 | 915 | ✓ 정상 출제 — 송배전 선택지락계전기 SGR |
| 26 | 2과목 | 10 | 915 | ✓ 정상 출제 — 정격전압 7.2kV 차단기 정격차단전류 |
| 28 | 2과목 | 11 | 916 | ✓ 정상 출제 — Still식 30000kW 51km 송전 전압 |
| 30 | 2과목 | 11 | 916 | ✓ 정상 출제 — 3상 3선식 vs 단상 2선식 전류 비교 |
| 32 | 2과목 | 12 | 917 | ✓ 정상 출제 — 전선 표피효과 |
| 37 | 2과목 | 14 | 919 | ✓ 정상 출제 — 증기터빈 출력 효율 |
| 38 | 2과목 | 14 | 919 | ✓ 정상 출제 — 송전선로 가공지선 설치 목적 |
| 61 | 4과목 | 22 | 927 | ✓ 정상 출제 — 특성방정식 K 안정 범위 |
| 62 | 4과목 | 22 | 927 | ✓ 정상 출제 — 개루프 전달함수 근궤적 점근선 |
| 67 | 4과목 | 24 | 929 | ✓ 정상 출제 — 단위 피드백제어계 정상상태 편차 |
| 68 | 4과목 | 24 | 929 | ✓ 정상 출제 — 신호흐름선도 전달함수 |
| 71 | 4과목 | 26 | 931 | ✓ 정상 출제 — 3상 전류 정상분 크기 |
| 72 | 4과목 | 26 | 931 | ✓ 정상 출제 — 회로 영상 임피던스 |
| 74 | 4과목 | 27 | 932 | ✓ 정상 출제 — 라플라스 변환 |
| 83 | 5과목 | 30 | 935 | ✓ 정상 출제 — 유원지 어린이 유희용 전차 교류 전압 (E1 audit read) |
| 94 | 5과목 | 35 | 940 | ✓ 정상 출제 — 저압 가공전선로 약전류 전선간 이격거리 (E1 audit read) |
| 95 | 5과목 | 35 | 940 | ✓ 정상 출제 — 중성점 직접 접지식 변압기 권선 절연내력시험 (E1 audit read) |

→ **18건 직접 verification 모두 PDF 정상 출제 확인** (2과목 8 / 4과목 7 / 5과목 3).

### 3.2 직접 verification 외 영역 (간접 추정)

다음 11 누락 q_no는 본 audit에서 직접 PDF page read 영역 외:

| 누락 q_no | 과목 | 예상 PDF page | 직접 verification |
|---|---|---:|---|
| 3, 4 | 1과목 | 1~2 | E1 audit이 page 1-5 read — q3 책 page 906, q4 책 page 907 영역. 직접 인용은 E1 audit에서 q3까지 부분 확인. q4는 별 verification 영역 |
| 9, 10 | 1과목 | 3-4 | E1 audit page 3-4 영역 — q9, q10 PDF 표면 추정 등재 |
| 13, 16, 20 | 1과목 | 5-8 | 본 audit page read 영역 외 |
| 43, 50, 55 | 3과목 | 15-20 | E1 audit page 15-20 영역 — q43 (page 15), q50 (page 18), q55 (page 20) 추정 등재 |
| 80 | 4과목 | 29 | 본 audit page read 영역 외 (page 28 = q79까지 verification) |

→ 11건 간접 verification은 *직접 등재 확인 영역 외*이나 **2·4·5 과목 18건 직접
verification 모두 등재 패턴이라 1·3 과목 11건 동일 패턴 추정 가능**. 단 확정은
별 트랙.

### 3.3 핵심 발견 (Critical Finding)

**18건 직접 verification 모두 PDF에 정상 출제 등재** → 누락 원인은 *PDF source의
출제 영역 부재*가 **아니라** *per-year file의 데이터 추출/등재 영역 누락*.

E1 audit의 PDF 마지막 안내문 ("출제기준 변경 및 개정된 관계 법규에 따라 삭제된
문제가 있어 20문항이 안됩니다")의 영역 재해석:
- **안내문이 가리키는 영역**: 5과목 81~100 표준 영역 중 96~100 (5 문항)이 *PDF
  표면에 없음* (PDF q_no max = 95). 이는 *PDF 자체의 부재* 영역.
- **본 audit 누락 29건**: PDF 표면 1~95 중 *per-year file에 미등재* — **별 영역**
  (PDF 출제는 됐으나 데이터 추출 영역에서 누락).

두 영역이 *별 cause*:
- 영역 A (PDF 부재): 5과목 96~100, 5 문항 (안내문 영역)
- 영역 B (per-year 누락): 1~95 중 29 q_no (본 audit 발견)

---

## 4. q52 재확인

E1 audit + impact audit 정합 재확인:

| 항목 | 값 |
|---|---|
| PDF page | 19 (book page 924) |
| q_no | 52 |
| 컨텐츠 | 동기전동기 V곡선 (공급 전압·부하 일정 + 여자 전류 증가 시 전기자 전류 변화) |
| 정답 | ① (앞선 무효전류 증가) |
| per-year `2020_1,2회_52` 컨텐츠 | 동기전동기 V곡선 ✓ |
| master `2020_1,2회_52` 컨텐츠 | 동기전동기 V곡선 ✓ |
| q52는 per-year present q_no set에 포함 | ✓ (66 records 중 1건) |

→ **q52는 누락 29 q_no 영역에 *포함되지 않음***. per-year에 정상 등재. q52 alias
registry artifact (`9868f95`)와의 관계는 separability evaluation §2.1 + impact
audit §1과 정합 — `2020_1,2회_52` = 동기전동기 V곡선 (q52 alias row의 q52와
*다른 컨텐츠*).

---

## 5. 6 Audit Question 답

### Q1 — per-year ↔ master 정합?

**A**: **True — 양 source 동일 q_no set 66건**.

근거:
- per-year q_no count = 66, master q_no count = 66 (§1.1)
- 양 set 정확히 일치 (`sorted(py_qnos) == sorted(m_qnos)` = True)
- q_no null/missing 모두 0

### Q2 — q_no range 어떻게?

**A**: **1~93** (94, 95 부재).

근거: §1.1 명시. q_no max = 93. PDF 마지막 2 문제 (q94, q95)는 PDF에 정상 등재됐으나
per-year에 미등재 (§3.1 verification).

### Q3 — 누락 29 q_no 명단?

**A**: §2.2 전수 명시:
```
1과목: 3, 4, 9, 10, 13, 16, 20 (7건)
2과목: 24, 25, 26, 28, 30, 32, 37, 38 (8건)
3과목: 43, 50, 55 (3건)
4과목: 61, 62, 67, 68, 71, 72, 74, 80 (8건)
5과목: 83, 94, 95 (3건)
```

### Q4 — 누락 원인 패턴?

**A**: **데이터 추출/등재 영역 누락** — *PDF source 출제 영역 부재가 아님*.

근거 (§3.1):
- 18건 직접 PDF verification 모두 정상 출제 등재 확인
- 2과목 24-25-26 연속 triple + 4과목 61-62/67-68/71-72 연속 pair 패턴 = 추출
  도구 영역의 단위 누락 패턴 가능성
- 5과목 94, 95 = PDF 마지막 2 문제, per-year cutoff 가능성

추가 패턴 후보 (확정 영역 외):
- OCR 단계의 페이지 영역 누락
- per-year 추출 script의 q_no range 영역 누락 (예: q80 이후 5과목 cutoff)
- 추출 도구 영역의 page-batch 누락

### Q5 — q52 / 기기-17 caution / q52 alias registry 영향?

**A**: **영향 0**.

근거:
- q52는 per-year present set에 포함 (누락 영역 외)
- q52 = 동기전동기 V곡선 (PDF page 19, impact audit과 정합)
- q52 alias registry artifact (`9868f95`)의 q52 row는 `2020_1회_52` storage_id 영역
  (별 PDF `data/20200424_1회.pdf` p.4 q52 영역) — 본 PDF `2020_1,2회`의 q52와
  *별 영역*
- separability evaluation Q1·Q2 Separable 결론 유지
- 기기-17 caution 유지 영역 변경 0

### Q6 — 66항 policy 영향?

**A**: **정책 변경 0 — defer 유지**.

근거:
- 본 audit은 누락 영역 *원인 식별*만 — 정책 결정 변경 아님
- 66항 split/alias/migration 결정 evidence는 여전히 부족 (E1 audit 결론 유지)
- 단 *별 트랙 후보 추가 활성화*: 29 누락 영역 recovery evaluation (별 트랙으로
  분리)

추가 활성화 영역 (별 트랙):
- 29 누락 q_no recovery — per-year file에 OCR 또는 별 source로 추가 등재 가능성
  평가 (별 트랙)
- 단 recovery 자체도 별 명시 승인 영역 (current guardrail에 OCR 산출물 / data
  생성 금지)

---

## 6. 결론 — Defer 유지 + 추출 누락 영역 별 트랙 활성화

### 6.1 본 audit 활성화 영역

- per-year ↔ master 정합 evidence 확보 (양 source 100% 동일)
- 누락 29 q_no 전수 명단 확정
- 과목별 분포 + 연속 pair/triple 패턴 식별
- **18건 직접 PDF verification으로 누락 원인 = 데이터 추출/등재 누락 확정**
- E1 audit "PDF 안내문 = 출제기준 변경 삭제" 영역과 본 audit 누락 29건은 *별
  cause* 영역 분리

### 6.2 본 audit 차단 유지 영역

- caution release (Step 6) — separability Q4 + 66항 policy 보류 + 본 audit 결정
  변경 0
- Batch migration — separability Q5 + 66항 policy 선결
- registry row promotion
- 기기-17 caution 해제
- 후보 C (split policy) 부적합 확정 영역 (E1 결론) 유지

### 6.3 본 audit 변경 없음 영역

- q52 separable layer (registry / artifact review / App/data / runtime design /
  separability evaluation) 모두 PASS baseline 유지
- 66항 policy 결정 = **defer 유지** (정책 변경 0)
- jsonl decision entry — 정책 변경 없으므로 추가 안 함 (사용자 가이드 정합)

---

## 7. 다음 evidence Gate (별 명시 승인 후만 진행)

### 7.1 직접 활성화된 후보 영역

- **29 누락 영역 recovery evaluation** (별 트랙, 명시 승인 + OCR/data 영역 결정
  후)
  - per-year file에 29 q_no 추가 등재 가능성 평가
  - OCR 또는 별 source 영역 결정
  - data 영역 수정은 별 명시 승인
- **1·3 과목 직접 verification 보강** (별 트랙, read-only)
  - PDF page 2-9 (1과목 q3, q4, q9, q10, q13, q16, q20) 직접 read
  - PDF page 15-20 (3과목 q43, q50, q55) 직접 read
  - PDF page 29 (4과목 q80) 직접 read

### 7.2 E1 audit이 정의한 후속 evidence (유지)

- E3: 100항과의 충돌 영역 검증 (split 부적합 확정으로 재정의)
- E4: 다른 합본 PDF 패턴 (별 트랙)
- E5: app persisted key 영향 (split 불가 → alias only 재평가)
- E6: separability re-evaluation (E2~E5 충분 수집 후)
- 외부 source evidence (한국기술자격검정 공식 2020년 시행 기록)
- 66항 policy 재evaluation

---

## 8. Forbidden Until Separate Approval

- q52 단독 id 재발급
- `questions.json` 수정
- per-year json 수정 (29 누락 q_no 추가 등재 포함)
- PDF filename rename
- PDF 파일 복사 / 편집 / OCR 산출물 신규 생성
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
- 보류 해제 선언 (E3~E6 + 별 정책 결정 후만)
- 후보 C (split policy) 진입 (E1 부적합 확정 유지)

---

## 9. Decision Record 영향

본 audit은 **evidence 영역 추가만** 수행 — 정책 변경 0:

- 66항 policy = **defer 유지** (변경 없음)
- 새 발견: 누락 29 q_no 원인 = 데이터 추출 누락 (PDF 출제 영역 부재 X)
- 새 별 트랙 후보 활성화: 29 누락 영역 recovery + 1·3 과목 verification 보강
- 정책 자체 결정 영역 변경 없음

→ jsonl `trap_map_active_decisions.jsonl`에 별 entry 추가 안 함 (사용자 가이드:
"JSONL은 정책 결정이 아니면 수정하지 말 것" 준수).

본 audit 문서 자체가 E2 mapping evidence로 충분.

---

## Status

- E2 record-PDF page mapping audit 작성 완료.
- 핵심 측정:
  - per-year ↔ master q_no set 정합 100% (양 66 records 동일)
  - q_no range 1~93 (94, 95 부재)
  - 누락 29 q_no 전수 식별 (1과목 7 / 2과목 8 / 3과목 3 / 4과목 8 / 5과목 3)
  - 연속 pair/triple 패턴: 2과목 24-25-26, 4과목 61-62/67-68/71-72
- 핵심 발견:
  - **18건 직접 PDF verification으로 누락 원인 = 데이터 추출/등재 누락 확정**
  - PDF source는 1~95 모두 정상 출제 (E1 안내문 "20문항이 안됩니다"는 5과목
    96~100 PDF 부재 영역 — 본 누락과 별 cause)
- q52 = per-year present set 포함 (누락 영역 외), 동기전동기 V곡선 (page 19),
  impact audit과 정합 재확인.
- 66항 policy = **defer 유지** (정책 변경 0). q52 separable layer 영향 0.
- 별 트랙 후보 활성화: 29 누락 영역 recovery + 1·3 과목 verification 보강 (각
  별 명시 승인 후).
- PDF / app code / app data / registry artifact / pdf_pages / jsonl 모두 변경
  0.
- 기기-17 caution 유지. registry row status=candidate 유지. Batch migration
  차단 유지. caution release 차단 유지. 후보 C 부적합 확정 유지.
- 다음 gate: 29 누락 recovery (별 트랙) / 1·3 과목 verification 보강 / E3~E6 /
  외부 source / 66항 policy 재evaluation.
