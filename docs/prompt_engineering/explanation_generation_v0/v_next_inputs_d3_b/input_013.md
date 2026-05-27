# v_next D-3 input 013: 전력공학 / 전력_보호고장S / 보호계전기·피뢰기

[문제]
id: 2000_2회_85
year: 2000
session: 2회
q_no: 85
subject: 전력공학
question_text: 피뢰기를 시설하지 않는 곳은？
choices:
  1. 변전소의 가공전선 인입구
  2. 수용 장소에서 분기되는 분기점
  3. 가공 전선로와 지중 전선로가 접속되는 곳
  4. 수용 및 특고압 가공 전선로로부터 공급을 받는 수용장소의 인입구
answer: 2
solution: **문제 분석:**
피뢰기를 시설하지 **않는** 곳을 찾는 문제입니다.

**풀이 과정:**

전기설비기술기준 341.13 피뢰기의 시설 규정을 검토합니다.

**피뢰기를 시설해야 하는 곳:**

고압 및 특고압의 전로 중 다음 곳에는 피뢰기를 시설해야 함:

가. 발전소·변전소 또는 이에 준하는 장소의 **가공전선 인입구 및 인출구**

나. 특고압 가공전선로에 접속하는 배전용 변압기의 **고압측 및 특고압측**

다. 고압 및 특고압 가공전선로로부터 공급을 받는 수용장소의 **인입구**

라. **가공전선로와 지중전선로가 접속되는 곳**

**선택지 검토:**
- (1) 변전소의 가공전선 인입구 → 규정 가항에 해당 → **피뢰기 필수**
- (2) [불완전한 선택지이나 제시된 규정에 없음] → **피뢰기 불필요**
- (3) 가공 전선로와 지중 전선로가 접속되는 곳 → 규정 라항에 해당 → **피뢰기 필수**
- (4) 고압 및 특고압 가공 전선로로부터 공급을 받는 수용장소의 인입구 → 규정 다항에 해당 → **피뢰기 필수**

**정답: (2)**

**(2) 선택지가 불완전하지만, 규정상 명시되지 않은 곳이 정답입니다.**

**결론:** (1), (3), (4) 모두 규정에 따라 피뢰기를 시설해야 하는 곳이므로, (2)가 유일한 피뢰기 불필요 지점입니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=피뢰기; audit_group=expansion

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
same_core_candidates: [2000_6회_28, 2001_3회_26, 2002_3회_23, 2003_1회_44, 2007_1회_87]
same_trap_pattern_candidates: [2000_6회_28, 2001_3회_26, 2002_3회_23, 2003_1회_44, 2007_1회_87]

