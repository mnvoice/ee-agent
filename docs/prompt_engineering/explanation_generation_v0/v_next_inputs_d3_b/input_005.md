# v_next D-3 input 005: 전력공학 / 전력_함정S / 부하율·수용률·부등률

[문제]
id: 1998_4회_25
year: 1998
session: 4회
q_no: 25
subject: 전력공학
question_text: 154/6.6 [kV], 5000 [kVA]의 3상 변압기 1대를 시설한 변전소가 있다. 이 변전소의 6.6 [kV] 차 배전선에 접속한 부하 설비 및 수용률이 표와 같고 각 배전선간의 부등률을 1.17로 하였을 때 변전소에 접하는 최대 전력은 약 몇 [kW]인가?
choices:
  1. 4186
  2. 4356
  3. 4598
  4. 4728
answer: 3
solution: 변전소에 걸리는 최대 전력을 구하는 문제입니다.

**주어진 데이터:**
- 변압기 용량: 5000 kVA (전압: 154/6.6 kV)
- 4개 배전선 부하 설비 및 수용률
- 배전선간 부등률: 1.17

**계산 절차:**

**Step 1: 각 배전선의 최대 수요 전력 계산**

각 배전선 최대 전력 = 부하 설비 × 수용률

- a선: 4716 × 0.24 = 1,131.84 kW
- b선: 1,635 × 0.74 = 1,209.90 kW
- c선: 3,600 × 0.48 = 1,728 kW
- d선: 4,095 × 0.32 = 1,310.40 kW

**Step 2: 합계 전력**
\[P_{합} = 1,131.84 + 1,209.90 + 1,728 + 1,310.40 = 5,380.14 \text{ kW}\]

**Step 3: 부등률을 적용한 최대 전력**

부등률의 정의:
\[부등률 = \frac{각 선의 최대 전력의 합}{동시에 나타나는 최대 전력}\]

따라서 동시에 나타나는 최대 전력:
\[P_{max} = \frac{P_{합}}{부등률} = \frac{5,380.14}{1.17} ≈ 4,598 \text{ kW}\]

**정답: (3) 4598 kW**

**개념 설명:**
- **수용률**: 설치된 부하가 실제로 사용하는 비율
- **부등률**: 모든 배전선이 동시에 최대값을 나타내지 않음을 반영하는 계수 (>1)
- 부등률이 클수록 각 선의 사용 시간이 겹치지 않음을 의미

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=수용률; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 부하율·수용률·부등률
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 부하율/수용률/부등률을 어떻게 구분해 외우는가
representative_trap: 부하율 vs 수용률 vs 부등률 정의 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 부하율 vs 수용률 vs 부등률 정의 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: [1999_6회_24, 2008_1회_25]
same_trap_pattern_candidates: [1999_6회_24, 2008_1회_25]

