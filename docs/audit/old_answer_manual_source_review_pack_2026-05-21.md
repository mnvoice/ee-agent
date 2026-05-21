# Old Answer Manual Source Review Pack (2026-05-21)

Review sheet for a human to verify the `q.answer` of the 30 C1 pilot questions
(1998-2016) against the original exam PDFs. This is NOT an answer-correction
step: no answer, choice, or solution is changed here. The reviewer fills the
blank fields per item; routing happens after that.

- Pilot source: `docs/audit/old_solution_quality_q2_dryrun_2026-05-21.md`
- Decision: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## 1. Why the automated crop+OCR path (V2-A) was blocked

- `data/batch_answer_key/mapping.json` `ak_*` pages are NOT a per-question
  answer index — they name only 2 pages per 회차, which do not contain the
  pilot questions' 풀이/answer markers.
- Pilot `문제 {q_no}` header found in the mapped ak-page OCR: **0 / 30**.
- Old exam PDFs (esp. 1998-2007) are low-quality scans; tesseract garbles even
  the Korean body text.
- Answer markers are scanned circled numbers (①②③④); local OCR cannot read
  them reliably.
- Conclusion: automated source-answer extraction is not feasible with local
  tools; the 30 items move to this manual review pack.

## 2. Manual verdict definitions

- `source_answer_verified` — source answer found in the PDF and it equals `q.answer`.
- `source_answer_conflict` — source answer found and it differs from `q.answer`.
- `source_choice_ocr_corrupt` — choices are too OCR-damaged to map an answer.
- `needs_better_scan` — the source page is unreadable; a better scan is required.
- `defer` — source ambiguous / structure unclear; hold.

## 3. Apply gate (re-confirmed)

- Only `source_answer_verified` items become answer-locked regeneration candidates.
- `source_answer_conflict` items go to a separate answer correction track.
- `source_choice_ocr_corrupt` items go to a separate choice recovery track.
- Q2 apply stays BLOCKED until manual review is complete and routed.

## 4. Pilot 30 — manual review entries

Reviewer: open the source PDF, find the question by `q_no`, read its 풀이 and
`[답]` marker, then fill the blank fields.

### 1. `1998_4회_10`

- current_q_answer: 1 | subject: 전기자기학 | q_no: 10
- source PDF: `data/문제_1998_4회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 경계조건 계산은 보기 4(μ₀(4,-8,8)), q.answer=1
- reviewer action: 원문 PDF에서 문제 10의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 2. `2001_1회_21`

- current_q_answer: 2 | subject: 전력공학 | q_no: 21
- source PDF: `data/문제_2001_1회_20260316.pdf`
- dry-run status: proposed_solution_written
- suspected issue: q.answer 표준 이론 일치 — 구해설이 보기번호 오결론
- reviewer action: 원문 PDF에서 문제 21의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 3. `2001_1회_68`

- current_q_answer: 1 | subject: 제어공학 | q_no: 68
- source PDF: `data/문제_2001_1회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 포물선 입력 lim s²GH=가속도 오차상수 보기 3, q.answer=1
- reviewer action: 원문 PDF에서 문제 68의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 4. `2001_3회_41`

- current_q_answer: 2 | subject: 전기기기 | q_no: 41
- source PDF: `data/문제_2001_3회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — '옳지 않은 것'=철손 증가(무부하손) 보기 4, q.answer=2(여자전류 불변=참)
- reviewer action: 원문 PDF에서 문제 41의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 5. `2001_3회_43`

- current_q_answer: 1 | subject: 전기기기 | q_no: 43
- source PDF: `data/문제_2001_3회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: OCR corrupt — 보기 본문 OCR 손상(3자 권선/승압콘/3도분만 젬에)
- reviewer action: 원문 PDF에서 문제 43의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 6. `2002_1회_32`

- current_q_answer: 1 | subject: 전력공학 | q_no: 32
- source PDF: `data/문제_2002_1회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: OCR corrupt — 보기 1이 \end{table} 잔재로 판독 불가
- reviewer action: 원문 PDF에서 문제 32의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 7. `2002_3회_4`

- current_q_answer: 2 | subject: 전기자기학 | q_no: 4
- source PDF: `data/문제_2002_3회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 차원상 전위형은 보기 4, q.answer=2(전계 차원)
- reviewer action: 원문 PDF에서 문제 4의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 8. `2005_3회_83`

- current_q_answer: 4 | subject: 전기설비기술기준 | q_no: 83
- source PDF: `data/문제_2005_3회_20260316.pdf`
- dry-run status: proposed_solution_written
- suspected issue: q.answer 표준 이론 일치 — 구해설 결론 waffling
- reviewer action: 원문 PDF에서 문제 83의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 9. `2006_1회_6`

- current_q_answer: 4 | subject: 전기자기학 | q_no: 6
- source PDF: `data/문제_2006_1회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 발열량 0.24CV²t/ρε(V²)은 보기 3, q.answer=4(CVt)
- reviewer action: 원문 PDF에서 문제 6의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 10. `2006_1회_7`

- current_q_answer: 2 | subject: 전기자기학 | q_no: 7
- source PDF: `data/문제_2006_1회_20260316.pdf`
- dry-run status: proposed_solution_written
- suspected issue: q.answer 표준 이론 일치 — 구해설이 발산값 3과 보기번호 3 혼동
- reviewer action: 원문 PDF에서 문제 7의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 11. `2006_2회_27`

- current_q_answer: 3 | subject: 전력공학 | q_no: 27
- source PDF: `data/문제_2006_2회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 제수문=유량 조정 보기 4, q.answer=3(모래 배제)
- reviewer action: 원문 PDF에서 문제 27의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 12. `2007_1회_9`

- current_q_answer: 4 | subject: 전기자기학 | q_no: 9
- source PDF: `data/문제_2007_1회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — A·B=0 → a=-1/3 보기 2, q.answer=4
- reviewer action: 원문 PDF에서 문제 9의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 13. `2007_2회_64`

- current_q_answer: 2 | subject: 회로이론 | q_no: 64
- source PDF: `data/문제_2007_2회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — Routh 제1열 전부 양수 → 안정 보기 1, q.answer=2
- reviewer action: 원문 PDF에서 문제 64의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 14. `2014_2회_50`

- current_q_answer: 3 | subject: 전기기기 | q_no: 50
- source PDF: `data/문제_2014_2회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — V곡선=출력 일정 시 계자-전기자 보기 2, q.answer=3
- reviewer action: 원문 PDF에서 문제 50의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 15. `2014_3회_62`

- current_q_answer: 4 | subject: 회로이론 | q_no: 62
- source PDF: `data/문제_2014_3회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict + OCR — 라플라스 1/s 필요, 보기 z변환부 OCR 손상
- reviewer action: 원문 PDF에서 문제 62의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 16. `2015_1회_13`

- current_q_answer: 1 | subject: 전기자기학 | q_no: 13
- source PDF: `data/문제_2015_1회_20260316.pdf`
- dry-run status: proposed_solution_written
- suspected issue: q.answer 표준 이론 일치 — 구해설이 sin²을 cos²로 오산
- reviewer action: 원문 PDF에서 문제 13의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 17. `2015_1회_22`

- current_q_answer: 1 | subject: 전력공학 | q_no: 22
- source PDF: `data/문제_2015_1회_20260316.pdf`
- dry-run status: proposed_solution_written
- suspected issue: q.answer 표준 이론 일치 — 구해설 오결론
- reviewer action: 원문 PDF에서 문제 22의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 18. `2015_1회_71`

- current_q_answer: 4 | subject: 전기자기학 | q_no: 71
- source PDF: `data/문제_2015_1회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — L=12H, τ=L/R=1s 보기 1, q.answer=4(0.001)
- reviewer action: 원문 PDF에서 문제 71의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 19. `2015_1회_87`

- current_q_answer: 3 | subject: 전기설비기술기준 | q_no: 87
- source PDF: `data/문제_2015_1회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 옥내전로 대지전압 300V 보기 2, q.answer=3(350)
- reviewer action: 원문 PDF에서 문제 87의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 20. `2015_2회_23`

- current_q_answer: 3 | subject: 전력공학 | q_no: 23
- source PDF: `data/문제 _2015_2회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — π형 송전단전류 보기 4, q.answer=3(보정항 누락)
- reviewer action: 원문 PDF에서 문제 23의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 21. `2015_2회_29`

- current_q_answer: 1 | subject: 전력공학 | q_no: 29
- source PDF: `data/문제 _2015_2회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 피뢰기 보기 2, q.answer=1(직렬리액터)
- reviewer action: 원문 PDF에서 문제 29의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 22. `2015_3회_22`

- current_q_answer: 4 | subject: 전력공학 | q_no: 22
- source PDF: `data/문제 _2015_3회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 제3고조파 제거=△결선 보기 1, q.answer=4(콘덴서)
- reviewer action: 원문 PDF에서 문제 22의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 23. `2015_3회_25`

- current_q_answer: 1 | subject: 전력공학 | q_no: 25
- source PDF: `data/문제 _2015_3회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: OCR corrupt — 보기 4 OCR 손상(footer 혼입)
- reviewer action: 원문 PDF에서 문제 25의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 24. `2015_3회_27`

- current_q_answer: 3 | subject: 전력공학 | q_no: 27
- source PDF: `data/문제 _2015_3회_20260316.pdf`
- dry-run status: proposed_solution_written
- suspected issue: q.answer 표준 이론 일치 — 구해설 오결론
- reviewer action: 원문 PDF에서 문제 27의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 25. `2016_1회_44`

- current_q_answer: 2 | subject: 전기기기 | q_no: 44
- source PDF: `data/문제_2016_1회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: ambiguous — 보기 2·4 표현 모호(전기적/기하학적 중성축 혼용)
- reviewer action: 원문 PDF에서 문제 44의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 26. `2016_1회_69`

- current_q_answer: 1 | subject: 전력공학 | q_no: 69
- source PDF: `data/문제_2016_1회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 안정도 최소관계=고유주파수 보기 4, q.answer=1(공진치)
- reviewer action: 원문 PDF에서 문제 69의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 27. `2016_1회_70`

- current_q_answer: 2 | subject: 제어공학 | q_no: 70
- source PDF: `data/문제_2016_1회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 임계점 -1+j0 → 0dB·±180° 보기 4, q.answer=2
- reviewer action: 원문 PDF에서 문제 70의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 28. `2016_1회_71`

- current_q_answer: 3 | subject: 제어공학 | q_no: 71
- source PDF: `data/문제_2016_1회_20260316.pdf`
- dry-run status: proposed_solution_written
- suspected issue: q.answer 표준 이론 일치 — 구해설이 El=Ep 풀고도 보기번호 1로 오기
- reviewer action: 원문 PDF에서 문제 71의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 29. `2016_3회_21`

- current_q_answer: 1 | subject: 전력공학 | q_no: 21
- source PDF: `data/문제_2016_3회_20260316.pdf`
- dry-run status: needs_source_answer_check
- suspected issue: q.answer conflict — 전선 단면적 A∝1/V² 보기 4, q.answer=1(전류 비례)
- reviewer action: 원문 PDF에서 문제 21의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____

### 30. `2016_3회_44`

- current_q_answer: 4 | subject: 전기기기 | q_no: 44
- source PDF: `data/문제_2016_3회_20260316.pdf`
- dry-run status: proposed_solution_written
- suspected issue: q.answer 표준 이론 일치 — 구해설이 무부하시험 풀고도 보기번호 1로 오기
- reviewer action: 원문 PDF에서 문제 44의 풀이/[답] 마커 확인 → source_answer 기록, 보기 OCR 상태 확인
- source_answer: _____
- source_page: _____
- evidence_note: _____
- verdict: _____
