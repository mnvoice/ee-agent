# Trap-Map B-Priority — 기기-18 Commit C Evidence Supplement (2026-05-23)

steps cleanup feasibility(`71f0082`) 승인에 따라 실행한 **Commit C**(`961291e`)의
`steps` cleanup 근거와 범위 검증을 보완 기록한다. 이미 push된 commit은 amend하지
않으며, 본 supplement가 git history에 담기지 못한 source·rationale·scope 정보를
보강한다.

본 단계는 evidence supplement 문서 작성까지 — app/data·questions.json 미수정.
solution/answer/choices/text 미수정. 학습 패키지 문서·closeout/errata 미수정.
유료 API 미호출. local server 미실행. amend/rebase/reset 없음.

---

## 1. Commit C 정보

| 항목 | 값 |
|---|---|
| Commit SHA (long) | `961291ea50666d4964159349670aabf45ae28164` |
| Commit SHA (short) | `961291e` |
| Author | mnvoice \<mnvoice@naver.com\> |
| Date | 2026-05-23 20:19:52 +0900 |
| Branch | `feat/phase-b-migration` |
| Parent | `71f0082` (= steps cleanup feasibility/review 문서 commit) |
| Commit message | `data: clean steps for 2010_2회_47\n\n🗿 MoAI <email@mo.ai.kr>` |
| Source 근거 | steps cleanup feasibility `71f0082` (option **A. proceed_minimal_cleanup**) |
| Plan 근거 | correction plan `d1ca5b2` §3.2 ("steps 별도 트랙") + follow-up erratum `c6d57d0` §5 우선순위 1 |
| Scope (실제) | `app/data/questions.json` / 단일 레코드 `2010_2회_47` / `steps` 필드만 |
| diff 통계 | 1 file changed, 1 insertion(+), 5 deletions(-) |

### 권한 부여 출처

사용자 메시지(2026-05-23): "기기-18 steps cleanup Commit C 진행 승인. 판단:
proceed_minimal_cleanup 채택. 2010_2회_47의 steps 필드를 null로 설정한다." +
허용 범위(파일/레코드/필드: steps only, 수정값 null) + 7가지 검증 요구.

본 권한 부여는 feasibility(`71f0082`) §8 권장 및 correction plan §6.5 "별도
명시 승인" 조건 충족.

---

## 2. Pre/Post Snapshot

### 2.1 Pre-state (`961291e^` = `71f0082` tree 재구성)

```
answer: 4                       (Commit A 정정 결과 유지)
choices[3]: '절연내력'          (Commit A 정정 결과 유지)
solution length: 194            (Commit B cleanup 결과 유지)
steps type: dict
steps keys: ['인식', '변환', '계산']
  steps[인식] type=str len=130
    "문제는 \"유도 전동기의 전부하 회전수\"를 구하는 것으로, 변압기 문제가 아닌
     유도 전동기 문제입니다. 핵심 키워드는 \"3상 유도 전동기\", \"전부하 동손\",
     \"기계손\"이며 ..."
  steps[변환] type=str len=556
    "유도 전동기의 에너지 평형식을 이용합니다.\n\n**동기속도**: N_s = 120f/P =
     900 [rpm]\n\n**슬립**: ..."
  steps[계산] type=str len=190
    "N_s = 900 [rpm]\n\nP_2 = 95 [kW]\n\n... **정답: (4) 약 874[rpm]**"
steps == null count (pre, corpus-wide): 69
total records (pre): 5,331
```

3 sub-key 전부 문제 48(유도전동기 회전수) 내용. 흥미롭게도 `인식` 첫 문장이
*"변압기 문제가 아닌 유도 전동기 문제입니다"*라고 자신의 mis-routing을 자인
— 추출 단계 인접 문항 혼입의 데이터 증언.

### 2.2 Post-state (HEAD `961291e`)

```
answer: 4                       (유지)
choices[3]: '절연내력'          (유지)
solution length: 194            (유지)
solution[:60]: '변압기의 시험\n（1）개방 회로 시험（무부하 시험）으로 측정할 수
                있는 항목\n－무부하 전류－히스테리시스손─와류'
solution_svg length: 3243       (유지)
steps: None
text: '변압기의 무부하시험，단락시험에서 구할 수 없는 것은？'   (유지)
difficulty: 3 / q_type: '개념형' / tag: '변압기의 등가회로'
subject: '전기기기' / quality: 'complete'
steps == null count (post, corpus-wide): 70
total records (post): 5,331
```

→ `steps`가 `dict {인식, 변환, 계산}` (876 chars 총 sub-key 합) → **`null`**로
교체. 다른 모든 필드 미변경.

### 2.3 Pre→Post 차이 요약

| 측정 | Pre | Post | Δ |
|---|---|---|---|
| `steps` 타입 | dict | None | dict → null |
| `steps` 본문 총 길이 (3 sub-key 합) | 876 chars | 0 chars | −876 chars |
| `answer` | 4 | 4 | unchanged |
| `choices[3]` | "절연내력" | "절연내력" | unchanged |
| `solution` length | 194 | 194 | unchanged |
| `solution_svg` length | 3243 | 3243 | unchanged |
| `text` · `difficulty` · `q_type` · `tag` · `subject` · `quality` | (각 값) | (각 값 동일) | unchanged |
| 파일 크기 (전체) | 22,621,553 bytes | 22,620,230 bytes | −1,323 bytes |
| git diff (라인) | — | — | +1 / −5 |
| total records | 5,331 | 5,331 | unchanged |
| corpus-wide `steps == null` 수 | 69 | 70 | **+1** |

---

## 3. Source / Rationale Label

### 3.1 변경 근거 — feasibility option A (proceed_minimal_cleanup) 채택

**근거 layer**:

1. **(a) 현재 데이터 상태**: `steps` dict 3 sub-key 전부 문제 48 유도전동기 내용.
   직접 확인 (Commit C 적용 전 inspection §1).
2. **(a) 원본 PDF**: `data/문제_2010_2회_20260316.pdf` page 8, 문제 47 풀이는
   분류·서술 단락(시험 항목 분류 + 절연내력 별도성), 계산형 식 구조 없음.
3. **(b) 사용자 결정**: option A (proceed_minimal_cleanup) 채택 — feasibility
   `71f0082` 권장 그대로 승인.
4. **(c→a 승격) corpus 관행**: `steps == null` 상태는 5,331 레코드 중 69개가
   사용 중인 **인정된 schema 상태** (feasibility §2). 인위적 추가가 아닌 기존
   관행.

### 3.2 왜 option B (source-grounded rewrite)가 아닌가

PDF 풀이는 `{인식, 변환, 계산}` 3 단계 schema(계산형 친화)와 자연 매핑되지 않음:
- `q_type: '개념형'` — 계산 단계 부재.
- PDF 풀이: 시험 항목 분류 단락 — 변환·계산 단계 부재.
- 강제로 3 단계화 시 PDF에 없는 진술 생성 필요 → G-1 anti-fabrication 위반 위험.

따라서 option B는 채택 안 함. option A가 PDF source-grounded 측면에서 더 안전
(PDF가 3 단계 구조를 제공하지 않으면 steps를 비우는 것이 정직).

### 3.3 왜 option C (defer) / D (no_action)이 아닌가

- option C·D는 contamination 잔존 → app에서 steps 직접 노출 시 잘못된 풀이
  표시 / 데이터 무결성 오염 지속.
- follow-up erratum(`c6d57d0`) §5 우선순위 1로 cleanup을 권장한 상태에서
  defer는 모순.

### 3.4 변경의 source label 분류

| 변경 단위 | 변경 내용 | Source Label |
|---|---|---|
| 단일 변경 — steps dict 제거 후 `null` 설정 | dict {인식, 변환, 계산} (문제 48 혼입) → `null` | **(a) PDF 문제 47 범위 외 + (a) corpus schema 선례 (69 null 레코드) + (b) 사용자 option A 승인** |

신규 사실·수치·공식 **생성 0건**. `null`은 schema 정합 값이며 corpus 내 이미
존재하는 형태.

---

## 4. Scope Evidence

### 4.1 변경 통계 (재기록)

| 지표 | 값 | 출처 |
|---|---|---|
| Changed files | 1 | `git diff --name-only`: `app/data/questions.json` |
| Insertions | 1 라인 | `git diff --stat`: `1 insertion(+)` |
| Deletions | 5 라인 | `git diff --stat`: `5 deletions(-)` |
| Net 라인 변화 | −4 | dict 5 라인 → null 1 라인 |
| Changed records | 1 | `2010_2회_47` |
| Changed fields | 1 | `steps` |
| Total records (post) | 5,331 | json.load `len()` |
| Total records (pre) | 5,331 | parent tree json.load (Δ=0) |
| corpus `steps == null` count | 69 → **70** | json.load 전체 스캔 |
| 파일 크기 | 22,621,553 → 22,620,230 bytes | `wc -c` |

### 4.2 비변경 영역 잠금 (재확인)

| 영역 | 상태 |
|---|---|
| `text` | unchanged ("변압기의 무부하시험，단락시험에서 구할 수 없는 것은？") |
| `choices[0..3]` | unchanged ('철손'·'전압 변동률'·'동손'·'절연내력') |
| `answer` | unchanged (4) — Commit A 결과 유지 |
| `solution` | unchanged (length 194, prefix '변압기의 시험\n（1）...') — Commit B 결과 유지 |
| `solution_svg` | unchanged (length 3,243, "정답: ④ 절연내력" 포함) |
| `difficulty` · `q_type` · `tag` · `subject` · `quality` | unchanged |
| 다른 레코드(5,330개) | unchanged |

### 4.3 JSON 유효성

- post-commit `json.load` 성공, 예외 없음, 총 5,331 레코드.
- 레코드 1개에서 1 필드의 값 타입이 dict → None으로 교체된 것 외 구조 변동 없음.
- `null`은 표준 JSON 값으로 schema 정합.

---

## 5. Rollback 가능성

- Commit C(`961291e`)는 단일 isolated commit으로 격리됨.
- `git revert 961291e` 단일 명령으로 parent `71f0082` tree 상태(steps =
  유도전동기 dict)로 안전 되돌리기 가능.
- revert 시 복구되는 pre-state는 §2.1과 정확히 일치(git 재구성 검증 완료).
- amend·rebase·reset 미사용으로 commit history가 단순·revert-safe 상태.
- 단, revert는 contamination을 다시 들이므로 실용 가치는 낮음 — feasibility 옵션
  결정을 뒤집을 경우에만 사용.

---

## 6. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. Commit C 정보 (SHA·메시지·parent·source·plan·scope) | ✅ §1 |
| 2. Pre/Post snapshot — git parent 재구성 | ✅ §2.1·2.2 |
| 2. Pre→Post 차이 요약 (steps dict → null, 다른 필드 unchanged) | ✅ §2.3 |
| 3. Source/rationale label — feasibility option A 근거 4 layer | ✅ §3.1 |
| 3. Why not B/C/D 명시 | ✅ §3.2·3.3 |
| 3. 변경의 source label (a)·(b) 분류, 신규 fact 0 | ✅ §3.4 |
| 4. Scope evidence — file/record/field 1·1·1, +1/−5, 5,331 records | ✅ §4.1 |
| 4. corpus null count 69 → 70 | ✅ §4.1 |
| 4. 비변경 영역 잠금 (text·choices·answer·solution·solution_svg·메타·다른 레코드) | ✅ §4.2 |
| 4. JSON 유효성 | ✅ §4.3 |
| 5. Rollback 가능성 (`git revert 961291e`) | ✅ §5 |
| 본 supplement 작성 외 데이터·학습 패키지·closeout/errata 미수정 | ✅ docs/audit/ 신규 1건만 |
| 금지사항 준수 | ✅ app/data·questions.json·learning 패키지·closeout/errata 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- Commit C(`961291e`) evidence supplement 작성 완료 — 데이터 미수정.
- Pre/post snapshot git 재구성: `steps` dict (876 chars 합, 3 sub-key 전부
  유도전동기 혼입) → **`null`**. 다른 필드 unchanged. 파일 크기 −1,323 bytes.
- Source label: (a) PDF 문제 47 범위 외 + (a) corpus 69 null 선례 + (b) 사용자
  option A 승인. 신규 사실·수치·공식 0건. option B(rewrite) G-1 위험 회피, C/D
  잔존 비용 회피.
- Scope: 1 file / 1 record / 1 field / +1/−5 / 5,331 records 유지. corpus
  null count 69 → 70 (+1).
- Rollback: `git revert 961291e` 단일 명령으로 parent `71f0082` 상태 복구 가능.
- 다음: 기기-18 redryrun(steps cleanup 후) → follow-up erratum 갱신(caution 2/2
  → 1/1, 완전 클린 34/39 → 35/40)으로 진행 가능 상태.
- 이 문서는 evidence supplement다. questions.json·학습 패키지·closeout/errata
  미수정, 기존 commit amend 없음.
