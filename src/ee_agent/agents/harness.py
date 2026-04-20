"""4-Agent sequential harness orchestrator with Vision-Solve branch."""
from __future__ import annotations

import asyncio
import io
import logging
from typing import Callable

from ee_agent.agents.base import AgentInput, AgentOutput
from ee_agent.agents.logic_solver import LogicFirstPrinciplesSolver
from ee_agent.agents.memory_sync import MemoryKnowledgeSync
from ee_agent.agents.verifier import VerifierGatekeeper
from ee_agent.agents.vision_analyst import VisionTopologyAnalyst
from ee_agent.agents.vision_solver import VisionSolver, needs_vision
from ee_agent.domain.models.question import Question

logger = logging.getLogger(__name__)


class PageCache:
    """Caches rendered page JPEGs so the same page isn't rasterised twice."""

    def __init__(self, pdf_path: str | None = None):
        self._pdf_path = pdf_path
        self._cache: dict[int, bytes] = {}

    def get_page(self, page_num: int) -> bytes | None:
        if not self._pdf_path or not page_num:
            return None
        if page_num in self._cache:
            return self._cache[page_num]
        try:
            import pdfplumber
            from PIL import Image

            with pdfplumber.open(self._pdf_path) as pdf:
                page = pdf.pages[page_num - 1]
                pil_img = page.to_image(resolution=150).original
                w, h = pil_img.size
                if max(w, h) > 1990:
                    ratio = 1990 / max(w, h)
                    pil_img = pil_img.resize(
                        (int(w * ratio), int(h * ratio)), Image.LANCZOS
                    )
                buf = io.BytesIO()
                pil_img.convert("RGB").save(buf, format="JPEG", quality=85)
                jpeg = buf.getvalue()
            self._cache[page_num] = jpeg
            logger.debug("PageCache: rendered page %d (%d bytes)", page_num, len(jpeg))
            return jpeg
        except Exception as exc:
            logger.warning("PageCache: failed to render page %d: %s", page_num, exc)
            return None


class EEAgentHarness:
    """
    Sequential orchestrator with optional Vision-Solve branch.

    Normal flow:  Vision Analyst → Solver → Verifier → Memory
    Vision flow:  VisionSolver (reads page image) → Verifier → Memory

    The Vision flow is taken when needs_vision(question) is True,
    meaning pdfplumber could not fully extract the stem or choices.
    """

    def __init__(
        self,
        vision: VisionTopologyAnalyst,
        solver: LogicFirstPrinciplesSolver,
        verifier: VerifierGatekeeper,
        memory: MemoryKnowledgeSync,
        vision_solver: VisionSolver | None = None,
        page_cache: PageCache | None = None,
    ):
        self.vision = vision
        self.solver = solver
        self.verifier = verifier
        self.memory = memory
        self.vision_solver = vision_solver
        self.page_cache = page_cache or PageCache()
        self._agents = [vision, solver, verifier, memory]

    async def process_question(self, question: Question) -> dict:
        """
        Process a single question through the appropriate agent path.
        """
        context = self._build_initial_context(question)
        context["question_number"] = question.question_number
        outputs: list[AgentOutput] = []
        agent_names: list[str] = []

        use_vision = (
            self.vision_solver is not None
            and needs_vision(question)
        )

        if use_vision:
            # ── Vision-Solve path ──────────────────────────────
            page_jpeg = self.page_cache.get_page(
                getattr(question, "source_page", None) or 0
            )
            context["page_jpeg"] = page_jpeg

            out_vs = await self.vision_solver.run(
                AgentInput(question_id=question.id, context=context)
            )
            outputs.append(out_vs)
            agent_names.append(self.vision_solver.name)

            if out_vs.succeeded and out_vs.result.get("selected_choice"):
                context["solver_result"] = out_vs.result
                logger.info(
                    "Q%d: Vision-Solve path (choice=%s, conf=%.2f)",
                    question.question_number,
                    out_vs.result.get("selected_choice"),
                    out_vs.confidence,
                )
            else:
                # Vision failed → fall through to normal solver
                logger.info(
                    "Q%d: Vision-Solve failed, falling back to text solver",
                    question.question_number,
                )
                use_vision = False

        if not use_vision:
            # ── Normal text path ───────────────────────────────
            out1 = await self.vision.run(
                AgentInput(question_id=question.id, context=context)
            )
            outputs.append(out1)
            agent_names.append(self.vision.name)
            if out1.succeeded:
                context.update(out1.result)

            out2 = await self.solver.run(
                AgentInput(question_id=question.id, context=context)
            )
            outputs.append(out2)
            agent_names.append(self.solver.name)
            if out2.succeeded:
                context["solver_result"] = out2.result

        # ── Verifier (always) ──────────────────────────────
        out3 = await self.verifier.run(
            AgentInput(question_id=question.id, context=context)
        )
        outputs.append(out3)
        agent_names.append(self.verifier.name)
        if out3.succeeded:
            context["verification"] = out3.result

        # ── Memory (always) ────────────────────────────────
        out4 = await self.memory.run(
            AgentInput(question_id=question.id, context=context)
        )
        outputs.append(out4)
        agent_names.append(self.memory.name)

        final_choice = context.get("verification", {}).get("selected_choice", 1)
        is_correct = final_choice == question.correct_answer

        return {
            "question_id": question.id,
            "question_number": question.question_number,
            "subject": question.subject.value,
            "predicted_choice": final_choice,
            "correct_choice": question.correct_answer,
            "is_correct": is_correct,
            "final_confidence": out4.confidence,
            "reasoning_traces": {
                name: o.reasoning_trace for name, o in zip(agent_names, outputs)
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
