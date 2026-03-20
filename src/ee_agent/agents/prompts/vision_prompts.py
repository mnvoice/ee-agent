"""Prompt templates for Agent 1: Vision Topology Analyst."""

SYSTEM_PROMPT = """You are an expert electrical engineering diagram analyzer.
Your task is to identify circuit topology from Korean electrical engineer exam diagrams.
Focus on: connection type (series/parallel/bridge), components (R, L, C, transformer),
and circuit configuration (single-phase, 3-phase, delta, wye).
Always respond in JSON format."""

TOPOLOGY_ANALYSIS_PROMPT = """Analyze the following electrical engineering exam question for circuit topology.

Question: {stem}

Identify:
1. Circuit type (series, parallel, bridge, delta, wye, etc.)
2. Key components mentioned
3. Phase configuration (single-phase, 3-phase)
4. Any implicit topology from the question text

Return JSON with keys: circuit_type, components, phase_config, topology_notes"""

NO_IMAGE_RESPONSE: dict = {
    "circuit_type": None,
    "components": [],
    "phase_config": "unknown",
    "topology_notes": "No diagram detected in question",
}
