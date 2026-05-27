# v_next D-3 input 039: 전력공학 / 전력_설비고장 / 절연내력 / 유도장해

[문제]
id: 2003_1회_22
year: 2003
session: 1회
q_no: 22
subject: 전력공학
question_text: 송전 선로의 1선 지락 고장시，인접 통신선 에 대한 전자 유도 장애의 방지 대책이 아닌 것은？
choices:
  1. 전력선과 통신선과의 병렬 거리 단축
  2. 전력선과 통신선과의 이격 거리 단축
  3. 고속도 계절기 및 차단기를 제용
  4. 도전율이 높은 도체로 가공 지선 설치
answer: 2
solution: 송전선로 1선 지락 고장시 인접 통신선의 전자유도 장해 방지 대책을 분석합니다.

**핵심 개념:**
전자유도 장해는 지락전류의 크기, 지락 지속시간, 전력선과 통신선의 상호인덕턴스에 비례합니다.

**전력선측 대책 (유도장해 경감):**
1) 상호거리 증가 → 상호인덕턴스 감소 ✓
2) 연가(Transposition) 충분 → 선로정수 평형, 중성점 잔류전압 감소 ✓
3) 케이블 사용 → 지락전류 감소 ✓
4) 고주파 발생 방지 ✓
5) 교차각을 직각 → 유도량 감소 ✓
6) 소호리액터 사용 → 지락전류 감소 ✓
7) 고장회선 고속차단 → 지속시간 단축 ✓
8) 차폐선 시설 ✓

**정답: (2) 누락된 보기**

풀이에서 (2)가 생략되었으나, 제시된 대책들은 모두 유도장해 경감 방법입니다. 문제에서 "방지 대책이 아닌 것"을 묻고 있으므로, 정상적인 보기 중 반대 효과를 가진 항목이 정답이어야 합니다. 예를 들어 '전력선과 통신선의 거리를 감소시킨다' 같은 항목이 정답 후보가 됩니다.

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=통신선; audit_group=non_expansion_metadata

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
same_core_candidates: [2000_6회_85, 2001_2회_24]
same_trap_pattern_candidates: [2000_6회_85, 2001_2회_24]

