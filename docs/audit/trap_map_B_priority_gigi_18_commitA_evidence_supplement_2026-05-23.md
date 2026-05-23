# Trap-Map B-Priority — 기기-18 Commit A Evidence Supplement (2026-05-23)

correction plan(`d1ca5b2`) Step 1 / **Commit A**(`6218d85`)의 정정 근거와 범위
검증을 보완 기록한다. 이미 push된 commit은 amend하지 않으며, 본 supplement가
git history에 담기지 못한 source·scope 정보를 별도 문서로 보강한다.

본 단계는 evidence supplement 문서 작성까지 — app/data·questions.json 미수정.
solution/steps 미적용. answer/choices/text 미수정. 학습 패키지 문서 미수정.
유료 API 미호출. local server 미실행. amend/rebase/reset 없음.

---

## 1. Commit A 정보

| 항목 | 값 |
|---|---|
| Commit SHA (long) | `6218d85ef583e7fe7648549a81f64ab6cc60777d` |
| Commit SHA (short) | `6218d85` |
| Author | mnvoice \<mnvoice@naver.com\> |
| Date | 2026-05-23 11:09:16 +0900 |
| Branch | `feat/phase-b-migration` |
| Parent | `d1ca5b2` (correction plan commit) |
| Actual commit message (전문) | `data: correct answer choice for 2010_2회_47\n\n🗿 MoAI <email@mo.ai.kr>` |
| Source 근거 | official answer verification `decaa99` |
| Plan 근거 | correction plan `d1ca5b2` |
| Scope (실제) | `app/data/questions.json` / 단일 레코드 `2010_2회_47` / `answer` + `choices[3]` 두 필드 |

### 권한 부여 출처

사용자 메시지(2026-05-23): "기기-18 correction plan 승인. Step 1 / Commit A만 진행하세요." +
허용 범위(파일/레코드/필드) 명시 + 금지 항목 명시 + 5가지 가드 검증 요구.

본 권한 부여는 correction plan §3·§5 Step 1·§6.5 "별도 명시 승인" 조건을 충족.
plan 자체의 승인이 아닌 Step 1 한정 데이터 수정 권한.

---

## 2. G-1 보완 — Pre/Post Snapshot (git 재구성)

### 2.1 G-1 제약 자기 진술

Commit A 실행 전 `2010_2회_47` 레코드의 pre-commit snapshot을 **파일로 저장하지
않았다.** Edit 실행 직전에는 Read·Bash(python json.load)로 화면 확인만 수행했고,
별도 snapshot 파일(예: `pre-commitA-2010_2회_47.json`)을 생성하지 않았다.

이는 G-1(pre-commit snapshot evidence)의 약점이다. 본 supplement는 그 약점을
보완하기 위해 **git parent tree에서 pre-state를 재구성**해 문서로 박제한다 —
git 자체가 진실의 원천이므로 재구성 가능.

### 2.2 Pre-state (재구성 — `git show 6218d85^:app/data/questions.json` 기준)

`6218d85^` = parent commit `d1ca5b2`. parent tree의 `2010_2회_47` 레코드:

```
answer: 2
choices[0]: '철손'
choices[1]: '전압 변동률'
choices[2]: '동손'
choices[3]: '철손내력'
solution[:40]: '변압기의 시혐\n（1）개방 회로 시험（무부하 시험）으로 측정할 수 있는 항'
solution length: 696
```

### 2.3 Post-state (HEAD `6218d85` 기준)

```
answer: 4
choices[0]: '철손'
choices[1]: '전압 변동률'
choices[2]: '동손'
choices[3]: '절연내력'
solution[:40]: '변압기의 시혐\n（1）개방 회로 시험（무부하 시험）으로 측정할 수 있는 항'
solution length: 696
```

### 2.4 Pre→Post 차이 요약

| 필드 | Pre | Post | 변경 |
|---|---|---|---|
| `answer` | 2 | 4 | 변경 |
| `choices[3]` | "철손내력" | "절연내력" | 변경 |
| `choices[0..2]` | 철손 / 전압 변동률 / 동손 | 동일 | 미변경 |
| `solution[:40]` | 변압기의 시혐\n（1）개방 회로 시험… | 동일 | 미변경 |
| `solution` length | 696 | 696 | 미변경 (전체 본문 동일) |

### 2.5 Rollback 가능성

- 본 commit은 단일 commit으로 isolation됨 → `git revert 6218d85`로 parent
  `d1ca5b2` 상태로 안전 되돌리기 가능.
- revert 시 복구되는 pre-state는 위 2.2와 정확히 일치(git 재구성 검증 완료).
- amend·rebase·reset 미사용으로 commit history가 단순·revert-safe 상태.

---

## 3. G-2 보완 — Commit Message Source/Scope 보강

### 3.1 G-2 제약 자기 진술

Commit A의 실제 commit message는 `data: correct answer choice for 2010_2회_47`로,
요구된 권장 메시지를 그대로 사용했다. 이 메시지는 (a) 변경 분류(data) (b) 동작
(correct) (c) 대상 문항 ID(2010_2회_47)를 담지만 다음을 **포함하지 않는다**:

| 누락 정보 | 의미 |
|---|---|
| source 근거 commit ID | `decaa99` (official answer verification) |
| plan 근거 commit ID | `d1ca5b2` (correction plan) |
| 실제 필드별 변경 (값) | `answer` 2→4, `choices[3]` "철손내력"→"절연내력" |
| scope 명시 (단일 레코드, 2 필드) | 다른 레코드·다른 필드 미변경임을 commit 본문이 직접 진술하지 않음 |
| 공식 정답 (4) 절연내력 명시 | 무엇이 옳은 답인지 commit이 직접 적지 않음 |

git history만으로 위 정보를 추적하려면 plan/verification 문서를 별도로 찾아 봐야
한다. amend 금지 정책으로 commit message 자체는 보강 불가 — 본 supplement가
그 역할을 대신한다.

### 3.2 Supplement에서 보강하는 Source / Scope

**Source 근거**:
- `decaa99` — official answer verification. 원본 PDF `data/문제_2010_2회_20260316.pdf`
  page 8, 지면 "10년도 2회" 문제 47의 인쇄된 보기 ④ "절연내력" + 풀이 끝
  "[답] ④" 직접 대조로 공식 정답 (4) 확정.
- `d1ca5b2` — correction plan. 본 Commit A의 범위·옵션·실행 순서를 사전 정의.
- `0045ce4` — post-closeout errata. 기기-18 blocked·B-pilot 9항 체계로 정정한
  결정.
- `1061a9f` — cleanup feasibility review. answer 충돌·choice OCR·solution 혼입을
  최초 발견.

**Scope (확정)**:
- 파일: `app/data/questions.json` 1개.
- 레코드: `2010_2회_47` 단일 (5,331개 중 1개).
- 필드: `answer`(2→4), `choices[3]`("철손내력"→"절연내력") — 2개.
- 그 외 필드(`text`, `choices[0..2]`, `solution`, `steps`, `solution_svg`,
  `difficulty`, `q_type`, `tag`, `subject`, `quality`)·다른 레코드는 **수정
  없음**.

### 3.3 보강된 commit message 재구성 (참고용, 적용 안 함)

amend 금지로 적용하지 않으나, 기준에 맞춰 다시 쓴다면 다음과 같다(참고만):

```
data(questions.json): correct 2010_2회_47 answer & choice[3]

- answer: 2 → 4 (official: 절연내력, source verification: decaa99)
- choices[3]: "철손내력" → "절연내력" (OCR fix, original PDF confirmed)
- scope: single record / 2 fields; solution/steps/solution_svg/text untouched
- per plan: d1ca5b2 (Step 1 / Commit A)
- per supervisor: 2026-05-23 explicit approval

🗿 MoAI <email@mo.ai.kr>
```

본 재구성은 supplement 본문 기록용. 실제 git history는 `6218d85`의 단순 메시지를
유지한다.

---

## 4. G-3 Evidence — Change Scope (정량)

### 4.1 변경 통계

| 지표 | 값 | 출처 |
|---|---|---|
| Changed files | 1 | `git diff --name-only`: `app/data/questions.json` |
| Insertions | 2 라인 | `git diff --stat`: `2 insertions(+)` |
| Deletions | 2 라인 | `git diff --stat`: `2 deletions(-)` |
| Net 라인 변화 | 0 | 같은 줄 위치에서 대체 |
| Changed records | 1 | `2010_2회_47` |
| Changed fields | 2 | `answer`, `choices[3]` |
| Total records (post) | 5,331 | json.load 후 `len()` |
| Total records (pre) | 5,331 | parent tree json.load (Δ=0) |

### 4.2 정정 값 확인

- `answer`: **4** (Pre 2, official 4) — 정합.
- `choices[3]`: **"절연내력"** (Pre "철손내력", official "절연내력") — 정합.
- `solution`: **unchanged** (Pre/Post 둘 다 `length=696`, prefix `'변압기의 시혐\n（1）...'`).

### 4.3 비변경 영역 잠금

- `choices[0..2]`: `철손` / `전압 변동률` / `동손` — 미변경.
- `text`: `변압기의 무부하시험，단락시험에서 구할 수 없는 것은？` — 미변경.
- `steps`·`solution_svg`·`difficulty`·`q_type`·`tag`·`subject`·`quality`:
  미변경 (`git show 6218d85` diff에 미등장).
- 다른 레코드(예: 인접 `2010_2회_46`, `2010_2회_48` 등): 미변경 (diff hunk가
  `2010_2회_47` 단일 레코드 영역 내, 라인 56991-56999에 한정).

### 4.4 JSON 유효성

- post-commit json.load 성공 (예외 없음), 총 5,331 레코드 로드.
- 레코드 1개에서 필드 2개만 값이 바뀌고 구조(키/타입)는 동일.

---

## 5. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| Commit A 정보 (SHA/메시지/parent/source/scope) | ✅ §1 |
| G-1 — pre-commit snapshot 파일 미생성 자기 진술 + git 재구성 | ✅ §2.1·2.2 |
| G-1 — post-state 기록 | ✅ §2.3 |
| G-1 — rollback 가능성 확인 (`git revert 6218d85`) | ✅ §2.5 |
| G-2 — commit message 누락 정보 명시 | ✅ §3.1 |
| G-2 — source/scope supplement 보강 | ✅ §3.2 |
| G-3 — changed file/record/field count | ✅ §4.1 |
| G-3 — answer=4, choices[3]="절연내력" 확인 | ✅ §4.2 |
| G-3 — solution unchanged | ✅ §4.2·4.3 |
| G-3 — 다른 레코드·필드 비변경 잠금 | ✅ §4.3 |
| 본 supplement 작성 외 데이터 미수정 | ✅ docs/audit/ 신규 1건만 |
| amend/rebase/reset 없음 | ✅ Commit A는 단순 commit, push 후 무수정 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- Commit A(`6218d85`) evidence supplement 작성 완료 — 데이터 미수정.
- G-1 보완: pre-commit snapshot 파일 미생성 자기 진술 + git parent tree 재구성으로
  pre-state(answer=2 / choices[3]="철손내력") 박제, post-state(answer=4 /
  choices[3]="절연내력") 기록, rollback 경로(`git revert 6218d85`) 확인.
- G-2 보완: commit message가 source(decaa99)·plan(d1ca5b2)·필드값·scope 명시를
  포함하지 못함을 진술. amend 금지로 본 supplement가 보강 역할 — §3.2에 명시.
- G-3 evidence: 변경 파일 1 / 레코드 1 / 필드 2 / 라인 +2-2. answer=4·
  choices[3]="절연내력" 정합. solution(length 696)·steps·solution_svg·text·다른
  choices·다른 레코드 전부 미변경.
- Commit B(solution cleanup) 진행 전 evidence 보강 완료. 다음 step은 별도 명시
  승인 대기.
- 이 문서는 evidence supplement다. questions.json·학습 패키지·closeout 미수정,
  기존 commit amend 없음.
