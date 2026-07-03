"""Corporate Knowledge Assistant — Coordinator Agent.

ANCHOR: agent
Role: root Coordinator Agent delegating to domain sub-agents via ADK's
      transfer_to_agent mechanism. Currently one domain (HR); adding a new
      domain means adding a sub-agent module under agents/ and listing it
      in sub_agents below — this file's structure doesn't change.
Input: interactive stdin question, or ask(question) programmatically.
Output: printed/returned agent response (final answer after any delegation).
"""

import asyncio
import os

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.hr_domain_agent import hr_domain_agent

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


async def ask(question: str) -> str:
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )
    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )

    content = types.Content(role="user", parts=[types.Part(text=question)])
    final_text = ""
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=content
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = event.content.parts[0].text or ""
    return final_text


async def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(
            "OPENAI_API_KEY not set. Export it before running: export OPENAI_API_KEY=sk-..."
        )
    print(f"{APP_NAME} — ask a question (Ctrl+C to exit)")
    while True:
        try:
            question = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            continue
        answer = await ask(question)
        print(f"\nAgent: {answer}")


if __name__ == "__main__":
    asyncio.run(main())
