# v_next D-3 input 004: 전력공학 / 전력_송배전D / 분포정수 송전

[문제]
id: 1998_4회_23
year: 1998
session: 4회
q_no: 23
subject: 전력공학
question_text: 선로의 특성 임피던스는？
choices:
  1. 선로의 길이가 길어질수록 같아 커진다.
  2. 선로의 길이가 길어질수록 같아 작아진다.
  3. 선로의 길이보다는 부하전력에 따라 같아 변한다.
  4. 선로의 길이에 관계없이 일정하다.
answer: 4
solution: 선로의 특성 임피던스(Characteristic Impedance)의 성질을 판별하는 문제입니다.

**특성 임피던스 공식:**

\[Z_0 = \sqrt{\frac{Z}{Y}} = \sqrt{\frac{R + j\omega L}{G + j\omega C}}\]

여기서:
- \(R\): 저항 (단위 길이당)
- \(L\): 인덕턴스 (단위 길이당)
- \(G\): 컨덕턴스 (단위 길이당)
- \(C\): 정전용량 (단위 길이당)

**핵심 분석:**

일반적으로 송전 선로에서 저항과 컨덕턴스 값은 매우 작으므로 무시할 수 있습니다:

\[Z_0 ≈ \sqrt{\frac{L}{C}}\]  (근사식)

**중요한 점:**
- \(L\)(단위 길이당 인덕턴스)과 \(C\)(단위 길이당 정전용량)은 **선로의 기하학적 구조**(도체 반경, 도체 간 거리)에만 의존
- **선로의 길이와는 무관**

**정답: (4) 선로의 길이보다는 부하전력에 따라 값이 변한다** (또는 길이에 무관)

오답 분석:
- (1), (2): 길이와 특성 임피던스는 무관
- (3): 부하전력과도 무관 (선로 자체의 물리적 특성)

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=특성 임피던스; audit_group=expansion

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
same_core_candidates: [2003_1회_62, 2004_3회_23, 2005_1회_21, 2005_2회_30, 2007_1회_62]
same_trap_pattern_candidates: [2003_1회_62, 2004_3회_23, 2005_1회_21, 2005_2회_30, 2007_1회_62]

