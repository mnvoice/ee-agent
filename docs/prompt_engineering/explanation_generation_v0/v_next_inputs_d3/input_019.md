# v_next D-3 input 019: 전력공학 / 전력_보호고장S / 보호계전기·피뢰기

[문제]
id: 2000_6회_28
year: 2000
session: 6회
q_no: 28
subject: 전력공학
question_text: 피뢰기의 정격을 나타내는 단위는？
choices:
  1. [A]
  2. [Ω]
  3. [V]
  4. [W]
answer: 1
solution: 피뢰기(Lightning Arrester, LA)의 정격은 **[kV](kilovolt, 킬로볼트)** 단위로 표시됩니다.

**핵심 개념:**
- 피뢰기는 전력계통의 과전압으로부터 기기를 보호하는 장치입니다.
- 정격은 피뢰기가 견딜 수 있는 최대 지속 전압을 나타내며, 보호하는 선로의 선간 전압 크기에 따라 결정됩니다.

**오답 분석:**
- (2) [Ω]: 임피던스 단위 (저항·리액턴스 관련)
- (3) [V]: 전압 단위이지만, 피뢰기 정격은 kV 단위 사용
- (4) [W]: 전력 단위 (피뢰기와 무관)

**정답: (1) [kV]**

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
same_core_candidates: [2000_2회_85, 2001_3회_26, 2002_3회_23, 2003_1회_44, 2007_1회_87]
same_trap_pattern_candidates: [2000_2회_85, 2001_3회_26, 2002_3회_23, 2003_1회_44, 2007_1회_87]

