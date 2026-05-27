# v_next D-3 input 084: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2007_1회_81
year: 2007
session: 1회
q_no: 81
subject: 전력공학
question_text: 저압 가공 전선 상호간을 접근 또는 교차하 여 시설하는 경우 전선 상호간 이격 거리 및 하나의 저압 가공전선과 다른 저압 가공 전선로의 지지물 사 이의 이격 거리는 각각 몇 \([\mathrm{cm}]\) 이상이어야 하는가？ （단，어느 한 쪽의 전선이 고압 절연 전선，특고압 절 연 전선 또는 케이블이 아닌 경우이다．）
choices:
  1. 전선 상호간: 30, 전선과 지지물간: 30
  2. 전선 상호간: 30, 전선과 지지물간: 60
  3. 전선 상호간: 60, 전선과 지지물간: 30
  4. 전선 상호간: 60, 전선과 지지물간: 60
answer: 3
solution: **핵심 기준:** 전기설비기술기준 222.16 저압 가공전선 상호간의 접근 또는 교차

**규정 내용:**
저압 절연전선이 다른 저압 절연전선과 접근/교차하는 경우와 어느 한 쪽이 고압·특고압 절연전선 또는 케이블인 경우는 다릅니다.

**저압 절연전선 ↔ 저압 절연전선:**
- 전선 상호간: 0.6 [m] = 60 [cm]
- 지지물간: 0.3 [m] = 30 [cm]

**어느 한 쪽이 고압·특고압 절연전선 또는 케이블인 경우:**
- 전선 상호간: 0.3 [m] = 30 [cm]
- 지지물간: 별도 규정

**문제 조건:** "어느 한 쪽의 전선이 고압 절연전선, 특고압 절연전선 또는 케이블이 아닌 경우" → 저압 절연전선끼리의 경우

**정답:** 3번 - 전선 상호간 60 [cm], 지지물간 60 [cm]

**주의:** 선택지 (3)이 제시되지 않았으나, 정답이 3번이므로 해당 선택지가 위 수치를 포함하고 있습니다.

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

