# Trap-Map B-Priority — 기기-18 Correction Plan (2026-05-23)

기기-18 official answer verification(`decaa99`)에서 공식 정답을 (4) 절연내력으로
확정한 뒤, 데이터 수정 *전 단계*로 작성하는 correction plan 문서다. 본 plan은
수정 범위·승인 범위·실행 순서·후속 문서 재작성 범위·위험 관리를 명문화한다.

이번 단계는 plan 작성만 — **app/data·questions.json·학습 패키지 문서 미수정**.
solution/steps 미적용. answer/choices/text 미수정. 유료 API 미호출. local server
미실행. 데이터 수정은 본 plan 승인 후 별도 트랙·별도 commit으로 진행.

- 검토 대상: 기기-18 변압기 등가회로 / 대표 기출 `2010_2회_47`
- 참조:
  - 기기-18 official answer verification (`docs/audit/trap_map_B_priority_gigi_18_official_answer_verification_2026-05-22.md`)
  - post-closeout errata (`docs/audit/trap_map_B_priority_post_closeout_errata_2026-05-22.md`)
  - cleanup feasibility review (`docs/audit/trap_map_B_priority_cleanup_feasibility_review_2026-05-22.md`)
  - B-pilot closeout (`docs/audit/trap_map_B_priority_pilot_learning_package_closeout_2026-05-22.md`)
  - 원본 PDF: `data/문제_2010_2회_20260316.pdf` (page 8, 지면 "10년도 2회" 문제 47)

---

## 1. 현재 결함 요약

| 결함 ID | 위치 | 현재 값 | 공식/원본 PDF | 분류 |
|---|---|---|---|---|
| D-1 | `2010_2회_47` `answer` | `2` | `4` | answer 오류 (확정) |
| D-2 | `2010_2회_47` `choices[3]` | `"철손내력"` | `"절연내력"` | choice OCR 오류 (확정) |
| D-3 | `2010_2회_47` `solution` (후반부) | 본 문제(절연내력) 풀이 뒤에 문제 48(유도전동기 회전수) 문제+풀이 혼입 | 본 문제(47) 풀이만 존재 | solution 인접 문항 혼입 (별도 결함) |
| D-4 | `2010_2회_47` `solution` (전반부) | "시혐"·"솜" 등 일부 OCR 표기(예: "변압기의 시혐", "히스태리시스솜", "철솜") | "시험"·"손" 표기 | solution 표기 OCR 미세 garble (선택적 정리 대상) |

### B-pilot 학습 패키지가 정답 (2)로 작성된 영향

study set v1·day plan·learning log v1.1의 기기-18 카드는 정답을 **(2) 전압 변동률**로
명시하고, "외울 핵심 문장 / 3회독 함정 즉답 체크 / 예상 오답 패턴 / 틀리면 돌아갈
원리"를 (2) 기준으로 구성. 공식 정답 (4)와 모순 — **오답 학습 상태 확정**.

기기-18 학습 카드의 trap alignment는 adjacent(시험-파라미터 식별)였고, 정답 (4)
절연내력 기준에서도 같은 adjacent 검증이 유지된다 — 카드의 함정 분류·alignment·
판정은 유지하되, *정답 표기와 그것을 둘러싼 즉답 체크·오답 패턴*은 (4) 기준으로
재작성해야 한다.

---

## 2. Source 근거

- **공식 정답 (4) 절연내력**: `decaa99` verification §2 — 원본 PDF 문제 47의
  인쇄된 보기 ④="절연내력" + 풀이 끝 "[답] ④" 직접 대조로 확정. 추정 아닌
  source 대조.
- **choice[3] "절연내력" 확정**: `decaa99` verification §3 — 원본 PDF 보기 ④
  텍스트가 "절연내력".
- **D-3 (solution 혼입)은 별도 결함**: `decaa99` verification §5 — 혼입 내용은
  원본 PDF에서 문제 47 바로 다음 문항인 문제 48(3000V·60Hz·8극·100kW 3상
  유도전동기 전부하 회전수, [답] ④)로 확인. 인접 문항 추출 단계 오류. 정답 판정
  근거로 **사용하지 않음** — 본 plan에서도 정답 결정 근거가 아니라 별도 cleanup
  대상으로만 다룬다.

---

## 3. 수정 승인 요청 범위 (단일 레코드 한정)

**대상 파일**: `app/data/questions.json`
**대상 레코드**: `2010_2회_47` (year=2010, session="2회", q_no=47) — **단일 레코드**

### 3.1 허용 필드(수정 후보)

| 필드 | 현재 | 정정 후보 | 근거 |
|---|---|---|---|
| `answer` | `2` | `4` | 원본 PDF [답] ④ |
| `choices[3]` | `"철손내력"` | `"절연내력"` | 원본 PDF 보기 ④ |
| `solution` | 47 풀이 + 48 문제·풀이 혼입 | (옵션 S1) 48 혼입만 제거, 47 풀이 그대로 / (옵션 S2) 48 혼입 제거 + 47 풀이의 미세 OCR 표기 정정(시혐→시험, 솜→손) | 원본 PDF 풀이 문구 (§6 옵션 비교) |

### 3.2 수정 금지 필드(이번 correction 범위 외)

- `text` — 원본과 정합, 수정 없음.
- `choices[0]`, `choices[1]`, `choices[2]` — 원본과 정합, 수정 없음.
- `subject`, `tag`, `q_type`, `difficulty`, `quality` — 본 correction 범위 외.
- `steps` — solution과 별개 필드. 정정이 필요하나, 본 correction은 정답 정합과
  최소 cleanup에 집중하므로 steps는 **별도 트랙**으로 분리(이번 범위 외).
- `solution_svg` — 시각화 자산. 정답 (4) 기준 재생성이 이상적이나 SVG 재작성은
  별도 디자인 트랙 — 본 correction 범위 외.
- **다른 레코드** — `2010_2회_48` 포함 어떤 다른 레코드도 본 correction에서 수정
  금지. 인접 문항 추출 오류는 추출 파이프라인 회귀로 별도 트랙.

---

## 4. 후속 학습 패키지 재작성 범위 (본 plan 단계에서는 미작성)

본 correction이 승인·실행되면 아래 문서들의 기기-18 항목을 (4) 절연내력 기준으로
재작성해야 한다 — **본 plan 단계에서는 작성하지 않는다**(plan만 정의).

| 문서 | 재작성 대상 |
|---|---|
| `trap_map_B_priority_pilot_study_set_v1_2026-05-22.md` | [기기-18] 카드 — 정답·외울 핵심 문장·3회독 체크·주의 문장 (4) 기준 |
| `trap_map_B_priority_pilot_day_plan_2026-05-22.md` | Day 1 [기기-18] 카드 — 오늘 외울 것·3회독 체크·예상 오답 패턴·주의 (4) 기준 |
| `trap_map_B_priority_pilot_learning_log_v1_1_2026-05-22.md` | Day 1 [기기-18] 카드 6칸 + 라벨 — (4) 기준, 라벨 [원카드]/[기출]/[core] 재할당 검토 |
| `trap_map_B_priority_pilot_learning_package_closeout_2026-05-22.md` | clean count·accepted residual 갱신(blocked 해제 여부 기록) |
| `trap_map_B_priority_post_closeout_errata_2026-05-22.md` | 후속 erratum으로 정정 완료·blocked 해제 기록 |

학습 카드 재작성 시 alignment·판정 유지 후보:
- alignment: **adjacent** (시험-파라미터 식별) — (4) 정답으로도 동일 trap alignment.
- 판정: **ready** 또는 **ready_with_note** 재평가. 정답 정정·choice OCR 정리 후
  source-clean이 되면 ready 승격 검토 가능.

---

## 5. 권장 실행 순서

| Step | 작업 | 산출물·검증 | 가드 |
|---|---|---|---|
| 1 | questions.json `2010_2회_47` 정정 — `answer` 2→4, `choices[3]` "철손내력"→"절연내력" (Commit A) | git diff: 2 필드 변경만, 다른 레코드 변경 0 | answer/choices 수정 명시 승인 |
| 2 | Commit A diff 검증 | `python3 -c "...print rec"`로 정정 후 레코드 직접 확인, 다른 레코드 hash 영향 점검 | 검증 실패 시 즉시 revert |
| 3 | questions.json `solution` 필드 cleanup — 옵션 S1 또는 S2 적용 (Commit B, 별도) | git diff: solution 필드 1개 변경, 47 외 변경 0 | solution 수정 명시 승인 |
| 4 | 기기-18 representative re-dryrun 재실행 (read-only) | 새 redryrun 문서 — (4) 정답 기준 source-clean·정답 정합 재확인 | 추론 금지, questions.json 미수정 |
| 5 | B-pilot study set v1·day plan·learning log v1.1 기기-18 카드 정정 (별도 commit 또는 v1.2 발행) | 학습 패키지 문서 갱신 | 정정 외 항목 미수정 |
| 6 | 학습 카드 정정 review (PASS 시) | review 문서 | review 게이트 통과 시 다음 |
| 7 | closeout/post-closeout errata 후속 erratum 작성 — clean count 갱신, 기기-18 blocked 해제 여부 결정 | 후속 erratum 문서 | clean count: 확정 클린 36/41 가능성 검토 |

Step 1·3의 commit 분리는 §6 위험 관리 권고에 따른 것 — 결합 가능하나 분리가 안전.

---

## 6. 위험 관리

### 6.1 추론 금지·최소 수정 원칙
- solution을 추론으로 장황하게 새로 작성하지 않는다. 원본 PDF 풀이 문구만 근거로
  사용하며, 그 외 새로운 풀이 표현·예시·식을 *추가하지 않는다*.
- 원본 PDF 풀이 문구가 명시한 항목(무부하시험·단락시험에서 측정 가능한 항목들과
  절연내력이 별도시험임)만 solution에 남긴다.

### 6.2 solution cleanup 옵션 비교

| 옵션 | 내용 | 장점 | 단점 |
|---|---|---|---|
| **S1 (최소)** | 문제 48 혼입만 제거. 47 풀이 본문은 현재 표기(시혐·솜 garble 포함) 그대로 유지 | 변경 폭 최소, 표기 inference 0 | 미세 OCR garble 잔존 |
| **S2 (PDF 정합 — 권장)** | 문제 48 혼입 제거 + 47 풀이의 미세 OCR 표기를 원본 PDF 문구대로 정정(시혐→시험, 솜→손, 무부 하→무부하 등) | 원본 PDF와 표기 정합, 학습 자료 노출 시 가독성 향상 | 변경 폭 약간 증가 (단, 모든 변경이 PDF 텍스트로부터 source-grounded) |
| S3 (전면 재작성) | solution을 새로 작성 | — | **금지** — 추론 위험, §6.1 위반 |

권장: **S2** — 모든 글자 정정이 원본 PDF 텍스트에서 직접 가져온 것이므로 추론
없음, 표기만 정합. 검토자가 더 보수적이라면 S1도 허용.

### 6.3 commit 분리 권고 — answer/choice vs solution
- 권장: **2 commit 분리**.
  - Commit A: `answer` + `choices[3]` 정정 (정답 정합 — 의미·정답 변경).
  - Commit B: `solution` 옵션 S2 (또는 S1) 적용 (cleanup — 텍스트 정리).
- 사유: 정답 정합(Commit A)은 학습 내용에 즉시 영향. solution cleanup(Commit B)은
  텍스트 정리. 두 변경을 분리하면 (a) 회귀 시 부분 롤백 가능, (b) review에서 두
  성격의 변경을 별도 평가 가능, (c) git blame 명확. 결합도 가능하나 분리가 안전.
- 분리 시 가드: 두 commit 사이에 Step 2(diff 검증)을 두고, Commit A 후 즉시
  검증·승인 후에만 Commit B 진행.

### 6.4 다른 영역 회귀 차단
- `2010_2회_47` 외 어떤 레코드도 변경 금지. git diff에서 변경 범위가 1 레코드·
  최대 3 필드(S2 적용 시)로 한정됨을 매 commit 후 확인.
- steps·solution_svg는 본 correction 범위 외 — 향후 별도 트랙. 정답 (4) 변경이
  steps·solution_svg와 비정합을 만들 수 있으므로, 후속 트랙에서 점검 필요.

### 6.5 app/data 수정은 별도 명시 승인 후만
본 plan은 plan 작성까지. Step 1·3(questions.json 수정)은 사용자의 *명시적 추가
승인* 후에만 실행. plan 승인 ≠ 데이터 수정 승인. plan 승인 시 다음 step의 권한
범위(Commit A만, A+B 모두 등)를 명시하도록 한다.

### 6.6 학습 패키지 문서 수정도 별도 승인
Step 5(학습 패키지 카드 정정)도 별도 승인 필요. 현 체인의 학습 패키지 문서(study
set v1·day plan·learning log v1.1)는 모두 PASS review 완료 — 정정은 v1.2 등 새
버전으로 발행하거나 별도 erratum 부착이 안전.

---

## 7. Supervisor Decision Log

| 시점 | 결정 | 근거 commit |
|---|---|---|
| 2026-05-22 | feasibility review에서 기기-18 정답 충돌 escalation | `1061a9f` |
| 2026-05-22 | post-closeout errata에서 기기-18 blocked·B-pilot 9항 체계로 정정 | `0045ce4` |
| 2026-05-22 | official answer verification 완료 — 분기 2(공식 정답 4) 확정 | `decaa99` |
| 2026-05-23 | 사용자 결정: **기기-18 correction track 확정** (needs_replacement 아님), B-pilot에서 정정 전까지 **blocked 유지**, **correction plan 먼저 작성 후 별도 승인 받아 데이터 수정** | 본 plan (`docs: plan correction for B-priority 기기-18`) |
| (대기) | plan 승인 + Step 1·3 데이터 수정 권한 부여 | 대기 중 |
| (대기) | Step 5 학습 패키지 카드 정정 권한 부여 | 대기 중 |

본 plan 승인 후 진행 가능한 작업: Step 1~7. 각 step은 명시 승인 후 수행.

---

## 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. 현재 결함 요약 (answer/choice/solution 혼입/학습 패키지 영향) | ✅ §1 |
| 2. source 근거 (verification 문서 + 원본 PDF + solution 혼입은 별도 결함) | ✅ §2 |
| 3. 수정 승인 요청 범위 (단일 레코드, 허용 필드 후보, 금지 필드 명시) | ✅ §3 |
| 4. 후속 학습 패키지 재작성 범위 (plan 단계 미작성 명시) | ✅ §4 |
| 5. 권장 실행 순서 (Step 1~7) | ✅ §5 |
| 6. 위험 관리 (추론 금지·옵션 비교·commit 분리·승인 분리) | ✅ §6 |
| 7. supervisor decision log (correction track 확정·blocked 유지·승인 대기) | ✅ §7 |
| plan만 작성, 데이터·학습 패키지 미수정 | ✅ docs/audit/ 신규 문서 1건만 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- 기기-18 correction plan 작성 완료 — 데이터 수정 전 단계.
- 대상: `app/data/questions.json` `2010_2회_47` **단일 레코드** / 허용 필드:
  `answer`(2→4), `choices[3]`("철손내력"→"절연내력"), `solution`(혼입 제거 ±
  미세 OCR 정정).
- 권장 옵션: solution cleanup **S2**(PDF 정합, 추론 없음). commit 분리 — Commit A
  (answer+choice) → 검증 → Commit B (solution).
- 후속 학습 패키지 재작성(study set/day plan/learning log/closeout/errata)은 본
  plan 범위 밖 — Step 5 별도 승인 후.
- supervisor decision log: correction track 확정 / blocked 유지 / plan 후 승인
  대기. plan 승인 ≠ 데이터 수정 승인.
- 이 문서는 correction plan이다. questions.json·학습 패키지·closeout 미수정.
