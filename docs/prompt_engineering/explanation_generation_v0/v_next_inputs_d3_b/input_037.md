# v_next D-3 input 037: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2002_3회_85
year: 2002
session: 3회
q_no: 85
subject: 전력공학
question_text: 농사용 저압 가공 전선로의 최대 경간은 몇 [m]인가?
choices:
  1. 30
  2. 60
  3. 50
  4. 100
answer: 1
solution: **문제:** 농사용 저압 가공 전선로의 최대 경간

**핵심 기준:** 전기설비기술기준 222.22 - 농사용 저압 가공전선로의 시설

**농사용 저압 가공전선로의 기준:**
- 사용 전압: 저압
- 전선 사양: 인장강도 1.38 [kN] 이상 또는 지름 2 [mm] 이상 경동선
- 지표상 높이: 3.5 [m] 이상 (또는 최소 3 [m])
- 목주 굵기: 말구 지름 0.09 [m] 이상
- **지지점 간 거리(경간): 30 [m] 이하** ✓

**선택지 검토:**
- (1) **30 [m]** ✓ **정답**
- (2) 60 [m] - 기준 초과
- (3) 50 [m] - 기준 초과
- (4) 100 [m] - 기준 초과

**결론:** 정답 **(1번) 30 [m]**

**설명:** 농사용 저압 가공전선로는 일반 저압 가공전선로보다 엄격한 기준을 적용받으며, 최대 경간은 30 [m] 이하로 제한됩니다. 이는 농촌 지역의 안전성을 보장하기 위한 규정입니다.

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
same_core_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82, 2003_3회_81, 2004_1회_84, 2004_1회_91, 2004_2회_86, 2004_3회_83]
same_trap_pattern_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82]

