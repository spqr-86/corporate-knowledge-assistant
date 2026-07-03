from unittest.mock import MagicMock

from guardrails.dow_limit import DOW_TOOL_CALL_LIMIT, dow_guardrail


def _make_tool_context(count: int = 0):
    ctx = MagicMock()
    ctx.state = {"dow_tool_call_count": count} if count else {}
    return ctx


def test_allows_call_under_limit():
    ctx = _make_tool_context(count=0)
    result = dow_guardrail(tool=MagicMock(), args={}, tool_context=ctx)
    assert result is None
    assert ctx.state["dow_tool_call_count"] == 1


def test_blocks_call_at_limit():
    ctx = _make_tool_context(count=DOW_TOOL_CALL_LIMIT)
    result = dow_guardrail(
        tool=MagicMock(name="search_handbook"), args={}, tool_context=ctx
    )
    assert result is not None
    assert result["status"] == "error"
    assert "limit" in result["error_message"].lower()
