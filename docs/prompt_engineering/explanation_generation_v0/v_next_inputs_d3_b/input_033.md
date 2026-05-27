# v_next D-3 input 033: 전력공학 / 전력_송배전D / 코로나 / 전선 도체

[문제]
id: 2002_3회_21
year: 2002
session: 3회
q_no: 21
subject: 전력공학
question_text: 복도체에서 2본의 전선이 서로 충돌하는 것을 방지하기 위하여 2본의 전선 사이에 적당한 간 격을 두어 설치하는 것은?
choices:
  1. 아모르드
  2. 댐퍼
  3. 아지손
  4. 스페이서
answer: 4
solution: **문제 분석:**
복도체(다도체)에서 2본 이상의 전선이 서로 충돌하는 것을 방지하기 위해 사용되는 장치를 묻는 문제입니다.

**핵심 개념:**
- 복도체: 하나의 상(phase)에 여러 개의 도체를 다발로 묶어 사용
- 이를 통해 코로나 현상 감소, 송전용량 증가 등의 장점

**각 선택지 분석:**
- (1) 아모로드: 송전선의 장력 조정용
- (2) 댐퍼: 풍진동(wind vibration) 방지용
- (3) 아킹혼: 지락(지면과의 접촉)으로 인한 아크 방지용
- **(4) 스페이서: 복도체의 전선 상호 간 접근·충돌 방지용** ✓

**정답:**
**4번 (스페이서)**

**오답 이유:**
- 아모로드, 댐퍼, 아킹혼은 모두 다른 목적의 부속품이며, 전선 간 충돌 방지와는 무관함

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
same_core_candidates: [2000_4회_23, 2007_2회_24]
same_trap_pattern_candidates: [2000_4회_23, 2007_2회_24]

