# v_next D-3 input 081: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2006_3회_83
year: 2006
session: 3회
q_no: 83
subject: 전력공학
question_text: 특고압 가공 전선로에 사용하는 가공 지선 에는 지름 몇［mm］의 나경동선 또는 이와 동등 이상 의 세기 및 굵기의 나선을 사용하여야 하는가？
choices:
  1. 2.6
  2. 3.5
  3. 4
  4. 5
answer: 4
solution: **핵심 규정:**

전기설비기술기준 제333.8조에서 특고압 가공전선로의 가공지선 규격을 규정합니다.

**가공지선 허용 규격:**

다음 중 **하나 이상**을 만족하는 지선 사용:

**가. 인장강도 기준**
- 인장강도 ≥ 8.01[kN] 이상의 나선

**나. 나경동선**
- 지름 ≥ **5[mm]** 이상

**다. 나경동연선**
- 단면적 ≥ 22[mm²] 이상

**라. 아연도강연선**
- 단면적 ≥ 22[mm²] 이상

**마. OPGW 전선**

**오답 분석:**
- (1) 2.6[mm]: 규정 미달
- (2) 3.5[mm]: 규정 미달
- (3) 4[mm]: 규정 미달 (5[mm] 미만)
- (4) **5[mm] 이상**: 정답 → 나경동선 기준 충족

**정답: (4) 5[mm] 이상의 나경동선**

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

