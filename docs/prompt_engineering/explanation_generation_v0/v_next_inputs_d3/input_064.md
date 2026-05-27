# v_next D-3 input 064: 전력공학 / 전력_송배전D / 전압강하·전력손실

[문제]
id: 2005_2회_23
year: 2005
session: 2회
q_no: 23
subject: 전력공학
question_text: 전력，역률，거리가 같을 때，사용 전선량이 같다면 3상 3선식과 3상 4선식의 전력 손실비는 얼 마인가？단，4선식의 중성선의 굵기는 외선과 같고， 외선과 중성선간의 전압은 3 선식의 선간 전압과 같 고， 3 상 평형 부하이다．
choices:
  1. \(\frac{1}{3}\)
  2. \(\frac{1}{2}\)
  3. \(\frac{3}{4}\)
  4. \(\frac{9}{4}\)
answer: 2
solution: 3상 3선식과 3상 4선식의 전력손실비를 비교하는 문제입니다.

**핵심 공식**:
전력손실은 
\[P_l = I^2 R\]

여기서 전선량이 같을 때, 선로의 저항은 전선량에 비례합니다.

**주어진 조건**:
- 전력, 역률, 거리 동일
- 사용 전선량 같음
- 3상 평형 부하
- 4선식의 중성선 굵기 = 외선과 동일
- 4선식의 선간 전압 = 3선식의 선간 전압

**풀이**:

표에서 주어진 소요 전선량:
- 3상 3선식: 18
- 3상 4선식: 8

같은 전력을 공급할 때 전선량이 같다는 조건에서:

3상 3선식에서 필요한 전류를 $I_3$, 3상 4선식에서 필요한 전류를 $I_4$라 하면,

전선량이 비례하므로:
\[\frac{P_{l3}}{P_{l4}} = \frac{I_3^2 R_3}{I_4^2 R_4}\]

전선량 비 18:8에서, 전선단면적 비는 역으로 나타나므로:

3상 3선식의 손실 기준치: 18
3상 4선식의 손실 기준치: 8

따라서 전력손실비는:
\[\frac{P_{l3}}{P_{l4}} = \frac{18}{8} = \frac{9}{4}\]

**정답**: (4) $\frac{9}{4}$

**개념 설명**:
4선식은 중성선으로 인해 회로 구성이 더 효율적이어서 더 적은 전선량으로 같은 전력을 공급할 수 있으므로 전력손실이 더 작습니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=전력손실; audit_group=expansion

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
same_core_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31, 2005_1회_28, 2006_1회_2, 2006_1회_28, 2008_1회_29]
same_trap_pattern_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31]

