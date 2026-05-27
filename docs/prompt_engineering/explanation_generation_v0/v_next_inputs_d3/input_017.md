# v_next D-3 input 017: 전력공학 / 전력_송배전D / 전압강하·전력손실

[문제]
id: 2000_6회_23
year: 2000
session: 6회
q_no: 23
subject: 전력공학
question_text: 역률 80 ［\％］의 3 상 평형 부하에 공급하고 있는 선로 길이 \(2[\mathrm{~km}]\) 의 3상 3선식 배전 선로가 있 다．부하의 단자 전압을 \(6000[\mathrm{~V}]\) 로 유지하였을 경 우 선로의 전압 강하율이 10 ［\％］를 넘지 않게 하기 위해서는 부하 전력을 몇［kW］까지 허용할 수 있는 가？단，전선 1 선당의 저항은 \(0.82[\Omega / \mathrm{km}]\) ，리액턴 스는 \(0.38[\Omega / \mathrm{km}]\) 라 하고 그 밖의 정수는 무시한다．
choices:
  1. 1303
  2. 1629
  3. 2257
  4. 2821
answer: 3
solution: **핵심 공식:**
3상 3선식 배전선로의 전압강하율:
\[ \varepsilon = \frac{P}{V^2}(R + X\tan\theta) \]

**단계별 풀이:**

1) 주어진 조건 정리:
   - 역률 \( \cos\theta = 0.8 \) → \( \tan\theta = \frac{0.6}{0.8} = 0.75 \)
   - 선로길이: \( l = 2 \text{ km} \)
   - 선저항: \( R = 0.82 \times 2 = 1.64 \text{ Ω} \)
   - 선리액턴스: \( X = 0.38 \times 2 = 0.76 \text{ Ω} \)
   - 부하단자전압: \( V = 6000 \text{ V} \)
   - 허용 전압강하율: \( \varepsilon \leq 0.1 \text{ (10%)} \)

2) 전압강하 요소 계산:
   \[ R + X\tan\theta = 1.64 + 0.76 \times 0.75 = 1.64 + 0.57 = 2.21 \text{ Ω} \]

3) 전압강하율 식에 대입:
   \[ 0.1 = \frac{P}{6000^2} \times 2.21 \]

4) 허용 부하전력 계산:
   \[ P = \frac{0.1 \times 6000^2}{2.21} \times 10^{-3} = \frac{0.1 \times 36,000,000}{2.21} \times 10^{-3} \]
   \[ P = \frac{3,600,000}{2.21} \times 10^{-3} = 1,628.95 \text{ kW} \approx 1,629 \text{ kW} \]

**정답: (2) 1629 kW**

**오답 이유:**
- (1) 1303: 저항만 고려하여 리액턴스 항 미포함
- (3), (4): 계산 오류 또는 잘못된 공식 적용

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=전압강하; audit_group=expansion

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
same_core_candidates: [1999_3회_22, 2001_3회_25, 2004_2회_23, 2004_2회_31, 2005_1회_28, 2005_2회_23, 2006_1회_2, 2006_1회_28, 2008_1회_29]
same_trap_pattern_candidates: [1999_3회_22, 2001_3회_25, 2004_2회_23, 2004_2회_31, 2005_1회_28]

