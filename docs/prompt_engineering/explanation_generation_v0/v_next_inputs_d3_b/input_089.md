# v_next D-3 input 089: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2007_2회_27
year: 2007
session: 2회
q_no: 27
subject: 전력공학
question_text: 가공 지선을 설치하는 목적이 아닌 것은？
choices:
  1. 뇌해 방지
  2. 뇌해 보호
  3. 접지 저해 요과
  4. 코로나의 방생 방지
answer: 4
solution: 가공 지선(Overhead Ground Wire, OHGW)의 설치 목적을 묻는 문제입니다.

**가공 지선의 정의:**
송전선 위에 나란히 가설된 도선으로, 각 철탑에 접지되어 있는 보호선입니다.

**설치 목적 (정답):**

(1) **직격뇌에 대한 차폐 효과** ✓
- 지선이 뇌우 시 직접 낙뢰를 받아 송전선을 보호
- 뇌격 차단 역할

(2) **유도뢰에 대한 정전 차폐 효과** ✓
- 지선이 접지되어 있어 주변 정전 유도의 영향을 차단
- 전자파 차폐 역할

(3) **통신선에 대한 전자 유도 장해 경감 효과** ✓
- 지선이 유도장해 전류를 분산시켜 통신선 피해 감소
- 유도장해 경감

(4) **정보 없음** ✗
- 문제에서 제시되지 않음
- 위 3가지가 유일한 목적

**정답:** **(4) 번** (정보 없음 - 유효한 목적이 아님)

**추가 설명:**
가공 지선은 송전 시스템의 필수 안전 장치로, 낙뢰 보호와 유도장해 경감의 이중 역할을 수행합니다.

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

