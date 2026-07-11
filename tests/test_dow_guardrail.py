from unittest.mock import MagicMock

from guardrails.dow_limit import _STATE_KEY, DOW_TOOL_CALL_LIMIT, dow_guardrail


def _make_tool_context(count: int = 0):
    ctx = MagicMock()
    ctx.state = {_STATE_KEY: count} if count else {}
    return ctx


def test_allows_call_under_limit():
    ctx = _make_tool_context(count=0)
    result = dow_guardrail(tool=MagicMock(), args={}, tool_context=ctx)
    assert result is None
    assert ctx.state[_STATE_KEY] == 1


def test_blocks_call_at_limit():
    ctx = _make_tool_context(count=DOW_TOOL_CALL_LIMIT)
    result = dow_guardrail(
        tool=MagicMock(name="search_handbook"), args={}, tool_context=ctx
    )
    assert result is not None
    assert result["status"] == "error"
    assert "limit" in result["error_message"].lower()


def test_counter_is_per_invocation_not_per_session():
    """The counter must live under the `temp:` state prefix, which ADK clears
    between invocations — otherwise 5 tool calls total permanently block the
    whole session (bug found in review)."""
    assert _STATE_KEY.startswith("temp:")

    # turn 1 exhausts the budget
    ctx = _make_tool_context()
    for _ in range(DOW_TOOL_CALL_LIMIT):
        assert dow_guardrail(tool=MagicMock(), args={}, tool_context=ctx) is None
    assert dow_guardrail(tool=MagicMock(), args={}, tool_context=ctx) is not None

    # turn 2: ADK dropped temp: state — fresh budget, calls allowed again
    ctx2 = _make_tool_context()
    assert dow_guardrail(tool=MagicMock(), args={}, tool_context=ctx2) is None
