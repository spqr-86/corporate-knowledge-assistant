"""Denial-of-Wallet guardrail (Day4) — before_tool_callback.

ANCHOR: dow_limit
Role: before_tool_callback for hr_domain_agent tools. Counts tool calls per
      session in tool_context.state and blocks once a session exceeds
      DOW_TOOL_CALL_LIMIT, preventing runaway/looping agent behavior from
      generating unbounded tool-call cost.
Input: tool, args, tool_context (ADK before_tool_callback signature).
Output: None (call proceeds) or a dict {status: "error", error_message}
      that short-circuits the tool call.
"""

from __future__ import annotations

DOW_TOOL_CALL_LIMIT = 5

_STATE_KEY = "dow_tool_call_count"


def dow_guardrail(*, tool, args: dict, tool_context) -> dict | None:
    count = tool_context.state.get(_STATE_KEY, 0)
    if count >= DOW_TOOL_CALL_LIMIT:
        return {
            "status": "error",
            "error_message": (
                f"Denial-of-Wallet limit reached ({DOW_TOOL_CALL_LIMIT} tool "
                "calls this session) — stopping to avoid a runaway loop."
            ),
        }
    tool_context.state[_STATE_KEY] = count + 1
    return None
