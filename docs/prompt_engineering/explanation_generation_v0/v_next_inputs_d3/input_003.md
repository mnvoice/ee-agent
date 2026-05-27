# v_next D-3 input 003: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 1998_4회_22
year: 1998
session: 4회
q_no: 22
subject: 전력공학
question_text: 자기 차단기의 특징 중 옳지 않은 것은？
choices:
  1. 화제의 위험이 적다.
  2. 보수 정전이 비교적 쉽다.
  3. 전류 질단에 의한 왜곡류가 발생하지 않는다.
  4. 회로의 고유 주파수에 차단 성능이 좌우된다.
answer: 4
solution: 유전 차단기(자기 차단기)의 특징을 판별하는 문제입니다.

**유전 차단기의 특징:**

(1) ✓ 화재 위험이 없다 - 유전유는 불연성 물질

(2) ✓ 보수 점검이 비교적 쉽다 - 간단한 구조

(3) ✓ 압축 공기 설비가 필요 없다 - 공기 차단기와 달리 압축 공기 미필요

(4) ✗ **전류 절단에 의한 과전압을 발생하지 않는다**
→ 이것이 **틀린 표현**입니다!
→ 실제로는 **전류 절단 시 과전압을 발생**하는 것이 유전 차단기의 단점
→ 이를 억제하기 위해 피뢰기 등 보호장치 필요

(5) ✓ 회로의 고유 주파수에 차단 성능이 좌우되는 일이 없다 - 유전유의 성질상 안정적

**정답: (4)**

**핵심:** 유전 차단기는 과전압 발생이 **단점**이므로, "발생하지 않는다"는 표현이 오류

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=차단기; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 차단기
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: 소호매질 종류가 차단 특성에 어떻게 작용하는가
representative_trap: 차단 용량 vs 차단 시간 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 차단 용량 vs 차단 시간 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 차단기 -> 회로 단락전류 / 임피던스 환산

[연관 문제 후보]
same_core_candidates: [2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_29, 2004_3회_82]
same_trap_pattern_candidates: [2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23]

