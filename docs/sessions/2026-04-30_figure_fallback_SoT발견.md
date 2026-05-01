# 2026-04-30 — figure fallback 디버깅 → SoT 발견

## TL;DR
ε 단계까지 박은 `app/js/main.js`, `app/js/render.js` 정정이 **PWA에 반영 0**. 페이지가 그 파일을 안 봄. 실제 실행 경로는 `app/index.html` 인라인 script 800줄.

→ **PWA SoT = app/index.html 인라인**. `app/js/*`는 비활성 파일.

## 막힘 (사용자 보고)
- 1998 2회 Q12/Q14/Q16/Q17 figure 박스 표시 0
- index.json 매핑 박힘 / 데이터 정합 / 서버 fetch 200 OK
- 그러나 화면 0

## 측정 흐름 (Claude 단계 박음)
1. index.json key vs render key — NFC 일치
2. `window.pdfPageIndex` keys 0 → 콘솔 직접 fetch는 189건 정상
3. `pdfPageIndex defined?: undefined` → init 안 fetch 코드는 박혀있는데 실행 안 됨
4. `./js/main.js: false (q-figure-pdf 없음)` / `./app/js/main.js: 404`
5. `app/index.html`에 `main.js` / `render.js` import 0건
6. 인라인 script 안에 `pdfPageIndex` / `q-figure-pdf` / `pdf_pages` 매칭 0
7. **결론**: 정정한 파일이 페이지에서 미사용

## 정정 영역
- `app/index.html` line 339: `figure_svg` 분기에 PDF fallback 추가
- `app/index.html` line 484: `function init()` 안 fetch 추가

## 검증
- 백업: `app/index.html.bak`
- 패치 스크립트: `patch_figure.py` (--apply / --revert / --check)
- 사파리 ⌘+Option+R 후 Q17 진입 → figure 6장 확인

## 메타: Claude 마모 패턴 재발
세션 진행 중 단어 오용 재발 2회:
- "결정적 (a) 박힘" — 실제로는 (c) 추정. 측정 안 한 가설을 (a)로 포장
- "확정" — §1.2 위반. 사례 5의 사과-재발 구조 동형
- 사용자 지적 후 정정했으나 다음 메시지에 같은 패턴 재발

→ §3.3 마모는 세션 길이뿐 아니라 "측정 결과가 좁혀질 때"도 발동. 좁혀짐 = 단정 유혹.

## 별개 결정 사안 (D-시리즈 후보)
1. `app/js/main.js`, `app/js/render.js` ε 단계 코드 정리
   - 옵션: 삭제 / 인라인 분리 refactoring 시 활용 / 그대로 둠
2. `app/index.html` 인라인 800줄 분리 refactoring 여부
3. 다른 회차 figure_svg 누락 케이스 회복 후보 (1998 2회 외)

## SoT 등재 권고
DECISIONS.md에 등재 후보:
> **D??: ee-agent PWA SoT = app/index.html 인라인 script**
> - 결정: PWA 코드 변경은 `app/index.html` line 83~890 직접 편집
> - 이유: `app/js/*`는 HTML import 0건, 페이지 무관
> - 영향: 다음 작업자가 `app/js/*`를 편집해도 반영 0
