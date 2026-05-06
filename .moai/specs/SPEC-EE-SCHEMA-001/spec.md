# SPEC-EE-SCHEMA-001: questions.json schema 정규화 (Phase 1)

## Metadata

- **Status**: DRAFT
- **Created**: 2026-05-07
- **Owner**: ee-agent
- **Origin**: D75 reflection (verify-agent DECISIONS.md, 2026-05-07)
- **Source lessons**: LESSON-001, LESSON-002, LESSON-004 (lessons.md)
- **Related decision**: DECISIONS.md D76 (Phase 1 SPEC 확정)

## Context

ee-agent의 `app/data/questions.json` (5,331 entries) 은 14개 필드로 구성되며, 다음 4개 부채를 보유한다:

1. `stem_figure` 1급 필드 부재 → D72 발현 (~3주), figure_recovery 트랙 분리
2. `session` 타입 이질 (int 1 vs str "1회", 97건 / 5,234건) → D74 발현
3. `figure_svg` 출처 메타 부재 → LLM 합성 vs 실측 구분 불가, 16.7% MISMATCH 측정 (DEVLOG 162)
4. 메모리/문서 entry 수 진술 불일치 (5,307 vs 5,331)

본 SPEC은 위 부채 중 1, 2, 3 + entry 수 정정을 schema 차원에서 해결한다.

## Scope

### In Scope (Phase 1)
- REQ-001: `stem_figure` 1급 필드 추가 (FigureRef 타입)
- REQ-002~003: FigureRef + Coords 구조 정의
- REQ-004: source 메타 모든 필드 적용 (4개 enum)
- REQ-005: `figure_svg` / `solution_svg` → FigureRef 통합 (옵션 A)
- REQ-006: batch 이력 외부 manifest 분리 (옵션 A2)
- REQ-007: session 타입 정규화 (str "{N}회" 통일)
- REQ-008: `image_path` 컨벤션 + NFC '회' suffix 강제
- REQ-009: entry 수 정정 (5,307 → 5,331)
- REQ-010: 신규 entry 강제 게이트 (pre-commit hook)
- REQ-011: external_tool source 의 tool_name 메타

### Out of Scope (별 SPEC 또는 별 트랙)
- M6: figure_text_90 90건의 stem_figure.coords 채움 → D73 fix 트랙
- M7: D73 manifest 10건의 source=measured 재분류 → D73 fix 트랙
- Phase C: ETL 입력 게이트 (LESSON-002 강화) → 별 SPEC
- Phase D: verify-agent Layer 1.5 합성 vs 실측 검증 (LESSON-008) → 별 SPEC
- LESSON-003 (디렉토리 명명 linter) → 별 SPEC
- LESSON-005 (glossary 강제) → verify-agent CONSTITUTION
- LESSON-006 (NFC/NFD 플랫폼 fallback) → REQ-008에 부분 포함, 전면적인 것은 별 SPEC
- LESSON-007 (외부 도구 scan probe) → 별 SPEC

## Requirements (EARS format)

### REQ-001 stem_figure 1급 필드

When a question entry is created or updated, the schema shall require a field named `stem_figure` of type `FigureRef | None`.

Acceptance:
- 모든 5,331 entry에 stem_figure key 존재 (M4 마이그레이션 후)
- None 값은 "그림 없음 명시" 의미 (key 누락과 구분)
- 신규 entry 는 None 허용 안 함 (REQ-010 참조)

### REQ-002 FigureRef 구조

When a `FigureRef` instance is constructed, it shall include the following fields:

| 필드 | 타입 | 필수 | 비고 |
|---|---|---|---|
| `type` | enum {raster, vector_svg, none} | 필수 | 6개 → 3개 축소 |
| `source` | enum {human, llm_synthesized, measured, external_tool} | 필수 | derived 제외 (4개) |
| `content_kind` | enum {circuit_diagram, table, graph, phasor_diagram, block_diagram, wave_form, vector_field, other} \| None | 선택 | tag 와 차원 분리 (CLI 결정) |
| `image_path` | str \| None | 선택 | type=raster 일 때 필수 |
| `svg_content` | str \| None | 선택 | type=vector_svg 일 때 필수 |
| `coords` | Coords \| None | 선택 | PDF 원본 좌표 |
| `confidence` | float [0.0, 1.0] | 필수 | 디폴트 1.0 |
| `verified_at` | datetime \| None | 선택 | 검증 완료 시각 |
| `verified_against_measurement` | bool \| None | 선택 | source=llm_synthesized 일 때만 의미 |
| `tool_name` | str \| None | 선택 | source=external_tool 일 때 필수 (REQ-011) |

Acceptance:
- type=raster 이면 image_path 필수
- type=vector_svg 이면 svg_content 필수
- source=external_tool 이면 tool_name 필수
- source=llm_synthesized 이면 verified_against_measurement 권장 (필수 아님)

### REQ-003 Coords 구조

When a `Coords` instance is constructed, it shall include:

| 필드 | 타입 | 비고 |
|---|---|---|
| `pdf_page` | int | 1-based |
| `bbox` | tuple[float, float, float, float] | (x0, y0, x1, y1), PDF point 단위 |
| `extraction_tool` | enum {mathpix, pymupdf, manual_crop, claude_vision} | 좌표 추출 도구 (FigureRef.tool_name 과 차원 분리) |

### REQ-004 source enum 모든 필드 적용

When the question schema is migrated, every data field shall declare its source.

| 필드 | source 표현 | 마이그레이션 디폴트 |
|---|---|---|
| `stem_figure` | FigureRef.source | (None entry 는 source 없음) |
| `figure_svg` | FigureRef.source | `llm_synthesized` |
| `solution_svg` | FigureRef.source | `llm_synthesized` |
| `text` | `text_source: SourceEnum` | `external_tool` (mathpix) |
| `choices` | `choices_source: SourceEnum` | `external_tool` (mathpix) |
| `solution` | `solution_source: SourceEnum` | `llm_synthesized` (Claude solver) |
| `steps` | `steps_source: SourceEnum` | `llm_synthesized` |
| `answer` | `answer_source: SourceEnum` | `human` (정답지 원본) |

Acceptance:
- 모든 source enum 외 값 0건
- 기존 정정 이력 있는 entry: text_source / choices_source 가 `human` 으로 승격 (별 마이그레이션 단계)

### REQ-005 figure_svg / solution_svg → FigureRef 통합 (옵션 A)

When existing `figure_svg` and `solution_svg` string fields are migrated, they shall be wrapped into `FigureRef` instances:

- type = `vector_svg`
- source = `llm_synthesized` (현재 모든 batch 결과)
- svg_content = 기존 문자열 값
- 필드명 (`figure_svg`, `solution_svg`) 유지

Acceptance:
- 기존 문자열 값 손실 0건
- 변환 후 FigureRef.svg_content 와 원본 문자열 hash 일치

### REQ-006 batch 이력 외부 manifest (옵션 A2)

When a `figure_svg` or `solution_svg` is created via LLM batch, the batch metadata shall be stored in external manifest at `data/batch_manifest/<batch_name>.json`.

Manifest schema:
```
{
  "batch_id": "batch_phase2_sonnet_20260429",
  "model": "claude-sonnet-4",
  "created_at": "2026-04-29T...",
  "entries": [
    {"q_no": 1, "year": 2020, "session": "1회", "field": "figure_svg"}
  ]
}
```

Acceptance:
- FigureRef 에 batch_id 필드 추가하지 않음 (entry 부피 유지)
- 기존 batch 디렉토리 (`data/batch_phase2_sonnet/`, `data/batch_solution_svg_v2/` 등) 에서 manifest 추출 가능

### REQ-007 session 타입 정규화

When the schema is migrated, all `session` field values shall be normalized to string format `"{N}회"` (NFC normalized).

- Integer `1` → string `"1회"`
- Existing string `"1회"` → 동일 (NFC 적용)

Acceptance:
- session 타입 100% str 단일
- NFC 비-NFC 형식 0건

### REQ-008 image_path 컨벤션

When `stem_figure.image_path` is set, it shall use the relative path:

```
data/pdf_pages/{year}_{session}/q{n}_stem.png
```

Where:
- `{year}` = 4-digit year (e.g., `2020`)
- `{session}` = NFC-normalized "{N}회" (e.g., `1회`, NOT `1`)
- `{n}` = q_no (1-based)

Acceptance:
- 기존 `data/pdf_pages/2011_1` outlier (회 누락) → `2011_1회` 로 정정
- 디렉토리 명명 linter 가 정규식 `^\d{4}_\d{1,2}회$` 강제 (별 SPEC LESSON-003)

### REQ-009 entry 수 정정

When SPEC-EE-SCHEMA-001 is implemented, all current-state references to entry count in memory and SPEC documents shall be updated to **5,331** (verified 2026-05-07).

대상 위치 (정정 필요):
- `~/.claude/projects/-Users-jeong-ujin-1/memory/MEMORY.md` (현재 진술 라인)
- `~/.claude/projects/-Users-jeong-ujin-1/memory/project_ee_agent_todo.md` (빌드 결과)
- `~/.claude/projects/-Users-jeong-ujin-1/memory/project_ee_practice.md` (symlink 측정)

보존 위치 (변화 이력 기록):
- `5,007 → 5,307` (T9 결과 기록)
- `5,307 → 5,331` (사본 2종 정리 후 정정 기록)
- `5,307 → 5,210` (4-13 retag 사이클 사본 처리 기록)

Acceptance:
- 메모리 / 본 SPEC 의 현재-상태 진술 5,307 출현 0건 (이력 기록 제외)

### REQ-010 신규 entry 강제 게이트

When a new entry is added to `app/data/questions.json` via git commit, a pre-commit hook shall verify:

1. `stem_figure` 키 존재 (omit 금지)
2. 신규 entry 의 `stem_figure` 값은 explicit FigureRef instance (None 거부, type="none" 허용)
3. 모든 source 메타 필드 (text_source, choices_source, solution_source, steps_source, answer_source) 존재

기존 5,331 entry (baseline) 는 면제: stem_figure: null 허용.

Hook location: `.pre-commit-config.yaml` 또는 `.git/hooks/pre-commit`.

Acceptance:
- 베이스라인 (5,331 entry) 검증 통과
- 신규 entry 추가 시 stem_figure 누락 → commit 차단

### REQ-011 external_tool source 의 tool_name 메타

When `FigureRef.source == external_tool`, the `FigureRef.tool_name` field shall be required.

- 예: `mathpix`, `tesseract`, `paddleocr`
- 본 필드는 `Coords.extraction_tool` (PDF 좌표 측정 도구) 과 차원 분리:
  - `tool_name`: 콘텐츠 생성 도구 (이미지/SVG 자체)
  - `extraction_tool`: 좌표 추출 도구

Acceptance:
- source=external_tool 인 모든 FigureRef 에 tool_name 존재
- tool_name 누락 → 검증 fail

## Migration Plan (Phase 1)

| Step | 작업 | 영향 entry | 검증 |
|---|---|---|---|
| M1 | session 타입 정규화 (int → str "{N}회") + NFC | ~97 (int) | 100% str 단일 |
| M2 | figure_svg 문자열 → FigureRef (source=llm_synthesized) | figure_svg 보유 entry | hash 일치 |
| M3 | solution_svg 문자열 → FigureRef (source=llm_synthesized) | solution_svg 보유 entry | hash 일치 |
| M4 | stem_figure: null 추가 (모든 entry) | 5,331 | 키 존재 100% |
| M5 | source 메타 필드 디폴트 채움 (text_source, choices_source, solution_source, steps_source, answer_source) | 5,331 | enum 외 값 0건 |
| MM1 | batch manifest 추출 (`data/batch_manifest/` 신설) | batch 이력 | manifest schema 통과 |

별 트랙 (Out of Scope):
- M6: figure_text_90 90건 stem_figure.coords 채움 (D73 fix)
- M7: D73 manifest 10건 source=measured 재분류 (D73 fix)

## Acceptance Criteria (전체)

- 5,331 entry 모두 신규 schema (Pydantic 모델) 검증 통과
- session 타입 100% str 단일 ({N}회 NFC)
- source enum 외 값 0건
- pre-commit hook 베이스라인 통과 + 신규 entry stem_figure 누락 거부
- batch manifest 모든 batch 디렉토리 매핑 (누락 0건)
- 메모리 5,307 현재-진술 0건 (이력 기록 제외)

## Framework Catch (사용자 명시, 본 SPEC 차원 직접 적용)

본 SPEC 은 다음 framework catch 를 schema 차원에서 직접 해결한다:

- **Catch #18 (사용자 명명 — 출처 catalog 확인 필요)**: 메모리 진술 자체 재발 — entry 수 5,331 vs 5,307 불일치
  - 본 SPEC 차원 적용: REQ-009 (entry 수 정정 강제)
- **D69 (외부 게이트, verify-agent DECISIONS.md)**: 외부 게이트 SPEC 차원 직접 적용
  - 본 SPEC 차원 적용: REQ-006 (batch 이력 외부 manifest 분리), REQ-010 (pre-commit hook)

## References

- LESSON-001 schema 1급 시민 (lessons.md, 2026-05-07)
- LESSON-002 입력 정규화 게이트 (lessons.md, 2026-05-07)
- LESSON-004 출처/품질 메타 (lessons.md, 2026-05-07)
- DECISIONS.md D75 (재발 차단 3 layer, 2026-05-07)
- DECISIONS.md D72 (stem figure 데이터 부재 진단, 2026-05-05)
- DECISIONS.md D74 (session 타입 이질, 2026-05-05)
- project_ee_agent_architecture_failure.md (D75 reflection)

---

Phase 1 implementation milestones (별 SPEC 분리 후속):
- Phase B: 마이그레이션 실행 (M1~M5, MM1)
- Phase C: ETL 입력 게이트 (LESSON-002 강화)
- Phase D: verify-agent Layer 1.5 합성 검증 (LESSON-008)
