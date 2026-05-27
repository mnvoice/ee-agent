# v_next D-3 input 061: 전력공학 / 전력_송배전D / 분포정수 송전

[문제]
id: 2005_1회_21
year: 2005
session: 1회
q_no: 21
subject: 전력공학
question_text: 전파 정수 \(\gamma\) ，특성 임피던스 \(Z_{0}\) ，길이 \(l\) 인 분포 정수 회로가 있다．수전단에 이 선로의 특성 임 피던스와 같은 임피던스 \(Z_{0}\) 를 부하로 접속하였을 때 송전단에서 부하측을 본 임피던스는？
choices:
  1. Z₀
  2. 1/Z₀
  3. Z₀ tanh γ l
  4. Z₀ coth γ l
answer: 1
solution: 분포 정수 회로에서 부하 임피던스가 특성 임피던스 Z₀와 같을 때의 송전단 임피던스를 구하는 문제입니다.

**핵심 개념:**
분포 정수 회로의 송전단 임피던스 공식은 다음과 같습니다:
\[ Z_{in} = Z_0 \frac{Z_L \cosh(\gamma l) + Z_0 \sinh(\gamma l)}{Z_0 \cosh(\gamma l) + Z_L \sinh(\gamma l)} \]

**풀이 단계:**
1) 부하 임피던스 Z_L = Z₀ (문제 조건)
2) 위 공식에 Z_L = Z₀를 대입하면:
\[ Z_{in} = Z_0 \frac{Z_0 \cosh(\gamma l) + Z_0 \sinh(\gamma l)}{Z_0 \cosh(\gamma l) + Z_0 \sinh(\gamma l)} \]
3) 분자와 분모에서 Z₀를 인수분해하면:
\[ Z_{in} = Z_0 \frac{\cosh(\gamma l) + \sinh(\gamma l)}{\cosh(\gamma l) + \sinh(\gamma l)} = Z_0 \]

**물리적 의미:**
부하가 특성 임피던스와 같으면 선로가 무한장 선로처럼 작용하여 반사파가 발생하지 않으므로, 송전단에서 본 임피던스는 특성 임피던스와 동일합니다.

**정답: ① Z₀**

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=분포정수; audit_group=expansion

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
same_core_candidates: [1998_4회_23, 2003_1회_62, 2004_3회_23, 2005_2회_30, 2007_1회_62]
same_trap_pattern_candidates: [1998_4회_23, 2003_1회_62, 2004_3회_23, 2005_2회_30, 2007_1회_62]

