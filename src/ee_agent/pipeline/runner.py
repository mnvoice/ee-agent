"""Main pipeline runner — ingestion → agents → graph sync."""
import asyncio
import json
import logging
from pathlib import Path

from ee_agent.agents.harness import EEAgentHarness
from ee_agent.agents.logic_solver import LogicFirstPrinciplesSolver
from ee_agent.agents.memory_sync import MemoryKnowledgeSync
from ee_agent.agents.verifier import VerifierGatekeeper
from ee_agent.agents.vision_analyst import VisionTopologyAnalyst
from ee_agent.domain.models.question import ParsedQuestionBatch, Question
from ee_agent.llm.anthropic_client import AnthropicClient
from ee_agent.llm.claude_code_client import ClaudeCodeClient
from ee_agent.llm.ollama_client import OllamaClient
from ee_agent.llm.router import LLMRouter
from ee_agent.pipeline.config import PipelineConfig
from ee_agent.rag.tfidf_retriever import TFIDFKnowledgeRetriever

logger = logging.getLogger(__name__)


def build_harness(config: PipelineConfig, solver_backend: str = "auto") -> EEAgentHarness:
    """Assemble the 4-agent harness from configuration.

    solver_backend:
      "api"        — Anthropic API (종량제, 가장 정확)
      "pro"        — Claude Code CLI (Pro 구독 사용, 터미널 직접 실행 필요)
      "ollama"     — 로컬 Ollama (무료, 정확도 낮음)
      "auto"       — pro 가능하면 pro, 아니면 api, 아니면 ollama
    """
    ollama = OllamaClient(base_url=config.ollama_base_url, model=config.ollama_model)
    anthropic = AnthropicClient(api_key=config.anthropic_api_key) if config.anthropic_api_key else None
    claude_code = ClaudeCodeClient()
    router = LLMRouter(ollama=ollama, anthropic=anthropic)

    if solver_backend == "pro":
        solver_llm = claude_code
        logger.info("Solver: Claude Code CLI (Pro subscription)")
    elif solver_backend == "api":
        solver_llm = anthropic if anthropic else router
        logger.info("Solver: Anthropic API (pay-per-use)")
    elif solver_backend == "ollama":
        solver_llm = ollama
        logger.info("Solver: Ollama (local)")
    else:  # auto — prefer Anthropic API for stability over CLI subprocess
        if anthropic:
            solver_llm = anthropic
            logger.info("Solver: Anthropic API [auto]")
        else:
            import asyncio as _asyncio
            pro_ok = _asyncio.get_event_loop().run_until_complete(claude_code.is_available())
            if pro_ok:
                solver_llm = claude_code
                logger.info("Solver: Claude Code CLI (Pro subscription) [auto]")
            else:
                solver_llm = router
                logger.info("Solver: Ollama [auto]")

    retriever = TFIDFKnowledgeRetriever()
    store_path = "data/knowledge_store"
    if Path(store_path + ".json").exists():
        retriever.load(store_path)
        logger.info(f"Loaded knowledge store: {retriever.size()} entries")
    else:
        logger.warning("No knowledge store found. Run scripts/seed_knowledge.py first.")

    return EEAgentHarness(
        vision=VisionTopologyAnalyst(llm_client=router),
        solver=LogicFirstPrinciplesSolver(llm_client=solver_llm, retriever=retriever),
        verifier=VerifierGatekeeper(),
        memory=MemoryKnowledgeSync(retriever=retriever),
    )


async def run_from_json(
    json_path: str,
    output_path: str,
    config: PipelineConfig | None = None,
    solver_backend: str = "auto",
) -> dict:
    """
    Load questions from JSON fixture and run through the 4-agent harness.
    Returns summary statistics.
    """
    config = config or PipelineConfig()
    harness = build_harness(config, solver_backend=solver_backend)

    with open(json_path) as f:
        data = json.load(f)

    batch = ParsedQuestionBatch(**data)
    logger.info(f"Loaded {len(batch.questions)} questions from {json_path}")

    results = await harness.process_batch(
        batch.questions, max_concurrent=config.max_concurrent
    )

    # Write results
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    correct = sum(1 for r in results if r.get("is_correct", False))
    total = len(results)
    accuracy = correct / total if total > 0 else 0.0

    summary = {
        "total": total,
        "correct": correct,
        "accuracy": round(accuracy, 3),
        "output_file": output_path,
    }
    logger.info(f"Pipeline complete: {correct}/{total} correct ({accuracy:.1%})")
    return summary


async def run_from_pdf(
    pdf_path: str,
    year: int,
    output_path: str,
    config: PipelineConfig | None = None,
    solver_backend: str = "auto",
) -> dict:
    """
    Parse PDF exam file and run through the 4-agent harness.
    Returns summary statistics.
    """
    from ee_agent.ingestion.korean_parser import KoreanQuestionParser
    from ee_agent.ingestion.pdf_extractor import PDFExtractor

    config = config or PipelineConfig()
    extractor = PDFExtractor()
    parser = KoreanQuestionParser()

    full_text = extractor.extract_full_text(pdf_path)
    questions = parser.parse_text(full_text, year=year)

    if not questions:
        logger.warning(f"No questions parsed from {pdf_path}")
        return {"total": 0, "correct": 0, "accuracy": 0.0}

    logger.info(f"Parsed {len(questions)} questions from PDF")

    harness = build_harness(config, solver_backend=solver_backend)
    results = await harness.process_batch(questions, max_concurrent=config.max_concurrent)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    correct = sum(1 for r in results if r.get("is_correct", False))
    total = len(results)
    summary = {
        "total": total,
        "correct": correct,
        "accuracy": round(correct / total, 3) if total > 0 else 0.0,
        "output_file": output_path,
    }
    return summary
