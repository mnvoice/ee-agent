# v_next D-3 input 030: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2002_1회_22
year: 2002
session: 1회
q_no: 22
subject: 전력공학
question_text: 고압 폐쇄 배전반에 수납할 수 없는 차단 기는?
choices:
  1. 유입 차단기 ( OCB )
  2. 자기 차단기 \((\mathrm{MBB})\)
  3. 공기 차단기 \((\mathrm{ABB})\)
  4. 진공 차단기 \((\mathrm{VCB})\)
answer: 2
solution: **핵심 개념**: 고압 폐쇄 배전반(GIS: Gas Insulated Switchgear)에 수납 가능한 차단기의 조건

**각 차단기의 특성**:

1) **유입 차단기(OCB)** - 유기 절연유 사용
   - 용량이 크고 대형 구조
   - 고압 폐쇄 배전반에 **수납 불가능** (공간 부족)

2) **자기 차단기(MBB)** - 자기 분기 방식
   - 콤팩트 설계 가능
   - 폐쇄 배전반 수납 가능

3) **공기 차단기(ABB)** - 압축 공기 사용
   - 소형화 가능
   - 폐쇄 배전반 수납 가능

4) **진공 차단기(VCB)** - 진공 호칭 방식
   - 초소형 설계, 무점검
   - 폐쇄 배전반 수납 가능

**정답**: (1) 유입 차단기(OCB)

**이유**: 유입 차단기는 대량의 절연유가 필요하여 구조가 크고 무겁기 때문에 고압 폐쇄 배전반의 제한된 공간에 수납할 수 없음.

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
same_core_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_3회_26, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_29, 2004_3회_82]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_3회_26, 2003_1회_23]

