"""Unit tests for LLM clients — no running LLM required."""
from dataclasses import dataclass
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ee_agent.llm.base import LLMClient, LLMResponse
from ee_agent.llm.router import LLMRouter, TaskComplexity


# ── LLMResponse ──────────────────────────────────────────────────────────────

class TestLLMResponse:
    def test_creation_minimal(self):
        r = LLMResponse(content="hello", model="llama3")
        assert r.content == "hello"
        assert r.model == "llama3"
        assert r.prompt_tokens == 0
        assert r.completion_tokens == 0
        assert r.finish_reason == "stop"

    def test_total_tokens(self):
        r = LLMResponse(content="x", model="m", prompt_tokens=10, completion_tokens=20)
        assert r.total_tokens == 30

    def test_custom_finish_reason(self):
        r = LLMResponse(content="x", model="m", finish_reason="length")
        assert r.finish_reason == "length"


# ── OllamaClient ─────────────────────────────────────────────────────────────

class TestOllamaClient:
    def test_model_name(self):
        from ee_agent.llm.ollama_client import OllamaClient
        client = OllamaClient(model="qwen2.5")
        assert client.model_name == "qwen2.5"

    def test_default_model(self):
        from ee_agent.llm.ollama_client import OllamaClient
        client = OllamaClient()
        assert client.model_name == "llama3"

    @pytest.mark.asyncio
    async def test_is_available_false_when_offline(self):
        from ee_agent.llm.ollama_client import OllamaClient
        client = OllamaClient(base_url="http://localhost:19999")  # non-existent port
        result = await client.is_available()
        assert result is False

    @pytest.mark.asyncio
    async def test_complete_success(self):
        from ee_agent.llm.ollama_client import OllamaClient
        import aiohttp

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.raise_for_status = MagicMock()
        mock_response.json = AsyncMock(return_value={
            "response": "전류 I = 10A",
            "prompt_eval_count": 15,
            "eval_count": 8,
        })
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=False)

        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            client = OllamaClient()
            result = await client.complete("V=100V, R=10Ω일 때 I는?")

        assert result.content == "전류 I = 10A"
        assert result.prompt_tokens == 15
        assert result.completion_tokens == 8
        assert result.model == "llama3"

    @pytest.mark.asyncio
    async def test_complete_with_system_prompt(self):
        from ee_agent.llm.ollama_client import OllamaClient

        mock_response = AsyncMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json = AsyncMock(return_value={"response": "OK", "prompt_eval_count": 5, "eval_count": 2})
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock(return_value=False)

        mock_session = AsyncMock()
        mock_session.post = MagicMock(return_value=mock_response)
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=False)

        with patch("aiohttp.ClientSession", return_value=mock_session):
            client = OllamaClient()
            result = await client.complete("question", system="You are an EE expert")

        assert result.content == "OK"

    @pytest.mark.asyncio
    async def test_list_models_returns_empty_on_error(self):
        from ee_agent.llm.ollama_client import OllamaClient
        client = OllamaClient(base_url="http://localhost:19999")
        models = await client.list_models()
        assert models == []


# ── AnthropicClient ──────────────────────────────────────────────────────────

class TestAnthropicClient:
    def test_model_name_default(self):
        from ee_agent.llm.anthropic_client import AnthropicClient
        client = AnthropicClient()
        assert client.model_name == "claude-sonnet-4-6"

    def test_model_name_custom(self):
        from ee_agent.llm.anthropic_client import AnthropicClient
        client = AnthropicClient(model="claude-opus-4-6")
        assert client.model_name == "claude-opus-4-6"

    @pytest.mark.asyncio
    async def test_is_available_when_not_installed(self):
        from ee_agent.llm import anthropic_client as ac_module
        original = ac_module.ANTHROPIC_AVAILABLE
        try:
            ac_module.ANTHROPIC_AVAILABLE = False
            from ee_agent.llm.anthropic_client import AnthropicClient
            client = AnthropicClient.__new__(AnthropicClient)
            client._model = "test"
            client._client = None
            result = await client.is_available()
            assert result is False
        finally:
            ac_module.ANTHROPIC_AVAILABLE = original

    @pytest.mark.asyncio
    async def test_complete_raises_when_not_available(self):
        from ee_agent.llm.anthropic_client import AnthropicClient
        from ee_agent.llm import anthropic_client as ac_module
        original = ac_module.ANTHROPIC_AVAILABLE
        try:
            ac_module.ANTHROPIC_AVAILABLE = False
            client = AnthropicClient.__new__(AnthropicClient)
            client._model = "test"
            client._client = None
            with pytest.raises(RuntimeError, match="not available"):
                await client.complete("test prompt")
        finally:
            ac_module.ANTHROPIC_AVAILABLE = original


# ── LLMRouter ────────────────────────────────────────────────────────────────

class TestLLMRouter:
    def _make_router(self, ollama_available: bool = True):
        from ee_agent.llm.ollama_client import OllamaClient
        from ee_agent.llm.anthropic_client import AnthropicClient

        ollama = AsyncMock(spec=OllamaClient)
        ollama.model_name = "llama3"
        ollama.is_available = AsyncMock(return_value=ollama_available)
        ollama.complete = AsyncMock(return_value=LLMResponse(content="ollama result", model="llama3"))

        anthropic = AsyncMock(spec=AnthropicClient)
        anthropic.model_name = "claude-sonnet-4-6"
        anthropic.is_available = AsyncMock(return_value=True)
        anthropic.complete = AsyncMock(return_value=LLMResponse(content="anthropic result", model="claude-sonnet-4-6"))

        router = LLMRouter(ollama=ollama, anthropic=anthropic)
        return router, ollama, anthropic

    @pytest.mark.asyncio
    async def test_routes_to_ollama_when_available(self):
        router, ollama, anthropic = self._make_router(ollama_available=True)
        result = await router.route("test prompt")
        assert result.content == "ollama result"
        ollama.complete.assert_called_once()
        anthropic.complete.assert_not_called()

    @pytest.mark.asyncio
    async def test_falls_back_to_anthropic_when_ollama_unavailable(self):
        router, ollama, anthropic = self._make_router(ollama_available=False)
        result = await router.route("test prompt")
        assert result.content == "anthropic result"
        anthropic.complete.assert_called_once()

    @pytest.mark.asyncio
    async def test_raises_when_both_unavailable(self):
        from ee_agent.llm.ollama_client import OllamaClient
        ollama = AsyncMock(spec=OllamaClient)
        ollama.is_available = AsyncMock(return_value=False)
        router = LLMRouter(ollama=ollama, anthropic=None)
        with pytest.raises(RuntimeError):
            await router.route("test prompt")

    def test_get_active_client_prefers_ollama(self):
        router, ollama, anthropic = self._make_router(ollama_available=True)
        router._ollama_available = True
        client = router.get_active_client()
        assert client is ollama

    def test_get_active_client_returns_anthropic_as_fallback(self):
        router, ollama, anthropic = self._make_router(ollama_available=False)
        router._ollama_available = False
        client = router.get_active_client()
        assert client is anthropic

    def test_task_complexity_values(self):
        assert TaskComplexity.SIMPLE == "simple"
        assert TaskComplexity.MEDIUM == "medium"
        assert TaskComplexity.COMPLEX == "complex"
