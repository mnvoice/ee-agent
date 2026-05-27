# v_next D-3 input 083: 전력공학 / 전력_송배전D / 분포정수 송전

[문제]
id: 2007_1회_62
year: 2007
session: 1회
q_no: 62
subject: 전력공학
question_text: 전송 선로의 특성 임피던스가 \(50[\Omega]\) 이고 부하 저항이 \(150[\Omega]\) 이면 부하에서의 반사 계수는 얼마인가？
choices:
  1. 0
  2. 0.5
  3. 0.7
  4. 1
answer: 2
solution: **핵심 공식:**
전송 선로에서 부하의 반사계수는

\[\rho = \frac{Z_L - Z_0}{Z_L + Z_0}\]

여기서:
- $Z_L$ = 부하 임피던스
- $Z_0$ = 특성 임피던스

**풀이 단계:**

1) 주어진 값:
   - 특성 임피던스: $Z_0 = 50\text{ }[\Omega]$
   - 부하 저항: $Z_L = 150\text{ }[\Omega]$

2) 반사계수 계산:
   \[\rho = \frac{150 - 50}{150 + 50} = \frac{100}{200} = 0.5\]

**정답: (2) 0.5**

**오답 분석:**
- (1) 0: 부하가 특성 임피던스와 정합할 때(정합 조건)
- (3) 0.7: 계산 오류
- (4) 1: 부하가 단절(개방)되었을 때

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=특성 임피던스; audit_group=expansion

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
same_core_candidates: [1998_4회_23, 2003_1회_62, 2004_3회_23, 2005_1회_21, 2005_2회_30]
same_trap_pattern_candidates: [1998_4회_23, 2003_1회_62, 2004_3회_23, 2005_1회_21, 2005_2회_30]

