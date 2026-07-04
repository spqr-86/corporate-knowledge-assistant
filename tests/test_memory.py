import pytest
from google.genai import types

import agent as agent_module
from agent import APP_NAME, USER_ID, ensure_session, get_runner, save_session_to_memory


@pytest.fixture(autouse=True)
def fresh_runner():
    """Each test gets a clean process-level runner/session/memory state."""
    agent_module._runner = None
    yield
    agent_module._runner = None


@pytest.mark.asyncio
async def test_ensure_session_creates_session_with_role_state():
    session = await ensure_session("s1", role="manager")
    assert session.state["user_role"] == "manager"


@pytest.mark.asyncio
async def test_ensure_session_is_idempotent_and_keeps_history():
    await ensure_session("s1", role="employee")
    runner = get_runner()
    await runner.session_service.append_event(
        session=await runner.session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id="s1"
        ),
        event=_user_event("I am in France."),
    )

    session = await ensure_session("s1", role="employee")

    assert len(session.events) == 1  # not recreated from scratch


@pytest.mark.asyncio
async def test_save_session_to_memory_makes_it_searchable():
    await ensure_session("s1", role="employee")
    runner = get_runner()
    await runner.session_service.append_event(
        session=await runner.session_service.get_session(
            app_name=APP_NAME, user_id=USER_ID, session_id="s1"
        ),
        event=_user_event("I am based in France."),
    )

    await save_session_to_memory("s1")

    response = await runner.memory_service.search_memory(
        app_name=APP_NAME, user_id=USER_ID, query="France"
    )
    assert len(response.memories) > 0


def test_hr_domain_agent_has_load_memory_tool():
    from google.adk.tools import load_memory

    from agents.hr_domain_agent import hr_domain_agent

    assert load_memory in hr_domain_agent.tools


def _user_event(text: str):
    from google.adk.events.event import Event

    return Event(
        author="user",
        content=types.Content(role="user", parts=[types.Part(text=text)]),
    )
