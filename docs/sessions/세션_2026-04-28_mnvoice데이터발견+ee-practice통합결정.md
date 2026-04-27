# 세션 2026-04-28 — ee-practice 디자인 검증 + mnvoice 데이터 발견

## 메타

- **선행 세션**: `세션_2026-04-27_ee-agent_정답키패치+풀이도구MVP.md`
- **시작 시점**: 4/27 세션 종료 후 사용자가 ee-practice 셋업 완료, iPad 접속 시작
- **이 세션의 핵심 발견**: 사용자가 **이미 만들어둔 도구**(mnvoice.github.io)와 **5,307건 데이터**가 존재함을 사용자가 환기. 4/27 세션은 *바퀴 재발명* 위에 있었음
- **종료 상태**: 통합 방향 결정됨 — *mnvoice 데이터 + ee-practice 학습 도구 디자인*. 1단계 작업 패키지 작성됨, 실행 대기

## 1. 4/27 세션 끝낸 후 화면 점검

iPad에서 v1 디자인을 다시 보고 사용자가 **"이 디자인에서 제공하는 내용이 매우 마음에 들었다"** 표명. v2 펜 캔버스보다 v1 두 textarea(이해/암기) + 학습 네비게이션 패널이 더 만족스러움.

분석 — 펜 추가가 잃은 것:
- 이해/암기 *라벨*이 사라져 사용자가 *어떤 측면을 적는지* 인식 도구가 없어짐
- AI 큐레이션 메모(ochre/navy)와 사용자 메모가 같은 시각 언어를 공유하던 것이 깨짐

대응 후보 셋 제시 — (1) 이해/암기 카드 각각에 펜 캔버스 / (2) 단일 펜 + 토글 / (3) v1 그대로 + 펜 옵션 — 결정은 보류. 다음 발견이 갈래를 바꿈.

## 2. 결정적 환기 — 사용자: "전에 만들었던 문제가 있다"

사용자가 https://mnvoice.github.io/ee-agent/?v=1 공유. 웹 fetch 시도했으나 SPA라 정적 텍스트만 회수. UI 라벨 분석으로 다음 추정:

- 5개 진입 탭: 📚전체 / 📖과목별 / 🔍태그별 / ✗오답노트 / ⚙️설정
- 한 문제씩 풀이가 기본 ("1 / 1" 표시)
- ✏️ 필기 모드 / 🚩 플래그 / 시험 제출 / 번호판 모달

ee-practice가 회차 단위만 갖고 있는 반면 mnvoice는 **선별 진입**(태그별, 오답노트)을 가짐. 학습은 "이 회차 100문제 차례로"가 아니라 "내 약점 + 자주 나오는 개념 + 오답"이라는 사용자의 학습 흐름 인식이 mnvoice에 박혀있음.

## 3. PDF 패널 제거 결정

사용자: *"전체 문제가 나올 필요가 없다. 개별 문제만 나오면 된다."*

해석 두 갈래 — (α) PDF 패널 자체가 불필요 / (β) 한 페이지에 여러 문제 섞임이 불필요. 사용자가 mnvoice 도구를 환기하면서 *"개별 이미지를 원한다"* 명시 — **(α) 확정**. 좌측 PDF 패널 통째로 제거 결정.

다만 *문항별 이미지*는 따로 필요 (회로도/그래프 있는 문항). ee-agent JSON엔 이미지 경로 없음(vision_solver 호출 후 폐기). 별건 작업 필요로 인지.

## 4. CLI 위임 — 이전 mnvoice 도구 분석

사용자가 *"전에 작업하던 것이 CLI에 있는 듯하다"* 환기. CLI에 위임하여 다음 보고 받음:

### 4.1 위치 + 형태
- `~/Developer/ee-agent/app/` — 백엔드와 같은 git repo이지만 디렉토리 분리
- **PWA 형식 vanilla HTML/JS** — React/Vite 아님. KaTeX는 CDN 직접 로드
- IndexedDB(`ee-study-db` v2)로 진척/오답/필기 저장
- main.js 65 KB

### 4.2 데이터
- `app/data/questions.json` — **16.6 MB, 5,307건** 누적
- 스키마 12 필드 + 2 선택:
  - 핵심: year, session, subject, q_no, text, choices, answer, solution
  - 메타: difficulty (1-5), q_type ("계산형"/"개념형" 등), tag (389개 고유), steps (인식/변환/...), quality
  - 선택: figure_svg, solution_svg
- stats.json — 집계 (43 KB)

### 4.3 이미지
- **외부 파일 X** — JSON 안에 figure_svg 문자열로 인라인 SVG 직접 임베드
- LLM 생성 SVG 추정 (viewBox + line/text 명시적 코드 — 트레이싱 아님)
- 평균 4 KB
- 보유율: 5,307건 중 341건 (6.4%) — figure_svg
- 보유율: 5,307건 중 691건 — solution_svg
- 2026 1회 100건 중 7건만 figure_svg 보유 (7%)

### 4.4 학습 메타 (4/27 mock과 비교)

| 항목 | mnvoice | ee-practice mock |
|---|---|---|
| subject | ✅ 5,307건 | mock 5건만 |
| q_type | ✅ | mock과 호환 |
| difficulty 1-5 정수 | ✅ | mock은 상/중/하 |
| tag (389개 고유) | ✅ — concept 역할 | mock의 concepts와 통합 가능 |
| solution 마크다운+KaTeX | ✅ | ai_solution(plain) |
| steps (인식/변환/...) | ✅ — 풀이 단계 분해 | **신규** |
| figure_svg | 6.4% | 없음 |
| freq | ❌ 직접 필드 X | **tag로 5,307건에서 자동 산출 가능** |
| related_questions | ❌ | **tag 매칭으로 자동 산출 가능** |
| 이해/암기 분리 | ❌ | ee-practice의 차별점 |

## 5. 통합 결정

### 5.1 핵심 통찰
- **mnvoice는 데이터를 빚었음** — 5,307건 + tag + difficulty + steps + figure_svg
- **ee-practice는 학습 도구 디자인을 빚었음** — 이해/암기 분리, 학습 네비게이션 UI, 펜 캔버스
- 둘이 *서로 결여한 부분*이라 결합이 자연스러움

### 5.2 갈래 비교

| 갈래 | 무엇 | 비용 | 채택 |
|---|---|---|---|
| (X) ee-practice가 mnvoice questions.json을 fetch + 진입 모드 흡수 | React 디자인 일관성 보존 | 중 (스키마 매핑 + 모드 추가) | **권고** |
| (Y) mnvoice 도구를 직접 개선 (펜+이해/암기 추가) | 65KB vanilla JS — 코드 친숙도 미지수 | 미지수 | 보류 |

(X) 채택. mnvoice는 *데이터 소스*로만 사용.

### 5.3 1단계 작업 패키지 (작성 완료, 실행 대기)

```text
[작업] ee-practice 데이터 교체 — mnvoice에서 mapping

소스: ~/Developer/ee-agent/app/data/questions.json (5,307건)
타깃: ~/Developer/ee-practice/public/data/questions.json

[1] 2026 1회만 추출 (100건)
[2] 스키마 매핑:
   q_no → question_number
   subject → subject_inferred
   text → stem
   choices(배열) → choices(객체 1~4)
   answer → correct_choice
   solution → ai_solution
   q_type → question_type
   difficulty(1-5) → difficulty(하/중/상: 1-2=하, 3=중, 4-5=상)
   tag → concepts: [{name: tag, subject, tier: "core"}]
   figure_svg → figure_svg (그대로)
   steps → steps (그대로)
[3] freq 자동 산출 — 5,307건 전수에서 같은 tag 카운트
[4] related_questions 자동 산출 — 2026 1회 내 동일 tag (최대 3)
[5] 보고: 변환 크기, figure_svg 7건 q_no, stem null 수, difficulty 분포

추가 작업 정지.
```

## 6. 1단계 후 다음 작업 (이번 세션엔 미실행)

- ee-practice UI에 figure_svg 인라인 표시 (`dangerouslySetInnerHTML`)
- ai_solution 마크다운 + KaTeX 렌더링 추가 (`react-markdown` + `rehype-katex`)
- 진입 모드 4개 추가:
  - 📚 회차 (현재 동작)
  - 📖 과목별 (subject 필터)
  - 🏷️ 태그별 (concepts/tag 필터)
  - ✗ 오답노트 (window.storage progress 필터)
- 펜 캔버스 보존 여부 — 사용자 결정 (v1 디자인 회귀 + 펜 옵션 토글이 가장 안전 후보)

## 7. 4/27 결정의 *재해석*

| 4/27 결정 | 4/28 재해석 |
|---|---|
| MVP-2 LLM 추출 (a/b/c/d 검토) | **불필요** — mnvoice가 이미 5,307건 메타 제공 |
| 펜 캔버스 추가 | **재고** — v1 디자인이 더 만족 |
| ee-agent law_used 49/100 한계 | **무관** — mnvoice solution 100% 보유 |
| 다회차 데이터 미해결 | **해결** — mnvoice가 이미 다년치 누적 |
| concept 자동 추출 별도 트랙 | **불필요** — tag 389개가 이미 있음 |

4/27 세션은 *재발명* 위에 있었음을 인지. 단 학습 도구 *디자인*(이해/암기, 학습 네비)은 mnvoice에 없으므로 살아남음.

## 8. 메타 관찰

### 8.1 verify-agent 원칙의 *데이터 측면 적용*
"주장은 증거가 아니다" — 4/27의 mock 5건은 *주장*이었고 mnvoice의 5,307건이 *증거*. mock 위에 도구를 빚는 동안 진짜 데이터는 따로 있었음. 사용자 환기로만 발견됨.

### 8.2 사용자 환기의 결정적 가치
사용자가 *"전에 만들었던 문제가 있다"* 환기 안 했으면 4/27 트랙 그대로 진행되어:
- (b)/(c)/(d) LLM 추출에 비용 들이고 (mnvoice가 이미 갖고 있는 것을)
- 5,307건이 아닌 100건 위에서 freq 산출 시도하다 의미 없음 발견하고
- figure_svg 없는 채로 PDF 페이지 PNG로 그림 처리하다 막힘

§1.5 자기 적용을 메모리/세션 문구로 처리 안 하더라도, *사용자 측 정보 부재*가 트랙을 빗나가게 할 수 있음. **시작 전 사용자가 이미 가진 자산 점검**이 작업 비용 결정 전에 와야 한다는 교훈.

### 8.3 도구의 두 측면
- *데이터*: 누가 만들든 결국 같은 곳을 향함 (5,307건 + 메타). 한 번 빚으면 재사용
- *학습 도구 디자인*: 사람마다 학습 방식 달라 빚는 사람의 흔적이 남음 (이해/암기 분리는 ee-practice 사용자의 학습 모델)

데이터는 통합, 디자인은 별개. 통합 방향이 그 구조를 따름.

## 9. 다음 세션 권고

다음 세션 첫 작업: **§5.3 1단계 패키지 CLI 실행**. 결과 보고 받고 ee-practice가 진짜 100건 + 이미지 7건 + freq + related로 동작하는 시점을 시작점으로 다음 결정.

## 10. 산출물 상태

- 코드: `/mnt/user-data/outputs/ee_practice_v1.jsx`, `ee_practice_v2.jsx`, `ee-practice/` (Vite 패키지)
- 사용자 PC: `~/Developer/ee-practice/` 셋업 완료, dev server 동작 중 (4/27 마무리)
- 미실행: §5.3 1단계 패키지 (이번 세션 작성, 다음 세션 실행)
- 미해결: 펜 보존 여부, 진입 모드 추가, KaTeX 렌더링 — 모두 1단계 후
