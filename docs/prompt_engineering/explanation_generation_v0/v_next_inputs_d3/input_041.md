# v_next D-3 input 041: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2003_1회_27
year: 2003
session: 1회
q_no: 27
subject: 전력공학
question_text: 차단기에서 차단시간을 옳게 설명한 것은?
choices:
  1. 고장발생에서 차단터 완전 소호시간까지의 합이다.
  2. 재극하는 시간을 말한다.
  3. 아크시간을 말한다.
  4. 재극과 아크시간의 합한 것을 말하며 약 3~8사이 이다.
answer: 4
solution: **핵심 개념**: 차단기의 차단시간(Breaking Time) 정의

**풀이**:
차단기의 차단시간은 다음 두 시간의 합으로 구성됩니다:

\[
\text{차단시간} = \text{개극시간(Opening Time)} + \text{아크시간(Arc Time)}
\]

각 항목 검토:
- (1) 고장발생에서 완전 소호까지: "고장발생"을 포함하므로 과도함 (차단기 가동 개시부터 계산)
- (2) 개극되는 시간만: 아크시간을 제외하므로 불완전
- (3) 아크시간만: 개극시간을 제외하므로 불완전
- **(4) 개극시간 + 아크시간**: 정확한 정의 ✓

**시간 범위**: 일반적으로 \(3 \sim 8 \text{ [ms]}\) (약 \(3\sim 8\) 사이클)

**결론**: 정답 (4)

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
same_core_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26, 2003_1회_23, 2004_1회_90, 2004_3회_27, 2004_3회_29, 2004_3회_82]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2002_3회_26]

