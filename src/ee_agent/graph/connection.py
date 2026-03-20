"""Neo4j connection management with async context manager support."""
import os
from contextlib import asynccontextmanager, contextmanager
from typing import AsyncGenerator, Generator

from neo4j import AsyncGraphDatabase, GraphDatabase, AsyncDriver, Driver
from pydantic_settings import BaseSettings, SettingsConfigDict


class Neo4jSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "ee_agent_password"
    neo4j_database: str = "neo4j"


class Neo4jConnection:
    """
    Manages Neo4j driver lifecycle.
    Supports both sync and async usage.
    """

    def __init__(self, settings: Neo4jSettings | None = None):
        self.settings = settings or Neo4jSettings()
        self._driver: Driver | None = None
        self._async_driver: AsyncDriver | None = None

    def get_driver(self) -> Driver:
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self.settings.neo4j_uri,
                auth=(self.settings.neo4j_user, self.settings.neo4j_password),
            )
        return self._driver

    def get_async_driver(self) -> AsyncDriver:
        if self._async_driver is None:
            self._async_driver = AsyncGraphDatabase.driver(
                self.settings.neo4j_uri,
                auth=(self.settings.neo4j_user, self.settings.neo4j_password),
            )
        return self._async_driver

    @contextmanager
    def session(self) -> Generator:
        driver = self.get_driver()
        with driver.session(database=self.settings.neo4j_database) as session:
            yield session

    @asynccontextmanager
    async def async_session(self) -> AsyncGenerator:
        driver = self.get_async_driver()
        async with driver.session(database=self.settings.neo4j_database) as session:
            yield session

    def close(self) -> None:
        if self._driver:
            self._driver.close()
            self._driver = None

    async def aclose(self) -> None:
        if self._async_driver:
            await self._async_driver.close()
            self._async_driver = None

    def verify_connectivity(self) -> bool:
        try:
            driver = self.get_driver()
            driver.verify_connectivity()
            return True
        except Exception:
            return False
