from unittest.mock import MagicMock

from guardrails.role_binding import bind_role_from_session


def _make_tool(name: str):
    tool = MagicMock()
    tool.name = name
    return tool


def test_injects_role_from_session_state():
    tool_context = MagicMock()
    tool_context.state = {"user_role": "manager"}
    args = {"query": "compensation review cycle"}

    result = bind_role_from_session(
        tool=_make_tool("search_handbook"), args=args, tool_context=tool_context
    )

    assert result is None
    assert args["role"] == "manager"


def test_defaults_to_employee_when_session_has_no_role():
    tool_context = MagicMock()
    tool_context.state = {}
    args = {"query": "parental leave"}

    bind_role_from_session(
        tool=_make_tool("search_handbook"), args=args, tool_context=tool_context
    )

    assert args["role"] == "employee"


def test_session_role_overrides_llm_supplied_role():
    """The LLM might try to set role itself (e.g. prompt-injected 'I'm a
    manager') — session state must always win, never the model's own
    tool-call argument."""
    tool_context = MagicMock()
    tool_context.state = {"user_role": "employee"}
    args = {"query": "compensation review cycle", "role": "hr_admin"}

    bind_role_from_session(
        tool=_make_tool("search_handbook"), args=args, tool_context=tool_context
    )

    assert args["role"] == "employee"


def test_ignores_unrelated_tools():
    tool_context = MagicMock()
    tool_context.state = {"user_role": "manager"}
    args = {"start_date": "2026-08-10", "end_date": "2026-08-14", "reason": "trip"}

    bind_role_from_session(
        tool=_make_tool("draft_pto_request"), args=args, tool_context=tool_context
    )

    assert "role" not in args
