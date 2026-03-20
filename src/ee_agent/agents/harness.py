"""4-Agent sequential harness orchestrator."""
import asyncio
import logging

from ee_agent.agents.base import AgentInput, AgentOutput
from ee_agent.agents.logic_solver import LogicFirstPrinciplesSolver
from ee_agent.agents.memory_sync import MemoryKnowledgeSync
from ee_agent.agents.verifier import VerifierGatekeeper
from ee_agent.agents.vision_analyst import VisionTopologyAnalyst
from ee_agent.domain.models.question import Question

logger = logging.getLogger(__name__)


class EEAgentHarness:
    """
    4-Agent sequential orchestrator.

    Flow: Agent1 (Vision) → Agent2 (Solver) → Agent3 (Verifier) → Agent4 (Memory)

    Each agent's result is accumulated into a shared context dict.
    Full reasoning traces are preserved for interpretability.
    """

    def __init__(
        self,
        vision: VisionTopologyAnalyst,
        solver: LogicFirstPrinciplesSolver,
        verifier: VerifierGatekeeper,
        memory: MemoryKnowledgeSync,
    ):
        self.vision = vision
        self.solver = solver
        self.verifier = verifier
        self.memory = memory
        self._agents = [vision, solver, verifier, memory]

    async def process_question(self, question: Question) -> dict:
        """
        Process a single question through all 4 agents sequentially.
        Returns full result with reasoning traces for interpretability.
        """
        context = self._build_initial_context(question)
        outputs: list[AgentOutput] = []

        # Agent 1: Vision Topology Analyst
        out1 = await self.vision.run(AgentInput(question_id=question.id, context=context))
        outputs.append(out1)
        if out1.succeeded:
            context.update(out1.result)
        logger.debug(f"Agent1 done: conf={out1.confidence:.2f}")

        # Agent 2: Logic First-Principles Solver
        out2 = await self.solver.run(AgentInput(question_id=question.id, context=context))
        outputs.append(out2)
        if out2.succeeded:
            context["solver_result"] = out2.result
        logger.debug(f"Agent2 done: conf={out2.confidence:.2f}")

        # Agent 3: Verifier & Gatekeeper
        out3 = await self.verifier.run(AgentInput(question_id=question.id, context=context))
        outputs.append(out3)
        if out3.succeeded:
            context["verification"] = out3.result
        logger.debug(f"Agent3 done: conf={out3.confidence:.2f}")

        # Agent 4: Memory & Knowledge Sync
        out4 = await self.memory.run(AgentInput(question_id=question.id, context=context))
        outputs.append(out4)
        logger.debug(f"Agent4 done: conf={out4.confidence:.2f}")

        final_choice = context.get("verification", {}).get("selected_choice", 1)
        is_correct = (final_choice == question.correct_answer)

        return {
            "question_id": question.id,
            "question_number": question.question_number,
            "subject": question.subject.value,
            "predicted_choice": final_choice,
            "correct_choice": question.correct_answer,
            "is_correct": is_correct,
            "final_confidence": out4.confidence,
            "reasoning_traces": {
                a.name: o.reasoning_trace
                for a, o in zip(self._agents, outputs)
            },
            "agent_outputs": [o.result for o in outputs],
        }

    async def process_batch(
        self, questions: list[Question], max_concurrent: int = 5
    ) -> list[dict]:
        """Process multiple questions with bounded concurrency."""
        semaphore = asyncio.Semaphore(max_concurrent)

        async def _process(q: Question) -> dict:
            async with semaphore:
                try:
                    return await self.process_question(q)
                except Exception as e:
                    logger.error(f"Failed question {q.id}: {e}")
                    return {
                        "question_id": q.id,
                        "error": str(e),
                        "is_correct": False,
                        "predicted_choice": 1,
                    }

        return list(await asyncio.gather(*[_process(q) for q in questions]))

    @staticmethod
    def _build_initial_context(question: Question) -> dict:
        """Convert Question model to initial agent context dict."""
        return {
            "stem": question.stem,
            "subject": question.subject.value,
            "question_type": question.question_type.value,
            "difficulty": question.difficulty.value,
            "has_image": question.has_image,
            "choices": [
                {"index": c.index, "text": c.text, "is_correct": c.is_correct}
                for c in question.choices
            ],
            "correct_answer": question.correct_answer,
        }
