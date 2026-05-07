#!/usr/bin/env python3
"""verify_questions_quality.py — questions.v2.json 통합 품질 검증.

Layer: L1.5 (parsing OK 후 quality 검증, dispatch 단계 입력)
read-only / exit 0 (catch 발견해도 0) / Pydantic SPEC import (defensive)

흡수 매핑:
  INV-2 needs_ocr        → check_distribution.quality
  INV-3 파싱 성공률       → validate_pydantic
  INV-4 OCR placeholder  → check_content_empty.placeholder_count
  INV-5 선택지 ≥5자       → check_choices (단계별: strict / warn / numeric_unit)
  INV-6 6과목 누락        → check_subject_distribution
  INV-8 Q0 부재          → check_answer_range
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

# Pydantic SPEC import (defensive)
PYDANTIC_AVAILABLE = False
PYDANTIC_ERR: str | None = None
try:
    _repo_root = Path(__file__).resolve().parent.parent
    sys.path.insert(0, str(_repo_root / ".moai" / "specs" / "SPEC-EE-SCHEMA-001"))
    from question import Question  # type: ignore
    PYDANTIC_AVAILABLE = True
except Exception as _e:
    PYDANTIC_ERR = f"{type(_e).__name__}: {_e}"

# 임계값 (INV-5 통합본 정합)
CHOICE_LEN_STRICT = 1   # ≤1자 = STRICT FAIL
CHOICE_LEN_WARN = 4     # 2~4자 = 추가 검증 (숫자·단위면 정상)
ANSWER_VALID = {1, 2, 3, 4}
ANSWER_SENTINEL = {0}
EXPECTED_SUBJECTS = {'전기자기학', '전력공학', '전기기기', '회로이론', '제어공학', '전기설비기술기준'}
NUMERIC_UNIT_RE = re.compile(r'^[\d.\-+/×x*]+\s*[A-Za-zΩμ가-힣%°]*\s*$')
PLACEHOLDER_RE = re.compile(r'(needs_ocr|<\s*ocr|TODO|placeholder|fill_me|XXX)', re.IGNORECASE)


def _id(it: dict) -> tuple:
    return (it.get('year'), it.get('session'), it.get('subject'), it.get('q_no'))


def validate_pydantic(items: list) -> list | None:
    if not PYDANTIC_AVAILABLE:
        return None
    fails = []
    for i, it in enumerate(items):
        try:
            Question(**it)
        except Exception as e:
            fails.append({'idx': i, 'id': _id(it), 'error': str(e)[:200]})
    return fails


def check_q_no(items: list) -> dict:
    none_entries = [it for it in items if it.get('q_no') is None]
    return {
        'total': len(items),
        'q_no_none_count': len(none_entries),
        'samples': [_id(it) for it in none_entries[:5]],
    }


def check_answer_range(items: list) -> dict:
    dist = Counter(it.get('answer') for it in items)
    sentinel = [it for it in items if it.get('answer') in ANSWER_SENTINEL]
    out_of_range = [it for it in items
                    if it.get('answer') not in (ANSWER_VALID | ANSWER_SENTINEL | {None})]
    return {
        'distribution': dict(dist),
        'sentinel_count': len(sentinel),
        'sentinel_samples': [_id(it) for it in sentinel[:5]],
        'out_of_range_count': len(out_of_range),
        'out_of_range_samples': [{'id': _id(it), 'answer': it.get('answer')}
                                 for it in out_of_range[:5]],
    }


def check_id_duplicate(items: list, per_round: bool = False) -> dict:
    if per_round:
        ids = Counter(_id(it) for it in items if it.get('q_no') is not None)
    else:
        ids = Counter(_id(it) for it in items)
    dups = [(k, v) for k, v in ids.items() if v > 1]
    return {
        'mode': 'per_round' if per_round else 'full_triplet',
        'unique_ids': len(ids),
        'duplicate_groups': len(dups),
        'duplicate_total_entries': sum(v for _, v in dups),
        'samples': [{'id': k, 'count': v} for k, v in dups[:10]],
    }


def check_content_empty(items: list) -> dict:
    out = {}
    for f in ['text', 'solution', 'steps']:
        empty, placeholder = [], []
        for it in items:
            v = it.get(f)
            is_empty = (v is None
                        or (isinstance(v, str) and v.strip() == '')
                        or (isinstance(v, (list, dict)) and len(v) == 0))
            if is_empty:
                if len(empty) < 5:
                    empty.append({'id': _id(it), 'value_type': type(v).__name__})
                else:
                    empty.append(None)  # count only
            elif isinstance(v, str) and PLACEHOLDER_RE.search(v):
                if len(placeholder) < 5:
                    placeholder.append({'id': _id(it), 'value': v[:60]})
                else:
                    placeholder.append(None)
        out[f] = {
            'empty_count': len(empty),
            'empty_samples': [e for e in empty if e][:5],
            'placeholder_count': len(placeholder),
            'placeholder_samples': [p for p in placeholder if p][:5],
        }
    return out


def check_choices(items: list) -> dict:
    counts = Counter()
    strict_fail, warn_short = [], []
    numeric_unit = 0
    for it in items:
        ch = it.get('choices')
        if not isinstance(ch, list):
            counts['none_or_invalid'] += 1
            continue
        counts[len(ch)] += 1
        for c_idx, c in enumerate(ch):
            if not isinstance(c, str):
                continue
            length = len(c.strip())
            if length <= CHOICE_LEN_STRICT:
                if len(strict_fail) < 10:
                    strict_fail.append({'id': _id(it), 'choice_idx': c_idx,
                                        'value': c[:30], 'len': length})
            elif length <= CHOICE_LEN_WARN:
                if NUMERIC_UNIT_RE.match(c.strip()):
                    numeric_unit += 1
                else:
                    if len(warn_short) < 10:
                        warn_short.append({'id': _id(it), 'choice_idx': c_idx,
                                           'value': c[:30], 'len': length})
    return {
        'choice_count_distribution': dict(counts),
        'strict_fail_count': len(strict_fail),
        'strict_fail_samples': strict_fail,
        'warn_short_non_numeric_count': len(warn_short),
        'warn_short_samples': warn_short,
        'numeric_unit_short_count': numeric_unit,
    }


def check_subject_distribution(items: list) -> dict:
    dist = Counter(it.get('subject') for it in items)
    extra = {k: v for k, v in dist.items() if k not in EXPECTED_SUBJECTS and k is not None}
    missing = sorted(EXPECTED_SUBJECTS - set(dist.keys()))
    return {'distribution': dict(dist), 'expected_missing': missing, 'extra_subjects': extra}


def check_assets(items: list, root: Path) -> dict:
    out = {}
    for af in ['figure_svg', 'solution_svg']:
        type_dist = Counter()
        raster_missing, vector_missing = [], []
        non_dict = 0
        for it in items:
            v = it.get(af)
            if v is None:
                continue
            if not isinstance(v, dict):
                non_dict += 1
                continue
            t = v.get('type')
            type_dist[t] += 1
            if t == 'raster':
                p = v.get('image_path')
                if not p:
                    if len(raster_missing) < 10:
                        raster_missing.append({'id': _id(it), 'reason': 'image_path missing'})
                else:
                    full = Path(p) if Path(p).is_absolute() else (root / p)
                    if not full.is_file() and len(raster_missing) < 10:
                        raster_missing.append({'id': _id(it), 'path': str(p),
                                               'reason': 'file not found'})
            elif t == 'vector_svg':
                if not v.get('svg_content') and len(vector_missing) < 10:
                    vector_missing.append({'id': _id(it)})
        out[af] = {
            'type_distribution': dict(type_dist),
            'non_dict_count': non_dict,
            'raster_missing': raster_missing,
            'vector_missing_content': vector_missing,
        }
    return out


def check_distribution(items: list) -> dict:
    return {
        'year': dict(Counter(it.get('year') for it in items)),
        'subject': dict(Counter(it.get('subject') for it in items)),
        'q_type': dict(Counter(it.get('q_type') for it in items)),
        'difficulty_value_types': dict(Counter(type(it.get('difficulty')).__name__ for it in items)),
        'quality': dict(Counter(it.get('quality') for it in items)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='questions.v2.json 통합 품질 검증')
    parser.add_argument('json_path', help='questions.v2.json 경로')
    parser.add_argument('--output', '-o', default=None, help='JSON report 출력 경로')
    parser.add_argument('--per-round', action='store_true',
                        help='회차당 q_no 단일 검증 (INV-7 단일 회차 모드)')
    parser.add_argument('--asset-root', default=None,
                        help='asset 파일 cross-check root (default: json 파일 디렉토리)')
    args = parser.parse_args()

    json_path = Path(args.json_path).resolve()
    if not json_path.is_file():
        print(f"ERROR: {json_path} not found", file=sys.stderr)
        return 2

    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    items = data.get('questions', data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        print(f"ERROR: items not a list (type={type(items).__name__})", file=sys.stderr)
        return 2

    asset_root = Path(args.asset_root).resolve() if args.asset_root else json_path.parent

    report = {
        'meta': {
            'json_path': str(json_path),
            'total_entries': len(items),
            'pydantic_available': PYDANTIC_AVAILABLE,
            'pydantic_error': PYDANTIC_ERR,
            'per_round_mode': args.per_round,
            'asset_root': str(asset_root),
            'generated_at': datetime.now(timezone.utc).isoformat(),
        },
        'pydantic_fails': validate_pydantic(items),
        'q_no': check_q_no(items),
        'answer_range': check_answer_range(items),
        'id_duplicate': check_id_duplicate(items, per_round=args.per_round),
        'content_empty': check_content_empty(items),
        'choices': check_choices(items),
        'subject_distribution': check_subject_distribution(items),
        'assets': check_assets(items, asset_root),
        'distribution': check_distribution(items),
    }

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        output_path = json_path.parent.parent / 'reports' / f'quality_{ts}.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)

    # stdout summary
    m = report['meta']
    print(f"=== quality report → {output_path} ===")
    print(f"total: {m['total_entries']} | Pydantic: "
          f"{'OK' if m['pydantic_available'] else 'FALLBACK ('+ str(m['pydantic_error'])[:80]+')'}")
    pf = report['pydantic_fails']
    if pf is not None:
        print(f"Pydantic fails: {len(pf)}/{m['total_entries']}")
        for s in pf[:3]:
            print(f"  - {s['id']}: {s['error'][:120]}")
    print(f"q_no=None: {report['q_no']['q_no_none_count']}")
    ar = report['answer_range']
    print(f"answer dist: {ar['distribution']}")
    print(f"  sentinel(0): {ar['sentinel_count']}, out_of_range: {ar['out_of_range_count']}")
    idd = report['id_duplicate']
    print(f"id_duplicate ({idd['mode']}): unique={idd['unique_ids']}, "
          f"dup_groups={idd['duplicate_groups']}, dup_entries={idd['duplicate_total_entries']}")
    for fld, v in report['content_empty'].items():
        print(f"  content_empty {fld}: empty={v['empty_count']}, placeholder={v['placeholder_count']}")
    ch = report['choices']
    print(f"choices counts: {ch['choice_count_distribution']}")
    print(f"  strict_fail(≤{CHOICE_LEN_STRICT}자): {ch['strict_fail_count']}")
    print(f"  warn_short_non_numeric: {ch['warn_short_non_numeric_count']}")
    print(f"  numeric_unit_short(정상): {ch['numeric_unit_short_count']}")
    sd = report['subject_distribution']
    print(f"subject extra: {sd['extra_subjects']}")
    print(f"  missing: {sd['expected_missing']}")
    for af, av in report['assets'].items():
        print(f"  asset {af}: types={av['type_distribution']}, "
              f"raster_missing={len(av['raster_missing'])}, "
              f"vector_missing={len(av['vector_missing_content'])}, "
              f"non_dict={av['non_dict_count']}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
