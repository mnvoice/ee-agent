#!/usr/bin/env python3
"""convert_pdf_pages_to_png.py

회복 후보 (text 기준 그림/회로/도면 키워드 + figure_svg 없음) 회차의 PDF를
페이지 단위 PNG로 변환.

작성만 — 사용자 별도 승인 후 실행.
실행 시에도 data/* 외에는 미수정. data/pdf_pages/ 디렉토리만 신규 생성.

Usage:
    python scripts/convert_pdf_pages_to_png.py dryrun   # 변환 계획만 출력
    python scripts/convert_pdf_pages_to_png.py run      # 실제 변환 실행
"""

import argparse
import json
import logging
import re
import sys
import unicodedata
from pathlib import Path
from collections import Counter

try:
    import fitz  # PyMuPDF
except ImportError:
    print("PyMuPDF not installed. Run: pip install pymupdf", file=sys.stderr)
    sys.exit(1)

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
QUESTIONS = PROJECT_ROOT / "app" / "data" / "questions.json"
OUTPUT_DIR = DATA_DIR / "pdf_pages"
INDEX_FILE = OUTPUT_DIR / "index.json"

DPI = 150  # 1MB/장 추정. figure-demo 1~2MB보다 작게.

# 결정 2: text 기준 좁은 패턴 (210건)
GRIM_RE = re.compile(r'그림(과 같은|에서|을|의)|회로(에서|와 같은|의)|도면')


def normalize_session(s):
    s = str(s).strip()
    if s.endswith('회회'):
        s = s[:-1]
    return s


def load_targets():
    """통합본에서 변환 대상 추출 (text 기준 210건)."""
    with open(QUESTIONS) as f:
        qs = json.load(f)
    targets = []
    for q in qs:
        text = str(q.get('text', ''))
        if GRIM_RE.search(text) and not q.get('figure_svg'):
            targets.append({
                'year': q.get('year'),
                'session': normalize_session(q.get('session', '')),
                'q_no': q.get('q_no'),
                'subject': q.get('subject'),
            })
    return targets


def find_pdf_for_round(year, session_norm, pdf_files):
    """년도+회차 → PDF 파일 매칭. NFC 정규화 + year 위치 정확화 + 콤마 r_num.

    year 정확화: year가 회차 정보 위치에 있을 때만 매칭 (날짜 prefix '20260316'의 '2026' 충돌 차단).
    콤마 r_num: '1,2회' 같은 합쳐진 회차 매칭.
    """
    # 콤마 보존 (1,2회 → r_num='1,2')
    r_num = re.sub(r'[^0-9_,]', '', session_norm)
    if not r_num:
        return None
    target = unicodedata.normalize('NFC', f'_{r_num}회')
    target_alt = unicodedata.normalize('NFC', f' {r_num}회')
    for pdf in pdf_files:
        pdf_nfc = unicodedata.normalize('NFC', pdf)
        # year 위치 정확화: _YYYY_ / 시작 YYYY / 문제YYYY_ 패턴만
        year_match = (
            f'_{year}_' in pdf_nfc
            or pdf_nfc.startswith(f'{year}')
            or pdf_nfc.startswith(f'문제{year}_')
        )
        if not year_match:
            continue
        if target in pdf_nfc or target_alt in pdf_nfc:
            return pdf
    return None


def plan_conversions():
    """변환 계획 수립 — 회차별 PDF 매핑."""
    targets = load_targets()
    pdf_files = sorted([f.name for f in DATA_DIR.glob("*.pdf")])

    round_dist = Counter(
        (t['year'], t['session']) for t in targets
    )

    plan = []
    for (year, sess), count in sorted(round_dist.items(),
                                       key=lambda x: (x[0][0] or 0, x[0][1])):
        pdf = find_pdf_for_round(year, sess, pdf_files)
        plan.append({
            'year': year,
            'session': sess,
            'count': count,
            'pdf': pdf,
            'output_dir': f'pdf_pages/{year}_{sess}',
        })
    return targets, plan


def dry_run():
    """변환 계획만 출력. 파일 생성 0."""
    targets, plan = plan_conversions()
    matched = [p for p in plan if p['pdf']]
    unmatched = [p for p in plan if not p['pdf']]

    print(f'\n=== 변환 계획 (dryrun, 파일 생성 0) ===')
    print(f'대상 문제: {len(targets)}건')
    print(f'대상 회차: {len(plan)}개')
    print(f'PDF 매칭: {len(matched)} / 미매칭: {len(unmatched)}')
    print()

    print('매칭 회차 (변환 예정):')
    for p in matched[:10]:
        print(f"  {p['year']}년 {p['session']} ({p['count']}건) "
              f"→ {p['pdf']} → {p['output_dir']}/")
    if len(matched) > 10:
        print(f'  ... + {len(matched) - 10}개')

    if unmatched:
        print('\n미매칭 회차 (수동 확인 필요):')
        for p in unmatched:
            print(f"  {p['year']}년 {p['session']} ({p['count']}건)")

    print(f'\n출력 디렉토리: {OUTPUT_DIR.relative_to(PROJECT_ROOT)}/')
    print(f'인덱스 파일: {INDEX_FILE.relative_to(PROJECT_ROOT)}')
    print(f'DPI: {DPI} (1장당 ~1MB 추정)')


def run_conversion():
    """실제 변환 — data/pdf_pages/ 신규 생성."""
    targets, plan = plan_conversions()
    matched = [p for p in plan if p['pdf']]

    if not matched:
        log.error("매칭된 회차 없음. dryrun으로 확인하세요.")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)
    index = {}  # {f"{year}_{session}_{q_no}": "pdf_pages/.../page_N.png"}

    for p in matched:
        year, sess, pdf_name = p['year'], p['session'], p['pdf']
        pdf_path = DATA_DIR / pdf_name
        out_dir = OUTPUT_DIR / f"{year}_{sess}"
        out_dir.mkdir(exist_ok=True)

        # skip: 이미 변환된 회차 (재실행 시 중복 변환 회피)
        existing_pngs = sorted(out_dir.glob('page_*.png'),
                                key=lambda p: int(re.search(r'page_(\d+)', p.name).group(1)))
        if existing_pngs:
            log.info(f"  skip {pdf_name} → {out_dir.name}/ ({len(existing_pngs)} pages already converted)")
            page_paths = [f"pdf_pages/{year}_{sess}/{p.name}" for p in existing_pngs]
        else:
            try:
                doc = fitz.open(pdf_path)
            except Exception as e:
                log.error(f"  fail open {pdf_name}: {e}")
                continue

            log.info(f"  converting {pdf_name} → {out_dir.name}/ ({len(doc)} pages)")
            page_paths = []
            for i, page in enumerate(doc):
                pix = page.get_pixmap(dpi=DPI)
                out_png = out_dir / f"page_{i+1}.png"
                pix.save(str(out_png))
                page_paths.append(f"pdf_pages/{year}_{sess}/page_{i+1}.png")
            doc.close()

        # 회차 안 모든 q_no를 페이지 통째로 매핑 (결정 1: A — 좌표 매핑 0)
        # 어느 페이지가 그 q_no인지 미박힘 → 전체 페이지 list로 매핑
        for t in targets:
            if t['year'] == year and t['session'] == sess:
                key = f"{year}_{sess}_{t['q_no']}"
                index[key] = page_paths  # 페이지 목록 통째 (사용자가 PWA에서 선택)

    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    log.info(f"\n변환 완료: {len(matched)} 회차 → {OUTPUT_DIR}/")
    log.info(f"인덱스: {INDEX_FILE} ({len(index)} 엔트리)")


def main():
    p = argparse.ArgumentParser()
    p.add_argument('cmd', choices=['dryrun', 'run'])
    args = p.parse_args()
    if args.cmd == 'dryrun':
        dry_run()
    elif args.cmd == 'run':
        run_conversion()


if __name__ == '__main__':
    main()
