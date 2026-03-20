"""Shared fixtures for integration tests."""
import pytest

from ee_agent.graph.connection import Neo4jConnection


@pytest.fixture
def neo4j_connection():
    """Provide a Neo4j connection, skipping if Neo4j is not available."""
    conn = Neo4jConnection()
    if not conn.verify_connectivity():
        pytest.skip("Neo4j not available")
    yield conn
    conn.close()
