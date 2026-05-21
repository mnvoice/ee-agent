# Answer-Selection Pedagogy — Expansion Solution Dry-run (2026-05-21)

Solution dry-run for the answer-selection pedagogy expansion batch. After the
pilot 7 (`2aadbe5`, review 7/7 `keep`), this is the next batch. For each item
it drafts a v2.1 plain-text-label `solution` / `steps` and checks the draft
against the quality gate.

This is a **dry-run document only**. It does NOT modify `app/data` and is not
an approval to apply. `apply_status` = `not_applied` for every item.

- Base commit: `f09b97e` (docs: record pedagogy push approval)
- Template: `docs/audit/answer_selection_pedagogy_template_v2_1_plaintext_2026-05-21.md`
  (v2.1 plain-text labels — the app renderer does not parse markdown)
- Design parent: `docs/audit/answer_selection_pedagogy_track_design_2026-05-21.md`
- Pilot precedent: `docs/audit/answer_selection_pedagogy_pilot_dryrun_2026-05-21.md`
- Source pool: `docs/audit/old_answer_verification_correction_final_closeout_2026-05-21.md`,
  `docs/audit/old_answer_conflict_correction_manifest_2026-05-21.md`
- Decisions: `DR-T35-Q2A-ANSWER-SOT-001`, `DR-T35-V2A-AK-MAPPING-BLOCKED-001`

## 1. Scope — planned 20, executed 18 (safety exclusions)

The expansion target was a 20-item batch. The source-verified pool is the
old-answer track's 28 resolved items (9 `source_answer_verified` + 19 C20
single-answer corrected); the pilot used 7, leaving 21 non-pilot
source-verified items. Of those 21, three are excluded for safety:

| key | subject | 제외 사유 | 후속 트랙 |
| --- | --- | --- | --- |
| `2005_3회_83` | 전기설비기술기준 | statute(법령) 문항 — 조문번호 / 법령 표현 날조 리스크. answer-selection 일반 템플릿으로 다루지 않음 | statute-safe 트랙 (별도) |
| `2015_1회_87` | 전기설비기술기준 | statute(법령) 문항 — 동일 (옥내 전로 대지전압 규정) | statute-safe 트랙 (별도) |
| `2002_1회_32` | 전력공학 | 정답 보기 `[1]`의 저장 텍스트가 `} \end{table}`로 손상. `answer`=1이라 **정답 보기 자체가 깨져** 보기 판단 매핑이 불가능 | DQ / 데이터 품질 트랙 (별도) |

`21 − 3 = 18` verified-clean candidates. The batch is **planned 20, executed
18 due to safety exclusions**. The 2-item shortfall is intentionally NOT
filled: padding with statute items (article-fabrication risk) or with
non-source-verified items (breaks the source-verified premise) was rejected
by supervisor decision (2026-05-21). The next batch resumes the 20-unit
rhythm after more source-verified clean candidates are secured.

## 2. Candidate set (18)

All 18 are `source_answer` verified or C20-corrected and closed; none is
statute; none has a corrupted answer choice. `solution_svg`, where present,
was confirmed illustrative (not stem-required) by the SVG audit `10d8901`
(`stale_svg` 0); every stem here is answerable from text alone.

| # | key | subject (stored) | answer | q_type | svg | note |
| --- | --- | --- | ---: | --- | --- | --- |
| 1 | `2001_1회_21` | 전력공학 | 2 | 계산형 | no | verified |
| 2 | `2015_1회_22` | 전력공학 | 1 | 암기형 | no | verified; choice [2] OCR |
| 3 | `2015_3회_27` | 전력공학 | 3 | 암기형 | no | verified; choice [4] OCR |
| 4 | `2015_2회_23` | 전력공학 | 4 | 암기형 | yes | C20-3 corrected (3→4) |
| 5 | `2015_2회_29` | 전력공학 | 2 | 암기형 | no | C20-3 corrected (1→2); choice [4] residue |
| 6 | `2015_3회_25` | 전력공학 | 4 | 암기형 | no | C20-3 corrected (1→4); choice-OCR recovered `fac4b8d` |
| 7 | `2016_1회_69` | 전력공학 | 4 | 개념형 | yes | C20-4 corrected (1→4); subject-label looks 제어공학 |
| 8 | `2006_1회_7` | 전기자기학 | 2 | 계산형 | yes | verified; text OCR residue (z항) |
| 9 | `2015_1회_13` | 전기자기학 | 1 | 계산형 | yes | verified |
| 10 | `1998_4회_10` | 전기자기학 | 4 | 계산형 | yes | C20-1 corrected (1→4) |
| 11 | `2002_3회_4` | 전기자기학 | 4 | 개념형 | yes | C20-1 corrected (2→4); choice [4] residue |
| 12 | `2006_1회_6` | 전기자기학 | 3 | 계산형 | yes | C20-2 corrected (4→3) |
| 13 | `2015_1회_71` | 전기자기학 | 1 | 계산형 | yes | C20-2 corrected (4→1); content is R-L 시정수(회로이론) |
| 14 | `2016_3회_44` | 전기기기 | 4 | 암기형 | yes | verified |
| 15 | `2001_3회_43` | 전기기기 | 2 | 개념형 | no | C20-1 corrected (1→2); choice-OCR recovered `fac4b8d`; obscure machine — risk |
| 16 | `2016_1회_44` | 전기기기 | 4 | 암기형 | no | C20-4 corrected (2→4); reasoning cleanup `4fbc820` |
| 17 | `2016_1회_71` | 제어공학 | 3 | 암기형 | yes | verified; choice [4] LaTeX residue; content is 3상 결선(회로이론) |
| 18 | `2001_1회_68` | 제어공학 | 3 | 암기형 | no | C20-1 corrected (1→3) |

Subject spread: 전력공학 7, 전기자기학 6, 전기기기 3, 제어공학 2. 회로이론 0
— the non-pilot source-verified pool has no 회로이론 item (the pilot used the
only one, `2007_2회_64`).

## 3. v2.1 template applied

Each `solution` uses plain-text labels (no markdown bold / heading / table):
`핵심 단서:` / `보기 판단:` / `근거/계산:` / `함정:` / `시험장 판별:` /
`정답:`. `정답:` is the last line. The conditional `다른 과목 연결:` element
is **omitted for all 18** — see Section 6 (no link in this pool is strong
enough to include without forcing it, which the template prohibits).
`steps` keeps the `인식` / `변환` / `계산` dict.

---

## 4. Per-item dry-run

### 1 — `2001_1회_21` · 전력공학 · answer 2 · 계산형

```
핵심 단서: 가공 전선로 1상당 작용 인덕턴스 공식을 묻는다. 도체 내부 자속분과 외부 자속분의 합으로 본다.

보기 판단: 작용 인덕턴스 = 내부분(상수 0.05[mH/km]) + 외부분(0.4605 log₁₀(D/r)). [1]은 내부분이 0.5로 10배 커서 틀림. [3]·[4]는 로그 안이 r/D로 뒤집혀(D>r일 때 음수) 틀림. [2]만 0.4605 log₁₀(D/r)+0.05로 정확.

근거/계산: L = 0.4605 log₁₀(D/r) + 0.05 [mH/km]. 0.05는 내부 자속분 고정값, 로그항은 외부 자속분.

함정: 내부 인덕턴스 상수를 0.5로 외우면 [1]을 고른다 — 실제 값은 0.05다.

시험장 판별: "+0.05"와 "log(D/r)"를 동시에 만족하는 보기를 찾는다. r/D 보기는 즉시 탈락.

정답: 2번 (L = 0.4605 log₁₀(D/r) + 0.05).
```

steps — `인식`: 가공 송전선로 1상 작용 인덕턴스 공식을 고르는 문제. /
`변환`: 작용 인덕턴스 = 내부 인덕턴스(고정값 0.05) + 외부 인덕턴스(0.4605
log₁₀(D/r)). / `계산`: L = 0.4605 log₁₀(D/r) + 0.05 [mH/km]. 로그 안은 D/r,
상수는 0.05 → 정답 ②.

self-review — answer match: YES (2). choice mapping: [1]-[4] all mapped. label:
6 elements, plain-text, `정답:` last. length: solution 453 / steps 152. iPad
risk: low. quality gate: pass.

### 2 — `2015_1회_22` · 전력공학 · answer 1 · 암기형

```
핵심 단서: 송전계통 안정도 "향상 방법이 아닌 것"을 찾는다. 안정 극한 전력이 직렬 리액턴스 X에 반비례한다는 점이 판단 기준.

보기 판단: P_max = V_s·V_r·sinδ/X. [1] 직렬 리액턴스를 늘리면 X↑ → P_max↓ → 안정도 악화 → 향상책이 아님: 정답. [2] 전압 변동을 줄이면 운전점이 안정 → 향상책. [3] 중간 조상은 전압 유지로 향상책. [4] 고장전류 저감·고속 차단은 고장 지속을 줄여 향상책.

근거/계산: P_max = V_s·V_r·sinδ / X. X가 분모이므로 X를 줄이면 향상, 늘리면 악화.

함정: "리액턴스"라는 단어만 보고 좋은 대책으로 착각한다 — 직렬 리액턴스는 줄여야 한다.

시험장 판별: "아닌 것"을 찾는 문제. X를 키우는 보기 하나만 고르면 끝 — [1]뿐.

정답: 1번 (직렬 리액턴스를 증가시킨다 — 안정도 향상책이 아님).
```

steps — `인식`: 송전계통 안정도 향상책이 "아닌 것"을 고르는 문제. / `변환`:
P_max = V_s·V_r·sinδ/X. 안정도는 직렬 리액턴스 X에 반비례. / `계산`: [1]
직렬 리액턴스 증가 → X↑ → P_max↓ → 악화 → 향상책 아님. [2]·[3]·[4]는 향상책
→ 정답 ①.

self-review — answer match: YES (1). choice mapping: [1]-[4] all mapped. label:
ok, `정답:` last. length: solution 452 / steps 141. iPad risk: low. quality
gate: pass. risk: choice [2] 저장 텍스트 "전압변동을 직접 한다"는 "전압변동을
적게 한다"의 OCR 변형으로 보임 — 보기 판단은 자명한 뜻(전압 변동을 줄임)으로
서술. answer-무관 보기이며 의미 손상 없음. choice-cleanup 후보로 flag.

### 3 — `2015_3회_27` · 전력공학 · answer 3 · 암기형

```
핵심 단서: 송전계통 안정도 "증진 방법이 아닌 것"을 찾는다. 증진책은 직렬 리액턴스를 줄이는 방향이라는 점이 기준.

보기 판단: P_max = V_s·V_r·sinδ/X. [1] 속응 여자는 고장 시 전압을 빠르게 회복 → 증진. [2] 고속도 재폐로는 고장 구간을 신속 복구 → 증진. [3] 발전기·변압기 리액턴스를 키우면 직렬 리액턴스↑ → 안정 극한 전력↓ → 악화 → 증진책이 아님: 정답. [4] 고장전류 저감·고속 차단은 증진.

근거/계산: 발전기 동기 리액턴스·변압기 리액턴스도 계통 직렬 리액턴스 X에 더해진다. 이를 키우면 X↑로 안정도가 나빠진다.

함정: 기기 리액턴스를 키우면 고장전류가 줄어 좋다고 오해한다 — 고장전류는 줄지만 안정도는 악화된다.

시험장 판별: 리액턴스를 키우는 보기 = 증진책 아님. [3]뿐.

정답: 3번 (발전기·변압기 리액턴스를 크게 — 증진책이 아님).
```

steps — `인식`: 송전계통 안정도 증진책이 "아닌 것"을 고르는 문제. / `변환`:
P_max = V_s·V_r·sinδ/X. 발전기·변압기 리액턴스도 직렬 리액턴스 X에 포함. /
`계산`: [3] 기기 리액턴스↑ → X↑ → 안정 극한 전력↓ → 악화 → 증진책 아님 →
정답 ③.

self-review — answer match: YES (3). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 456 / steps 132. iPad risk: low. quality gate: pass.
risk: choice [4] 저장 텍스트 "고속도 자단방식"은 "고속도 차단방식"의 OCR
변형 — 보기 판단은 자명한 뜻(고속 차단)으로 서술. choice-cleanup 후보로 flag.

### 4 — `2015_2회_23` · 전력공학 · answer 4 · 암기형

```
핵심 단서: 중거리 송전선로 π형 회로의 송전단 전류 Is를 묻는다. "π형 회로"가 단서 — 4단자(ABCD) 정수 문제다.

보기 판단: π형의 ABCD는 A=D=1+ZY/2, B=Z, C=Y(1+ZY/4). Is=C·Er+D·Ir = Y(1+ZY/4)Er+(1+ZY/2)Ir → [4]: 정답. [1]은 (1+ZY/2)Er+Z·Ir로 송전단 전압 Es의 식. [2]도 계수가 Es형. [3]은 C가 단순 Y로 π형 C=Y(1+ZY/4)와 다름.

근거/계산: [Es;Is]=[A B;C D][Er;Ir]. 둘째 행 Is = C·Er+D·Ir = Y(1+ZY/4)Er+(1+ZY/2)Ir.

함정: 송전단 전압 Es의 식 [1]과 혼동하기 쉽다 — 묻는 것은 Is(전류)이므로 둘째 행을 쓴다.

시험장 판별: Is는 Er 앞에 C(Y 계열), Ir 앞에 D(1+ZY/2). Y로 시작하는 보기를 고른다.

정답: 4번.
```

steps — `인식`: π형 중거리 송전선로의 송전단 전류 Is를 4단자 정수로 구하는
문제. / `변환`: [Es;Is]=[A B;C D][Er;Ir]. π형: A=D=1+ZY/2, B=Z,
C=Y(1+ZY/4). / `계산`: 둘째 행 Is = C·Er + D·Ir = Y(1+ZY/4)Er + (1+ZY/2)Ir
→ 정답 ④.

self-review — answer match: YES (4). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 461 / steps 154. iPad risk: low-medium. quality gate:
pass.

### 5 — `2015_2회_29` · 전력공학 · answer 2 · 암기형

```
핵심 단서: "이상전압의 파고치를 저감시켜 기기를 보호"하는 설비를 묻는다. 보기마다 설비와 기능이 함께 적혀 있다.

보기 판단: [1] 직렬 리액터는 전력용 콘덴서와 함께 제5고조파를 제거 — 이상전압 저감이 아님. [2] 피뢰기는 뇌·개폐 이상전압을 방전해 파고치를 제한 → 요구와 일치: 정답. [3] 아킹 호온은 섬락 시 애자련을 보호. [4] 아모 로드는 전선 진동에 의한 단선을 막는 보강재.

근거/계산: 피뢰기는 이상전압이 방전 개시 전압을 넘으면 도통해 서지를 대지로 흘리고, 정상 전압으로 돌아오면 속류를 차단한다.

함정: 직렬 리액터도 "보호" 설비라 끌리기 쉽다 — 그것은 고조파 제거용이지 서지 저감용이 아니다.

시험장 판별: "이상전압·파고치·서지"가 보이면 피뢰기.

정답: 2번 (피뢰기).
```

steps — `인식`: 이상전압 파고치를 저감해 기기를 보호하는 설비를 고르는 문제. /
`변환`: 피뢰기=이상전압 방전·파고치 제한 / 직렬 리액터=제5고조파 / 아킹
호온=애자 보호 / 아모 로드=진동 방지. / `계산`: 요구 기능 "이상전압 파고치
저감"에 맞는 설비는 피뢰기 → 정답 ②.

self-review — answer match: YES (2). choice mapping: [1]-[4] all mapped (저장
보기는 "설비 : 기능" 형식이며, 보기 판단은 그 설비명에 대응). label: ok.
length: solution 405 / steps 135. iPad risk: low. quality gate: pass. risk:
choice [4] 저장 텍스트 끝에 페이지 푸터 잔류물(`[답] 15년도 2회 / 439 /
전기기사 펄기 D－60 시리즈`) — 보기 문장 자체는 온전. choice-cleanup 후보로
flag.

### 6 — `2015_3회_25` · 전력공학 · answer 4 · 암기형

```
핵심 단서: 보호 계전기의 "반한시·정한시" 특성의 정의를 묻는다. 두 특성을 결합한 복합 특성이라는 점이 이름 자체에 들어 있다.

보기 판단: [1] 동작전류가 클수록 동작시간이 짧아짐 — 반한시. [2] 최소 동작전류를 넘으면 즉시 동작 — 순한시. [3] 동작전류 크기와 무관하게 일정 시간에 동작 — 정한시. [4] 저전류에서는 반한시(전류↑→시간↓), 일정 전류 이상에서는 정한시(시간 고정) — 두 특성을 결합 → 정답.

근거/계산: 반한시 t∝1/I, 정한시 t=일정. 반한시-정한시는 작은 고장전류에서는 반한시로 빠르게, 큰 고장전류에서는 정한시로 일정하게 동작.

함정: 이름에 "정한시"가 들어 있어 [3](정한시만)을 고르기 쉽다 — "반한시·정한시"는 둘을 결합한 [4]다.

시험장 판별: 보기 문장이 두 구간을 모두 서술하면 결합 특성, 한 구간만 서술하면 단일 특성.

정답: 4번 (반한시-정한시 특성).
```

steps — `인식`: 보호 계전기의 "반한시·정한시" 복합 특성의 정의를 고르는 문제.
/ `변환`: 반한시 t∝1/I / 정한시 t=일정 / 반한시-정한시=두 영역 결합. /
`계산`: 저전류는 반한시, 일정 전류 이상은 정한시로 동작하는 결합 특성 → 정답
④.

self-review — answer match: YES (4). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 468 / steps 118. iPad risk: low. quality gate: pass.
note: `choices`는 `fac4b8d`에서 source PDF로 복구 — 현재 텍스트는 온전.

### 7 — `2016_1회_69` · 전력공학(저장) · answer 4 · 개념형

```
핵심 단서: 주파수 응답으로 안정도를 판정할 때 "안정도 척도와 관계가 적은 것"을 찾는다. 보드선도에서 직접 읽는 상대 안정도 지표인가가 기준.

보기 판단: [1] 공진치 Mp는 응답의 최대 피크로, 크면 감쇠가 작아 안정도가 낮음 → 척도. [2] 위상여유는 이득 0dB에서 위상이 −180°까지 남은 여유 → 대표 척도. [3] 이득여유는 위상 −180°에서 이득이 0dB까지 남은 여유 → 대표 척도. [4] 고유주파수는 계의 고정 파라미터(ωn)일 뿐 상대 안정도를 나타내지 않음 → 관계가 적음: 정답.

근거/계산: 위상여유·이득여유·공진치는 주파수 응답 곡선의 모양에서 상대 안정도를 읽는 양. ωn은 응답의 빠르기를 정할 뿐 감쇠비와 분리된다.

함정: 고유주파수가 응답을 정하니 안정도와도 관계있다고 넘겨짚는다 — 안정/불안정을 가르는 것은 감쇠비(여유)다.

시험장 판별: "여유"가 붙은 보기와 공진치는 척도. "관계 적은 것"은 고유주파수.

정답: 4번 (고유주파수).
```

steps — `인식`: 주파수 응답 기반 안정도 척도와 "관계가 적은 것"을 고르는 문제.
/ `변환`: 위상여유·이득여유·공진치=주파수 응답에서 읽는 상대 안정도 지표 /
고유주파수=계의 고정 파라미터. / `계산`: [4] 고유주파수는 안정도 척도가 아님
→ 정답 ④.

self-review — answer match: YES (4). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 501 / steps 121 — solution이 목표 상한을 1자 초과(아래
Section 5). iPad risk: low-medium. quality gate: pass. note: 저장 subject는
`전력공학`이나 문항 내용(주파수 응답·위상/이득여유)은 제어공학 — subject-label
mismatch 관찰 (Section 6).

### 8 — `2006_1회_7` · 전기자기학 · answer 2 · 계산형

```
핵심 단서: 주어진 전계 E의 발산을 원점에서 구한다. div E = ∂Ex/∂x+∂Ey/∂y+∂Ez/∂z의 합이 출발점.

보기 판단: 각 성분을 자기 변수로 편미분 — ∂Ex/∂x=6e^{3x}sin5y, ∂Ey/∂y=5e^{3x}sin5y는 둘 다 원점(y=0)에서 0. ∂Ez/∂z=3e^{4z}(1+4z)는 원점(z=0)에서 3. 합 0+0+3=3 → [2]. [1] 0은 z항 누락, [3] 6·[4] 10은 x·y항이 0임을 놓친 값.

근거/계산: div E = ∂(2e^{3x}sin5y)/∂x + ∂(−e^{3x}cos5y)/∂y + ∂(3z·e^{4z})/∂z. 원점에서 앞 두 항 sin0=0, 셋째 항 3.

함정: 원점 좌표는 미분을 끝낸 뒤 대입한다 — 미분 전에 sin5y를 0으로 보면 안 된다.

시험장 판별: 원점에서 sin0=0이 되는 항을 지우면 z항만 남는다.

정답: 2번 (발산 = 3).
```

steps — `인식`: 전계 벡터의 발산을 원점에서 구하는 문제. / `변환`: div E =
∂Ex/∂x + ∂Ey/∂y + ∂Ez/∂z. 각 성분을 같은 방향 변수로 편미분. / `계산`:
원점에서 x·y항은 sin5y=0으로 0, z항 3e^{4z}(1+4z)=3. 합 3 → 정답 ②.

self-review — answer match: YES (2). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 465 / steps 132. iPad risk: low. quality gate: pass.
risk: 문제 `text`의 z성분 지수에 OCR 잔류물(`e^{\overline{4z}}`) — 자명한
뜻은 `e^{4z}`. `text`는 수정하지 않음; text-OCR 후보로 flag.

### 9 — `2015_1회_13` · 전기자기학 · answer 1 · 계산형

```
핵심 단서: x방향으로 진행하는 평면 전자파의 포인팅 벡터 크기를 구한다. 직교 두 전계 성분 Ey, Ez가 단서.

보기 판단: S=|E|²/η₀, |E|²=Ey²+Ez²=(9+16)×10⁻⁴sin²=25×10⁻⁴sin². S=25×10⁻⁴/377·sin²≈6.63×10⁻⁶sin² → [1]. [2]는 위상이 cos²로 틀림(E가 sin이면 S∝sin²). [3]·[4]는 지수 10⁻⁴에 1제곱이라 차원·제곱이 모두 틀림.

근거/계산: S=|E|²/η₀, 공기 η₀≈377[Ω]. |E|²=(3²+4²)×10⁻⁴sin²ω(x−vt) → S≈6.63×10⁻⁶sin²ω(x−vt).

함정: 직교 성분은 Ey+Ez로 더하지 않고 √(3²+4²)=5로 합성한다. S∝E²이라 위상은 sin².

시험장 판별: 직교 3·4 → 합성 5, 위상 sin², 지수 10⁻⁶ 대.

정답: 1번 (6.63×10⁻⁶ sin²ω(x−vt)).
```

steps — `인식`: 두 직교 전계 성분이 만드는 평면파의 포인팅 벡터 크기를 구하는
문제. / `변환`: S = |E|²/η₀, |E|²=Ey²+Ez², 공기 η₀≈377[Ω]. / `계산`:
|E|²=(9+16)×10⁻⁴sin²=25×10⁻⁴sin². S≈6.63×10⁻⁶sin² → 정답 ①.

self-review — answer match: YES (1). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 465 / steps 136. iPad risk: low. quality gate: pass.

### 10 — `1998_4회_10` · 전기자기학 · answer 4 · 계산형

```
핵심 단서: 두 자성체 경계면에서 자속밀도 B₂를 구한다. "경계면에 전류가 흐르지 않는다"가 단서 — 법선 B 연속, 접선 H 연속을 쓴다.

보기 판단: x=0 면이 경계 → x가 법선, y·z가 접선. 법선: μR1·H1x=μR2·H2x → 2·2=4·H2x → H2x=1, B2x=4μ0. 접선: H2y=−2, H2z=2 → B2y=−8μ0, B2z=8μ0. B₂=μ0(4ax−8ay+8az) → [4]. [1]·[2]·[3]은 조건을 잘못 적용한 값.

근거/계산: 표면전류 없는 경계조건 — 법선 B 연속, 접선 H 연속. x성분만 B 연속, y·z성분은 H 연속으로 풀어 B₂=μ0μR2·H₂.

함정: 세 성분 모두 같은 조건을 적용하면 [2](8,−8,8) — 법선만 B 연속, 접선은 H 연속으로 갈라 적용한다.

시험장 판별: 경계면 좌표로 법선축을 정하고 "법선=B 연속, 접선=H 연속"을 성분별로 적용.

정답: 4번 (B₂=μ0(4ax−8ay+8az)).
```

steps — `인식`: 두 자성체 경계면에서 자속밀도 B₂를 구하는 문제(표면전류 없음).
/ `변환`: 법선(x) 성분 B 연속, 접선(y·z) 성분 H 연속. B₂=μ0μR2·H₂. /
`계산`: H2x=μR1·2/μR2=1→B2x=4μ0. H2y·H2z 연속→B2y=−8μ0, B2z=8μ0 → 정답
④.

self-review — answer match: YES (4). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 493 / steps 142. iPad risk: low-medium. quality gate:
pass.

### 11 — `2002_3회_4` · 전기자기학 · answer 4 · 개념형

```
핵심 단서: 면전하 분포가 거리 r인 점에 만드는 전위 U를 묻는다. "전위"는 1/r에, 전계는 1/r²에 비례한다는 점이 단서.

보기 판단: 점전하 전위 V=q/(4πεr)를 면전하로 확장 — dq=ρs·dS의 dU=ρs·dS/(4πεr), 전체 U=(1/4πε)∬ρs/r dS → [4]. [1]은 분모가 2πε로 점전하의 4πε가 아님. [2]·[3]은 1/r²로, 전위가 아니라 전계의 거리 의존성이다.

근거/계산: 점전하 전위 V=q/(4πεr)를 dq=ρs·dS로 쪼개 적분 → U=(1/4πε)∬(ρs/r)dS.

함정: 전위와 전계를 혼동해 1/r²을 고른다. r은 점마다 달라 적분 안에 있어야 하며, 밖으로 빼면 [2]·[3]처럼 r²이 나온다.

시험장 판별: "전위"는 1/r·4πε. 1/r²이나 2πε가 보이면 제외.

정답: 4번 (U=(1/4πε)∬ρs/r dS).
```

steps — `인식`: 면전하 분포가 만드는 한 점의 전위 U를 구하는 문제. / `변환`:
점전하 전위 V=q/(4πεr)를 면전하 dq=ρs·dS로 확장해 적분. / `계산`:
dU=ρs·dS/(4πεr) → U=(1/4πε)∬ρs/r dS → 정답 ④.

self-review — answer match: YES (4). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 447 / steps 113. iPad risk: low. quality gate: pass.
risk: choice [4] 저장 텍스트 끝에 페이지 푸터 잔류물(`2-286 / D-60 전기기사`)
— 보기 수식 자체는 온전. choice-cleanup 후보로 flag.

### 12 — `2006_1회_6` · 전기자기학 · answer 3 · 계산형

```
핵심 단서: 유전체로 채운 콘덴서의 t초간 발열량[cal]을 묻는다. 유전율 ε과 고유저항 ρ이 함께 주어진 것이 단서 — 누설저항을 통한 발열이다.

보기 판단: C=εA/d, 누설저항 R=ρd/A → RC=ερ → R=ερ/C. 발열 Q=V²t/R=CV²t/(ερ)[J], cal 환산 0.24를 곱해 Q=0.24·CV²t/(ερ) → [3]. [1]은 환산계수 4.2(cal→J)로 방향이 거꾸로. [2]·[4]는 V²이 아니라 V로 줄열의 제곱을 놓침.

근거/계산: RC=ερ(C=εA/d, R=ρd/A의 곱으로 면적·간격 소거). Q[J]=V²t/R, 1J=0.24cal → Q=0.24·CV²t/(ερ)[cal].

함정: 줄열은 V²에 비례한다 — V로 쓰면 [2]·[4]. cal 환산은 0.24(J→cal)이며 4.2는 역수다.

시험장 판별: RC=ερ → R=ερ/C 대입. 단위 [cal]→0.24, 발열→V². 둘 다 만족하는 보기는 [3].

정답: 3번 (0.24·CV²t/(ρε)).
```

steps — `인식`: 유전체 콘덴서의 누설저항을 통한 t초간 발열량[cal]을 구하는
문제. / `변환`: RC=ερ → R=ερ/C. Q[J]=V²t/R, 1J=0.24cal. / `계산`:
Q=V²t/R=CV²t/(ερ)[J] → Q=0.24·CV²t/(ερ)[cal] → 정답 ③.

self-review — answer match: YES (3). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 511 / steps 130 — solution이 목표 상한을 11자 초과
(Section 5). iPad risk: low-medium. quality gate: pass.

### 13 — `2015_1회_71` · 전기자기학(저장) · answer 1 · 계산형

```
핵심 단서: 솔레노이드의 권수·자속·전류·저항이 주어지고 "시정수"를 구한다. 시정수는 R-L 회로의 과도현상 양 τ=L/R이며, 먼저 인덕턴스 L을 구한다.

보기 판단: 쇄교 자속으로 L 산출 — L=N·φ/I=(2000×6×10⁻²)/10=120/10=12[H]. 시정수 τ=L/R=12/12=1[sec] → [1]. [2]·[3]·[4]는 L 계산에서 권수 N을 빠뜨리거나 자릿수를 잘못 잡은 값.

근거/계산: 인덕턴스 정의 L=N·φ/I (쇄교 자속/전류). N=2000, φ=6×10⁻²Wb, I=10A → L=12H. 시정수 τ=L/R=12/12=1초.

함정: φ만 보고 L≈φ/I로 N을 빠뜨리면 L이 작아져 τ도 한참 작아진다 — 쇄교 자속은 N·φ다.

시험장 판별: τ=L/R, L은 N·φ/I로 먼저 구한다. N을 곱하면 12H, τ=1초.

정답: 1번 (1초).
```

steps — `인식`: 솔레노이드 R-L 회로의 시정수 τ를 구하는 문제. / `변환`:
인덕턴스 L=N·φ/I(쇄교 자속/전류), R-L 시정수 τ=L/R. / `계산`:
L=2000×6×10⁻²/10=12[H]. τ=L/R=12/12=1[sec] → 정답 ①.

self-review — answer match: YES (1). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 442 / steps 116. iPad risk: low. quality gate: pass.
note: 저장 subject는 `전기자기학`이나 문항 내용(시정수 τ=L/R, R-L 과도)은
회로이론에 가까움 — subject-label mismatch 관찰 (Section 6).

### 14 — `2016_3회_44` · 전기기기 · answer 4 · 암기형

```
핵심 단서: 변압기에서 철손을 측정하는 시험을 묻는다. 철손이 무부하손이라는 점이 시험 선택의 기준.

보기 판단: [1] 유도시험은 철손 측정의 표준 시험명이 아님. [2] 단락시험은 2차를 단락하고 정격전류를 흘려 동손(부하손)을 구함 — 철손이 아님. [3] 부하시험은 효율·전압변동을 보는 시험. [4] 무부하시험은 2차를 개방하고 1차에 정격전압을 가해 입력전력으로 철손을 측정 → 정답.

근거/계산: 무부하시험은 부하전류가 거의 0이라 동손이 무시되고 입력전력이 곧 철손(히스테리시스손+와류손)이 된다.

함정: "철"에 끌려 단락시험과 헷갈리거나, 부하를 걸어야 손실이 보인다고 [3]을 고른다 — 철손은 무부하손이다.

시험장 판별: 무부하시험=철손, 단락시험=동손으로 짝지어 외운다.

정답: 4번 (무부하시험).
```

steps — `인식`: 변압기 철손을 측정하는 시험을 고르는 문제. / `변환`:
철손=무부하손(정격전압 인가, 부하 무관) / 동손=부하손(단락시험). / `계산`:
2차 개방·정격전압 인가하는 무부하시험의 입력전력=철손 → 정답 ④.

self-review — answer match: YES (4). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 409 / steps 101. iPad risk: low. quality gate: pass.

### 15 — `2001_3회_43` · 전기기기 · answer 2 · 개념형

```
핵심 단서: 정류자형 주파수 변환기의 설명 중 "틀린 것"을 고른다. 권선이 회전자·고정자 중 어디에 놓이는가가 보기를 가른다.

보기 판단: [1] 한 자극마다 전기각 2π/3(120°) 간격 3조 브러시 — 3상 대칭 출력용 정상 배치: 옳음. [2] "1차·조정권선을 회전자에, 2차 권선을 고정자에" — 표준은 1차·조정권선이 고정자, 2차가 회전자로, 회전자·고정자가 뒤바뀜: 틀린 설명 → 정답. [3] 3개 슬립링이 회전자 권선 3등분점에 접속: 옳음. [4] 대용량기는 정류 개선을 위해 보상권선·보극권선을 고정자에 설치: 옳음.

근거/계산: 정류자형 주파수 변환기는 유도전동기 2차 여자용 특수기로, 1차·조정권선은 고정자, 2차 권선은 회전자에 두는 것이 표준 구조다.

함정: [2]는 문장이 그럴듯해 옳게 읽기 쉽다 — 권선의 회전자/고정자 위치가 뒤바뀐 것이 오류다.

시험장 판별: "틀린 것" — 권선 배치 보기에서 회전자·고정자가 표준과 뒤바뀐 것을 찾는다.

정답: 2번 (회전자·고정자 권선 배치가 뒤바뀐 설명).
```

steps — `인식`: 정류자형 주파수 변환기의 설명 중 "틀린 것"을 고르는 개념 문제.
/ `변환`: 표준 구조 — 1차·조정권선은 고정자, 2차 권선은 회전자에 설치. /
`계산`: [2]는 1차·조정권선을 회전자, 2차를 고정자로 서술해 배치가 뒤바뀜 →
틀린 설명 → 정답 ②.

self-review — answer match: YES (2; manifest source 【답】②, pack1 `4317aea`).
choice mapping: [1]-[4] all mapped. label: ok. length: solution 530 / steps
129 — solution이 목표 상한을 30자 초과 (Section 5). iPad risk: medium.
**content risk: MEDIUM** — 정류자형 주파수 변환기는 출제 빈도가 낮은 특수기.
보기 [2]의 오류 판정은 "1차·조정권선=고정자, 2차=회전자"라는 표준 권선 배치에
의존한다. 정답(②)은 source 【답】로 확정되어 있으나, 오류 내용의 정밀 서술은
apply 전 교재 source spot-check 권장. `choices`는 `fac4b8d`에서 복구됨.

### 16 — `2016_1회_44` · 전기기기 · answer 4 · 암기형

> 보정 2026-05-21: `solution`을 548 → 491자로 trim (≤500 목표 달성). 정답·
> 보기 판단·근거 구조 유지. 보정 경위는
> `docs/audit/answer_selection_pedagogy_expansion_correction_2026-05-21.md`.

```
핵심 단서: 직류기 전기자 반작용의 영향이 "아닌 것"을 고른다. 반작용의 3대 영향과 정류 과정의 별개 현상을 구분한다.

보기 판단: [1] 전기자 자속이 주자속을 약화(감자작용) → 자속·유기기전력 감소: 영향. [2] 발전기는 회전 방향으로, [3] 전동기는 그 반대 방향으로 중성축 이동: 둘 다 영향. [4] 브러시로 단락된 코일의 기전력으로 유기기전력이 "증가"한다 — 반작용은 감자작용으로 기전력을 감소시켜 방향이 정반대이고, 단락 코일 기전력은 정류 과정의 별개 현상 → 영향이 아님: 정답.

근거/계산: 전기자 반작용 = 감자작용(주자속·기전력 감소) + 편자작용(중성축 이동) + 정류 악화. 이 3대 영향에 "기전력 증가"는 없다.

함정: [4]의 "기전력 증가"는 반작용(감자작용)의 결과와 정반대다.

시험장 판별: "유기기전력 증가"가 보이면 반작용의 영향이 아니다.

정답: 4번 (브러시 사이 유기기전력 증가 — 전기자 반작용의 영향이 아님).
```

steps — `인식`: 직류기 전기자 반작용의 영향이 "아닌 것"을 고르는 문제. /
`변환`: 전기자 반작용=감자작용(기전력 감소)+중성축 이동+정류 악화. 단락 코일
기전력=정류의 리액턴스 전압(별개). / `계산`: [4] 유기기전력 "증가"는 감자작용
(감소)과 반대이며 정류 현상 → 영향 아님 → 정답 ④.

self-review — answer match: YES (4). choice mapping: [1]-[4] all mapped (보정본
[2]·[3]을 한 문장에 합쳤으나 두 보기 모두 명시 참조). label: ok, 6 elements,
`정답:` last. length: solution 491 / steps 145 — solution 목표 350-500 범위
내(보정 후). iPad risk: low-medium. quality gate: pass. note: 원안 548자에서
`근거/계산` 중복 문장 제거 + `함정`/`시험장 판별` 압축으로 trim.

### 17 — `2016_1회_71` · 제어공학(저장) · answer 3 · 암기형

```
핵심 단서: 평형 3상 △(델타) 결선에서 선간전압 E_l과 상전압 E_p의 관계를 묻는다. 상권선이 두 선 사이에 직접 걸리는 결선 구조가 답을 정한다.

보기 판단: △결선은 한 상의 권선 양끝이 곧 두 선이므로 선간전압=상전압 → E_l=E_p → [3]. [1] √3배는 Y(스타) 결선의 전압 관계. [2] 3배는 어떤 결선에도 없음. [4] 1/√3배는 Y 관계의 역수로 거꾸로다.

근거/계산: △결선은 E_l=E_p이고 선전류=√3·상전류. Y결선은 반대로 E_l=√3·E_p, 선전류=상전류.

함정: Y의 "√3배"를 결선 구분 없이 외워 [1]을 고른다 — √3은 Y의 전압, △의 전류에 나타난다.

시험장 판별: "△=전압 같다, Y=전류 같다"로 외운다. △+전압 → E_l=E_p.

정답: 3번 (E_l = E_p).
```

steps — `인식`: 평형 3상 △결선의 선간전압과 상전압의 관계를 고르는 문제. /
`변환`: △결선=각 상권선이 두 선 사이에 직결 → 선간전압=상전압. / `계산`:
E_l=E_p → 정답 ③. 선간·상 전압의 √3배 관계는 Y(스타) 결선의 특성이다.

self-review — answer match: YES (3). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 417 / steps 114. iPad risk: low. quality gate: pass.
risk: choice [4] 저장 텍스트에 LaTeX 잔류물(`rac{1}{\sqrt{3}}` — 백슬래시
누락) — 자명한 뜻은 1/√3. choice-cleanup 후보로 flag. note: 저장 subject는
`제어공학`이나 문항 내용(3상 △/Y 결선)은 회로이론 — subject-label mismatch
관찰 (Section 6).

### 18 — `2001_1회_68` · 제어공학 · answer 3 · 암기형

```
핵심 단서: Ks=lim_{s→0}s²G(s)H(s)의 이름을 묻는다. s의 차수(s²)와 "포물선 입력"이 단서 — 오차상수 3종을 입력 형태로 구분한다.

보기 판단: 계단 입력 → 위치상수 Kp=lim G·H(s⁰). 램프 입력 → 속도상수 Kv=lim s·G·H. 포물선 입력 → 가속도상수 Ka=lim s²·G·H. 문제 식은 s²이고 입력이 포물선이므로 [3] 가속도 오차 상수. [1] 위치는 s⁰, [2] 속도는 s¹이라 차수가 다름. [4] "평면 오차 상수"는 없는 용어다.

근거/계산: 정상상태 오차 e_ss는 입력 차수에 대응하는 오차상수로 정해진다 — 포물선 입력 e_ss=1/Ka, Ka=lim_{s→0}s²G(s)H(s).

함정: s의 차수와 입력 이름을 잘못 짝지으면 [1]·[2]로 빠진다 — s⁰=위치, s¹=속도, s²=가속도.

시험장 판별: s의 지수를 센다 — 0=위치, 1=속도, 2=가속도. s²이면 가속도 오차 상수.

정답: 3번 (가속도 오차 상수).
```

steps — `인식`: Ks=lim_{s→0}s²G(s)H(s)의 명칭을 고르는 문제. / `변환`:
오차상수는 입력별 — 계단=위치(s⁰), 램프=속도(s¹), 포물선=가속도(s²). /
`계산`: s²·G·H의 극한 + 포물선 입력 → 가속도 오차 상수 → 정답 ③.

self-review — answer match: YES (3). choice mapping: [1]-[4] all mapped. label:
ok. length: solution 505 / steps 120 — solution이 목표 상한을 5자 초과
(Section 5). iPad risk: low-medium. quality gate: pass.

---

## 5. Summary

| # | key | subject | answer | quality gate | solution chars | steps chars | flag | apply_status |
| --- | --- | --- | ---: | --- | ---: | ---: | --- | --- |
| 1 | `2001_1회_21` | 전력공학 | 2 | pass | 453 | 152 | — | not_applied |
| 2 | `2015_1회_22` | 전력공학 | 1 | pass | 452 | 141 | choice [2] OCR | not_applied |
| 3 | `2015_3회_27` | 전력공학 | 3 | pass | 456 | 132 | choice [4] OCR | not_applied |
| 4 | `2015_2회_23` | 전력공학 | 4 | pass | 461 | 154 | — | not_applied |
| 5 | `2015_2회_29` | 전력공학 | 2 | pass | 405 | 135 | choice [4] residue | not_applied |
| 6 | `2015_3회_25` | 전력공학 | 4 | pass | 468 | 118 | — | not_applied |
| 7 | `2016_1회_69` | 전력공학 | 4 | pass | 501 | 121 | len +1; subject-label | not_applied |
| 8 | `2006_1회_7` | 전기자기학 | 2 | pass | 465 | 132 | text OCR (z항) | not_applied |
| 9 | `2015_1회_13` | 전기자기학 | 1 | pass | 465 | 136 | — | not_applied |
| 10 | `1998_4회_10` | 전기자기학 | 4 | pass | 493 | 142 | — | not_applied |
| 11 | `2002_3회_4` | 전기자기학 | 4 | pass | 447 | 113 | choice [4] residue | not_applied |
| 12 | `2006_1회_6` | 전기자기학 | 3 | pass | 511 | 130 | len +11 | not_applied |
| 13 | `2015_1회_71` | 전기자기학 | 1 | pass | 442 | 116 | subject-label | not_applied |
| 14 | `2016_3회_44` | 전기기기 | 4 | pass | 409 | 101 | — | not_applied |
| 15 | `2001_3회_43` | 전기기기 | 2 | pass | 530 | 129 | len +30; content risk MEDIUM | not_applied |
| 16 | `2016_1회_44` | 전기기기 | 4 | pass | 491 (보정) | 145 | trimmed 548→491 | not_applied |
| 17 | `2016_1회_71` | 제어공학 | 3 | pass | 417 | 114 | choice [4] residue; subject-label | not_applied |
| 18 | `2001_1회_68` | 제어공학 | 3 | pass | 505 | 120 | len +5 | not_applied |

Quality gate (per item): answer matches `q.answer`, every choice explanation
maps to an actual stored choice, no invented source/article/statute, no
unsupported cross-subject claim, no contradiction with the source answer.
All 18 drafts pass.

### Length

- `solution`: 405-548 chars; target is 350-500 (v2.1). 13/18 within target;
  5 over — `2016_1회_69` 501, `2001_1회_68` 505, `2006_1회_6` 511,
  `2001_3회_43` 530, `2016_1회_44` 548. The 5 are all 4-choice items whose
  per-choice `보기 판단` carries the pedagogy weight; further trimming would
  cut choice-judgment substance. All 5 are still below the pilot's applied
  range (512-678, `2aadbe5`, review 7/7 `keep`). The final length call is
  deferred to apply-prep, alongside the iPad / browser viewport check the
  supervisor moved to the limited-apply gate.
- `steps`: 101-154 chars; target 100-180. All 18 within target.

### Choice-OCR / text-OCR flags (6 items)

`2015_1회_22` choice [2] (`직접`→`적게`), `2015_3회_27` choice [4]
(`자단`→`차단`), `2015_2회_29` choice [4] (trailing footer residue),
`2002_3회_4` choice [4] (trailing footer residue), `2016_1회_71` choice [4]
(LaTeX residue `rac{` → `\frac{`), `2006_1회_7` `text` z-component (OCR
residue `\overline`). None is answer-corrupting — the answer-relevant meaning
is readable in every case, and each draft references the evident meaning
(the same handling the pilot used). `choices` / `text` are NOT modified here.
Recommendation: a small choice/text-cleanup pass for these 6 before the
pedagogy apply, OR proceed describing the evident meaning — a supervisor
decision (same choice as the pilot's).

### Content risk

`2001_3회_43` (정류자형 주파수 변환기) — MEDIUM. The answer (②) is fixed by
the source 【답】 marker (manifest `4317aea`), but the precise wording of why
choice [2] is wrong rests on the standard winding arrangement of an
infrequently-tested special machine. Recommend a textbook source spot-check
before this item's apply.

### `다른 과목 연결` omitted for all 18

The conditional cross-subject element is included by the v2.1 template only
when a genuine, exam-relevant link exists, and forced links are prohibited.
No item in this 18-item pool has a link as strong as the pilot's
`2007_2회_64` (Routh-Hurwitz 회로↔제어). Two borderline links exist —
`2016_1회_71` (△/Y 결선, used in 전력공학·전기기기 변압기 결선) and
`2015_1회_71` (시정수 τ=L/R, core 회로이론) — and may be added at apply-prep
if wanted; they were left out here to avoid forcing.

### Subject-label observations (not modified)

Three items have a stored `subject` that does not match the question content:
`2016_1회_69` (저장 전력공학 / 내용 제어공학), `2016_1회_71` (저장 제어공학 /
내용 회로이론 3상 결선), `2015_1회_71` (저장 전기자기학 / 내용 회로이론 R-L
시정수). `subject` is metadata and is OUT OF SCOPE here — this dry-run drafts
only `solution` / `steps`. Recorded as an observation for a possible separate
metadata-audit track.

## 6. Judgment

- The 18 items are source-verified (9 verified + 9 C20-corrected) and
  answer/choices-mappable clean candidates; they are appropriate dry-run
  targets. Every draft passes the quality gate, with answer-locked
  conclusions matching `q.answer`.
- The batch was planned at 20 but executed at 18. The 2-item shortfall was
  NOT filled — padding would have required statute items (article-fabrication
  risk) or non-source-verified items (breaking the source-verified premise).
  Holding quality over the round number is the deliberate choice, consistent
  with the track's conservative principle.
- The next batch resumes the 20-unit rhythm after additional source-verified
  clean candidates are secured (e.g. a further source-verification pass on
  the broader corpus, or resolving the 3 excluded items via the statute-safe
  / DQ tracks).
- Before any apply: supervisor review of this dry-run, a decision on the
  6 choice/text-OCR flags, a closer source check for `2001_3회_43`, and the
  length call on the 5 over-target solutions — all at apply-prep, with the
  iPad / browser viewport check as the limited-apply quality gate.

## Not done in this step

- No `app/data/questions.json` modification.
- No `app/data/questions.v2.json` modification.
- No `solution` / `steps` apply.
- No `answer` / `choices` modification.
- No app code or schema modification.
- No `subject` metadata modification.
- No expansion apply; no bulk apply.
- No paid API call.
- No commit; no push.

## Status

- Expansion solution dry-run complete for 18 verified-clean candidates
  (planned 20, executed 18 due to safety exclusions). The v2.1 plain-text
  template fits all 18; every draft passes the quality gate.
- 3 items excluded for safety (2 statute, 1 corrupted answer choice), routed
  to the statute-safe / DQ tracks.
- No `app/data` modification. Next (separate approval): supervisor review of
  this dry-run, then a limited pedagogy `solution` / `steps` apply with its
  own approval, the OCR-cleanup decision, and the iPad viewport gate.
