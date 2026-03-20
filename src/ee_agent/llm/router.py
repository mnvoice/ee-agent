"""LLM router — selects Ollama or Anthropic based on availability."""
import logging
from enum import Enum

from ee_agent.llm.anthropic_client import AnthropicClient
from ee_agent.llm.base import LLMClient, LLMResponse
from ee_agent.llm.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class TaskComplexity(str, Enum):
    SIMPLE = "simple"    # keyword extraction, classification
    MEDIUM = "medium"    # formula derivation, calculation
    COMPLEX = "complex"  # multi-step reasoning, diagram analysis


class LLMRouter:
    """
    Routes LLM calls to Ollama (default) or Anthropic (fallback).
    Strategy: try Ollama first; on failure fall back to Anthropic.
    """

    def __init__(
        self,
        ollama: OllamaClient,
        anthropic: AnthropicClient | None = None,
    ):
        self.ollama = ollama
        self.anthropic = anthropic
        self._ollama_available: bool | None = None

    async def route(
        self,
        prompt: str,
        system: str = "",
        complexity: TaskComplexity = TaskComplexity.MEDIUM,
        max_tokens: int = 2048,
    ) -> LLMResponse:
        """Route request to appropriate LLM backend."""
        if self._ollama_available is None:
            self._ollama_available = await self.ollama.is_available()

        if self._ollama_available:
            try:
                return await self.ollama.complete(prompt, system, max_tokens)
            except Exception as e:
                logger.warning(f"Ollama failed: {e}. Falling back to Anthropic.")
                self._ollama_available = False

        if self.anthropic and await self.anthropic.is_available():
            return await self.anthropic.complete(prompt, system, max_tokens)

        raise RuntimeError(
            "No LLM backend available. Start Ollama or set ANTHROPIC_API_KEY."
        )

    async def complete(
        self, prompt: str, system: str = "", max_tokens: int = 2048
    ) -> LLMResponse:
        """Convenience wrapper — delegates to route() with MEDIUM complexity."""
        return await self.route(prompt, system, TaskComplexity.MEDIUM, max_tokens)

    async def is_available(self) -> bool:
        """Check if any backend is reachable."""
        if await self.ollama.is_available():
            return True
        if self.anthropic:
            return await self.anthropic.is_available()
        return False

    @property
    def model_name(self) -> str:
        return self.ollama.model_name

    def get_active_client(self) -> LLMClient:
        """Return currently preferred LLM client."""
        if self._ollama_available:
            return self.ollama
        if self.anthropic:
            return self.anthropic
        return self.ollama
