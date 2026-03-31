# EE-Agent TODO

Updated: 2026-04-01

## Current Status

- Total questions: 5,007 (complete, filtered)
- Incomplete: 187 (excluded from app)
- EE-Agent accuracy: 2020 75.0%, 2022 92.5%

## Phase 1: Data Recovery ($0) -- DONE

- [x] T1: Add validation filter to `scripts/build_app_data.py`
- [x] T2: Analyze 928 incomplete questions (year/subject distribution)
- [x] T3: Check Mathpix data (65 files) -- 898/902 matched, Vision API unnecessary

## Phase 2: Mathpix Recovery ($0) -- DONE

- [x] T4: Mathpix parsing recovery (recover_from_mathpix.py)
- [x] T5: Merge recovered data and verify quality (4,834 -> 5,007 complete)

## Phase 3: CBT App Features ($0) -- DONE

- [x] T6: CBT mock exam (timer, 100Q random, marking, grid, pass/fail)
- [x] T7: Concept-based group study (tag progress dots + percentage)
- [x] T8: Weakness analysis (top 10 weak concepts, error rate ranking)

## Phase 4: iPad Deployment ($0)

- [ ] T11: Deploy to GitHub Pages for iPad offline study (5min)

## Phase 5: Future

- [ ] T9: Acquire post-2022 CBT questions
- [ ] T10: Improve EE-Agent accuracy (2020: 75% -> 85%)
