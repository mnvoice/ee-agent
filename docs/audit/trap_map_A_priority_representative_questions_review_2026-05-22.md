# Trap-Map A-Priority Representative Questions — Dry-Run Review (2026-05-22)

`docs/audit/trap_map_A_priority_representative_questions_dryrun_2026-05-22.md`(이하 dry-run)
결과에 대한 리뷰다. dry-run의 주장을 (a) 출처(`app/data/questions.json`)에 대해
독립 재검증하고, 리스크를 재분류하며, 다음 배치 대상을 4버킷으로 분류한다.

이 문서는 **리뷰 + 분류**다. app/data 미수정. solution/steps 미적용.
answer/choices/text 미수정. commit/push 없음. 유료 API 미호출. local server 미실행.

- 검토 대상: `docs/audit/trap_map_A_priority_representative_questions_dryrun_2026-05-22.md`
- 재검증 (a) 출처: `app/data/questions.json` (5,331문항), v3.2 입력 문서
- 검증 도구: read-only Python 1회용 스크립트 (repo 외부 미생성, 인라인 실행)

---

## 0. 시작 전 git 확인

- `git status --short --untracked-files=no` → tracked working tree clean
- branch `feat/phase-b-migration` ↔ origin 동기 (ahead/behind 0)
- HEAD `ccc9bb4` (변동 없음)

---

## 1. 리뷰 목표별 결과

### 1.1 목표 1 — A등급 31항 추출 정확성 → 일치 확인

v3.2 입력 문서(`docs/audit/input/...v3.2...md`)의 §4.1~4.4 함정 블록 61개를
정규식으로 재파싱하여 `우선순위:` 라벨을 독립 카운트:

| 과목 | A | B | C | A 항목 번호 |
|---|--:|--:|--:|---|
| 전기기기 | 17 | 10 | 0 | 1,2,3,5,6,8,9,10,11,12,13,14,15,16,27,29,30 |
| 전기설비 | 6 | 11 | 4 | 1,5,6,9,18,19 |
| 전력공학 | 8 | 3 | 0 | 3,5,7,8,9,21,24,26 |
| 회로이론 | 0 | 1 | 1 | (없음) |
| **합** | **31** | **25** | **5** | — |

→ **dry-run의 A등급 31항 추출과 항목 번호까지 정확히 일치.** 검증 통과.
dry-run finding F0(§5.2 표 per-subject 불일치)도 재확인 — 라벨 실측은 기기 A=17,
전력 A=8로 §5.2 표(18/7)와 어긋남. F0 판정 유효.

### 1.2 목표 2 — source-clean main 21항 적절성 → **dry-run 분류에 오류 2건**

dry-run이 제시한 main 후보 29개(31항 − 부재 2) 키를 전부 `questions.json`에서
조회: **29키 전부 실재, KEY-NOT-FOUND 0, 중복 키 0.** text 내용도 dry-run 기재와 일치.

그러나 구조적 OCR/DQ 재검사(헤더 잔류물 `D-60`, latex 조각, 빈/중복 choices,
answer 범위)에서 dry-run 분류 오류를 발견:

- **R1 [중대] 설비-9 main `2020_3회_97` 오분류** — dry-run은 "source-clean"으로
  기재했으나, **정답 보기 (4)가 파괴된 페이지 헤더 잔류물**:
  `"976\nD－60 전기기사"`. answer=4이므로 **정답 보기의 실제 텍스트가 소실**됨.
  현재 데이터로는 정답 내용 확인 불가. → source-clean 아님, needs-cleanup(중증).
  - 원인: dry-run 검색 스크립트의 `ocr_risk` 검출기에 **헤더 잔류물(`D-60`) 검사가
    없었음**. latex/PUA/빈 choices/answer 범위만 검사 → 헤더형 손상이 빠져나감.
    본 리뷰의 확장 검출기(헤더 검사 추가)가 회수.
- **R2 [경미] dry-run §5 카운트 "source-clean 21 / needs-cleanup·DQ경미 8"
  재현 불가** — "8" 버킷에 명확한 편입 규칙이 없음. dry-run은 "기기-9/11, 설비-18,
  전력-8 등"만 열거하고 나머지 4를 "등"으로 처리. 실제로 dry-run은 (a) main 자체
  OCR 손상과 (b) metadata DQ 경미(tag/subject/session 오라벨)를 한 버킷에 섞었다.
  두 축은 분리해야 한다 — (b)는 학습자 노출 콘텐츠를 손상시키지 않음.

dry-run main 29건 구조 재검사 결과:

| 구조 검사 | 건수 | 항목 |
|---|--:|---|
| 구조적 clean (헤더/latex/빈/중복/answer 이상 없음) | 27 | 설비-9·18 외 전부 |
| 구조 손상 | 2 | 설비-9(헤더, 정답 보기), 설비-18(중복 보기) |

여기에 구조 검출기가 못 잡는 **한글 OCR 오타**가 1건 추가:
- 기기-9 main `2007_2회_43` 보기 (2) "각 변압기 터릭 것" — dry-run이 내용 읽기로
  이미 needs-cleanup 표기. 본 리뷰 재확인.

→ **정정된 main 후보 상태: 콘텐츠 clean 26 / needs-cleanup 3 / 부재 2.**
(dry-run의 "source-clean 21"은 metadata-DQ 항목을 clean에서 빼고 설비-9를 잘못
포함시킨 결과 — 본 리뷰가 26으로 정정.)

### 1.3 목표 3 — needs-cleanup / DQ 리스크 재분류

dry-run의 혼합 버킷("8")을 **2축으로 분리**한다:

**축 A — main 후보 콘텐츠 손상** (학습자 노출 텍스트/보기 손상, study-set 진입 차단):

| 항목 | main | 손상 | 정도 | 정답 보기 영향 |
|---|---|---|---|---|
| 기기-9 | 2007_2회_43 | 보기 (2) 한글 OCR 오타 | 중간 | 없음 (오답 보기) |
| 설비-18 | 2011_2회_92 | 보기 (2)(3) 중복 "120분" | 중간 | 없음 (정답=(4) 정상) |
| 설비-9 | 2020_3회_97 | 보기 (4) 헤더 잔류물 | 중증 | **있음 (정답 보기 소실)** |

**축 B — metadata DQ 경미** (tag/subject/session/q_type 오라벨, study-set 진입은
차단 안 함 — 콘텐츠는 정상, 통계·필터·라우팅에만 영향):

| 항목 | main | metadata 이슈 |
|---|---|---|
| 기기-6 | 2021_3회_55 | tag='변압기'(상위 개념 오라벨) |
| 기기-10 | 2021_1회_51 | tag='유도전동기'(상위 개념 오라벨) |
| 기기-11 | 2011_1_60 | session='1' 표기 이질 |
| 기기-29 | 2021_3회_57 | q_type='계산형'인데 실제 개념형 |
| 전력-5 | 2014_2회_25 | 중복쌍 (`2003_1회_31`과 동일) |
| 전력-7 | 2018_2회_25 | alt `2022_2회_21` 중복쌍 + subject='전기자기학' 오라벨 |
| 전력-8 | 2011_1_27 | session='1' 표기 이질 |
| 전력-24 | 2021_2회_26 | tag='개폐장치'(허용 태그 외) |
| 전력-26 | 2011_1_21 | subject='전기기기' 오라벨 + session='1' |

→ **축 A(콘텐츠 손상)만 study-set 진입을 차단한다.** 축 B는 콘텐츠가 정상이므로
study-set-ready를 막지 않으며, DQ 트랙에서 일괄 정정한다 (개별 A항목 deferral 아님).

설비-9 alt 후보(`2006_2회_84`, `2011_3회_87`)도 재검증 — **둘 다 OCR 손상**:
- `2006_2회_84`: 정답 보기 (4) 텍스트 정상("75[cm]…2[m]"), 단 보기 전체에 한글
  오타("저하…보부터" = 지하…로부터). → 정답 보존, 오답 보기 cleanup 필요.
- `2011_3회_87`: 보기 (2) latex 테이블 조각으로 파괴. → 손상.
→ 설비-9는 main을 alt `2006_2회_84`로 교체 시 **정답 보기 보존** 상태가 됨
(needs-cleanup, 정답 무결성 확보). 현 main `2020_3회_97`은 정답 보기 소실로 부적합.

### 1.4 목표 4 — statute-risk 2항 → statute-safe-defer 판단 **확정**

설비-5(제1종 접지공사)·설비-6(제2종 접지공사)에 대해 dry-run의 "후보 없음 +
statute-risk" 판단을 3중으로 재검증:

1. tag 버킷 — '제1종 접지공사' 45건은 text가 무관 주제·헤더 잔류물로 거의 전부
   오라벨. '제2종 접지공사' 5건도 on-topic 0.
2. text 직접 검색 — "제1종" 7건 / "제2종" 3건, **전부 "제N종 특고압 보안공사"**
   (별개 주제 — 가공전선로 보안공사).
3. choices 직접 검색 — "제1종" 5건 / "제2종" 4건, **전부 "특고압 보안공사"**.
4. 법규 — 제N종 접지공사는 KEC(한국전기설비규정, 2021 시행)에서 폐지. 계통접지
   (TN/TT/IT)로 대체. 최근 출제는 종별 접지를 다루지 않음.

→ 코퍼스에 제1·2종 **접지공사** 대표 문항이 존재하지 않음이 4중 확인됨.
**statute-safe-defer 판단 확정.** closeout(2026-05-21)의 statute-safe 트랙
(2005_3회_83, 2015_1회_87)과 동일 범주 — 설비-5/6도 같은 트랙으로 라우팅.

### 1.5 목표 5 — tag 버킷 오염 finding의 후속 처리 → DQ 트랙 finding으로 등재 (catch는 별건)

dry-run finding F1(tag 버킷 오염)·F3(OCR 잔류물)·F4(빈 choices)는 본 리뷰에서
재확인됐다. 특히 R1(설비-9 헤더형 손상)은 F3의 한 변종이 dry-run 검출기를 빠져
나간 사례다. 결정:

- **DQ 트랙 finding으로 등재** — F1/F3/F4는 corpus-wide 데이터 품질 이슈로,
  trap-map뿐 아니라 모든 후속 작업의 검색·선정 신뢰도에 영향. DQ 트랙(closeout이
  언급한 미설계 트랙)의 작업 항목으로 명시 등재 권장.
- **verify-agent Catch 등재는 별건** — tag 버킷 오염은 "검증 통로 없이 누적된 LLM
  태깅 결과"로 verify-agent CONSTITUTION §1.7(시스템 설계 시 검증 동반) 패턴에
  해당. Catalog 등재 후보이나, Catch 등재는 verify-agent 저장소의 별도 작업이며
  별도 승인이 필요 — 본 리뷰에서 자동 등재하지 않음. 후보로만 기록.

### 1.6 목표 6 — 다음 배치 4버킷 분류 → Section 3

---

## 2. 리뷰 발견 요약

| # | 발견 | 정도 | 조치 |
|---|---|---|---|
| R1 | 설비-9 main `2020_3회_97` 정답 보기 (4) 헤더 잔류물 소실 — dry-run "source-clean" 오분류 | 중대 | needs-cleanup 재분류, main을 alt `2006_2회_84`로 교체 권고 |
| R2 | dry-run §5 카운트 "source-clean 21 / 8" 재현 불가 — main 콘텐츠 손상과 metadata DQ를 한 버킷에 혼합 | 경미 | 2축 분리, 콘텐츠 clean 26 / needs-cleanup 3 / 부재 2로 정정 |
| R3 | dry-run 검색 스크립트 `ocr_risk` 검출기에 헤더 잔류물 검사 누락 | 경미 | 후속 검색 시 헤더(`D-60`/`NN년도 N회`) 검사 추가 |
| R4 | A등급 31항 추출·F0(§5.2 표 불일치)는 정확 — 검증 통과 | — | 변경 없음 |
| R5 | statute-safe-defer(설비-5/6) 판단은 4중 검증 통과 | — | 확정 |
| R6 | tag 오염(F1)·OCR 잔류물(F3)·빈 choices(F4)는 corpus-wide DQ | 중간 | DQ 트랙 finding 등재, verify-agent Catch는 별건 후보 |

dry-run의 항목별 후보 선정(어느 문항을 main으로 잡았는가)은 R1을 제외하면
(a) 출처 검증을 통과했다 — 29 main 키 전부 실재, 내용 정합.

---

## 3. 다음 배치 4버킷 분류 (A등급 31항 전체)

분류 기준:
- **study-set-ready** — main 후보의 text·choices·answer가 콘텐츠 clean. 학습 세트
  구성·후속 pedagogy 적용에 바로 진입 가능. (metadata DQ 경미는 진입 차단 안 함)
- **needs-cleanup-before-study-set** — main(또는 교체 권고 alt)의 보기/텍스트에
  OCR 손상이 있으나 **정답 보기는 보존**되거나 source 재-OCR로 복구 가능.
- **statute-safe-defer** — 법규 개정(KEC)으로 출제 기준 무효, 코퍼스에 대표 문항
  부재. statute-safe 트랙으로 이관.
- **DQ-defer** — 정답 무결성이 현 데이터로 확인 불가하거나, OCR cleanup을 넘어선
  데이터 품질 차단이 있는 항목.

### 3.1 study-set-ready — 26항

전기기기 16: 기기-1, 2, 3, 5, 6, 8, 10, 11, 12, 13, 14, 15, 16, 27, 29, 30
전기설비 2: 설비-1, 19
전력공학 8: 전력-3, 5, 7, 8, 9, 21, 24, 26

비고:
- metadata DQ 경미 9항(기기-6·10·11·29, 전력-5·7·8·24·26)은 study-set-ready 유지
  — 콘텐츠 정상. tag/subject/session/q_type 오라벨은 DQ 트랙에서 일괄 정정.
- **대표성 B-tier 4항** (study-set-ready이나 v3.2 항목 범위를 부분만 커버):
  - 기기-3: main `2012_1회_59`는 동기속도만 커버, v3.2 항목의 권계수(kp/kd)·
    유기기전력 함정 미커버 → 권계수 계산형 후보 별도 mapping 필요.
  - 기기-13: main `2015_1회_41`은 2차여자 중심, E1=4.44fΦN1 등 본 공식 미정면.
  - 기기-27: main `2010_2회_46`은 직류발전기 종류별 종합 문항, 분권발전기 단독 함정 아님.
  - 전력-21: main `2016_3회_38`은 단일 비교 축(전압상승), 4방식 종합 trade-off 아님.
  → 이 4항은 study-set 진입은 가능하나, 학습 세트 구성 시 보조 문항 추가 또는
    더 정합한 대표 문항 발굴을 권장.
- 중복쌍(전력-5 `2003_1회_31`≡`2014_2회_25`, 전력-7 `2018_2회_25`≡`2022_2회_21`)은
  study-set 구성 시 한쪽만 채택.

### 3.2 needs-cleanup-before-study-set — 3항

| 항목 | main(현/권고) | 손상 | cleanup 작업 |
|---|---|---|---|
| 기기-9 | `2007_2회_43` 유지 | 보기 (2) 한글 OCR 오타 "각 변압기 터릭 것" | 보기 (2) source 재-OCR (정답 보기 (2번 아님) 무관) |
| 설비-9 | `2020_3회_97` → **`2006_2회_84`로 교체 권고** | (현 main) 정답 보기 (4) 헤더 소실 / (권고 alt) 오답 보기 한글 오타 | main 교체 후 alt의 오답 보기 한글 오타 cleanup |
| 설비-18 | `2011_2회_92` 유지 | 보기 (2)(3) 중복 "120분" | 보기 (3) source 재-OCR (정답=(4) 정상) |

세 항목 모두 cleanup 후 study-set-ready로 승격 가능. 정답 보기는 (설비-9는 alt
교체 전제로) 보존되거나 복구 가능.

### 3.3 statute-safe-defer — 2항

- 설비-5 (제1종 접지공사 ★5 S/F)
- 설비-6 (제2종 접지공사 ★5 S/F)

KEC 폐지 구 분류 체계. 코퍼스에 대표 문항 부재(4중 검증). statute-safe 트랙
(closeout의 2005_3회_83·2015_1회_87과 동일 트랙)으로 이관. 외부 출처(구 출제기준
기출집) 확보 또는 v3.2 설비-5/6/7/8 항목군의 KEC 정합성 재검토가 선행 조건.

### 3.4 DQ-defer — 0항 (A등급 기준)

A등급 31항 중 DQ-defer로 분류되는 항목은 **없다.** 근거:
- 콘텐츠 손상 3항(기기-9·설비-9·설비-18)은 모두 정답 보기 보존(설비-9는 alt 교체
  전제) 또는 source 재-OCR로 복구 가능 → needs-cleanup으로 충분.
- 발견된 DQ 이슈(tag 오염 F1, subject 오라벨 F2, 중복쌍 F5, q_type 오라벨)는
  **corpus-wide metadata 문제**로, 개별 A항목의 study-set 진입을 차단하지 않는다.
  이들은 DQ 트랙의 일괄 작업 대상이지 개별 A항목 deferral이 아니다.
- 버킷을 채우기 위해 A항목을 DQ-defer로 강제 편입하지 않는다 (근거 없는 분류 회피).

**DQ 트랙으로 라우팅되는 것은 항목이 아니라 finding이다**: F1(tag 버킷 오염),
F2(subject 오라벨), F3(OCR 잔류물 — 헤더형 포함), F4(빈 choices), F5(중복쌍),
F6(session 표기 이질), q_type 오라벨, F8(태깅 실패 tag 값).

### 3.5 분류 요약

| 버킷 | 항목 수 | 항목 |
|---|--:|---|
| study-set-ready | 26 | 기기 16 + 설비 2 + 전력 8 |
| needs-cleanup-before-study-set | 3 | 기기-9, 설비-9, 설비-18 |
| statute-safe-defer | 2 | 설비-5, 설비-6 |
| DQ-defer | 0 | (없음 — DQ는 finding 단위로 DQ 트랙 라우팅) |
| **합** | **31** | — |

---

## 4. 권고

1. **설비-9 main 후보 교체** — `2020_3회_97`(정답 보기 소실)에서 `2006_2회_84`
   (정답 보기 보존)로 교체. dry-run 산출물의 설비-9 main 정정 필요.
2. **dry-run 산출물 정정** — §5 카운트(source-clean 21 → 콘텐츠 clean 26),
   설비-9 리스크 라벨(source-clean → needs-cleanup) 정정. (별도 승인 시)
3. **needs-cleanup 3항** — 기기-9·설비-9·설비-18의 손상 보기를 source PDF에서
   재-OCR. 정답 보기 무결성 우선 확인(closeout의 answer-locked 패턴 준용).
4. **statute-safe 트랙** — 설비-5/6을 closeout의 statute-safe 트랙(미설계)에
   합류. 트랙 착수 시 외부 출처 또는 v3.2 KEC 정합성 재검토 선행.
5. **DQ 트랙 finding 등재** — F1~F6 + q_type 오라벨 + F8을 DQ 트랙 작업
   목록으로 명시. tag 버킷 오염은 verify-agent Catch 후보로 별도 기록(자동 등재 안 함).
6. **검색 방법 보강** — 후속 trap-map 검색 시 OCR 검출기에 헤더 잔류물
   (`D-60`, `NN년도 N회`, 페이지 번호) 검사 추가 (R3).

다음 단계 우선순위: study-set-ready 26항이 가장 큰 즉시-가용 풀. needs-cleanup
3항은 source 재-OCR 후 합류. statute-safe 2항·DQ finding은 별 트랙.

## Not done in this step

- `app/data/questions.json` / `questions.v2.json` 미수정.
- solution / steps 미적용. answer / choices / text 미수정.
- dry-run 산출물 문서 미정정 (정정은 별도 승인 — 본 리뷰는 정정 사항 기록만).
- 설비-9 main 후보 실제 교체 미수행 (권고만).
- needs-cleanup 3항 source 재-OCR 미수행.
- verify-agent Catch 미등재 (별건).
- commit / push 없음. 유료 API 미호출. local server 미실행.

## Status

- dry-run 결과 리뷰 완료. A등급 31항 추출·F0·statute 판단은 검증 통과.
- 발견 6건(R1~R6): R1(설비-9 정답 보기 소실, dry-run 오분류) 중대,
  R2(§5 카운트 재현 불가)·R3(검출기 헤더 검사 누락) 경미.
- 정정된 main 후보 상태: 콘텐츠 clean 26 / needs-cleanup 3 / 부재 2.
- 4버킷 분류: study-set-ready 26 / needs-cleanup-before-study-set 3 /
  statute-safe-defer 2 / DQ-defer 0.
- 권고 6건 — 설비-9 main 교체, dry-run §5/설비-9 라벨 정정, needs-cleanup 재-OCR,
  statute-safe·DQ 트랙 라우팅, 검색 검출기 보강.
- 모든 정정·교체·등재는 별도 승인 대기 — 본 리뷰는 검증·분류·권고까지만.
