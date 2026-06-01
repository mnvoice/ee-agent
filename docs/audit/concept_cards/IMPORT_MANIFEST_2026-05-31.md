# Concept Card Governance Import Manifest

작성일: 2026-05-31 KST
작성자: Codex supervisor

## 1. Import Purpose

This folder preserves the concept-card supervisor workflow artifacts inside the `ee-agent` git repository so they can be versioned, reviewed, and accessed from other devices.

This import does not claim:

- gold set completion
- corpus grounding completion
- semantic gain proof
- expansion pilot promotion to baseline

## 2. Source

Original Codex workspace:

```text
/Users/jeong-ujin_1/Documents/Codex/2026-05-30/ee-agent-d-3-governance-repo
```

Imported repository path:

```text
docs/audit/concept_cards/
```

Import branch:

```text
codex/concept-card-governance-import-2026-05-31
```

Base commit:

```text
d23bfad docs: dynamic binding spec v0.1 보존
```

## 3. Imported Content

Primary artifacts:

- `concept_cards/*.yaml`
- `concept_cards/index.md`
- `moai_artifacts/*`
- supervisor records and review summaries
- handoff reconciliation records
- new-window handoff/checklist files

Expected verification state:

| check | expected |
|---|---:|
| Codex concept-card YAML files | 33 |
| Codex YAML structure | OK |
| Codex extension risk levels | LOW 19 / MEDIUM 14 |
| MOAI entries | 30 |
| MOAI extension risk levels | LOW 18 / MEDIUM 12 |

## 4. Safety Policy

The original `~/Developer/ee-agent` working tree had many unrelated modified or untracked files at import time.

To avoid mixing this import with that dirty working tree, Codex created a separate clean git worktree:

```text
/Users/jeong-ujin_1/Documents/Codex/2026-05-31/ee-agent-concept-card-governance-import
```

Only `docs/audit/concept_cards/` should be staged for this import.

## 5. Rollback

If this import is wrong before merging, delete the import branch/worktree instead of touching the original dirty working tree.

If the import has already been committed but should be undone on the branch:

```bash
git revert <import-commit-sha>
```

If the branch should be discarded entirely:

```bash
git worktree remove /Users/jeong-ujin_1/Documents/Codex/2026-05-31/ee-agent-concept-card-governance-import
git branch -D codex/concept-card-governance-import-2026-05-31
```

