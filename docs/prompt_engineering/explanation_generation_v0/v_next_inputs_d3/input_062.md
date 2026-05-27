# v_next D-3 input 062: 전력공학 / 전력_송배전D / 전압강하·전력손실

[문제]
id: 2005_1회_28
year: 2005
session: 1회
q_no: 28
subject: 전력공학
question_text: 단일부하 배전선에서 부하 역률 \(\cos \theta\) ，부 하 전류 \(I\) ，선로 저항 \(r\) ，리액턴스를 \(x\) 라 하면 배전 선에서 최대 전압강하가 생기는 조건은？
choices:
  1. \(\cos\theta = \frac{r}{x}\)
  2. \(\sin\theta = \frac{x}{r}\)
  3. \(\tan\theta = \frac{x}{r}\)
  4. \(\tan\theta = \frac{r}{x}\)
answer: 4
solution: 배전선에서 최대 전압강하가 발생하는 조건을 미분으로 구합니다.

**기본 공식:**
전압강하: \[ e = I(r \cos \theta + x \sin \theta) \]

여기서:
- \(I\): 부하 전류
- \(r\): 선로 저항
- \(x\): 선로 리액턴스
- \(\theta\): 부하의 위상각

**풀이 과정:**

\(e\)가 최대가 되는 조건을 구하기 위해 \(\theta\)에 대해 미분:

\[ \frac{\partial e}{\partial \theta} = I(-r \sin \theta + x \cos \theta) = 0 \]

0이 되는 조건:
\[ x \cos \theta = r \sin \theta \]

양변을 \(\cos \theta\)로 나누면:
\[ x = r \tan \theta \]

따라서:
\[ \tan \theta = \frac{x}{r} \]

**오답 검토:**
- (1) \(\cos \theta = \frac{r}{x}\): 잘못된 형태
- (2) \(\sin \theta = \frac{x}{r}\): 삼각함수 관계 오류
- (4) \(\tan \theta = \frac{r}{x}\): 분자·분모 반대

**정답: (3)** \(\tan \theta = \frac{x}{r}\)

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
same_core_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31, 2005_2회_23, 2006_1회_2, 2006_1회_28, 2008_1회_29]
same_trap_pattern_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31]

