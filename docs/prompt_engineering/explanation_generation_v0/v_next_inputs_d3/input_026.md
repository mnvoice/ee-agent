# v_next D-3 input 026: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2001_2회_82
year: 2001
session: 2회
q_no: 82
subject: 전력공학
question_text: 저압 가공 전선이 \(25[\mathrm{kV}]\) 교류 전차선의 위에 교차하여 시설되는 경우 저압 가공 전선으로 케이블을 사용하고 단면적 몇 \(\left[\mathrm{mm}^{2}\right]\) 이상인 아연도 강연선으로 인장 강도 \(19.61[\mathrm{kN}]\) 이상인 것으로 조 가하여 시설하여야 하는가?
choices:
  1. 22
  2. 35
  3. 55
  4. 100
answer: 3
solution: 이 문제는 전기설비기술기준 222.15에 따른 저압 가공전선과 교류전차선의 교차 시설 기준을 묻고 있습니다.

**핵심 기준:**
저압 가공전선이 25[kV] 교류 전차선의 위에 교차하여 시설되는 경우, 다음 조건을 모두 만족해야 합니다:
- 저압 가공전선으로는 **케이블을 사용**
- 아연도강연선(가선)의 단면적: **35[mm²] 이상**
- 아연도강연선의 인장강도: **19.61[kN] 이상**

**관련 규정:**
가. 저압 가공전선에는 케이블을 사용하고 또한 이를 단면적 **35[mm²] 이상**인 아연도강연선으로서 인장강도 19.61[kN] 이상인 것으로 조가하여 시설할 것.

**보기 분석:**
- (1) 22[mm²]: 부족함 - 최소 35[mm²] 필요
- (2) 정보 없음
- (3) 55[mm²]: 35[mm²]보다 크므로 가능하나, 최소 기준은 35
- (4) 100[mm²]: 35[mm²]보다 크므로 가능하나, 최소 기준은 35

**정답: (2) 35[mm²]** (표기상 빈칸이나 기준값은 35[mm²])

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
same_core_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2002_3회_85, 2003_3회_81, 2004_1회_84, 2004_1회_91, 2004_2회_86, 2004_3회_83]
same_trap_pattern_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2002_3회_85]

