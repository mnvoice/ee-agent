"""
Phase 1 Schema SPEC — D75 fix 트랙.
ee-agent 데이터 표준. 모든 question entry는 본 schema 통과 필수.

결정 사항:
- type enum 3개 (raster/vector_svg/none) — 차원 혼재 catch 회피
- source enum 4개 (human/llm_synthesized/measured/external_tool)
- figure_svg/solution_svg → FigureRef 통합 (옵션 A)
- batch 이력 → 외부 manifest (옵션 A2, D69 외부 게이트 원칙)
- entry 수 5,331 (메모리 5,307 정정)

옵션 C 수정 (Phase 1 = 다수파 type 수용, Phase B에서 정규화):
- q_no: Optional[int] (None 48건 허용)
- difficulty: Optional[Union[int, str]] (int 4,957 + str 267 혼재 수용)
- tag: Optional[str] (다수파 str 5,304건)
- steps: Optional[dict] (다수파 dict 5,262건)
- 마이그레이션 q_no/tag default 보정
"""
from datetime import datetime
from enum import Enum
from typing import Literal, Optional, Union
from pydantic import BaseModel, Field, field_validator


# ===== Enum =====

class SourceEnum(str, Enum):
    HUMAN = "human"
    LLM_SYNTHESIZED = "llm_synthesized"
    MEASURED = "measured"
    EXTERNAL_TOOL = "external_tool"


FigureType = Literal["raster", "vector_svg", "none"]
ExtractionTool = Literal[
    "mathpix", "pymupdf", "manual_crop", "claude_vision", "ollama_qwen2_5vl"
]


# ===== Sub-models =====

class Coords(BaseModel):
    pdf_page: int
    bbox: tuple[float, float, float, float]  # PDF point: (x0, y0, x1, y1)
    extraction_tool: ExtractionTool


class FieldSource(BaseModel):
    """텍스트 필드 출처 메타 (text/choices/answer/solution/steps)."""
    source: SourceEnum
    tool_name: Optional[str] = None
    verified_at: Optional[datetime] = None


class FigureRef(BaseModel):
    """
    그림 참조 표준 (stem_figure / figure_svg / solution_svg 공통).
    type=raster → image_path 필수
    type=vector_svg → svg_content 필수
    type=none → 그림 없음 명시
    """
    type: FigureType
    source: SourceEnum
    image_path: Optional[str] = None
    svg_content: Optional[str] = None
    coords: Optional[Coords] = None
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    verified_at: Optional[datetime] = None
    verified_against_measurement: Optional[bool] = None
    tool_name: Optional[str] = None

    @field_validator("image_path")
    @classmethod
    def _check_image_path(cls, v, info):
        if info.data.get("type") == "raster" and not v:
            raise ValueError("type=raster requires image_path")
        return v

    @field_validator("svg_content")
    @classmethod
    def _check_svg_content(cls, v, info):
        if info.data.get("type") == "vector_svg" and not v:
            raise ValueError("type=vector_svg requires svg_content")
        return v


# ===== Question =====

class Question(BaseModel):
    """
    전기기사 시험 question 표준 schema.
    questions.json의 모든 entry는 본 model 통과 필수.
    """
    # 기본 식별
    year: int
    session: str  # '1회'/'2회' — D74 정규화 후 str 통일
    subject: str
    q_no: Optional[int] = None  # 옵션 C: None 48건 허용

    # 본문 (출처 메타 부착)
    text: str
    text_source: FieldSource
    choices: list[str]
    choices_source: FieldSource
    answer: int
    answer_source: FieldSource = Field(
        default_factory=lambda: FieldSource(source=SourceEnum.HUMAN)
    )

    # 풀이 (있을 때만 source)
    solution: Optional[str] = None
    solution_source: Optional[FieldSource] = None
    steps: Optional[dict] = None  # 옵션 C: dict 다수파 (5,262건) 수용
    steps_source: Optional[FieldSource] = None

    # 그림 (1급 시민) — Phase 1 핵심
    stem_figure: Optional[FigureRef] = None   # null = 그림 없음 명시
    figure_svg: Optional[FigureRef] = None    # 기존 LLM 합성
    solution_svg: Optional[FigureRef] = None  # 기존 풀이 도식

    # 분류 메타
    difficulty: Optional[Union[int, str]] = None  # 옵션 C: int/str 혼재 수용
    q_type: Optional[str] = None
    tag: Optional[str] = None  # 옵션 C: str 다수파 (5,304건) 수용
    quality: Optional[str] = None

    @field_validator("session", mode="before")
    @classmethod
    def _normalize_session(cls, v):
        # D74 정규화: int(1)/str("1") → str("1회")
        if isinstance(v, int):
            return f"{v}회"
        if isinstance(v, str) and v and not v.endswith("회"):
            return f"{v}회"
        return v


# ===== Migration =====

def migrate_legacy_question(legacy: dict) -> Question:
    """
    기존 questions.json entry → 신 Question model 변환.

    Phase 1 마이그레이션 규칙:
    - figure_svg/solution_svg (str SVG) → FigureRef(vector_svg, llm_synthesized)
    - stem_figure → None (Phase 1 default)
    - text/choices source → external_tool (mathpix)
    - answer source → human
    - solution/steps source → llm_synthesized
    """
    legacy = dict(legacy)

    def _svg_to_ref(svg: Optional[str]) -> Optional[FigureRef]:
        if not svg:
            return None
        return FigureRef(
            type="vector_svg",
            source=SourceEnum.LLM_SYNTHESIZED,
            svg_content=svg,
        )

    figure_svg_ref = _svg_to_ref(legacy.pop("figure_svg", None))
    solution_svg_ref = _svg_to_ref(legacy.pop("solution_svg", None))

    base_text_src = FieldSource(
        source=SourceEnum.EXTERNAL_TOOL, tool_name="mathpix"
    )

    return Question(
        year=legacy["year"],
        session=legacy["session"],
        subject=legacy["subject"],
        q_no=legacy.get("q_no"),  # 옵션 C: 키 누락 48건 허용
        text=legacy["text"],
        text_source=base_text_src,
        choices=legacy.get("choices", []),
        choices_source=base_text_src,
        answer=legacy["answer"],
        answer_source=FieldSource(source=SourceEnum.HUMAN),
        solution=legacy.get("solution"),
        solution_source=(
            FieldSource(source=SourceEnum.LLM_SYNTHESIZED)
            if legacy.get("solution") else None
        ),
        steps=legacy.get("steps"),
        steps_source=(
            FieldSource(source=SourceEnum.LLM_SYNTHESIZED)
            if legacy.get("steps") else None
        ),
        stem_figure=None,
        figure_svg=figure_svg_ref,
        solution_svg=solution_svg_ref,
        difficulty=legacy.get("difficulty"),
        q_type=legacy.get("q_type"),
        tag=legacy.get("tag"),  # 옵션 C: default None (다수파 str)
        quality=legacy.get("quality"),
    )


# ===== Validation =====

def validate_questions_json(path: str) -> dict:
    """
    questions.json 전체 검증. CLI 실행용 (환경 의존).
    """
    import json

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    stats = {
        "total": len(data),
        "ok": 0,
        "errors": [],
        "by_source": {},
    }

    for i, entry in enumerate(data):
        try:
            q = migrate_legacy_question(entry)
            stats["ok"] += 1
            for fname, fref in [
                ("figure_svg", q.figure_svg),
                ("solution_svg", q.solution_svg),
                ("stem_figure", q.stem_figure),
            ]:
                if fref:
                    key = f"{fname}.{fref.source.value}"
                    stats["by_source"][key] = stats["by_source"].get(key, 0) + 1
        except Exception as e:
            stats["errors"].append({
                "index": i,
                "year": entry.get("year"),
                "session": entry.get("session"),
                "q_no": entry.get("q_no"),
                "error": str(e),
            })

    return stats


if __name__ == "__main__":
    # CLI: python question.py <questions.json path>
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python question.py <questions.json path>")
        sys.exit(1)

    result = validate_questions_json(sys.argv[1])
    summary = {
        "total": result["total"],
        "ok": result["ok"],
        "errors_count": len(result["errors"]),
        "by_source": result["by_source"],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if result["errors"]:
        print("\n첫 5개 오류:")
        for err in result["errors"][:5]:
            print(f"  [{err['year']}_{err['session']}_q{err['q_no']}] {err['error']}")
