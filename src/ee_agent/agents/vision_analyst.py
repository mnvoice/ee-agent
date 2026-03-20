"""Agent 1: Vision Topology Analyst."""
import json
import logging

from ee_agent.agents.base import AgentInput, AgentOutput, BaseAgent
from ee_agent.agents.prompts.vision_prompts import (
    NO_IMAGE_RESPONSE,
    SYSTEM_PROMPT,
    TOPOLOGY_ANALYSIS_PROMPT,
)

logger = logging.getLogger(__name__)


class VisionTopologyAnalyst(BaseAgent):
    """
    Agent 1: Vision Topology Analyst
    Strategy: Lazy Discovery + MaxSim keyword detection

    Lazy Discovery: Skip LLM call when no image present — saves tokens.
    MaxSim: Match circuit keywords to detect topology from question text.
    """

    CIRCUIT_KEYWORDS = ["직렬", "병렬", "브리지", "델타", "와이", "단상", "3상", "R-L-C"]
    COMPONENTS = ["저항", "코일", "콘덴서", "변압기", "인덕터", "커패시터", "다이오드", "사이리스터"]

    def __init__(self, llm_client=None, config: dict | None = None):
        super().__init__(config)
        self.llm = llm_client

    @property
    def name(self) -> str:
        return "vision_analyst"

    async def run(self, input_data: AgentInput) -> AgentOutput:
        trace: list[str] = []
        stem = input_data.context.get("stem", "")
        has_image = input_data.context.get("has_image", False)

        if not has_image:
            trace.append("Lazy Discovery: no diagram detected, skipping LLM call")
            topology = self._text_based_topology(stem)
            trace.append(f"Text-based topology: circuit_type={topology['circuit_type']}")
            confidence = 0.75
        else:
            trace.append("Image detected, performing LLM topology analysis")
            topology = await self._analyze_with_llm(stem, trace)
            confidence = 0.9

        return AgentOutput(
            agent_name=self.name,
            question_id=input_data.question_id,
            result={"topology": topology, "has_image": has_image},
            confidence=confidence,
            reasoning_trace=trace,
        )

    def _text_based_topology(self, stem: str) -> dict:
        """Detect circuit topology from question text keywords (MaxSim)."""
        circuit_type = "unknown"
        for kw in self.CIRCUIT_KEYWORDS:
            if kw in stem:
                circuit_type = kw
                break

        components = [c for c in self.COMPONENTS if c in stem]
        phase_config = "3상" if "3상" in stem else "단상" if "단상" in stem else "unknown"

        return {
            "circuit_type": circuit_type,
            "components": components,
            "phase_config": phase_config,
            "topology_notes": "Text-based keyword detection",
        }

    async def _analyze_with_llm(self, stem: str, trace: list[str]) -> dict:
        """Use LLM for topology analysis when image is present."""
        if self.llm is None:
            trace.append("LLM not configured, falling back to text-based detection")
            return self._text_based_topology(stem)

        prompt = TOPOLOGY_ANALYSIS_PROMPT.format(stem=stem)
        try:
            response = await self.llm.complete(prompt, system=SYSTEM_PROMPT, max_tokens=512)
            result = json.loads(response.content)
            trace.append(f"LLM topology: {result.get('circuit_type')}")
            return result
        except Exception as e:
            logger.warning(f"LLM topology analysis failed: {e}")
            trace.append(f"LLM failed ({e}), using text-based fallback")
            return self._text_based_topology(stem)
