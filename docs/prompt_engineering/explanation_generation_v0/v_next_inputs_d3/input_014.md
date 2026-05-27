# v_next D-3 input 014: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2000_2회_86
year: 2000
session: 2회
q_no: 86
subject: 전력공학
question_text: 애자공사로 시설하는 고압 옥내 배선과 다 른 애자공사에 의한 고압 옥내 배선이 접근하거나 교차하는 경우，상호간의 이격 거리는 최소 몇［cm］ 이상이어야 하는가？
choices:
  1. 10
  2. 15
  3. 20
  4. 25
answer: 3
solution: **문제 분석**
애자공사로 시설하는 고압 옥내 배선이 다른 애자공사에 의한 고압 옥내 배선과 접근하거나 교차할 때의 최소 이격거리를 묻는 문제입니다.

**전기설비기술기준 적용**

전기설비기술기준 제342.1조(고압 옥내배선 등의 시설)에서 고압 옥내배선이 다른 고압 옥내배선, 저압 옥내전선 또는 약전류 전선 등과 접근하거나 교차하는 경우의 이격거리는 다음과 같이 규정됩니다:

- **다른 고압 옥내배선·저압 옥내전선·관등회로의 배선·약전류 전선**: \(15\text{ cm}\)
- **수관·가스관이나 이와 유사한 것**: \(15\text{ cm}\)
- **저압 옥내전선이 나전선인 경우**: \(30\text{ cm}\)

**풀이**

애자공사에 의한 고압 옥내 배선 상호 간의 이격거리는 '다른 고압 옥내배선'에 해당하므로, 기준에 따라 **15 cm** 이상이어야 합니다.

**정답**: (2) 15 cm

**오답 분석**
- (1) 10 cm: 기준 미만으로 부적절
- (3) 20 cm: 과도한 거리 (필요 이상)
- (4) 25 cm: 과도한 거리 (필요 이상)

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=이격거리; audit_group=non_expansion_metadata

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
same_core_candidates: [1999_4회_81, 1999_4회_84, 2000_6회_92, 2001_2회_82, 2002_3회_85, 2003_3회_81, 2004_1회_84, 2004_1회_91, 2004_2회_86, 2004_3회_83]
same_trap_pattern_candidates: [1999_4회_81, 1999_4회_84, 2000_6회_92, 2001_2회_82, 2002_3회_85]

