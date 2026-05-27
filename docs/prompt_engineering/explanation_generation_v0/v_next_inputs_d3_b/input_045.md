# v_next D-3 input 045: 전력공학 / 전력_설비고장 / 가공전선로 경간·이도

[문제]
id: 2004_1회_30
year: 2004
session: 1회
q_no: 30
subject: 전력공학
question_text: 가공 송전 선로를 가선할 때에는 하중 조 건과 온도 조건을 고려하여 적당한 이도(dip)를 주도 록 하여야 한다. 다음 중 이도에 대한 설명으로 옳은 것은?
choices:
  1. 구분점수
  2. 리률로지
  3. 써지널라이저
  4. 구분개폐기
answer: 4
solution: 가공 송전선로의 이도(Dip, Sag)에 관한 개념 문제입니다.

**이도의 정의:**
전선의 양쪽 지지점을 연결하는 수평선으로부터 전선이 아래로 처진 길이

**각 보기 검토:**

**(1) 이도가 작으면 전선이 좌우로 흔들린다 → ❌ 오답**
- 이도가 **크면** 장력이 작아져 좌우 진동이 커짐
- 이도가 작으면 장력이 커져 진동이 감소

**(2) 전선을 팽팽하게 가선하는 것을 이도를 크게 준다 → ❌ 오답**
- 반대: 팽팽하게 가선 = 이도를 **작게** 줌
- 느슨하게 가선 = 이도를 **크게** 줌

**(3) 이도를 작게 하면 전선의 장력이 증가하고 극단적으로 전선이 꼬인다 → ✓ 정답**
\[ T = \frac{W L^2}{8d} \]
이도 d가 감소하면 장력 T는 증가합니다. 과도한 장력은 전선 손상 및 단선 위험

**이도의 올바른 이해:**
- 이도가 너무 **크면**: 진동↑, 다른 상 전선 접촉 위험, 지지물 높이↑
- 이도가 너무 **작으면**: 장력↑, 단선 위험, 절약적(낮은 지지물)

**정답:** (4) - 위 설명 (3)의 내용이 정답

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=이도; audit_group=non_expansion_metadata

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
same_core_candidates: [2004_2회_25, 2004_3회_25, 2006_3회_25]
same_trap_pattern_candidates: [2004_2회_25, 2004_3회_25, 2006_3회_25]

