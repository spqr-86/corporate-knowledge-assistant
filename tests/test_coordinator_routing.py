"""Tests for Coordinator → HR Domain Agent delegation.

ANCHOR: test_coordinator_routing
Verifies routing CATEGORY (was the HR sub-agent actually invoked / did a
citation-bearing answer come back), not exact response text — LLM decisions
are non-deterministic even at temperature=0 (see PLAN.md §3.5), so exact
string matching on agent output would be flaky by design.
"""

import os

import pytest

from agent import ask

pytestmark = pytest.mark.smoke

requires_openai_key = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set — routing test needs a live model call.",
)


@requires_openai_key
@pytest.mark.asyncio
async def test_hr_question_is_answered_via_handbook():
    """An HR-domain question should be routed to the HR sub-agent and
    answered with a handbook citation — proxy for 'routing worked', since
    we can't assert on the exact transfer_to_agent event without wiring up
    a custom event-capturing runner."""
    # Names a country so the context-perimeter guardrail (added later, see
    # guardrails/context_perimeter.py) doesn't short-circuit with a
    # clarifying question instead of routing through to a handbook answer.
    answer = await ask("How many weeks of parental leave does GitLab offer in the US?")
    assert answer
    assert ".md" in answer.lower() or "handbook" in answer.lower()
