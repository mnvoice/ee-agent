# v_next D-3 input 086: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2007_1회_84
year: 2007
session: 1회
q_no: 84
subject: 전력공학
question_text: 가공 전선로의 지지물에 시설하는 지선에 관한 사항으로 옳은 것은？
choices:
  1. 지선의 안전율은 1.2 이상인 것
  2. 지선에 연선을 사용할 경우에는 소선은 3가닥 이상인 것
  3. 소선은 지름 1.2 [mm] 이상인 금속선을 사용한 것인 것
  4. 도로를 횡단하여 시설하는 지선의 높이는 표통에서 5[m] 이상으로 하여야 한다
answer: 1
solution: **핵심 기준:** 전기설비기술기준 331.11 지선(가공전선로 지지물)의 시설

**각 선택지 검토:**

**(1) 소선 3가닥 이상의 연선일 것** ✓ 정답
- 규정: "지선에 연선을 사용할 경우 소선 3가닥 이상의 연선일 것"

**(2) [제시되지 않음]**

**(3) 소선은 지름 1.2 [mm] 이상인 금속선을 사용한 것** ✗
- 오류: 규정에서는 **2.6 [mm] 이상**으로 규정
- 1.2 mm는 규정보다 너무 작음

**(4) 도로 횡단 지선 높이 2.0 [m] 이상** ✗
- 오류: 규정 높이는 다음과 같음:
  - 일반적: 5.0 [m] 이상
  - 교통 지장 우려 없는 경우: 4.5 [m] 이상
  - 보도의 경우: 2.5 [m] 이상
  - 2.0 [m]는 규정에 없는 수치

**정답:** 2번 (선택지 (1))

**추가 규정 사항:**
- 안전율: 2.5 이상 (허용 인장하중 최저 4.31 [kN])
- 지중부분 및 0.3 [m]까지: 내식성 있는 재료 또는 아연도금 철봉 사용

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=가공전선; audit_group=non_expansion_metadata

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

