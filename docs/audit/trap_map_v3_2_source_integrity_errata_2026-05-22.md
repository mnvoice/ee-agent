# Trap-Map v3.2 — Source Integrity Errata (2026-05-22)

웹 리뷰에서 제기된 v3.2 corrected actionable trap-map 문서의 수치 무결성 이슈를,
현재 진행 중인 A-priority / B-priority pilot 상태와 **분리**해 정리한다. 본 errata는
v3.2 원본의 검증 결과를 기록할 뿐이며, A/B pilot 산출물의 유효성을 별도로 판정한다.

이번 단계는 errata 문서 작성만 — app/data·questions.json 미수정. solution/steps
미적용. answer/choices/text 미수정. 유료 API 미호출. local server 미실행.

- 검증 대상: `docs/audit/input/전기기사_6과목_라벨링_v3.2_corrected_actionable_20260522.md`
- 검증 방법: §4 본문 카드 헤더(`[과목-N]`)·우선순위 라인 전수 추출 후 §5 검증표
  주장값과 대조 (read-only).
- 분리 평가 대상:
  - A-priority closeout (`docs/audit/trap_map_A_priority_pilot_learning_package_closeout_2026-05-22.md`)
  - B-priority study set v1 (`docs/audit/trap_map_B_priority_pilot_study_set_v1_2026-05-22.md`)

---

## 결론

v3.2 §5.2 우선순위 분포에 **confirmed 오류 2건**(기기·전력 row), §4 번호 체계
미문서화 등 무결성 이슈 5건을 확인했다. 단 **A-priority closeout·B-priority study
set v1은 invalidate되지 않는다** — 두 pilot 모두 v3.2를 *주제 목록* source로만
쓰고 대표 기출은 questions.json 대조 dryrun으로 독립 검증했으며, §5.2 오류는 pilot
산출 경로에 전파되지 않았다(§3).

v3.2 원본 전체 지도(61항)를 **canonical source로 쓰기 전에는 보완 필요** — §5.2
정정, 번호 체계 명문화, "대표 보기 함정" source label 재표기(§4).

---

## 1. 검증 결과 — §4 본문 vs §5 검증표

### 1.1 §5.1 항목 수 검증 — 정합 (오류 없음)

`[과목-N]` 카드 헤더 전수 집계:

| 과목 | §4 본문 카드 수 | §5.1 주장 | 정합 |
|---|--:|--:|:--:|
| 전기기기 (§4.1) | 27 | 27 | ✅ |
| 전기설비 (§4.2) | 21 | 21 | ✅ |
| 전력공학 (§4.3) | 11 | 11 | ✅ |
| 회로이론 (§4.4) | 2 | 2 | ✅ |
| 합 | 61 | 61 | ✅ |

§5.1 항목 수 검증은 4과목 전부 본문과 정합한다.

### 1.2 §5.2 우선순위 분포 — confirmed 오류 2건

본문 카드별 `우선순위:` 라인 61개 전수 집계 vs §5.2 주장:

| 과목 | 본문 집계 (A/B/C) | §5.2 주장 (A/B/C) | 판정 |
|---|---|---|---|
| 전기기기 | **17 / 10 / 0** | 18 / 9 / 0 | ❌ A·B 각 1항 오분류 |
| 전기설비 | 6 / 11 / 4 | 6 / 11 / 4 | ✅ |
| 전력공학 | **8 / 3 / 0** | 7 / 4 / 0 | ❌ A·B 각 1항 오분류 |
| 회로이론 | 0 / 1 / 1 | 0 / 1 / 1 | ✅ |
| 합 | 31 / 25 / 5 | 31 / 25 / 5 | (합계만 정합) |

본문 B등급 항목(전수):
- 전기기기 B 10항: 기기-4·7·17·18·19·20·23·25·26·28
- 전력공학 B 3항: 전력-18·22·25

§5.2는 기기를 A18/B9, 전력을 A7/B4로 주장하나, 본문 우선순위 라벨 집계는 기기
A17/B10, 전력 A8/B3이다. 기기에서 B 1항이 A로, 전력에서 A 1항이 B로 — **반대
방향 1항씩 오분류**되어 A합(31)·B합(25)·과목합은 모두 정합한다. §5.3 핵심 수치
합 검증이 row/column 합계만 확인하므로 이 cell 단위 오류를 통과시켰다.

---

## 2. 발견 사항 (errata 항목)

| # | 이슈 | severity | confirmed/추정 |
|---|---|---|---|
| F1 | `[과목-N]` 번호 체계 미문서화 (기기-21·22·24 등 결번) | low | 정합(누락 아님) |
| F2 | §5.2 우선순위 분포 기기·전력 row 오류 | medium | **confirmed** |
| F3 | 설비 본문 count — 웹 리뷰 "20" vs 실제 21 | none | 정합(웹 주장 미재현) |
| F4 | 전기기기 S/F count §2.1 주장 3 vs 본문 식별 2 | low | 검증 불가 |
| F5 | "대표 보기 함정"이 검증된 (a) 출처 아닌 (c) 추정 | medium | **confirmed (source label)** |

### F1 — `[과목-N]` 번호 체계 미문서화

기기 카드 ID는 1~20, 23, 25~30 — **기기-21·22·24가 결번**이다. 설비도 2·3·4·
11·15·17·24·25·26이 결번, 전력·회로도 다수 결번(회로는 회로-20·27만 존재).

회로이론 ★4~5 함정이 2항인데 ID가 회로-20·회로-27인 점이 결정적 — `[과목-N]`은
함정 순번이 아니라 **과목별 핵심 단위 global index**다. 따라서 기기-21·22·24
결번은 "해당 핵심 단위가 ★4~5 함정이 아님"을 뜻하며 **누락(erroneous omission)이
아니다**. 카드 count(기기 27)는 §5.1과 정합(§1.1).

단 v3.2는 핵심 단위 master list(★1~3 포함 전체)를 포함하지 않아, 결번 ID가 실재
핵심 단위인지 삭제 흔적인지 v3.2 단독으로 검증 불가. v3.2 §1은 v3 65항 →
v3.2 61항(★4~5 함정 −4)을 기록 — 일부 결번은 개정 중 삭제 가능성. **canonical
사용 시 번호 체계와 master index 출처 명문화 필요.**

### F2 — §5.2 우선순위 분포 기기·전력 row 오류 (confirmed)

§1.2 참조. 기기 row(A18/B9)·전력 row(A7/B4)가 본문 집계(기기 A17/B10, 전력
A8/B3)와 불일치. 합계 net-zero라 §5.3을 통과. v3.2 §7 E가 이미 예고한 catch
후보 "교차표 1항 단위 검증 누락"의 실현 — 본 errata가 confirmed로 승격.

### F3 — 설비 본문 count (웹 리뷰 "20" 미재현)

`[설비-N]` 헤더 전수 집계 = **21항**(설비-1·5·6·7·8·9·10·12·13·14·16·18·19·
20·21·22·23·27·28·29·30). §5.1 주장 21과 정합. 웹 리뷰가 제기한 "본문 20"은
재현되지 않음 — 본 errata는 실측값 21을 기록하며, 웹 리뷰 "20" 주장은
**confirmed 오류 아님**으로 분류.

### F4 — 전기기기 S/F count (검증 불가)

§2.1 D/S×현상기원 교차표는 전기기기 S/F = 3(전체 59항 기준)으로 주장. §4 본문
27개 ★4~5 함정 카드 중 S/F는 **기기-5(★5 S/F), 기기-29(★4 S/F) 2항**. 차이
1항은 ★1~3 구간에 있다고 가정해야 정합하나, v3.2가 ★1~3 항목을 나열하지 않아
**v3.2 단독으로 검증 불가**. v3.2 §6 #2가 "6축 카운트는 약식 추정 ±2 오차"를
이미 명시 — S/F 3은 ±2 추정 범위 내이며 본문 식별 2항과 모순은 아니다. confirmed
오류 아님, traceability gap.

### F5 — "대표 보기 함정" = (c) 추정 source label

§4 각 카드의 `대표 보기 함정:` 라인(예: 기기-17 "권수비가 전압만 변환한다고 보는
보기")은 실제 기출 보기를 검증한 (a) 출처가 아니라 **구성된 가설(c) 추정**이다.

근거:
- v3.2 §6 #1 "현상기원 라벨링은 (b)~(c) source label", #4 "'외울 것'과 '이해할
  것'은 가설적 분리" — v3.2 자체가 가설임을 자인.
- B-priority 1차 representative dryrun(`4a92294`)이 10항 중 5항에서 대표 기출이
  v3.2 "대표 보기 함정"과 mismatch이거나 source-clean FAIL임을 발견 — "대표 보기
  함정"이 실제 기출 검증을 거치지 않은 추정임을 실증.

→ "대표 보기 함정"은 학습 설계 가설로는 유효하나, **검증된 함정 카탈로그가
아니다.** canonical 사용 시 항목별 representative dryrun(기출 대조)이 필수.

---

## 3. 영향 판정 — A/B pilot invalidate 여부

### 판정: A-priority closeout·B-priority study set v1 모두 **invalidate되지 않는다.**

근거 4가지:

1. **v3.2는 주제 목록 source로만 사용** — A/B pilot은 v3.2에서 "어떤 항목이
   ★4~5 함정 / A·B등급인가"라는 주제 목록만 가져왔다. 수치 집계표(§5.2)를 학습
   콘텐츠나 우선순위 결정에 직접 쓰지 않았다.

2. **B selection이 §5.2가 아닌 본문을 source로 사용** — B-priority selection
   문서 §2는 B등급 25항을 §4 본문 카드의 `우선순위:` 라벨에서 직접 집계해 기기
   B 10항·전력 B 3항으로 기록했다. 이는 F2의 오류값(§5.2: 기기 B9·전력 B4)이
   아니라 **본문 정확값과 일치**한다. 즉 F2의 오류는 §5.2 요약표에 갇혀 있고
   pilot 산출 경로로 전파되지 않았다.

3. **대표 기출은 questions.json 대조로 독립 검증** — B-priority는 1차 dryrun →
   replacement selection → re-dryrun(PASS, 10/10)을 거쳐 대표 기출을
   questions.json full-content와 대조했다. 이 dryrun 절차가 F5(대표 보기 함정 =
   추정)를 잡아내는 장치 그 자체 — 1차 dryrun이 5/10을 catch했고 교체 후 redryrun이
   10/10에 도달했다. A-priority도 representative dryrun을 거쳐 closeout했다.

4. **study set v1이 추정 약점을 이미 흡수** — B-priority study set v1은 10항을
   exact 3 / adjacent 7로 표기하고, adjacent 항목마다 "원래 카드 함정 ≠ 대표
   기출이 검증하는 함정"을 분리 기재했다. 즉 F5의 "대표 보기 함정이 실제 기출과
   다를 수 있다"는 약점은 adjacent 라벨로 이미 문서화·반영되어 있다.

→ A-priority 26항 패키지와 B-priority 10항 study set v1은 v3.2 수치 무결성 이슈와
**독립적으로 검증 완료**된 산출물이다. 본 errata는 이들을 자동 무효 처리하지
않는다.

(단 v3.2 §5.2를 우선순위 결정에 직접 인용한 *향후* 작업이 있다면 F2 정정값으로
재확인 필요.)

---

## 4. v3.2 canonical source 사용 전 보완 필요

v3.2 원본 전체 지도(61항)를 canonical source(향후 A/B/C 확장, 정직 학습 지도 등)로
쓰기 전에 다음을 보완해야 한다.

| ID | 대응 이슈 | 보완 항목 |
|---|---|---|
| C1 | F1 | `[과목-N]` 번호 체계 명문화 — 핵심 단위 master index를 포함하거나 v3.1 교차 참조를 명시. 결번(기기-21·22·24 등)의 의미(★1~3 / 삭제) 기록 |
| C2 | F2 | §5.2 우선순위 분포 정정 — 기기 row A17/B10, 전력 row A8/B3 |
| C3 | F5 | "대표 보기 함정" 라인을 (c) 추정/가설로 명시 relabel. canonical 학습 패키지화 시 항목별 representative dryrun(기출 대조) 의무화 |
| C4 | F2 근본원인 | §5.3 정합 검증을 row/column 합계뿐 아니라 **cell 단위**로 확장 — F2가 §5.3을 통과한 원인이 cell 미검증 |

F3·F4는 정정 불요 — F3는 정합(웹 주장 미재현), F4는 §6 #2 "±2 추정" 명시가 이미
존재(유지). 단 canonical 사용 시 ★1~3 항목 미나열로 §2.1 교차표가 v3.2 단독
검증 불가임을 한계로 명시 권장.

v3.2 §7 E는 이미 "별점 분포 원본 미대조 / 교차표 1항 단위 검증 누락 / 함정 자리
카운트 과대" catch 후보를 예고했다 — F2는 그 예고된 catch class의 confirmed 실현.
본 errata는 §7 E의 catch 후보를 구체 항목으로 승격한 기록이다.

---

## 5. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| §4 본문 카드 수 ↔ §5.1 재확인 | ✅ 기기 27 / 설비 21 / 전력 11 / 회로 2 = 61 — 전부 정합 |
| 기기-21·22·24 누락 여부 | ✅ 결번이나 누락 아님(F1) — `[과목-N]`은 핵심 단위 global index, count 27 정합 |
| 설비 본문 count 20 vs 21 | ✅ 실측 21 — §5.1과 정합, 웹 리뷰 "20" 미재현(F3) |
| 전기기기 S/F 3 vs 본문 식별 | ✅ 본문 ★4~5 함정 S/F 2항 확인, 차이 1항 검증 불가로 기록(F4) |
| "대표 보기 함정" source label | ✅ (c) 추정으로 기록(F5) — v3.2 §6 자인 + B 1차 dryrun 실증 인용 |
| §5.2 우선순위 분포 검증 | ✅ confirmed 오류 2건(기기·전력 row) — 본문 우선순위 라인 전수 집계 대조(F2) |
| A-priority closeout invalidate 여부 | ✅ invalidate 아님 — §3 근거 4가지 |
| B-priority study set v1 invalidate 여부 | ✅ invalidate 아님 — §3 근거 4가지 |
| v3.2 canonical 사용 전 보완 명시 | ✅ C1~C4 명시(§4) |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps 미수정 / API·server 미실행 |

---

## Status

- v3.2 corrected actionable trap-map source integrity errata 작성 완료.
- §4 본문 카드 헤더·우선순위 라인 전수 추출 후 §5 검증표 대조.
- 발견 5건: F1 번호 체계 미문서화(low) / **F2 §5.2 우선순위 분포 기기·전력 row
  오류(confirmed, medium)** / F3 설비 count 21 정합(웹 "20" 미재현) / F4 전기기기
  S/F 검증 불가(low) / **F5 "대표 보기 함정" = (c) 추정(confirmed, medium)**.
- §5.1 항목 수 검증은 4과목 전부 정합 — count 오류 없음.
- A-priority closeout·B-priority study set v1은 **invalidate되지 않음** — v3.2를
  주제 목록 source로만 쓰고 대표 기출은 questions.json 대조 dryrun으로 독립 검증,
  §5.2 오류는 pilot 경로에 미전파(§3 근거 4).
- v3.2 전체 지도를 canonical source로 쓰기 전 보완 필요 — C1~C4(§4).
- 이 문서는 source integrity errata다. v3.2 원본·questions.json·pilot 산출물
  미수정.
