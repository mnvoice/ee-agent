# v_next D-3 input 023: 전력공학 / 전력_보호고장S / 단락전류·임피던스

[문제]
id: 2001_2회_21
year: 2001
session: 2회
q_no: 21
subject: 전력공학
question_text: 그림에 표시하는 무부하 송전선의 S 점에 있어서 3상 단락이 일어났을 때의 단락 전류[A]는? 단, \(\mathrm{G}_{1}: 15\) [MVA], \(11[\mathrm{kV}], \% Z=30[\%]\) \(\mathrm{G}_{2}: 15[\mathrm{MVA}], 11[\mathrm{kV}], \% Z=30[\%]\) \(\mathrm{T}: 30[\mathrm{MVA}], 11[\mathrm{kV}] / 154[\mathrm{kV}], \% Z=8[\%]\) 송전선 TS 사이 \(50[\mathrm{~km}], Z=0.5[\Omega / \mathrm{km}]\)
choices:
  1. 12.7
  2. 151.3
  3. 273
  4. 383.3
answer: 3
solution: **주어진 조건:**
- 발전기 G₁, G₂: 각 15 [MVA], 11 [kV], %Z = 30%
- 변압기 T: 30 [MVA], 11/154 [kV], %Z = 8%
- 송전선 TS: 50 [km], Z = 0.5 [Ω/km]
- S점에서 3상 단락 발생

**풀이 단계:**

**1단계: 송전선의 %Z 계산 (30 [MVA] 기준)**

송전선의 임피던스:
\[Z = 0.5 × 50 = 25 [Ω]\]

기준값 기반:
\[\%Z_{line} = \frac{Z × P}{10 × V^2} = \frac{25 × 30,000}{10 × 154^2} = \frac{750,000}{237,160} = 3.16[\%]\]

**2단계: 발전기의 %Z 계산 (30 [MVA] 기준)**

두 발전기(각 15 [MVA], %Z = 30%)를 병렬로 연결시, 병렬 임피던스:
\[\%Z_{gen} = \frac{60 × 60}{60 + 60} × \frac{30}{15} = \frac{3600}{120} × 2 = 30 × \frac{15}{30} = 15[\%]\]

단순화하면, 기준값 30 [MVA] 기준으로:
\[\%Z_{gen} = \frac{30 × 30}{30 + 30} = 15[\%]\]

**3단계: 총 %Z 계산 (30 [MVA] 기준)**

\[\%Z_{total} = \%Z_{gen} + \%Z_{transformer} + \%Z_{line}\]
\[\%Z_{total} = 15 + 8 + 3.16 = 26.16[\%]\]

**참고:** 풀이의 OCR 결과에서 "60 × 60/(60+60)"로 표기된 것은 두 발전기(30+30=60 [MVA]) 병렬 계산을 의미하며, 실제로는 15%입니다. 최종 합이 41.16%로 표시되었으나, 정확한 재계산 결과는 26.16%입니다.

**4단계: 정격 전류 계산 (30 [MVA] 기준, 154 [kV] 측)**

\[I_n = \frac{P}{\sqrt{3} × V} = \frac{30,000 × 10^3}{\sqrt{3} × 154,000} = \frac{30 × 10^6}{1.732 × 154 × 10^3}\]
\[I_n ≈ 112.5 [A]\]

**5단계: 단락 전류 계산**

\[I_s = \frac{100}{\%Z} × I_n = \frac{100}{26.16} × 112.5 ≈ 430 [A]\]

**정답:** 3번 (보기: 1차, 3차 권선)

**주의사항:**
- 제시된 풀이에서 %Z 합계 41.16%는 재검토 필요
- 단락 전류 273 [A]는 위의 상세 계산과 차이 발생
- 최종 정답은 문제의 선택지(1~4번)와 맥락을 고려하여 3번이 정답으로 표시됨

[데이터 품질 사전 점검]
conflict_status: CLEAN
conflict_detail: score=18; v_next_d3_clean94; hard_filter=PASS; source_overlap=false; evidence_field=both; matched_keyword=단락전류; audit_group=expansion

[v3.2 라벨링 매칭 결과]
matched_core_id: null
matched_core_name: 단락전류·임피던스
star: null
ds_class: S
phenomenon_origin: S/Fault
six_axis: []
essence_question: %Z와 기준용량을 어떻게 환산해 단락전류를 구하는가
representative_trap: 기준용량 환산 비율 함정 / %Z 기준 변경 혼동
memorize_hint: null

[함정 지도 61항 매칭]
is_trap_map_member: true
trap_type: 기준용량 환산 비율 함정 / %Z 기준 변경 혼동
trap_alignment_hint: null

[동적 7항 매핑]
dynamic_link: 전력 단락전류 -> 회로 옴의 법칙 -> 회로 임피던스 환산

[연관 문제 후보]
same_core_candidates: [2000_6회_27, 2002_1회_30, 2003_1회_21]
same_trap_pattern_candidates: [2000_6회_27, 2002_1회_30, 2003_1회_21]

