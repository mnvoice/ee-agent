# v_next D-3 input 080: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2006_3회_81
year: 2006
session: 3회
q_no: 81
subject: 전력공학
question_text: 사용 전압이 몇 \([\mathrm{kV}]\) 를 넘는 특고압 가공전 선과 가공 약전류 전선 등은 동일 지지물에 시설하여 서는 아니 되는가?
choices:
  1. 6.6
  2. 22.9
  3. 30
  4. 35
answer: 4
solution: **핵심 기준:**

전기설비기술기준 제333.19조에서 규정하는 특고압 가공전선과 가공약전류전선 등의 공용설치 기준입니다.

**규정 내용:**

사용전압이 **35[kV]를 초과하는** 특고압 가공전선과 가공약전류전선, 안테나 등은 동일 지지물에 시설하여서는 안 됩니다.

**오답 분석:**
- (1) 6.6[kV]: 고압 범위 → 조건 미해당
- (2) 22.9[kV]: 특고압이나 35[kV] 이하 → 조건 미해당
- (3) 30[kV]: 35[kV] 이하 → 조건 미해당
- (4) **35[kV] 초과**: 정답 → 동일 지지물 설치 금지

**정답: (4) 35[kV]를 초과하는 경우**

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

