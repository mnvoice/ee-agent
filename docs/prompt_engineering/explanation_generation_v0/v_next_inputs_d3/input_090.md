# v_next D-3 input 090: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2007_2회_81
year: 2007
session: 2회
q_no: 81
subject: 전력공학
question_text: 특고압 가공 전선로의 지지물에 시설하는 통신선 또는 이에 직접 접속하는 통신선 중 옥내에 시설하는 부분은 몇［V］초과의 저압 옥내 배선의 규 정에 준하여 시설하도록 하고 있는가？
choices:
  1. 150
  2. 300
  3. 380
  4. 400
answer: 2
solution: **핵심 기준:** 특고압 가공전선로의 지지물에 시설하는 통신선 또는 이에 직접 접속하는 통신선 중 옥내에 시설하는 부분의 안전 기준

**관련 규정:** 전기설비기술기준 제362.7조

**풀이:**
특고압 가공전선로(광섬유 케이블 제외)의 지지물에 시설하거나 직접 접속하는 통신선이 옥내로 들어오는 부분은 저압 옥내 배선의 규정을 적용해야 한다. 이때 적용 기준은 
\[ 400[\mathrm{V}] \text{ 초과의 저압 옥내 배선 기준} \]
으로 정해져 있다.

**정답:** (4) 130 → **정정: 정답은 400V**

**오답 분석:**
- (1) 0V: 의미 없음
- (2) 110V: 기준 미달
- (3) 120V: 기준 미달
- (4) 130V: 보기에 있으나 정답이 아님

실제 정답은 보기에 없으며, 기준은 **400V**이다.

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

