# v_next D-3 input 042: 전력공학 / 전력_보호고장S / 보호계전기·피뢰기

[문제]
id: 2003_1회_44
year: 2003
session: 1회
q_no: 44
subject: 전력공학
question_text: 보호 계전기 구성요소의 기본 원리에 속하 지 않는 것은?
choices:
  1. 전자 흡인
  2. 전자 유도
  3. 정지형 소위치 회로
  4. 광전관
answer: 4
solution: 보호 계전기의 기본 원리에 속하지 않는 것을 찾는 문제입니다.

**보호 계전기 구성요소의 기본 원리:**
- (1) 전자 흡인: 전자석의 원리로 철심을 흡인하여 접점을 작동
- (2) 전자 유도: 교류 자속의 변화로 인한 유도작용 이용
- (3) 정지형 스위칭 회로: 반도체 소자를 이용한 고속 스위칭

**오답 이유:**
보기 (4)는 광전 효과(광전관)입니다. 이는 빛의 강도 변화를 전류의 변화로 변환하는 원리로, 보호 계전기의 기본 작동 원리와는 무관합니다. 보호 계전기는 전기적 신호(전압, 전류)에 반응하는 장치이지, 광신호에 반응하지 않습니다.

**정답:** 보기 (4)번 (광전 효과)

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=보호계전기; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 보호계전기·피뢰기
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: 보호계전기 동작 특성과 피뢰기 정격이 어떻게 작용하는가
representative_trap: 보호계전기 정정 / 피뢰기 정격 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 보호계전기 정정 / 피뢰기 정격 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 보호계전기/피뢰기 -> 설비 절연/보호 -> 회로 임피던스

[연관 문제 후보]
same_core_candidates: [2000_2회_85, 2000_6회_28, 2001_3회_26, 2002_3회_23, 2007_1회_87]
same_trap_pattern_candidates: [2000_2회_85, 2000_6회_28, 2001_3회_26, 2002_3회_23, 2007_1회_87]

