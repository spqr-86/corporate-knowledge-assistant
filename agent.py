"""Corporate Knowledge Assistant — Coordinator Agent.

ANCHOR: agent
Role: root Coordinator Agent delegating to domain sub-agents via ADK's
      transfer_to_agent mechanism. Currently one domain (HR); adding a new
      domain means adding a sub-agent module under agents/ and listing it
      in sub_agents below — this file's structure doesn't change.
Input: interactive stdin question, or ask(question) programmatically.
Output: printed/returned agent response (final answer after any delegation).
Memory: one process-level Runner holds the session service (multi-turn
      within a session) and an InMemoryMemoryService (cross-session recall
      via the load_memory tool). /new in the CLI archives the current
      session to memory and starts a fresh one; exit archives too.
"""

import asyncio
import os
import uuid

from google.adk.agents import Agent
from google.adk.memory import InMemoryMemoryService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.hr_domain_agent import hr_domain_agent
from observability import TurnObserver

APP_NAME = "corporate_knowledge_assistant"
USER_ID = "petr"
SESSION_ID = "dev-session"

root_agent = Agent(
    model=hr_domain_agent.model,
    name="coordinator",
    description="Routes employee questions to the right domain specialist.",
    instruction="""
You are the Coordinator for the Corporate Knowledge Assistant. You do not
answer questions yourself — you delegate every question to the right
domain sub-agent.

Currently the only domain available is HR (policies, benefits, hiring) —
delegate all such questions to 'hr_domain_agent'. If a question is clearly
outside HR (e.g. engineering, security, sales) and no matching domain
sub-agent exists yet, say this assistant currently only covers HR topics.
""",
    sub_agents=[hr_domain_agent],
)


# Process-level runner: one session service (multi-turn history within a
# session) and one memory service (cross-session recall) per process. Lazy
# so tests can reset it between cases.
_runner: Runner | None = None


def get_runner() -> Runner:
    global _runner
    if _runner is None:
        _runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )
    return _runner


async def ensure_session(session_id: str, role: str = "employee"):
    """Get the session, creating it (with user_role seeded) on first use.

    role only applies at creation — an existing session keeps the role it
    was created with (see guardrails/role_binding.py for why role must come
    from session state, never from the model).
    """
    runner = get_runner()
    session = await runner.session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    if session is None:
        session = await runner.session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            state={"user_role": role},
        )
    return session


async def save_session_to_memory(session_id: str) -> None:
    """Archive a finished conversation into cross-session memory."""
    runner = get_runner()
    session = await runner.session_service.get_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=session_id
    )
    if session is not None and session.events:
        await runner.memory_service.add_session_to_memory(session)


last_turn_observer: TurnObserver | None = None


async def ask(
    question: str, role: str = "employee", session_id: str = SESSION_ID
) -> str:
    """role: the requesting user's role (employee/manager/hr_admin), set
    once at session creation from a trusted context — never derived from
    the model's own tool-call arguments (see guardrails/role_binding.py).

    Records a structlog step per tool call/final response and accumulates
    token usage for the turn in `last_turn_observer` (module-level, read by
    scripts/compute_cps.py) — see observability.py."""
    global last_turn_observer
    await ensure_session(session_id, role=role)
    runner = get_runner()
    observer = TurnObserver()

    content = types.Content(role="user", parts=[types.Part(text=question)])
    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=session_id, new_message=content
    ):
        observer.record(event)
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text or ""
    last_turn_observer = observer
    return final_text


async def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY not set. Export it before running: export OPENAI_API_KEY=sk-..."
        )
    role = os.environ.get("USER_ROLE", "employee")
    session_id = f"cli-{uuid.uuid4().hex[:8]}"
    print(
        f"{APP_NAME} — ask a question as role={role} "
        "(/new = archive conversation & start fresh, Ctrl+C to exit)"
    )
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            continue
        if question == "/new":
            await save_session_to_memory(session_id)
            session_id = f"cli-{uuid.uuid4().hex[:8]}"
            print("(conversation archived to memory — starting a new one)")
            continue
        answer = await ask(question, role=role, session_id=session_id)
        print(f"\nAgent: {answer}")
    # archive the last conversation on exit too — becomes real persistence
    # for free if InMemoryMemoryService is swapped for a durable backend
    await save_session_to_memory(session_id)


if __name__ == "__main__":
    asyncio.run(main())
