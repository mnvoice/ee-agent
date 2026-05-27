# v_next D-3 input 024: 전력공학 / 전력_설비고장 / 절연내력 / 유도장해

[문제]
id: 2001_2회_24
year: 2001
session: 2회
q_no: 24
subject: 전력공학
question_text: 송전선의 통신선에 대한 유도 장해 방지 대책이 아닌 것은?
choices:
  1. 접지선과 통신선과의 상호 인덕턴스를 크게 한다.
  2. 접지선의 저항을 충분히 한다.
  3. 고장 발생 시 지락류를 직제하고 고장 구간은 빨리 차단한다.
  4. 차폐선을 설치한다.
answer: 1
solution: 송전선의 통신선에 대한 유도 장해 방지 대책을 묻는 문제입니다.

**유도 장해 발생 메커니즘**:

유도 전압의 크기는 다음 식으로 표현됩니다:

$$E_m = 2\pi f M l \times 3I_0$$

여기서:
- $M$ = 상호 인덕턴스 (송전선과 통신선 간)
- $I_0$ = 지락 전류
- $f$ = 주파수
- $l$ = 선로 길이

**유도 장해 경감 대책**:

(2) **연가를 충분히 한다**: 송전선과 통신선 간의 거리를 증가시켜 상호 인덕턴스 $M$을 감소 → 유도 전압 감소 ✓

(3) **지락 전류 억제 및 고장 구간 신속 차단**: 지락 전류 $I_0$를 감소시키고 노출 시간을 단축 → 유도 전압 저감 ✓

(4) **차폐선 설치**: 차폐선이 유도 전압을 차단하여 보호 ✓

(1) **오답 이유**: 상호 인덕턴스 $M$을 크게 하면 유도 전압이 증가하므로, 이는 유도 장해 방지 대책이 될 수 없습니다.

**정답**: 1번

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=유도장해; audit_group=non_expansion_metadata

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 절연내력 / 유도장해
star: null
ds_class: S
phenomenon_origin: S/Static
six_axis: []
essence_question: 절연내력 시험전압과 유도장해 경감이 어떻게 작용하는가
representative_trap: 절연내력 시험전압 배율 / 유도장해 경감대책 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 절연내력 시험전압 배율 / 유도장해 경감대책 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: null

[연관 문제 후보]
same_core_candidates: [2000_6회_85, 2003_1회_22]
same_trap_pattern_candidates: [2000_6회_85, 2003_1회_22]

