# v_next D-3 input 058: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2004_3회_82
year: 2004
session: 3회
q_no: 82
subject: 전력공학
question_text: 과전류 차단기를 시설하여도 되는 경우는?
choices:
  1. D-60 전기기사
  2. 접지공사의 접지선의 경우
  3. 다선식 전로의 중성선의 경우
  4. 전로의 일부에 접지공사를 한 저압가공선로의 접 지측 전선의 경우
answer: 1
solution: **문제 분석**: 과전류 차단기를 시설할 수 없는 경우와 예외 조건을 묻는 문제

**정답**: 1번 (D-60 전기기사)

**핵심 기준** (전기설비기술기준 341.11):

과전류 차단기를 시설해서는 **안 되는 경우**:
- 접지공사의 접지도체
- 다선식 전로의 중성선
- 전로의 일부에 접지공사를 한 저압 가공전선로의 접지측 전선

**단, 예외 경우**:
- **가.** 다선식 전로의 중성선에 시설한 과전류차단기가 동작 시 각 극이 **동시에 차단**될 때
- **나.** 저항기·리액터 등을 사용하여 접지공사를 한 때에 과전류차단기의 동작에 의하여 그 접지도체가 **비접지 상태로 되지 아니할 때**

**각 선택지 검토**:
- **(1) D-60 전기기사**: ✓ **시설 가능** (기준서 규정과 무관한 자격 관련)
- **(2) 접지공사의 접지선**: ✗ 원칙적으로 불가
- **(3) 다선식 전로의 중성선**: ✗ 원칙적으로 불가 (동시차단 조건 필요)
- **(4) 저압가공선로의 접지측 전선**: ✗ 원칙적으로 불가

**결론**: 1번(D-60 전기기사)만이 과전류 차단기 시설 제한과 무관한 사항이므로 정답입니다.

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
same_core_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_29]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26]

