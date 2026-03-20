"""Neo4j schema initialization - constraints, indexes, seed subjects."""
import logging

from ee_agent.graph.connection import Neo4jConnection
from ee_agent.graph.queries import CypherQueries

logger = logging.getLogger(__name__)


class SchemaManager:
    def __init__(self, connection: Neo4jConnection):
        self.conn = connection

    def initialize_schema(self) -> None:
        """Create all constraints and indexes."""
        constraints = [
            CypherQueries.CREATE_PROBLEM_CONSTRAINT,
            CypherQueries.CREATE_CONCEPT_CONSTRAINT,
            CypherQueries.CREATE_FORMULA_CONSTRAINT,
            CypherQueries.CREATE_REGULATION_CONSTRAINT,
            CypherQueries.CREATE_SUBJECT_CONSTRAINT,
        ]
        indexes = [
            CypherQueries.CREATE_PROBLEM_FULLTEXT,
            CypherQueries.CREATE_CONCEPT_FULLTEXT,
        ]
        with self.conn.session() as session:
            for query in constraints:
                try:
                    session.run(query)
                    logger.debug(f"Created constraint: {query[:50]}...")
                except Exception as e:
                    logger.warning(f"Constraint already exists or error: {e}")

            for query in indexes:
                try:
                    session.run(query)
                    logger.debug(f"Created index: {query[:50]}...")
                except Exception as e:
                    logger.warning(f"Index already exists or error: {e}")

    def seed_subjects(self) -> None:
        """Seed the 6 exam subjects."""
        from ee_agent.domain.models.question import Subject

        with self.conn.session() as session:
            for subject in Subject:
                session.run(CypherQueries.MERGE_SUBJECT, name=subject.value)
        logger.info("Seeded 6 subjects into Neo4j")

    def verify_schema(self) -> dict:
        """Return schema health check results."""
        with self.conn.session() as session:
            constraints = session.run("SHOW CONSTRAINTS").data()
            indexes = session.run("SHOW INDEXES").data()
            return {
                "constraints": len(constraints),
                "indexes": len(indexes),
                "healthy": len(constraints) >= 5,
            }
