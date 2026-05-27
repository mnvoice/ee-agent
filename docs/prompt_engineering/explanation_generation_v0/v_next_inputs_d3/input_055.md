# v_next D-3 input 055: 전력공학 / 전력_설비고장 / 가공전선로 경간·이도

[문제]
id: 2004_3회_25
year: 2004
session: 3회
q_no: 25
subject: 전력공학
question_text: 송전선로에 있어서 장경간(long span)이 라고 하는 것은 표준경간에 몇 \([\mathrm{m}]\) 를 더한 경간을 넘 는 것을 말하는가?
choices:
  1. 100
  2. 150
  3. 200
  4. 250
answer: 4
solution: 송전선로의 경간 분류에서 장경간(long span)의 정의입니다.

**핵심 정의:**

송전선로의 경간(span) 분류:
- **표준경간(standard span)**: 기본 설계 경간 (일반적으로 약 250~300m)
- **단경간(short span)**: 표준경간보다 짧은 경간
- **장경간(long span)**: 표준경간에 일정 거리를 더한 경간을 초과

**장경간의 정의:**
\[\text{장경간} > \text{표준경간} + 250[m]\]

즉, 표준경간에 250m를 더한 경간을 넘는 것을 장경간이라 합니다.

**실무적 의의:**
- 장경간은 지형이 가파르거나 넓은 지역을 통과할 때 사용
- 경간이 길어질수록 처짐(sag), 진동, 강도 고려 필요
- 설계 시 선재 굵기, 내압성 등을 더 강화해야 함

**보기 분석:**
- (1) 100m: 너무 짧음
- (2) 150m: 일반적 추가 거리 아님
- (3) 200m: 표준 정의보다 짧음
- (4): 250m이 정답

**정답:** **(4)번** (표준경간 + 250[m] 이상)

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=경간; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 가공전선로 경간·이도
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 전선 장력·이도·경간이 어떻게 작용하는가
representative_trap: 경간 vs 이도 관계 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 경간 vs 이도 관계 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: [2004_1회_30, 2004_2회_25, 2006_3회_25]
same_trap_pattern_candidates: [2004_1회_30, 2004_2회_25, 2006_3회_25]

