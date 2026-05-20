---
title: index.json 추적 정책과 재현성 위험
date: 2026-05-20
cycle: T3.5 / G5 / H1
branch: feat/phase-b-migration
type: supervisor-reasoning-log
tags:
  - 전기기사/supervisor-log
  - 전기기사/판단근거
  - ee-agent/재현성
related:
  - docs/audit/supervisor_logs/2026-05-20_t3_5_g5_h1_supervisor_reasoning_log.md
  - docs/audit/decision_records/t3_5_g5_h1_decisions.jsonl
---

# index.json 추적 정책과 재현성 위험

> hold 3건 crop 연결을 C안으로 확정하면서 드러난 `data/pdf_pages/index.json` 미추적
> 문제를 기록한다. 결정(DR-T35-12)의 후속 — 위험의 실체와 단기·중기·장기 정책 방향이다.
> 문장은 평어체로 적는다. 그쪽이 읽기 쉽다.

---

## 현재 상태

지금 로컬에서는 그림이 뜬다. 그러나 다른 환경에서 clone하면 사정이 다르다.

- `data/pdf_pages/index.json`이 없다 (미추적).
- PDF 페이지 이미지도 없다 (대부분 미추적).
- 그래서 기존 원문 그림 렌더 일부가 안 뜰 가능성이 있다.

즉 "내 로컬에서 보인다"는 것이 "어디서나 보인다"를 뜻하지 않는다.

## 파급 효과

### 1. 재현성 문제

내 로컬에서는 보이는데 다른 사람·CI·배포 환경에서는 안 보일 수 있다.
이번 hold 3건은 C안으로 해결했다 — crop PNG를 추적(`bd99bc8`)하고 `app/index.html`
상수로 직접 fallback하므로 git만으로 자족한다. 그러나 기존 `pdfPageIndex` 기반
그림 문항들은 여전히 위험하다. 그것들은 미추적 `index.json` + 미추적 페이지 이미지에
의존한다.

### 2. 배포 누락 가능성

앱은 `fetch('data/pdf_pages/index.json')`을 시도한다. 파일이 배포에 없으면 fetch가
실패한다. 코드가 실패를 잘 무시하면 그림만 안 나오고 넘어간다. 그러나 엄밀히는
asset packaging 문제다 — 배포 산출물에 무엇이 포함되어야 하는지가 정의되어 있지 않다.

### 3. 감사·검증 결과의 지역성

clean Chrome 검증이 "현재 로컬 workspace" 기준이라면, 미추적 파일 덕분에 통과한
항목이 있을 수 있다. 즉 검증이 로컬 상태에 의존한다.
다만 이번 G5 74건은 answer-locked 해설 렌더가 중심이고, hold 3건은 C안으로 추적된
PNG를 직접 fallback한다. 그래서 이번 cycle의 직접 피해는 제한적이다. 위험은 "검증
방법론"에 남는 것이지 "이번 결과"가 틀렸다는 뜻은 아니다.

### 4. 미래 작업에서 혼선

누가 `index.json`을 source로 봐야 하는지, runtime/generated로 봐야 하는지 애매하다.
이 애매함 때문에 "수정했는데 commit할까 말까"가 계속 반복된다. 실제로 이번 cycle에서
그 망설임이 한 번 발생했고, 매번 감독자 판단을 요구하게 만든다.

## 의사결정 요약

- **상황**: `data/pdf_pages/index.json`은 앱이 fetch해 `pdfPageIndex`로 쓰는
  source-like manifest다. 그러나 repo에서 미추적이고, 참조하는 `page_N.png`
  이미지도 대부분 미추적이다.
- **판단**: 이번 hold crop cycle에서는 `index.json`을 통째로 commit하지 않는다.
  hold 3건은 추적된 `figure_crops` PNG와 `app/index.html`의 `FIGURE_CROP_HOLD`
  상수 fallback으로 재현성을 확보한다. 전체 `pdfPageIndex` asset 정책은 별도
  트랙으로 분리한다.
- **근거**: `index.json`만 commit해도 참조 page 이미지가 미추적이라 재현성이
  완성되지 않는다. 게다가 133KB·193키 중 190키가 hold 트랙과 무관해 범위가
  과도하다. hold 3건 crop PNG는 이미 `bd99bc8`로 추적되어, app 상수 fallback이
  가장 작고 재현성이 높다.
- **검토한 대안**:
  - A: `index.json`을 통째로 신규 추적한다 (+ `app/index.html`).
  - B: hold 전용 소형 manifest를 신설하고 app에서 merge한다.
  - C: `app/index.html`에 crop 경로를 상수로 두어 fallback한다. — **채택**
- **기각한 대안과 이유**:
  - A 기각: 무관한 190키를 대량 commit하면서도, 참조 page 이미지가 미추적이라
    재현성을 실제로 해결하지 못한다.
  - B 기각: 새 manifest 파일과 fetch/merge 로직이 늘어 C보다 변경 범위가 크다.
- **다음 행동**: 아래 "정책 방향"의 단기·중기·장기 항목을 따른다.

## 정책 방향

### 단기

- `index.json`은 계속 untracked / runtime artifact로 취급한다.
- 이번 hold 3건처럼, 필요한 자산만 tracked fallback 또는 소형 manifest로 관리한다.

### 중기

- `data/pdf_pages/index.json`의 생성 스크립트와 산출 정책을 문서화한다.
- 어떤 이미지를 repo에 포함할지, 어떤 것을 배포 artifact로 둘지 결정한다.

### 장기

- `pdfPageIndex` 자산을 build artifact로 분리하거나,
- tracked manifest + tracked crops만 쓰는 구조로 재설계한다.

---

*이 문서는 "지금 동작한다"와 "어디서나 동작한다"의 간극을 기록한다.
hold 3건은 C안으로 그 간극을 닫았다. 나머지 그림 문항은 아직 열려 있다.*
