"""Compute cost-per-query (CPS) by running a few representative live questions.

ANCHOR: compute_cps
Role: one-off manual script (not a test) — runs sample HR questions through
      the real agent, reads token usage from agent.last_turn_observer after
      each ask(), and prints the average cost per query for the pitch/writeup.
Requires OPENAI_API_KEY exported. Run: python3 scripts/compute_cps.py
"""

import asyncio

import agent

SAMPLE_QUESTIONS = [
    "What parental leave benefits does GitLab offer in France?",
    "How many vacation days do I get per year?",
    "I want to take PTO from 2026-08-01 to 2026-08-10 for vacation.",
]


async def main() -> None:
    costs = []
    for i, question in enumerate(SAMPLE_QUESTIONS):
        session_id = f"cps-{i}"
        await agent.ask(question, session_id=session_id)
        observer = agent.last_turn_observer
        cost = observer.cost_usd()
        costs.append(cost)
        print(
            f"Q{i + 1}: {len(observer.steps)} steps, "
            f"{observer.total_prompt_tokens + observer.total_candidates_tokens} tokens, "
            f"${cost:.6f}"
        )
    avg = sum(costs) / len(costs)
    print(f"\nAverage cost per query (CPS): ${avg:.6f}")


if __name__ == "__main__":
    asyncio.run(main())
