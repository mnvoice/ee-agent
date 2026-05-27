# v_next D-3 input 022: 전력공학 / 전력_송배전D / 송전 용량/거리

[문제]
id: 2001_1회_22
year: 2001
session: 1회
q_no: 22
subject: 전력공학
question_text: 송전 전압을 올린 경우에 생기는 문제점이 아닌 것은？
choices:
  1. \(1.237[\mathrm{mH} / \mathrm{km}]\)
  2. \(1.287[\mathrm{mH} / \mathrm{km}]\)
  3. \(2.849[\mathrm{mH} / \mathrm{km}]\)
  4. \(2.899[\mathrm{mH} / \mathrm{km}]\)
answer: 3
solution: **문제 해석:**
송전 전압을 올렸을 때 발생하는 문제점과 발생하지 않는 항목을 찾는 문제입니다.

**제시된 정보:**
- 절연 파괴 전위 경도: 직류 30[kV/cm], 교류 21[kV/cm]
- 원래 문제: "237/3.7[mm] 경동연선(반지름 0.555[cm])의 완전 연가 66[kV] 송전선 인덕턴스"

**송전전압 상승의 주요 문제점:**

1. **절연 파괴 위험 증가** - 높은 전압은 절연물을 파괴할 수 있음
2. **코로나 현상** - 도체 표면에서 부분 방전 발생 (전력손실, 소음, 무선간섭)
3. **전압 강하 및 손실 증가** - 저항에 의한 손실: \( P_l = I^2R \)
4. **기계적 응력 증가** - 도체에 작용하는 힘과 스팬 증가
5. **절연재 비용 증가** - 더 높은 등급의 절연 필요

**발생하지 않는 항목:**
- **전력 손실 감소**: 송전 전압을 올리면 같은 전력 전송 시 전류가 감소하여 \( P_l = I^2R \)에 의해 손실이 오히려 **감소**합니다. 따라서 이것이 답일 가능성이 높습니다.

**정답: (3)번 - 2.849[mH/km]**

(원래 문제와 보기가 혼재되어 있으나, 문제의 의도는 "전압 상승의 부작용이 아닌 것"을 찾는 것이며, 선택지들이 단위 [mH/km]인 인덕턴스 값으로 표기된 것으로 보아 기출 문제 편집에 오류가 있음을 알 수 있습니다. 정확한 문제 재확인이 필요합니다.)

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=송전전압; audit_group=expansion

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
same_core_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_2회_29, 2002_3회_37, 2004_2회_24, 2005_2회_31, 2005_3회_26, 2007_1회_24]
same_trap_pattern_candidates: [1998_2회_23, 1998_4회_21, 1999_6회_23, 2000_6회_21, 2001_2회_29]

