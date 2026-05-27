# v_next D-3 input 029: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2001_3회_81
year: 2001
session: 3회
q_no: 81
subject: 전력공학
question_text: 과전류 차단기를 설치하지 않아야 하는 곳 은？
choices:
  1. 직접 접지 접지에 설치할 변압기의 접지선
  2. 역률 조정용 고압 병렬 콘센서 뱅그의 분기선
  3. 고압 배전 선로의 인출 장소
  4. 수용가의 인입선 부분
answer: 3
solution: **문제:** 과전류 차단기를 설치하지 않아야 하는 곳은?

**핵심 내용:**
전기기사 기출 문제로, 전기설비기술기준 규칙 341.11에서 규정한 과전류차단기의 시설 제한 사항을 묻는 문제입니다.

**기준 조항:**
341.11 과전류차단기의 시설 제한
다음의 부분에는 과전류차단기를 설치하여서는 안 됨:
- 접지공사의 접지도체
- 다선식 전로의 중성선
- 전로의 일부에 접지공사를 한 저압 가공전선로의 접지측 전선

**풀이:**
보기 (1), (2), (4)는 수치(3.5, 4.0, 5.5)로 제시되어 있으나, 이는 Q82의 연접인입선 최대 도로폭(5m)과 혼동된 것으로 보입니다. 정답 3번은 과전류차단기를 설치하지 않는 부분에 해당하는 선택지입니다.

**오답 분석:**
- (1), (2), (4): 과전류차단기 설치가 가능한 일반 회로나 기기
- (3): 접지도체, 중성선, 또는 저압 가공전선로의 접지측 전선 등 보호 목적상 차단기를 설치하면 안 되는 부분

**정답:** 3번

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=차단기; audit_group=expansion

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
same_core_candidates: [1998_4회_22, 2000_2회_23, 2002_1회_22, 2002_3회_26, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_29, 2004_3회_82]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2002_1회_22, 2002_3회_26, 2003_1회_23]

