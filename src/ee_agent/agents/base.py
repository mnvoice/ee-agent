"""Base agent classes for the EE-Agent 4-agent harness."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class AgentInput:
    question_id: str
    context: dict  # accumulated context from previous agents
    metadata: dict = field(default_factory=dict)


@dataclass
class AgentOutput:
    agent_name: str
    question_id: str
    result: dict
    confidence: float  # 0.0 - 1.0
    reasoning_trace: list[str]
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return self.error is None


class BaseAgent(ABC):
    """Abstract base for all 4 agents in the harness."""

    def __init__(self, config: dict | None = None):
        self.config = config or {}

    @property
    @abstractmethod
    def name(self) -> str:
        """Agent identifier."""
        ...

    @abstractmethod
    async def run(self, input_data: AgentInput) -> AgentOutput:
        """Execute the agent's main logic."""
        ...
