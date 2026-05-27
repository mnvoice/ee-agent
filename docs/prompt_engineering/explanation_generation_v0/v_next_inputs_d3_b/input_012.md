# v_next D-3 input 012: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2000_2회_23
year: 2000
session: 2회
q_no: 23
subject: 전력공학
question_text: 수（數）10기압의 압축 공기를 소호실 내의 아크에 급부（扱附）하여 아크 흔적을 급속히 치환하 며 차단 정격 전압이 가장 높은 차단기는 다음 중 어 느 것인가？
choices:
  1. MBB
  2. ABB
  3. VCB
  4. ACB
answer: 3
solution: **핵심 개념:**
차단기의 소호매질과 정격 전압 범위

**각 차단기의 특성:**

1) **ABB (공기 차단기 - Air Blast Circuit Breaker)**
   - 15~30 [kg/cm²]의 압축공기를 아크에 분사
   - 정격전압: **66kV 이상의 초고압 계통**에 사용
   - 가장 높은 차단정격전압 보유

2) VCB (진공 차단기)
   - 정격전압: 24~77kV

3) ACB (절연유 차단기)
   - 정격전압: ~66kV

4) MBB (몰드형 차단기)
   - 저전압용 (~0.66kV)

**원리:**
압축공기는 우수한 절연성과 냉각 특성을 가지므로 초고압 계통의 강력한 아크를 빠르게 소호할 수 있어, 가장 높은 정격전압에서 사용 가능

**정답: (2) ABB (공기 차단기)**

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
dynamic_link: 전력 차단기 -> 회로 단락전류 / 회로 임피던스 환산

[연관 문제 후보]
same_core_candidates: [1998_4회_22, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_29, 2004_3회_82]
same_trap_pattern_candidates: [1998_4회_22, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23]

