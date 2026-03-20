"""Agent 3: Verifier & Gatekeeper."""
import logging
import re

from ee_agent.agents.base import AgentInput, AgentOutput, BaseAgent

logger = logging.getLogger(__name__)

try:
    from thefuzz import fuzz

    THEFUZZ_AVAILABLE = True
except ImportError:
    THEFUZZ_AVAILABLE = False
    logger.warning("thefuzz not available. Using substring fallback.")


class VerifierGatekeeper(BaseAgent):
    """
    Agent 3: Verifier & Gatekeeper
    Strategy: Fuzzy Matching + Staged Compaction

    Fuzzy Matching: thefuzz token_sort_ratio to compare predicted vs choices.
    Staged Compaction: numerical (stage 1) → fuzzy (stage 2) → default (stage 3).
    """

    TOLERANCE_PCT = 0.05  # 5% numerical tolerance

    @property
    def name(self) -> str:
        return "verifier"

    async def run(self, input_data: AgentInput) -> AgentOutput:
        trace: list[str] = []
        choices = input_data.context.get("choices", [])
        solver_result = input_data.context.get("solver_result", {})
        calculated = str(solver_result.get("final_answer", ""))

        # Priority 0: solver already selected a choice directly
        direct_choice = solver_result.get("selected_choice")
        if isinstance(direct_choice, int) and 1 <= direct_choice <= 4:
            trace.append(f"Using solver's direct choice: {direct_choice}")
            return AgentOutput(
                agent_name=self.name,
                question_id=input_data.question_id,
                result={"selected_choice": direct_choice, "confidence": 0.85, "verification_passed": True},
                confidence=0.85,
                reasoning_trace=trace,
            )

        trace.append(f"Verifying '{calculated}' against {len(choices)} choices")

        if not choices or not calculated or calculated == "unknown":
            trace.append("Insufficient data — defaulting to choice 1")
            return AgentOutput(
                agent_name=self.name,
                question_id=input_data.question_id,
                result={"selected_choice": 1, "confidence": 0.1, "verification_passed": False},
                confidence=0.1,
                reasoning_trace=trace,
            )

        # Stage 1: Numerical match (highest precision)
        numerical = self._numerical_match(calculated, choices, trace)

        # Stage 2: Fuzzy text match (fallback)
        fuzzy = self.fuzzy_audit(calculated, choices, trace)

        # Stage 3: Combine
        final = self._staged_compact(numerical, fuzzy, trace)

        return AgentOutput(
            agent_name=self.name,
            question_id=input_data.question_id,
            result=final,
            confidence=final["confidence"],
            reasoning_trace=trace,
        )

    def fuzzy_audit(self, predicted: str, choices: list[dict], trace: list[str]) -> dict:
        """Stage 2: Fuzzy text matching."""
        scores = []
        for choice in choices:
            text = str(choice.get("text", ""))
            if THEFUZZ_AVAILABLE:
                score = fuzz.token_sort_ratio(predicted, text) / 100.0
            else:
                score = 1.0 if predicted.strip() in text else 0.3
            scores.append({"choice_index": choice.get("index", 1), "text": text, "score": score})

        best = max(scores, key=lambda x: x["score"])
        trace.append(f"Fuzzy: best=choice {best['choice_index']} (score={best['score']:.2f})")
        return {"selected_choice": best["choice_index"], "confidence": best["score"]}

    def _numerical_match(self, predicted: str, choices: list[dict], trace: list[str]) -> dict:
        """Stage 1: Numerical comparison within TOLERANCE_PCT."""
        pred_nums = self._extract_numbers(predicted)
        if not pred_nums:
            trace.append("Numerical: no numbers in predicted answer")
            return {"selected_choice": None, "confidence": 0.0}

        pred_val = pred_nums[0]
        best_idx = None
        best_diff = float("inf")

        for choice in choices:
            nums = self._extract_numbers(str(choice.get("text", "")))
            if nums:
                diff = abs(nums[0] - pred_val) / (abs(pred_val) + 1e-9)
                if diff < best_diff:
                    best_diff = diff
                    best_idx = choice.get("index", 1)

        if best_idx is not None and best_diff <= self.TOLERANCE_PCT:
            conf = 1.0 - (best_diff / self.TOLERANCE_PCT)
            trace.append(f"Numerical: choice {best_idx} (diff={best_diff:.3f}, conf={conf:.2f})")
            return {"selected_choice": best_idx, "confidence": conf}

        trace.append("Numerical: no match within tolerance")
        return {"selected_choice": None, "confidence": 0.0}

    def _staged_compact(self, numerical: dict, fuzzy: dict, trace: list[str]) -> dict:
        """Stage 3: Prefer numerical match if confident, else fuzzy."""
        num_conf = numerical.get("confidence", 0.0)
        fuzz_conf = fuzzy.get("confidence", 0.0)

        if numerical.get("selected_choice") and num_conf >= 0.7:
            trace.append(f"Staged compact: numerical match accepted (conf={num_conf:.2f})")
            return {
                "selected_choice": numerical["selected_choice"],
                "confidence": num_conf,
                "verification_passed": True,
                "method": "numerical",
            }

        if fuzzy.get("selected_choice") and fuzz_conf >= 0.5:
            trace.append(f"Staged compact: fuzzy match accepted (conf={fuzz_conf:.2f})")
            return {
                "selected_choice": fuzzy["selected_choice"],
                "confidence": fuzz_conf * 0.8,
                "verification_passed": fuzz_conf >= 0.6,
                "method": "fuzzy",
            }

        trace.append("Staged compact: low confidence — defaulting to choice 1")
        return {"selected_choice": 1, "confidence": 0.1, "verification_passed": False, "method": "default"}

    @staticmethod
    def _extract_numbers(text: str) -> list[float]:
        nums = []
        for m in re.finditer(r"[-+]?\d*\.?\d+", text):
            try:
                nums.append(float(m.group()))
            except ValueError:
                pass
        return nums
