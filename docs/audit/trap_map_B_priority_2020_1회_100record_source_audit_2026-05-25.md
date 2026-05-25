# Trap-Map B-Priority — 2020_1회 100 Record Source Audit (2026-05-25)

S2 — 100 records 전수 source audit. read-only. data 수정 0. caution release / registry 확장 / Batch migration / missing 29 recovery / resolver implementation 모두 0.

- 관련 plan: `docs/audit/trap_map_B_priority_2020_1회_100record_source_audit_plan_2026-05-25.md` (2d2c176 + 보강 dbad447)
- 관련 plan review: `docs/audit/trap_map_B_priority_2020_1회_100record_source_audit_plan_review_2026-05-25.md` (c0b7362, PASS 12/12)
- 관련 closeout: `docs/audit/trap_map_B_priority_gigi_17_B_track_docs_baseline_closeout_2026-05-25.md` (aeca5a4, `DR-TRAP-GIGI17-BTRACK-DOCS-BASELINE-CLOSEOUT`)
- 관련 E6 separability: `docs/audit/trap_map_B_priority_2020_session_namespace_E6_separability_reevaluation_2026-05-25.md` (a787cc3, `DR-TRAP-GIGI17-SEPARABILITY-REEVAL`)
- 관련 impact audit: `docs/audit/trap_map_B_priority_gigi_17_B_track_impact_audit_2026-05-25.md` (3a5bad5)
- 관련 registry artifact: `docs/audit/registries/trap_map_gigi_17_alias_registry_2026-05-25.json` (9868f95, q52 row candidate)

---

## 1. Scope / Guardrails

본 audit은 **2020_1회 100 records의 PDF source 영역 read-only 전수 매핑** 한정.

**guardrails 영역**:
- data 수정 / registry artifact 수정 / registry framing 확장 / caution release / Batch migration / missing 29 recovery / resolver implementation 모두 0
- PDF 복사 / rename / 편집 / OCR 산출물 생성 0
- 임시 결과는 `/tmp/audit_results.json` (최종 repo 영역 외)
- q52 storage_id `2020_1회_52` Permanent Invariant 영역 유지 — 본 audit 결과는 systemic 영역 evidence input 한정, 단독 변경 영역 영구 금지 유지
- 기기-17 caution 유지
- registry row status=candidate 유지
- 66항 policy defer 유지
- caution release 차단 유지
- 본 audit 정책 변경 0 → JSONL entry 추가 0 (사용자 가이드: docs-only audit + 정책 변경 0)

## 2. Method

| step | 영역 |
|---|---|
| input PDF | `data/20200424_1회.pdf` (9 pages, 표지 명시 "2022년 04월 24일 필기 기출문제") |
| input per-year | `data/questions_기출_2020_1회.json` (100 records, q_no 1~100) |
| input master cross-check | `app/data/questions.json` year=2020 session=1회 (100 records, per-year ↔ master 100% 정합 — E2 5f1c9c5 재확인) |
| parse | PyMuPDF (fitz) per-page text extraction → regex `^\s*(\d{1,3})\.\s+(.+)` q_no marker |
| match | record text head 30 chars (normalize: whitespace + non-alphanumeric 제거) vs PDF text prefix |
| classify | score >=0.9 = matched / 0.5~0.9 = partial strong / 0.2~0.5 = partial inferred / <0.2 = mismatch / regex parse 누락 = manual verify (page raw text 직접 측정) |
| q52 별도 측정 | N1 audit + impact audit + registry artifact baseline 정합 — p.4 q52 직접 측정 |

**regex parse 한계 영역** (3건):
- q65 ("의 역 z 변환은?") — 수식 image 시작, 본문 단어 짧음 → regex `len(rest) < 5` skip
- q79 ("회로에서 , I3= ...") — 회로 image 영역 + 수식 시작 → regex skip
- q80 ("는?") — 수식 image 직후 본문 단일 어구 → regex skip

**3건 manual verify**: page 5 / page 7 raw text 직접 측정 → 모두 PDF q_no 본문 정확 존재 + per-year record text 일치 확정. PDF 실제 부재 영역 아님.

## 3. Summary Counts

### 3.1 pdf_match_status

| status | count | % |
|---|---:|---:|
| matched | 100 | 100% |
| mismatch | 0 | 0% |
| partial | 0 | 0% |
| not_found | 0 | 0% |
| uncertain | 0 | 0% |

### 3.2 confidence_level

| level | count | % |
|---|---:|---:|
| source-internal confirmed | 100 | 100% |
| strong hypothesis | 0 | 0% |
| inferred | 0 | 0% |
| unmatched | 0 | 0% |

**중요 (L-1 plan 보강 영역 정합)**: confidence = **source-internal confirmed** (PDF text + record text + page 3-way 정합). 외부 official source (한국기술자격검정 공식 2020/2022 시행 기록) 부재 영역에서는 *확정* 영역으로 승급 안 함 — 모든 record는 *source-internal confirmed* / *강한 가설* 상한 영역 유지.

### 3.3 per-subject 분포 (per-year JSON record subject 라벨 기준)

| subject | count |
|---|---:|
| 전력공학 | 30 |
| 전기자기학 | 20 |
| 전기기기 | 20 |
| 제어공학 | 15 |
| 전기설비기술기준 | 9 |
| 회로이론 | 6 |
| **total** | **100** |

**catch 영역**: 본 분포는 표준 전기기사 시험 5과목 × 20문항 분포 영역 아님. per-year JSON subject 라벨 영역의 별 catch (본 audit scope 영역 외 — 별 트랙 1·3·4 verification 영역과 정합 가능성). 본 audit은 source PDF match 영역 한정.

### 3.4 per-page q_no 분포 (PDF parse 결과)

| page | q_no range | count |
|---:|---|---:|
| p.1 | q1~q11 | 11 |
| p.2 | q12~q23 | 12 |
| p.3 | q24~q38 | 15 |
| p.4 | q39~q53 | 15 (q52 포함) |
| p.5 | q54~q67 | 14 (q65 포함) |
| p.6 | q68~q75 | 8 |
| p.7 | q76~q83 | 8 (q79, q80 포함) |
| p.8 | q84~q100 | 17 |
| **total** | q1~q100 | **100** |

## 4. q52 Finding

| field | value |
|---|---|
| storage_id | `2020_1회_52` (**Permanent Invariant 영역, 단독 변경 영구 금지**) |
| canonical candidate | `2022_1회_52` (registry artifact baseline 정합) |
| source PDF | `data/20200424_1회.pdf` p.4 q52 |
| source text head | "권수비가 a인 단상변압기 3대가 있다. 이것을 1차에 △, 2차에 Y로 결선하여 3상 교류 평형회로에 접속할 때 2차측의 단자전압을 V(V)..." |
| PDF 본문 일치 | source-internal confirmed (score 1.0, 정확 일치) |
| PDF 표지 시행 일자 | 2022년 04월 24일 (2022-04-24) |
| subject (per-year) | 전기기기 (3과목) |

q52는 N1 audit + impact audit + registry artifact baseline과 정확 일치. 본 audit으로 q52는 systemic 1 사례 영역 재확인 — 100/100 mis-label 영역의 1 instance.

**Permanent Invariant 영역 유지**: q52 storage_id 단독 변경 영역 영구 금지 (E6 §3 + plan §7). 본 audit 결과는 systemic 영역 evidence input 한정. 단독 storage_id 변경 영역 진입 0.

## 5. 100-Record Table

| storage_id | q_no | subject | text_short | status | conf | page | notes |
|---|---:|---|---|---|---|---:|---|
| `2020_1회_1` | 1 | 전기자기학 | εr = 81, μr = 1 인 매질의 고유 임피던스는 약 몇 Ω 인가? (단, εr은 비유전율이고, μr은 | matched | source-internal confirmed | 1 |  |
| `2020_1회_2` | 2 | 전기자기학 | 강자성체의 B-H 곡선을 자세히 관찰하면 매끈한 곡선이 아 니라 자속밀도가 어느 순간 급격히 계단적으로 증가 | matched | source-internal confirmed | 1 |  |
| `2020_1회_3` | 3 | 전기자기학 | 진공 중에 무한 평면도체와 d(m)만큼 떨어진 곳에 선전하밀 도 λ(C/m)의 무한 직선도체가 평행하게 놓여 | matched | source-internal confirmed | 1 |  |
| `2020_1회_4` | 4 | 전기자기학 | 평행 극판 사이에 유전율이 각각 ε1, ε2 인 유전체를 그림과 같이 채우고, 극판 사이에 일정한 전압을 걸 | matched | source-internal confirmed | 1 |  |
| `2020_1회_5` | 5 | 전기자기학 | 정전용량이 20μF인 공기의 평행판 커패시터에 0.1C의 전하 량을 충전하였다. 두 평행판 사이에 비유전율이 | matched | source-internal confirmed | 1 |  |
| `2020_1회_6` | 6 | 전기자기학 | 유전율이 ε1과 ε2인 두 유전체가 경계를 이루어 평행하게 접 하고 있는 경우 유전율이 ε1인 영역에 전하  | matched | source-internal confirmed | 1 |  |
| `2020_1회_7` | 7 | 전기자기학 | 단면적이 균일한 환상철심에 권수 100회인 A코일과 권수 400회인 B코일이 있을 때 A코일의 자기 인덕턴스 | matched | source-internal confirmed | 1 |  |
| `2020_1회_8` | 8 | 전기자기학 | 평균 자로의 길이가 10cm, 평균 단면적이 2cm2인 환상 솔레 노이드의 자기 인덕턴스를 5.4mH 정도로 | matched | source-internal confirmed | 1 |  |
| `2020_1회_9` | 9 | 전기자기학 | 투자율이 μ(H/m), 단면적이 S(m2), 길이가 l(m)인 자성체에 권선을 N회 감아서 I(A)의 전류를 | matched | source-internal confirmed | 1 |  |
| `2020_1회_10` | 10 | 전기자기학 | 그림은 커패시터의 유전체 내에 흐르는 변위전류를 보여준 다. 커패시터의 전극 면적을 S(m2), 전극에 축적 | matched | source-internal confirmed | 1 |  |
| `2020_1회_11` | 11 | 전기자기학 | 진공 중에서 점(1, 3)m의 위치에 -2×10-9C의 점전하가 있 을 때 점(2, 1)m에 있는 1C의 점 | matched | source-internal confirmed | 1 |  |
| `2020_1회_12` | 12 | 전기자기학 | 정전용량이 C0(μF)인 평행판의 공기 커패시터가 있다. 두 극판 사이에 극판과 평행하게 절반을 비유전율이  | matched | source-internal confirmed | 2 |  |
| `2020_1회_13` | 13 | 전기자기학 | 그림과 같이 점 O를 중심으로 반지름이 a(m)인 구도체 1과 안쪽 반지름이 b(m)이고 바깥쪽 반지름이 C | matched | source-internal confirmed | 2 |  |
| `2020_1회_14` | 14 | 전기자기학 | 자계의 세기를 나타내는 단위가 아닌 것은? | matched | source-internal confirmed | 2 |  |
| `2020_1회_15` | 15 | 전기자기학 | 그림과 같이 평행한 무한장 직선의 두 도선에 I(A), 4I(A)인 전류가 각각 흐른다. 두 도선 사이 점  | matched | source-internal confirmed | 2 |  |
| `2020_1회_16` | 16 | 전기자기학 | 내압 및 정전용량이 각각 1000V –2μF, 700V –3μF, 600V – 4μF, 300V -8μF인  | matched | source-internal confirmed | 2 |  |
| `2020_1회_17` | 17 | 전기자기학 | 반지름이 2m이고, 권수가 120회인 원형코일 중심에서의 자 계의 세기를 30 AT/m로 하려면 원형코일에  | matched | source-internal confirmed | 2 |  |
| `2020_1회_18` | 18 | 전기자기학 | 내구의 반지름이 a = 5cm, 외구의 반지름이 b = 10cm 이 고, 공기로 채워진 동심구형 커패시터의  | matched | source-internal confirmed | 2 |  |
| `2020_1회_19` | 19 | 전기자기학 | 자성체의 종류에 대한 설명으로 옳은 것은? (단, χm는 자화 율이고, μr는 비투자율이다.) | matched | source-internal confirmed | 2 |  |
| `2020_1회_20` | 20 | 전기자기학 | 구좌표계에서 ∇2r 의 값은 얼마인가? (단, ) | matched | source-internal confirmed | 2 |  |
| `2020_1회_21` | 21 | 전력공학 | 피뢰기의 충격방전 개시전압은 무엇으로 표시하는가? | matched | source-internal confirmed | 2 |  |
| `2020_1회_22` | 22 | 전력공학 | 전력용 콘덴서에 비해 동기조상기의 이점으로 옳은 것은? | matched | source-internal confirmed | 2 |  |
| `2020_1회_23` | 23 | 전력공학 | 단락 보호방식에 관한 설명으로 틀린 것은? 2과목 : 전력공학 | matched | source-internal confirmed | 2 |  |
| `2020_1회_24` | 24 | 전력공학 | 밸런서의 설치가 가장 필요한 배전방식은? | matched | source-internal confirmed | 3 |  |
| `2020_1회_25` | 25 | 전력공학 | 부하전류가 흐르는 전로는 개폐할 수 없으나 기기의 점검이 나 수리를 위하여 회로를 분리하거나, 계통의 접속을 | matched | source-internal confirmed | 3 |  |
| `2020_1회_26` | 26 | 전력공학 | 정전용량 0.01μF/km, 길이 173.2km, 선간전압 60kV, 주파 수 60Hz인 3상 송전선로의 충 | matched | source-internal confirmed | 3 |  |
| `2020_1회_27` | 27 | 전력공학 | 보호계전기의 반한시ㆍ정한시 특성은? | matched | source-internal confirmed | 3 |  |
| `2020_1회_28` | 28 | 전력공학 | 전력계통의 안정도에서 안정도의 종류에 해당하지 않는 것 은? | matched | source-internal confirmed | 3 |  |
| `2020_1회_29` | 29 | 전력공학 | 배전선로의 역률 개선에 따른 효과로 적합하지 않은 것은? | matched | source-internal confirmed | 3 |  |
| `2020_1회_30` | 30 | 전기기기 | 저압뱅킹 배전방식에서 캐스케이딩현상을 방지하기 위하여 인접 변압기를 연락하는 저압선의 중간에 설치하는 것으로 | matched | source-internal confirmed | 3 |  |
| `2020_1회_31` | 31 | 전력공학 | 승압기에 의하여 전압 Ve에서 Vh로 승압할 때, 2차 정격전 압 e, 자기용량 W인 단상 승압기가 공급할  | matched | source-internal confirmed | 3 |  |
| `2020_1회_32` | 32 | 전력공학 | 배기가스의 여열을 이용해서 보일러에 공급되는 급수를 예 열함으로써 연료 소비량을 줄이거나 증발량을 증가시키기 | matched | source-internal confirmed | 3 |  |
| `2020_1회_33` | 33 | 전력공학 | 직렬콘덴서를 선로에 삽입할 때의 이점이 아닌 것은? | matched | source-internal confirmed | 3 |  |
| `2020_1회_34` | 34 | 전력공학 | 전선의 굵기가 균일하고 부하가 균등하게 분산되어 있는 배 전선로의 전력손실은 전체 부하가 선로 말단에 집중되 | matched | source-internal confirmed | 3 |  |
| `2020_1회_35` | 35 | 전력공학 | 송전단 전압 161kV, 수전단 전압 154kV, 상차각 35°, 리액 턴스 60Ω 일 때 선로 손실을 무시 | matched | source-internal confirmed | 3 |  |
| `2020_1회_36` | 36 | 전력공학 | 직접접지방식에 대한 설명으로 틀린 것은? | matched | source-internal confirmed | 3 |  |
| `2020_1회_37` | 37 | 전력공학 | 그림과 같이 지지점 A, B, C에는 고저차가 없으며, 경간 AB와 BC 사이에 전선이 가설되어 그 이도가  | matched | source-internal confirmed | 3 |  |
| `2020_1회_38` | 38 | 전력공학 | 수차의 캐비테이션 방지책으로 틀린 것은? | matched | source-internal confirmed | 3 |  |
| `2020_1회_39` | 39 | 전력공학 | 송전선로에 매설지선을 설치하는 목적은? | matched | source-internal confirmed | 4 |  |
| `2020_1회_40` | 40 | 전기기기 | 1회선 송전선과 변압기의 조합에서 변압기의 여자 어드미턴 스를 무시하였을 경우 송수전단의 관계를 나타내는 4 | matched | source-internal confirmed | 4 |  |
| `2020_1회_41` | 41 | 전기기기 | 단상 변압기의 무부하 상태에서 V1 = 200sin(ωt+30°)(V) 의 전압이 인가되었을 때 Io = 3 | matched | source-internal confirmed | 4 |  |
| `2020_1회_42` | 42 | 전기기기 | 단상 직권 정류자 전동기의 전기자 권선과 계자 권선에 대 한 설명으로 틀린 것은? | matched | source-internal confirmed | 4 |  |
| `2020_1회_43` | 43 | 전기기기 | 전부하시의 단자전압이 무부하시의 단자전압보다 높은 직류 발전기는? | matched | source-internal confirmed | 4 |  |
| `2020_1회_44` | 44 | 전기기기 | 직류기의 다중 중권 권선법에서 전기자 병렬회로 수 a와 극 수 P 사이의 관계로 옳은 것은? (단, m은 다 | matched | source-internal confirmed | 4 |  |
| `2020_1회_45` | 45 | 전기기기 | 슬립 st에서 최대 토크를 발생하는 3상 유도전동기에 2차측 한상의 저항을 r2라 하면 최대 토크로 기동하기 | matched | source-internal confirmed | 4 |  |
| `2020_1회_46` | 46 | 전기기기 | 단상 변압기를 병렬 운전할 경우 부하전류의 분담은? | matched | source-internal confirmed | 4 |  |
| `2020_1회_47` | 47 | 제어공학 | 스텝 모터(step motor)의 장점으로 틀린 것은? | matched | source-internal confirmed | 4 |  |
| `2020_1회_48` | 48 | 전기기기 | 380V, 60Hz, 4극, 10kW인 3상 유도전동기의 전부하 슬립 이 4%이다. 전원 전압을 10% 낮추 | matched | source-internal confirmed | 4 |  |
| `2020_1회_49` | 49 | 전기기기 | 3상 권선형 유도전동기의 기동 시 2차측 저항을 2배로 하면 최대토크 값은 어떻게 되는가? | matched | source-internal confirmed | 4 |  |
| `2020_1회_50` | 50 | 전기기기 | 직류 분권전동기에서 정출력 가변속도의 용도에 적합한 속 도제어법은? | matched | source-internal confirmed | 4 |  |
| `2020_1회_51` | 51 | 전기기기 | 직류 분권전동기의 전기자전류가 10A일 때 5Nㆍm의 토크 가 발생하였다. 이 전동기의 계자의 자속이 80% | matched | source-internal confirmed | 4 |  |
| `2020_1회_52` ⚠️ | 52 | 전기기기 | 권수비가 a인 단상변압기 3대가 있다. 이것을 1차에 △, 2 차에 Y로 결선하여 3상 교류 평형회로에 접속 | matched | source-internal confirmed | 4 |  |
| `2020_1회_53` | 53 | 제어공학 | 3상 전원전압 220V를 3상 반파정류회로의 각 상에 SCR을 사용하여 정류제어 할 때 위상각을 60°로 하 | matched | source-internal confirmed | 4 |  |
| `2020_1회_54` | 54 | 전기기기 | 유도자형 동기발전기의 설명으로 옳은 것은? | matched | source-internal confirmed | 5 |  |
| `2020_1회_55` | 55 | 전기기기 | 3상 동기발전기의 여자전류 10A에 대한 단자전압이 1000√3 V, 3상 단락전류가 50A 인 경우 동기임 | matched | source-internal confirmed | 5 |  |
| `2020_1회_56` | 56 | 전기기기 | 동기발전기에서 무부하 정격전압일 때의 여자전류를 Ifo, 정 격부하 정격전압일 때의 여자전류를 If1, 3상 | matched | source-internal confirmed | 5 |  |
| `2020_1회_57` | 57 | 전기기기 | 변압기의 습기를 제거하여 절연을 향상시키는 건조법이 아 닌 것은? | matched | source-internal confirmed | 5 |  |
| `2020_1회_58` | 58 | 전기기기 | 극수 20, 주파수 60Hz인 3상 동기발전기의 전기자권선이 2 층 중권, 전기자 전 슬롯 수 180, 각  | matched | source-internal confirmed | 5 |  |
| `2020_1회_59` | 59 | 전력공학 | 2방향성 3단자 사이리스터는 어느 것인가? | matched | source-internal confirmed | 5 |  |
| `2020_1회_60` | 60 | 전기기기 | 일반적인 3상 유도전동기에 대한 설명으로 틀린 것은? | matched | source-internal confirmed | 5 |  |
| `2020_1회_61` | 61 | 제어공학 | 다음 블록선도의 전달함수 는? | matched | source-internal confirmed | 5 |  |
| `2020_1회_62` | 62 | 제어공학 | 전달함수가 과 같은 제 어시스템에서 ω = 0.1 rad/s 일 때의 이득(dB)과 위상각(°) 은 약 얼마 | matched | source-internal confirmed | 5 |  |
| `2020_1회_63` | 63 | 회로이론 | 다음의 논리식과 등가인 것은? | matched | source-internal confirmed | 5 |  |
| `2020_1회_64` | 64 | 제어공학 | 다음의 개루프 전달함수에 대한 근궤적이 실수축에서 이탈 하게 되는 분리점은 약 얼마인가? | matched | source-internal confirmed | 5 |  |
| `2020_1회_65` | 65 | 회로이론 | 의 역 z 변환은? | matched | source-internal confirmed | 5 | manual verify — PDF raw page text 직접 일치 (regex parse 한계: 수식 image / 짧은 본문) |
| `2020_1회_66` | 66 | 제어공학 | 기본 제어요소인 비례요소의 전달함수는? (단, K는 상수이 다.) | matched | source-internal confirmed | 5 |  |
| `2020_1회_67` | 67 | 제어공학 | 다음의 상태방정식으로 표현되는 시스템의 상태천이행렬은? 4과목 : 회로이론 및 제어공학 | matched | source-internal confirmed | 5 |  |
| `2020_1회_68` | 68 | 제어공학 | 제어시스템의 전달함수가 과 같 이 표현될 때 이 시스템의 고유주파수(ωn(rad/s))와 감쇠율 (ζ)은? | matched | source-internal confirmed | 6 |  |
| `2020_1회_69` | 69 | 회로이론 | 그림의 신호흐름도를 미분방정식으로 표현한 것으로 옳은 것은? (단, 모든 초기 값은 0이다.) | matched | source-internal confirmed | 6 |  |
| `2020_1회_70` | 70 | 제어공학 | 제어시스템의 특성방정식이 s4+s3-3s2-s+2=0 와 같을 때, 이 특성방정식에서 s 평면의 오른쪽에 위 | matched | source-internal confirmed | 6 |  |
| `2020_1회_71` | 71 | 제어공학 | 회로에서 6Ω에 흐르는 전류(A)는? | matched | source-internal confirmed | 6 |  |
| `2020_1회_72` | 72 | 제어공학 | RL 직렬회로에서 시정수가 0.03s, 저항이 14.7Ω일 때 이 회로의 인덕턴스(mH)는? | matched | source-internal confirmed | 6 |  |
| `2020_1회_73` | 73 | 회로이론 | 상의 순서가 a-b-c인 불평형 3상 교류회로에서 각 상의 전 류가 Ia = 7.28∠15.95°(A), I | matched | source-internal confirmed | 6 |  |
| `2020_1회_74` | 74 | 회로이론 | 그림과 같은 T형 4단자 회로의 임피던스 파라미터 Z22는? | matched | source-internal confirmed | 6 |  |
| `2020_1회_75` | 75 | 제어공학 | 그림과 같은 부하에 선간전압이 Vab = 100∠30°(V)인 평형 3상 전압을 가했을 때 선전류 Ia(A) | matched | source-internal confirmed | 6 |  |
| `2020_1회_76` | 76 | 전력공학 | 분포정수로 표현된 선로의 단위 길이당 저항이 0.5Ω/km, 인덕턴스가 1μH/km, 커패시스턴스가 6μF/ | matched | source-internal confirmed | 7 |  |
| `2020_1회_77` | 77 | 제어공학 | 그림 (a)의 Y결선 회로를 그림 (b)의 △결선회로로 등가 변 환했을 때 Rab, Rbc, Rca는 각각  | matched | source-internal confirmed | 7 |  |
| `2020_1회_78` | 78 | 회로이론 | 다음과 같은 비정현파 교류 전압 v(t)와 전류 i(t)에 의한 평 균전력은 약 몇 W 인가? | matched | source-internal confirmed | 7 |  |
| `2020_1회_79` | 79 | 제어공학 | 회로에서 , I3= 5.0(A), Z3 = 1.0Ω 일 때 부하(Z1, Z2, Z3) 전체에 대한 복 소 전 | matched | source-internal confirmed | 7 | manual verify — PDF raw page text 직접 일치 (regex parse 한계: 수식 image / 짧은 본문) |
| `2020_1회_80` | 80 | 제어공학 | 는? | matched | source-internal confirmed | 7 | manual verify — PDF raw page text 직접 일치 (regex parse 한계: 수식 image / 짧은 본문) |
| `2020_1회_81` | 81 | 전기설비기술기준 | 풍력터빈의 피뢰설비 시설기준에 대한 설명으로 틀린 것은? | matched | source-internal confirmed | 7 |  |
| `2020_1회_82` | 82 | 전력공학 | 샤워시설이 있는 욕실 등 인체가 물에 젖어있는 상태에서 전기를 사용하는 장소에 콘센트를 시설할 경우 인체감전 | matched | source-internal confirmed | 7 |  |
| `2020_1회_83` | 83 | 전력공학 | 강관으로 구성된 철탑의 갑종 풍압하중은 수직 투영면적 1m2에 대한 풍압을 기초로 하여 계산한 값이 몇 Pa | matched | source-internal confirmed | 7 |  |
| `2020_1회_84` | 84 | 전기설비기술기준 | 한국전기설비규정에 따른 용어의 정의에서 감전에 대한 보 호 등 안전을 위해 제공되는 도체를 말하는 것은? | matched | source-internal confirmed | 8 |  |
| `2020_1회_85` | 85 | 전기설비기술기준 | 통신상의 유도 장해방지 시설에 대한 설명이다. 다음 ( )에 들어갈 내용으로 옳은 것은? | matched | source-internal confirmed | 8 |  |
| `2020_1회_86` | 86 | 전기설비기술기준 | 주택의 전기저장장치의 축전지에 접속하는 부하 측 옥내배 선을 사람이 접촉할 우려가 없도록 케이블배선에 의하여 | matched | source-internal confirmed | 8 |  |
| `2020_1회_87` | 87 | 전기설비기술기준 | 전압의 구분에 대한 설명으로 옳은 것은? | matched | source-internal confirmed | 8 |  |
| `2020_1회_88` | 88 | 전력공학 | 고압 가공전선로의 가공지선으로 나경동선을 사용할 때의 최소 굵기는 지름 몇 mm 이상인가? | matched | source-internal confirmed | 8 |  |
| `2020_1회_89` | 89 | 전기기기 | 특고압용 변압기의 내부에 고장이 생겼을 경우에 자동차단 장치 또는 경보장치를 하여야 하는 최소 뱅크용량은 몇 | matched | source-internal confirmed | 8 |  |
| `2020_1회_90` | 90 | 전기설비기술기준 | 합성수지관 및 부속품의 시설에 대한 설명으로 틀린 것은? | matched | source-internal confirmed | 8 |  |
| `2020_1회_91` | 91 | 전력공학 | 사용전압이 22.9kV인 가공전선이 철도를 횡단하는 경우, 전 선의 레일면상의 높이는 몇 m 이상인가? | matched | source-internal confirmed | 8 |  |
| `2020_1회_92` | 92 | 전력공학 | 가공전선로의 지지물에 시설하는 통신선 또는 이에 직접 접 속하는 가공 통신선이 철도 또는 궤도를 횡단하는 경 | matched | source-internal confirmed | 8 |  |
| `2020_1회_93` | 93 | 전기설비기술기준 | 전력보안통신설비의 조가선은 단면적 몇 mm2 이상의 아연 도강연선을 사용하여야 하는가? | matched | source-internal confirmed | 8 |  |
| `2020_1회_94` | 94 | 전기설비기술기준 | 가요전선관 및 부속품의 시설에 대한 내용이다. 다음 ( )에 들어갈 내용으로 옳은 것은? | matched | source-internal confirmed | 8 |  |
| `2020_1회_95` | 95 | 전력공학 | 사용전압이 154kV인 전선로를 제1종 특고압 보안공사로 시 설할 경우, 여기에 사용되는 경동연선의 단면적은 | matched | source-internal confirmed | 8 |  |
| `2020_1회_96` | 96 | 전력공학 | 사용전압이 400V 이하인 저압 옥측전선로를 애자공사에 의 해 시설하는 경우 전선 상호 간의 간격은 몇 m  | matched | source-internal confirmed | 8 |  |
| `2020_1회_97` | 97 | 전력공학 | 지중전선로는 기설 지중약전류전선로에 대하여 통신상의 장 해를 주지 않도록 기설약전류전선로로부터 충분히 이격시 | matched | source-internal confirmed | 8 |  |
| `2020_1회_98` | 98 | 전기설비기술기준 | 최대 사용전압이 10.5kV를 초과하는 교류의 회전기 절연내 력을 시험하고자 한다. 이때 시험전압은 최대사용 | matched | source-internal confirmed | 8 |  |
| `2020_1회_99` | 99 | 전력공학 | 폭연성 분진 또는 화약류의 분말에 전기설비가 발화원이 되 어 폭발할 우려가 있는 곳에 시설하는 저압 옥내배선 | matched | source-internal confirmed | 8 |  |
| `2020_1회_100` | 100 | 전력공학 | 과전류차단기로 저압전로에 사용하는 범용의 퓨즈(「전기 | matched | source-internal confirmed | 8 |  |

⚠️ q52: Permanent Invariant 영역 (단독 변경 영구 금지).

## 6. Pattern Analysis

### 6.1 systemic batch mis-label 영역 판정

**결과**: **systemic batch mis-label 가능성 매우 강화** (100/100 mis-label).

| 패턴 후보 | 본 audit evidence |
|---|---|
| all/near-all mismatch → systemic batch | **본 audit 정합** (100/100 all-mismatch, label 2020_1회 / 실제 source 2022-04-24 PDF) |
| 일부만 mismatch → partial contamination | 부적합 (0건 partial) |
| q52만 mismatch → isolated | 부적합 (q52 외 99건 모두 동일 PDF source) |

**핵심 측정**:
- 100/100 records 모두 `data/20200424_1회.pdf` (표지 2022-04-24) 본문과 정확 일치
- PDF q_no 1~100 모두 본 PDF 안에서 발견 (page 분포 정합)
- per-year ↔ master 100% 정합 (E2 5f1c9c5 재확인)
- 본 audit은 systemic 1 batch mis-label 가설 (impact audit §1) 영역 evidence 강화

### 6.2 caution release C1 acceptance criteria 영역

closeout §4 C1 (caution release acceptance criteria) 측정:

| criterion | threshold | 본 audit measurement | 충족 영역 |
|---|---|---|---|
| C1 minimum sample | 15 sample | **100 sample** | 임계점 압도적 초과 |
| all-mismatch >= 10/15 → systemic | 10/15 = 66.7% | **100/100 = 100%** | systemic 영역 압도적 강화 |
| 0~4/15 → isolated 강화 | <= 26.7% | 0% (isolated 영역 부적합) | isolated 부적합 |
| 5~9/15 → 추가 audit 필요 | 33%~60% | 100% (영역 명확) | 추가 audit 영역 0 |

→ **C1 (systemic batch mis-label) acceptance criteria 충족** (압도적 evidence).

**중요**: C1 충족 ≠ caution release 충족. closeout §4 C2 + C3 영역 모두 충족 영역 진입 필요:
- **C2 (66항 policy 결정)**: 영역 0 — defer 유지 (df7e932). C2 측정 = 미충족.
- **C3 (storage_id ↔ canonical_source_id 혼동 방지 evidence)**: 영역 0 — resolver implementation 미진입 / app screen smoke test 미수행 / docs-only current-state wording 부분 영역. C3 측정 = 미충족.

→ **caution release 차단 영역 유지** (C1 충족만으로 unblock 안 됨).

### 6.3 99 records alias 확장 evidence R1~R7 영역 (plan §6)

| evidence | 본 audit 결과 |
|---|---|
| R1 Phase A~D 완료 | **충족** (전수 PDF source 매핑 + 정합 결과) |
| R2 C1 패턴 record 수 정량 | **충족** (100/100, C1 패턴 = q52와 동일 mis-label 영역) |
| R3 99 records 각각 candidate canonical_source_id 매핑 | **충족** (99 records 모두 `2022_1회_q_no` 매핑 가능 영역, 표지 일자 2022-04-24 기준) |
| R4 evidence_ref 양식 | **충족** (N1 audit + impact audit + 본 audit + per-year JSON cross-reference) |
| R5 Permanent Invariant 영역 준수 | **충족** (storage_id 영역 보존 명시) |
| R6 registry artifact 확장 양식 결정 | **미충족** (양식 영역 = 별 design decision 영역, 본 audit 영역 외) |
| R7 app key 영역 영향 0 재확인 | **확인** (E5 §6 영역 유지 — alias-only resolver 영역 + impact audit §3 app key 영역 영향 0) |

→ R1~R5, R7 충족 / R6 별 design decision 영역 진입 영역. 99 records alias 확장 evaluation 트랙 진입 가능성 영역 활성.

## 7. Impact on E6 Separability / Closeout Baseline

### 7.1 E6 separability framework 영역 영향

| layer | E6 직전 결론 | 본 audit 영향 |
|---|---|---|
| Q1·Q2 Registry creation/review | Separable 강화 | 영역 변경 0 (강화 유지). registry framing 확장 가능성 영역 input 강화. |
| Q3 App/data decision | Refined Partial Separable | 영역 변경 0. alias-only resolver Separable 영역 유지. |
| Q4 Caution release | Inseparable 유지 | C1 evidence 강화 / C2 + C3 미충족 영역 유지 → Inseparable 유지. |
| Q5 Batch migration | Inseparable 강화 (영구 분리 불가) | mapping granularity 5 영역에 input evidence 1건 추가 (100 records → 2022_1회 systemic mapping 영역 후보). 영구 분리 불가 영역 유지. |
| Q6 systemic session-label policy | 별 문서 필요 + defer 유지 | 영역 변경 0. 66항 policy 재evaluation 트랙 영역 별. |
| q52 Permanent Invariant | 영구 금지 | **유지 강화** — systemic 1 사례 영역 100/100 evidence로 재확인. |

→ E6 framework 변경 0. q52 invariant 강화. caution release Q4 Inseparable 유지.

### 7.2 closeout baseline 영향

| 영역 | 본 audit 영향 |
|---|---|
| accomplished 6 영역 | 모두 유지 (변경 0) |
| explicitly_blocked 8 영역 | 모두 유지 (변경 0) |
| C1 acceptance criteria evidence | **충족 (압도적 강화)** |
| C2 acceptance criteria evidence | 미충족 유지 (defer) |
| C3 acceptance criteria evidence | 미충족 유지 (resolver / smoke test 영역 0) |
| self_reference_note (P1) | 영역 변경 0 (lookback rate / supersede density 측정 데이터 영역) |
| next_review_trigger | S2 audit 트리거 (본 audit) 충족 — 본 audit이 첫 트리거 측정 사례 |

## 8. Next Gates

각 별 명시 승인 영역:

1. **99 records alias 확장 evaluation 트랙 진입 결정** — R1~R5+R7 충족 영역 + R6 (registry artifact 확장 양식) 별 design decision 필요
2. **registry artifact 확장 양식 design decision** — C1~C7 영역 (plan §8) 충족 영역
3. **66항 policy 재evaluation** — E4 + 외부 source evidence 수집 후
4. **runtime resolver implementation plan** — Refined Partial Separable alias-only 영역
5. **caution release review** — C2 + C3 evidence 수집 후만 (C1 충족만으로 진입 0)
6. **외부 official source evidence** — 한국기술자격검정 공식 2020/2022 시행 기록 (R1~R3 confidence 영역 source-internal confirmed → 확정 영역 승급 input)
7. **E4 다른 합본 PDF 패턴 영역** — `data/20200424_1회.pdf` 외 다른 시기 합본 PDF 패턴 catch 영역
8. **missing 29 recovery plan** — 별 트랙 (q52 separability 영향 0 영역 유지)
9. **1·3·4 과목 verification** — per-subject 분포 catch 영역 (전력공학 30 / 회로이론 6 / 전기설비 9 표준 분포 부적합 영역)
10. **layer review** — DR-TRAP-LAYER-V1-OPERATIONAL 이후 closeout 첫 사례 (`DR-TRAP-GIGI17-BTRACK-DOCS-BASELINE-CLOSEOUT`) + 본 audit 첫 next_review_trigger 측정

## 9. Status

- 2020_1회 100 records 전수 source audit 완료 (read-only).
- 결과: **100/100 matched + source-internal confirmed** (PDF text + record text + page 3-way 정합).
- pattern: **systemic batch mis-label** (label 2020_1회 / 실제 source `data/20200424_1회.pdf` 표지 2022-04-24).
- q52는 systemic 1 사례 영역. Permanent Invariant 영역 유지 (단독 변경 영구 금지).
- caution release C1 acceptance criteria 영역 충족 (100/100, 임계점 압도적 초과). C2 + C3 영역 미충족 영역 유지 → caution release 차단 유지.
- 99 records alias 확장 evidence R1~R5+R7 충족. R6 (registry artifact 확장 양식) 별 design decision 영역.
- E6 separability framework 변경 0. q52 Permanent Invariant 강화. caution release Q4 Inseparable 유지.
- closeout baseline accomplished/explicitly_blocked 영역 모두 유지. C1 evidence 강화 / C2 + C3 미충족 영역 유지.
- next gates 10 영역 활성 (각 별 명시 승인 영역).
- 본 audit 정책 변경 0 → JSONL entry 추가 0 (사용자 가이드 정합 — docs-only audit + 정책 변경 0).
- 기기-17 caution 유지. registry row status=candidate 유지. 66항 policy defer 유지. Batch migration 차단 유지. caution release 차단 유지. missing 29 data debt 별 트랙 분리 유지. q52 storage_id 단독 변경 영구 금지 유지.
- app code / app data / questions.json / per-year / pdf_pages / PDF / registry artifact / JSONL 모두 변경 0.
- 임시 결과 `/tmp/audit_results.json` 영역 — 최종 repo 영역 외 영역 (사용자 명시 정합).

