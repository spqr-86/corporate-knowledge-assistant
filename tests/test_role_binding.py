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


def test_fail_closed_binds_role_for_unknown_tool_carrying_role_arg():
    """Defence in depth against drift: if search_handbook is ever renamed, or
    a second permission-gated retrieval tool is added, an LLM-supplied `role`
    on ANY tool call must still be overwritten from trusted session state —
    the RBAC bypass must not silently reopen just because the tool name no
    longer matches the hardcoded one."""
    tool_context = MagicMock()
    tool_context.state = {"user_role": "employee"}
    args = {"query": "compensation review cycle", "role": "hr_admin"}

    bind_role_from_session(
        tool=_make_tool("search_handbook_v2"), args=args, tool_context=tool_context
    )

    assert args["role"] == "employee"


def test_fail_closed_defaults_unknown_tool_role_to_least_privilege():
    tool_context = MagicMock()
    tool_context.state = {}
    args = {"query": "x", "role": "hr_admin"}

    bind_role_from_session(
        tool=_make_tool("some_future_retrieval_tool"),
        args=args,
        tool_context=tool_context,
    )

    assert args["role"] == "employee"


def test_fail_closed_binds_declared_role_even_when_llm_omits_it():
    """The real drift risk: a new/renamed retrieval tool that DECLARES a
    `role` param, called by the LLM WITHOUT one (so it falls back to the
    tool's own permissive default). Binding must trigger off the tool's
    signature, not off whether the model happened to volunteer the arg."""
    from google.adk.tools import FunctionTool

    def search_payroll(query: str, role: str = "hr_admin") -> dict:
        return {}

    tool = FunctionTool(func=search_payroll)  # deliberately NOT registered
    tool_context = MagicMock()
    tool_context.state = {"user_role": "employee"}
    args = {"query": "salaries"}  # LLM omitted role -> would use hr_admin default

    bind_role_from_session(tool=tool, args=args, tool_context=tool_context)

    assert args["role"] == "employee"


def test_ignores_unrelated_tools():
    tool_context = MagicMock()
    tool_context.state = {"user_role": "manager"}
    args = {"start_date": "2026-08-10", "end_date": "2026-08-14", "reason": "trip"}

    bind_role_from_session(
        tool=_make_tool("draft_pto_request"), args=args, tool_context=tool_context
    )

    assert "role" not in args
