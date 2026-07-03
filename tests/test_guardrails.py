from google.adk.models.llm_request import LlmRequest
from google.genai import types

from guardrails.context_perimeter import (
    _first_user_text,
    is_ambiguous_jurisdiction_query,
)


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


def test_first_user_text_ignores_transfer_to_agent_synthesized_notes():
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
    assert _first_user_text(request) == "What parental leave benefits do I get?"
