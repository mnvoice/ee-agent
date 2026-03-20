"""Unit tests for 4-Agent Harness — no Ollama required."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from ee_agent.agents.base import AgentInput, AgentOutput, BaseAgent
from ee_agent.agents.vision_analyst import VisionTopologyAnalyst
from ee_agent.agents.logic_solver import LogicFirstPrinciplesSolver
from ee_agent.agents.verifier import VerifierGatekeeper
from ee_agent.agents.memory_sync import MemoryKnowledgeSync
from ee_agent.agents.harness import EEAgentHarness
from ee_agent.domain.models.question import (
    Choice, DifficultyLevel, Question, QuestionType, Subject
)


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def ohms_law_question():
    return Question(
        year=2023, exam_session=1, question_number=1,
        subject=Subject.ELECTRICAL_THEORY,
        question_type=QuestionType.CALCULATION,
        difficulty=DifficultyLevel.EASY,
        stem="저항 R=10Ω인 회로에 전압 V=100V를 인가할 때 전류 I는 몇 A인가?",
        choices=[
            Choice(index=1, text="5A", is_correct=False),
            Choice(index=2, text="10A", is_correct=True),
            Choice(index=3, text="15A", is_correct=False),
            Choice(index=4, text="20A", is_correct=False),
        ],
        correct_answer=2,
        explanation="옴의 법칙: I = V/R = 100/10 = 10A",
    )


@pytest.fixture
def regulation_question():
    return Question(
        year=2023, exam_session=1, question_number=5,
        subject=Subject.ELECTRICAL_SAFETY,
        question_type=QuestionType.REGULATION,
        difficulty=DifficultyLevel.MEDIUM,
        stem="전기설비기술기준 제3조에 따른 접지 저항값은?",
        choices=[
            Choice(index=1, text="10Ω 이하", is_correct=False),
            Choice(index=2, text="100Ω 이하", is_correct=True),
            Choice(index=3, text="1000Ω 이하", is_correct=False),
            Choice(index=4, text="제한 없음", is_correct=False),
        ],
        correct_answer=2,
    )


def make_harness(mock_llm=None):
    """Build harness with mock LLM and no-op retriever."""
    mock_retriever = MagicMock()
    mock_retriever.retrieve_formulas.return_value = []
    mock_retriever.add_concept = MagicMock()
    mock_retriever.add_formula = MagicMock()

    return EEAgentHarness(
        vision=VisionTopologyAnalyst(llm_client=mock_llm),
        solver=LogicFirstPrinciplesSolver(llm_client=mock_llm, retriever=mock_retriever),
        verifier=VerifierGatekeeper(),
        memory=MemoryKnowledgeSync(retriever=mock_retriever),
    )


# ── BaseAgent / AgentOutput ───────────────────────────────────────────────────

class TestAgentOutput:
    def test_succeeded_true_when_no_error(self):
        out = AgentOutput("a", "q1", {}, 0.9, [])
        assert out.succeeded is True

    def test_succeeded_false_when_error_set(self):
        out = AgentOutput("a", "q1", {}, 0.0, [], error="oops")
        assert out.succeeded is False

    def test_confidence_field(self):
        out = AgentOutput("a", "q1", {"k": 1}, 0.75, ["step1"])
        assert out.confidence == 0.75
        assert out.result == {"k": 1}
        assert out.reasoning_trace == ["step1"]


# ── VisionTopologyAnalyst ─────────────────────────────────────────────────────

class TestVisionTopologyAnalyst:
    def test_name(self):
        assert VisionTopologyAnalyst().name == "vision_analyst"

    @pytest.mark.asyncio
    async def test_lazy_discovery_skips_llm(self, ohms_law_question):
        mock_llm = AsyncMock()
        agent = VisionTopologyAnalyst(llm_client=mock_llm)
        inp = AgentInput(
            question_id=ohms_law_question.id,
            context=EEAgentHarness._build_initial_context(ohms_law_question),
        )
        out = await agent.run(inp)
        mock_llm.complete.assert_not_called()  # Lazy Discovery
        assert "Lazy Discovery" in out.reasoning_trace[0]
        assert out.succeeded

    @pytest.mark.asyncio
    async def test_returns_topology_dict(self, ohms_law_question):
        agent = VisionTopologyAnalyst()
        inp = AgentInput(
            question_id=ohms_law_question.id,
            context=EEAgentHarness._build_initial_context(ohms_law_question),
        )
        out = await agent.run(inp)
        assert "topology" in out.result
        assert "has_image" in out.result

    def test_text_based_topology_detects_3phase(self):
        agent = VisionTopologyAnalyst()
        result = agent._text_based_topology("3상 회로에서 선간전압이 380V일 때")
        assert result["phase_config"] == "3상"

    def test_text_based_topology_detects_series(self):
        agent = VisionTopologyAnalyst()
        result = agent._text_based_topology("직렬로 연결된 저항 R1=5Ω, R2=5Ω")
        assert result["circuit_type"] == "직렬"

    def test_text_based_topology_detects_components(self):
        agent = VisionTopologyAnalyst()
        result = agent._text_based_topology("변압기의 1차 권선에 100V를 인가할 때")
        assert "변압기" in result["components"]

    def test_text_based_topology_unknown_when_no_keywords(self):
        agent = VisionTopologyAnalyst()
        result = agent._text_based_topology("다음 중 옳은 것은?")
        assert result["circuit_type"] == "unknown"

    @pytest.mark.asyncio
    async def test_llm_fallback_when_none_and_has_image(self):
        agent = VisionTopologyAnalyst(llm_client=None)
        inp = AgentInput("q1", {"stem": "직렬 회로", "has_image": True})
        out = await agent.run(inp)
        assert out.succeeded
        assert "text-based" in " ".join(out.reasoning_trace).lower()


# ── LogicFirstPrinciplesSolver ────────────────────────────────────────────────

class TestLogicFirstPrinciplesSolver:
    def test_name(self):
        assert LogicFirstPrinciplesSolver().name == "logic_solver"

    @pytest.mark.asyncio
    async def test_schema_exclusion_in_trace(self, ohms_law_question):
        agent = LogicFirstPrinciplesSolver(llm_client=None)
        inp = AgentInput(
            question_id=ohms_law_question.id,
            context=EEAgentHarness._build_initial_context(ohms_law_question),
        )
        out = await agent.run(inp)
        combined = " ".join(out.reasoning_trace)
        assert "Schema Exclusion" in combined

    @pytest.mark.asyncio
    async def test_fallback_when_no_llm(self, ohms_law_question):
        agent = LogicFirstPrinciplesSolver(llm_client=None)
        inp = AgentInput(
            question_id=ohms_law_question.id,
            context=EEAgentHarness._build_initial_context(ohms_law_question),
        )
        out = await agent.run(inp)
        assert out.result["final_answer"] == "unknown"
        assert out.confidence <= 0.15

    @pytest.mark.asyncio
    async def test_retriever_called_for_formulas(self, ohms_law_question):
        mock_retriever = MagicMock()
        mock_retriever.retrieve_formulas.return_value = []
        agent = LogicFirstPrinciplesSolver(llm_client=None, retriever=mock_retriever)
        inp = AgentInput(
            question_id=ohms_law_question.id,
            context=EEAgentHarness._build_initial_context(ohms_law_question),
        )
        await agent.run(inp)
        mock_retriever.retrieve_formulas.assert_called_once()

    def test_fallback_extract_gets_numbers(self):
        agent = LogicFirstPrinciplesSolver()
        result = agent._fallback_extract("R=10Ω, V=100V인 회로")
        assert len(result["given"]["extracted_numbers"]) >= 1

    @pytest.mark.asyncio
    async def test_llm_json_parse_error_gives_low_confidence(self):
        mock_llm = AsyncMock()
        from ee_agent.llm.base import LLMResponse
        mock_llm.complete.return_value = LLMResponse(content="not valid json", model="test")
        agent = LogicFirstPrinciplesSolver(llm_client=mock_llm)
        inp = AgentInput("q1", {"stem": "test", "topology": {}})
        out = await agent.run(inp)
        assert out.result["confidence"] <= 0.35


# ── VerifierGatekeeper ────────────────────────────────────────────────────────

class TestVerifierGatekeeper:
    def test_name(self):
        assert VerifierGatekeeper().name == "verifier"

    def test_extract_numbers_basic(self):
        nums = VerifierGatekeeper._extract_numbers("10A and 20.5V")
        assert 10.0 in nums
        assert 20.5 in nums

    def test_extract_numbers_empty(self):
        assert VerifierGatekeeper._extract_numbers("no numbers here") == []

    def test_numerical_match_exact(self):
        v = VerifierGatekeeper()
        choices = [
            {"index": 1, "text": "5A"},
            {"index": 2, "text": "10A"},
            {"index": 3, "text": "15A"},
            {"index": 4, "text": "20A"},
        ]
        result = v._numerical_match("10", choices, [])
        assert result["selected_choice"] == 2
        assert result["confidence"] > 0.9

    def test_numerical_match_within_tolerance(self):
        v = VerifierGatekeeper()
        choices = [{"index": 1, "text": "41.88"}, {"index": 2, "text": "50"}, {"index": 3, "text": "60"}, {"index": 4, "text": "70"}]
        result = v._numerical_match("41.9", choices, [])
        assert result["selected_choice"] == 1

    def test_numerical_match_no_match(self):
        v = VerifierGatekeeper()
        choices = [{"index": 1, "text": "100"}, {"index": 2, "text": "200"}, {"index": 3, "text": "300"}, {"index": 4, "text": "400"}]
        result = v._numerical_match("5", choices, [])
        assert result["selected_choice"] is None

    def test_fuzzy_audit_finds_best(self):
        v = VerifierGatekeeper()
        choices = [
            {"index": 1, "text": "5A"},
            {"index": 2, "text": "10A"},
            {"index": 3, "text": "15A"},
            {"index": 4, "text": "20A"},
        ]
        result = v.fuzzy_audit("10A", choices, [])
        assert result["selected_choice"] == 2

    def test_staged_compact_prefers_numerical(self):
        v = VerifierGatekeeper()
        numerical = {"selected_choice": 2, "confidence": 0.95}
        fuzzy = {"selected_choice": 3, "confidence": 0.8}
        result = v._staged_compact(numerical, fuzzy, [])
        assert result["selected_choice"] == 2
        assert result["method"] == "numerical"

    def test_staged_compact_falls_back_to_fuzzy(self):
        v = VerifierGatekeeper()
        numerical = {"selected_choice": None, "confidence": 0.0}
        fuzzy = {"selected_choice": 2, "confidence": 0.75}
        result = v._staged_compact(numerical, fuzzy, [])
        assert result["selected_choice"] == 2
        assert result["method"] == "fuzzy"

    def test_staged_compact_default_when_all_low(self):
        v = VerifierGatekeeper()
        result = v._staged_compact(
            {"selected_choice": None, "confidence": 0.0},
            {"selected_choice": 2, "confidence": 0.1},
            [],
        )
        assert result["selected_choice"] == 1
        assert result["method"] == "default"

    @pytest.mark.asyncio
    async def test_run_with_empty_choices_defaults(self):
        v = VerifierGatekeeper()
        inp = AgentInput("q1", {"choices": [], "solver_result": {"final_answer": "10"}})
        out = await v.run(inp)
        assert out.result["selected_choice"] == 1
        assert out.result["verification_passed"] is False

    @pytest.mark.asyncio
    async def test_run_with_valid_choices(self, ohms_law_question):
        v = VerifierGatekeeper()
        ctx = EEAgentHarness._build_initial_context(ohms_law_question)
        ctx["solver_result"] = {"final_answer": "10", "law_used": "옴의 법칙"}
        inp = AgentInput(ohms_law_question.id, ctx)
        out = await v.run(inp)
        assert "selected_choice" in out.result
        assert 1 <= out.result["selected_choice"] <= 4


# ── MemoryKnowledgeSync ───────────────────────────────────────────────────────

class TestMemoryKnowledgeSync:
    def test_name(self):
        assert MemoryKnowledgeSync().name == "memory_sync"

    def test_infer_latex_ohms_law(self):
        assert MemoryKnowledgeSync._infer_latex("옴의 법칙") == "V = IR"

    def test_infer_latex_3phase(self):
        latex = MemoryKnowledgeSync._infer_latex("3상 전력")
        assert "sqrt" in latex or "\\sqrt" in latex

    def test_infer_latex_unknown_returns_input(self):
        assert MemoryKnowledgeSync._infer_latex("미지의 법칙") == "미지의 법칙"

    @pytest.mark.asyncio
    async def test_run_returns_final_choice(self, ohms_law_question):
        m = MemoryKnowledgeSync()
        ctx = EEAgentHarness._build_initial_context(ohms_law_question)
        ctx["solver_result"] = {"final_answer": "10", "law_used": "옴의 법칙"}
        ctx["verification"] = {"selected_choice": 2, "confidence": 0.95}
        inp = AgentInput(ohms_law_question.id, ctx)
        out = await m.run(inp)
        assert out.result["final_answer_choice"] == 2
        assert out.confidence == 0.95

    @pytest.mark.asyncio
    async def test_sync_to_retriever_called(self, ohms_law_question):
        mock_retriever = MagicMock()
        mock_retriever.add_concept = MagicMock()
        mock_retriever.add_formula = MagicMock()
        m = MemoryKnowledgeSync(retriever=mock_retriever)
        ctx = EEAgentHarness._build_initial_context(ohms_law_question)
        ctx["solver_result"] = {"final_answer": "10", "law_used": "옴의 법칙"}
        ctx["verification"] = {"selected_choice": 2, "confidence": 0.9}
        await m.run(AgentInput(ohms_law_question.id, ctx))
        mock_retriever.add_concept.assert_called()

    def test_extract_knowledge_extracts_law(self):
        m = MemoryKnowledgeSync()
        result = m._extract_knowledge(
            "R=10Ω, V=100V", "전기이론", {"law_used": "옴의 법칙"}, []
        )
        assert any(c["name"] == "옴의 법칙" for c in result["concepts"])


# ── EEAgentHarness ────────────────────────────────────────────────────────────

class TestEEAgentHarness:
    def test_build_initial_context(self, ohms_law_question):
        ctx = EEAgentHarness._build_initial_context(ohms_law_question)
        assert ctx["stem"] == ohms_law_question.stem
        assert len(ctx["choices"]) == 4
        assert ctx["has_image"] is False
        assert ctx["correct_answer"] == 2

    @pytest.mark.asyncio
    async def test_process_question_calls_all_agents(self, ohms_law_question):
        harness = make_harness()

        # Spy on each agent
        for agent in [harness.vision, harness.solver, harness.verifier, harness.memory]:
            agent.run = AsyncMock(wraps=agent.run)

        result = await harness.process_question(ohms_law_question)

        harness.vision.run.assert_called_once()
        harness.solver.run.assert_called_once()
        harness.verifier.run.assert_called_once()
        harness.memory.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_process_question_returns_required_keys(self, ohms_law_question):
        harness = make_harness()
        result = await harness.process_question(ohms_law_question)
        for key in ["question_id", "predicted_choice", "correct_choice", "is_correct",
                    "final_confidence", "reasoning_traces", "agent_outputs"]:
            assert key in result

    @pytest.mark.asyncio
    async def test_process_question_correct_for_ohms_law(self, ohms_law_question):
        """Verifier should pick choice 2 (10A) for the Ohm's law question."""
        harness = make_harness()
        # Override solver to return the correct numerical answer
        async def mock_solver_run(inp):
            ctx = inp.context.copy()
            return AgentOutput(
                agent_name="logic_solver",
                question_id=inp.question_id,
                result={"final_answer": "10", "law_used": "옴의 법칙", "unit": "A", "confidence": 0.9},
                confidence=0.9,
                reasoning_trace=["I = V/R = 100/10 = 10A"],
            )
        harness.solver.run = mock_solver_run
        result = await harness.process_question(ohms_law_question)
        assert result["predicted_choice"] == 2
        assert result["is_correct"] is True

    @pytest.mark.asyncio
    async def test_process_batch_processes_all(self, ohms_law_question, regulation_question):
        harness = make_harness()
        results = await harness.process_batch([ohms_law_question, regulation_question])
        assert len(results) == 2
        ids = {r["question_id"] for r in results}
        assert ohms_law_question.id in ids
        assert regulation_question.id in ids

    @pytest.mark.asyncio
    async def test_process_batch_handles_error_gracefully(self, ohms_law_question):
        harness = make_harness()
        harness.vision.run = AsyncMock(side_effect=RuntimeError("test error"))
        results = await harness.process_batch([ohms_law_question])
        assert len(results) == 1
        assert "error" in results[0]

    @pytest.mark.asyncio
    async def test_reasoning_traces_have_all_agents(self, ohms_law_question):
        harness = make_harness()
        result = await harness.process_question(ohms_law_question)
        traces = result["reasoning_traces"]
        assert "vision_analyst" in traces
        assert "logic_solver" in traces
        assert "verifier" in traces
        assert "memory_sync" in traces
