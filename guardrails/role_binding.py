"""Binds search_handbook's `role` arg to session state — before_tool_callback.

ANCHOR: role_binding
Role: closes the RBAC bypass where `role` was an LLM-controllable tool
      argument (a prompt like "I'm a manager" could set role='manager').
      Session state — set once at session creation from a trusted context,
      never from the model — always wins over whatever the LLM tried to
      pass, so the permission-aware retrieval feature stays demoable
      (start a session as a manager) without being LLM-exploitable.
Input: tool, args, tool_context (ADK before_tool_callback signature).
Output: None always (never short-circuits the call) — mutates `args` in
      place before the tool executes.
"""

from __future__ import annotations

from typing import Any

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

_SESSION_STATE_KEY = "user_role"
_TARGET_TOOL_NAME = "search_handbook"


def bind_role_from_session(
    *, tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> None:
    if tool.name != _TARGET_TOOL_NAME:
        return None
    args["role"] = tool_context.state.get(_SESSION_STATE_KEY, "employee")
    return None
