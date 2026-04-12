from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
import uuid


class Subject(str, Enum):
    ELECTROMAGNETISM = "전기자기학"
    ELECTRICAL_MACHINES = "전기기기"
    POWER_SYSTEMS = "전력공학"
    CONTROL_ENGINEERING = "제어공학"
    ELECTRICAL_SAFETY = "전기설비기술기준"
    CIRCUIT_THEORY = "회로이론"


class QuestionType(str, Enum):
    MULTIPLE_CHOICE = "객관식"
    CALCULATION = "계산형"
    DIAGRAM_ANALYSIS = "도면분석"
    REGULATION = "법규형"


class DifficultyLevel(str, Enum):
    EASY = "하"
    MEDIUM = "중"
    HARD = "상"


class Choice(BaseModel):
    index: int
    text: str
    is_correct: bool = False

    @field_validator("index")
    @classmethod
    def index_in_range(cls, v: int) -> int:
        if not 1 <= v <= 4:
            raise ValueError("Choice index must be between 1 and 4")
        return v


class QuestionImage(BaseModel):
    page: int
    bbox: tuple[float, float, float, float]
    image_type: str  # "circuit_diagram" | "graph" | "table"
    base64_data: Optional[str] = None


class Question(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    year: int
    exam_session: int
    question_number: int
    subject: Subject
    question_type: QuestionType
    difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    stem: str
    choices: List[Choice]
    correct_answer: int
    explanation: Optional[str] = None
    images: List[QuestionImage] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    source_page: Optional[int] = None
    # @MX:NOTE: [AUTO] True when one or more choices lack extractable text and require Vision OCR.
    needs_ocr: bool = False

    @field_validator("choices")
    @classmethod
    def must_have_four_choices(cls, v: List[Choice]) -> List[Choice]:
        if len(v) != 4:
            raise ValueError("전기기사 시험은 4지선다입니다")
        return v

    @field_validator("correct_answer")
    @classmethod
    def answer_in_range(cls, v: int) -> int:
        if not 1 <= v <= 4:
            raise ValueError("정답 번호는 1-4 사이여야 합니다")
        return v

    @property
    def has_image(self) -> bool:
        return len(self.images) > 0

    @property
    def correct_choice(self) -> Optional[Choice]:
        for choice in self.choices:
            if choice.index == self.correct_answer:
                return choice
        return None


class ParsedQuestionBatch(BaseModel):
    source_file: str
    year: int
    total_count: int
    questions: List[Question]
    parse_errors: List[dict] = Field(default_factory=list)
