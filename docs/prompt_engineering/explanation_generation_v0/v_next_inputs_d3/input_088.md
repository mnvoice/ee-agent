# v_next D-3 input 088: 전력공학 / 전력_송배전D / 코로나 / 전선 도체

[문제]
id: 2007_2회_24
year: 2007
session: 2회
q_no: 24
subject: 전력공학
question_text: 전선의 반지름 \(r[\mathrm{~m}]\) ，소도체 간의 거리 1 \([\mathrm{m}]\) ，선간 거리 \(D[\mathrm{~m}]\) 인 복도체의 인덕턴스 \(L\) 은 \(L=0.4605 P+0.025[\mathrm{mH} / \mathrm{km}]\) 이다．이 식에서 \(P\) 에 해당되는 값은？
choices:
  1. \(\log_{10}\frac{D}{\sqrt{rl}}\)
  2. \(\log_e\frac{D}{\sqrt{rl}}\)
  3. \(\log_{10}\frac{l}{\sqrt{rD}}\)
  4. \(\log_e\frac{l}{\sqrt{rD}}\)
answer: 1
solution: 복도체(Bundle conductor)의 인덕턴스를 구하는 문제로, 일반 공식에서 P에 해당하는 항을 찾는 것입니다.

**일반 n-도체 인덕턴스 공식:**
\[L_n = \frac{0.05}{n} + 0.4605 \log_{10} \frac{D}{\sqrt[n]{rl^{n-1}}} \text{ [mH/km]}\]

**복도체 적용 (n=2):**

\[L = 0.025 + 0.4605 \log_{10} \frac{D}{\sqrt{rl}}\]

비교하면:
\[L = 0.025 + 0.4605 P\]

따라서:
\[P = \log_{10} \frac{D}{\sqrt{rl}}\]

**정답: 1번** (\(\log_{10} \frac{D}{\sqrt{rl}}\))

**각 항의 의미:**
- D: 도체 간의 거리
- r: 각 도체의 반지름
- l: 소도체(bundled conductor) 간의 거리
- 0.025: 상수항 (0.05/2)
- 0.4605: 계수

**오답 분석:**
- (2) \(\log_e \frac{D}{\sqrt{rl}}\): 자연로그(밑 e) 사용 - 틀림
- (3) \(\log_{10} \frac{l}{\sqrt{rD}}\): 분자와 분모 위치 바뀜 - 틀림
- (4) \(\log_e \frac{l}{\sqrt{rD}}\): 자연로그 + 위치 바뀜 - 틀림

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=복도체; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 코로나 / 전선 도체
star: null
ds_class: D
phenomenon_origin: D/Dynamic
six_axis: []
essence_question: 전선 표면 전계와 도체 손실이 어떻게 작용하는가
representative_trap: 코로나 임계전압 vs 정격 전압 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 코로나 임계전압 vs 정격 전압 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 코로나/표피효과 -> 회로 분포정수 -> 회로 임피던스

[연관 문제 후보]
same_core_candidates: [2000_4회_23, 2002_3회_21]
same_trap_pattern_candidates: [2000_4회_23, 2002_3회_21]

