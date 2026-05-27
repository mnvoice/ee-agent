# v_next D-3 input 034: 전력공학 / 전력_보호고장S / 보호계전기·피뢰기

[문제]
id: 2002_3회_23
year: 2002
session: 3회
q_no: 23
subject: 전력공학
question_text: 피뢰기의 구조에 해당되지 않는 것은?
choices:
  1. 특성 요소
  2. 직렬 갭(gap)
  3. 콘센서
  4. 실드링
answer: 3
solution: 피뢰기의 구조 및 역할을 묻는 문제입니다.

**피뢰기의 주요 구조 요소:**

1. **직렬 갭(Series Gap)**
   - 역할: 속류(follow current) 차단
   - 뇌격 후 일반 전원 전류를 차단하여 소호(arc extinction)를 담당

2. **특성 요소(Non-linear Resistance)**
   - 역할: 도전도 형성
   - 비선형 저항으로서 고전압에서는 저항값이 낮고, 저전압에서는 높음

3. **쉴드링(Shielding)**
   - 역할: 전기적·자기적 충격으로부터 보호
   - 외부 방전 및 유도에 의한 손상으로부터 차단기를 보호

**정답:** 3번

**풀이:**
문제는 "피뢰기의 구조에 해당되지 않는 것"을 묻고 있습니다. 보기 (3)은 문제에서 명시되지 않았으나, 풀이에 따르면 "쉴드링"이 정답입니다. 쉴드링은 피뢰기의 외부 보호 장치이지만, 피뢰기 자체의 핵심 구조(직렬 갭, 특성 요소)와는 다른 보조적 역할을 수행하므로 "피뢰기의 구조"라고 보기 어렵습니다.

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
same_core_candidates: [2000_2회_85, 2000_6회_28, 2001_3회_26, 2003_1회_44, 2007_1회_87]
same_trap_pattern_candidates: [2000_2회_85, 2000_6회_28, 2001_3회_26, 2003_1회_44, 2007_1회_87]

