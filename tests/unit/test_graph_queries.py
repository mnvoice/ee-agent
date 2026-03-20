"""Unit tests for CypherQueries and Neo4jSettings - no Neo4j instance required."""
import pytest

from ee_agent.domain.models.question import Subject
from ee_agent.graph.connection import Neo4jSettings
from ee_agent.graph.queries import CypherQueries


class TestCypherQueriesExistence:
    """Verify that all required query constants are present as string attributes."""

    def test_create_problem_constraint_exists(self):
        assert isinstance(CypherQueries.CREATE_PROBLEM_CONSTRAINT, str)

    def test_create_concept_constraint_exists(self):
        assert isinstance(CypherQueries.CREATE_CONCEPT_CONSTRAINT, str)

    def test_create_formula_constraint_exists(self):
        assert isinstance(CypherQueries.CREATE_FORMULA_CONSTRAINT, str)

    def test_create_regulation_constraint_exists(self):
        assert isinstance(CypherQueries.CREATE_REGULATION_CONSTRAINT, str)

    def test_create_subject_constraint_exists(self):
        assert isinstance(CypherQueries.CREATE_SUBJECT_CONSTRAINT, str)

    def test_create_problem_fulltext_exists(self):
        assert isinstance(CypherQueries.CREATE_PROBLEM_FULLTEXT, str)

    def test_create_concept_fulltext_exists(self):
        assert isinstance(CypherQueries.CREATE_CONCEPT_FULLTEXT, str)

    def test_merge_subject_exists(self):
        assert isinstance(CypherQueries.MERGE_SUBJECT, str)

    def test_merge_problem_exists(self):
        assert isinstance(CypherQueries.MERGE_PROBLEM, str)

    def test_merge_concept_exists(self):
        assert isinstance(CypherQueries.MERGE_CONCEPT, str)

    def test_merge_formula_exists(self):
        assert isinstance(CypherQueries.MERGE_FORMULA, str)

    def test_merge_regulation_exists(self):
        assert isinstance(CypherQueries.MERGE_REGULATION, str)

    def test_link_problem_subject_exists(self):
        assert isinstance(CypherQueries.LINK_PROBLEM_SUBJECT, str)

    def test_link_problem_concept_exists(self):
        assert isinstance(CypherQueries.LINK_PROBLEM_CONCEPT, str)

    def test_link_problem_formula_exists(self):
        assert isinstance(CypherQueries.LINK_PROBLEM_FORMULA, str)

    def test_link_problem_regulation_exists(self):
        assert isinstance(CypherQueries.LINK_PROBLEM_REGULATION, str)

    def test_link_concept_depends_exists(self):
        assert isinstance(CypherQueries.LINK_CONCEPT_DEPENDS, str)

    def test_get_problem_by_id_exists(self):
        assert isinstance(CypherQueries.GET_PROBLEM_BY_ID, str)

    def test_get_concepts_for_subject_exists(self):
        assert isinstance(CypherQueries.GET_CONCEPTS_FOR_SUBJECT, str)

    def test_get_problem_concept_chain_exists(self):
        assert isinstance(CypherQueries.GET_PROBLEM_CONCEPT_CHAIN, str)

    def test_get_subject_stats_exists(self):
        assert isinstance(CypherQueries.GET_SUBJECT_STATS, str)

    def test_fulltext_search_problems_exists(self):
        assert isinstance(CypherQueries.FULLTEXT_SEARCH_PROBLEMS, str)


class TestCypherQueryKeywords:
    """Verify that query strings contain expected Cypher keywords."""

    def test_constraint_queries_contain_constraint(self):
        constraint_queries = [
            CypherQueries.CREATE_PROBLEM_CONSTRAINT,
            CypherQueries.CREATE_CONCEPT_CONSTRAINT,
            CypherQueries.CREATE_FORMULA_CONSTRAINT,
            CypherQueries.CREATE_REGULATION_CONSTRAINT,
            CypherQueries.CREATE_SUBJECT_CONSTRAINT,
        ]
        for query in constraint_queries:
            assert "CONSTRAINT" in query, f"Expected CONSTRAINT in: {query[:80]}"

    def test_merge_queries_contain_merge(self):
        merge_queries = [
            CypherQueries.MERGE_SUBJECT,
            CypherQueries.MERGE_PROBLEM,
            CypherQueries.MERGE_CONCEPT,
            CypherQueries.MERGE_FORMULA,
            CypherQueries.MERGE_REGULATION,
        ]
        for query in merge_queries:
            assert "MERGE" in query, f"Expected MERGE in: {query[:80]}"

    def test_link_queries_contain_match_and_merge(self):
        link_queries = [
            CypherQueries.LINK_PROBLEM_SUBJECT,
            CypherQueries.LINK_PROBLEM_CONCEPT,
            CypherQueries.LINK_PROBLEM_FORMULA,
            CypherQueries.LINK_PROBLEM_REGULATION,
            CypherQueries.LINK_CONCEPT_DEPENDS,
        ]
        for query in link_queries:
            assert "MATCH" in query, f"Expected MATCH in: {query[:80]}"
            assert "MERGE" in query, f"Expected MERGE in: {query[:80]}"

    def test_get_problem_by_id_contains_optional_match(self):
        assert "OPTIONAL MATCH" in CypherQueries.GET_PROBLEM_BY_ID

    def test_fulltext_index_queries_contain_fulltext(self):
        assert "FULLTEXT" in CypherQueries.CREATE_PROBLEM_FULLTEXT
        assert "FULLTEXT" in CypherQueries.CREATE_CONCEPT_FULLTEXT

    def test_fulltext_search_contains_call(self):
        assert "CALL" in CypherQueries.FULLTEXT_SEARCH_PROBLEMS

    def test_merge_problem_contains_required_fields(self):
        query = CypherQueries.MERGE_PROBLEM
        required_fields = ["year", "exam_session", "question_number", "subject", "stem"]
        for field in required_fields:
            assert field in query, f"Expected field '{field}' in MERGE_PROBLEM query"

    def test_merge_concept_contains_required_fields(self):
        query = CypherQueries.MERGE_CONCEPT
        for field in ["name", "definition", "subject"]:
            assert field in query, f"Expected field '{field}' in MERGE_CONCEPT query"


class TestNeo4jSettingsDefaults:
    """Verify Neo4jSettings default values."""

    def test_default_uri(self):
        settings = Neo4jSettings()
        assert settings.neo4j_uri == "bolt://localhost:7687"

    def test_default_user(self):
        settings = Neo4jSettings()
        assert settings.neo4j_user == "neo4j"

    def test_default_password(self):
        settings = Neo4jSettings()
        assert settings.neo4j_password == "ee_agent_password"

    def test_default_database(self):
        settings = Neo4jSettings()
        assert settings.neo4j_database == "neo4j"

    def test_settings_can_be_overridden(self):
        settings = Neo4jSettings(
            neo4j_uri="bolt://remotehost:7687",
            neo4j_user="admin",
            neo4j_password="secret",
            neo4j_database="mydb",
        )
        assert settings.neo4j_uri == "bolt://remotehost:7687"
        assert settings.neo4j_user == "admin"
        assert settings.neo4j_password == "secret"
        assert settings.neo4j_database == "mydb"


class TestSubjectEnumAsQueryParams:
    """Verify that Subject enum values are valid strings suitable for Cypher parameters."""

    def test_all_subjects_are_strings(self):
        for subject in Subject:
            assert isinstance(subject.value, str)

    def test_subject_count_is_six(self):
        assert len(list(Subject)) == 6

    def test_subject_values_are_non_empty(self):
        for subject in Subject:
            assert len(subject.value) > 0

    def test_subject_values_are_korean(self):
        # All subject names should contain Korean characters
        for subject in Subject:
            has_korean = any("\uac00" <= char <= "\ud7a3" for char in subject.value)
            assert has_korean, f"Subject '{subject.value}' should contain Korean text"

    def test_known_subject_values(self):
        subject_values = {s.value for s in Subject}
        assert "전기이론" in subject_values
        assert "전기기기" in subject_values
        assert "전력공학" in subject_values
        assert "제어공학" in subject_values
        assert "전기설비기술기준" in subject_values
        assert "회로이론" in subject_values
