#!/usr/bin/env python3
"""verify_data_pdf_mapping.py

read-only. 통합본 (app/data/questions.json) ↔ Mathpix OCR (PDF text 추출) 매핑 정합성 검증.

분류:
  CONSISTENT: 통합본 text 핵심 토큰 80%+ → mathpix에서 발견
  PARTIAL:    40~80% 매칭 (OCR 손상 또는 부분 누락)
  MISMATCH:   40% 미만 (다른 문제로 매핑됐을 가능성)
  MISSING:    해당 회차 mathpix 자산 부재
  EMPTY:      통합본 text 자체가 너무 짧음 (분류 불가)

샘플링:
  TIER_2: figure_svg 보유 (대조군) — 30건
  TIER_3: 회복 후보 (figure 키워드+SVG 없음) — 30건
  TIER_4: figure 불필요 추정 (대조군) — 30건
  FORCED: 첨부 케이스 2건 (2000-2-3, 2011-3-41) 강제 포함

출력: output/data_pdf_mismatch_20260430.json
변경 0: data/* 미수정.
"""

import json
import re
import random
import sys
from pathlib import Path
from collections import Counter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)
QUESTIONS = PROJECT_ROOT / "app" / "data" / "questions.json"

MATHPIX_FILE_RE = re.compile(r'mathpix_기출_(\d{4})_(.+?)\.json$')
GRIM_RE = re.compile(r'그림(과 같은|에서|을|에|이|의|에서는)|회로(에서|와 같은|이|의)|도면|아래 그림')


def normalize_session(s):
    """통합본 session 표기 정규화 (1회회→1회, 1,2회회→1_2회 등)."""
    s = str(s).strip()
    if s.endswith('회회'):
        s = s[:-1]
    s = s.replace(',', '_')
    return s


def load_mathpix_corpus():
    """{(year, session_normalized): full_concatenated_text}"""
    corpus = {}
    for f in DATA_DIR.glob("mathpix_기출_*.json"):
        m = MATHPIX_FILE_RE.match(f.name)
        if not m:
            continue
        year = int(m.group(1))
        sess = m.group(2)
        try:
            with open(f) as fh:
                pages = json.load(fh)
            full = "\n".join(p.get('text', '') for p in pages if isinstance(p, dict))
            corpus[(year, sess)] = full
        except Exception as e:
            print(f"  mathpix load fail {f.name}: {e}", file=sys.stderr)
    return corpus


def find_mathpix_text(corpus, year, session_raw):
    """다양한 session 표기 시도."""
    sess_norm = normalize_session(session_raw)
    candidates = [
        (year, sess_norm),
        (year, sess_norm.replace('_', ',') + '회'),
    ]
    if sess_norm in ('1회', '2회'):
        candidates.append((year, '1_2회'))  # 합쳐진 파일 fallback
    for k in candidates:
        if k in corpus:
            return corpus[k], f"{k[0]}_{k[1]}"
    return None, None


def normalize_for_match(s):
    """LaTeX/공백/특수문자 제거하여 매칭용 정규화."""
    s = re.sub(r'\\[a-zA-Z]+\b', ' ', s)
    s = re.sub(r'\\[\(\)\[\]]', ' ', s)
    s = re.sub(r'[{}\\]', ' ', s)
    s = re.sub(r'\s+', ' ', s)
    return s.strip()


def classify_match(needle, haystack):
    """needle의 핵심 토큰이 haystack에 얼마나 있나."""
    n = normalize_for_match(needle)
    h = normalize_for_match(haystack)

    if len(n) < 15:
        return ('EMPTY', 0.0)

    # 직접 substring (강력한 정합)
    if len(n) >= 30 and n[:30] in h:
        return ('CONSISTENT', 1.0)
    if len(n) >= 20 and n[:20] in h:
        return ('CONSISTENT', 0.95)

    # 한국어/숫자 토큰 (3자 이상) 추출
    tokens = [t for t in re.findall(r'[가-힣]{3,}|\d{2,}', n) if len(t) >= 2][:15]
    if not tokens:
        # 영문/특수 위주 — 단순 ngram 비교
        return ('EMPTY', 0.0)

    hits = sum(1 for t in tokens if t in h)
    ratio = hits / len(tokens)
    if ratio >= 0.8:
        return ('CONSISTENT', ratio)
    if ratio >= 0.4:
        return ('PARTIAL', ratio)
    return ('MISMATCH', ratio)


def verify_one(q, corpus):
    year = q.get('year')
    sess = q.get('session', '')
    hay, key = find_mathpix_text(corpus, year, sess)
    if hay is None:
        return ('MISSING', 0.0, None)
    needle = str(q.get('text', ''))
    cat, score = classify_match(needle, hay)
    return (cat, score, key)


def main():
    with open(QUESTIONS) as f:
        all_qs = json.load(f)
    print(f"통합본 로드: {len(all_qs)}건", file=sys.stderr)

    corpus = load_mathpix_corpus()
    print(f"Mathpix corpus: {len(corpus)}회차", file=sys.stderr)

    # 분류
    def tier_of(q):
        text = str(q.get('text', '')) + ' ' + str(q.get('solution', ''))
        has_kw = bool(GRIM_RE.search(text))
        has_svg = bool(q.get('figure_svg'))
        if has_kw and has_svg:
            return 'TIER_2'
        if has_kw and not has_svg:
            return 'TIER_3'
        return 'TIER_4'

    grouped = {'TIER_2': [], 'TIER_3': [], 'TIER_4': []}
    for q in all_qs:
        grouped[tier_of(q)].append(q)
    print(f"  TIER_2 (대조: figure_svg 있음): {len(grouped['TIER_2'])}",
          file=sys.stderr)
    print(f"  TIER_3 (회복 후보): {len(grouped['TIER_3'])}", file=sys.stderr)
    print(f"  TIER_4 (figure 불필요 추정): {len(grouped['TIER_4'])}",
          file=sys.stderr)

    rng = random.Random(42)
    samples = {
        t: rng.sample(qs, min(30, len(qs))) for t, qs in grouped.items()
    }

    # FORCED
    forced = []
    for q in all_qs:
        y = str(q.get('year', ''))
        s = normalize_session(q.get('session', ''))
        n = q.get('q_no')
        if y == '2000' and s.startswith('2') and n == 3:
            forced.append(('FORCED_2000_2_3', q))
        if y == '2011' and s.startswith('3') and n == 41:
            forced.append(('FORCED_2011_3_41', q))

    results = {'TIER_2': [], 'TIER_3': [], 'TIER_4': [], 'FORCED': []}

    for tier, qs in samples.items():
        for q in qs:
            cat, score, key = verify_one(q, corpus)
            results[tier].append({
                'year': q.get('year'),
                'session': q.get('session'),
                'q_no': q.get('q_no'),
                'subject': q.get('subject'),
                'category': cat,
                'score': round(score, 2),
                'mathpix_key': key,
                'text_head': str(q.get('text', ''))[:80],
            })

    for label, q in forced:
        cat, score, key = verify_one(q, corpus)
        results['FORCED'].append({
            'label': label,
            'year': q.get('year'),
            'session': q.get('session'),
            'q_no': q.get('q_no'),
            'subject': q.get('subject'),
            'category': cat,
            'score': round(score, 2),
            'mathpix_key': key,
            'text_head': str(q.get('text', ''))[:200],
            'has_figure_svg': bool(q.get('figure_svg')),
            'has_solution_svg': bool(q.get('solution_svg')),
        })

    # 보고
    print('\n=== 분류 결과 (각 30건) ===')
    summary = {}
    for tier in ['TIER_2', 'TIER_3', 'TIER_4']:
        cnts = Counter(r['category'] for r in results[tier])
        summary[tier] = dict(cnts)
        n = len(results[tier])
        print(f'\n{tier}: {n}건')
        for cat in ['CONSISTENT', 'PARTIAL', 'MISMATCH', 'MISSING', 'EMPTY']:
            v = cnts.get(cat, 0)
            pct = (100 * v / n) if n else 0
            print(f'  {cat:12s}: {v:3d} ({pct:5.1f}%)')

    print('\n=== FORCED (첨부 케이스) ===')
    for r in results['FORCED']:
        print(f"\n{r['label']}")
        print(f"  {r['year']}-{r['session']}-{r['q_no']} ({r['subject']})")
        print(f"  category: {r['category']} | score: {r['score']} "
              f"| mathpix: {r['mathpix_key']}")
        print(f"  has_figure_svg: {r['has_figure_svg']} | "
              f"has_solution_svg: {r['has_solution_svg']}")
        print(f"  text head: {r['text_head']}")

    # 산수 검증
    total_in = sum(len(s) for s in samples.values()) + len(forced)
    total_out = sum(len(r) for r in results.values())
    print(f'\n=== 산수 검증 ===')
    print(f'입력: {sum(len(s) for s in samples.values())} samples '
          f'+ {len(forced)} forced = {total_in}')
    print(f'출력: {total_out}')
    print(f'일치: {total_in == total_out}')

    # 저장
    out_file = OUTPUT_DIR / 'data_pdf_mismatch_20260430.json'
    with open(out_file, 'w') as f:
        json.dump({
            'mathpix_corpus_size': len(corpus),
            'mathpix_keys': sorted(f"{k[0]}_{k[1]}" for k in corpus.keys()),
            'tier_sizes': {t: len(qs) for t, qs in grouped.items()},
            'sample_sizes': {t: len(s) for t, s in samples.items()},
            'forced_count': len(forced),
            'summary': summary,
            'results': results,
        }, f, ensure_ascii=False, indent=2)
    print(f'\n결과 저장: {out_file.relative_to(PROJECT_ROOT)}')


if __name__ == '__main__':
    main()
