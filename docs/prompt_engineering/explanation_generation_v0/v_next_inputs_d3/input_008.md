# v_next D-3 input 008: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 1999_4회_81
year: 1999
session: 4회
q_no: 81
subject: 전력공학
question_text: 고압 가공 전선로의 지지물로서 사용하는 목주의 풍압 하중에 대한 안전율은?
choices:
  1. 1.1 이상
  2. 1.2 이상
  3. 1.3 이상
  4. 1.5 이상
answer: 3
solution: **문제**: 고압 가공전선로의 지지물(목주)의 풍압 하중에 대한 안전율은?

**풀이**:

전기설비기술기준 제332.7조(고압 가공전선로의 지지물의 강도)에서 지지물이 목주인 경우의 안전율을 규정합니다.

**안전율 기준표**:

| 전압의 종별 | 안전율 | 비고 |
|:----------:|:-----:|:-----:|
| 저 압 | 1.2 | - |
| **고 압** | **1.3** | 말구 지름 0.12m 이상 |
| 특고압 | 1.5 | 말구 지름 0.12m 이상 |

**결론**:

고압 가공전선로의 목주는 풍압 하중에 대해 **안전율 1.3**을 적용합니다.

**정답**: 3번 (1.3)

**오답 분석**:
- (1) 3.2: 오류
- (2) 3.4: 오류  
- (4) 3.8: 오류

이들은 기술기준에 명시된 기준값이 아닙니다.

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
same_core_candidates: [1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82, 2002_3회_85, 2003_3회_81, 2004_1회_84, 2004_1회_91, 2004_2회_86, 2004_3회_83]
same_trap_pattern_candidates: [1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82, 2002_3회_85]

