# v_next D-3 input 066: 전력공학 / 전력_송배전D / 분포정수 송전

[문제]
id: 2005_2회_30
year: 2005
session: 2회
q_no: 30
subject: 전력공학
question_text: 송전선로의 특성 임피던스를 \(Z_{0}[\Omega]\) ，전파 정수를 \(\alpha\) 라 할 때，이 선로의 직렬 임피던스는 어떻 게 표현되는가？
choices:
  1. Zc·α
  2. Zc/α
  3. α/Zc
  4. 1/Zcα
answer: 1
solution: 송전선로의 직렬 임피던스를 특성 임피던스와 전파 정수로 표현하는 문제입니다.

**핵심 공식:**

- 특성 임피던스: \(Z_0 = \sqrt{\frac{Z}{Y}}\)
- 전파 정수(전파상수): \(\gamma = \alpha + j\beta = \sqrt{Z \cdot Y}\)

여기서 \(\alpha\)는 감쇠상수, \(\beta\)는 위상상수입니다.

**단계별 풀이:**

1) 특성 임피던스와 전파 정수의 관계식:
\[Z_0 \cdot \gamma = \sqrt{\frac{Z}{Y}} \cdot \sqrt{Z \cdot Y}\]

2) 근호 성질을 이용한 정리:
\[Z_0 \cdot \gamma = \sqrt{\frac{Z}{Y} \cdot Z \cdot Y} = \sqrt{Z^2} = Z\]

3) 따라서 직렬 임피던스:
\[Z = Z_0 \cdot \gamma\]

만약 문제에서 \(\alpha\)만을 의미한다면, 전파 정수의 실수부이므로:
\[Z ≈ Z_0 \cdot \alpha\] (저손실 선로 근사)

**정답:** (1) \(Z_0 \cdot \gamma\) 또는 \(Z_0 \cdot \alpha\)

**오답 이유:**
- (2) \(\frac{Z_0}{\alpha}\): 역수 관계, 오류
- (3) \(\frac{\alpha}{Z_0}\): 불가능한 관계식
- (4) \(\frac{1}{Z_0\alpha}\): 어드미턴스와 혼동

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
same_core_candidates: [1998_4회_23, 2003_1회_62, 2004_3회_23, 2005_1회_21, 2007_1회_62]
same_trap_pattern_candidates: [1998_4회_23, 2003_1회_62, 2004_3회_23, 2005_1회_21, 2007_1회_62]

