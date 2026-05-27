# v_next D-3 input 052: 전력공학 / 전력_송배전D / 전압강하·전력손실

[문제]
id: 2004_2회_31
year: 2004
session: 2회
q_no: 31
subject: 전력공학
question_text: 배전선의 전력손실 경감 대책이 아닌 것은？
choices:
  1. 43.7
  2. 47.7
  3. 53.7
  4. 59.7
answer: 2
solution: 송전선로의 전력손실은 다음 공식으로 계산됩니다:

**핵심 공식:**
\[ P_l = I^2 R = \frac{P^2 R}{V^2 \cos^2\phi} \]

전력손실률(k)은:
\[ k(\%) = \frac{P_l}{P} \times 100 = \frac{P \cdot R}{V^2 \cos^2\phi} \times 100 \]

**풀이 단계:**
1. 주어진 송전전압, 송전전력, 선로저항, 역률을 파악
2. 선로전류 계산: \( I = \frac{P}{\sqrt{3}V\cos\phi} \)
3. 전력손실 계산: \( P_l = I^2 R \)
4. 전력손실률 계산: \( k = \frac{P_l}{P} \times 100(\%) \)

**주의사항:**
- 3상 송전의 경우 \(\sqrt{3}\) 항 포함
- 역률이 낮을수록 손실 증가
- 송전전압이 높을수록 손실 감소 (V²에 반비례)

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
same_core_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2005_1회_28, 2005_2회_23, 2006_1회_2, 2006_1회_28, 2008_1회_29]
same_trap_pattern_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2005_1회_28]

