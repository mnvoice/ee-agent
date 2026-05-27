# v_next D-3 input 068: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 2005_3회_26
year: 2005
session: 3회
q_no: 26
subject: 전력공학
question_text: 초고압 장거리 송전선로에 접속되는 타 변전소에 분로 리액터를 설치하는 목적은？
choices:
  1. 변화 없다．
  2. \(1 / 2\) 배로 된다．
  3. 분제 28 2015년도 1회 문제 21
  4. 4 배로 된다．
answer: 3
solution: **페란티 현상의 정의 및 발생 원인:**
장거리 송전선로에서 무부하 또는 경부하 상태일 때, 선로의 정전용량으로 인해 진상 전류가 흘러 수전단 전압이 송전단 전압보다 높아지는 현상을 페란티 현상이라 한다.

**분로 리액터(Shunt Reactor) 설치의 목적:**
분로 리액터는 선로의 정전용량에 의해 발생하는 진상 전류를 상쇄시키는 지상(선로의 중간에 연결)용량을 제공한다. 이를 통해:
- 과전압(페란티 현상)을 억제
- 선로의 안정성 향상
- 전압 상승을 제어

**정답 선택:**
정답은 **(4) 4배로 된다**가 아니라 **문제 풀이에서 명시된 조상 용량으로 페란티 현상을 방지한다**는 개념형 암기 답변이다.

**참고:** 원문에 다소의 일관성 부족이 있으나, 분로 리액터의 주 목적은 **초고압 장거리 송전에서 페란티 현상(무부하/경부하 시 과전압)을 억제**하는 것이다.

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
same_core_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22, 2001_2회_29, 2002_3회_37, 2004_2회_24, 2005_2회_31, 2007_1회_24]
same_trap_pattern_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22]

