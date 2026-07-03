"""HR Domain Agent — the sole domain sub-agent for now.

ANCHOR: hr_domain_agent
Role: sub-agent under the Coordinator, handles HR-policy questions using
      the handbook_search tool. Model-agnostic via ADK's LiteLLM connector
      (OpenAI gpt-4o-mini — Gemini quota is blocked, see PLAN.md §6).
Input: delegated user query (via Coordinator's transfer_to_agent).
Output: cited answer grounded in tools/handbook_search.py results.
Extension point: this is domain plugin #1 (HR). Adding a second domain
(e.g. Engineering) means adding another sub-agent module here and listing
it in the Coordinator's sub_agents in agent.py — no change to this file.
"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import FunctionTool

from guardrails.context_perimeter import context_perimeter_guardrail
from guardrails.dow_limit import dow_guardrail
from tools.handbook_search import search_handbook

MODEL_ID = LiteLlm(model="openai/gpt-4o-mini")

handbook_tool = FunctionTool(func=search_handbook)

hr_domain_agent = Agent(
    model=MODEL_ID,
    name="hr_domain_agent",
    description=(
        "Handles employee questions about HR policies, benefits, hiring and "
        "total rewards using the GitLab Handbook HR subset."
    ),
    instruction="""
You are the HR Domain Agent for the Corporate Knowledge Assistant. You
answer employee questions about HR policies, benefits and hiring using
ONLY the 'search_handbook' tool — never answer from memory.

Rules:
1. Always call search_handbook with the user's question (or a focused
   keyword version of it) before answering.
2. If the tool returns no results, say you could not find this in the
   handbook subset (total-rewards, hiring, people-policies) and suggest
   the user rephrase or ask HR directly — do not guess.
3. If the question depends on the employee's country/entity (e.g.
   benefits, leave law) and the tool results show entity-specific docs
   (e.g. france-sas.md, canada-corp-benefits.md), ask which country/
   entity the user is in before giving a definitive answer, unless they
   already stated it.
4. Always cite the relative_path of the handbook doc(s) you used.
""",
    tools=[handbook_tool],
    before_model_callback=context_perimeter_guardrail,
    before_tool_callback=dow_guardrail,
)
