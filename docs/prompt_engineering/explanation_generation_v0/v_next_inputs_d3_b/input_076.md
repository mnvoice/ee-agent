# v_next D-3 input 076: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2006_2회_83
year: 2006
session: 2회
q_no: 83
subject: 전력공학
question_text: 시가지에서 저압 가공전선로를 도로에 따 라 시설할 경우 지표상의 최저 높이는 몇［m］이상이 어야 하는가？
choices:
  1. 4.5
  2. 5
  3. 5.5
  4. 6
answer: 1
solution: 시가지에서 저압 가공전선로를 도로에 따라 시설할 경우의 지표상 최저 높이는 전기설비기술기준 제222.7조(저압 가공전선의 높이)에서 규정합니다.

도로횡단(번잡하지 않은 도로 제외)의 경우:
\[ \text{지표상 높이} \geq 6 \text{ [m]} \]

제시된 표에 따르면 도로를 횡단하는 저압 가공전선의 최저 높이는 **6[m] 이상**이어야 합니다.

오답 분석:
- (1) 4.5[m]: 불충분한 높이
- (2) 5[m]: 불충분한 높이
- (3) 5.5[m]: 불충분한 높이
- (4) 6[m]: **정답** - 기술기준에서 규정한 정확한 값

정답: **(4) 6[m]**

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=가공전선; audit_group=non_expansion_metadata

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
same_core_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82, 2002_3회_85, 2003_3회_81, 2004_1회_84, 2004_1회_91, 2004_2회_86]
same_trap_pattern_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82]

