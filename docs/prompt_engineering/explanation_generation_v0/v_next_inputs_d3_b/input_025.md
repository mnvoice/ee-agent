# v_next D-3 input 025: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 2001_2회_29
year: 2001
session: 2회
q_no: 29
subject: 전력공학
question_text: 교류 송전에서 송전 거리가 멀어질수록 동 일 전압에서의 송전 가능 전력이 적어진다. 그 이유 는?
choices:
  1. 선로의 어드미턴스가 커지기 때문이다
  2. 선로의 유도성 리액턴스가 커지기 때문이다
  3. 코로나 손실이 증가하기 때문이다
  4. 자항 손실이 커지기 때문이다
answer: 2
solution: 교류 송전에서 거리 증가에 따른 송전 가능 전력 감소 이유를 묻는 문제입니다.

**핵심 공식:**

송전 가능 전력: \[ P = \frac{E_S E_R}{X} \sin \delta \]

여기서:
- \(E_S\): 송전 전압
- \(E_R\): 수전 전압
- \(X\): 선로의 유도 리액턴스
- \(\delta\): 전압 위상각

**분석:**

송전 거리가 멀어지면 선로 정수 중 유도 리액턴스 \(X\) 가 증가합니다.

초고압 장거리 송전에서는:
- 저항(R)과 정전용량(C) → 유도 리액턴스(X)에 비해 무시 가능
- 유도 리액턴스가 주요 영향 인자

\(X\) 가 증가하면 송전 가능 전력은 감소합니다.

**오답 분석:**
- (1) 어드미턴스 증가 → 주 영향 요인 아님
- (3) 코로나 손실 → 송전 용량 저하의 직접 원인 아님
- (4) 저항 손실 → 초고압 송전에서 무시 가능

**정답: (2) 선로의 유도 리액턴스 증가**

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=송전 거리; audit_group=expansion

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
same_core_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22, 2002_3회_37, 2004_2회_24, 2005_2회_31, 2005_3회_26, 2007_1회_24]
same_trap_pattern_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22]

