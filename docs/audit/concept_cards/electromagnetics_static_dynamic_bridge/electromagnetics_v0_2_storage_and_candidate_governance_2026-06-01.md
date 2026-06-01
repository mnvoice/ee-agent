# Electromagnetics v0.2 Storage and Candidate Governance - 2026-06-01

Scope: review-only governance memo for continuing `electromagnetics_static_dynamic_bridge_discovery_v0.1` into a possible v0.2 candidate pass.

This memo fixes the storage policy before any additional candidate selection. It does not mutate source data, YAML, answer keys, JSON, or concept cards.

## Guardrails

- Keep PR #1 open, draft, and unmerged.
- Do not patch YAML.
- Do not create new concept-card YAML files.
- Do not promote `expansion_pilot` cards.
- Do not claim gold-set, benchmark, semantic-gain, or production readiness.
- Treat pressure flags as evidence signals only, not patch authorization.

## Current PR State Check

PR #1 was checked through the GitHub connector during this continuation.

| Field | Observed state |
|---|---|
| Repository | `mnvoice/ee-agent` |
| PR | `#1` |
| State | `open` |
| Draft | `true` |
| Merged | `false` |
| Head branch | `codex/concept-card-governance-import-2026-05-31` |
| Base branch | `feat/phase-b-migration` |

Supervisor interpretation:

```text
PR #1 can remain the iPad-accessible review container, but it must not be merged or marked ready for review.
```

## Canonical Local Storage

The canonical local artifact directory for this electromagnetic continuation is:

```text
/Users/jeong-ujin_1/Documents/Codex/2026-06-01/repo-mnvoice-ee-agent-pr-1
```

Reason:

- It already contains the v0.1 governance Markdown files.
- It already contains the integrated HTML learning map.
- It already contains the Obsidian natural-language full session record.
- It already contains the artifact index for navigation.
- The sibling `repo-mnvoice-ee-agent-pr-1-2` directory is empty and should not become the canonical record unless a later supervisor explicitly migrates the archive.

## Git Parallel Storage Policy

Git storage is allowed only as a mirror of review artifacts, not as a source-data patch.

Allowed Git-side artifacts:

- governance Markdown;
- review Markdown;
- Obsidian-style natural-language memo;
- HTML review files;
- artifact index or manifest files.

Disallowed Git-side artifacts:

- YAML mutation;
- new concept-card YAML;
- JSON answer-key mutation;
- source-data patch;
- `expansion_pilot` promotion;
- any file that claims gold-set, benchmark, semantic-gain, or production readiness.

Recommended Git-side path if artifacts are mirrored later:

```text
docs/audit/concept_cards/electromagnetics_static_dynamic_bridge/
```

The repository working tree at `/Users/jeong-ujin_1/Developer/ee-agent` is currently broad and dirty. Therefore Git mirroring must be selective:

```text
Add only the explicit review artifact paths intended for preservation.
Do not use broad add commands.
Do not sweep unrelated data, PDF, generated OCR, or output files into the PR.
```

## Save Flow

Recommended two-lane save flow:

| Lane | Location | Purpose | Mutation level |
|---|---|---|---|
| Local canonical archive | `Documents/Codex/2026-06-01/repo-mnvoice-ee-agent-pr-1` | Fast continuation, full session memory, HTML review work | Review artifacts only |
| Git mirror | `mnvoice/ee-agent` PR #1 branch, review-only path | Remote backup and iPad-accessible review container | Selected review artifacts only |

This means local artifact creation can continue first. Git mirroring should happen in small, explicit batches after the artifact index is updated.

## v0.2 Candidate Entry Rule

v0.2 should not start by blindly sampling more rows.

It should start from the integrated learning map and select rows that strengthen the five-bundle structure:

1. 정전계 / 정자계 앵커
2. 유도기전력
3. 인덕턴스 / 결합
4. 맥스웰 / 변위전류
5. 전자파 속도

The selection question is:

```text
Does this row make a physical quantity movement clearer?
```

Not:

```text
Does this row merely add another formula name?
```

## v0.2 Hold Boundary

The following rows remain blocked from study-card use:

| Row | Reason |
|---|---|
| `p4 q1` | answer or choice conflict |
| `p154 q1` | calculation/answer conflict |
| `p158 q9` | choice alignment contamination |
| `p57 q7` | boundary-condition answer conflict |
| `p130 q3` | figure dependency and likely calculation conflict |

These rows may appear only as cleanup or source-recovery evidence. They do not authorize patching.

## v0.2 Candidate Shape

The next review artifact should be a candidate manifest, not a patch.

Recommended artifact:

```text
electromagnetics_static_dynamic_bridge_v0_2_candidate_manifest_2026-06-01.md
```

Recommended fields:

| Field | Meaning |
|---|---|
| Row | Page/question identifier or source locator |
| Bundle | One of the five learning-map bundles |
| Physical quantity flow | Example: `Q or rho -> E -> D -> Psi` |
| Static parent | Root static concept |
| Dynamic bridge | If present, the bridge behavior |
| Cross-subject target | Machines, circuit theory, power engineering, control, Maxwell/electromagnetic waves |
| Source status | source-grounded, caveated, figure-dependent, conflicted, or hold |
| Candidate decision | usable-review, caveated-review, cleanup-only, or hold |
| Non-authorization note | Explicit reminder that this row does not authorize YAML or answer-key mutation |

## Closeout

This memo authorizes only the next review-layer step:

```text
Create a v0.2 candidate manifest from the integrated learning map while preserving the local archive and preparing for selective Git mirroring.
```

This memo does not authorize:

- PR merge;
- PR ready-for-review transition;
- YAML mutation;
- source-data mutation;
- answer-key mutation;
- concept-card creation;
- concept-card promotion.

## Git Mirror Continuation

Selected Markdown review artifacts were mirrored to PR #1's head branch through the GitHub connector.

Branch:

```text
codex/concept-card-governance-import-2026-05-31
```

Mirrored paths:

```text
docs/audit/concept_cards/electromagnetics_static_dynamic_bridge/electromagnetics_v0_2_storage_and_candidate_governance_2026-06-01.md
docs/audit/concept_cards/electromagnetics_static_dynamic_bridge/electromagnetics_static_dynamic_bridge_v0_2_candidate_manifest_2026-06-01.md
docs/audit/concept_cards/electromagnetics_static_dynamic_bridge/electromagnetics_static_dynamic_bridge_v0_2_exam_memory_lines_2026-06-01.md
```

Git commit SHAs observed from the connector:

```text
fe0be82258529547c8c709f8f0c4701c07d08d3a
f366174d026e63f33d8b89f31e64fb5861e1dcbd
c3e354ea50a3caef8fa562aa0415d487d967336f
```

HTML review artifacts remain in the local canonical archive for direct browser viewing.

This mirror pass still does not authorize:

- PR merge;
- PR ready-for-review transition;
- YAML mutation;
- source-data mutation;
- answer-key mutation;
- concept-card creation;
- concept-card promotion.
