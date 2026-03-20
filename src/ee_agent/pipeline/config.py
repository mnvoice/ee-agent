"""Pipeline configuration via environment variables."""
from pydantic_settings import BaseSettings


class PipelineConfig(BaseSettings):
    # LLM
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    anthropic_api_key: str = ""

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "ee_agent_password"
    neo4j_database: str = "neo4j"

    # Processing
    batch_size: int = 10
    max_concurrent: int = 5
    log_level: str = "INFO"

    model_config = {"env_file": ".env", "extra": "ignore"}
