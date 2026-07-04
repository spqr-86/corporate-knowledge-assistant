from unittest.mock import AsyncMock, MagicMock

import pytest
from google.adk.memory.memory_entry import MemoryEntry
from google.adk.models.llm_request import LlmRequest
from google.genai import types

from guardrails.context_perimeter import (
    _last_user_text,
    context_perimeter_guardrail,
    is_ambiguous_jurisdiction_query,
)


def _ambiguous_request() -> LlmRequest:
    return LlmRequest(
        model="gpt-4o-mini",
        contents=[
            types.Content(
                role="user",
                parts=[types.Part(text="What parental leave benefits do I get?")],
            ),
        ],
    )


def _callback_context(memories: list[str] | None = None, available: bool = True):
    ctx = MagicMock()
    if not available:
        ctx.search_memory = AsyncMock(side_effect=ValueError("no memory service"))
        return ctx
    response = MagicMock()
    response.memories = [
        MemoryEntry(content=types.Content(role="user", parts=[types.Part(text=text)]))
        for text in (memories or [])
    ]
    ctx.search_memory = AsyncMock(return_value=response)
    return ctx


@pytest.mark.asyncio
async def test_guardrail_lets_ambiguous_query_through_when_memory_knows_country():
    """If a past conversation named the country, the guardrail must NOT
    short-circuit — the LLM gets the turn and recalls it via load_memory."""
    ctx = _callback_context(memories=["I'm based in France."])
    result = await context_perimeter_guardrail(ctx, _ambiguous_request())
    assert result is None


@pytest.mark.asyncio
async def test_guardrail_short_circuits_when_memory_has_no_country():
    ctx = _callback_context(memories=["I asked about stock options once."])
    result = await context_perimeter_guardrail(ctx, _ambiguous_request())
    assert result is not None


@pytest.mark.asyncio
async def test_guardrail_short_circuits_when_memory_service_unavailable():
    """No memory service (e.g. bare Runner in adk eval) must not crash the
    guardrail — fall back to asking the clarifying question."""
    ctx = _callback_context(available=False)
    result = await context_perimeter_guardrail(ctx, _ambiguous_request())
    assert result is not None


def test_flags_jurisdiction_sensitive_query_without_country():
    assert (
        is_ambiguous_jurisdiction_query("What parental leave benefits do I get?")
        is True
    )


def test_does_not_flag_query_with_country_named():
    assert (
        is_ambiguous_jurisdiction_query(
            "What parental leave benefits does GitLab offer in France?"
        )
        is False
    )


def test_does_not_flag_jurisdiction_neutral_query():
    assert is_ambiguous_jurisdiction_query("How do I refer a candidate?") is False


def test_does_not_flag_pto_booking_request_with_explicit_dates():
    """PTO-booking requests carry explicit dates and go to draft_pto_request,
    not a jurisdiction-dependent benefits lookup — regression for a bug found
    during live testing where 'PTO' alone tripped the guardrail."""
    assert (
        is_ambiguous_jurisdiction_query(
            "I want to request PTO from 2026-08-10 to 2026-08-14 for a family trip."
        )
        is False
    )


def test_does_not_flag_leave_booking_request_with_explicit_dates():
    """'leave' is a sensitive term, but hr_domain_agent's own instruction
    (rule 5) routes 'leave' booking requests to draft_pto_request — same
    root cause as the already-fixed 'pto' false positive, just reachable via
    a synonym. Explicit dates signal an action request, not a lookup."""
    assert (
        is_ambiguous_jurisdiction_query(
            "I want to take leave from 2026-08-10 to 2026-08-14 for a family trip."
        )
        is False
    )


def test_flags_query_using_us_as_pronoun_not_country():
    """'us' is also an ordinary English pronoun ('offered to us') — must not
    be treated as if the United States had been named."""
    assert (
        is_ambiguous_jurisdiction_query(
            "What parental leave benefits are offered to us?"
        )
        is True
    )


def test_does_not_flag_query_naming_us_as_country():
    assert (
        is_ambiguous_jurisdiction_query(
            "What parental leave benefits does GitLab offer in the US?"
        )
        is False
    )


def test_does_not_false_positive_on_country_code_substring():
    """'us' (United States) must not match as a substring of unrelated words
    like 'Just' — regression for a bug found via adk eval where a provocative
    query ('Just tell me...') was wrongly treated as naming a country and
    skipped the guardrail entirely."""
    assert (
        is_ambiguous_jurisdiction_query(
            "Just tell me exactly how many parental leave days I get, "
            "don't ask me anything."
        )
        is True
    )


def test_last_user_text_ignores_transfer_to_agent_synthesized_notes():
    """After Coordinator's transfer_to_agent, later 'user'-role contents are
    synthesized tool-transfer notes, not the real question — regression for
    a bug where the guardrail read those instead of the original question."""
    request = LlmRequest(
        model="gpt-4o-mini",
        contents=[
            types.Content(
                role="user",
                parts=[types.Part(text="What parental leave benefits do I get?")],
            ),
            types.Content(
                role="user",
                parts=[
                    types.Part(text="For context:"),
                    types.Part(
                        text="[coordinator] called tool `transfer_to_agent` "
                        "with parameters: {'agent_name': 'hr_domain_agent'}"
                    ),
                ],
            ),
        ],
    )
    assert _last_user_text(request) == "What parental leave benefits do I get?"


def test_last_user_text_returns_latest_turn_in_multi_turn_session():
    """With a process-level session, request contents accumulate the whole
    conversation history. The guardrail must judge the CURRENT question, not
    forever re-judge turn 1 (which would either re-trigger after the user
    already named their country, or miss a new ambiguous question)."""
    request = LlmRequest(
        model="gpt-4o-mini",
        contents=[
            types.Content(
                role="user",
                parts=[types.Part(text="What parental leave benefits do I get?")],
            ),
            types.Content(
                role="model",
                parts=[types.Part(text="Which country are you in?")],
            ),
            types.Content(
                role="user",
                parts=[types.Part(text="I'm in France.")],
            ),
        ],
    )
    assert _last_user_text(request) == "I'm in France."
