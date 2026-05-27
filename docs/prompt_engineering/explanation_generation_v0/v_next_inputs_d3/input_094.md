# v_next D-3 input 094: 전력공학 / 전력_송배전D / 전압강하·전력손실

[문제]
id: 2008_1회_29
year: 2008
session: 1회
q_no: 29
subject: 전력공학
question_text: 단상 2선식（110［V］）저압 배전선로를 단상 3 선식 \((110 / 220[\mathrm{~V}])\) 으로 변경하였을 때 전선로의 전 압 강하율은 변경전에 비해서 어떻게 되는가？단，부 하용량은 변경 전후에 같고 역률은 1.0 이며 평형부하 이다．
choices:
  1. 5
  2. 1.8
  3. 83
  4. 560
answer: 3
solution: 전압 강하율 \(\epsilon=\frac{e}{V}=\frac{P}{V^{2}}(R+X \tan \theta)\) 의 식에서 \(n\) 배 승압하였을 때의 전압 강하율은
\[\frac{\epsilon^{\prime}}{\epsilon}=\frac{\frac{P}{(n V)^{2}}(R+X \tan \theta)}{\frac{P}{V^{2}}(R+X \tan \theta)}=\frac{1}{n^{2}} \text { 가 된다. }\]

즉，단상 2선식을 단상 3선식으로 변경하였을 경우는 2 배 승압한 경 우이므로 전압 강하율은 \(\frac{1}{4}\) 배가 된다．

【답］（1）

문제 \(30154 / 22.9[\mathrm{kV}], 40\)［MVA］인 3상 변압기의 \(\%\) 리액턴스가 14 ［\％］라면 1차측으로 환산한 리액턴 스는 약 몇 \([\Omega]\) 인가？
（1） 5
（2） 1.8
（3） 83
（4） 560
풀이
\(\% Z=\frac{Z P}{10 V^{2}}\) 에서 임피턴스 \(Z=\frac{10 V^{2} \times \% Z}{P}\)
여기서，\(V\) ：정격전압［ kV ］，\(P:\) 기준용량［ kVA ］
\[Z=\frac{10 \times 154^{2} \times 14}{40000}=83[\Omega]\]

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=전압강하; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 전압강하·전력손실
star: null
ds_class: D
phenomenon_origin: D/Dynamic
six_axis: []
essence_question: 송전 거리·전류·임피던스가 전압강하에 어떻게 작용하는가
representative_trap: 단상 vs 3상 전압강하 공식 혼동 함정
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 단상 vs 3상 전압강하 공식 혼동 함정
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 전압강하/손실 -> 회로 임피던스 -> 회로 옴의 법칙

[연관 문제 후보]
same_core_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31, 2005_1회_28, 2005_2회_23, 2006_1회_2, 2006_1회_28]
same_trap_pattern_candidates: [1999_3회_22, 2000_6회_23, 2001_3회_25, 2004_2회_23, 2004_2회_31]

