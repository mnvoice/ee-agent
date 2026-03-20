"""Claude Code CLI client — uses Pro subscription instead of API credits."""
import asyncio
import logging
import os
import shutil

from ee_agent.llm.base import LLMClient, LLMResponse

logger = logging.getLogger(__name__)

CLAUDE_CLI = shutil.which("claude") or "claude"


class ClaudeCodeClient(LLMClient):
    """
    LLM client that calls the `claude -p` CLI as a subprocess.
    Uses Claude Pro/Max subscription credits instead of pay-per-use API.

    Limitation: Cannot run inside an active Claude Code session.
    Run the pipeline from a regular terminal (not from within Claude Code).
    """

    DEFAULT_MODEL = "claude-sonnet-4-6"

    def __init__(self, model: str = DEFAULT_MODEL):
        self._model = model

    @property
    def model_name(self) -> str:
        return self._model

    async def complete(
        self, prompt: str, system: str = "", max_tokens: int = 2048
    ) -> LLMResponse:
        # Build CLI command — output-format json gives structured result + usage info
        cmd = [
            CLAUDE_CLI, "--print",
            "--output-format", "json",
            "--no-session-persistence",  # avoid session state leaking between questions
        ]
        if system:
            cmd += ["--system-prompt", system]
        cmd.append(prompt)

        # Unset CLAUDECODE to allow running outside Claude Code session check
        env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
        except asyncio.TimeoutError:
            raise RuntimeError("claude CLI timed out after 120s")

        if proc.returncode != 0:
            err = stderr.decode(errors="replace").strip()
            raise RuntimeError(f"claude CLI error (rc={proc.returncode}): {err}")

        raw = stdout.decode(errors="replace").strip()

        # --output-format json wraps response: {"result": "...", "usage": {...}, ...}
        import json as _json
        try:
            wrapper = _json.loads(raw)
            content = wrapper.get("result", raw)
            usage = wrapper.get("usage", {})
            input_tokens = usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
            output_tokens = usage.get("output_tokens", 0)
            cost = wrapper.get("total_cost_usd", 0)
            if cost:
                logger.debug(f"Claude CLI cost: ${cost:.4f}")
        except (_json.JSONDecodeError, AttributeError):
            content = raw
            input_tokens = len(prompt.encode()) // 4
            output_tokens = len(raw.encode()) // 4

        return LLMResponse(
            content=content,
            model=self._model,
            prompt_tokens=input_tokens,
            completion_tokens=output_tokens,
            finish_reason="stop",
        )

    async def is_available(self) -> bool:
        if not CLAUDE_CLI:
            return False
        # Inside Claude Code session → subprocess would fail
        if os.environ.get("CLAUDECODE"):
            logger.warning(
                "ClaudeCodeClient: CLAUDECODE env detected. "
                "Run pipeline from a regular terminal, not inside Claude Code."
            )
            return False
        try:
            proc = await asyncio.create_subprocess_exec(
                CLAUDE_CLI, "--version",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await asyncio.wait_for(proc.communicate(), timeout=10)
            return proc.returncode == 0
        except Exception:
            return False
