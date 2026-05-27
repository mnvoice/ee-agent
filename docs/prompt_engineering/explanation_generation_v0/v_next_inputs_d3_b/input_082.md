# v_next D-3 input 082: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 2007_1회_24
year: 2007
session: 1회
q_no: 24
subject: 전력공학
question_text: 반지름 \(0.6[\mathrm{~cm}]\) 인 경동선을 사용하는 3상 1 회선 송전선에서 선간 거리를 \(2[\mathrm{~m}]\) 로 정삼각형 배 치할 경우, 각 선의 인덕턴스는 약 몇 \([\mathrm{mH} / \mathrm{km}]\) 인가?
choices:
  1. 0.81
  2. 1.21
  3. 1.51
  4. 1.81
answer: 2
solution: **핵심 공식:**

3상 송전선로의 인덕턴스:
\[ L = 0.05 + 0.4605 \log \frac{D}{r} \text{ [mH/km]} \]

여기서:
- \(D\): 선간 거리 [m]
- \(r\): 도체 반지름 [m]

**주어진 조건:**
- 도체 반지름: \( r = 0.6 \text{ [cm]} = 0.6 \times 10^{-2} \text{ [m]} \)
- 정삼각형 배치 선간 거리: \( D = 2 \text{ [m]} \)

**계산 단계:**

정삼각형 배치에서 \( D_{12} = D_{23} = D_{31} = 2 \text{ [m]} \)이므로:

\[ L = 0.05 + 0.4605 \log \frac{2}{0.6 \times 10^{-2}} \]

\[ = 0.05 + 0.4605 \log \frac{2}{0.006} \]

\[ = 0.05 + 0.4605 \log 333.33 \]

\[ = 0.05 + 0.4605 \times 2.523 \]

\[ = 0.05 + 1.161 \]

\[ = 1.21 \text{ [mH/km]} \]

**정답:** (2) 1.21

**오답 분석:**
- (1) 0.81: 로그값 계산 오류
- (3) 1.51: 기본값 0.05를 과다 적용
- (4) 1.81: 로그 계산 시 거리 값 잘못 적용

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
same_core_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22, 2001_2회_29, 2002_3회_37, 2004_2회_24, 2005_2회_31, 2005_3회_26]
same_trap_pattern_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22]

