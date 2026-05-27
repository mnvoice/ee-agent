# v_next D-3 input 070: 전력공학 / 전력_송배전D / 전압강하·전력손실

[문제]
id: 2006_1회_2
year: 2006
session: 1회
q_no: 2
subject: 전력공학
question_text: 전선에 흐르는 전류를 1.5 배 증가시켜도 저 항에 의한 전압강하가 변하지 않으려면 전선의 반지 름을 약 몇 배로 하여야 되는가?
choices:
  1. 0.67
  2. 0.82
  3. 1.22
  4. 3
answer: 3
solution: 전선의 저항 변화에 따른 반지름 변화를 구하는 문제입니다.

**핵심 공식:**
저항: \(R = \rho\frac{l}{\pi r^2}\)
전압강하: \(e = Ri\)

**풀이 과정:**
1) 전압강하가 변하지 않으므로: \(e = e'\)
\[I \cdot R = I' \cdot R'\]

2) 주어진 조건: \(I' = 1.5I\), 따라서:
\[I \cdot R = 1.5I \cdot R'\]
\[R' = \frac{R}{1.5}\]

3) 저항은 반지름의 제곱에 반비례하므로:
\[\frac{R'}{R} = \frac{r^2}{r'^2}\]

4) 대입하면:
\[\frac{1}{1.5} = \frac{r^2}{r'^2}\]

5) 반지름의 비:
\[r' = \sqrt{1.5} \cdot r = 1.22r\]

**정답: 3번** \(r' \approx 1.22r\) (약 1.2배 또는 \(\sqrt{1.5}\)배)

**오답 분석:**
- (1), (2)는 1.5배 미만으로 전압강하 증가
- (4) 3배는 저항이 1/9로 줄어들어 과도함

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=전압강하; audit_group=expansion

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
same_core_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31, 2005_1회_28, 2005_2회_23, 2006_1회_28, 2008_1회_29]
same_trap_pattern_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31]

