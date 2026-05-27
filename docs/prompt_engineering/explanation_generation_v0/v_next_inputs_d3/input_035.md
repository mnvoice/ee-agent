# v_next D-3 input 035: 전력공학 / 전력_보호고장S / 차단기

[문제]
id: 2002_3회_26
year: 2002
session: 3회
q_no: 26
subject: 전력공학
question_text: 변전소의 가스 차단기에 대한 설명이 잘못 된 것은?
choices:
  1. 불연성이므로 화재의 위험성이 적다.
  2. 자력 소호가 가능하다.
  3. 특고압 계통의 차단기로 많이 사용된다.
  4. 긴거리 차단에 유리하지 못하다.
answer: 4
solution: 가스 차단기(SF₆ 차단기)의 특징과 성능을 묻는 문제입니다.

**가스 차단기(SF₆ 차단기)의 특징:**

1. **불연성** ✓
   - SF₆ 가스는 불연성이므로 화재 위험이 적음
   - 보기 (1)은 **올바른 설명**

2. **자력 소호(Self-extinguishing arc)** ✓
   - SF₆ 가스의 우수한 절연성과 소호능력으로 가능
   - 보기 (2)는 **올바른 설명**

3. **특고압 계통 사용** ✓
   - 소호능력이 뛰어나 고전압 대전류 차단에 적합
   - 특고압 이상의 계통에 많이 사용됨
   - 보기 (3)은 **올바른 설명**

**SF₆ 가스 차단기의 추가 장점:**
- 이상 전압의 발생이 적음
- 아크 소멸 후 절연 회복능력이 우수
- 탈조 차단(out-of-step protection) 및 근거리 차단에 유리
- 절연거리를 적게 할 수 있어 소형·경량화 가능
- 유지보수가 용이

**정답:** 4번

**풀이:**
보기 (1), (2), (3)은 모두 가스 차단기의 실제 특징입니다. 따라서 "설명이 잘못 된 것"을 묻는 문제에서 4번 보기(명시되지 않음)가 잘못된 설명을 담고 있으며, 이는 가스 차단기의 특징과 배치되는 내용일 것입니다.

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
same_core_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2003_1회_23, 2003_1회_27, 2004_1회_90, 2004_3회_27, 2004_3회_29, 2004_3회_82]
same_trap_pattern_candidates: [1998_4회_22, 2000_2회_23, 2001_3회_81, 2002_1회_22, 2003_1회_23]

