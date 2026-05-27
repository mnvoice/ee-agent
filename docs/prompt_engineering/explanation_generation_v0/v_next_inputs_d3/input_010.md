# v_next D-3 input 010: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 1999_6회_23
year: 1999
session: 6회
q_no: 23
subject: 전력공학
question_text: 3상 3선식 1회선의 가공 송전선로에서 \(\bar{D}\) 를 선간거리，\(r\) 을 전선의 반지름이라고 하면 1선당 정전용량 \(C\) 는？
choices:
  1. \(\log_{10}\frac{D}{r}\)에 비례한다.
  2. \(\log_{10}\frac{D}{r}\)에 반비례한다.
  3. \(\frac{D}{r}\)에 비례한다.
  4. \(\frac{r}{D}\)에 비례한다.
answer: 2
solution: 3상 3선식 가공 송전선로의 정전용량과 선간거리, 전선반지름의 관계를 묻는 문제입니다.

**핵심 공식:**
1선당 정전용량:
\[C_w = \frac{0.02413}{\log_{10} \frac{D}{r}} \text{ [μF/km]}\]

여기서:
- D: 선간거리 [m]
- r: 전선의 반지름 [m]

**관계식 분석:**
\[C \propto \frac{1}{\log_{10} \frac{D}{r}}\]

따라서 정전용량은 \(\log_{10} \frac{D}{r}\)에 **반비례**합니다.

**각 보기 검토:**
- (1) \(\log_{10} \frac{D}{r}\)에 비례 - 거짓 (반비례)
- (2) 정답 선택지
- (3) \(\frac{D}{r}\)에 비례 - 거짓 (선간거리가 증가하면 정전용량 감소)
- (4) \(\frac{r}{D}\)에 비례 - 거짓

**정답:** (2)번 (정전용량은 \(\log_{10} \frac{D}{r}\)에 반비례)

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
same_core_candidates: [1998_2회_23, 1998_4회_21, 2000_6회_21, 2001_1회_22, 2001_2회_29, 2002_3회_37, 2004_2회_24, 2005_2회_31, 2005_3회_26, 2007_1회_24]
same_trap_pattern_candidates: [1998_2회_23, 1998_4회_21, 2000_6회_21, 2001_1회_22, 2001_2회_29]

