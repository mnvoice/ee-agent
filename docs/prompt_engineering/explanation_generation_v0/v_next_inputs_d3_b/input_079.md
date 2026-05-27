# v_next D-3 input 079: 전력공학 / 전력_설비고장 / 가공전선로 경간·이도

[문제]
id: 2006_3회_25
year: 2006
session: 3회
q_no: 25
subject: 전력공학
question_text: 송배전 선로에서 전선의 장력을 2 배로 하 고 또 경간을 2 배로 하면 전선의 이도는 처음의 몇 배 가 되는가？
choices:
  1. 1/4
  2. 1/2
  3. 2
  4. 4
answer: 2
solution: 송배전 선로에서 전선의 이도 변화를 계산하는 문제입니다.

**이도 공식:**
\[ D = \frac{WS^2}{8T} \]

여기서:
- D: 이도 [m]
- W: 단위 길이당 전선의 무게 [kg/m]
- S: 경간(지간) [m]
- T: 전선의 장력 [kg]

**초기 조건:**
- 장력: T
- 경간: S
- 초기 이도: \( D = \frac{WS^2}{8T} \)

**변화된 조건:**
- 장력: 2T (2배)
- 경간: 2S (2배)

**계산:**
\[ D' = \frac{W(2S)^2}{8(2T)} = \frac{W \times 4S^2}{8 \times 2T} = \frac{4WS^2}{16T} = \frac{1}{2} \times \frac{WS^2}{8T} \times 4 = 2 \times \frac{WS^2}{8T} = 2D \]

**결과:**
전선의 이도는 처음의 **2배**가 됩니다.

**이도 변화의 요인 분석:**
- 경간이 2배 → 이도는 4배 증가 (경간의 제곱에 비례)
- 장력이 2배 → 이도는 1/2로 감소
- 결합 효과: \( 4 \times \frac{1}{2} = 2 \)

**정답: (3) 2배**

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
same_core_candidates: [2004_1회_30, 2004_2회_25, 2004_3회_25]
same_trap_pattern_candidates: [2004_1회_30, 2004_2회_25, 2004_3회_25]

