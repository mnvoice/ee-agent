# v_next D-3 input 049: 전력공학 / 전력_송배전D / 전압강하·전력손실

[문제]
id: 2004_2회_23
year: 2004
session: 2회
q_no: 23
subject: 전력공학
question_text: 송전 전력，부하 역률，송전 거리，전력 손 실 및 선간 전압이 같을 경우 3상 3선식에서 전선 한 가닥에 흐르는 전류는 단상 2선식에서 전선 한 가닥 에 흐르는 경우의 몇 배가 되는가？
choices:
  1. \(\frac{1}{\sqrt{3}}\) 배
  2. \(\frac{2}{3}\) 배
  3. \(\frac{3}{4}\) 배
  4. \(\frac{4}{9}\) 배
answer: 4
solution: **핵심 공식:**
송전 전력식:
- 단상 2선식: $P = VI_1\cos\theta$
- 3상 3선식: $P = \sqrt{3}VI_3\cos\theta$

**조건:**
송전 전력, 부하 역률, 송전 거리, 전력손실, 선간 전압이 모두 동일

**단계별 풀이:**

1단계: 동일한 전력 조건식 수립
$$VI_1\cos\theta = \sqrt{3}VI_3\cos\theta$$

2단계: V와 $\cos\theta$ 약분
$$I_1 = \sqrt{3}I_3$$

3단계: 3상에서의 전류를 단상 기준으로 표현
$$I_3 = \frac{I_1}{\sqrt{3}} = \frac{1}{\sqrt{3}}I_1$$

**정답:** (1) $\frac{1}{\sqrt{3}}$ 배

**개념 설명:**
- 같은 전력을 전송할 때, 3상 시스템이 단상 시스템보다 필요 전류가 $\frac{1}{\sqrt{3}}$배 적음
- 따라서 전선 단면적을 줄일 수 있어 경제적
- 이것이 3상 송전의 주요 장점

**오답 이유:**
- (2), (3), (4): 전력 관계식에 위반되는 임의의 비율값

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=전력손실; audit_group=expansion

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
same_core_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_31, 2005_1회_28, 2005_2회_23, 2006_1회_2, 2006_1회_28, 2008_1회_29]
same_trap_pattern_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_31, 2005_1회_28]

