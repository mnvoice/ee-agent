# Trap-Map B-Priority — 기기-18 Learning Materials Correction Review (2026-05-23)

correction plan(`d1ca5b2`) Step 5(`6051e21`)의 학습 패키지 기기-18 정정이 정확
하고 범위 내인지 6개 기준으로 리뷰한다. 본 단계는 리뷰 문서만 — 학습 패키지·
questions.json·closeout/errata 미수정.

본 단계는 리뷰 문서 작성까지 — app/data·questions.json 미수정. solution/steps
미적용. answer/choices/text 미수정. 학습 패키지 문서 미수정. closeout/errata
미수정. 유료 API 미호출. local server 미실행. amend/rebase/reset 없음.

- 리뷰 대상 commit: `6051e21`
- 리뷰 대상 파일:
  1. `docs/audit/trap_map_B_priority_pilot_study_set_v1_2026-05-22.md`
  2. `docs/audit/trap_map_B_priority_pilot_day_plan_2026-05-22.md`
  3. `docs/audit/trap_map_B_priority_pilot_learning_log_v1_1_2026-05-22.md`
- 대조 참조:
  - redryrun after correction (`docs/audit/trap_map_B_priority_gigi_18_redryrun_after_correction_2026-05-23.md`)
  - official answer verification (`docs/audit/trap_map_B_priority_gigi_18_official_answer_verification_2026-05-22.md`)
  - 원본 PDF: `data/문제_2010_2회_20260316.pdf` page 8, 문제 47

---

## 판정: **PASS** — Step 7 clean count 갱신·blocked 해제 판단 가능

Step 5 정정은 6개 리뷰 기준을 모두 충족한다. 변경 범위는 기기-18 카드 한정,
정답 (4) 절연내력 기준으로 정합 정정, redryrun(adjacent / ready_with_note) 분류
유지, 원래 카드 함정(1차/2차 환산 혼동) 보존, learning log v1.1 G-1·G-2·G-3
모두 유지, residual(steps · clean count) 처리 적절.

→ **Step 7(closeout/post-closeout errata 후속 erratum · clean count 갱신 ·
기기-18 blocked 해제 결정) 진입 가능.** P0·P1·P2 결함 없음.

---

## 1. 기준별 검토

### 기준 1 — 수정 범위 ✅

| 점검 | 결과 |
|---|---|
| 변경 파일 = 3개 | ✅ study set v1 / day plan / learning log v1.1 (`git diff --name-only 6051e21^ 6051e21`) |
| 각 파일 diff hunk count | ✅ 1 hunk per file (총 3 hunks) |
| 각 hunk 위치 = 기기-18 카드 범위 | ✅ study set @@-54,22 +54,24 (card lines 56-77) / day plan @@-56,21 +56,26 (card lines 59-81) / learning log @@-68,25 +68,27 (card lines 71-94) |
| 다른 카드(기기-17·4·23, 설비-13·14·10·21, 전력-25·18) diff 라인 | ✅ 0건 (각 파일 grep 검증) |
| diff 통계 | ✅ 3 files / +42 / -33 |

→ 수정 범위는 의도된 기기-18 카드 단일 위치 한정.

### 기준 2 — 정답 기준 ✅

| 파일 | (정답 4) 또는 절연내력 등장 (카드 범위) | (정답 2)·전압 변동률 정답처럼 가르치는 문장 |
|---|---|---|
| study set v1 | "(정답 4)" 카드 헤더 + "절연내력" 5회 | **0건** |
| day plan | "(정답 4)" 카드 헤더 + "절연내력" 6회 | **0건** |
| learning log v1.1 | "(정답 4)" 카드 헤더 + "절연내력" 8회 | **0건** |

(tight regex: `정답.*\(2\)|정답.* 2|전압.?변동률` — 3 파일 기기-18 카드 범위 전부 0 hits.)

→ (4) 절연내력 기준으로 일관 정정. (2) 전압 변동률을 정답처럼 가르치는 문장 0건.

### 기준 3 — redryrun 반영 ✅

| redryrun 결과 | 학습 패키지 적용 |
|---|---|
| 판정 = ready_with_note | ✅ 3 파일 카드 헤더에 명시 (`판정: **ready_with_note**` / `ready_with_note`) |
| alignment = adjacent | ✅ 3 파일 카드 헤더에 명시 (`trap alignment: **adjacent**` / `alignment: **adjacent**` / `adjacent / ready_with_note`) |
| 대표 기출이 검증하는 함정 = 시험 범위 식별 | ✅ 3 파일 모두 "시험 범위 식별" 또는 "시험 범위 식별 — 절연내력은 두 시험으로 구할 수 없음" 명시 |
| 절연내력은 무부하시험·단락시험으로 구할 수 없음 | ✅ 3 파일 모두 외울 핵심/오늘 외울 것/1회독 암기에 명시 |
| PDF 풀이 절합 (5종 무부하 항목 + 2종 단락 항목 + 절연내력 별도) | ✅ 3 파일 모두 PDF 풀이 §(1)(2) 항목을 5종/2종으로 인용 |

### 기준 4 — 원래 카드 함정 유지 ✅

| 파일 | "1차/2차 환산 혼동" 라인 | 원래 카드 함정 ↔ 기출 함정 분리 |
|---|---|---|
| study set v1 | ✅ "원래 카드 함정: 1차 환산값과 2차 실제값을 혼동하는 보기." 라인 유지 | ✅ 카드에 별도 두 라인 + "→ 원래 카드 함정(1차/2차 환산 혼동)과 **다르다**" 명시 |
| day plan | ✅ "원래 카드 함정(v3.2): 1차 환산값과 2차 실제값을 혼동하는 보기." 라인 유지 | ✅ "→ 원래 카드 함정과 **다르다**" 명시 |
| learning log v1.1 | ✅ "원래 카드 함정(v3.2): 1차/2차 환산 혼동" 라인 유지 + 칸 3에 [원래 카드 함정] O/X 별도 | ✅ 칸 3에 [대표 기출 함정] 단답 + [원래 카드 함정] O/X 둘 다 prompt |

→ adjacent 분류의 핵심인 두 함정 분리 표기가 전 파일에 유지됨.

### 기준 5 — learning log G-1 / G-2 / G-3 유지 ✅

#### G-1 — 신규 사실·수치·공식 생성 없음

- 1회독 암기·외울 핵심의 모든 항목(철손·여자전류·히스테리시스손·와류손·여자
  어드미턴스·임피던스 와트·임피던스 전압)은 **원본 PDF 풀이 §(1)(2)의 명시 항목**.
- "절연내력은 절연재의 종류에 따라 정해지며 두 시험으로 구할 수 없다"는 PDF
  풀이 문구의 직접 paraphrase.
- "5종/2종/별도"의 수치는 PDF 풀이가 명시한 항목 list의 **tally** — 신규 수치
  생성 아닌 enumeration.
- "절연내력은 회로 가지가 아닌 절연재 특성이라 등가회로 시험 밖" (day plan
  이해할 것/learning log 4회독 등) — PDF "절연재의 종류에 따라 정해진다"의
  논리 paraphrase. 등가회로 = 회로 가지 모델이라는 v3.2 카드의 이미-기재 개념
  + PDF의 절연내력 별도성 결합. 신규 fact 생성 아님 (v3.2·PDF 범위 내 결합).
- → G-1 anti-fabrication 취지 충족.

#### G-2 — 칸 5 [원카드]/[기출]/[core] 라벨 분리 유지

- learning log v1.1 기기-18 카드 칸 5 (예상 오답 패턴):
  - `[기출] 절연내력을 단락시험으로 측정 가능하다고 분류`
  - `[원카드] 1차 환산값과 2차 실제값을 같은 값으로 대입`
  - `[기출] 무부하시험을 절연내력 측정용이라고 답함`
- 라벨 3개 모두 부여, [원카드]/[기출] 분리 명확. [core]는 이번 카드에 미사용
  (해당 패턴이 core 단계 오답이 아니라 [기출]·[원카드] 영역에 모두 매핑됨).
- v1→v1.1 변경 명세표(line 308)는 Step 5 이전의 v1→v1.1 history record로
  **의도적으로 leave** — Step 5는 별도 변경 layer로 본 commit(`6051e21`)이 history.
  표는 v1→v1.1 변경 시점 기록을 정확히 보존하며 G-2 라벨 규약 자체와 충돌 없음.

#### G-3 — questions.json 추가 수정 없음, 학습 문서만 정정

- Step 5 commit(`6051e21`) diff에 `app/data/` 변경 0건.
- closeout/errata 변경 0건 (Step 7 보류).
- 학습 문서 3개만 정정. 학습 문서 외 산출물(redryrun·feasibility review·official
  answer verification·correction plan·Commit A/B evidence supplement·closeout/
  errata 등) 미수정.

### 기준 6 — Residual 처리 ✅

| residual | 처리 |
|---|---|
| steps 필드 잔존 결함 | ✅ 별도 트랙으로 logging — study set 주의 문장 "steps 필드 cleanup은 별도 트랙", day plan 주의 "steps 필드 cleanup은 별도 트랙", learning log 주의 "steps 필드는 별도 cleanup 트랙 대기" |
| clean count 갱신 | ✅ 미행사 — Step 7 보류. closeout(`3f2a840`)·post-closeout errata(`0045ce4`)의 count(확정 클린 35/40 / 기기-17 caution 1/1 / 기기-18 blocked 1/1) 그대로 유지 |
| blocked 해제 | ✅ 미행사 — Step 7에서 학습 패키지 정정 완료 + steps cleanup 트랙 정합 확인 후 결정 |

---

## 2. 수정 필요 항목

### P0 (Step 7 차단) — 없음
### P1 (Step 7 전 권장) — 없음
### P2 (선택) — 없음

해당 사항 없음. 본 Step 5 정정은 사용자 명시 범위(기기-18 카드만)·redryrun
판정(ready_with_note / adjacent)·G-1·G-2·G-3·residual 처리 모두 준수.

### 정밀 확인 (위반 아님, 투명성 기록)

- **learning log v1.1 §변경 명세표(line 308)**: 본 표는 "v1 → v1.1 변경 명세"
  history record로 v1→v1.1 변경 시점의 칸 5 라벨 부여 내용(당시 (2)-era 패턴)을
  그대로 보존. Step 5(`6051e21`)는 v1.1 이후의 별도 변경 layer이며 commit
  history로 추적됨. 현재 카드(line 84-86)의 칸 5와 변경 명세표(line 308)의
  기기-18 row 패턴 텍스트가 다른 것은 layer 차이를 반영한 의도된 설계이며,
  표 제목이 명시적으로 "v1 → v1.1 변경"임을 밝히므로 misleading 없음. P 항목
  아님.
- **칸 5 [core] 라벨 미사용**: G-2 규약상 허용되는 옵션 라벨로, 본 카드의 3개
  오답 패턴이 [기출]·[원카드]에 모두 깨끗하게 매핑돼 [core] 부여가 불요했음.
  라벨 규약 준수 (라벨 부재가 아닌 분류 결과).

---

## 3. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. 수정 범위 (3 파일 / 기기-18 카드만 / 다른 카드 미변경) | ✅ §1 기준 1 |
| 2. (4) 절연내력 기준 정정 / (2) 전압 변동률 0건 | ✅ §1 기준 2 |
| 3. redryrun 반영 (판정·alignment·시험 범위 식별·절연내력 명시) | ✅ §1 기준 3 |
| 4. 원래 카드 함정 유지 (1차/2차 환산 혼동) + 분리 표기 | ✅ §1 기준 4 |
| 5. G-1 / G-2 / G-3 | ✅ §1 기준 5 |
| 6. residual 처리 (steps 별도 트랙 / clean count·blocked 미행사) | ✅ §1 기준 6 |
| P0/P1/P2 분류 | ✅ P0 0 / P1 0 / P2 0 |
| 판정 출력 + 다음 단계 명시 | ✅ §4 |
| 본 리뷰 작성 외 미수정 | ✅ docs/audit/ 신규 1건만 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지·closeout/errata 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## 4. 결론 및 다음 단계

- 판정: **PASS**.
- P0 0건 / P1 0건 / P2 0건. 정밀 확인 2건(v1→v1.1 변경 명세표 historical layer /
  [core] 라벨 미사용) 모두 위반 아닌 의도된 설계로 기록.
- **Step 7 진입 가능** — closeout/post-closeout errata 후속 erratum 작성 +
  clean count 갱신 + 기기-18 blocked 해제 결정.

### Step 7 준비된 입력 (참조용)

- 데이터 부분: `answer=4` / `choices[3]="절연내력"` / `solution` cleanup 완료
  (Commit A `6218d85` + Commit B `753a9b2`).
- 학습 패키지: study set v1 · day plan · learning log v1.1의 기기-18 카드가
  (4) 절연내력 기준 정정 완료 (Step 5 `6051e21`).
- redryrun: `ready_with_note` / `adjacent` (`39be9d9`).
- steps 필드: 여전히 유도전동기(문제 48) 내용 잔존 — **별도 cleanup 트랙**.
  Step 7에서 blocked 해제 시 이 잔존 결함을 caution 사유로 표기할지 정책 결정
  필요.
- B-pilot count 갱신 후보(Step 7 결정 대상):
  - 기기-18: blocked 1/1 → caution 1/1 (steps 결함 잔존) 또는 clean 1/1
    (steps 결함을 외부 트랙으로 분리하고 학습 가능으로 분류).
  - 기기-17: caution 1/1 유지.
  - 확정 클린 (사용 가능): 35/40 → 36/41 (기기-18 사용 가능 전환 시).

(이 문서는 Step 5 정정 리뷰까지 — Step 7 closeout/errata 갱신은 별도 트랙·별도
승인.)

---

## Status

- 기기-18 학습 패키지 정정(Step 5 `6051e21`) 리뷰 완료 — 6개 기준 전수 검토.
- 판정 **PASS**. P0 0 / P1 0 / P2 0.
- 수정 범위(3 파일 / 기기-18 카드만)·정답 (4) 절연내력 기준·redryrun 판정 반영·
  원래 카드 함정 유지·G-1/G-2/G-3·residual 처리 — 전부 충족.
- 정밀 확인 2건(v1→v1.1 변경 명세표 historical record / [core] 라벨 분류 결과)은
  위반 아님.
- **Step 7 진입 가능** — closeout/errata 후속 erratum + clean count 갱신 +
  blocked 해제 결정.
- 이 문서는 리뷰 문서다. 학습 패키지·questions.json·closeout/errata 미수정.
