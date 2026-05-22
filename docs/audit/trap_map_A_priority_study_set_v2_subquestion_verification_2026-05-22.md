# Trap-Map A-Priority Study Set v2 — Sub-Question Verification (2026-05-22)

study-set v2(`..._study_set_v2_2026-05-22.md`)의 needs-alt-question 3항(기기-3·
기기-13·전력-21)에 추가된 **보조 문항(sub) 5개**를 검증한다.

이 문서는 **검증 + 분류**다. app/data 미수정. solution/steps 미적용.
answer/choices/text 미수정. commit/push 없음. 유료 API 미호출.

- 검증 대상 sub 5개:
  - 기기-3: `2011_2회_47`, `2015_2회_55`
  - 기기-13: `2008_1회_41`
  - 전력-21: `2009_1회_22`, `2012_1회_39`
- (a) 출처: `app/data/questions.json`, `app/data/questions.v2.json`

검증 항목: (1) 두 파일 실재 (2) 4지선다 보존 (3) OCR 잔류물·정답 보기 손상 부재
(4) 보강 함정 축 정합 (5) 정답/보기 obvious conflict 부재 (6) 4버킷 분류.

분류 버킷: sub-verified / needs-cleanup / weak-alignment / reject.

---

## 0. 시작 전 git 확인

- `git status --short --untracked-files=no` → tracked working tree clean
- branch `feat/phase-b-migration` ↔ origin 동기, HEAD `ccc9bb4` (변동 없음)

---

## 1. 항목별 검증

### 1.1 `2011_2회_47` — 기기-3 sub-1 (권계수 영역)

| 검증 항목 | 결과 |
|---|---|
| (1) 실재 | questions.json ✓ / questions.v2.json ✓ — 양쪽 동일, 중복 키 없음 |
| (2) 4지선다 | choices 4개, answer=4 (약 0.887), 범위 정상 |
| (3) OCR | 잔류물 0, 정답 보기 손상 0 (헤더·latex·PUA·빈 보기 없음) |
| (4) 축 정합 | 기기-3 **권계수 영역 직접 정합** — "4극 3상 48슬롯 매극매상 분포, 코일간격 75% 단절권 → 권선계수?" 권선계수 = kp(단절권)·kd(분포권) 계산을 정면으로 검증 |
| (5) 정답 conflict | 없음 — q=48/(3×4)=4, kp=sin(67.5°)≈0.924, kd≈0.958, kw≈0.885≈0.887. 정답 (4)와 정합. solution이 kd 산출 과정 보유 |

- subject='전기기기' / tag='동기발전기의 동기속도(Ns), 단절권 계수(kp), 분포권
  계수(kd), 유기기전력(E)'.
- **참고**: 문항 소재는 *유도전동기*의 권선계수이나, kp·kd 공식·계산은 기종(동기/
  유도) 무관하게 동일하다. 기기-3(동기발전기 권계수) 보강용으로 권계수 *계산 절차*
  검증에는 적합. 기종 표기 차이는 학습에 무관.
- **분류: sub-verified**

### 1.2 `2015_2회_55` — 기기-3 sub-2 (권계수 영역)

| 검증 항목 | 결과 |
|---|---|
| (1) 실재 | questions.json ✓ / questions.v2.json ✓ — 양쪽 동일, 중복 키 없음 |
| (2) 4지선다 | choices 4개, answer=2, 범위 정상 |
| (3) OCR | 잔류물 0, 정답 보기 손상 0 |
| (4) 축 정합 | 기기-3 **권계수 영역 직접 정합** — 분포계수(kd) 식 선택. "분포권과 단절권으로 파형 개선 ... 분포계수 식은?" |
| (5) 정답 conflict | 없음 — 정답 (2) `sin(π/2m)/(q·sin(π/2mq))`는 표준 분포권계수 공식. solution이 동일 공식 명시 |

- subject='전기기기' / tag=동기발전기 동기속도/권계수 버킷 (정합).
- **참고**: 문제 단서는 슬롯 간격을 α로 정의하나 보기 (1)(4)는 'a'로 표기 (α→a
  표기 혼재). 정답 보기 (2)는 π/2m 형식으로 명확 — 정답 판단에 영향 없음. 경미한
  표기 비일관(비차단).
- **분류: sub-verified**

### 1.3 `2008_1회_41` — 기기-13 sub (f2=sf 영역)

| 검증 항목 | 결과 |
|---|---|
| (1) 실재 | questions.json ✓ / questions.v2.json ✓ — 양쪽 동일, 중복 키 없음 |
| (2) 4지선다 | choices 4개 (6/54/60/600), answer=1, 범위 정상 |
| (3) OCR | 정답 보기 손상 0, 잔류물(헤더·latex) 0. 단, 문제 text에 1자 OCR 오타 (아래 참고) |
| (4) 축 정합 | 기기-13 **f2=sf 영역 직접 정합** — "60Hz 4극 권선형 유도전동기 슬립 0.1 → 회전자 주파수?" 회전자(2차) 주파수 f2=sf를 정면으로 검증 |
| (5) 정답 conflict | 없음 — f2 = s·f1 = 0.1×60 = 6Hz. 정답 (1)=6과 정합 |

- subject='전기기기' / tag='동기발전기의 병렬운전 조건' (**tag 오라벨** — 내용은
  권선형 유도전동기 회전자 주파수. 메타데이터 경미, 학습 무관).
- solution 필드 비어 있음 — study-set v2는 pedagogy 적용 전 단계이므로 비차단
  (해설은 후속 pedagogy apply 단계 작업).
- **참고**: 문제 text "슬림 0.1" — "슬립 0.1"의 1자 OCR 오타. 보기·정답에는 영향
  없고, 문맥(권선형 유도전동기, 회전자, 슬립값)으로 의미 명확. 검증 항목 (3)의
  차단 기준(잔류물·정답 보기 손상)에는 해당하지 않음 — 비차단. 선택적 cleanup 대상.
- **분류: sub-verified** (text 1자 오타 "슬림→슬립"은 비차단 — 선택적 cleanup 권장)

### 1.4 `2009_1회_22` — 전력-21 sub-1 (중성점 접지방식 다축 비교)

| 검증 항목 | 결과 |
|---|---|
| (1) 실재 | questions.json ✓ / questions.v2.json ✓ — 양쪽 동일, 중복 키 없음 |
| (2) 4지선다 | choices 4개, answer=3, 범위 정상 |
| (3) OCR | 잔류물 0, 정답 보기 손상 0 |
| (4) 축 정합 | 전력-21 **중성점 접지방식 비교 직접 정합** — 비접지방식 vs 직접접지를 전자유도장해·지락전류·보호계전기·영상전류 다축으로 비교. main(`2016_3회_38`, 전압상승 단축)이 못 다루는 다축 비교를 보강 |
| (5) 정답 conflict | 없음 — 정답 (3) "보호계전기 동작 확실"이 옳지 않은 것 (비접지는 보호계전 불확실). 보기 (1)(2) 참(비접지 유도장해·지락전류 작음), (3) 거짓. solution이 "보호계전기 동작 불확실" 명시. 단일 오답 명확 |

- subject='전력공학' / tag='중성점 접지방식의 각 항목에 대한 비교표' (정합).
- **분류: sub-verified**

### 1.5 `2012_1회_39` — 전력-21 sub-2 (지락전류 축)

| 검증 항목 | 결과 |
|---|---|
| (1) 실재 | questions.json ✓ / questions.v2.json ✓ — 양쪽 동일, 중복 키 없음 |
| (2) 4지선다 | choices 4개, answer=4, 범위 정상 |
| (3) OCR | 잔류물 0, 정답 보기 손상 0 |
| (4) 축 정합 | 전력-21 **중성점 접지방식 비교 직접 정합** — "1선 지락 시 지락전류 가장 작은 방식?" 4방식을 지락전류 축으로 비교. main(전압상승 축)·sub-1(다축)과 함께 지락전류 축 보강 |
| (5) 정답 conflict | 없음 — 정답 (4) 소호리액터접지. 지락전류 크기: 직접 > 저항 > 비접지 > 소호리액터. solution이 동일 순서 명시. 정합 |

- subject='전력공학' / tag='중성점 접지방식의 각 항목에 대한 비교표' (정합).
- **분류: sub-verified**

---

## 2. 검증 결과 요약

| sub | 보강 대상 | 실재(v1/v2) | 4지선다 | OCR | 축 정합 | 정답 conflict | 분류 |
|---|---|:-:|:-:|:-:|:-:|:-:|---|
| `2011_2회_47` | 기기-3 권계수 | ✓/✓ | ✓ | clean | 직접 정합 | 없음 | **sub-verified** |
| `2015_2회_55` | 기기-3 권계수 | ✓/✓ | ✓ | clean | 직접 정합 | 없음 | **sub-verified** |
| `2008_1회_41` | 기기-13 f2=sf | ✓/✓ | ✓ | clean¹ | 직접 정합 | 없음 | **sub-verified** |
| `2009_1회_22` | 전력-21 다축 비교 | ✓/✓ | ✓ | clean | 직접 정합 | 없음 | **sub-verified** |
| `2012_1회_39` | 전력-21 지락전류 축 | ✓/✓ | ✓ | clean | 직접 정합 | 없음 | **sub-verified** |

¹ `2008_1회_41`: 정답 보기·잔류물 손상 0. 문제 text에 1자 OCR 오타("슬림→슬립") —
검증 차단 기준 외, 비차단.

| 분류 | 건수 | 항목 |
|---|--:|---|
| sub-verified | 5 | 5개 sub 전부 |
| needs-cleanup | 0 | — |
| weak-alignment | 0 | — |
| reject | 0 | — |

- **5개 sub 전부 sub-verified.** 모든 sub가 questions.json·questions.v2.json
  양쪽에 동일하게 실재, 4지선다 보존, 잔류물·정답 보기 손상 없음, 보강 대상 함정
  축과 직접 정합, 정답·보기 obvious conflict 없음.
- 경미 사항 3건 (전부 비차단):
  - `2011_2회_47`: 문항 소재가 유도전동기 — 단, 권계수 계산은 기종 무관 동일.
  - `2015_2회_55`: 단서 α vs 보기 'a' 표기 혼재 — 정답 보기는 명확.
  - `2008_1회_41`: text "슬림→슬립" 1자 오타 + tag 오라벨('동기발전기 병렬운전').
- 메타데이터 경미(tag 오라벨): `2008_1회_41`, `2011_2회_47` — 콘텐츠·학습 무관,
  DQ 트랙 일괄 정정 대상.

---

## 3. study-set v2 분류 갱신 권고

5개 sub 전부 sub-verified이므로, study-set v2의 needs-alt-question 3항(기기-3·
기기-13·전력-21)은 보조 문항 검증을 통과했다. v2 §5.3의 승급 조건("sub 후보의
정합·정답 검증을 거치면 study-ready-with-adjacent-note로 승격 가능")이 충족된다.

권고: study-set v3(또는 v2 갱신) 작성 시 —
- 기기-3·기기-13·전력-21을 **needs-alt-question → study-ready-with-adjacent-note**로
  승격. main+sub 묶음 구성 확정.
- 갱신 후 4버킷: study-ready 6 / study-ready-with-adjacent-note 20 /
  needs-alt-question 0 / hold 0.
- `2008_1회_41` text 오타("슬림→슬립")는 선택적 cleanup — 학습 사용은 비차단이나
  needs-cleanup 트랙에서 함께 정정 가능.

(승격·갱신은 별도 승인 — 본 문서는 검증·분류·권고까지만.)

---

## Not done in this step

- `app/data/questions.json` / `questions.v2.json` 미수정.
- solution / steps 미적용. answer / choices / text 미수정.
- study-set v2 문서 미갱신 (needs-alt-question→study-ready 승격은 별도 승인).
- `2008_1회_41` text 오타 미수정 (선택적 cleanup 권고만).
- commit / push 없음. 유료 API 미호출.

## Status

- study-set v2 보조 문항 5개 검증 완료.
- 5개 sub 전부 questions.json·questions.v2.json 양쪽 실재·동일, 4지선다 보존,
  잔류물·정답 보기 손상 없음, 보강 축 직접 정합, 정답 conflict 없음.
- 분류: **sub-verified 5 / needs-cleanup 0 / weak-alignment 0 / reject 0.**
- 경미 비차단 사항 3건 (유도전동기 소재 / α-a 표기 혼재 / 슬림→슬립 오타).
- 권고: needs-alt-question 3항을 study-ready-with-adjacent-note로 승격 (별도 승인).
