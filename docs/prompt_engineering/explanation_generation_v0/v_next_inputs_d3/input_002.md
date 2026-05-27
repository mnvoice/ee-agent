# v_next D-3 input 002: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 1998_4회_21
year: 1998
session: 4회
q_no: 21
subject: 전력공학
question_text: 송전 선로의 정상，역상 및 영상 임피던스 를 각각 \(Z_{1}, Z_{2}\) 및 \(Z_{0}\) 라 하면 다음 어떤 관계가 성 립하는가？
choices:
  1. \(Z_{1}=Z_{2}=Z_{0}\)
  2. \(Z_{1}=Z_{2}>Z_{0}\)
  3. \(Z_{1}>Z_{2}=Z_{0}\)
  4. \(Z_{1}=Z_{2}<Z_{0}\)
answer: 4
solution: 송전 선로의 정상(正相), 역상(逆相), 영상(零相) 임피던스 관계를 파악하는 문제입니다.

**핵심 개념:**
- 정상 임피던스와 역상 임피던스: 송전 선로는 정지 회로(對稱 회로)이므로 구조가 동일하여 
\(Z_1 = Z_2\)

- 영상 임피던스: 
\[Z_0 = Z + 3Z_n\]
여기서 
\(Z\)는 정상 임피던스, 
\(Z_n\)은 중성점 접지 임피던스

**크기 비교:**
- 영상 임피던스는 정상분의 약 3~4배 수준
- 따라서 
\(Z_0 > Z_1 = Z_2\)
즉, 
\(Z_1 = Z_2 < Z_0\)

**정답: (4) 
\(Z_1 = Z_2 < Z_0\)**

**오답 분석:**
- (1), (3): 정상과 역상이 다르다는 것은 오류 (대칭 회로)
- (2): 영상 임피던스가 더 크므로 오류

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=송전선; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 송전 용량/거리
star: null
ds_class: D
phenomenon_origin: D/Dynamic
six_axis: []
essence_question: 송전 거리와 전압이 송전 용량에 어떻게 작용하는가
representative_trap: 송전 전압급 단위 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 송전 전압급 단위 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 송전용량 -> 회로 4단자망 -> 회로 분포정수

[연관 문제 후보]
same_core_candidates: [1998_2회_23, 1999_6회_23, 2000_6회_21, 2001_1회_22, 2001_2회_29, 2002_3회_37, 2004_2회_24, 2005_2회_31, 2005_3회_26, 2007_1회_24]
same_trap_pattern_candidates: [1998_2회_23, 1999_6회_23, 2000_6회_21, 2001_1회_22, 2001_2회_29]

