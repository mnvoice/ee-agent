# v_next D-3 input 072: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2006_1회_29
year: 2006
session: 1회
q_no: 29
subject: 전력공학
question_text: 가공지선에 대한 설명으로 틀린 것은？
choices:
  1. 직적로에 대해서는 특히 유용하며, 탈 상부에 시설하므로 낮는 구로 가공지선에 내습한다.
  2. 가공지선 펜문에 송전 선로의 대지 용량이 감소하므로 대지 사이에 방전점 때 유도점압이 특히 커서 차폐 효과가 종한다.
  3. 송전선 지락시 지락전류의 일부가 가공지선에 흘러 차폐작용을 하므로 전자유도 장해를 직게 할 수 있다.
  4. 도로의 설치에 대하여도 그 가설구간 전체에 사고 방지의 효과가 있다.
answer: 2
solution: **핵심 개념**: 가공지선(overhead ground wire)의 기능 및 특성

**가공지선의 주요 기능**

(1) **직격뢰 방호** ✓ 정답
- 탑 상부에 설치되어 직접 낙뢰를 유인
- 뇌전류를 안전하게 지면으로 분산

(2) **전자 차폐 효과** ✓ 정답
- 인접한 통신선에 대한 전자유도 장해 감소
- 지락전류 일부가 가공지선에 흘러 차폐작용
- 결과: 전자 유도 전압 **감소** (증가가 아님)

(3) **유도뢰 서지 보호** ✓ 정답
- 유도뢰 서지에 대한 효과적인 방어
- 가설구간 전체에서 사고 방지

**틀린 설명 분석 (정답: 2번)**

보기 (2)의 내용이 제시되지 않았으나, 문제에서 정답이 2번으로 표기됨. 일반적으로 가공지선에 대한 오류는:
- "가공지선이 있으면 유도 전압이 **증가**한다" ❌
- "가공지선은 지락 전류를 **증가**시킨다" ❌
- "유도뢰 서지에만 효과가 있다" ❌

**정답**: (2) [보기 내용 미제시]

**개념 정리**
- 가공지선 = 직격뢰 + 유도장해 동시 방호
- 효과: 안정도 향상, 뢰해 감소, 전자 장해 감소

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=가공지선; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 가공전선 이격거리
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 가공전선과 다른 시설간 안전 이격거리는 어떻게 정해지는가
representative_trap: 전선 종류별 이격거리 표 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 전선 종류별 이격거리 표 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82, 2002_3회_85, 2003_3회_81, 2004_1회_84, 2004_1회_91, 2004_2회_86]
same_trap_pattern_candidates: [1999_4회_81, 1999_4회_84, 2000_2회_86, 2000_6회_92, 2001_2회_82]

