"""Integration tests for Neo4j schema management and repositories.

These tests require a running Neo4j instance. Mark with pytest.mark.integration
and use the neo4j_connection fixture which skips automatically when Neo4j is
unavailable.
"""
import pytest

from ee_agent.domain.models.knowledge import Concept
from ee_agent.domain.models.question import Choice, DifficultyLevel, Question, QuestionType, Subject
from ee_agent.graph.connection import Neo4jConnection
from ee_agent.graph.repository import ProblemRepository, RelationRepository
from ee_agent.graph.schema_manager import SchemaManager


pytestmark = pytest.mark.integration


def _make_question(
    subject: Subject = Subject.ELECTRICAL_THEORY,
    year: int = 2024,
    question_number: int = 1,
) -> Question:
    """Build a minimal valid Question for testing."""
    choices = [
        Choice(index=1, text="Choice A", is_correct=False),
        Choice(index=2, text="Choice B", is_correct=True),
        Choice(index=3, text="Choice C", is_correct=False),
        Choice(index=4, text="Choice D", is_correct=False),
    ]
    return Question(
        year=year,
        exam_session=1,
        question_number=question_number,
        subject=subject,
        question_type=QuestionType.MULTIPLE_CHOICE,
        difficulty=DifficultyLevel.MEDIUM,
        stem="Test question stem",
        choices=choices,
        correct_answer=2,
        explanation="Test explanation",
        tags=["test", "unit"],
    )


class TestSchemaManagerInitialize:
    def test_initialize_schema_creates_constraints(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        # Should not raise even if called multiple times (IF NOT EXISTS)
        manager.initialize_schema()
        manager.initialize_schema()

        result = manager.verify_schema()
        assert result["constraints"] >= 5

    def test_initialize_schema_creates_indexes(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()

        result = manager.verify_schema()
        # At minimum the constraint indexes plus fulltext indexes
        assert result["indexes"] >= 2


class TestSchemaManagerSeedSubjects:
    def test_seed_subjects_creates_all_six(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()
        manager.seed_subjects()

        with neo4j_connection.session() as session:
            result = session.run("MATCH (s:Subject) RETURN count(s) AS cnt")
            record = result.single()
            assert record["cnt"] >= 6

    def test_seed_subjects_is_idempotent(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()
        manager.seed_subjects()
        # Second call should not raise or create duplicates
        manager.seed_subjects()

        with neo4j_connection.session() as session:
            result = session.run("MATCH (s:Subject) RETURN count(s) AS cnt")
            record = result.single()
            assert record["cnt"] >= 6


class TestSchemaManagerVerifySchema:
    def test_verify_schema_returns_healthy_after_init(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()

        result = manager.verify_schema()
        assert result["healthy"] is True

    def test_verify_schema_returns_dict_with_expected_keys(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()

        result = manager.verify_schema()
        assert "constraints" in result
        assert "indexes" in result
        assert "healthy" in result


class TestProblemRepository:
    def test_upsert_returns_id(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()

        repo = ProblemRepository(neo4j_connection)
        question = _make_question()
        returned_id = repo.upsert(question)

        assert returned_id == question.id

    def test_get_by_id_returns_node(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()

        repo = ProblemRepository(neo4j_connection)
        question = _make_question(year=2023, question_number=5)
        repo.upsert(question)

        result = repo.get_by_id(question.id)
        assert result is not None
        assert result["id"] == question.id

    def test_get_by_id_returns_none_for_missing(self, neo4j_connection: Neo4jConnection):
        repo = ProblemRepository(neo4j_connection)
        result = repo.get_by_id("non-existent-id-12345")
        assert result is None

    def test_upsert_is_idempotent(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()

        repo = ProblemRepository(neo4j_connection)
        question = _make_question(question_number=99)
        repo.upsert(question)
        repo.upsert(question)  # Should not create a duplicate

        count_query = "MATCH (p:Problem {id: $id}) RETURN count(p) AS cnt"
        with neo4j_connection.session() as session:
            record = session.run(count_query, id=question.id).single()
            assert record["cnt"] == 1

    def test_count_reflects_inserted_problems(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()

        repo = ProblemRepository(neo4j_connection)
        before = repo.count()

        question = _make_question(year=2022, question_number=77)
        repo.upsert(question)

        after = repo.count()
        assert after >= before + 1


class TestRelationRepository:
    def test_link_problem_to_subject(self, neo4j_connection: Neo4jConnection):
        manager = SchemaManager(neo4j_connection)
        manager.initialize_schema()
        manager.seed_subjects()

        prob_repo = ProblemRepository(neo4j_connection)
        rel_repo = RelationRepository(neo4j_connection)

        question = _make_question(subject=Subject.ELECTRICAL_THEORY, question_number=10)
        prob_repo.upsert(question)

        # Should not raise
        rel_repo.link_problem_to_subject(question.id, Subject.ELECTRICAL_THEORY.value)

        # Verify relationship exists
        verify_query = """
            MATCH (p:Problem {id: $id})-[:BELONGS_TO]->(s:Subject)
            RETURN count(s) AS cnt
        """
        with neo4j_connection.session() as session:
            record = session.run(verify_query, id=question.id).single()
            assert record["cnt"] == 1
