# Study Mode (필기학습) 개선 계획

## 목표
iPad + Apple Pencil 사용자를 위한 필기 학습 전용 화면 추가

## 사용자 문제 4가지
1. 문제 보면서 필기할 공간 부족
2. 필기 내용이 문제별 저장 안 됨
3. 풀이 후 정답/해설 비교 불편
4. 회로도 자유 캔버스 필요

## 수정 원칙
- 기존 코드(index.html, main.js 등) 수정 금지
- 새 파일만 추가: study.html, js/study.js, css/study.css
- index.html에 링크 1개만 추가 (최소 수정)

## 안전망
- Tag: v1.0-stable (commit 01e54f0)
- Branch: backup-stable
- Restore: git checkout backup-stable

## 단계
1. [x] git tag + branch 생성
2. [ ] 기능 체크리스트 작성
3. [ ] study.html 개발 (새 브랜치)
4. [ ] 자동 테스트 추가
