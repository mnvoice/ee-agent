# Input Selection Algorithm v2

## 1. 배경

v2 100문제 선택은 옵션 D 분포를 지키는 데는 성공했지만, 선택 알고리즘이 `tag` 키워드에 과하게 의존했다. 대표 사례가 `input_001`이다.

- 슬롯 의도: 전기자기학 동적 7항 중 `전자파`
- 실제 문제: 도체에 교류가 흐를 때의 `표피효과`
- 원인: 문제 데이터의 `tag`가 `전자파`였고, 선택기가 tag hit를 충분 조건처럼 사용함

이 문제는 단순 1건 교체 문제가 아니다. v2 품질 감사에서 `TAG_CONTENT_SUSPECT` 34건이 나왔고, 이는 tag 단독 매칭이 시스템적으로 불안정하다는 신호다. v3/v_full로 갈수록 이 문제가 확대될 수 있으므로, 입력 선택 알고리즘은 tag를 참고값으로 낮추고 `question_text`와 `solution`의 실제 내용 검증을 중심에 둬야 한다.

## 2. 새 알고리즘 원칙

1. **tag 단독 매칭 금지**
   - 기존 방식처럼 `tag`에 핵심어가 있다는 이유만으로 슬롯 후보에 넣지 않는다.
   - 후보는 `tag`, `question_text`, `solution`, 슬롯의 `matched_core_name`, `essence_question`을 함께 본다.

2. **매칭 점수 시스템**
   - 각 후보 문제에 슬롯 적합도 점수를 부여한다.
   - `question_text`를 가장 무겁게 본다. 문제 본문이 실제 출제 주제이기 때문이다.
   - `tag`는 보조 신호다. tag가 맞아도 본문이 다르면 제외될 수 있다.

3. **충돌 자동 제외**
   - tag와 question_text 핵심어가 명백히 다른 주제면 제외한다.
   - solution이 `정답 없음`을 명시하거나 hard conflict 신호를 갖는 후보는 제외한다.
   - question_text가 OCR로 깨져 주제를 판정할 수 없으면 제외하거나 SUSPECT로만 둔다.

4. **SUSPECT 영역 명시적 처리**
   - 100% 자동 선별을 목표로 하지 않는다.
   - 점수는 되지만 명확성이 낮은 문제는 `SUSPECT`로 남겨 사용자 검토 트랙에 태운다.
   - 옵션 D의 가치는 자동화율이 아니라 의심 케이스를 정확히 드러내는 데 있다.

## 3. 점수 가중치

| 항목 | 점수 | 사유 |
|---|--:|---|
| tag에 핵심어 포함 | +3 | 기존 라벨링 신호지만 오류 가능성이 있어 낮은 가중치 |
| question_text에 핵심어 포함 | +5 | 실제 출제 문장이므로 가장 강한 신호 |
| solution에 핵심어 포함 | +2 | 해설은 보조 근거. OCR/생성 해설 혼입 가능성이 있어 낮게 둠 |
| matched_core_name과 의미적으로 일치 | +5 | 슬롯 주제와 문제의 핵심이 직접 맞는지 보는 핵심 점수 |
| essence_question 주제와 일치 | +3 | 단순 단어가 아니라 본질 질문과 맞는지 확인 |

판정 기준:

| 총점 | 판정 | 처리 |
|---:|---|---|
| 15점 이상 | CLEAN | 표준 입력 후보 |
| 10~14점 | SUSPECT | 입력에는 포함 가능하나 `conflict_status: SUSPECT`와 score/detail 필수 |
| 10점 미만 | EXCLUDE | 자동 제외 |

기존 `CONFLICT_HARD`, `CONFLICT_SOFT`, `OCR_SUSPECT` 정책은 유지한다. 새 점수는 tag-content 정합성 판정용으로 추가된다.

## 4. 선택 알고리즘 흐름

점수 계산은 hard filter를 통과한 후보에만 적용한다. hard filter에서 제외된 후보는 점수가 10점 이상으로 보일 수 있어도 `EXCLUDE`로 확정한다.

1. 사전 자동 제외(Hard Filter)
   - tag-text 핵심어 명백 충돌 -> `EXCLUDE`
   - solution이 `정답 없음`, `문제 분석 불가`, 선택지 부재 등 해설 불능을 명시 -> `EXCLUDE`
   - question_text가 비어 있거나 OCR 파손으로 주제를 판정할 수 없음 -> `EXCLUDE`
   - session 형식 비정합 -> 정규화 가능하면 정규화, 불가능하면 `EXCLUDE`
2. 점수 계산
   - hard filter 통과 후 5축 점수를 계산한다.
   - 총점 15점 이상 -> `CLEAN`
   - 총점 10~14점 -> `SUSPECT`
   - 총점 10점 미만 -> `EXCLUDE`
3. 슬롯 배정
   - `CLEAN` 후보를 우선 배정한다.
   - `SUSPECT` 후보를 배정할 때는 입력 메타에 score와 근거를 반드시 박는다.
   - 후보가 부족하면 낮은 점수 후보를 끌어오지 않고 후보 부족을 report에 남긴다.

## 5. 충돌 자동 제외 룰

### tag-text 불일치 판정

다음 조건을 모두 만족하면 tag-text 명백 충돌로 보고 점수 계산 전에 자동 제외한다.

1. tag 또는 슬롯 핵심어가 question_text에 포함되지 않는다.
2. tag 또는 슬롯 핵심어가 solution에 포함되지 않는다.
3. question_text의 다른 핵심어가 tag 또는 슬롯과 다른 주제다.

예외: 다른 과목으로 이어지는 연결 주제는 자동 충돌로 보지 않는다. 예를 들어 자기학 `전자유도` 문제가 전기기기 `변압기`로 이어지는 경우는 과목 간 연결로 남기고, exact/synonym/parent-child 판정을 별도로 한다.

input_001 사례:

- tag/slot: `전자파`
- question_text 핵심어: `도체`, `교류`, `표피효과`, `전류 밀도`
- solution 핵심어: `주파수`, `도체`, `전류 밀도`, `표피효과`, `표피두께`
- 조건 1: question_text에 `전자파/전자기파/전파` 없음
- 조건 2: solution에 `전자파/전자기파/전파` 없음
- 조건 3: text 핵심어 `표피효과`는 `전자파`와 다른 동적7 주제이며 별도 슬롯으로 존재
- 판정: 점수 계산 전 `EXCLUDE`

추가 자동 제외 예:

- tag 또는 슬롯명이 상위 주제인데 question_text가 완전히 다른 하위 주제를 명시하고, 그 하위 주제가 별도 슬롯으로 존재함
- tag는 회로/제어 동적 주제인데 question_text가 법규/설비 숫자 암기 문제처럼 다른 과목 성격을 띰

### 핵심어 추출 방법

각 후보에서 다음 순서로 명사형 핵심어 3~5개를 뽑는다. 동사·형용사·조사·접속사와 일반 문제 문구(`옳은 것`, `틀린 것`, `다음 중`)는 제외한다. 도메인 용어를 우선한다.

1. question_text의 주어/목적어 명사
2. 보기의 반복 명사
3. solution 첫 문단의 정의 명사
4. 단위·공식에 붙은 개념명

예: `표피효과`, `변압기`, `피뢰기`, `접지`, `라플라스`, `전달함수`, `소호리액터`.

question_text와 solution은 각각 따로 추출한다. 둘 중 하나가 비어 있으면 비어 있는 축은 0점이고, question_text가 비어 있으면 hard filter에서 `EXCLUDE`한다.

### 의미적 일치 판정

의미적 일치는 다음 세 단계로 본다.

1. exact: 핵심어가 matched_core_name과 직접 일치
2. synonym: 같은 시험 주제의 표기 차이, 예: `피뢰기`와 `LA`
3. parent-child: 상위 주제와 하위 주제 관계, 예: `변압기 일반`과 `변압기 효율`

parent-child는 자동 CLEAN이 아니다. 하위 주제 슬롯이 별도로 있으면 AMBIGUOUS 또는 SUSPECT로 둔다.

## 6. session 변형 처리 정책

### session `1` 단독 97건 점검 결과

`app/data/questions.json`에서 session 값이 raw number `1`인 record는 97건이다. `app/data/questions.v2.json`에는 같은 97건이 `1회`로 정규화되어 있어, 회차 의미 자체는 `1회`가 맞다.

| 항목 | 결과 |
|---|---:|
| 대상 파일 | `app/data/questions.json` |
| session `1` 건수 | 97 |
| year 분포 | 2011년 97건 |
| q_no 범위 | 1~98, 642 |
| 누락 q_no | 31, 64, 99, 100 |
| subject 분포 | 전기자기학 24, 전기기기 25, 전력공학 22, 회로이론 8, 제어공학 10, 전기설비기술기준 7, 기타 1 |
| question_text 상태 | 97건 모두 빈 문자열 |
| solution 상태 | 대부분 존재, `questions.v2.json` 기준 2건 빈 문자열 |
| OCR 깨짐 흔적 | 명시적 깨짐 문자는 없음. 단, 본문 부재로 주제 판정 불가 |

`app/data/questions.v2.json`에서는 같은 year/session 묶음이 `2011_1회` 97건으로 존재한다. 따라서 session `1`은 **종류 A — 데이터 입력 노이즈**로 판정한다. 단, q_no 642 outlier와 question_text 전부 공백이라는 별도 품질 문제가 있으므로 회차 정규화만으로 CLEAN 후보가 되지는 않는다.

### 채택 정책

- raw session `1`은 입력 전처리에서 `1회`로 정규화한다.
- 후보 id 정규식은 output 검증 기준으로 `^[0-9]{4}_([1-6]회|1,2회)_[0-9]+$`를 유지한다. id에 raw `1`을 직접 허용하지 않는다.
- 정규화 후에도 question_text가 비어 있으면 hard filter에서 `EXCLUDE`한다.
- `2011_1_642`처럼 q_no가 1~100 범위를 벗어나는 outlier는 별도 데이터 정정 트랙으로 보내고 자동 입력 풀에서는 제외한다.

즉, session `1` 문제의 본질은 회차 문자열만 보면 종류 A지만, v2/v3 입력 풀에서는 `1 -> 1회` 정규화와 question_text hard filter를 모두 통과해야 한다.

## 7. 슬롯 배정 흐름

옵션 D 분포는 유지한다.

| 과목 | 개수 |
|---|--:|
| 전기자기학 | 15 |
| 회로이론 | 25 |
| 제어공학 | 15 |
| 전기기기 | 20 |
| 전기설비기술기준 | 15 |
| 전력공학 | 10 |

슬롯 배정 순서:

1. 각 과목의 슬롯을 먼저 고정한다.
2. 각 슬롯의 핵심어, 동의어, 제외어를 정의한다.
3. 5,331문제에서 subject가 맞는 후보를 먼저 거른다.
4. session 값을 정규화한다. raw `1`은 `1회`로 바꾸고, 허용할 수 없는 session은 제외한다.
5. `CONFLICT_HARD`, 명백한 tag-text mismatch, question_text 공백, 심한 OCR 파손은 hard filter에서 제외한다.
6. hard filter를 통과한 후보에 점수를 부여한다.
7. 점수 15점 이상을 우선 배정한다.
8. 점수 10~14점만 남으면 `SUSPECT`로 배정하되 입력 메타에 score와 사유를 박는다.
9. 후보가 부족하면 무리한 fallback을 하지 않고 후보 부족을 report에 남긴다.

입력 파일의 데이터 품질 메타는 다음처럼 확장한다.

```text
conflict_status: CLEAN | SUSPECT | AMBIGUOUS | CONFLICT_SOFT | OCR_SUSPECT
conflict_detail: score=12; question_text 핵심어는 맞지만 solution 핵심어 부족
```

## 8. 새 알고리즘 vs 기존 알고리즘 비교

| 사례 | 기존 알고리즘 | 새 알고리즘 |
|---|---|---|
| input_001 전자파 슬롯 | tag가 `전자파`라 선택됨 | question_text/solution 핵심어가 `표피효과`이고 전자파 핵심어가 없어 EXCLUDE |
| 상위 topic `변압기 일반` | tag/text 중 하나만 맞아도 선택 가능 | 하위 주제 `변압기 효율/병렬운전/권수비`가 명확하면 AMBIGUOUS 또는 해당 슬롯으로 재배정 |
| 후보 부족 슬롯 | 같은 과목 fallback 가능 | 점수 10 미만 fallback 금지. 후보 부족으로 보고 |
| 후보 배열 출력 | Markdown 리스트 문자열을 모델이 재해석 | 구조화 배열을 그대로 복사. 파싱 오염 시 빈 배열 처리 |

새 알고리즘에서는 `input_001` 같은 케이스가 박힐 수 없다. 기존 점수식만 단독 적용하면 tag +3, matched_core_name 표면 일치 +5, essence_question 표면 일치 +3으로 11점 `SUSPECT`처럼 보일 위험이 있다. 그러나 새 흐름에서는 hard filter가 먼저 작동하므로, question_text/solution에 `전자파` 핵심어가 없고 `표피효과`가 별도 주제로 확인되는 즉시 `EXCLUDE`된다.

기존 SUSPECT 34건은 새 알고리즘에서 세 갈래로 나뉜다.

- 점수 15점 이상: CLEAN 승격
- 점수 10~14점: SUSPECT 유지, 수동 검토
- 점수 10점 미만: EXCLUDE

## 9. 5,331문제 적용 가능성

v2 품질 감사의 100건 표본을 단순 환산하면 다음 위험이 있다.

| 항목 | 100건 관측 | 5,331건 환산 |
|---|--:|--:|
| TAG_CONTENT_MISMATCH | 1 | 약 53 |
| TAG_CONTENT_AMBIGUOUS | 5 | 약 267 |
| TAG_CONTENT_SUSPECT | 34 | 약 1,813 |
| PARSING_CONTAMINATED | 4 | 약 213 |

새 알고리즘 적용 후 예상은 다음과 같다.

| 분류 | 예상 비율 | 의미 |
|---|---:|---|
| CLEAN | 60~75% | question_text와 solution이 슬롯 핵심과 정합 |
| SUSPECT/AMBIGUOUS | 15~30% | 자동 해설 생성 전 수동 검토 또는 낮은 신뢰도 표시 필요 |
| EXCLUDE | 5~15% | tag-content 충돌, hard conflict, OCR 파손, 후보 부족 |

v2 100건 감사 결과를 새 hard filter 우선순위에 보수적으로 대입하면 다음과 같이 추정한다.

| 분류 | 추정 건수 | 근거 |
|---|--:|---|
| CLEAN | 60~75 | 기존 CLEAN 60건 + 일부 TAG_CONTENT_SUSPECT의 점수 승격 가능 |
| SUSPECT/AMBIGUOUS | 20~35 | 기존 AMBIGUOUS 5건과 핵심어 약한 SUSPECT 일부 |
| EXCLUDE | 1~5 | input_001 명백 mismatch 1건 + question_text/solution 불능 또는 hard conflict 후보 |

v_full 5,331문제 진입은 가능하지만, `SUSPECT`를 숨기면 안 된다. 자동화 성공 기준은 모든 문제를 CLEAN으로 만드는 것이 아니라, CLEAN/SUSPECT/EXCLUDE를 안정적으로 분리하는 것이다.

## 10. 검증 방법

새 알고리즘으로 v2 100건을 재선정하면 다음을 확인한다.

1. 전기자기학 동적 7항이 모두 실제 question_text/solution과 일치하는가.
2. `input_001` 전자파/표피효과 같은 mismatch가 0건인가.
3. `SUSPECT`가 34건에서 얼마나 줄었는가.
4. 후보 부족 케이스에서 output 후보 id 오염이 재발하지 않는가.
5. `related_problems.same_core`와 `same_trap_pattern`의 모든 id가 `^[0-9]{4}_([1-6]회|1,2회)_[0-9]+$`를 통과하는가.
6. raw session `1` 후보가 `1회`로 정규화되며, question_text 공백 후보가 입력에 들어오지 않는가.

예측:

- tag-text mismatch는 0건에 가까워져야 한다.
- 후보 부족은 일부 남을 수 있지만, 파싱 오염은 0건이어야 한다.
- 가설 1 검증은 input_001을 제외하지 않고도 동적 7항 전체로 다시 계산 가능해야 한다.
