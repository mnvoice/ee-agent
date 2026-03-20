"""Agent 4: Memory & Knowledge Sync."""
import logging

from ee_agent.agents.base import AgentInput, AgentOutput, BaseAgent

logger = logging.getLogger(__name__)

# LaTeX formula lookup for common Korean EE laws
_LATEX_MAP = {
    "옴의 법칙": "V = IR",
    "전력": "P = VI",
    "키르히호프 전압 법칙": r"\sum V = 0",
    "키르히호프 전류 법칙": r"\sum I = 0",
    "3상 전력": r"P = \sqrt{3} V_L I_L \cos\phi",
    "패러데이 법칙": r"e = -N\frac{d\Phi}{dt}",
    "렌츠 법칙": r"e = -\frac{d\Phi}{dt}",
}


class MemoryKnowledgeSync(BaseAgent):
    """
    Agent 4: Memory & Knowledge Sync
    Strategy: GMM Dynamic Top-K + Graph Sync

    Responsibilities:
    - Extract structured knowledge from solved problems
    - Sync concepts/formulas to RAG vector store (GMMDynamicRetriever)
    - Stub for Neo4j graph sync (activated when graph_repo provided)
    """

    def __init__(self, retriever=None, graph_repo=None, config: dict | None = None):
        super().__init__(config)
        self.retriever = retriever
        self.graph_repo = graph_repo

    @property
    def name(self) -> str:
        return "memory_sync"

    async def run(self, input_data: AgentInput) -> AgentOutput:
        trace: list[str] = []
        stem = input_data.context.get("stem", "")
        subject = input_data.context.get("subject", "unknown")
        solver_result = input_data.context.get("solver_result", {})
        verification = input_data.context.get("verification", {})

        knowledge = self._extract_knowledge(stem, subject, solver_result, trace)

        if self.retriever:
            self._sync_to_retriever(knowledge, trace)
        else:
            trace.append("Retriever not configured — skipping vector store sync")

        if self.graph_repo:
            trace.append("Neo4j sync: placeholder (activate when Neo4j is running)")
        else:
            trace.append("Graph repo not configured — skipping Neo4j sync")

        selected = verification.get("selected_choice", 1)
        confidence = verification.get("confidence", 0.0)
        trace.append(f"Final answer: choice {selected} (confidence={confidence:.2f})")

        return AgentOutput(
            agent_name=self.name,
            question_id=input_data.question_id,
            result={
                "final_answer_choice": selected,
                "final_confidence": confidence,
                "knowledge_synced": len(knowledge.get("concepts", [])),
                "knowledge": knowledge,
            },
            confidence=confidence,
            reasoning_trace=trace,
        )

    def _extract_knowledge(
        self, stem: str, subject: str, solver_result: dict, trace: list[str]
    ) -> dict:
        """Extract structured knowledge from problem and solution."""
        law = solver_result.get("law_used", "")
        concepts = []
        if law and law != "unknown":
            concepts.append({"name": law, "definition": f"Applied in: {stem[:80]}"})
            trace.append(f"Extracted concept: {law}")

        formula: dict = {}
        if law and law != "unknown":
            formula = {
                "name": law,
                "latex": self._infer_latex(law),
                "description": f"Used to solve: {stem[:60]}",
            }

        trace.append(f"Knowledge: {len(concepts)} concept(s), formula={'yes' if formula else 'no'}")
        return {"concepts": concepts, "formula": formula, "subject": subject}

    def _sync_to_retriever(self, knowledge: dict, trace: list[str]) -> None:
        """Update RAG vector store with extracted knowledge."""
        synced = 0
        for concept in knowledge.get("concepts", []):
            name = concept.get("name", "")
            if name and name != "unknown":
                self.retriever.add_concept(
                    name=name,
                    definition=concept.get("definition", ""),
                    subject=knowledge.get("subject", ""),
                )
                synced += 1

        formula = knowledge.get("formula", {})
        fname = formula.get("name", "")
        if fname and fname != "unknown":
            self.retriever.add_formula(
                name=fname,
                latex=formula.get("latex", ""),
                description=formula.get("description", ""),
            )
            synced += 1

        trace.append(f"Vector store: synced {synced} item(s)")

    @staticmethod
    def _infer_latex(law_name: str) -> str:
        """Map Korean law name to LaTeX formula. Prefers exact match, then longest partial."""
        # Exact match first
        if law_name in _LATEX_MAP:
            return _LATEX_MAP[law_name]
        # Partial match — prefer the longest matching key to avoid false substring matches
        best_key: str | None = None
        for key in _LATEX_MAP:
            if key in law_name or law_name in key:
                if best_key is None or len(key) > len(best_key):
                    best_key = key
        return _LATEX_MAP[best_key] if best_key else law_name
