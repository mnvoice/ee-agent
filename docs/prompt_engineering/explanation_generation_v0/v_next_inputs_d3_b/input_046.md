# v_next D-3 input 046: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2004_1회_84
year: 2004
session: 1회
q_no: 84
subject: 전력공학
question_text: 특고압 지중전선이 가연성이나 유독성의 유체를 내포하는 관과 접근하기 때문에 상호간에 견 고한 내화성의 격벽을 시설하였다．상호간의 이격거 리가 몇 \([\mathrm{m}]\) 이하인 경우인가？
choices:
  1. 0.4
  2. 0.6
  3. 0.8
  4. 1
answer: 2
solution: 특고압 지중전선이 가연성이나 유독성의 유체를 내포하는 관과 접근 또는 교차하는 경우, 상호간에 내화성의 격벽을 설치해야 한다.

전기설비기술기준 제334.6조의 표에 따르면:

**가연성, 유독성의 유체를 내포하는 관과 접근 또는 교차하는 경우**
- 특고압: **1[m]** 이하의 이격거리
- 25[kV] 이하: 0.5[m] 이하의 이격거리

문제에서 "특고압 지중전선이 가연성이나 유독성의 유체를 내포하는 관과 접근"이라고 명시되어 있으므로, 이 조건에 해당한다.

따라서 정답은 **(1) 0.4[m]이 아니라 1[m] 이하**이며, 문제의 정답 표기 "0번"은 보기 (4) 1을 의미한다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=이격거리; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 가공전선 이격거리
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 가공전선과 다른 시설간 안전 이격거리는 어떻게 정해지는가
representative_trap: 전선 종류별 이격거리 표 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 전선 종류별 이격거리 표 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82, 2002_3회_85, 2003_3회_81, 2004_1회_91, 2004_2회_86, 2004_3회_83]
same_trap_pattern_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82]

