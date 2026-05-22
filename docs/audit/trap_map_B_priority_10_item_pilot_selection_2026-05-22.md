# Trap-Map B-Priority — 10항 Pilot 선별 (2026-05-22)

A-priority 26항 학습 패키지 closeout(`7ae4c92`) 이후, B등급 함정 항목으로
A-priority 방식이 확장 가능한지 **작은 단위로 검증**하기 위한 pilot 후보 선별 문서다.

이번 단계는 **선별/검증 설계까지만** — 학습 로그·day plan은 작성하지 않는다.
app/data 미수정. solution/steps 미적용. answer/choices/text 미수정. 유료 API
미호출. local server 미실행.

- 참조: A-priority closeout / study-set v2.1 final / 26항 day plan /
  v3.2 corrected actionable trap-map(`docs/audit/input/전기기사_6과목_라벨링_v3.2_corrected_actionable_20260522.md`)
- representative-ready 판정 근거: `app/data/questions.json` read-only 검색

---

## 1. 최종 결론

- v3.2 ★4~5 함정 **B등급 25항**(기기 10 / 설비 11 / 전력 3 / 회로 1)을 검토.
- **include 정확히 10항** 확정 — B-priority pilot 대상.
- **reserve 5항** — include 다음 순번, 검증 보강 후 승격 가능.
- **defer 10항** — statute-risk 또는 대표 기출 representative mapping 미완.
- A-priority deferred `2001_3회_43`은 representative-ready 아님 → **defer 유지**.
- pilot 규모: include 10항 = 10문제 (partial+sub 0 — pilot을 lean하게 유지).

---

## 2. B등급 25항 확인 (v3.2 라벨 직접 추출)

| 과목 | B항목 |
|---|---|
| 전기기기 (10) | 4 동기기 %Z / 7 변압기 %강하 / 17 권수비·전압비 / 18 등가회로 / 19 유도전압 조정기 / 20 회전 변류기 / 23 유도전동기 속도제어 / 25 동기전동기 V곡선 / 26 변압기 결선 / 28 단권변압기 |
| 전기설비 (11) | 7 제3종 접지공사 / 8 특별 제3종 접지공사 / 10 수도관·철골 접지극 / 12 전로 절연·절연저항 / 13 가공전선 이격거리 / 14 병가 / 21 발전기·변압기 보호장치 / 23 금속관공사 / 27 가공전선 높이 / 29 접지공사 생략 예외 / 30 가공지선·가공공동지선 |
| 전력공학 (3) | 18 차단기 종류(소호매질) / 22 연가 / 25 보호계전기 기능별 분류 |
| 회로이론 (1) | 20 실효값과 평균값 |

설비-7·8(제3종·특별 제3종 접지공사)은 KEC(2021)에서 폐지된 종별 접지 체계 —
A-priority 설비-5·6(제1·2종)과 동일한 statute-risk. 검토 시작부터 statute-defer 대상.

---

## 3. `2001_3회_43` 처리 방침

- A-priority answer-selection pedagogy 트랙의 deferred 항목 (closeout R1).
- 정답 ②는 source-verified이나 보기 [2] 오류 메커니즘이 repo 내부 source로 확인
  불가 — 외부 전기기기 교재 필요.
- B-pilot 후보 검토: `2001_3회_43`(정류자형 주파수 변환기)은 questions.json
  검색에서 기기-20(회전 변류기) 인접 영역에 등장하나, **대표 보기 함정을 검증할
  source가 없어 representative-ready가 아니다.**
- → **defer 유지.** 억지로 include하지 않는다. 외부 전기기기 교재 확보 시 단독
  처리(closeout R1 방침 그대로).

---

## 4. 선별 표 (B등급 25항 + 2001_3회_43)

trap type: S/C 정상상태↔에너지 변환 / S/F 정적 규칙↔고장·보호 / S/D 정적 공식↔
시변 신호. representative-ready: yes(대표 후보 on-topic·clean 식별) / medium
(clean 후보 있으나 검색 상위 off-topic — targeted pick 필요) / no(대표 부재).

### 4.1 include — 10항

| ID | 주제 | trap | 왜 B-pilot 적합 | 대표 기출 후보 | source-clean | repr-ready | risk/blocker | 포함 |
|---|---|---|---|---|---|---|---|---|
| 기기-17 | 변압기 권수비·전압비 | S/C ★5 | 권수비가 전압만 아니라 전류·임피던스도 변환 — 명확한 보기 함정 | `2020_1회_52` | clean 64건 | yes | — | include |
| 기기-18 | 변압기 등가회로 | S/C ★5 | 1차/2차 환산 혼동 함정, 시험 단골 | `2010_2회_47` | clean 24건 | yes | 대표 후보는 시험 파라미터 측, 환산 혼동 함정과 인접 | include |
| 기기-19 | 유도전압 조정기 | S/C ★4 | 위상 조정 ↔ 권수비 조정 혼동, 함정 뚜렷 | `2004_2회_56` | clean 26건 | yes | — | include |
| 기기-25 | 동기전동기 V곡선 | S/C ★4 | 계자전류↔무효분 관계, 출력 불변 함정 명확 | `2014_2회_50` | clean 3건 | yes | clean 풀 작음(3건) | include |
| 기기-28 | 단권변압기 | S/C ★4 | 자기용량/부하용량 혼동, 계산형 대표 | `2013_3회_59` | clean 12건 | yes | 계산형 — 보기 함정 대신 계산에 원리 내재 | include |
| 설비-13 | 가공전선 이격거리 | S/F ★5 | 시설별 이격거리 차등, 함정 분명 | `2010_2회_83` | clean 103건 | yes | — | include |
| 설비-14 | 병가 | S/F ★5 | 상하 배치·이격 조건, 함정 뚜렷 | `2009_1회_92` | clean 9건 | yes | 후보 subject='전력공학' 오라벨(내용 병가) | include |
| 설비-30 | 가공지선·가공공동지선 | S/F ★4 | 가공지선 용도(낙뢰 차폐 vs 전송) 함정 명확 | `2006_1회_29` | clean 11건 | yes | 후보 subject='전력공학' 오라벨 | include |
| 전력-25 | 보호계전기 기능별 분류 | S/F ★4 | 사고유형↔계전기 매핑, 함정 분명 | `2019_3회_31` | clean 55건 | yes | A 전력-26·기기-29와 보호계전기 주제 인접(항목 ID 중복 아님) | include |
| 회로-20 | 실효값과 평균값 | S/D ★4 | 실효값↔평균값 혼동, 비정현파 함정 — 유일한 회로 B | `2008_2회_75` | clean 44건 | yes | 후보 subject='제어공학' 오라벨(내용 회로이론) | include |

### 4.2 reserve — 5항

| ID | 주제 | trap | 대표 기출 후보 | source-clean | repr-ready | risk/blocker | 포함 |
|---|---|---|---|---|---|---|---|
| 기기-4 | 동기기 %Z | S/C ★5 | `2008_1회_46` | clean 12건 | medium | 후보는 동기임피던스 포화 측 — %Z↔효율 함정과 인접, targeted pick 권장 | reserve |
| 기기-23 | 유도전동기 속도제어 | S/C ★4 | (재선정 필요) | clean 21건 | medium | 검색 상위 `2007_2회_41`은 2차여자 제어 — A 기기-13 main과 주제 근접. 속도제어 종합 문항 별도 발굴 필요 | reserve |
| 설비-10 | 수도관·철골 접지극 | S/F ★5 | `2004_2회_82` | clean 1건 | medium | clean 후보 단 1건 — alt 부재, 풀 빈약 | reserve |
| 설비-21 | 발전기·변압기 보호장치 | S/F ★4 | `2021_2회_84` | clean 18건 | medium | A 기기-29·전력-26과 보호 주제 인접 — 시설 기준 각도로 차별화 가능하나 중복 주의 | reserve |
| 전력-18 | 차단기 종류(소호매질) | S/F ★4 | (tag 버킷서 재선정) | clean 101건(키워드) | medium | '소호' 키워드가 소호리액터 접지를 다수 흡입 — tag '소호매질에 따른 차단기' 버킷서 targeted pick 필요 | reserve |

### 4.3 defer — 10항 (+ 2001_3회_43)

| ID | 주제 | defer 사유 | 분류 |
|---|---|---|---|
| 설비-7 | 제3종 접지공사 | KEC(2021) 폐지 종별 접지 — statute-risk (A 설비-5·6과 동일) | defer |
| 설비-8 | 특별 제3종 접지공사 | KEC 폐지 종별 접지 — statute-risk | defer |
| 기기-20 | 회전 변류기 | clean 후보가 전부 정류자형 주파수변환기(다른 기기) — 회전 변류기 전용 대표 부재 | defer |
| 전력-22 | 연가 | 연가 목적·횟수·효과를 묻는 clean 문항 부재(검색 1건이 작용 인덕턴스 계산) | defer |
| 기기-7 | 변압기 %저항·리액턴스·임피던스 강하 | 검색 상위가 off-topic, %z=√(p²+q²) 벡터합 함정 문항 미식별 — representative mapping 미완 | defer |
| 기기-26 | 변압기 결선 | '결선' 키워드 과대 — 변압기 Y/Δ/V결선 전용 대표 미식별, mapping 미완 | defer |
| 설비-12 | 전로 절연·절연저항 | 검색 상위가 대지전압·애자 절연저항 — 전로 절연저항 기준 문항 미식별, mapping 미완 | defer |
| 설비-23 | 금속관공사 | 검색에 가요전선관·합성수지관 혼재 — 금속관 전용 대표 미식별, mapping 미완 | defer |
| 설비-27 | 가공전선 높이 | '가공전선' 키워드 과대(189건) — 높이 전용 대표 미식별, mapping 미완 | defer |
| 설비-29 | 접지공사 생략 예외 | '접지' 키워드 과대 — 생략 예외 전용 대표 미식별, mapping 미완 | defer |
| `2001_3회_43` | 정류자형 주파수 변환기 | 보기 [2] 오류 메커니즘 검증에 외부 전기기기 교재 필요 (closeout R1) — representative-ready 아님 | defer (별도 항목) |

defer 분류 요약: statute-risk 2(설비-7·8) / 대표 부재 2(기기-20·전력-22) /
representative mapping 미완 6(기기-7·26, 설비-12·23·27·29) + `2001_3회_43`
(외부 교재 필요, 별도).

---

## 5. include 10항 확정

기기-17, 기기-18, 기기-19, 기기-25, 기기-28, 설비-13, 설비-14, 설비-30,
전력-25, 회로-20.

- 과목 분포: 전기기기 5 / 전기설비 3 / 전력공학 1 / 회로이론 1 — 4개 과목 모두 포함.
- trap type 분포: S/C 5 / S/F 4 / S/D 1.
- 별점: ★5 4항 + ★4 6항.
- partial+sub: **0항** — B-pilot은 main 10문제로 lean하게 유지.
- A-priority 26항과 항목 ID 중복 0 (B등급은 A와 정의상 배타적).

## 6. reserve 5항

기기-4, 기기-23, 설비-10, 설비-21, 전력-18.
- include 다음 순번. medium readiness — 대표 기출 targeted 재선정/검증 보강 후
  pilot 승격 가능. include 항목에 결격 발생 시 대체 투입.

---

## 7. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| include 정확히 10항 | ✅ 기기 5 + 설비 3 + 전력 1 + 회로 1 = 10 |
| reserve 3~5항 | ✅ 5항 (기기-4·23, 설비-10·21, 전력-18) |
| defer 사유 명확 | ✅ statute 2 / 대표 부재 2 / mapping 미완 6 + 2001_3회_43 별도 |
| 2001_3회_43 처리 방침 | ✅ defer 유지 — representative-ready 아님(외부 교재 필요) |
| A-priority 26항 중복 없음 | ✅ include·reserve 전부 B등급 — A의 항목 ID와 배타적 |
| 범위 외 항목 미혼입 | ✅ 기기-31·32(미존재) 등 미포함, B등급 25항 + 2001_3회_43만 검토 |
| source-clean / representative-ready 상태 명시 | ✅ 전 항목 표에 clean 후보 건수·repr-ready 등급 기재 |
| 과목/유형 편중 점검 | ✅ include 4개 과목 분산(기기 50%는 B-pool 기기 비중 반영), trap type S/C 5·S/F 4·S/D 1 — 단일 유형 과반 없음 |
| partial+sub 제한 | ✅ include 0항 — pilot 10문제로 제한, 과대화 방지 |
| 합계 검증 | ✅ include 10 + reserve 5 + defer 10 = 25 (B등급 전수), + 2001_3회_43 별도 |
| 금지사항 준수 | ✅ app/data·solution·answer/choices/text 미수정 / API·server 미실행 / 학습 로그·day plan 미작성 / amend·rebase·reset 없음 |

### 알려진 한계

- reserve·defer의 representative mapping 미완 항목(기기-7·26, 설비-12·23·27·29,
  전력-18 등)은 A-priority dryrun 같은 **대표 기출 mapping 단계**를 거치지 않았다 —
  검색은 키워드·tag 기반 readiness 추정이며, pilot 착수 시 targeted dryrun 필요.
- include 후보의 subject 오라벨(설비-14·30, 회로-20)·tag 오염은 A-priority에서
  확인된 corpus-wide DQ — 학습 콘텐츠에는 무관, DQ 트랙 별도 정정 대상.

---

## 8. 다음 단계 (제안만)

include 10항으로 B-priority pilot 착수 시:
1. include 10항 대표 기출 targeted dryrun — source-clean·representative 검증
   (A-priority representative dryrun 방식 준용).
2. A-priority 방식(study-set → day plan → inline trap cues → 6칸 학습 로그)을
   10항 소규모로 적용해 B등급 확장 가능성 검증.
3. reserve 5항은 include 검증 중 결격 발생 시 대체 투입.

(이 문서는 선별/검증 설계까지 — 학습 로그·day plan은 별도 트랙·별도 승인.)

---

## Status

- trap-map B-priority 10항 pilot 선별 완료.
- B등급 25항 검토 → include 10 / reserve 5 / defer 10 + `2001_3회_43` defer(별도).
- include 10항: 기기-17·18·19·25·28, 설비-13·14·30, 전력-25, 회로-20 — 4개 과목
  분산, trap type S/C 5·S/F 4·S/D 1, partial+sub 0.
- `2001_3회_43`은 외부 교재 필요로 defer 유지.
- 다음 작업자는 include 10항 대표 기출 targeted dryrun으로 B-pilot 착수 가능.
- 이 문서는 선별/검증 설계 문서다. 학습 로그·day plan 미작성.
