# v_next D-3 input 007: 전력공학 / 전력_보호고장S / 지락·중성점 접지

[문제]
id: 1999_3회_23
year: 1999
session: 3회
q_no: 23
subject: 전력공학
question_text: 소호 리액터 접지에 대한 설명으로 옳지 않은 것은？
choices:
  1. 지락전류가 작다.
  2. 전자 유도 장해가 경감된다.
  3. 지락 중에도 송전이 가능하다.
  4. 선떤 지락 계전기의 동작이 우아 하다.
answer: 4
solution: 소호 리액터 접지방식은 중성점을 송전선로의 대지정전용량과 공진하는 리액터를 통해 접지하는 방식입니다.

**각 보기 검토:**
(1) 지락전류가 적다 - 맞음. 리액터에 의해 지락전류가 최소화됨
(2) 전자 유도 장해가 경감된다 - 맞음. 지락전류 감소로 유도장해 최소화
(3) 지락 중에도 송전이 가능하다 - 맞음. 지락전류가 작아 송전 지속 가능
(4) 선택 지락 계전기의 동작이 용이하다 - 틀림. 지락전류가 너무 작아서 선택 지락 계전기의 동작이 오히려 곤란함

**정답: (4)번**

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=소호리액터; audit_group=expansion

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
same_core_candidates: [2002_1회_33, 2005_2회_28, 2006_3회_21]
same_trap_pattern_candidates: [2002_1회_33, 2005_2회_28, 2006_3회_21]

