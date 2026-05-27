# v_next D-3 input 050: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 2004_2회_24
year: 2004
session: 2회
q_no: 24
subject: 전력공학
question_text: 가공 송전선로에서 이상전압의 내습에 대 한 대책으로 틀린 것은？
choices:
  1. 휘림의 탑각 설치저항을 작게 한다.
  2. 기기 보호용으로서의 피뢰기를 설치한다.
  3. 가공지선을 설치한다.
  4. 차폐각을 크게 한다.
answer: 1
solution: **핵심 개념:**
가공 송전선로에서 뇌(이상전압)의 내습에 대한 대책들과 그 역할

**각 보기 검토:**

**(1) 철탑의 탑각 접지저항을 작게 한다** ✓ 정책
- 매설지선(탑각 접지)의 저항 감소
- 뇌 방전 경로의 임피던스 감소 → 역섬락 방지
- 뇌의 에너지를 빠르게 대지로 흐르도록 함

**(2) 기기 보호용으로서의 피뢰기를 설치한다** ✓ 정책
- 뇌로부터 발전기, 변압기 등 기기 직접 보호
- 과전압을 제한하여 절연 파괴 방지

**(3) 가공지선을 설치한다** ✓ 정책
- 뇌의 직접 타격으로부터 도체선을 차폐
- 차폐각이 적을수록 보호 효율 높음

**(4) 기재되지 않음**
정답은 (4) - 문제에서 4번 보기가 불완전하므로 정답이 될 수 없음

**정답:** (4)

**개념 정리:**
| 대책 | 목적 | 효과 |
|------|------|------|
| 탑각 접지저항 ↓ | 역섬락 방지 | 도체 간섭 방지 |
| 피뢰기 설치 | 기기 보호 | 과전압 제한 |
| 가공지선 | 뇌 차폐 | 직접 타격 방지 |

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=15; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=송전선; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 송전 용량/거리
star: null
ds_class: D
phenomenon_origin: D/Dynamic
six_axis: []
essence_question: 송전 거리와 전압이 송전 용량에 어떻게 작용하는가
representative_trap: 송전 전압급 단위 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 송전 전압급 단위 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 송전용량 -> 회로 4단자망 -> 회로 분포정수

[연관 문제 후보]
same_core_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22, 2001_2회_29, 2002_3회_37, 2005_2회_31, 2005_3회_26, 2007_1회_24]
same_trap_pattern_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22]

