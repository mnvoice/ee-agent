"""Seed the Neo4j knowledge graph with ontology schema and initial subjects."""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ee_agent.graph.connection import Neo4jConnection, Neo4jSettings
from ee_agent.graph.schema_manager import SchemaManager

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    settings = Neo4jSettings()
    conn = Neo4jConnection(settings)

    if not conn.verify_connectivity():
        logger.error(
            f"Cannot connect to Neo4j at {settings.neo4j_uri}. "
            "Start Neo4j first: docker compose up -d neo4j"
        )
        sys.exit(1)

    logger.info(f"Connected to Neo4j at {settings.neo4j_uri}")
    manager = SchemaManager(conn)

    logger.info("Initializing schema (constraints + indexes)...")
    manager.initialize_schema()

    logger.info("Seeding 6 exam subjects...")
    manager.seed_subjects()

    health = manager.verify_schema()
    logger.info(f"Schema health: {health}")

    conn.close()
    logger.info("Seed complete.")


if __name__ == "__main__":
    main()
