# v_next D-3 input 075: 전력공학 / 전력_함정S / 역률 개선

[문제]
id: 2006_2회_26
year: 2006
session: 2회
q_no: 26
subject: 전력공학
question_text: 역률 0．6，출력 480 ［kW］인 부하에 병렬를 용량 400 ［kVA］의 전력용 콘덴서를 설치하면 합성 역률은 어느 정도로 개선되는가？
choices:
  1. 0.75
  2. 0.86
  3. 0.89
  4. 0.94
answer: 2
solution: 역률 개선용 콘덴서 설치 후 합성 역률을 구하는 문제입니다.

**주어진 조건:**
- 부하 출력: \(W = 480\) kW
- 부하 역률: \(\cos\theta_1 = 0.6\) (지상)
- 콘덴서 용량: \(Q_c = 400\) kVAr

**풀이 과정:**

**1단계: 부하의 무효전력 계산**

부하 역률이 0.6일 때:
\(\sin\theta_1 = \sqrt{1 - \cos^2\theta_1} = \sqrt{1 - 0.36} = 0.8\)

부하의 무효전력:
\[Q_1 = W \tan\theta_1 = W \cdot \frac{\sin\theta_1}{\cos\theta_1} = 480 \times \frac{0.8}{0.6} = 640 \text{ kVAr}\]

**2단계: 콘덴서 설치 후 합성 무효전력**

콘덴서는 무효전력을 감소시킵니다:
\[Q_2 = Q_1 - Q_c = 640 - 400 = 240 \text{ kVAr}\]

**3단계: 합성 역률 계산**

합성 역률:
\[\cos\theta_2 = \frac{W}{\sqrt{W^2 + Q_2^2}} = \frac{480}{\sqrt{480^2 + 240^2}} = \frac{480}{\sqrt{230400 + 57600}} = \frac{480}{\sqrt{288000}}\]

\[= \frac{480}{536.66} = 0.894 \approx 0.89\]

또는:
\[\cos\theta_2 = \frac{480}{\sqrt{480^2 + 240^2}} = \frac{480}{480\sqrt{1 + 0.25}} = \frac{1}{\sqrt{1.25}} = 0.8944\]

**정답: (3) 0.89**

**오답 이유:**
- (1) 0.75: 계산 오류
- (2) 0.86: 불완전한 개선
- (4) 0.94: 과도한 값

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=16; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=question_text; matched_keyword=전력용 콘덴서; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 역률 개선
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 역률 개선 콘덴서 용량을 어떻게 계산하는가
representative_trap: Qc 공식 sin / cos 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: Qc 공식 sin / cos 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: []
same_trap_pattern_candidates: []

