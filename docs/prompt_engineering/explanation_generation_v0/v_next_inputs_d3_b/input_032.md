# v_next D-3 input 032: 전력공학 / 전력_보호고장S / 지락·중성점 접지

[문제]
id: 2002_1회_33
year: 2002
session: 1회
q_no: 33
subject: 전력공학
question_text: 중성점 고저항 접지 방식의 평행 2회선 송 전 선로의 지락사고 차단에 사용되는 계전기는?
choices:
  1. 가공지선
  2. 메셜지선
  3. 크로스본드선
  4. 차폐선
answer: 1
solution: 중성점 고저항 접지 방식에서 병행(평행) 2회선 송전선로의 지락사고 차단 방법을 분석합니다.

**중성점 고저항 접지 방식의 특성:**
- 지락 고장 시 지락 전류가 매우 작음 (수십~수백 A)
- 단상 지락 시에도 3상 전압이 크게 왜곡되지 않음
- 병행 회선 구성으로 한 회선 지락 시에도 다른 회선은 계속 운전 가능

**병행 2회선 지락사고 차단의 필요성:**
병행 2회선에서 한 회선이 지락하면, 지락 전류가 인접한 정상 회선으로 유도되어 상호 간섭이 발생합니다. 이를 선택적으로 감지하기 위해서는:

**필요한 계전기:**
- **(1) 선택 접지 계전기(Ground Selective Relay)**: 영상 전류(Zero Sequence Current)를 감지하여 지락 회선을 특정하고 차단 ✓
- **(2) 과전류 계전기**: 지락 전류가 작아서 부적절
- **(3) 거리 계전기**: 거리 측정에는 부적절
- **(4) 역상 계전기**: 단상 지락 감지에는 부족

**정답: 1번 선택 접지 계전기**

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=중성점; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 지락·중성점 접지
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: 중성점 접지 방식이 지락전류에 어떻게 작용하는가
representative_trap: 직접접지 vs 소호리액터 vs 비접지 특성 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 직접접지 vs 소호리액터 vs 비접지 특성 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 중성점 접지 -> 회로 대칭분 해석

[연관 문제 후보]
same_core_candidates: [1999_3회_23, 2005_2회_28, 2006_3회_21]
same_trap_pattern_candidates: [1999_3회_23, 2005_2회_28, 2006_3회_21]

