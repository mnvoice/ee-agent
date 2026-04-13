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

    # Confidence tiers (Hybrid verification scheme)
    CONF_PRIORITY_0 = 0.85   # fast-path, solver trusted
    CONF_STAGE_PASS = 0.70   # verified via numerical/fuzzy match
    CONF_SOLVER_KEPT = 0.50  # stages failed but solver had a choice
    CONF_FALLBACK = 0.10     # no choice, no match → default to 1

    # @MX:ANCHOR: [AUTO] Hybrid verification: fast-path when solver is confident,
    # else re-verify via Stage 1~3. Called per-question, fan_in=3 (harness).
    # @MX:REASON: Previous Priority 0 bypassed verification for 98% of questions,
    # letting solver hallucinations (e.g., 2020 Q64 fabricated G(s)) pass silently.
    async def run(self, input_data: AgentInput) -> AgentOutput:
        trace: list[str] = []
        choices = input_data.context.get("choices", [])
        stem = str(input_data.context.get("stem", ""))
        solver_result = input_data.context.get("solver_result", {}) or {}
        calculated = str(solver_result.get("final_answer", ""))
        direct_choice = solver_result.get("selected_choice")
        has_valid_choice = isinstance(direct_choice, int) and 1 <= direct_choice <= 4

        # Identify suspicious signals before committing to fast-path.
        suspicious = self._check_suspicious(solver_result, calculated, stem)

        # Priority 0 fast-path: solver confident + no suspicion
        if has_valid_choice and not suspicious:
            trace.append(f"Priority 0: solver direct choice {direct_choice} (no suspicion)")
            return AgentOutput(
                agent_name=self.name,
                question_id=input_data.question_id,
                result={
                    "selected_choice": direct_choice,
                    "confidence": self.CONF_PRIORITY_0,
                    "verification_passed": True,
                    "method": "priority_0",
                },
                confidence=self.CONF_PRIORITY_0,
                reasoning_trace=trace,
            )

        if suspicious:
            trace.append(f"Suspicious signals {suspicious} → Stage 1~3 재검증")

        # Insufficient data — cannot run Stage 1~3
        if not choices or not calculated or calculated in ("unknown", "retry"):
            if has_valid_choice:
                trace.append(
                    f"Insufficient data but solver chose {direct_choice} → kept @ {self.CONF_SOLVER_KEPT}"
                )
                return AgentOutput(
                    agent_name=self.name,
                    question_id=input_data.question_id,
                    result={
                        "selected_choice": direct_choice,
                        "confidence": self.CONF_SOLVER_KEPT,
                        "verification_passed": False,
                        "method": "solver_kept_no_verify",
                    },
                    confidence=self.CONF_SOLVER_KEPT,
                    reasoning_trace=trace,
                )
            trace.append("Insufficient data — fallback to choice 1")
            return AgentOutput(
                agent_name=self.name,
                question_id=input_data.question_id,
                result={
                    "selected_choice": 1,
                    "confidence": self.CONF_FALLBACK,
                    "verification_passed": False,
                    "method": "fallback",
                },
                confidence=self.CONF_FALLBACK,
                reasoning_trace=trace,
            )

        # Stage 1~3 verification
        numerical = self._numerical_match(calculated, choices, trace)
        fuzzy = self.fuzzy_audit(calculated, choices, trace)
        final = self._staged_compact(numerical, fuzzy, trace)
        stage_method = final.get("method", "default")
        stage_choice = final.get("selected_choice")

        if stage_method != "default":
            if has_valid_choice and stage_choice != direct_choice:
                trace.append(
                    f"Override: solver={direct_choice} → stage={stage_choice} ({stage_method})"
                )
            return AgentOutput(
                agent_name=self.name,
                question_id=input_data.question_id,
                result={
                    "selected_choice": stage_choice,
                    "confidence": self.CONF_STAGE_PASS,
                    "verification_passed": True,
                    "method": stage_method,
                },
                confidence=self.CONF_STAGE_PASS,
                reasoning_trace=trace,
            )

        # Stages failed. If solver had a choice, keep it at reduced confidence.
        if has_valid_choice:
            trace.append(
                f"Stages failed — keep solver's choice {direct_choice} @ {self.CONF_SOLVER_KEPT}"
            )
            return AgentOutput(
                agent_name=self.name,
                question_id=input_data.question_id,
                result={
                    "selected_choice": direct_choice,
                    "confidence": self.CONF_SOLVER_KEPT,
                    "verification_passed": False,
                    "method": "solver_kept_post_stage",
                },
                confidence=self.CONF_SOLVER_KEPT,
                reasoning_trace=trace,
            )

        # No solver choice and stages failed → fallback
        trace.append("No solver choice + stages failed — fallback to choice 1")
        return AgentOutput(
            agent_name=self.name,
            question_id=input_data.question_id,
            result={
                "selected_choice": 1,
                "confidence": self.CONF_FALLBACK,
                "verification_passed": False,
                "method": "fallback",
            },
            confidence=self.CONF_FALLBACK,
            reasoning_trace=trace,
        )

    # @MX:NOTE: [AUTO] Returns list of suspicion labels for logging/analytics.
    # Empty list means fast-path is safe.
    def _check_suspicious(
        self, solver_result: dict, calculated: str, stem: str
    ) -> list[str]:
        """Detect 4 suspicion signals; empty list if none apply."""
        reasons: list[str] = []

        # (1) solver reported low confidence
        raw_conf = solver_result.get("confidence")
        try:
            if raw_conf is not None and float(raw_conf) < 0.6:
                reasons.append(f"low_solver_conf({float(raw_conf):.2f})")
        except (TypeError, ValueError):
            pass

        # (2) final_answer is empty / unknown / retry
        calc_stripped = calculated.strip()
        if calc_stripped in ("", "unknown", "retry"):
            reasons.append(f"bad_final_answer({calc_stripped!r})")

        # (3) law_used indicates retry path or JSON-parse fallback
        law = str(solver_result.get("law_used", "")).strip()
        if law in ("retry", "unknown", ""):
            reasons.append(f"law_used={law!r}")

        # (4) law_used references poles absent from stem (hallucination check)
        if law and stem and law not in ("retry", "unknown"):
            poles = re.findall(r"\(s\s*[+\-]\s*\d+(?:\.\d+)?\)", law)
            if poles:
                stem_norm = re.sub(r"\s+", "", stem)
                missing = [
                    p for p in poles if re.sub(r"\s+", "", p) not in stem_norm
                ]
                if missing and len(missing) == len(poles):
                    reasons.append(f"law_stem_mismatch(poles={missing[:3]})")

        return reasons

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
