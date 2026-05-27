# v_next D-3 input 038: 전력공학 / 전력_보호고장S / 단락전류·임피던스

[문제]
id: 2003_1회_21
year: 2003
session: 1회
q_no: 21
subject: 전력공학
question_text: 3상 선로에서 회로의 상규선간전압을 \(\bar{V}_{n} [\mathrm{kV}]\) ，계통의 전원용량에 상당하는 전류를 \(I_{n}[\mathrm{~A}], V_{n}\) 과 \(I_{n}\) 을 기준으로 하여 \％로 나타낸 \％임피던스를 \(\% Z_{s}\) 라 할 때 3 상 단락 전류를 계산하는 식은？
choices:
  1. \( rac{V_r I_L}{100%Z}\)
  2. \( rac{100I_L}{%Z}\)
  3. \( rac{V_r^2}{%Z}\)
  4. \( rac{%Z_r I_L}{V_n}\)
answer: 2
solution: 3상 단락전류 계산식을 유도합니다.

**핵심 공식:**
기준값(Base) 기준으로 표현된 %임피던스와 기준전류의 관계식

**단계별 풀이:**
1) %임피던스의 정의:
\[ \%Z_s = \frac{Z \times 100}{V_n^2/S_n} = \frac{Z \times 100 \times I_n}{V_n} \]

2) 단락전류 도출:
\[ I_s = \frac{V_n}{Z} = \frac{V_n \times \%Z_s}{100 \times V_n \times I_n/I_n} = \frac{100}{\%Z_s} \times I_n \]

**정답: (2) \( I_s = \frac{100}{\%Z_s} \times I_n \)**

**오답 분석:**
- (1) \( \frac{V_n I_n}{\%Z_s} \): 차원이 맞지 않음
- (3) \( \frac{V_n^2}{\%Z_s} \): %Z_s는 이미 백분율이므로 중복
- (4) \( \frac{\%Z_s I_n}{V_n} \): 역수 관계로 잘못됨

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=단락전류; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 단락전류·임피던스
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: %Z와 기준용량을 어떻게 환산해 단락전류를 구하는가
representative_trap: 기준용량 환산 비율 함정 / %Z 기준 변경 혼동
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 기준용량 환산 비율 함정 / %Z 기준 변경 혼동
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 단락전류 -> 회로 옴의 법칙 -> 회로 임피던스 환산

[연관 문제 후보]
same_core_candidates: [2000_6회_27, 2001_2회_21, 2002_1회_30]
same_trap_pattern_candidates: [2000_6회_27, 2001_2회_21, 2002_1회_30]

