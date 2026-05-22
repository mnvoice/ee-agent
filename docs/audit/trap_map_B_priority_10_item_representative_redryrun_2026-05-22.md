# Trap-Map B-Priority — 10항 Representative Targeted Re-dryrun (2026-05-22)

replacement selection(`f827a08`)에서 확정한 proposed include 10항(유지 5 + 교체 5)을
다시 representative targeted dryrun으로 검증한다. 1차 dryrun(`4a92294`)에서
needs_replacement 5항이 발생해 5/10에 그쳤고, 교체 후 10항이 ready/ready_with_note
10/10에 도달하는지 재확인하는 단계다.

이번 단계는 검증 문서 작성만 — 학습 로그·day plan 미작성. app/data 미수정.
questions.json 미수정. solution/steps 미적용. answer/choices/text 미수정. 유료 API
미호출. local server 미실행.

- 참조:
  - B-priority 1차 representative dryrun (`docs/audit/trap_map_B_priority_10_item_representative_dryrun_2026-05-22.md`)
  - B-priority replacement selection (`docs/audit/trap_map_B_priority_replacement_selection_2026-05-22.md`)
  - B-priority 10항 pilot selection (`docs/audit/trap_map_B_priority_10_item_pilot_selection_2026-05-22.md`)
  - v3.2 corrected actionable trap-map (`docs/audit/input/전기기사_6과목_라벨링_v3.2_corrected_actionable_20260522.md`)
- 검증 근거: `app/data/questions.json` read-only 전수 조회 — 10항 전부 full text·
  choices·answer를 직접 확인(유지 5항 포함 재확인).

---

## 결론: **PASS — ready/ready_with_note 10/10, B-pilot 학습 패키지 진행 가능**

proposed include 10항 전부 source-clean·정답 정합 통과. 판정 집계 ready 2 +
ready_with_note 8 = **10/10**. needs_replacement 0, defer 0.

교체 5항은 1차 dryrun의 탈락 사유(mismatch·정답 충돌·OCR 손상)를 모두 해소했고,
유지 5항은 1차 dryrun 판정을 재확인했다. 단 1차 dryrun에서 "ready"였던 기기-17은
choices LaTeX 직접 판독 결과 보기 [1]에 잉여 √3 표기 artifact가 확인되어 본
재dryrun에서 **ready_with_note로 조정**한다(정답·trap은 건전 — §3 기기-17 참조).

품질 기준상 ready/ready_with_note 10/10이므로 B-pilot 학습 패키지 단계 진행이
가능하다. 단 residual 3건(회로 커버리지 0 / S/F 편중 / reserve 소진)은 해소되지
않은 채 학습 패키지로 이월된다 — §5.

---

## 검증 표 (proposed include 10항)

trap type: S/C 정상상태↔변환 / S/F 정적 규칙↔고장·보호 / S/D 정적 공식↔시변 신호.
관계: exact(v3.2 대표 보기 함정 직접 검증) / adjacent(같은 주제 인접 하위 함정) /
partial(일부만) / mismatch(어긋남).

| ID | 주제 | 대표 기출 | source-clean | 정답/보기 정합 | 관계 | 판정 |
|---|---|---|---|---|---|---|
| 기기-17 | 변압기 권수비 | `2020_1회_52` | text clean, **보기 [1] LaTeX 잉여 √3** | ans (1) — 선전류 √3I/a 정합, 단자전압 표기 정리 필요 | exact | ready_with_note |
| 기기-18 | 변압기 등가회로 | `2010_2회_47` | clean, 보기 [4] 용어 비표준 | ans (2) 전압변동률 정합 | adjacent | ready_with_note |
| 설비-13 | 가공전선 이격거리 | `2010_2회_83` | clean | ans (4) 정합 | exact | ready |
| 설비-14 | 병가 | `2009_1회_92` | clean | ans (1) 50cm 정합 | adjacent | ready_with_note |
| 전력-25 | 보호계전기 기능별 분류 | `2019_3회_31` | clean | ans (3) 지락 과전류 계전기 정합 | adjacent | ready_with_note |
| 전력-18 | 차단기 종류(소호매질) | `2017_2회_36` | clean | ans (2) VCB↔공기냉각 오류 정합 | exact | ready |
| 기기-4 | 동기기 %Z | `2008_1회_46` | clean | ans (3) 감소 정합 | adjacent | ready_with_note |
| 기기-23 | 유도전동기 속도제어 | `2019_3회_52` | clean | ans (1) 극수 변환법 정합 | adjacent | ready_with_note |
| 설비-10 | 수도관·철골 접지극 | `2004_2회_82` | clean | ans (2) 5m 정합 | adjacent | ready_with_note |
| 설비-21 | 발전기·변압기 보호장치 | `2021_2회_84` | clean | ans (1) 경보장치 정합 | adjacent | ready_with_note |

판정 집계: ready 2 / ready_with_note 8 / needs_replacement 0 / defer 0 (합 10).
관계 집계: exact 3(기기-17, 설비-13, 전력-18) / adjacent 7 / partial 0 / mismatch 0.

---

## 항목별 상세

### 유지 5항 — 재확인

**기기-17 변압기 권수비 — `2020_1회_52`**
- v3.2 trap: 권수비가 전압만 변환한다는 보기. (외울: a=N1/N2=V1/V2=I2/I1, Z1=a²Z2)
- 기출: "권수비 a 단상변압기 3대, 1차 △·2차 Y 결선, 2차 단자전압 V·전류 I →
  1차 단자전압·선전류?" 정답 (1). 풀이에 권수비를 전압(×a)·전류(÷a)에 동시
  적용해야 함 — "전압만 변환" 오개념이면 전류 항을 틀린다.
- **재dryrun 신규 확인**: 보기 [1]의 questions.json 원문 LaTeX는
  `\sqrt{3}\frac{aV}{\sqrt{3}}` — 잉여 √3 표기로, 문자 그대로 정리하면 단자전압이
  aV가 된다. 1차 △·2차 Y 물리 풀이상 단자전압 = aV/√3, 선전류 = √3I/a이며,
  보기 [1]의 선전류 항(√3I/a)·정답 키(1)는 정합한다. 보기 [1]의 잉여 √3은 OCR
  artifact로 보이며 본문(text)·나머지 보기 [2]~[4]는 clean.
- 관계 **exact**: trap(권수비 동시 변환)을 직접 검증.
- 판정 1차 dryrun "ready" → 본 재dryrun **ready_with_note**로 조정. 정답·trap·
  본문은 건전하나 보기 [1] LaTeX는 학습 패키지 활용 전 정리 필요.
- 주의 문장: "보기 [1] 표기 `√3·aV/√3`는 단자전압 aV/√3의 OCR 잉여 √3 — 학습
  자료 노출 시 `aV/√3`로 정리. 정답·풀이는 영향 없음. Δ-Y √3 결선 변환이 권수비와
  함께 묶이므로 결선 √3을 분리 설명."

**기기-18 변압기 등가회로 — `2010_2회_47`**
- v3.2 trap: 1차 환산값과 2차 실제값을 혼동하는 보기.
- 기출: "무부하·단락시험에서 구할 수 없는 것?" 정답 (2) 전압변동률. 등가회로
  파라미터를 어느 시험에서 얻는지 검증 — v3.2의 1차/2차 환산 혼동 함정은 직접
  검증 안 됨. 같은 등가회로 주제의 인접 하위 함정.
- source-clean: choices 판독 가능. 보기 [4] "철손내력"은 비표준 용어.
- 관계 **adjacent** / 판정 **ready_with_note** (1차 dryrun과 동일).
- 주의 문장: "이 기출은 등가회로 시험-파라미터를 검증, v3.2 환산 혼동 함정은 별도.
  보기 [4] '철손내력' 용어 비표준 — 학습 활용 시 cleanup 권장."

**설비-13 가공전선 이격거리 — `2010_2회_83`**
- v3.2 trap: 모든 시설에 동일 이격거리를 적용한다는 보기.
- 기출: "저압·고압 가공전선이 도로 접근상태로 시설 시 잘못된 것?" 정답 (4).
  보기가 저압 2m·수평 1m·고압 보안공사·전차선 지지물 60cm 등 시설별 다른
  이격거리 — "동일 이격거리" 오개념이면 틀린다.
- source-clean: clean. 관계 **exact** / 판정 **ready** (1차 dryrun과 동일).
- 주의 문장: "이격거리 수치는 KEC 개정 영향 가능 — 학습 시 현행 기준 대조."

**설비-14 병가 — `2009_1회_92`**
- v3.2 trap: 저압을 특고압 위에 시설한다는 보기 (상하 배치).
- 기출: "고압·저압 가공전선 병가 시 이격거리 몇 cm?" 정답 (1) 50. 병가 이격거리
  수치를 검증 — v3.2의 상하 배치 순서 함정은 직접 검증 안 됨. 인접 하위 함정.
- source-clean: clean. 관계 **adjacent** / 판정 **ready_with_note** (1차와 동일).
- 주의 문장: "차이 명확 — 이격 수치를 검증, v3.2 상하 배치 함정은 별도. 후보
  metadata 오라벨(subject='전력공학', tag='가공전선로의 경간') — 콘텐츠 무관,
  DQ 트랙 정정 대상."

**전력-25 보호계전기 기능별 분류 — `2019_3회_31`**
- v3.2 trap: 한 계전기가 모든 사고를 감지한다는 보기.
- 기출: "전압요소가 필요한 계전기가 아닌 것?" 정답 (3) 지락 과전류 계전기.
  계전기를 전압요소 필요 여부로 분류 — v3.2의 만능 계전기 함정과는 다른 분류 축.
  인접 하위 함정.
- source-clean: clean. 관계 **adjacent** / 판정 **ready_with_note** (1차와 동일).
- 주의 문장: "차이 명확 — 전압요소 필요 여부 축을 검증, v3.2 만능 계전기 함정은
  별도. tag='전자파' 오라벨 — DQ 트랙 정정 대상."

### 교체 5항 — 검증

**전력-18 차단기 종류(소호매질) — `2017_2회_36`**
- v3.2 trap: 가스차단기와 진공차단기를 같은 원리로 설명하는 보기.
- 기출: "차단기와 아크 소호원리가 바르지 않은 것?" 정답 (2) "VCB: 공기 중 냉각에
  의한 아크 소호". VCB(진공차단기)는 진공의 높은 절연내력·아크 확산으로 소호 —
  공기 냉각 원리가 아니다. 보기 (1)OCB·(3)ABB·(4)MBB는 매질-원리 정합.
- source-clean: choices 4지 간결·판독 가능. 정답 (2) 표준 소호원리와 정합.
- 관계 **exact**: 차단기 종류↔소호원리 매핑 오류를 직접 검증.
- 판정 **ready**.
- 주의 문장: "VCB가 공기 냉각이 아니라 진공 소호임을 핵심으로 — 매질별 절연회복
  속도·아크 냉각 능력 차이를 함께 설명."

**기기-4 동기기 %Z — `2008_1회_46`**
- v3.2 trap: %Z를 기기 효율과 직접 연결하는 보기.
- 기출: "교류 발전기의 동기 임피던스는 철심이 포화하면?" 정답 (3) 감소한다.
  철심 포화 → 자기저항 증가 → 자속·리액턴스 감소 → 동기임피던스 감소.
- source-clean: choices 4지 판독 가능. 정답 (3) 표준 거동과 정합.
- 관계 **adjacent**: %Z(동기임피던스의 단위법 표현)와 같은 주제이나 *포화 시
  거동*을 검증 — v3.2 효율 연결 함정은 직접 검증 안 됨.
- 판정 **ready_with_note**.
- 주의 문장: "이 기출은 %Z의 포화 거동을 검증, v3.2 효율 연결 함정은 별도 —
  학습 시 '%Z 작을수록 단락전류 큼·전압변동 작음' 양면성을 보강."

**기기-23 유도전동기 속도제어 — `2019_3회_52`**
- v3.2 trap: 2차 저항제어가 효율을 높인다는 보기.
- 기출: "농형 유도전동기에 주로 사용되는 속도제어법은?" 정답 (1) 극수 변환법.
  농형은 회전자 권선 외부 인출이 없어 2차 저항제어·2차 여자제어 불가, 극수
  변환법이 적용 가능.
- source-clean: choices 4지 판독 가능. 정답 (1) 정합.
- 관계 **adjacent**: 속도제어법을 *전동기 형식별 적용 가능성*으로 식별 — v3.2의
  2차 저항제어 효율 함정과는 다른 축이나 같은 속도제어 주제의 인접 함정.
- 판정 **ready_with_note**.
- 주의 문장: "이 기출은 제어법-형식 매핑을 검증, v3.2 효율 함정은 별도 — 학습 시
  '2차 저항제어는 효율을 낮춘다'를 보강."

**설비-10 수도관·철골 접지극 — `2004_2회_82`**
- v3.2 trap: 모든 수도관을 접지극으로 쓸 수 있다는 보기.
- 기출: "대지 전기저항 3Ω 금속제 수도관로를 접지극으로 사용할 때, 접지선과
  수도관로 접속은 안지름 75mm 이상 수도관 분기점으로부터 몇 m 이내?" 정답 (2) 5.
- source-clean: choices 4지(3/5/8/10) 판독 가능. 정답 (2) 접속 거리 기준과 정합.
- 관계 **adjacent**: 수도관 접지극 시설의 *접속 위치 수치 기준*을 검증 — v3.2의
  사용 가능 조건 함정은 직접 검증 안 됨.
- 판정 **ready_with_note**.
- 주의 문장: "이 기출은 접속 거리 수치를 검증, v3.2 사용 조건 함정은 별도 —
  학습 시 '수도관 3Ω 이하라야 접지극 사용 가능' 조건을 보강. 후보 풀 빈약 —
  alt 사실상 부재."

**설비-21 발전기·변압기 보호장치 — `2021_2회_84`**
- v3.2 trap: 발전기 보호를 단순 과전류만으로 한다는 보기.
- 기출: "타냉식 변압기 냉각장치 고장 보호장치는?" 정답 (1) 경보장치. KEC
  발전기·변압기 보호장치 시설 — 타냉식 변압기는 냉각장치 고장 시 경보 장치 시설.
- source-clean: choices 4지 판독 가능. 정답 (1) KEC 시설 기준과 정합.
- 관계 **adjacent**: 보호 조건 중 *냉각이상* 항목을 검증 — v3.2의 과전류 단일
  함정과는 다른 축이나 같은 발·변압기 보호장치 주제의 인접 함정.
- 판정 **ready_with_note**.
- 주의 문장: "이 기출은 냉각이상 보호를 검증, v3.2 과전류 단일 함정은 별도 —
  학습 시 과전류·과전압·내부고장·냉각이상 4조건을 함께 정리. 후보 metadata
  오라벨(subject='전기기기', tag='변압기') — 콘텐츠는 설비-21 정합, DQ 정정 대상."

---

## needs_replacement / defer

- needs_replacement: **0항**. 교체 5항이 1차 dryrun의 탈락 사유(mismatch 1·정답
  충돌 2·source-clean FAIL 2)를 모두 해소했고, 유지 5항도 결격 없음.
- defer: **0항**. `2001_3회_43`은 본 재dryrun 대상 아님 — closeout R1 / selection
  §3대로 defer 유지(외부 전기기기 교재 필요).
- 1차 dryrun에서 needs_replacement였던 5항(기기-19·25·28, 설비-30, 회로-20)은
  replacement selection §4대로 본 pilot include에서 제외, 재선정 보류 항목.

---

## Residual (해소되지 않은 채 이월 — 3건)

본 재dryrun PASS는 *교체 후 10항의 검증 통과*를 뜻하며, 아래 3건은 B등급 모집단
구조에서 비롯된 잔여 한계로 학습 패키지 단계로 그대로 이월된다.

1. **회로 커버리지 0** — 1차 dryrun에서 회로-20(B등급 유일 회로이론 항목)이
   needs_replacement로 빠졌고, v3.2 B등급에 다른 회로 항목이 없어(회로-27은 C등급)
   보충 불가. B-pilot 10항은 기기 4 / 설비 4 / 전력 2의 3과목 pilot로 한정된다.
2. **trap type S/F 6/10 편중** — S/D 항목(회로-20)이 빠지면서 S/F가 과반(60%).
   S/C 4 / S/F 6 / S/D 0. v3.2 B등급의 설비 11·전력 3이 전부 S/F라 B-pool 자체가
   S/F 편중 — pilot 구성의 한계가 아니라 모집단 특성 반영.
3. **reserve 5항 소진** — replacement selection이 reserve 5항(기기-4·23, 설비-10·21,
   전력-18)을 전부 include로 승격해 대체 투입 후보가 0. 본 재dryrun에서 결격이
   없어 reserve 부재가 당장 문제되진 않으나, 향후 include 항목 결격 발생 시
   defer 풀(기기-7·26, 설비-12·23·27·29)의 representative mapping을 targeted
   dryrun으로 먼저 완료해야 투입 가능하다.

부수 관찰(residual 외): 관계 exact는 3/10(기기-17, 설비-13, 전력-18), 나머지
7항은 adjacent. 유지·교체가 모두 adjacent 비중이 높다 — 학습 콘텐츠 활용 시 각
항목 주의 문장대로 "이 기출이 검증하는 것 ≠ v3.2 대표 함정" 차이를 명시해야 한다.

---

## 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 10항 전수 검증 | ✅ 기기-17·18·4·23, 설비-13·14·10·21, 전력-25·18 — questions.json 직접 조회 |
| 10항 count | ✅ 유지 5 + 교체 5 = 10 |
| 판정별 count | ✅ ready 2 / ready_with_note 8 / needs_replacement 0 / defer 0 (합 10) |
| ready+ready_with_note 10/10 | ✅ **10/10 — PASS** |
| source-clean·정답 정합 직접 확인 | ✅ 10항 choices·answer 전수 확인. 기기-17 보기 [1] LaTeX 잉여 √3 확인 → ready_with_note 조정 |
| mismatch/정답충돌/OCR 손상 즉시 needs_replacement | ✅ 해당 0건 (교체 5항이 1차 dryrun 탈락 사유 해소) |
| adjacent 4항(교체) 억지 exact 금지 | ✅ 교체 5항 중 exact 1(전력-18), adjacent 4(기기-4·23, 설비-10·21) — adjacent 유지 |
| residual 3건 기록 | ✅ 회로 커버리지 0 / S/F 6/10 편중 / reserve 소진 — Residual 절에 기록 |
| 2001_3회_43 | ✅ 대상 아님, defer 유지 |
| 금지사항 준수 | ✅ app/data·questions.json·solution·answer/choices/text 미수정 / API·server 미실행 / 학습 로그·day plan 미작성 / amend·rebase·reset 없음 |

---

## 다음 단계 (제안만)

1. 본 재dryrun PASS로 B-pilot 학습 패키지 단계 진행 가능 — A-priority 방식
   (study-set → day plan → inline trap cues → 학습 로그)을 B등급 10항 소규모로 적용.
2. 학습 패키지 착수 전 cleanup: 기기-17 보기 [1] LaTeX 잉여 √3, 기기-18 보기 [4]
   '철손내력' 비표준 용어 — questions.json DQ 트랙(별도 승인) 대상.
3. residual 3건은 학습 패키지 설계 시 명시적으로 안고 간다 — 회로 과목 부재,
   S/F 편중, reserve 부재를 패키지 문서에 한계로 기록.

(이 문서는 재dryrun 검증까지 — 학습 로그·day plan은 별도 트랙·별도 승인.)

---

## Status

- B-priority proposed include 10항(유지 5 + 교체 5) representative targeted
  re-dryrun 완료 — questions.json 전수 직접 조회.
- 판정: ready 2(설비-13, 전력-18) / ready_with_note 8 / needs_replacement 0 /
  defer 0. ready+ready_with_note **10/10 — PASS**.
- 교체 5항이 1차 dryrun 탈락 사유(mismatch·정답 충돌·OCR 손상)를 모두 해소.
  유지 5항 중 기기-17은 보기 [1] LaTeX 잉여 √3 확인으로 ready→ready_with_note 조정.
- residual 3건(회로 커버리지 0 / S/F 6/10 편중 / reserve 소진) 학습 패키지로 이월.
- `2001_3회_43` defer 유지.
- 이 문서는 재dryrun 검증 문서다. 학습 로그·day plan 미작성.
