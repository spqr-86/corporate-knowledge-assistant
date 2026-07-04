"""Live smoke test for cross-session memory recall.

ANCHOR: test_memory_recall_e2e
Role: reproduces the demo flow — conversation 1 names the country, gets
      archived to memory (/new equivalent), conversation 2 asks a
      jurisdiction-sensitive question and must NOT re-ask for the country
      (the agent should recall it via the load_memory tool).
"""

import os

import pytest

import agent as agent_module
from agent import ask, save_session_to_memory

pytestmark = pytest.mark.smoke

requires_openai_key = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set — memory recall test needs live model calls.",
)


@pytest.fixture(autouse=True)
def fresh_runner():
    agent_module._runner = None
    yield
    agent_module._runner = None


@requires_openai_key
@pytest.mark.asyncio
async def test_agent_recalls_country_from_past_conversation():
    # Conversation 1: user names their country.
    await ask(
        "I'm based in France. What parental leave benefits do I get?",
        session_id="memory-conv-1",
    )
    await save_session_to_memory("memory-conv-1")

    # Conversation 2 (fresh session): same topic, country not named.
    answer = await ask(
        "What are my parental leave benefits?", session_id="memory-conv-2"
    )

    assert answer
    # Must not re-ask for the country — memory recall should supply it.
    assert "which country" not in answer.lower(), (
        "Agent re-asked for the country despite it being available in "
        f"cross-session memory. Answer: {answer!r}"
    )
