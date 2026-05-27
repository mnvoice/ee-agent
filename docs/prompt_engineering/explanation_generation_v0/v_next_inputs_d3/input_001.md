# v_next D-3 input 001: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 1998_2회_23
year: 1998
session: 2회
q_no: 23
subject: 전력공학
question_text: 가공송전선의 정전 용량이 \(0.008[\mu \overline{\mathrm{~F} /} \mathrm{km}]\) 이고, 인덕턴스가 \(1.1[\mathrm{mH} / \mathrm{km}]\) 일 때, 파동 임피 던스는 약 몇 \([\Omega]\) 이 되겠는가? 단. 주어지지 않은 기타 정수는 무시한다.
choices:
  1. 350
  2. 370
  3. 390
  4. 410
answer: 2
solution: **핵심 공식**: 파동(특성) 임피던스(Wave Impedance)

\[Z_0 = \sqrt{\frac{Z}{Y}} \approx \sqrt{\frac{L}{C}}\]

여기서:
- \(L\) = 단위 길이당 인덕턴스 [H/km]
- \(C\) = 단위 길이당 정전용량 [F/km]

**주어진 데이터**:
- \(C = 0.008\text{ [μF/km]} = 0.008 \times 10^{-6}\text{ [F/km]}\)
- \(L = 1.1\text{ [mH/km]} = 1.1 \times 10^{-3}\text{ [H/km]}\)

**계산 과정**:

\[Z_0 = \sqrt{\frac{L}{C}} = \sqrt{\frac{1.1 \times 10^{-3}}{0.008 \times 10^{-6}}}\]

\[= \sqrt{\frac{1.1 \times 10^{-3}}{8 \times 10^{-9}}} = \sqrt{\frac{1.1}{8} \times 10^{6}}\]

\[= \sqrt{0.1375 \times 10^{6}} = \sqrt{137500} \approx 370\text{ [Ω]}\]

**정답**: (2) 370 [Ω]

**의미**: 송전선로의 파동 임피던스는 전자파 전파 특성을 결정하는 중요한 매개변수입니다.

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
same_core_candidates: [1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22, 2001_2회_29, 2002_3회_37, 2004_2회_24, 2005_2회_31, 2005_3회_26, 2007_1회_24]
same_trap_pattern_candidates: [1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_1회_22, 2001_2회_29]

