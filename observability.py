"""Structured per-turn observability: step log + cost-per-query (CPS).

ANCHOR: observability
Role: wraps the ADK event stream consumed in agent.ask() to (a) emit a
      structlog line per meaningful step (tool call / final response) with
      tool_name, args, latency and decision_reason, and (b) accumulate token
      usage across the turn to compute an approximate cost in USD.
Input: ADK Event objects, as yielded by Runner.run_async().
Output: structlog log lines (side effect) + TurnObserver.cost_usd()/steps
      for callers that want the numbers (e.g. scripts/compute_cps.py).
Pricing: gpt-4o-mini list price as of the model's release (per 1M tokens),
      hardcoded — not fetched live, this is an approximation for the pitch,
      not a billing-accurate figure.
"""

import time

import structlog

from config import settings

logger = structlog.get_logger("corporate_knowledge_assistant")

GPT_4O_MINI_PRICING: dict[str, float] = settings.pricing


class TurnObserver:
    """Accumulates steps and token usage for a single ask() turn."""

    def __init__(self) -> None:
        self.steps: list[dict] = []
        self.total_prompt_tokens = 0
        self.total_candidates_tokens = 0
        self._last_ts = time.monotonic()

    def record(self, event) -> None:
        now = time.monotonic()
        latency_s = now - self._last_ts
        self._last_ts = now

        usage = getattr(event, "usage_metadata", None)
        if usage is not None:
            self.total_prompt_tokens += usage.prompt_token_count or 0
            self.total_candidates_tokens += usage.candidates_token_count or 0

        function_call = None
        content = getattr(event, "content", None)
        if content is not None and getattr(content, "parts", None):
            for part in content.parts:
                if getattr(part, "function_call", None):
                    function_call = part.function_call
                    break

        if function_call is not None:
            step = {
                "tool_name": function_call.name,
                "args": function_call.args,
                "latency_s": round(latency_s, 3),
                "decision_reason": "tool_call",
            }
            self.steps.append(step)
            logger.info("agent_step", author=getattr(event, "author", None), **step)
        elif getattr(event, "is_final_response", lambda: False)():
            step = {
                "tool_name": None,
                "args": None,
                "latency_s": round(latency_s, 3),
                "decision_reason": "final_response",
            }
            self.steps.append(step)
            logger.info("agent_step", author=getattr(event, "author", None), **step)

    def cost_usd(self) -> float:
        return (
            self.total_prompt_tokens
            / 1_000_000
            * GPT_4O_MINI_PRICING["prompt_per_million"]
            + self.total_candidates_tokens
            / 1_000_000
            * GPT_4O_MINI_PRICING["candidates_per_million"]
        )
