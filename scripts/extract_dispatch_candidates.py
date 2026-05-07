#!/usr/bin/env python3
"""extract_dispatch_candidates.py — ee-agent quality dispatch 후보 추출.

Layer: L1.5 후속 (verify_questions_quality.py 검증 결과의 dispatch 단계)
read-only / 부작용 0 (markdown report 1개 신규 생성만)
exit 0 (catch 발견해도) / 사용자 review용 markdown

작동:
  1. questions.v2.json 입력
  2. Pydantic SPEC import (defensive fallback, verify_questions_quality.py 일관)
  3. 카테고리별 dispatch 후보 entry 추출:
     - 3-2: subject EXPECTED_SUBJECTS 외 분류 ("기타" 등)
     - 3-3: strict_fail (≤1자 선택지) — 데이터 오염 의심
     - 3-4: warn_short_non_numeric (2~4자, 숫자/단위 패턴 외)
     - 3-5: answer sentinel(0) — 별 트랙 (sample 추출만)
  4. markdown report 생성 (사용자 정정 결정용)

사용:
  python3 scripts/extract_dispatch_candidates.py app/data/questions.v2.json
  python3 scripts/extract_dispatch_candidates.py app/data/questions.v2.json -o reports/dispatch.md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
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

# 임계값 (verify_questions_quality.py 일관)
CHOICE_LEN_STRICT = 1
CHOICE_LEN_WARN = 4
ANSWER_VALID = {1, 2, 3, 4}
ANSWER_SENTINEL = {0}
EXPECTED_SUBJECTS = {'전기자기학', '전력공학', '전기기기', '회로이론', '제어공학', '전기설비기술기준'}
NUMERIC_UNIT_RE = re.compile(r'^[\d.\-+/×x*]+\s*[A-Za-zΩμ가-힣%°]*\s*$')


def _id(it: dict) -> str:
    return f"({it.get('year')}, {it.get('session')}, {it.get('subject')}, q{it.get('q_no')})"


def truncate(s, n=100):
    if not isinstance(s, str):
        return f"<{type(s).__name__}>"
    s = s.strip().replace('\n', ' ')
    return s[:n] + ("..." if len(s) > n else "")


def extract_subject_extra(items):
    out = []
    for it in items:
        sub = it.get('subject')
        if sub is not None and sub not in EXPECTED_SUBJECTS:
            choices = it.get('choices') or []
            out.append({
                'id': _id(it),
                'subject': sub,
                'text_preview': truncate(it.get('text'), 150),
                'choices_preview': [truncate(c, 30) for c in choices[:4]] if isinstance(choices, list) else None,
                'answer': it.get('answer'),
            })
    return out


def extract_strict_fail(items):
    out = []
    for it in items:
        ch = it.get('choices')
        if not isinstance(ch, list):
            continue
        bad = [(idx, c) for idx, c in enumerate(ch)
               if isinstance(c, str) and len(c.strip()) <= CHOICE_LEN_STRICT]
        if bad:
            out.append({
                'id': _id(it),
                'all_choices': [truncate(c, 30) for c in ch],
                'bad_choices': [{'idx': idx, 'value': repr(c), 'len': len(c.strip())} for idx, c in bad],
                'answer': it.get('answer'),
                'text_preview': truncate(it.get('text'), 100),
            })
    return out


def extract_warn_short_non_numeric(items):
    out = []
    for it in items:
        ch = it.get('choices')
        if not isinstance(ch, list):
            continue
        bad = []
        for idx, c in enumerate(ch):
            if not isinstance(c, str):
                continue
            stripped = c.strip()
            length = len(stripped)
            if CHOICE_LEN_STRICT < length <= CHOICE_LEN_WARN and not NUMERIC_UNIT_RE.match(stripped):
                bad.append((idx, c, length))
        if bad:
            out.append({
                'id': _id(it),
                'all_choices': [truncate(c, 30) for c in ch],
                'suspect_choices': [{'idx': idx, 'value': c, 'len': length} for idx, c, length in bad],
                'answer': it.get('answer'),
                'text_preview': truncate(it.get('text'), 100),
            })
    return out


def extract_answer_sentinel(items):
    out = []
    for it in items:
        if it.get('answer') in ANSWER_SENTINEL:
            choices = it.get('choices') or []
            out.append({
                'id': _id(it),
                'text_preview': truncate(it.get('text'), 150),
                'choices_preview': [truncate(c, 50) for c in choices[:4]] if isinstance(choices, list) else None,
                'answer': it.get('answer'),
                'solution_preview': truncate(it.get('solution'), 100),
            })
    return out


def render_markdown(report: dict, json_path: Path) -> str:
    L = []
    L.append(f"# ee-agent dispatch 후보 (D82 후속 cycle)")
    L.append("")
    L.append(f"- 입력: `{json_path}`")
    L.append(f"- 총 entry: {report['meta']['total_entries']}")
    L.append(f"- Pydantic SPEC: {'OK' if report['meta']['pydantic_available'] else 'FALLBACK ('+ str(report['meta']['pydantic_error'])[:80] +')'}")
    L.append(f"- EXPECTED_SUBJECTS: {sorted(EXPECTED_SUBJECTS)}")
    L.append(f"- 생성: {report['meta']['generated_at']}")
    L.append("")

    # Pydantic fails
    pf = report.get('pydantic_fails')
    if pf is not None:
        L.append(f"## Pydantic schema fails ({len(pf)}건)")
        L.append("")
        if not pf:
            L.append("_정합 — 5,331/5,331 통과 (D79 baseline 정합)._")
        else:
            for f in pf[:10]:
                L.append(f"- {f['id']}: `{f['error'][:120]}`")
            if len(pf) > 10:
                L.append(f"_... 외 {len(pf) - 10}건_")
        L.append("")

    # 3-2 subject extra
    extras = report['subject_extra']
    L.append(f"## 3-2 subject EXPECTED_SUBJECTS 외 분류 ({len(extras)}건)")
    L.append("")
    if not extras:
        L.append("_정합 — 모든 entry가 6과목에 매핑됨 (4fa87f5 EXPECTED_SUBJECTS '전기설비기술기준' 정정 후 효과 입증)._")
    else:
        for e in extras:
            L.append(f"### {e['id']}")
            L.append(f"- **subject**: `{e['subject']}`")
            L.append(f"- **text**: {e['text_preview']}")
            L.append(f"- **choices**: {e['choices_preview']}")
            L.append(f"- **answer**: {e['answer']}")
            L.append(f"- **결정**: 6과목 매핑 (전기자기학/전력공학/전기기기/회로이론/제어공학/전기설비기술기준)")
            L.append("")

    # 3-3 strict_fail
    strict = report['strict_fail']
    L.append(f"## 3-3 strict_fail (≤1자 선택지) ({len(strict)}건)")
    L.append("")
    if not strict:
        L.append("_정합._")
    else:
        for e in strict:
            L.append(f"### {e['id']}")
            L.append(f"- **text**: {e['text_preview']}")
            L.append(f"- **all_choices**: {e['all_choices']}")
            L.append(f"- **bad_choices**: {e['bad_choices']}")
            L.append(f"- **answer**: {e['answer']}")
            L.append(f"- **결정**: 데이터 오염 / 잘림 / 정상 (단일 글자 답)")
            L.append("")

    # 3-4 warn_short
    warn = report['warn_short_non_numeric']
    L.append(f"## 3-4 warn_short_non_numeric (2~4자, 숫자/단위 패턴 외) ({len(warn)}건)")
    L.append("")
    if not warn:
        L.append("_정합._")
    else:
        for e in warn:
            L.append(f"### {e['id']}")
            L.append(f"- **text**: {e['text_preview']}")
            L.append(f"- **all_choices**: {e['all_choices']}")
            L.append(f"- **suspect_choices**: {e['suspect_choices']}")
            L.append(f"- **answer**: {e['answer']}")
            L.append(f"- **결정**: 잘림 / 약어 정상 / 정정 필요")
            L.append("")

    # 3-5 sentinel
    sent = report['answer_sentinel']
    L.append(f"## 3-5 answer sentinel(0) ({len(sent)}건) — 별 트랙")
    L.append("")
    if not sent:
        L.append("_정합 — sentinel 0건._")
    else:
        L.append("_사용자 도메인 결정 필요 (sentinel 유지 / 누락 정정 / 별 분류). Sample 10건만 출력._")
        L.append("")
        for e in sent[:10]:
            L.append(f"- **{e['id']}**")
            L.append(f"  - text: {e['text_preview']}")
            L.append(f"  - choices: {e['choices_preview']}")
            L.append(f"  - solution: {e['solution_preview']}")
            L.append("")
        if len(sent) > 10:
            L.append(f"_... 외 {len(sent) - 10}건 (전체 list는 별 export 필요 시 --full flag 추가 권고)_")
            L.append("")

    # 종합
    L.append("## 종합 요약")
    L.append("")
    L.append(f"| 카테고리 | 건수 | 트랙 |")
    L.append(f"|---|---:|---|")
    if pf is not None:
        L.append(f"| Pydantic fails | {len(pf)} | SPEC 보강 후 재검증 |")
    L.append(f"| 3-2 subject extra | {len(extras)} | 본 cycle (사용자 도메인 매핑) |")
    L.append(f"| 3-3 strict_fail | {len(strict)} | 본 cycle (sample 분석 후 정정) |")
    L.append(f"| 3-4 warn_short_non_numeric | {len(warn)} | 본 cycle |")
    L.append(f"| 3-5 answer sentinel(0) | {len(sent)} | 별 트랙 (도메인 결정) |")
    L.append("")

    return "\n".join(L)


def main() -> int:
    parser = argparse.ArgumentParser(description='ee-agent quality dispatch 후보 추출')
    parser.add_argument('json_path', help='questions.v2.json 경로')
    parser.add_argument('--output', '-o', default=None, help='markdown report 출력 경로')
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

    # Pydantic 검증 (있을 때만)
    pydantic_fails = None
    if PYDANTIC_AVAILABLE:
        pydantic_fails = []
        for i, it in enumerate(items):
            try:
                Question(**it)
            except Exception as e:
                pydantic_fails.append({'idx': i, 'id': _id(it), 'error': str(e)[:200]})

    report = {
        'meta': {
            'json_path': str(json_path),
            'total_entries': len(items),
            'pydantic_available': PYDANTIC_AVAILABLE,
            'pydantic_error': PYDANTIC_ERR,
            'generated_at': datetime.now(timezone.utc).isoformat(),
        },
        'pydantic_fails': pydantic_fails,
        'subject_extra': extract_subject_extra(items),
        'strict_fail': extract_strict_fail(items),
        'warn_short_non_numeric': extract_warn_short_non_numeric(items),
        'answer_sentinel': extract_answer_sentinel(items),
    }

    # output path
    if args.output:
        output_path = Path(args.output).resolve()
    else:
        ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        output_path = json_path.parent.parent / 'reports' / f'dispatch_{ts}.md'

    output_path.parent.mkdir(parents=True, exist_ok=True)
    md = render_markdown(report, json_path)
    output_path.write_text(md, encoding='utf-8')

    # stdout summary
    print(f"=== dispatch report → {output_path} ===")
    print(f"total: {report['meta']['total_entries']}")
    if pydantic_fails is not None:
        print(f"  Pydantic fails: {len(pydantic_fails)}")
    print(f"  3-2 subject extra: {len(report['subject_extra'])}")
    print(f"  3-3 strict_fail: {len(report['strict_fail'])}")
    print(f"  3-4 warn_short_non_numeric: {len(report['warn_short_non_numeric'])}")
    print(f"  3-5 answer sentinel(0): {len(report['answer_sentinel'])}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
