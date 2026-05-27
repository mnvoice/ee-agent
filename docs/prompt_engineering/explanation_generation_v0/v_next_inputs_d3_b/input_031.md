# v_next D-3 input 031: 전력공학 / 전력_보호고장S / 단락전류·임피던스

[문제]
id: 2002_1회_30
year: 2002
session: 1회
q_no: 30
subject: 전력공학
question_text: 기준 용량 \(P[\mathrm{kVA}] . V[\mathrm{kV}]\) 일 때 \％임피던 스값이 \(Z_{P}\) 인 것을 기준용량 \(P_{1}[\mathrm{kVA}], V_{1}[\mathrm{kV}]\) 로 기 준값을 변환하면 새로운 기준값에 대한 \％임피던스 값 \(Z_{P 1}\) 은？
choices:
  1. \(Z_{n1} = \frac{P_1}{P} \times \left(\frac{V}{V_1}\right)^2 Z_n\)
  2. \(Z_{n1} = \frac{P_1}{P} \times \frac{V}{V_1} Z_n\)
  3. \(Z_{n1} = \frac{P_1}{P} \times \left(\frac{V_1}{V}\right)^2 Z_n\)
  4. \(Z_{n1} = \frac{P_1}{P} \times \frac{V_1}{V} Z_n\)
answer: 3
solution: 기준 용량 변환에 따른 %임피던스 변환 문제입니다.

**핵심 공식:**
%임피던스의 정의:
\[
Z_P = \frac{Z \cdot P}{10V^2} \quad \text{[%]}
\]

여기서:
- \(Z\): 실제 임피던스 [Ω]
- \(P\): 기준 용량 [kVA]
- \(V\): 기준 전압 [kV]

**풀이:**

기준값 (P, V)에서의 %임피던스:
\[
Z_P = \frac{Z \cdot P}{10V^2}
\]

새로운 기준값 (P₁, V₁)에서의 %임피던스:
\[
Z_{P1} = \frac{Z \cdot P_1}{10V_1^2}
\]

두 식의 비를 구하면:
\[
\frac{Z_{P1}}{Z_P} = \frac{\frac{Z \cdot P_1}{10V_1^2}}{\frac{Z \cdot P}{10V^2}} = \frac{P_1}{P} \cdot \frac{V^2}{V_1^2}
\]

따라서 새로운 기준값에 대한 %임피던스 값은:
\[
Z_{P1} = Z_P \cdot \frac{P_1}{P} \cdot \left(\frac{V}{V_1}\right)^2
\]

또는 정리하면:
\[
Z_{P1} = \left(\frac{V}{V_1}\right)^2 \cdot \frac{P_1}{P} \cdot Z_P
\]

**정답: (1)** 
\[
Z_{P1} = \left(\frac{V}{V_1}\right)^2 \cdot \frac{P_1}{P} \cdot Z_P
\]

**적용 예:**
- 기준용량이 커지면(P₁ > P): Z_{P1} 증가
- 기준전압이 올라가면(V₁ > V): Z_{P1} 감소
- 이는 높은 전압의 시스템에서 임피던스가 상대적으로 작게 표현되는 현상을 반영합니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=기준용량; audit_group=expansion

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
same_core_candidates: [2000_6회_27, 2001_2회_21, 2003_1회_21]
same_trap_pattern_candidates: [2000_6회_27, 2001_2회_21, 2003_1회_21]

