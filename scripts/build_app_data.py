#!/usr/bin/env python3
"""
Build script: Combine all question JSON files into a single app data file.
Strips unused fields, validates data quality, and outputs stats.
"""
import json
import glob
import logging
import os
from collections import defaultdict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
APP_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'app', 'data')

STRIP_FIELDS = {'solution_ocr', 'concept'}


def validate_question(q: dict) -> dict[str, bool]:
    """Validate question data completeness."""
    text = q.get('text', '').strip()
    choices = q.get('choices', [])
    answer = q.get('answer', 0)

    has_text = bool(text)
    has_all_choices = len(choices) == 4 and all(c.strip() for c in choices)
    has_some_choices = len(choices) == 4 and any(c.strip() for c in choices)
    has_valid_answer = answer in [1, 2, 3, 4]

    return {
        'has_text': has_text,
        'has_all_choices': has_all_choices,
        'has_some_choices': has_some_choices,
        'has_valid_answer': has_valid_answer,
        'is_complete': has_text and has_all_choices and has_valid_answer,
    }


def build():
    os.makedirs(APP_DATA_DIR, exist_ok=True)

    pattern = os.path.join(DATA_DIR, 'questions_기출_*.json')
    files = sorted(glob.glob(pattern))

    if not files:
        logger.error("No files found matching %s", pattern)
        return

    logger.info("Found %d files...", len(files))

    all_questions = []
    subjects = set()
    tags = set()
    years = set()
    sessions_by_year = defaultdict(set)

    # Validation counters
    total_complete = 0
    total_incomplete = 0
    defect_text_empty = 0
    defect_choices_all_empty = 0
    defect_choices_some_empty = 0
    defect_answer_bad = 0
    file_quality = {}

    for fpath in files:
        fname = os.path.basename(fpath)
        with open(fpath, encoding='utf-8') as f:
            questions = json.load(f)

        file_complete = 0
        file_incomplete = 0

        for q in questions:
            # Strip unwanted fields
            for field in STRIP_FIELDS:
                q.pop(field, None)

            # Validate and tag quality
            v = validate_question(q)
            if v['is_complete']:
                q['quality'] = 'complete'
                file_complete += 1
                total_complete += 1
            else:
                q['quality'] = 'incomplete'
                file_incomplete += 1
                total_incomplete += 1
                if not v['has_text']:
                    defect_text_empty += 1
                if not v['has_all_choices'] and not v['has_some_choices']:
                    defect_choices_all_empty += 1
                elif not v['has_all_choices']:
                    defect_choices_some_empty += 1
                if not v['has_valid_answer']:
                    defect_answer_bad += 1

            # Collect stats
            subjects.add(q.get('subject', ''))
            tags.add(q.get('tag', ''))
            year = q.get('year', 0)
            session = q.get('session', '')
            years.add(year)
            if year and session:
                sessions_by_year[year].add(session)

            all_questions.append(q)

        file_quality[fname] = {
            'total': len(questions),
            'complete': file_complete,
            'incomplete': file_incomplete,
        }

    total = len(all_questions)
    logger.info("Total questions: %d", total)

    # Validation report
    logger.info("")
    logger.info("=" * 60)
    logger.info("DATA QUALITY VALIDATION REPORT")
    logger.info("=" * 60)
    logger.info("Complete:   %d / %d (%.1f%%)", total_complete, total,
                total_complete / total * 100 if total else 0)
    logger.info("Incomplete: %d / %d (%.1f%%)", total_incomplete, total,
                total_incomplete / total * 100 if total else 0)
    logger.info("")
    logger.info("Defect breakdown (among incomplete):")
    logger.info("  text empty:         %d", defect_text_empty)
    logger.info("  all choices empty:  %d", defect_choices_all_empty)
    logger.info("  some choices empty: %d", defect_choices_some_empty)
    logger.info("  answer invalid:     %d", defect_answer_bad)
    logger.info("")

    # Per-file report for files with issues
    problem_files = {k: v for k, v in file_quality.items() if v['incomplete'] > 0}
    if problem_files:
        logger.info("Files with incomplete questions (%d files):", len(problem_files))
        for fname, stats in sorted(problem_files.items()):
            pct = stats['incomplete'] / stats['total'] * 100 if stats['total'] else 0
            logger.info("  %s: %d/%d incomplete (%.0f%%)",
                        fname, stats['incomplete'], stats['total'], pct)
    logger.info("=" * 60)

    # Write questions.json
    questions_path = os.path.join(APP_DATA_DIR, 'questions.json')
    with open(questions_path, 'w', encoding='utf-8') as f:
        json.dump(all_questions, f, ensure_ascii=False, separators=(',', ':'))

    file_size_mb = os.path.getsize(questions_path) / (1024 * 1024)
    logger.info("Written: %s (%.1f MB)", questions_path, file_size_mb)

    # Build subjects with tag lists
    subject_tags = defaultdict(set)
    for q in all_questions:
        subj = q.get('subject', '')
        tag = q.get('tag', '')
        if subj and tag:
            subject_tags[subj].add(tag)

    subjects_data = {
        s: sorted(list(t)) for s, t in sorted(subject_tags.items())
    }

    # Build year-session map (sort sessions by converting numeric parts)
    def session_sort_key(s):
        try:
            return int(s.replace('회', '').replace('차', ''))
        except Exception:
            return 0

    year_sessions = {
        str(year): sorted(list(sessions), key=session_sort_key)
        for year, sessions in sorted(sessions_by_year.items(), reverse=True)
    }

    # Stats (include quality metrics)
    stats = {
        'total': len(all_questions),
        'complete': total_complete,
        'incomplete': total_incomplete,
        'subjects': subjects_data,
        'tags': sorted(list(tags)),
        'years': year_sessions,
        'tag_count': len(tags),
        'subject_count': len(subjects),
    }

    stats_path = os.path.join(APP_DATA_DIR, 'stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    logger.info("Written: %s", stats_path)
    logger.info("")
    logger.info("Stats summary:")
    logger.info("  Subjects: %s", sorted(subjects))
    logger.info("  Tags: %d unique", len(tags))
    logger.info("  Years: %s", sorted(years))
    logger.info("  Total: %d questions (%d complete, %d incomplete)",
                len(all_questions), total_complete, total_incomplete)


if __name__ == '__main__':
    build()
