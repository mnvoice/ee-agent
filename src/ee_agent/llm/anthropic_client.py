"""Anthropic Claude API client (fallback for complex reasoning)."""
import logging
import os

from ee_agent.llm.base import LLMClient, LLMResponse

logger = logging.getLogger(__name__)

try:
    import anthropic

    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


class AnthropicClient(LLMClient):
    """
    Anthropic Claude API client.
    Used as fallback when Ollama is unavailable or for complex reasoning.
    Default model: claude-sonnet-4-6
    """

    DEFAULT_MODEL = "claude-sonnet-4-6"

    def __init__(self, api_key: str | None = None, model: str = DEFAULT_MODEL):
        self._model = model
        if ANTHROPIC_AVAILABLE:
            self._client = anthropic.AsyncAnthropic(
                api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            self._client = None
            logger.warning("anthropic package not installed. AnthropicClient disabled.")

    @property
    def model_name(self) -> str:
        return self._model

    async def complete(
        self, prompt: str, system: str = "", max_tokens: int = 2048
    ) -> LLMResponse:
        if not ANTHROPIC_AVAILABLE or self._client is None:
            raise RuntimeError(
                "Anthropic client not available. Install 'anthropic' package."
            )

        messages = [{"role": "user", "content": prompt}]
        kwargs: dict = {
            "model": self._model,
            "max_tokens": max_tokens,
            "messages": messages,
            "temperature": 0,  # deterministic output for exam solving
        }
        if system:
            kwargs["system"] = system

        response = await self._client.messages.create(**kwargs)
        content = response.content[0].text if response.content else ""
        return LLMResponse(
            content=content,
            model=self._model,
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
            finish_reason=response.stop_reason or "stop",
        )

    async def is_available(self) -> bool:
        if not ANTHROPIC_AVAILABLE or self._client is None:
            return False
        return True
