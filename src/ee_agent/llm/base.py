"""Abstract LLM client interface."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class LLMResponse:
    content: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    finish_reason: str = "stop"

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens


class LLMClient(ABC):
    """Abstract interface for LLM backends (Ollama, Anthropic)."""

    @abstractmethod
    async def complete(self, prompt: str, system: str = "", max_tokens: int = 2048) -> LLMResponse:
        """Generate a completion for the given prompt."""
        ...

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if the LLM backend is reachable."""
        ...

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Return the model identifier."""
        ...
