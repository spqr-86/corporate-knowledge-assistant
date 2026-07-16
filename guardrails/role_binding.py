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

import inspect
from typing import Any

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

from config import settings

_SESSION_STATE_KEY = "user_role"
_DEFAULT_ROLE = "employee"
_ROLE_ARG = "role"


def _tool_declares_role(tool: BaseTool) -> bool:
    """True if the tool exposes a `role` parameter (so binding it is safe and
    necessary), regardless of whether the LLM supplied one on this call.

    Checked via the tool's declared signature, not the runtime args — a
    permissive tool default is exploitable precisely when the model OMITS
    role, which arg-inspection alone would miss.
    """
    func = getattr(tool, "func", None)
    if func is not None:
        try:
            if _ROLE_ARG in inspect.signature(func).parameters:
                return True
        except (TypeError, ValueError):
            pass
    try:  # MCP/remote tools expose params via a function declaration schema
        declaration = tool._get_declaration()
        properties = getattr(
            getattr(declaration, "parameters", None), "properties", None
        )
        return bool(properties) and _ROLE_ARG in properties
    except Exception:
        return False


def bind_role_from_session(
    *, tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> None:
    # Fail-closed: bind whenever the tool can carry a role — it's in the known
    # gated set, its signature declares a `role` param, or the LLM already put
    # one in args. If search_handbook is renamed or a second permission-gated
    # retrieval tool is added, its `role` is still overwritten from trusted
    # session state (even when the model omits it and would hit a permissive
    # default) instead of silently reopening the RBAC bypass. Tools with no
    # `role` param (draft_pto_request, create_hr_ticket) are untouched.
    if (
        tool.name not in settings.rbac_gated_tools
        and _ROLE_ARG not in args
        and not _tool_declares_role(tool)
    ):
        return None
    args[_ROLE_ARG] = tool_context.state.get(_SESSION_STATE_KEY, _DEFAULT_ROLE)
    return None
