# v_next D-3 input 074: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2006_1회_86
year: 2006
session: 1회
q_no: 86
subject: 전력공학
question_text: 빙설이 많은 지방이고 인가가 많이 연접된 장소에 시설하는 가공전선로의 구성재 중 병종 풍압 하중의 적용을 할 수 없는 것은？
choices:
  1. 지판 또는 고압 가공전선로의 가선선
  2. 지판 또는 고압 가공전선로의 지지물
  3. 35[kV] 이하인 전선에 특고압 절연전선을 사용하는 특고압 가공전선로의 지지물에 시설하는 가공전선
  4. 35[kV]를 초과하는 특고압 가공전선로의 지지물에 시설하는 가공전선
answer: 4
solution: **핵심 규정:**

전기설비기술기준 331.6 풍압하중의 종별과 적용

**기준 내용:**
인가가 많이 연접되어 있는 장소에 시설하는 가공전선로의 구성재 중 **병종 풍압하중을 적용할 수 있는 경우:**

가. 저압 또는 고압 가공전선로의 **지지물 또는 가섭선**

나. 사용전압이 \(35[\mathrm{kV}]\) 이하의 전선에 특고압 절연전선 또는 케이블을 사용하는 특고압 가공전선로의 **지지물, 가섭선 및 특고압 가공전선을 지지하는 애자장치 및 완금류**

**풀이 과정:**
- 병종 풍압하중은 인가 밀집지역의 안전기준 완화
- (1) 가섭선: 가능 ✓
- (2) 지지물: 가능 ✓
- (3) 특고압 관련 지지물: 가능 ✓
- (4) 기타 구성재: 불가능

**정답:** 4번 (병종 풍압하중 적용 불가 구성재)

**오답 분석:**
- (1), (2), (3): 모두 병종 풍압하중 적용 가능

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

