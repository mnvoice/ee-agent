# EE-Agent DEVLOG

코드 저장소-Obsidian DECISIONS.md 분리 해소의 첫 단계.
정식 결정문은 `/Users/jeong-ujin/Documents/Obsidian Vault/DECISIONS.md` (D-번호 부여).
본 파일은 작업 로그 (시간순).

분리 해소 정책 자체는 **D24 후보**로 보존 (별도 결정 필요).

---

## 2026-04-30 — D23 본 세션 옵션 (가) 종결

### §1.5 두 진술

1. **작업**: results 다운로드 + 586건 차이 측정만 (JSON merge 다음 세션)
2. **결과 입력처**: CBT 풀이 도구 `app/` 풀이 그림 영역
   - `app/js/render.js:170` — `<div class="sol-figure">${solution_svg}</div>`
   - `app/index.html:360` — 동일

### §1.7 측정 (변경 0)

| 항목 | 값 |
|------|-----|
| 회로+전자기 전체 후보 (74파일 전수) | **1,620건** |
| solution 비어있음 | 177건 |
| 이미 solution_svg 있음 | **1,443건** |
| batch 입력 대상 (지금) | **0건** |
| 산수 검증 | 177+1,443+0 = 1,620 ✅ |
| batch_history.md §3 권장 | 1,848건 |
| requests.jsonl 실제 batch | 1,262건 |
| 권장-실제 차이 | 586건 |
| 실측-실제 차이 | **358건** (권장값 부정확) |

### 옵션 C 채택 사유 (다운로드 보류)

- 2026-04-29 API key validation 오류 1건 흔적 + 오늘 동일 오류 재발 시 디버깅 부담
- 사례 6 변형 차단 ("기왕 시작했으니 다운로드 끝내자")
- 다운로드는 다음 세션 첫 작업 (a) 출처 살아있음 (`batch_id.txt` 보존)

### (c) → (b) 정정

- 직전 (c) 추정: "results*.jsonl 부재 → 다운로드 미완료" — 표면 단서로 본질 추정 = 사례 1 구조
- 정정: 1,443건 출처 (a) 미확정 → 다음 세션 (b) 검증 영역

### 보존 산출물 (다음 세션 첫 작업의 (a) 출처)

- `data/batch_solution_svg_v2/batch_id.txt`: `msgbatch_015BB1UsrAx4naBBUByCtxWZ`
- `data/batch_solution_svg_v2/requests.jsonl`: 1,262줄
- `data/batch_solution_svg_v2/id_mapping.json`: 108KB / `bak_20260429_predown`: 112KB
- `data/batch_solution_svg_v2/failed_ids.json`: 568B (1건 OverloadedError, retry 가능)

### 다음 세션 첫 작업 후보

1. `id_mapping.json` vs `bak_20260429_predown` diff (다운로드 후 갱신 여부)
2. 1,443건 연도별/과목별 분해 (691건 기존 + 752건 이번 일부 가설 검증)
3. `python scripts/generate_solution_svg_batch.py status` (read-only API)
4. 위 결과 따라 다운로드/다른 경로/보류 결정

### 본 세션 위반 0건

- `cmd_download` 호출 (JSON merge 동반) — 차단됨
- 추가 batch CLI — 0회
- `data/questions_기출_*.json` 수정 — 0건
- 미커밋 22건 + 추적 안 됨 20+건 — 그대로 보존
- commit — 0건

### 연관

- 본 세션 박음: **D23** (Obsidian DECISIONS.md)
- 후속 후보: **D24** (저장소 ↔ Obsidian 분리 해소 정책)
- 기존: D14(stem 소실 22%), D16(Phase 1 stem OCR 승격), D19(INV-9), D22(멀티연도 91.3%)

---

## 2026-04-30 (cont.) — 분포 분해 + 사용자 (b) 기억 박음

### §1.5 두 진술

1. **작업**: 회로+전자기학 1,443건 (solution_svg 채워진 것) 통합본 read-only 분해
2. **결과 입력처**: D23 가설 판정의 (a) 분포 데이터, (b) 검증 영역 보존 (자동 download/merge 금지)

### (a) 분해 결과 — 산수 1,443 = 1,443 ✅

| 차원 | 분포 |
|------|------|
| 과목 | 회로이론 354 / 전기자기학 1,089 (3:1 불균형) |
| 시기 | 2020 이후 306 (21.2%) / 이전 1,137 (78.8%) |
| 연도 누락 | **2023, 2024 통째로 미수집** |
| 연도 최대 | 2025년 89건, 2011년 75건 |
| session 표기 | 7변형 (`1회`, `1회회`, `1,2회회`, `2회회`, `3회회`, `4회회`, `6회회` — OCR 파싱 잔재) |

### 분포가 직접 박는 사실 ((a) 결론)

1. **2023, 2024 미수집** — 분포 직접 보임 (추정 아님)
2. **2020 이후 21.2%만** — 신규 SVG 비중 작음
3. **전기자기학:회로이론 = 3:1** — 과목별 채움 불균형
4. **session 표기 7변형** — OCR 파싱 정합성 잔존

### 분포 단독으로 안 박히는 것 → (b) 검증 영역 보존

- 691건(기존)이 어떤 batch에서 채워졌나
- 752건이 4-29 batch 일부인가 (`requests.jsonl` 1,262 ID vs 1,443 SVG ID 교집합 필요)
- 1,262 − 752 = 510 어디로 갔나

→ 가설 A(691+752) / B(691만) / C(다른조합) 판정 — **(c) 추정 안 박음**, (b) 검증 영역 보존

### 사용자 기억 (b) — 다음 세션 (a) 검증 대상

1. "실제 이미지 ↔ 처리 이미지 매핑 안 되는 문제 있었음"
2. "매핑 위해 데이터 정합성 맞추는 과정 거침"

(c) 미확정: D-번호 / 자산종류(stem vs solution_svg vs 다른) / 시점

### 다음 세션 첫 작업 후보 4종 (트랙)

```
A. session 표기 7변형 정규화 (데이터 위생, 통합본 수정 = §1.5 별도 필요)
B. requests.jsonl 1,262 ID vs 1,443 SVG ID 교집합 (가설 A/B/C 결정적 판정)
C. 2023, 2024 수집 계획 (PDF 출처 + OCR + 새 batch)
D. 사용자 (b) 기억 → (a) 검증 (DEVLOG grep / git log / scripts 식별)
```

### §1.5 자기 적용 박힘 — 마모 패턴 회피

- 분포 박은 직후 "정규화도, 교집합도" 자동 제안 = 사례 6 변형 = **차단됨**
- 본 세션 추가 트랙 **0건**
- D23 (c)→(b) 정정 패턴 재적용 (가설 판정 보류)
- 사용자 종결 선언 후 "어느 방향?" → 트랙 4개 박을 때 또 마모 입구 → §1.5 자기 적용으로 차단

### 본 세션 위반 0건

- download/merge — 0건
- 통합본 수정 — 0건
- (c) 추정 가설 판정 — 0건
- 자동 commit — 0건
- 자동 트랙 확장 — 0건

### 보존 위치 3중

- 본 DEVLOG.md (이 섹션)
- `~/.claude/projects/-Users-jeong-ujin-1/memory/project_ee_agent_session_part4.md`
- MEMORY.md 인덱스 (포인터 1줄)
- Obsidian DECISIONS.md — 사용자 직접 (D23 후속 또는 D24 신규는 사용자 결정)

---

## 2026-04-30 — figure 활용 결정 트랙

### 진술 1 (작업)
PDF 페이지 직접 표시로 그림 있는 368건 해결.
회로 다이어그램 SVG 재생성 안 함 (어제 폐기 트랙 부활 회피).

### 진술 2 (입력처)
아이패드 PWA에서 그림 필요한 회로 문제 풀이 가능.
사용자 학습/시험 합격 결과 도달.

### (a) 박힌 사실 — 본 세션 측정
- 통합본 5,331건 / figure_svg 채워짐 340 / 회복 후보 368
- figure-demo: PDF 페이지 PNG 22장, SVG 0장 (의도된 비교 데모)
- 케이스 1 (2000-2-3): 통합본↔mathpix 정합 (score 1.0)
- 케이스 2 (2011-3-41): 통합본↔mathpix 정합 (score 1.0)
- TIER_3 회복 후보 30건 샘플: 76.7% 정합, 16.7% MISMATCH (mathpix OCR 한계)
- 데이터 시스템적 꼬임 없음

### (c) 미확정 / (b) 검증 영역
- 첨부 이미지 figure 박스 정확한 출처 (figure-demo 화면 가능성 우세)
- mathpix 2021~2026 자산 부재 (6년치 OCR 미수집)
- figure_svg 340건 정확한 batch 출처

### 4가지 활용 경로 — 비교
| 경로 | 비용 | 정합성 | 결정 |
|---|---|---|---|
| A. SVG 재batch 368건 | $3.20 | 폐기 트랙 부활 위험 | 보류 |
| **B. PDF 페이지 직접 표시** | $0 | figure-demo 패턴 일반화 | **선택** |
| C. Vision Live | 디바이스 비용 | 풀이 시점 동적 | 보류 |
| D. text만 | $0 | 그림 누락 | 폐기 |

### 다음 단계
- PDF 페이지 PNG 자산 확인 (전체 65회차 분량)
- PWA renderer에 figure_svg fallback → PDF 페이지 표시 로직 추가
- 좌표 매핑 자산 확인 (페이지 통째 표시? 문제 영역 분할?)

### 진행 상태
진행 중 — DEVLOG 박음 + 다음 단계 측정 대기
브랜치: feat/solution-svg-batch

### 관련 산출물
- scripts/verify_data_pdf_mapping.py (268 lines)
- output/data_pdf_mismatch_20260430.json
- app/data/questions.json (5,331건, 미수정)

### 차단 조건
- batch CLI 호출 0
- data/* 수정 0
- app/data/* 수정 0
- 자동 매핑 정정 금지

### 2026-04-30 16:XX — 분기점: 표시 방식 + 작업 분량 결정 대기

**상황**: B 트랙 1단계 측정 완료. 기술적 막힘 0 (PDF 86건 / 변환 코드 있음 / 비용 $0).
남은 결정 = 사용자 영역 2가지.

**(a) 박힌 사실**:
- PNG 자산 현재 거의 0건 → 변환 1회 후 ~100% 매칭 가능
- 변환 비용: $0 (PyMuPDF 로컬, parse_cbt_dasan.py 재활용)
- 변환 결과: 360~576 PNG (0.5~0.75GB)
- 회복 후보 분량 두 기준:
  - 368건 (text+solution 광범위, DEVLOG 본 entry 기록값)
  - 210건 (text만, 더 정확)
  - 차이 158건 = solution에만 "그림" 키워드 (figure 필요성 (b) 의심)

**결정 1 — 표시 방식**:
- A. 페이지 통째 표시 (좌표 매핑 0, 한 페이지에 다른 문제도 같이 보임)
- B. 문제 영역만 잘라서 (좌표 매핑 작업 필요, 현재 2건만 박힘)

**결정 2 — 작업 분량**:
- 368건 (DEVLOG 양식, 광범위)
- 210건 (text 기준, 정확)

**시스템 권장 (직설)**: A + 210건
- 좌표 매핑 0 → 일단 결과 보이는 게 우선
- 깔끔하게 자르는 건 나중 트랙
- text 기준이 더 정확

**사용자 결정**: 미정

**다음 단계 (결정 후)**:
- A + 210건: PyMuPDF 변환 → PWA renderer fallback → 1~2시간
- B: 좌표 매핑 자산 추가 작업 선행 → 비용 큼

**산출물**:
- 본 entry (분기점 기록)
- output/data_pdf_mismatch_20260430.json (검증 결과)
- scripts/verify_data_pdf_mapping.py (검증 로직)

**차단 조건**:
- 사용자 결정 박히기 전 변환 작업 0
- PWA 코드 수정 0
- 좌표 매핑 자동 진행 0

**진행 상태**: 분기점 — 사용자 결정 대기

### 2026-04-30 — 결정 박힘

- 결정 1: **A** (페이지 통째 표시 — 좌표 매핑 0)
- 결정 2: **210건** (text 기준 좁은 패턴, 정확)
- 다음 단계: PDF→PNG 변환 + PWA renderer fallback

---

## 2026-04-30 ~ 05-01 — figure fallback SoT + D54 + 사례 10 회피

**진행**:
- γ-1~4: figure 페이지 매핑 부채 발견 (mathpix 9p ↔ PDF 32p, 다른 단위 박힘)
- ε: PDF→PNG 변환 + verify_data_pdf_mapping.py 직접 측정 박힘
- patch: app/index.html + app/js/{main,render}.js figure_svg → PDF page fallback (B 트랙 폴백)
- D54 도출 — 본 세션에서 체크리스트 4항 도출 (sessions/2026-04-30_체크리스트_D54_도출.md)
  · D54 본문은 verify-agent DECISIONS.md에 별 시점 박힘 (V1은 형식 정정만)
- 사례 10 등재 (verify-agent 5e6a2d3): 다중 도구 환경 인식 ≠ 박힘

**3채널 박힘 매트릭스 (5/1)**:
- DEVLOG (ee-agent): 본 entry — 분기점(line 249) 다음
- Git (ee-agent): C1 61d3f62 (도구) / C2 222e908 (SoT) / C3 4bca0f8 (sessions) / D1 30b4670 (D54 도출) / C4 본 entry
- Git (verify-agent): 5e6a2d3 사례 10 / e0acd6f V1 형식 정정
- Vault: D54 원문대화 + 사례 10 도출 복기

**§1.5 / §1.7 / 사례 10 회피 작동**:
- 진술 1·2 박힘 (figure 트랙 도달 + 저장소 명시)
- 검증 통로 3 (3채널 매트릭스 직접 측정 + commit 단위 분리 + 저장소 명시)
- 4단계 — 진술 → 측정 → plan → 박힘

**잔여 부채 (다음 트랙)**:
- main.js/render.js 참조 (a) — index.html → js import 측정 필요
- B1 (.moai 자동 갱신) 별 commit
- B2 (runner answer-key) 별 commit
- Vault figure 트랙 별도 entry
- feat/solution-svg-batch branch 27건 main 미반영 — 별 트랙 결정

---

## 2026-05-02 — Layer 4 batch 종결 + Layer M 신설

**진행**:
- 추천시스템 측 Layer 4 (Track B, RAG 본문 grep 게이트) 진입
- B 안 (Eager batch 선행) 채택 — 584 concept 일괄 grep
- 첫 batch Index 300까지 정상, Index 301 KeyError → 스키마 이중성 발견
- A 안 (Δ 3줄 fallback) 진행 → 584건 전수 처리 성공 (5.2초)
- B 안 (백업 제외, 3건 commit) — bee40291 박음
- gate 위치 식별 측정 (read-only) — web_ui.py:157/985 식별
- gate 추가는 다음 세션 (별 트랙)
- Layer M (분류 박음 protocol) 신설 + 첫 적용

**5채널 박음 매트릭스 (5/2)**:
- Git (추천시스템): bee40291 — L4 batch
- DECISIONS (verify-agent): D55 (L4 batch), D56 (Layer M)
- CONSTITUTION (verify-agent): 사례 0/7/9 보강
- DEVLOG (ee-agent): 본 entry
- Vault (Obsidian): 00_NAVIGATION.md + 4 entry
- Memory (Claude): #5/#6 갱신, #7 신규

**Layer 진행 매트릭스**:

| Layer | 상태 |
|---|---|
| L1 카탈로그 | ✅ |
| L2 작업 규약 | ✅ |
| L3 사후 정리 | ✅ |
| L4 자동 차단 | 🔄 80% (gate/Q 다음 세션) |
| LM 분류 박음 | 🔄 적용 3건째 |
| L5 멀티 채널 | ❌ |
| L6 Self-Harness | ❌ |

**사례 0 세 발현 정량화**:
1. 메타 노이즈/오타 — 244건
2. 스키마 이중성 — 58건
3. 책 raw 자체 부재 — 128건

**잔여 부채**:
- L4 gate 추가 + Q1/Q2/Q3 평가 (다음 세션 1순위)
- 244 fiction suspect 정리 (별 D-번호)
- 128 unverifiable 처리 (별 D-번호)
- 스키마 B 58건 마이그레이션
- feat/solution-svg-batch 27건 main 미반영
- 백업 정책 일관 결정

**§1.5 / §1.7 / 사례 10 회피 작동**:
- 진술 1·2 박음 (L4 batch 종결 + 저장소 명시)
- 검증 통로 3 (4채널 매트릭스 + commit 단위 분리)
- 4단계: 진술 → 측정 → plan → 박음

---
