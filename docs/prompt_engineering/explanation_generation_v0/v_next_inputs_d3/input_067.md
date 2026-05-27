# v_next D-3 input 067: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 2005_2회_31
year: 2005
session: 2회
q_no: 31
subject: 전력공학
question_text: 송전 선로의 페란티 효과를 방지하는데 효 과적인 것은？
choices:
  1. 분로 리액터 사용
  2. 복토제 사용
  3. 병렬 콘덴서 사용
  4. 직렬 콘덴서 사용
answer: 1
solution: 송전선로의 페란티 효과 방지 대책에 관한 문제입니다.

**페란티 현상(Ferranti Effect):**

송전선로의 정전용량으로 인하여 무부하 또는 경부하 운전 시 진상 전류가 흐르게 되고, 이로 인해 수전단 전압이 송전단 전압보다 높아지는 현상입니다.

\[V_R > V_S\] (무부하 또는 경부하 시)

**페란티 효과 방지 대책:**

1) **분로 리액터(Shunt Reactor) 설치** ✓
   - 정전용량의 지상 전류를 흡수
   - 가장 효과적인 방법

2) **동기 조상기(Synchronous Condenser)** ✓
   - 지상 무효전력 공급
   - 유연한 제어 가능

**오답 분석:**

- (2) 복도체 사용: 선로 임피던스 감소로 오히려 페란티 현상 악화
- (3) 병렬 콘덴서 사용: 지상 전류 증가로 현상 악화
- (4) 직렬 콘덴서 사용: 송전 용량 증가용도, 페란티 효과 해결 불가

**정답:** (1) 분로 리액터 또는 동기 조상기의 지상 용량 사용

**핵심 포인트:**
ページンティ현상은 **과잉 전압** 현상이므로, 이를 억제하려면 **지상 무효전력 흡수**가 필요합니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=송전선; audit_group=expansion

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
same_core_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22, 2001_2회_29, 2002_3회_37, 2004_2회_24, 2005_3회_26, 2007_1회_24]
same_trap_pattern_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22]

