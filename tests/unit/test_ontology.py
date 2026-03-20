import json
import tempfile
from pathlib import Path

import pytest
from rdflib import Graph, Literal, RDF, URIRef, XSD

from ee_agent.domain.models.knowledge import Concept, Formula, Regulation
from ee_agent.domain.models.question import (
    Choice,
    DifficultyLevel,
    Question,
    QuestionType,
    Subject,
)
from ee_agent.ontology.builder import EEOntologyBuilder
from ee_agent.ontology.schema import EE, EEClass, EEProperty
from ee_agent.ontology.serializer import OntologySerializer


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_four_choices(correct: int = 2) -> list[dict]:
    return [
        {"index": i, "text": f"보기 {i}", "is_correct": (i == correct)}
        for i in range(1, 5)
    ]


def make_question(subject: str = "전기이론", **overrides) -> Question:
    data = {
        "year": 2023,
        "exam_session": 1,
        "question_number": 1,
        "subject": subject,
        "question_type": "계산형",
        "difficulty": "중",
        "stem": "옴의 법칙에 의해 I = V/R = 100/10 = 몇 A인가?",
        "choices": make_four_choices(),
        "correct_answer": 2,
    }
    data.update(overrides)
    return Question(**data)


def make_concept(**overrides) -> Concept:
    data = {
        "name": "옴의 법칙",
        "definition": "전압 V = 전류 I × 저항 R의 관계 법칙",
        "subject": "전기이론",
    }
    data.update(overrides)
    return Concept(**data)


def make_formula(**overrides) -> Formula:
    data = {
        "name": "옴의 법칙",
        "latex": "V = IR",
        "description": "전압과 전류, 저항의 관계",
    }
    data.update(overrides)
    return Formula(**data)


def make_regulation(**overrides) -> Regulation:
    data = {
        "article": "제175조",
        "content": "저압 옥내배선의 전선 규격",
        "keywords": ["저압", "배선"],
    }
    data.update(overrides)
    return Regulation(**data)


# ---------------------------------------------------------------------------
# EEOntologyBuilder — initialisation
# ---------------------------------------------------------------------------

class TestEEOntologyBuilderInit:
    def test_builder_creates_graph(self):
        builder = EEOntologyBuilder()
        assert builder.graph is not None
        assert isinstance(builder.graph, Graph)

    def test_seed_ontology_loads_subject_individuals(self):
        """Confirm the TTL file's Subject individuals are in the graph."""
        builder = EEOntologyBuilder()
        subjects = [
            EE.ElectricalTheory,
            EE.ElectricalMachines,
            EE.PowerSystems,
            EE.ControlEngineering,
            EE.ElectricalSafety,
            EE.CircuitTheory,
        ]
        for subject_uri in subjects:
            assert (subject_uri, RDF.type, EEClass.SUBJECT) in builder.graph, \
                f"Expected Subject individual {subject_uri} not found in graph"

    def test_seed_ontology_loads_classes(self):
        builder = EEOntologyBuilder()
        owl_class = URIRef("http://www.w3.org/2002/07/owl#Class")
        class_uris = [
            EEClass.PROBLEM, EEClass.CONCEPT, EEClass.FORMULA,
            EEClass.REGULATION, EEClass.SUBJECT, EEClass.DIAGRAM,
        ]
        for cls_uri in class_uris:
            assert (cls_uri, RDF.type, owl_class) in builder.graph, \
                f"Expected OWL Class {cls_uri} not found in graph"


# ---------------------------------------------------------------------------
# add_question
# ---------------------------------------------------------------------------

class TestAddQuestion:
    def test_add_question_returns_uri(self):
        builder = EEOntologyBuilder()
        q = make_question()
        uri = builder.add_question(q)
        assert isinstance(uri, URIRef)
        assert "question/" in str(uri)

    def test_add_question_creates_rdf_type_triple(self):
        builder = EEOntologyBuilder()
        q = make_question()
        uri = builder.add_question(q)
        assert (uri, RDF.type, EEClass.PROBLEM) in builder.graph

    def test_add_question_stores_question_text(self):
        builder = EEOntologyBuilder()
        q = make_question(stem="테스트 문제입니다.")
        uri = builder.add_question(q)
        texts = list(builder.graph.objects(uri, EEProperty.QUESTION_TEXT))
        assert len(texts) == 1
        assert str(texts[0]) == "테스트 문제입니다."

    def test_add_question_stores_correct_answer(self):
        builder = EEOntologyBuilder()
        q = make_question(correct_answer=3)
        uri = builder.add_question(q)
        answers = list(builder.graph.objects(uri, EEProperty.CORRECT_ANS))
        assert len(answers) == 1
        assert int(answers[0]) == 3

    def test_add_question_stores_year(self):
        builder = EEOntologyBuilder()
        q = make_question(year=2022)
        uri = builder.add_question(q)
        years = list(builder.graph.objects(uri, EEProperty.YEAR))
        assert int(years[0]) == 2022

    def test_add_question_stores_difficulty_score(self):
        builder = EEOntologyBuilder()
        q = make_question(difficulty="상")
        uri = builder.add_question(q)
        scores = list(builder.graph.objects(uri, EEProperty.DIFFICULTY))
        assert int(scores[0]) == 3  # "상" maps to 3

    def test_add_question_difficulty_easy_maps_to_1(self):
        builder = EEOntologyBuilder()
        q = make_question(difficulty="하")
        uri = builder.add_question(q)
        scores = list(builder.graph.objects(uri, EEProperty.DIFFICULTY))
        assert int(scores[0]) == 1

    def test_add_question_unique_uri_per_question(self):
        builder = EEOntologyBuilder()
        q1 = make_question()
        q2 = make_question()
        uri1 = builder.add_question(q1)
        uri2 = builder.add_question(q2)
        assert uri1 != uri2


# ---------------------------------------------------------------------------
# add_concept
# ---------------------------------------------------------------------------

class TestAddConcept:
    def test_add_concept_returns_uri(self):
        builder = EEOntologyBuilder()
        c = make_concept()
        uri = builder.add_concept(c)
        assert isinstance(uri, URIRef)
        assert "concept/" in str(uri)

    def test_add_concept_creates_rdf_type_triple(self):
        builder = EEOntologyBuilder()
        c = make_concept()
        uri = builder.add_concept(c)
        assert (uri, RDF.type, EEClass.CONCEPT) in builder.graph

    def test_add_concept_stores_name(self):
        builder = EEOntologyBuilder()
        c = make_concept(name="키르히호프 법칙")
        uri = builder.add_concept(c)
        names = list(builder.graph.objects(uri, EE.name))
        assert str(names[0]) == "키르히호프 법칙"

    def test_add_concept_stores_definition(self):
        builder = EEOntologyBuilder()
        c = make_concept(definition="전류 법칙과 전압 법칙으로 구성")
        uri = builder.add_concept(c)
        defs = list(builder.graph.objects(uri, EE.definition))
        assert str(defs[0]) == "전류 법칙과 전압 법칙으로 구성"


# ---------------------------------------------------------------------------
# add_formula
# ---------------------------------------------------------------------------

class TestAddFormula:
    def test_add_formula_returns_uri(self):
        builder = EEOntologyBuilder()
        f = make_formula()
        uri = builder.add_formula(f)
        assert isinstance(uri, URIRef)
        assert "formula/" in str(uri)

    def test_add_formula_creates_rdf_type_triple(self):
        builder = EEOntologyBuilder()
        f = make_formula()
        uri = builder.add_formula(f)
        assert (uri, RDF.type, EEClass.FORMULA) in builder.graph

    def test_add_formula_stores_latex(self):
        builder = EEOntologyBuilder()
        f = make_formula(latex=r"P = \frac{V^2}{R}")
        uri = builder.add_formula(f)
        exprs = list(builder.graph.objects(uri, EEProperty.LATEX_EXPR))
        assert r"P = \frac{V^2}{R}" in str(exprs[0])


# ---------------------------------------------------------------------------
# add_regulation
# ---------------------------------------------------------------------------

class TestAddRegulation:
    def test_add_regulation_returns_uri(self):
        builder = EEOntologyBuilder()
        r = make_regulation()
        uri = builder.add_regulation(r)
        assert isinstance(uri, URIRef)
        assert "regulation/" in str(uri)

    def test_add_regulation_creates_rdf_type_triple(self):
        builder = EEOntologyBuilder()
        r = make_regulation()
        uri = builder.add_regulation(r)
        assert (uri, RDF.type, EEClass.REGULATION) in builder.graph

    def test_add_regulation_stores_article_number(self):
        builder = EEOntologyBuilder()
        r = make_regulation(article="제331조")
        uri = builder.add_regulation(r)
        articles = list(builder.graph.objects(uri, EEProperty.ARTICLE_NUM))
        assert str(articles[0]) == "제331조"


# ---------------------------------------------------------------------------
# Linking methods
# ---------------------------------------------------------------------------

class TestLinkQuestionToConcept:
    def test_link_adds_requires_triple(self):
        builder = EEOntologyBuilder()
        q = make_question()
        c = make_concept()
        q_uri = builder.add_question(q)
        c_uri = builder.add_concept(c)
        builder.link_question_to_concept(q_uri, c_uri)
        assert (q_uri, EEProperty.REQUIRES, c_uri) in builder.graph

    def test_multiple_concepts_linked(self):
        builder = EEOntologyBuilder()
        q = make_question()
        c1 = make_concept(name="옴의 법칙")
        c2 = make_concept(name="키르히호프 법칙")
        q_uri = builder.add_question(q)
        c1_uri = builder.add_concept(c1)
        c2_uri = builder.add_concept(c2)
        builder.link_question_to_concept(q_uri, c1_uri)
        builder.link_question_to_concept(q_uri, c2_uri)
        requires = list(builder.graph.objects(q_uri, EEProperty.REQUIRES))
        assert len(requires) == 2


class TestLinkQuestionToFormula:
    def test_link_adds_applies_triple(self):
        builder = EEOntologyBuilder()
        q = make_question()
        f = make_formula()
        q_uri = builder.add_question(q)
        f_uri = builder.add_formula(f)
        builder.link_question_to_formula(q_uri, f_uri)
        assert (q_uri, EEProperty.APPLIES, f_uri) in builder.graph


class TestLinkQuestionToSubject:
    def test_link_adds_belongs_to_triple(self):
        builder = EEOntologyBuilder()
        q = make_question(subject="전력공학")
        q_uri = builder.add_question(q)
        builder.link_question_to_subject(q_uri, q.subject)
        belongs = list(builder.graph.objects(q_uri, EEProperty.BELONGS_TO))
        assert len(belongs) == 1
        assert belongs[0] == EE.PowerSystems

    @pytest.mark.parametrize("subject_str,expected_uri", [
        ("전기이론", EE.ElectricalTheory),
        ("전기기기", EE.ElectricalMachines),
        ("전력공학", EE.PowerSystems),
        ("제어공학", EE.ControlEngineering),
        ("전기설비기술기준", EE.ElectricalSafety),
        ("회로이론", EE.CircuitTheory),
    ])
    def test_all_subjects_link_correctly(self, subject_str, expected_uri):
        builder = EEOntologyBuilder()
        q = make_question(subject=subject_str)
        q_uri = builder.add_question(q)
        builder.link_question_to_subject(q_uri, q.subject)
        belongs = list(builder.graph.objects(q_uri, EEProperty.BELONGS_TO))
        assert belongs[0] == expected_uri


# ---------------------------------------------------------------------------
# serialize_turtle
# ---------------------------------------------------------------------------

class TestSerializeTurtle:
    def test_serialize_creates_file(self):
        builder = EEOntologyBuilder()
        q = make_question()
        c = make_concept()
        q_uri = builder.add_question(q)
        c_uri = builder.add_concept(c)
        builder.link_question_to_concept(q_uri, c_uri)
        builder.link_question_to_subject(q_uri, q.subject)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "output.ttl")
            builder.serialize_turtle(output_path)
            assert Path(output_path).exists()
            content = Path(output_path).read_text()
            assert "@prefix" in content
            assert "ee-agent.kr" in content

    def test_serialize_creates_parent_dirs(self):
        builder = EEOntologyBuilder()
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "nested" / "dir" / "output.ttl")
            builder.serialize_turtle(output_path)
            assert Path(output_path).exists()

    def test_serialized_file_is_parseable_turtle(self):
        builder = EEOntologyBuilder()
        q = make_question()
        c = make_concept()
        q_uri = builder.add_question(q)
        c_uri = builder.add_concept(c)
        builder.link_question_to_concept(q_uri, c_uri)
        builder.link_question_to_subject(q_uri, q.subject)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = str(Path(tmpdir) / "output.ttl")
            builder.serialize_turtle(output_path)
            # Re-parse the file to verify it is valid Turtle
            g2 = Graph()
            g2.parse(output_path, format="turtle")
            assert len(g2) > 0


# ---------------------------------------------------------------------------
# validate_owl_dl
# ---------------------------------------------------------------------------

class TestValidateOwlDl:
    def test_valid_graph_returns_no_violations(self):
        builder = EEOntologyBuilder()
        q = make_question()
        c = make_concept()
        q_uri = builder.add_question(q)
        c_uri = builder.add_concept(c)
        builder.link_question_to_concept(q_uri, c_uri)
        builder.link_question_to_subject(q_uri, q.subject)
        violations = builder.validate_owl_dl()
        assert violations == []

    def test_problem_without_subject_is_violation(self):
        builder = EEOntologyBuilder()
        q = make_question()
        c = make_concept()
        q_uri = builder.add_question(q)
        c_uri = builder.add_concept(c)
        builder.link_question_to_concept(q_uri, c_uri)
        # Deliberately NOT linking subject
        violations = builder.validate_owl_dl()
        assert len(violations) >= 1
        assert any("belongsTo" in v for v in violations)

    def test_problem_without_concept_is_violation(self):
        builder = EEOntologyBuilder()
        q = make_question()
        q_uri = builder.add_question(q)
        builder.link_question_to_subject(q_uri, q.subject)
        # Deliberately NOT linking any concept
        violations = builder.validate_owl_dl()
        assert len(violations) >= 1
        assert any("requires" in v for v in violations)

    def test_problem_with_two_subjects_is_violation(self):
        builder = EEOntologyBuilder()
        q = make_question()
        c = make_concept()
        q_uri = builder.add_question(q)
        c_uri = builder.add_concept(c)
        builder.link_question_to_concept(q_uri, c_uri)
        # Add two subjects (violates FunctionalProperty)
        builder.graph.add((q_uri, EEProperty.BELONGS_TO, EE.ElectricalTheory))
        builder.graph.add((q_uri, EEProperty.BELONGS_TO, EE.CircuitTheory))
        violations = builder.validate_owl_dl()
        assert len(violations) >= 1
        assert any("Functional" in v or "belongsTo" in v for v in violations)

    def test_multiple_violations_reported(self):
        """A problem with neither subject nor concept should yield 2 violations."""
        builder = EEOntologyBuilder()
        q = make_question()
        builder.add_question(q)
        # No linking at all
        violations = builder.validate_owl_dl()
        assert len(violations) >= 2


# ---------------------------------------------------------------------------
# OntologySerializer
# ---------------------------------------------------------------------------

class TestOntologySerializer:
    def _build_graph_with_data(self) -> Graph:
        builder = EEOntologyBuilder()
        q = make_question()
        c = make_concept()
        q_uri = builder.add_question(q)
        c_uri = builder.add_concept(c)
        builder.link_question_to_concept(q_uri, c_uri)
        builder.link_question_to_subject(q_uri, q.subject)
        return builder.graph

    def test_to_turtle_creates_file(self):
        graph = self._build_graph_with_data()
        serializer = OntologySerializer(graph)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "out.ttl")
            serializer.to_turtle(path)
            assert Path(path).exists()

    def test_to_turtle_file_is_parseable(self):
        graph = self._build_graph_with_data()
        serializer = OntologySerializer(graph)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "out.ttl")
            serializer.to_turtle(path)
            g2 = Graph()
            g2.parse(path, format="turtle")
            assert len(g2) > 0

    def test_to_json_ld_creates_file(self):
        graph = self._build_graph_with_data()
        serializer = OntologySerializer(graph)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "out.jsonld")
            serializer.to_json_ld(path)
            assert Path(path).exists()

    def test_to_json_ld_is_valid_json(self):
        graph = self._build_graph_with_data()
        serializer = OntologySerializer(graph)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "out.jsonld")
            serializer.to_json_ld(path)
            content = Path(path).read_text()
            parsed = json.loads(content)
            assert parsed is not None

    def test_to_string_returns_turtle_by_default(self):
        graph = self._build_graph_with_data()
        serializer = OntologySerializer(graph)
        result = serializer.to_string()
        assert isinstance(result, str)
        assert "@prefix" in result

    def test_to_string_json_ld_format(self):
        graph = self._build_graph_with_data()
        serializer = OntologySerializer(graph)
        result = serializer.to_string(fmt="json-ld")
        parsed = json.loads(result)
        assert parsed is not None

    def test_to_turtle_creates_parent_dirs(self):
        graph = self._build_graph_with_data()
        serializer = OntologySerializer(graph)
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(Path(tmpdir) / "nested" / "subdir" / "out.ttl")
            serializer.to_turtle(path)
            assert Path(path).exists()
