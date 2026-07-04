"""Tests for observability.py — structured step logging + per-turn cost calc.

ANCHOR: test_observability
Role: TDD for TurnObserver (structlog step log + CPS/cost accumulation).
      Uses lightweight fakes instead of real ADK Event objects — only the
      attributes TurnObserver actually reads are faked.
"""

from types import SimpleNamespace

from observability import GPT_4O_MINI_PRICING, TurnObserver


def _fake_usage(prompt=100, candidates=50):
    return SimpleNamespace(
        prompt_token_count=prompt,
        candidates_token_count=candidates,
        total_token_count=prompt + candidates,
    )


def _fake_function_call(name="search_handbook", args=None):
    return SimpleNamespace(name=name, args=args or {"query": "parental leave"})


def _fake_event(*, author="hr_domain_agent", usage_metadata=None, function_call=None):
    part = SimpleNamespace(
        function_call=function_call, text=None if function_call else "hi"
    )
    content = SimpleNamespace(parts=[part]) if (function_call or True) else None
    return SimpleNamespace(
        author=author,
        usage_metadata=usage_metadata,
        content=content,
        is_final_response=lambda: function_call is None,
    )


def test_records_tool_call_step():
    observer = TurnObserver()
    event = _fake_event(function_call=_fake_function_call())
    observer.record(event)
    assert len(observer.steps) == 1
    assert observer.steps[0]["tool_name"] == "search_handbook"
    assert observer.steps[0]["args"] == {"query": "parental leave"}


def test_accumulates_token_usage_across_events():
    observer = TurnObserver()
    observer.record(_fake_event(usage_metadata=_fake_usage(100, 50)))
    observer.record(_fake_event(usage_metadata=_fake_usage(80, 20)))
    assert observer.total_prompt_tokens == 180
    assert observer.total_candidates_tokens == 70


def test_cost_uses_gpt4o_mini_pricing():
    observer = TurnObserver()
    observer.record(_fake_event(usage_metadata=_fake_usage(1_000_000, 1_000_000)))
    expected = (
        GPT_4O_MINI_PRICING["prompt_per_million"]
        + GPT_4O_MINI_PRICING["candidates_per_million"]
    )
    assert observer.cost_usd() == expected


def test_cost_zero_with_no_events():
    observer = TurnObserver()
    assert observer.cost_usd() == 0.0
    assert observer.steps == []
