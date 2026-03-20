"""Repository classes for Neo4j graph operations."""
import logging
from typing import Any

from ee_agent.domain.models.knowledge import Concept
from ee_agent.domain.models.question import Question
from ee_agent.graph.connection import Neo4jConnection
from ee_agent.graph.queries import CypherQueries

logger = logging.getLogger(__name__)


class ProblemRepository:
    """Repository for Problem nodes in Neo4j."""

    def __init__(self, connection: Neo4jConnection):
        self.conn = connection

    def upsert(self, question: Question) -> str:
        """Save a Question to Neo4j and return its id."""
        with self.conn.session() as session:
            session.run(
                CypherQueries.MERGE_PROBLEM,
                id=question.id,
                year=question.year,
                exam_session=question.exam_session,
                question_number=question.question_number,
                subject=question.subject.value,
                question_type=question.question_type.value,
                difficulty=question.difficulty.value,
                stem=question.stem,
                correct_answer=question.correct_answer,
                explanation=question.explanation or "",
                tags=question.tags,
                has_image=question.has_image,
            )
        return question.id

    def get_by_id(self, id: str) -> dict[str, Any] | None:
        """Retrieve a problem node by id, including related concepts, formulas, and subject."""
        with self.conn.session() as session:
            result = session.run(CypherQueries.GET_PROBLEM_BY_ID, id=id)
            record = result.single()
            if record is None:
                return None
            node = record["p"]
            return {
                **dict(node),
                "concepts": record["concepts"],
                "formulas": record["formulas"],
                "subject": record["subject"],
            }

    def get_all_by_subject(self, subject: str) -> list[dict[str, Any]]:
        """Return all problems belonging to a given subject."""
        query = """
            MATCH (p:Problem)-[:BELONGS_TO]->(s:Subject {name: $subject})
            RETURN p
            ORDER BY p.year DESC, p.question_number ASC
        """
        with self.conn.session() as session:
            result = session.run(query, subject=subject)
            return [dict(record["p"]) for record in result]

    def count(self) -> int:
        """Return total number of Problem nodes."""
        query = "MATCH (p:Problem) RETURN count(p) AS cnt"
        with self.conn.session() as session:
            result = session.run(query)
            record = result.single()
            return record["cnt"] if record else 0


class ConceptRepository:
    """Repository for Concept nodes in Neo4j."""

    def __init__(self, connection: Neo4jConnection):
        self.conn = connection

    def upsert(self, concept: Concept) -> str:
        """Save a Concept to Neo4j and return its id."""
        with self.conn.session() as session:
            session.run(
                CypherQueries.MERGE_CONCEPT,
                id=concept.id,
                name=concept.name,
                definition=concept.definition,
                subject=concept.subject,
                korean_terms=concept.korean_terms,
            )
        return concept.id

    def get_by_name(self, name: str) -> dict[str, Any] | None:
        """Retrieve a concept by its name."""
        query = "MATCH (c:Concept {name: $name}) RETURN c"
        with self.conn.session() as session:
            result = session.run(query, name=name)
            record = result.single()
            if record is None:
                return None
            return dict(record["c"])

    def get_all(self) -> list[dict[str, Any]]:
        """Return all Concept nodes."""
        query = "MATCH (c:Concept) RETURN c ORDER BY c.name ASC"
        with self.conn.session() as session:
            result = session.run(query)
            return [dict(record["c"]) for record in result]


class RelationRepository:
    """Repository for creating relationships between nodes in Neo4j."""

    def __init__(self, connection: Neo4jConnection):
        self.conn = connection

    def link_problem_to_subject(self, problem_id: str, subject_name: str) -> None:
        """Create BELONGS_TO relationship between a Problem and a Subject."""
        with self.conn.session() as session:
            session.run(
                CypherQueries.LINK_PROBLEM_SUBJECT,
                problem_id=problem_id,
                subject_name=subject_name,
            )

    def link_problem_to_concept(self, problem_id: str, concept_name: str) -> None:
        """Create REQUIRES relationship between a Problem and a Concept."""
        with self.conn.session() as session:
            session.run(
                CypherQueries.LINK_PROBLEM_CONCEPT,
                problem_id=problem_id,
                concept_name=concept_name,
            )

    def link_problem_to_formula(self, problem_id: str, formula_id: str) -> None:
        """Create APPLIES relationship between a Problem and a Formula."""
        with self.conn.session() as session:
            session.run(
                CypherQueries.LINK_PROBLEM_FORMULA,
                problem_id=problem_id,
                formula_id=formula_id,
            )

    def link_problem_to_regulation(self, problem_id: str, article: str) -> None:
        """Create REFERENCES relationship between a Problem and a Regulation."""
        with self.conn.session() as session:
            session.run(
                CypherQueries.LINK_PROBLEM_REGULATION,
                problem_id=problem_id,
                article=article,
            )

    def link_concept_depends_on(self, concept_a: str, concept_b: str) -> None:
        """Create DEPENDS_ON relationship from concept_a to concept_b."""
        with self.conn.session() as session:
            session.run(
                CypherQueries.LINK_CONCEPT_DEPENDS,
                concept_a=concept_a,
                concept_b=concept_b,
            )
