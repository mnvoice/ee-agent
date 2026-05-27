# v_next D-3 input 071: 전력공학 / 전력_송배전D / 전압강하·전력손실

[문제]
id: 2006_1회_28
year: 2006
session: 1회
q_no: 28
subject: 전력공학
question_text: 3상 선로의 전압이 \(V[\mathrm{~V}]\) 이고，\(P[\mathrm{~W}]\) ，역를 \(\cos \theta\) 인 부하에서 한 선의 저항이 \(R[\Omega]\) 이라면 이3 상 선로의 전체 전력손실은 몇 \([\mathrm{W}]\) 가 되겠는가？
choices:
  1. \(\frac{PR}{\sqrt{3}V^2\cos^2\theta}\)
  2. \(\frac{P^2R^2}{V^2\cos^2\theta}\)
  3. \(\frac{PR^2}{V\cos\theta}\)
  4. \(\frac{P^2R}{V^2\cos\theta}\)
answer: 4
solution: **핵심 개념**: 3상 송전선의 전력손실 계산

**주어진 정보**
- 3상 선로 전압: 
\[ V \ [\mathrm{V}] \]
- 전송 전력: 
\[ P \ [\mathrm{W}] \]
- 역률(power factor): 
\[ \cos\theta \]
- 한 선의 저항: 
\[ R \ [\Omega] \]

**풀이 단계**

1) 3상 전력 공식으로부터 선전류 구하기:
\[ P = \sqrt{3}VI\cos\theta \]

따라서 선전류:
\[ I = \frac{P}{\sqrt{3}V\cos\theta} \]

2) 3상 전력손실 계산:

각 상에서 손실: 
\[ P_{\text{상}} = I^2R \]

3상 전체 손실:
\[ P_l = 3I^2R \]

3) I 값 대입:
\[ P_l = 3 \times \left(\frac{P}{\sqrt{3}V\cos\theta}\right)^2 \times R \]

\[ P_l = 3 \times \frac{P^2}{3V^2\cos^2\theta} \times R = \frac{P^2R}{V^2\cos^2\theta} \ [\mathrm{W}] \]

**정답**: (4) 
\[ \frac{P^2R}{V^2\cos^2\theta} \ [\mathrm{W}] \]

**오답 분석**
- (1): 분모에 
\( \sqrt{3} \) 불필요
- (2): R²는 오류 (R만 사용)
- (3): V가 분자에 있고 R²는 오류

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=전력손실; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 전압강하·전력손실
star: null
ds_class: D
phenomenon_origin: D/Dynamic
six_axis: []
essence_question: 송전 거리·전류·임피던스가 전압강하에 어떻게 작용하는가
representative_trap: 단상 vs 3상 전압강하 공식 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 단상 vs 3상 전압강하 공식 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 전압강하/손실 -> 회로 임피던스 -> 회로 옴의 법칙

[연관 문제 후보]
same_core_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31, 2005_1회_28, 2005_2회_23, 2006_1회_2, 2008_1회_29]
same_trap_pattern_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31]

