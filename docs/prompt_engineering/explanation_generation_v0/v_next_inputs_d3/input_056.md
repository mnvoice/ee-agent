# v_next D-3 input 056: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2004_3회_27
year: 2004
session: 3회
q_no: 27
subject: 전력공학
question_text: 콘덴서용 차단기의 정격 전류는 콘덴서군 전류의 몇 [\%] 이상의 것을 선정하는 것이 바람직한 가?
choices:
  1. 120
  2. 130
  3. 140
  4. 150
answer: 4
solution: 콘덴서용 차단기의 정격 전류 선정 기준:

**핵심 내용:**
- 일반 회로 차단기: 정격 전류는 사용 전류의 120% 이상
- 콘덴서 회로 차단기: 정격 전류는 콘덴서군 전류의 **150% 이상**

**이유:**
콘덴서는 투입 시 과도 전류(inrush current)가 발생하며, 이는 정상 운전 전류의 1.5배 이상에 달한다. 또한 콘덴서 회로는 고조파의 영향으로 불안정한 전류 특성을 가지므로, 차단기는 더 큰 용량으로 선정하여 신뢰성을 확보해야 한다.

**정답: 4번 (150%)**

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=차단기; audit_group=expansion

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
dynamic_link: 전력 차단기 -> 회로 단락전류 / 임피던스 환산

[연관 문제 후보]
same_core_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_29, 2004_3회_82]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26]

