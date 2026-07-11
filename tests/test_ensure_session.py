import pytest

import agent


@pytest.fixture(autouse=True)
def _fresh_runner(monkeypatch):
    monkeypatch.setattr(agent, "_runner", None)


@pytest.mark.asyncio
async def test_ensure_session_creates_with_role():
    session = await agent.ensure_session("s1", role="manager")
    assert session.state["user_role"] == "manager"


@pytest.mark.asyncio
async def test_ensure_session_same_role_ok():
    await agent.ensure_session("s2", role="employee")
    session = await agent.ensure_session("s2", role="employee")
    assert session.state["user_role"] == "employee"


@pytest.mark.asyncio
async def test_ensure_session_rejects_role_mismatch():
    """A session created as manager must not be silently reusable with
    role='employee' (or vice versa) — that's a privilege confusion bug."""
    await agent.ensure_session("s3", role="manager")
    with pytest.raises(ValueError, match="role"):
        await agent.ensure_session("s3", role="employee")
    # stored role untouched
    session = await agent.ensure_session("s3", role="manager")
    assert session.state["user_role"] == "manager"
