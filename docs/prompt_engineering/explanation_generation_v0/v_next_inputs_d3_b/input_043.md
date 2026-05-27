# v_next D-3 input 043: 전력공학 / 전력_송배전D / 분포정수 송전

[문제]
id: 2003_1회_62
year: 2003
session: 1회
q_no: 62
subject: 전력공학
question_text: 수전단 개방시의 무손실 선로에 있어서 입 력 임피던스의 절대값을 특성 임피던스와 같게 하려 면 선로의 길이를 파장의 몇 배로 하면 되는가？
choices:
  1. \(\frac{1}{8} \lambda\)
  2. \(\frac{1}{6} \lambda\)
  3. \(\frac{1}{4} \lambda\)
  4. \(\frac{1}{2} \lambda\)
answer: 3
solution: **핵심 공식:**

수전단 개방시 입력 임피던스:
\[Z_{in} = Z_0 \coth(\gamma l)\]

무손실 선로에서:
- \(\gamma = j\beta = j\frac{2\pi}{\lambda}\)
- \(Z_0 = \sqrt{\frac{L}{C}}\) (특성 임피던스)
- \(\coth(jx) = -j\cot(x)\)

**단계별 계산:**

1) 무손실 선로이므로 입력 임피던스:
\[Z_{in} = Z_0 \coth(j\beta l) = -jZ_0 \cot(\beta l)\]

2) 임피던스의 절대값이 특성 임피던스와 같다는 조건:
\[|Z_{in}| = Z_0\]

3) 따라서:
\[|Z_0 \cot(\beta l)| = Z_0\]
\[|\cot(\beta l)| = 1\]
\[\cot(\beta l) = \pm 1\]

4) 양의 조건에서 \(\cot(\beta l) = 1\)일 때:
\[\beta l = \frac{\pi}{4}\]

5) \(\beta = \frac{2\pi}{\lambda}\)를 대입:
\[\frac{2\pi}{\lambda} \cdot l = \frac{\pi}{4}\]

6) 선로 길이 계산:
\[l = \frac{\pi}{4} \times \frac{\lambda}{2\pi} = \frac{\lambda}{8}\]

**정답: (1) \(\frac{1}{8}\lambda\)**

**설명:**
수전단 개방 조건에서 입력 임피던스의 절대값이 특성 임피던스와 일치하려면 선로 길이가 파장의 1/8배여야 합니다. 이는 임피던스 정합(matching) 조건 중 하나입니다.

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
same_core_candidates: [1998_4회_23, 2004_3회_23, 2005_1회_21, 2005_2회_30, 2007_1회_62]
same_trap_pattern_candidates: [1998_4회_23, 2004_3회_23, 2005_1회_21, 2005_2회_30, 2007_1회_62]

