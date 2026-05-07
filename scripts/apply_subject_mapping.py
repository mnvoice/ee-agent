#!/usr/bin/env python3
"""apply_subject_mapping.py — questions.v2.json subject 필드 정정.

사용:
  # 1. dry-run (write X, 매칭 결과 확인)
  python3 scripts/apply_subject_mapping.py app/data/questions.v2.json mapping.json --dry-run

  # 2. 실제 적용 (백업 자동 생성)
  python3 scripts/apply_subject_mapping.py app/data/questions.v2.json mapping.json

mapping.json 형식:
{
  "matches": [
    {"year": 1999, "session": 3, "q_no": 1,
     "current_subject": "기타", "new_subject": "전기자기학"},
    ...
  ]
}

- 매칭 키: (year, session, q_no, current_subject) 4-tuple — 정확 entry 식별
- new_subject는 EXPECTED_SUBJECTS = 6과목 외 reject
- 적용 시 원본 자동 백업 (questions.v2.json.bak_<UTC>.json — .gitignore 정합)
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

EXPECTED_SUBJECTS = {'전기자기학', '전력공학', '전기기기', '회로이론', '제어공학', '전기설비기술기준'}


def main() -> int:
    parser = argparse.ArgumentParser(description='subject 필드 매핑 정정')
    parser.add_argument('json_path', help='questions.v2.json 경로')
    parser.add_argument('mapping_path', help='mapping JSON 경로')
    parser.add_argument('--dry-run', action='store_true', help='write X, log만')
    args = parser.parse_args()

    json_path = Path(args.json_path).resolve()
    mapping_path = Path(args.mapping_path).resolve()

    if not json_path.is_file():
        print(f"ERROR: {json_path} not found", file=sys.stderr); return 2
    if not mapping_path.is_file():
        print(f"ERROR: {mapping_path} not found", file=sys.stderr); return 2

    # mapping load + validate
    with open(mapping_path, encoding='utf-8') as f:
        mapping_data = json.load(f)
    matches = mapping_data.get('matches', [])
    if not isinstance(matches, list):
        print("ERROR: mapping['matches'] must be list", file=sys.stderr); return 2

    invalid = [m for m in matches if m.get('new_subject') not in EXPECTED_SUBJECTS]
    if invalid:
        print(f"ERROR: invalid new_subject (EXPECTED 외):", file=sys.stderr)
        for m in invalid:
            print(f"  {m}", file=sys.stderr)
        print(f"  EXPECTED: {sorted(EXPECTED_SUBJECTS)}", file=sys.stderr)
        return 2

    # data load
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    items = data.get('questions', data) if isinstance(data, dict) else data
    if not isinstance(items, list):
        print(f"ERROR: items not a list", file=sys.stderr); return 2

    # 매핑 적용 (D-fix: dup-aware FIFO queue per 4-tuple key)
    from collections import defaultdict
    match_queue = defaultdict(list)
    for m in matches:
        key = (m.get('year'), m.get('session'), m.get('q_no'), m.get('current_subject'))
        match_queue[key].append(m['new_subject'])

    applied = []
    for it in items:
        it_key = (it.get('year'), it.get('session'), it.get('q_no'), it.get('subject'))
        if match_queue.get(it_key):
            new_subject = match_queue[it_key].pop(0)
            if not args.dry_run:
                it['subject'] = new_subject
            applied.append({'key': it_key, 'new_subject': new_subject})

    # 남은 매칭 = not_found
    not_found = []
    for key, remaining in match_queue.items():
        for new_sub in remaining:
            not_found.append({'key': key, 'new_subject': new_sub})

    # 보고
    mode = "(dry-run)" if args.dry_run else ""
    print(f"=== subject mapping {mode} ===")
    print(f"applied: {len(applied)}/{len(matches)}")
    for a in applied:
        print(f"  {a['key']} → '{a['new_subject']}'")
    if not_found:
        print(f"not_found: {len(not_found)}")
        for nf in not_found:
            print(f"  {nf}")
        if not args.dry_run:
            print("ERROR: not_found exists — 적용 중단 (원본 무결)", file=sys.stderr)
            return 1

    # 실제 write (dry-run 아니고 적용할 게 있을 때만)
    if not args.dry_run and applied:
        ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        backup_path = json_path.with_name(f"{json_path.stem}.bak_{ts}{json_path.suffix}")
        # 원본을 백업 path로 복사 (원본 그대로)
        backup_path.write_bytes(json_path.read_bytes())
        # 수정본 write
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ backup: {backup_path}")
        print(f"✓ written: {json_path}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
