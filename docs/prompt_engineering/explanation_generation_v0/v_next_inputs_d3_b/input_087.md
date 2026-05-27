# v_next D-3 input 087: 전력공학 / 전력_보호고장S / 보호계전기·피뢰기

[문제]
id: 2007_1회_87
year: 2007
session: 1회
q_no: 87
subject: 전력공학
question_text: 피뢰기를 반드시 시설하여야 할 곳은？
choices:
  1. 전기 수용 장소 내의 차단기 2차측
  2. 가공 전선로와 지중 전선로가 접속되는 곳
  3. 수전용 변압기의 2차측
  4. 장강이 긴 가공 전선로
answer: 2
solution: **문제 분석:**
피뢰기를 반드시 시설해야 할 곳을 찾는 문제입니다.

**전기설비기술기준 341.13 피뢰기의 시설:**

고압 및 특고압의 전로 중 다음 장소에 피뢰기를 시설해야 합니다:

**가.** 발전소·변전소 또는 이에 준하는 장소의 가공전선 인입구 및 인출구

**나.** 특고압 가공전선로에 접속하는 배전용 변압기의 고압측 및 특고압측

**다.** 고압 및 특고압 가공전선로로부터 공급을 받는 수용장소의 인입구

**라.** 가공전선로와 지중전선로가 접속되는 곳

**보기 검토:**
- (1) 전기수용장소 내의 차단기 2차측: 저압 영역 → 피뢰기 불필요
- (2) 정답 (기준 나항: 배전용 변압기의 고압측)
- (3) 수전용 변압기의 2차측: 저압 영역 → 피뢰기 불필요
- (4) 경간이 긴 가공전선로: 절연 강화 등으로 대응 가능, 필수 조건 아님

**정답: 2번**

배전용 변압기의 고압측은 고압 가공전선로 접속 지점으로 낙뢰에 노출되므로 피뢰기 설치가 필수입니다.

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
same_core_candidates: [2000_2회_85, 2000_6회_28, 2001_3회_26, 2002_3회_23, 2003_1회_44]
same_trap_pattern_candidates: [2000_2회_85, 2000_6회_28, 2001_3회_26, 2002_3회_23, 2003_1회_44]

