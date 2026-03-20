import pytest
from pydantic import ValidationError

from ee_agent.domain.models.question import (
    Choice,
    DifficultyLevel,
    ParsedQuestionBatch,
    Question,
    QuestionImage,
    QuestionType,
    Subject,
)
from ee_agent.domain.models.knowledge import (
    Concept,
    Formula,
    GraphEdge,
    GraphNode,
    Regulation,
    RelationType,
)


# ---------------------------------------------------------------------------
# Helper factories
# ---------------------------------------------------------------------------

def make_choices(correct_index: int = 2) -> list[dict]:
    """Return a valid list of 4 choice dicts."""
    return [
        {"index": i, "text": f"선택지 {i}", "is_correct": (i == correct_index)}
        for i in range(1, 5)
    ]


def make_question(**overrides) -> dict:
    """Return a valid question dict, optionally overriding fields."""
    base = {
        "year": 2023,
        "exam_session": 1,
        "question_number": 1,
        "subject": "전기이론",
        "question_type": "계산형",
        "difficulty": "중",
        "stem": "저항 R=10Ω인 회로에 전압 V=100V를 인가할 때 전류 I는?",
        "choices": make_choices(correct_index=2),
        "correct_answer": 2,
        "explanation": "I = V/R = 100/10 = 10A",
        "tags": ["옴의 법칙"],
        "source_page": 1,
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Choice model tests
# ---------------------------------------------------------------------------

class TestChoice:
    def test_valid_choice(self):
        choice = Choice(index=1, text="선택지 1", is_correct=False)
        assert choice.index == 1
        assert choice.text == "선택지 1"
        assert choice.is_correct is False

    def test_default_is_correct_false(self):
        choice = Choice(index=3, text="some text")
        assert choice.is_correct is False

    @pytest.mark.parametrize("bad_index", [0, 5, -1, 10])
    def test_index_out_of_range_raises(self, bad_index):
        with pytest.raises(ValidationError) as exc_info:
            Choice(index=bad_index, text="bad")
        assert "Choice index must be between 1 and 4" in str(exc_info.value)

    @pytest.mark.parametrize("valid_index", [1, 2, 3, 4])
    def test_valid_index_range(self, valid_index):
        choice = Choice(index=valid_index, text="text")
        assert choice.index == valid_index


# ---------------------------------------------------------------------------
# Question model tests
# ---------------------------------------------------------------------------

class TestQuestion:
    def test_valid_question_creation(self):
        q = Question(**make_question())
        assert q.year == 2023
        assert q.subject == Subject.ELECTRICAL_THEORY
        assert q.question_type == QuestionType.CALCULATION
        assert len(q.choices) == 4
        assert q.correct_answer == 2

    def test_auto_generates_uuid(self):
        q1 = Question(**make_question())
        q2 = Question(**make_question())
        assert q1.id != q2.id

    def test_custom_id_preserved(self):
        q = Question(**make_question(id="custom-id-123"))
        assert q.id == "custom-id-123"

    def test_default_difficulty_is_medium(self):
        data = make_question()
        del data["difficulty"]
        q = Question(**data)
        assert q.difficulty == DifficultyLevel.MEDIUM

    # --- Validator: must_have_four_choices ---

    def test_five_choices_raises(self):
        data = make_question()
        data["choices"] = make_choices() + [{"index": 4, "text": "extra", "is_correct": False}]
        # choices list now has 5 elements (but index 4 appears twice – still 5 items)
        data["choices"] = [
            {"index": 1, "text": "a", "is_correct": False},
            {"index": 2, "text": "b", "is_correct": True},
            {"index": 3, "text": "c", "is_correct": False},
            {"index": 4, "text": "d", "is_correct": False},
            {"index": 4, "text": "e", "is_correct": False},
        ]
        with pytest.raises(ValidationError) as exc_info:
            Question(**data)
        assert "4지선다" in str(exc_info.value)

    def test_three_choices_raises(self):
        data = make_question()
        data["choices"] = [
            {"index": 1, "text": "a", "is_correct": False},
            {"index": 2, "text": "b", "is_correct": True},
            {"index": 3, "text": "c", "is_correct": False},
        ]
        with pytest.raises(ValidationError) as exc_info:
            Question(**data)
        assert "4지선다" in str(exc_info.value)

    def test_empty_choices_raises(self):
        data = make_question(choices=[])
        with pytest.raises(ValidationError):
            Question(**data)

    # --- Validator: answer_in_range ---

    @pytest.mark.parametrize("bad_answer", [0, 5, -1, 99])
    def test_correct_answer_out_of_range_raises(self, bad_answer):
        data = make_question(correct_answer=bad_answer)
        with pytest.raises(ValidationError) as exc_info:
            Question(**data)
        assert "1-4 사이" in str(exc_info.value)

    @pytest.mark.parametrize("valid_answer", [1, 2, 3, 4])
    def test_valid_correct_answer(self, valid_answer):
        q = Question(**make_question(correct_answer=valid_answer))
        assert q.correct_answer == valid_answer

    # --- has_image property ---

    def test_has_image_false_when_no_images(self):
        q = Question(**make_question())
        assert q.has_image is False

    def test_has_image_true_when_images_present(self):
        data = make_question()
        data["images"] = [
            {
                "page": 1,
                "bbox": (0.0, 0.0, 100.0, 100.0),
                "image_type": "circuit_diagram",
            }
        ]
        q = Question(**data)
        assert q.has_image is True

    # --- correct_choice property ---

    def test_correct_choice_returns_matching_choice(self):
        q = Question(**make_question(correct_answer=3))
        cc = q.correct_choice
        assert cc is not None
        assert cc.index == 3

    def test_correct_choice_returns_none_when_no_match(self):
        """Edge case: correct_answer index not present in choices list."""
        data = make_question()
        # Manually build choices without index 2 to force mismatch
        data["choices"] = [
            {"index": 1, "text": "a", "is_correct": False},
            {"index": 1, "text": "b", "is_correct": False},  # duplicate index 1
            {"index": 3, "text": "c", "is_correct": False},
            {"index": 4, "text": "d", "is_correct": False},
        ]
        data["correct_answer"] = 2
        # ValidationError not expected here because choices count is 4
        q = Question(**data)
        assert q.correct_choice is None

    # --- Subject enum ---

    def test_all_subjects_valid(self):
        subjects = [
            "전기이론", "전기기기", "전력공학",
            "제어공학", "전기설비기술기준", "회로이론"
        ]
        for subj in subjects:
            data = make_question(subject=subj)
            q = Question(**data)
            assert q.subject.value == subj

    def test_invalid_subject_raises(self):
        data = make_question(subject="불법과목")
        with pytest.raises(ValidationError):
            Question(**data)

    # --- QuestionType enum ---

    def test_all_question_types_valid(self):
        types = ["객관식", "계산형", "도면분석", "법규형"]
        for qt in types:
            data = make_question(question_type=qt)
            q = Question(**data)
            assert q.question_type.value == qt

    # --- Optional fields ---

    def test_optional_explanation_defaults_none(self):
        data = make_question()
        del data["explanation"]
        q = Question(**data)
        assert q.explanation is None

    def test_tags_default_empty(self):
        data = make_question()
        del data["tags"]
        q = Question(**data)
        assert q.tags == []


# ---------------------------------------------------------------------------
# ParsedQuestionBatch model tests
# ---------------------------------------------------------------------------

class TestParsedQuestionBatch:
    def test_valid_batch_creation(self):
        q = Question(**make_question())
        batch = ParsedQuestionBatch(
            source_file="test_2023",
            year=2023,
            total_count=1,
            questions=[q],
        )
        assert batch.source_file == "test_2023"
        assert batch.year == 2023
        assert batch.total_count == 1
        assert len(batch.questions) == 1

    def test_parse_errors_default_empty(self):
        batch = ParsedQuestionBatch(
            source_file="test",
            year=2023,
            total_count=0,
            questions=[],
        )
        assert batch.parse_errors == []

    def test_batch_with_parse_errors(self):
        batch = ParsedQuestionBatch(
            source_file="test",
            year=2023,
            total_count=0,
            questions=[],
            parse_errors=[{"page": 5, "error": "parse failed"}],
        )
        assert len(batch.parse_errors) == 1
        assert batch.parse_errors[0]["page"] == 5


# ---------------------------------------------------------------------------
# Concept model tests
# ---------------------------------------------------------------------------

class TestConcept:
    def test_valid_concept(self):
        c = Concept(
            name="옴의 법칙",
            definition="전압 V = 전류 I × 저항 R의 관계를 나타내는 법칙",
            subject="전기이론",
        )
        assert c.name == "옴의 법칙"
        assert c.subject == "전기이론"

    def test_auto_generates_uuid(self):
        c1 = Concept(name="A", definition="def A", subject="전기이론")
        c2 = Concept(name="B", definition="def B", subject="전기이론")
        assert c1.id != c2.id

    def test_default_lists_empty(self):
        c = Concept(name="A", definition="def", subject="전기이론")
        assert c.related_formulas == []
        assert c.korean_terms == []

    def test_concept_with_related_formulas(self):
        c = Concept(
            name="임피던스",
            definition="교류회로에서 전류 흐름을 방해하는 복소 저항",
            subject="회로이론",
            related_formulas=["Z = R + jX", "|Z| = sqrt(R² + X²)"],
            korean_terms=["임피던스", "복소저항"],
        )
        assert len(c.related_formulas) == 2
        assert "임피던스" in c.korean_terms


# ---------------------------------------------------------------------------
# Formula model tests
# ---------------------------------------------------------------------------

class TestFormula:
    def test_valid_formula(self):
        f = Formula(
            name="옴의 법칙",
            latex="V = IR",
            description="전압 = 전류 × 저항",
            variables={"V": "전압 [V]", "I": "전류 [A]", "R": "저항 [Ω]"},
            applicable_subjects=["전기이론", "회로이론"],
        )
        assert f.name == "옴의 법칙"
        assert f.latex == "V = IR"
        assert len(f.applicable_subjects) == 2

    def test_auto_generates_uuid(self):
        f1 = Formula(name="F1", latex="a=b", description="test")
        f2 = Formula(name="F2", latex="c=d", description="test")
        assert f1.id != f2.id

    def test_default_variables_empty(self):
        f = Formula(name="F", latex="P=VI", description="전력")
        assert f.variables == {}


# ---------------------------------------------------------------------------
# Regulation model tests
# ---------------------------------------------------------------------------

class TestRegulation:
    def test_valid_regulation(self):
        r = Regulation(
            article="제175조",
            content="저압 옥내배선의 전선은 단면적 1.5mm² 이상의 연동선을 사용하여야 한다.",
            keywords=["저압배선", "연동선", "단면적"],
        )
        assert r.article == "제175조"
        assert len(r.keywords) == 3

    def test_auto_generates_uuid(self):
        r1 = Regulation(article="제1조", content="내용1")
        r2 = Regulation(article="제2조", content="내용2")
        assert r1.id != r2.id

    def test_default_keywords_empty(self):
        r = Regulation(article="제1조", content="내용")
        assert r.keywords == []


# ---------------------------------------------------------------------------
# GraphNode and GraphEdge tests
# ---------------------------------------------------------------------------

class TestGraphNode:
    def test_valid_graph_node(self):
        node = GraphNode(
            node_id="node-001",
            label="Concept",
            properties={"name": "옴의 법칙", "subject": "전기이론"},
        )
        assert node.node_id == "node-001"
        assert node.label == "Concept"
        assert node.properties["name"] == "옴의 법칙"


class TestGraphEdge:
    def test_valid_graph_edge(self):
        edge = GraphEdge(
            source_id="q-001",
            target_id="c-001",
            relation_type="REQUIRES",
        )
        assert edge.source_id == "q-001"
        assert edge.target_id == "c-001"
        assert edge.relation_type == "REQUIRES"

    def test_default_properties_empty(self):
        edge = GraphEdge(source_id="a", target_id="b", relation_type="APPLIES")
        assert edge.properties == {}

    def test_edge_with_properties(self):
        edge = GraphEdge(
            source_id="q-001",
            target_id="f-001",
            relation_type="APPLIES",
            properties={"weight": 0.9, "confidence": "high"},
        )
        assert edge.properties["weight"] == 0.9


# ---------------------------------------------------------------------------
# RelationType constants tests
# ---------------------------------------------------------------------------

class TestRelationType:
    def test_all_constants_defined(self):
        assert RelationType.REQUIRES == "REQUIRES"
        assert RelationType.APPLIES == "APPLIES"
        assert RelationType.REFERENCES == "REFERENCES"
        assert RelationType.BELONGS_TO == "BELONGS_TO"
        assert RelationType.DEPENDS_ON == "DEPENDS_ON"
        assert RelationType.HAS_TOPOLOGY == "HAS_TOPOLOGY"

    def test_constants_are_strings(self):
        for attr in ["REQUIRES", "APPLIES", "REFERENCES", "BELONGS_TO", "DEPENDS_ON", "HAS_TOPOLOGY"]:
            assert isinstance(getattr(RelationType, attr), str)


# ---------------------------------------------------------------------------
# QuestionImage tests
# ---------------------------------------------------------------------------

class TestQuestionImage:
    def test_valid_question_image(self):
        img = QuestionImage(
            page=5,
            bbox=(10.0, 20.0, 200.0, 150.0),
            image_type="circuit_diagram",
        )
        assert img.page == 5
        assert img.image_type == "circuit_diagram"
        assert img.base64_data is None

    def test_with_base64_data(self):
        img = QuestionImage(
            page=1,
            bbox=(0.0, 0.0, 100.0, 100.0),
            image_type="graph",
            base64_data="base64encodedstring==",
        )
        assert img.base64_data == "base64encodedstring=="
