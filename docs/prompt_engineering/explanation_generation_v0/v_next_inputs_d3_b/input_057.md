# v_next D-3 input 057: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2004_3회_29
year: 2004
session: 3회
q_no: 29
subject: 전력공학
question_text: 최근 \(154[\mathrm{kV}]\) 급 변전소에 주로 설치되는 차단기의 종류는？
choices:
  1. 자기 차단기(MBB)
  2. 유입 차단기(OCB)
  3. 기중 차단기(ACB)
  4. SF₆ 가스 차단기(GCB)
answer: 4
solution: 154kV급 변전소에 주로 설치되는 차단기:

**각 차단기의 특성 및 적용 전압:**

| 차단기 종류 | 소호 매질 | 적용 전압 | 특징 |
|-----------|---------|---------|------|
| 유입 차단기(OCB) | 절연유 | 154kV 이상 | 고전압, 대용량 |
| 기중 차단기(ACB) | 공기 | 저전압(~440V) | 저전압 배전용 |
| 자기 차단기(MBB) | 자기장 | 저전압 | 특수용도 |
| SF₆ 차단기(GCB) | SF₆ 가스 | 154kV 이상 | 현대식, 최근 주류 |

**154kV급 현황:**
- 과거: 유입 차단기(OCB)가 주류
- 최근: SF₆ 가스 차단기(GCB)로 교체 추세

**정답: 4번 (선택지 누락)**
정확한 정답은 "**SF₆ 차단기(GCB)**" 또는 "**유입 차단기(OCB)**"

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
same_core_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_82]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26]

