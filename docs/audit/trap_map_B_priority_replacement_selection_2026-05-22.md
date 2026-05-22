# Trap-Map B-Priority — needs_replacement 5항 교체 후보 재선정 (2026-05-22)

B-priority 10항 representative dryrun(`4a92294`)에서 needs_replacement 판정된 5항을
교체할 후보를 재선정한다. dryrun 결과 ready/ready_with_note 5/10으로 학습 패키지
진행이 불가했고, 본 문서는 교체 5항을 채워 proposed include 10항을 다시 구성한다.

이번 단계는 교체 후보 선정·근거 문서화만 — 학습 로그·day plan 미작성. app/data
미수정. questions.json 미수정. solution/steps 미적용. answer/choices/text 미수정.
유료 API 미호출. local server 미실행.

- 참조:
  - B-priority 10항 pilot selection (`docs/audit/trap_map_B_priority_10_item_pilot_selection_2026-05-22.md`)
  - B-priority representative dryrun (`docs/audit/trap_map_B_priority_10_item_representative_dryrun_2026-05-22.md`)
  - A-priority pilot learning package closeout (`docs/audit/trap_map_A_priority_pilot_learning_package_closeout_2026-05-22.md`)
  - v3.2 corrected actionable trap-map (`docs/audit/input/전기기사_6과목_라벨링_v3.2_corrected_actionable_20260522.md`)
- 교체 후보 검증 근거: `app/data/questions.json` read-only 전수 조회 (후보별 full
  text·choices·answer 직접 확인).

---

## 결론: proposed include 10항 = 유지 5 + 교체 5 (전 항목 representative-ready)

dryrun에서 살아남은 유지 5항에, reserve 5항을 대표 기출 검증을 거쳐 교체 5항으로
승격한다. 교체 5항은 모두 source-clean·정답 검증 통과 — relationship은 exact 1 +
adjacent 4. proposed include 10항 전부 ready/ready_with_note 도달.

dryrun에서 빠진 needs_replacement 5항(기기-19·25·28, 설비-30, 회로-20)은 본
pilot include에서 제외 — 대표 기출 재선정 보류 항목으로 남긴다(아래 §4).

reserve 풀(기기-4·23, 설비-10·21, 전력-18)은 본 교체로 **5항 전부 소진**. 향후
include 결격 발생 시 대체 투입 가능한 reserve는 없으며, defer 풀의 representative
mapping 미완 항목을 targeted dryrun 후 승격하는 경로만 남는다(아래 §5).

---

## 1. 유지 5항 (dryrun ready / ready_with_note)

dryrun(`4a92294`) 판정 그대로 유지 — 본 문서에서 재검증하지 않는다.

| ID | 주제 | trap | 대표 기출 | dryrun 판정 |
|---|---|---|---|---|
| 기기-17 | 변압기 권수비 | S/C ★5 | `2020_1회_52` | ready (exact) |
| 기기-18 | 변압기 등가회로 | S/C ★5 | `2010_2회_47` | ready_with_note (adjacent) |
| 설비-13 | 가공전선 이격거리 | S/F ★5 | `2010_2회_83` | ready (exact) |
| 설비-14 | 병가 | S/F ★5 | `2009_1회_92` | ready_with_note (adjacent) |
| 전력-25 | 보호계전기 기능별 분류 | S/F ★4 | `2019_3회_31` | ready_with_note (adjacent) |

---

## 2. 교체 5항 재선정 (reserve 5항 검증)

dryrun selection의 reserve 5항을 검토 대상으로 우선 검증했다. reserve 후보 중
OCR 손상으로 탈락한 항목은 같은 tag 내 clean 후보로 교체했다(아래 표 비고).

trap relationship: exact(v3.2 대표 보기 함정 직접 검증) / adjacent(같은 주제의
인접 하위 함정) / mismatch(어긋남). source-clean: questions.json choices 4지 전수
판독 가능 여부.

| ID | 주제 | trap | 대표 기출 | source-clean | 검증 포인트 | 관계 | 판정 |
|---|---|---|---|---|---|---|---|
| 기기-4 | 동기기 %Z | S/C ★5 | `2008_1회_46` | clean | 철심 포화 시 동기임피던스 거동(감소) | adjacent | ready_with_note |
| 기기-23 | 유도전동기 속도제어 | S/C ★4 | `2019_3회_52` | clean | 농형 전동기 적용 가능 속도제어법 식별(극수변환) | adjacent | ready_with_note |
| 설비-10 | 수도관·철골 접지극 | S/F ★5 | `2004_2회_82` | clean | 수도관 접지극 접속 위치 기준(분기점 5m 이내) | adjacent | ready_with_note |
| 설비-21 | 발전기·변압기 보호장치 | S/F ★4 | `2021_2회_84` | clean | 타냉식 변압기 냉각장치 고장 시 보호장치(경보장치) | adjacent | ready_with_note |
| 전력-18 | 차단기 종류(소호매질) | S/F ★4 | `2017_2회_36` | clean | 차단기-소호원리 매핑 오류 식별(VCB↔공기냉각) | exact | ready |

판정 집계: ready 1 / ready_with_note 4 / needs_replacement 0 / defer 0 (합 5).

### reserve 후보 중 OCR 손상 탈락 항목

| ID | selection이 제시한 후보 | 탈락 사유 | 채택한 clean 후보 |
|---|---|---|---|
| 기기-4 | `2011_2회_43` | choice [2]에 페이지 헤더("11년도 2회 / D-60 시리즈")가 보기로 혼입, 정답 [2]가 손상 보기를 가리킴 — source-clean FAIL | `2008_1회_46` |
| 설비-10 | `2006_2회_82` | choice [2]에 페이지 헤더("06년도 2회 / 2-173") 혼입, 정답 [2]가 손상 보기를 가리킴 — source-clean FAIL | `2004_2회_82` |
| 전력-18 | (selection은 후보 미지정, "tag 버킷서 재선정") | — | `2017_2회_36` (tag '소호매질에 따른 차단기' 51건 중 exact) |
| 기기-23 | (selection은 후보 미지정, "재선정 필요") | — | `2019_3회_52` |

기기-4·설비-10은 reserve 표의 후보가 dryrun과 같은 종류의 손상(보기에 무관 텍스트
혼입)을 갖고 있어 같은 tag 내 다른 clean 후보로 교체했다. 두 항목 모두 후보 풀이
빈약(기기-4 on-topic clean 소수, 설비-10 clean 후보 사실상 단건)하여 채택 후보가
trap 직접 검증이 아닌 adjacent에 그친다 — §6 한계 참조.

---

## 3. 항목별 상세 (교체 5항)

### 기기-4 동기기 %Z — `2008_1회_46`
- v3.2 trap: %Z를 기기 효율과 직접 연결하는 보기. (외울: %Z=(I·Z/V)×100 /
  이해: %Z 작을수록 단락전류 큼·전압변동 작음)
- 기출: "교류 발전기의 동기 임피던스는 철심이 포화하면 어떻게 되는가?" 정답 (3)
  감소한다. 철심 포화 → 자기저항 증가 → 자속·리액턴스 감소 → 동기임피던스 감소.
- 관계 **adjacent**: %Z(동기임피던스의 단위법 표현)와 같은 주제이나, v3.2 대표
  함정(%Z↔효율 연결, %Z↔단락전류 양면성)이 아닌 *포화 시 거동*을 검증.
- source-clean: choices 4지 전부 판독 가능. 정답 (3) 표준 거동과 정합.
- 판정 **ready_with_note**. note: "이 기출은 %Z의 포화 거동을 검증, v3.2 효율 연결
  함정은 별도" — 학습 시 차이 명시.

### 기기-23 유도전동기 속도제어 — `2019_3회_52`
- v3.2 trap: 2차 저항제어가 효율을 높인다는 보기. (이해: 각 제어법이
  N=(120f/P)(1-s)에서 어느 변수를 건드리는지 다름)
- 기출: "농형 유도전동기에 주로 사용되는 속도제어법은?" 정답 (1) 극수 변환법.
  농형은 회전자 권선 외부 인출이 없어 2차 저항제어(3)·2차 여자제어(4) 불가,
  극수 변환법이 적용 가능.
- 관계 **adjacent**: 속도제어법을 *전동기 형식별 적용 가능성*으로 식별 — v3.2의
  *2차 저항제어 효율* 함정과는 다른 축이나, 같은 속도제어 주제의 인접 함정.
- source-clean: choices 4지 전부 판독 가능. 정답 (1) 정합. (`2009_2회_57`은
  같은 문항이나 choice [4] "중속 제어법" OCR 손상 — `2019_3회_52` 채택.)
- 판정 **ready_with_note**. note: 제어법-형식 매핑을 검증, v3.2 효율 함정은 별도.

### 설비-10 수도관·철골 접지극 — `2004_2회_82`
- v3.2 trap: 모든 수도관을 접지극으로 쓸 수 있다는 보기. (외울: 수도관 3Ω 이하 /
  이해: 충분히 낮은 저항이면 별도 접지극 없이 보호 가능)
- 기출: "대지 전기저항 3Ω 금속제 수도관로를 접지극으로 사용할 때, 접지선과
  수도관로의 접속은 안지름 75mm 이상 수도관(또는 분기 75mm 미만 수도관)
  분기점으로부터 몇 m 이내에서 하여야 하는가?" 정답 (2) 5.
- 관계 **adjacent**: 수도관 접지극 시설의 *접속 위치 수치 기준*을 검증 — v3.2의
  *사용 가능 조건* 함정은 직접 검증 안 됨. 같은 수도관 접지극 주제의 인접 함정.
- source-clean: choices 4지(3/5/8/10) 전부 판독 가능. 정답 (2) 판단기준·KEC
  접속 거리 기준과 정합.
- 판정 **ready_with_note**. note: 접속 거리 수치를 검증, v3.2 사용 조건 함정은
  별도. 후보 풀이 가장 빈약한 항목 — alt 사실상 부재(§6).

### 설비-21 발전기·변압기 보호장치 — `2021_2회_84`
- v3.2 trap: 발전기 보호를 단순 과전류만으로 한다는 보기. (외울: 과전류·과전압·
  내부고장·냉각이상 차단 조건)
- 기출: "타냉식 변압기 냉각장치 고장 보호장치는?" 정답 (1) 경보장치. KEC
  발전기·변압기 보호장치 시설 — 타냉식 변압기는 냉각장치 고장 시 이를 경보하는
  장치 시설.
- 관계 **adjacent**: 보호 조건 중 *냉각이상* 항목을 검증 — v3.2의 *과전류 단일*
  함정과는 다른 축이나, 같은 발·변압기 보호장치 주제의 인접 함정.
- source-clean: choices 4지 전부 판독 가능. 정답 (1) KEC 시설 기준과 정합.
- 판정 **ready_with_note**. note 2건:
  1. 차이 명시 — 냉각이상 보호를 검증, v3.2 과전류 단일 함정은 별도.
  2. 후보 metadata 오라벨(subject='전기기기', tag='변압기') — 콘텐츠는 발·변압기
     보호장치 시설로 설비-21에 정합, DQ 트랙 정정 대상. A 전력-26(발·변압기 보호
     계전기)·A 기기-29(변압기 내부고장 보호)와 보호 주제 인접하나, 본 후보는
     *시설 기준 보호장치* 각도로 계전기 종류 문항과 차별 — 항목 ID 중복 0.

### 전력-18 차단기 종류(소호매질) — `2017_2회_36`
- v3.2 trap: 가스차단기와 진공차단기를 같은 원리로 설명하는 보기. (이해: 매질의
  절연회복 속도·아크 냉각 능력이 차단 성능 결정)
- 기출: "차단기와 아크 소호원리가 바르지 않은 것은?" 정답 (2) "VCB: 공기 중
  냉각에 의한 아크 소호". VCB(진공차단기)는 진공의 높은 절연내력·아크 확산으로
  소호 — 공기 냉각 원리가 아니다. 보기 (1)OCB·(3)ABB·(4)MBB는 매질-원리 정합.
- 관계 **exact**: 차단기 종류↔소호원리 매핑 오류를 직접 검증 — v3.2 대표 함정
  (매질/원리 혼동)과 정확히 일치.
- source-clean: choices 4지 전부 간결·판독 가능. 정답 (2) 표준 소호원리와 정합.
- 판정 **ready**. (tag '소호매질에 따른 차단기' 51건 중 `2010_1회_28`도 동일
  유형이나 choices에 OCR 잔류 garble — clean도가 높은 `2017_2회_36` 채택.)

---

## 4. dryrun needs_replacement 5항 처리 (본 pilot 제외)

dryrun에서 needs_replacement 판정된 5항은 본 B-pilot include에서 제외한다.
대표 기출 재선정 보류 항목으로 남기며, clean·정답 검증된 대표 기출 확보 시
별도 트랙으로 재검토 가능.

| ID | 주제 | dryrun 탈락 사유 | 처리 |
|---|---|---|---|
| 기기-19 | 유도전압 조정기 | trap mismatch (단락권선 역할은 핵심 함정 아님) | 재선정 보류 |
| 기기-25 | 동기전동기 V곡선 | 정답 표기와 표준 정의 충돌 | 재선정 보류 |
| 기기-28 | 단권변압기 | source-clean FAIL (보기가 문제와 무관) | 재선정 보류 |
| 설비-30 | 가공지선 | source-clean FAIL (한글 OCR 심각 손상) | 재선정 보류 |
| 회로-20 | 실효값과 평균값 | 정답 표기와 표준 계산값 충돌 | 재선정 보류 |

회로-20은 v3.2 B등급 *유일한 회로이론 항목*이다 — 본 교체로 회로-20이 빠지면서
B-pilot의 회로이론 커버리지가 0이 된다. v3.2 회로이론 B등급에 다른 항목이 없어
(회로-27은 C등급) B등급 범위 내 보충 불가 — §6 한계 참조.

`2001_3회_43`은 본 작업 대상 아님. closeout R1 / selection §3대로 **defer 유지**
(외부 전기기기 교재 필요, representative-ready 아님).

---

## 5. proposed include 10항 확정

기기-17, 기기-18, 기기-4, 기기-23, 설비-13, 설비-14, 설비-10, 설비-21,
전력-25, 전력-18.

| 분류 | 과목 분포 | trap type | 별점 |
|---|---|---|---|
| 유지 5 | 기기 2 / 설비 2 / 전력 1 | S/C 2 / S/F 3 | ★5 4 / ★4 1 |
| 교체 5 | 기기 2 / 설비 2 / 전력 1 | S/C 2 / S/F 3 | ★5 2 / ★4 3 |
| **합 10** | **기기 4 / 설비 4 / 전력 2 / 회로 0** | **S/C 4 / S/F 6 / S/D 0** | **★5 6 / ★4 4** |

- partial+sub: 0항 — B-pilot은 main 10문제로 lean하게 유지(selection §5 방침).
- A-priority 26항 항목 ID 중복: 0 — proposed include 10항 전부 B등급, A와 정의상
  배타적. (설비-21·전력-25는 A 전력-26/기기-29와 보호 주제 인접하나 ID 중복 아님.)
- reserve: 0항 — reserve 5항 전부 본 교체로 소진. include 결격 시 대체 투입
  후보 없음. 향후 보충은 defer 풀(기기-7·26, 설비-12·23·27·29)의 representative
  mapping을 targeted dryrun으로 완료한 뒤에만 가능.

---

## 6. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| proposed include 정확히 10항 | ✅ 기기 4 + 설비 4 + 전력 2 + 회로 0 = 10 |
| 유지 5항 + 교체 5항 구성 | ✅ 유지 기기-17·18, 설비-13·14, 전력-25 / 교체 기기-4·23, 설비-10·21, 전력-18 |
| 교체 5항 전부 representative-ready | ✅ ready 1(전력-18) + ready_with_note 4(기기-4·23, 설비-10·21) |
| 교체 5항 source-clean | ✅ 5항 전부 choices 4지 판독 가능 — questions.json 직접 확인 |
| mismatch·정답 충돌·심한 OCR 손상 제외 | ✅ 교체 5항 모두 정답 검증 통과·exact 또는 adjacent. 손상 후보(2011_2회_43, 2006_2회_82, 2010_1회_28)는 채택 제외 |
| reserve 우선 검토 | ✅ reserve 5항(기기-4·23, 설비-10·21, 전력-18) 전수 검토 후 채택. B등급 추가 탐색 불필요(reserve로 5항 충족) |
| A-priority 26항 중복 없음 | ✅ proposed include 10항 전부 B등급 — A 항목 ID와 배타적 |
| 2001_3회_43 처리 | ✅ defer 유지 — 본 작업 대상 아님, 외부 교재 필요 |
| 금지사항 준수 | ✅ app/data·questions.json·solution·answer/choices/text 미수정 / API·server 미실행 / 학습 로그·day plan 미작성 / amend·rebase·reset 없음 |

### 알려진 한계

1. **교체 5항 중 4항이 adjacent** — exact는 전력-18 1항뿐. 기기-4·23, 설비-10·21은
   v3.2 대표 보기 함정을 직접 검증하지 않고 같은 주제의 인접 하위 함정을 검증한다.
   유지 5항도 dryrun에서 ready 2 + ready_with_note 3 — adjacent 비중은 유지·교체가
   유사하다. 학습 콘텐츠 활용 시 "이 기출이 검증하는 것 ≠ v3.2 대표 함정" 차이를
   각 항목 note대로 명시해야 한다.
2. **회로이론 커버리지 0** — 회로-20(B등급 유일 회로 항목)이 needs_replacement로
   빠지면서 B-pilot에 회로 과목이 없다. v3.2 B등급에 다른 회로 항목이 없어 B등급
   범위 내 보충 불가. B-pilot은 기기·설비·전력 3과목 pilot로 한정된다.
3. **trap type S/F 6/10 (60%)** — S/D 항목(회로-20)이 빠지면서 S/F가 과반이다.
   v3.2 B등급은 설비 11·전력 3이 전부 S/F라 B-pool 자체가 S/F 편중 — pilot 구성의
   한계가 아니라 모집단 특성 반영.
4. **reserve 소진** — reserve 5항을 전부 include로 승격해 대체 투입 후보가 없다.
   include 항목 결격 발생 시 defer 풀의 mapping 미완 항목을 targeted dryrun으로
   먼저 검증해야 투입 가능하다.
5. **설비-10 후보 풀 빈약** — clean 후보가 사실상 `2004_2회_82` 단건. 이 후보가
   이후 결격으로 드러나면 설비-10은 즉시 대체 불가 — 교체 5항 중 최약 항목.

---

## 7. 다음 단계 (제안만)

1. proposed include 10항으로 B-pilot representative dryrun을 1회 더 거쳐 교체
   5항의 ready/ready_with_note를 재확인(본 문서는 후보 선정·근거까지).
2. 10항 전부 ready/ready_with_note 확정 시 A-priority 방식(study-set → day plan →
   inline trap cues → 학습 로그)을 B등급 10항 소규모로 적용.
3. needs_replacement 5항(기기-19·25·28, 설비-30, 회로-20)은 clean·정답 검증된
   대표 기출 확보 시 별도 트랙으로 재검토 — 본 pilot에 강제 편입하지 않는다.

(이 문서는 교체 후보 선정·근거 문서화까지 — 학습 로그·day plan은 별도 트랙·별도 승인.)

---

## Status

- B-priority needs_replacement 5항 교체 후보 재선정 완료.
- proposed include 10항 = 유지 5(기기-17·18, 설비-13·14, 전력-25) + 교체 5
  (기기-4 `2008_1회_46` / 기기-23 `2019_3회_52` / 설비-10 `2004_2회_82` /
  설비-21 `2021_2회_84` / 전력-18 `2017_2회_36`).
- 교체 5항 판정: ready 1(전력-18, exact) + ready_with_note 4(adjacent) — 전부
  source-clean·정답 검증 통과.
- reserve 5항 전부 소진. needs_replacement 5항은 재선정 보류. `2001_3회_43`
  defer 유지.
- 과목 분포 기기 4 / 설비 4 / 전력 2 / 회로 0 — 회로 커버리지 0(B등급 한계).
- 이 문서는 교체 후보 선정 문서다. 학습 로그·day plan 미작성.
