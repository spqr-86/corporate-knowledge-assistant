"""End-to-end smoke test for the ADK agent loop.

ANCHOR: test_agent_e2e
Role: reproducible version of the manual live check done on 2026-07-03
      (agent → LLM → tool call → cited answer). Run this after every commit
      to catch integration breakage (ADK config, model wiring, tool wiring)
      before it reaches a demo. Requires OPENAI_API_KEY in the environment —
      skips (not fails) if missing, so CI/offline runs don't break on it.
"""

import os

import pytest

from agent import ask

pytestmark = pytest.mark.smoke

requires_openai_key = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set — smoke test needs a live model call.",
)


@requires_openai_key
@pytest.mark.asyncio
async def test_agent_answers_with_citation():
    answer = await ask("What parental leave benefits does GitLab offer in France?")
    assert answer, "Agent returned an empty response."
    assert "handbook" in answer.lower() or ".md" in answer.lower(), (
        "Agent answered without citing a handbook source — expected a "
        "relative_path citation per the agent's instruction."
    )
