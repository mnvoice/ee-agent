# v_next D-3 input 092: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2008_1회_23
year: 2008
session: 1회
q_no: 23
subject: 전력공학
question_text: 그림은 유입 차단기（탱크형）의 구조도이다． A 의 명칭은？
choices:
  1. 절연 liner
  2. 승강간
  3. 가능 접촉자
  4. 고장 접촉자
answer: 3
solution: A ：가동 접촉자
B ：고정 접촉자
C：승강간
D ：절연 liner

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=16; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=question_text; matched_keyword=차단기; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 차단기
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: 소호매질 종류가 차단 특성에 어떻게 작용하는가
representative_trap: 차단 용량 vs 차단 시간 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 차단 용량 vs 차단 시간 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 차단기 -> 회로 단락전류 / 회로 임피던스 환산

[연관 문제 후보]
same_core_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_29]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26]

