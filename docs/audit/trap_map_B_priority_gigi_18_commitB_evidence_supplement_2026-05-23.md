# Trap-Map B-Priority — 기기-18 Commit B Evidence Supplement (2026-05-23)

correction plan(`d1ca5b2`) Step 3 / **Commit B**(`753a9b2`)의 solution cleanup
근거와 범위 검증을 보완 기록한다. 이미 push된 commit은 amend하지 않으며, 본
supplement가 git history에 담기지 못한 변경 단위별 source·범위 정보를 보강한다.

본 단계는 evidence supplement 문서 작성까지 — app/data·questions.json 미수정.
solution/steps 미적용. answer/choices/text 미수정. 학습 패키지 문서 미수정.
유료 API 미호출. local server 미실행. amend/rebase/reset 없음.

---

## 1. Commit B 정보

| 항목 | 값 |
|---|---|
| Commit SHA (long) | `753a9b2e8e011a5b9cff84debf5525127b6479c0` |
| Commit SHA (short) | `753a9b2` |
| Author | mnvoice \<mnvoice@naver.com\> |
| Date | 2026-05-23 18:16:46 +0900 |
| Branch | `feat/phase-b-migration` |
| Parent | `cc46d66` (= Commit A evidence supplement) |
| Commit message | `data: clean solution for 2010_2회_47\n\n🗿 MoAI <email@mo.ai.kr>` |
| Source 근거 | official answer verification `decaa99` + 원본 PDF `data/문제_2010_2회_20260316.pdf` 문제 47 풀이 |
| Plan 근거 | correction plan `d1ca5b2` (Step 3, 옵션 S2) |
| Scope (실제) | `app/data/questions.json` / 단일 레코드 `2010_2회_47` / `solution` 필드만 |
| diff 통계 | 1 file changed, 1 insertion(+), 1 deletion(-) |

### 권한 부여 출처

사용자 메시지(2026-05-23): "기기-18 correction plan Step 3 / Commit B 진행 승인."
+ 허용 범위(파일/레코드/필드: solution only) + 허용 작업(문제 48 혼입 제거 + OCR
미세 정리, source-grounded only) + 전면 재작성·새 풀이 창작 금지 + 7가지 검증
요구.

본 권한 부여는 correction plan §3·§5 Step 3·§6.1·6.5 조건을 충족.

---

## 2. G-1 보완 — 변경 단위별 Source Label

본 commit의 모든 변경은 **원본 PDF 문제 47 풀이**라는 (a) 출처에 source-grounded.
변경 단위별 매핑:

| 변경 단위 | Pre | Post | Source Label | 근거 |
|---|---|---|---|---|
| C-1 Part 2 제거 | `\n\n문제 \(483000... ［답］（4）` (유도전동기 회전수 문항+풀이, 554 source-encoded 문자) | (제거) | **(a) PDF 문제 47 범위 외** | 원본 PDF 문제 47 풀이에 해당 내용 없음. 해당 내용은 원본 PDF 문제 **48**의 본문·풀이로 확인 — 인접 문항 추출 오류 |
| C-2 시혐 → 시험 | "변압기의 **시혐**" / "단락 **시혐**으로" (2 위치) | "변압기의 **시험**" / "단락 **시험**으로" | **(a) OCR/PDF 문구 매칭** | 원본 PDF: "변압기의 **시험**", "단락 **시험**으로 측정" — "혐"은 "험"의 OCR 오인 |
| C-3 히스태리시스솜 → 히스테리시스손 | "－**히스태리시스솜**－" (1 위치) | "－**히스테리시스손**－" | **(a) OCR/PDF 문구 매칭** | 원본 PDF: "**히스테리시스손**" — "태"는 "테"의, "솜"은 "손"의 OCR 오인 |
| C-4 철솜 → 철손 | "－**철솜**" (1 위치) | "－**철손**" | **(a) OCR/PDF 문구 매칭** | 원본 PDF: "**철손**" — "솜"은 "손"의 OCR 오인 (C-3과 동일 오인 패턴) |
| C-5 무부 하 시험 → 무부하 시험 | "**무부 하 시험**과 단락시험" (1 위치, 잉여 공백) | "**무부하 시험**과 단락시험" | **(a) OCR/PDF 문구 매칭** | 원본 PDF: "**무부하 시험**과 단락시험" — 단어 중간의 잉여 공백 제거 |

### Source 등급 정리

- **(a) 출처 — 원본 PDF (`data/문제_2010_2회_20260316.pdf`)**: 모든 변경 단위.
- **(b) 출처 — 사용자 발화**: correction plan §6 옵션 S2 명시("PDF 정합")에
  사용자 승인.
- **(c) 추정**: 본 commit에 (c) 추정 0건. 모든 변경 단위에 PDF 출처 매핑 존재.

### 전면 재작성·창작 금지 준수

- 새 문장·예시·식·풀이 단계 **추가 없음**. 모든 post-state 텍스트는 pre-state의
  부분집합(또는 부분집합의 character-level 정정)에 한정.
- C-1은 문장 제거(잘라내기). C-2~C-5는 character-level 정정. 어느 것도 신규 텍스트
  생성을 수반하지 않음.

---

## 3. G-2 보완 — Pre/Post Snapshot + Diff Size

### 3.1 Pre-state (`753a9b2^` = `cc46d66` tree 재구성)

```
answer: 4
choices[3]: '절연내력'
solution length (decoded): 696 chars
solution[:50]: '변압기의 시혐\n（1）개방 회로 시험（무부하 시험）으로 측정할 수 있는 항목\n－무부하 전류－'
solution[-50:]: ' \\frac{120 \\times 60}{8}=874[\\mathrm{rpm}]\\)［답］（4）'
Part 2 markers presence:
  '483000': True
  '유도 전동기': True
  '회전수는': True
```

(Note: parent `cc46d66`는 Commit A evidence supplement이며 동일 데이터 상태를
가짐. 실질적 데이터 변경 직전 상태는 `6218d85` = Commit A 결과와 동일.)

### 3.2 Post-state (HEAD `753a9b2`)

```
answer: 4
choices[3]: '절연내력'
solution length (decoded): 194 chars
solution (full decoded):
변압기의 시험
（1）개방 회로 시험（무부하 시험）으로 측정할 수 있는 항목
－무부하 전류－히스테리시스손－와류손
－여자 어드미턴스－철손
（2）단락 시험으로 측정할 수 있는 항목
－임피던스 와트（전부하 동손）－임피던스 전압（전압 강하）

그러나，절연내력은 절연재의 종류에 따라 정해지는 것으로서 무부하 시험과 단락시험으로는 구할 수 없다．
［답］（4）
```

### 3.3 Diff Size 분석

| 측정 | Pre | Post | Δ |
|---|---|---|---|
| solution 디코딩 길이 (chars) | 696 | 194 | **−502** |
| solution 소스 인코딩 길이 (file bytes excl. JSON quotes) | 757 | 202 | **−555** |
| Part 2 source-encoded 길이 (제거분) | — | — | 554 |
| OCR 미세 정정 net Δ (소스 인코딩) | — | — | −1 (무부 하→무부하 공백 1 제거; C-2~C-4는 길이 보존) |
| git diff 라인 변동 | — | — | +1 / −1 (같은 라인 위치 대체) |
| changed file/record/field | — | — | 1 / 1 / 1 |

### 3.4 길이 축소의 의미 — "전면 재작성"이 아닌 "혼입 제거 + 미세 정정"

- 길이 감소 −502자(decoded)의 거의 전부(−501자)가 **C-1 Part 2 혼입 제거**에서 발생.
- C-2~C-5는 character-level 정정으로 길이가 사실상 변하지 않음(C-5만 공백 1자 감소).
- 따라서 본 commit은 **전면 재작성이 아님** — 잘못 혼입된 인접 문항(문제 48)을
  제거하고 문제 47의 표기 OCR을 PDF 문구대로 다듬은 것.
- post-state 본문 9개 절(변압기의 시험 / (1) 무부하시험 측정 항목 5개 / (2)
  단락시험 측정 항목 2개 / 절연내력 단서 / [답](4))은 pre-state Part 1의 절들과
  1:1 대응. 추가된 절·문장 0건.

---

## 4. G-3 보완 — PDF Source 인용

### 4.1 PDF 파일·위치

| 항목 | 값 |
|---|---|
| PDF 파일명 | `data/문제_2010_2회_20260316.pdf` |
| Crop 출처 commit | `decaa99` verification §1 (원본 PDF 접근·조회 기록) |
| PDF 페이지 | PDF 8 페이지 (지면 라벨 "2-29 / 10년도 2회") |
| 시리즈 | "전기기사 필기 D-60 시리즈" 2010년 2회 기출문제집 |
| 문제 번호 | 문제 47 (3과목 전기기기) |

### 4.2 원본 PDF 문제 47 풀이 발췌 (재인용 — `decaa99` §1 동일)

```
문제 47  변압기의 무부하시험, 단락시험에서 구할 수 없는 것은?
 ① 철손        ② 전압 변동률
 ③ 동손        ④ 절연내력

풀이
변압기의 시험
 (1) 개방 회로 시험(무부하 시험)으로 측정할 수 있는 항목
   · 무부하 전류 · 히스테리시스손 · 와류손 · 여자 어드미턴스 · 철손
 (2) 단락 시험으로 측정할 수 있는 항목
   · 임피던스 와트(전부하 동손) · 임피던스 전압(전압 강하)
 그러나, 절연내력은 절연재의 종류에 따라 정해지는 것으로서 무부하
 시험과 단락시험으로는 구할 수 없다.   [답] ④
```

### 4.3 정정 후 solution이 발췌 범위와 정합함

post-state solution의 모든 절을 PDF 풀이의 절과 매핑:

| post-state 절 | PDF 풀이 절 | 정합 |
|---|---|---|
| "변압기의 시험" | "변압기의 시험" | ✅ exact |
| "（1）개방 회로 시험（무부하 시험）으로 측정할 수 있는 항목" | "(1) 개방 회로 시험(무부하 시험)으로 측정할 수 있는 항목" | ✅ (괄호 폭만 다름, 의미 동일) |
| "－무부하 전류－히스테리시스손－와류손" | "· 무부하 전류 · 히스테리시스손 · 와류손" | ✅ (구분 기호만 다름) |
| "－여자 어드미턴스－철손" | "· 여자 어드미턴스 · 철손" | ✅ |
| "（2）단락 시험으로 측정할 수 있는 항목" | "(2) 단락 시험으로 측정할 수 있는 항목" | ✅ |
| "－임피던스 와트（전부하 동손）－임피던스 전압（전압 강하）" | "· 임피던스 와트(전부하 동손) · 임피던스 전압(전압 강하)" | ✅ |
| "그러나，절연내력은 절연재의 종류에 따라 정해지는 것으로서 무부하 시험과 단락시험으로는 구할 수 없다．" | "그러나, 절연내력은 절연재의 종류에 따라 정해지는 것으로서 무부하 시험과 단락시험으로는 구할 수 없다." | ✅ |
| "［답］（4）" | "[답] ④" | ✅ (괄호 폭·번호 표기만 다름) |

post-state는 PDF 풀이 발췌 범위 **안**에 한정되며, 범위 밖 내용(예: 문제 48의
유도전동기 회전수)은 0건. 신규 문장·식·예시 0건.

스타일 차이(전각 vs 반각 괄호·구분 기호 "－" vs "·" 등)는 questions.json 전체의
표기 관행(Mathpix 기반 추출 결과)이며, 본 commit이 도입한 것이 아닌 pre-state
부터 동일. 의미·정답·풀이 논리에 영향 없음.

---

## 5. 사후 검증 V1~V7 (재기록)

| # | 검증 | 결과 |
|---|---|---|
| V1 | diff가 `app/data/questions.json` 1개 파일만 포함 | ✅ `git diff --name-only` |
| V2 | diff가 `2010_2회_47` 단일 레코드에만 있음 | ✅ diff hunk = line 56997 단일, 레코드 범위(56984-57008) 내 |
| V3 | 변경 필드가 `solution` 뿐 | ✅ diff = solution 라인 1개 (1 ins / 1 del) |
| V4 | `answer=4`, `choices[3]="절연내력"` 유지 (Commit A 결과 보존) | ✅ post-state 확인 |
| V5 | 문제 48 혼입 제거 | ✅ 마커 `483000`·`유도 전동기`·`회전수는`·`문제 \(` 모두 0 hits |
| V6 | solution이 원본 PDF 문제 47 풀이 범위 내 | ✅ §4.3 절별 매핑, 범위 밖 0건 |
| V7 | JSON parse 정상, 총 레코드 5,331 유지 | ✅ json.load 성공, len()=5331 |

비변경 영역 잠금 (재확인):
- `text`, `choices[0..2]`, `choices[3]`, `answer`, `steps`, `solution_svg`,
  `difficulty`, `q_type`, `tag`, `subject`, `quality`: 미변경.
- 다른 레코드(인접 `2010_2회_46`·`2010_2회_48` 포함): 미변경.

---

## 6. 자체 점검

| 점검 항목 | 결과 |
|---|---|
| 1. Commit B 정보 (SHA/메시지/parent/source/plan/scope) | ✅ §1 |
| 2. G-1 — 변경 단위별 source label (5건 전수) | ✅ §2.1 — C-1 PDF 범위 외·C-2~C-5 OCR/PDF 매칭 |
| 2. G-1 — source 등급 정리 ((a)/(b)/(c) 분류) | ✅ §2.2 — (a) 5건·(b) 1건·(c) 0건 |
| 2. G-1 — 전면 재작성·창작 금지 준수 | ✅ §2.3 |
| 3. G-2 — pre/post snapshot (git 재구성) | ✅ §3.1·3.2 |
| 3. G-2 — diff size 분석 (decoded/source-encoded 둘 다) | ✅ §3.3 |
| 3. G-2 — "전면 재작성 아닌 혼입 제거+미세 정정" 명시 | ✅ §3.4 |
| 4. G-3 — PDF 파일명·page 정보 | ✅ §4.1 |
| 4. G-3 — 문제 47 풀이 발췌 | ✅ §4.2 |
| 4. G-3 — post-state ↔ 발췌 범위 절별 매핑 | ✅ §4.3 |
| 5. 사후 검증 V1~V7 재기록 | ✅ §5 |
| 본 supplement 작성 외 데이터 미수정 | ✅ docs/audit/ 신규 1건만 |
| amend/rebase/reset 없음 | ✅ Commit B는 단순 commit, push 후 무수정 |
| 금지사항 준수 | ✅ app/data·questions.json·answer/choices/text·solution/steps·학습 패키지 미수정 / API·server 미실행 / amend·rebase·reset 없음 |

---

## Status

- Commit B(`753a9b2`) evidence supplement 작성 완료 — 데이터 미수정.
- G-1 보완: 5개 변경 단위(C-1~C-5) 전부 source label (a) 원본 PDF로 매핑.
  (c) 추정 0건, 신규 텍스트·식 0건. 전면 재작성 아님(문제 48 혼입 제거 + Part 1
  OCR 미세 정정).
- G-2 보완: pre/post snapshot git 재구성. solution decoded 696 → 194(−502),
  source-encoded 757 → 202(−555). 감소분의 거의 전부가 C-1 Part 2 제거.
- G-3 보완: PDF `data/문제_2010_2회_20260316.pdf` page 8 문제 47 풀이 발췌
  인용. post-state solution 8개 절을 PDF 풀이 절과 1:1 매핑, 범위 밖 0건.
- V1~V7 재확인. Commit B 단계는 보강 완료. Step 4 (기기-18 redryrun)로 진행
  가능 상태.
- 이 문서는 evidence supplement다. questions.json·학습 패키지·closeout 미수정,
  기존 commit amend 없음.
