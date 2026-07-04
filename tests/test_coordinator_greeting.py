"""Tests for the Coordinator's greeting behavior.

ANCHOR: test_coordinator_greeting
A judge/outsider opening the web UI cold has no idea what to ask. On a
greeting-like first message the Coordinator should proactively suggest 2-3
concrete example questions instead of just waiting or saying "ask me
anything" — proxy-checked via keyword presence, not exact text (LLM output
is non-deterministic even at temperature=0, see PLAN.md §3.5).
"""

import os

import pytest

from agent import ask

pytestmark = pytest.mark.smoke

requires_openai_key = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set — greeting test needs a live model call.",
)


@requires_openai_key
@pytest.mark.asyncio
async def test_greeting_surfaces_example_questions():
    answer = await ask("hi")
    assert answer
    lowered = answer.lower()
    assert "?" in answer
    assert any(kw in lowered for kw in ("pto", "leave", "handbook", "policy", "ticket"))
