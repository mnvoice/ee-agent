# v_next D-3 input 016: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 2000_6회_21
year: 2000
session: 6회
q_no: 21
subject: 전력공학
question_text: 송전 선로의 선로 정수가 아닌 것은 다흠 중 어느 것인가？
choices:
  1. 지향
  2. 리액턴스
  3. 정전용량
  4. 누설 콘덕턴스
answer: 2
solution: **문제 분석:**
송전 선로의 선로 정수(line constants)가 아닌 것을 찾는 문제입니다.

**선로 정수의 정의:**
송전선로의 단위 길이당 전기적 특성을 나타내는 4가지 기본 정수:

1. **저항 (R)**: 도체의 저항, 거리에 무관한 상수
2. **인덕턴스 (L)**: 도체 주변의 자계에 의한 인덕턴스, 거리에 무관한 상수
3. **정전용량 (C)**: 도체 간의 정전용량, 거리에 무관한 상수
4. **누설 콘덕턴스 (G)**: 절연체의 누설, 거리에 무관한 상수

**리액턴스는 선로 정수가 아닌 이유:**
\[X = 2\pi f L\]

리액턴스는:
- **주파수(f)에 따라 값이 변함** → 상수가 아님
- 인덕턴스(L)는 선로 정수이지만, 리액턴스(X)는 인덕턴스에 주파수를 곱한 값
- 선로 정수는 물리적 특성에 의해 결정되어야 하는데, 리액턴스는 운영 조건(주파수)에 따라 달라짐

**정답: 2번 (리액턴스 X)**

**오답 분석:**
- (1), (3), (4)에 제시된 열역학 사이클은 전력공학과 무관한 내용으로, 문제와 맞지 않는 보기입니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=선로 정수; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 송전 용량/거리
star: null
ds_class: D
phenomenon_origin: D/Dynamic
six_axis: []
essence_question: 송전 거리와 전압이 송전 용량에 어떻게 작용하는가
representative_trap: 송전 전압급 단위 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 송전 전압급 단위 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 송전용량 -> 회로 4단자망 -> 회로 분포정수

[연관 문제 후보]
same_core_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2001_1회_22, 2001_2회_29, 2002_3회_37, 2004_2회_24, 2005_2회_31, 2005_3회_26, 2007_1회_24]
same_trap_pattern_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2001_1회_22, 2001_2회_29]

