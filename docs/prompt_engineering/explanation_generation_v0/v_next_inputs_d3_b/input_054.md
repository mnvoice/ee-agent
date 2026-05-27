# v_next D-3 input 054: 전력공학 / 전력_송배전D / 분포정수 송전

[문제]
id: 2004_3회_23
year: 2004
session: 3회
q_no: 23
subject: 전력공학
question_text: 3상 3선식 송전선에서 \(L\) 을 작용 인덕턴스 라 하고 \(L_{m}\) 및 \(L_{e}\) 는 대지를 귀로로 하는 1선의 자 기 인덕턴스 및 상호 인덕턴스라고 할 때 이들 사이 의 관계식은?
choices:
  1. \(L = L_m - L_c\)
  2. \(L = L_c - L_m\)
  3. \(L = L_m + L_c\)
  4. \(L = \frac{L_m}{L_c}\)
answer: 1
solution: 3상 3선식 송전선로에서 작용 인덕턴스(working inductance)는 송전선과 대지 간의 자기 인덕턴스 성분을 고려한 개념입니다.

**핵심 개념:**

송전선의 인덕턴스는 다음과 같이 구성됩니다:
- **자기 인덕턴스(\(L_m\))**: 대지를 귀로로 하는 1선의 자기적 특성
- **상호 인덕턴스(\(L_e\))**: 대지를 귀로로 하는 다른 상들과의 상호 유도 성분

**작용 인덕턴스 정의:**

3상 3선식에서 한 상의 작용 인덕턴스는 자기 인덕턴스에서 상호 인덕턴스를 뺀 값입니다:
\[L = L_m - L_e\]

이는 실제 송전선에서 전류가 흐를 때 경험하는 유효한 인덕턴스를 나타냅니다. 대지를 귀로로 하는 3상 송전에서 상호 인덕턴스의 영향을 제거하여 순수한 작용 인덕턴스를 얻습니다.

**정답:** **(1)번** 
\[L = L_m - L_e\]

**오답 이유:**
- (2) \(L_e - L_m\): 부호 반대
- (3) \(L_m + L_e\): 덧셈은 정전용량에서 사용
- (4) \(L_m/L_e\): 비율 관계가 아님

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=작용인덕턴스; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 분포정수 송전
star: null
ds_class: D
phenomenon_origin: D/Dynamic
six_axis: []
essence_question: 송전선을 분포정수 모델로 어떻게 표현하는가
representative_trap: 집중정수 vs 분포정수 모델 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 집중정수 vs 분포정수 모델 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 분포정수 -> 회로 분포정수 -> 회로 4단자망

[연관 문제 후보]
same_core_candidates: [1998_4회_23, 2003_1회_62, 2005_1회_21, 2005_2회_30, 2007_1회_62]
same_trap_pattern_candidates: [1998_4회_23, 2003_1회_62, 2005_1회_21, 2005_2회_30, 2007_1회_62]

