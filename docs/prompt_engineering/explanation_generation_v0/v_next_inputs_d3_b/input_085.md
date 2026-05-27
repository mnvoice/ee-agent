# v_next D-3 input 085: 전력공학 / 전력_설비고장 / 가공전선 이격거리

[문제]
id: 2007_1회_82
year: 2007
session: 1회
q_no: 82
subject: 전력공학
question_text: 사용 전압이 \(400[\mathrm{~V}]\) 이하인 저압 가공 전 선은 케이블이나 절연전선인 경우를 제외하고 인장 강도가 \(3.43[\mathrm{kN}]\) 이상인 것 또는 지름이 몇 \([\mathrm{mm}]\) 이 상의 경동선이어야 하는가？
choices:
  1. 1.2
  2. 2.6
  3. 3.2
  4. 4.0
answer: 3
solution: **핵심 기준:** 전기설비기술기준 222.5 저압 가공전선의 굵기 및 종류

**문제 조건:**
- 사용 전압: 400 [V] 이하
- 케이블이나 절인전선이 아닌 경우
- 인장강도 3.43 [kN] 이상 또는 지름 ? [mm] 이상의 경동선

**규정 내용:**

| 전압 | 조건 | 지름(경동선) |
|------|------|-------------|
| 400V 이하 | 절연전선 | 2.6 mm 이상 |
| 400V 이하 | 케이블 이외 | **3.2 mm 이상** |
| 400V 초과(시가지) | 케이블 이외 | 5 mm 이상 |
| 400V 초과(시가지 외) | 케이블 이외 | 4 mm 이상 |

**정답:** 3번 - 3.2 [mm]

**오답 분석:**
- (1) 1.2 mm: 규정 미만
- (2) 2.6 mm: 절연전선 기준 (케이블 이외 아님)
- (4) 4.0 mm: 400V 초과 시가지 외 기준

선택지 (3)이 표시되지 않았으나 3.2 mm이 정답입니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=가공전선; audit_group=non_expansion_metadata

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

