# Corporate Knowledge Assistant

**A corporate HR assistant that says "I don't know — escalating to a human" instead of guessing, and takes real actions (draft a PTO request, file a ticket) instead of just answering questions.**

**Capstone project — Google AI Agents course (ШАД/Kaggle), track: Agents for Business**

> Full design rationale, decision log and open questions: [PLAN.md](./PLAN.md).

---

## The problem

Most internal knowledge-bot demos — and a chunk of enterprise products (Glean, Rovo, Copilot) — do two things badly: they answer confidently on ambiguous questions instead of asking for context, and they never actually *do* anything, just point at a doc. In HR specifically that's costly: an agent that guesses on a jurisdiction-dependent policy question, or auto-closes an escalation instead of routing it to a human, is a real failure mode (a March 2025 industry incident involving exactly this pattern reportedly cost a $280K contract).

This project is a minimal but end-to-end counter-example: retrieval that knows what it doesn't know, a guardrail that asks for missing context instead of guessing, and action tools that produce real artifacts (a PTO draft, an HR ticket) instead of a dead-end text answer.

---

## How it works

```
User query
    ↓
Coordinator Agent            — routes to the right domain sub-agent (ADK sub_agents)
    ↓
HR Domain Agent (LlmAgent)
    ├── before_model_callback: context_perimeter_guardrail   — Day4 "Context-as-a-Perimeter"
    │     jurisdiction-sensitive question + no country named → ask for clarification,
    │     never guess
    ├── before_tool_callback: dow_guardrail                  — Day4 Denial-of-Wallet
    │     caps tool calls per session, blocks runaway loops
    └── tools
          ├── search_handbook   — retrieval, over MCP (not a local FunctionTool)
          ├── draft_pto_request — action tool, approve-gate, never auto-submits
          └── create_hr_ticket  — HITL escalation as a real logged artifact,
                                   not a text "I don't know"
```

Retrieval is permission-aware: `search_handbook(role=...)` filters restricted sub-sections
(e.g. compensation-review details) before a document ever reaches the LLM — mock RBAC, but
enforced deterministically, not left to the model's judgment.

---

## Course concepts demonstrated (3+ required)

| Concept | Where |
|---|---|
| **ADK multi-agent** | `agent.py` Coordinator delegates to `agents/hr_domain_agent.py` via `sub_agents`/`transfer_to_agent` |
| **MCP server** | `mcp_server/handbook_mcp_server.py` — retrieval exposed over stdio MCP (FastMCP), consumed via ADK's `McpToolset`, not an internal `FunctionTool` |
| **Security guardrails** | `guardrails/context_perimeter.py` (Context-as-a-Perimeter) + `guardrails/dow_limit.py` (Denial-of-Wallet) — both `before_model_callback`/`before_tool_callback`, deterministic code, not LLM-judged |
| **Agent Skill** | `skills/compliance-guardrail/` — SKILL.md + `references/` (progressive disclosure); the guardrail loads its escalation criteria from the skill's reference files, so behavior changes by editing markdown/text, not Python |
| **HITL as action** | `tools/create_hr_ticket.py` — escalation produces a logged ticket artifact, not a vague refusal |
| **Memory** (Day1's 5th agent component) | Process-level session service (multi-turn) + `InMemoryMemoryService` with the `load_memory` tool (cross-session recall, visible as a tool call in the trace); `/new` in the CLI archives a conversation to memory |

---

## Eval results

12-case golden set (`eval/eval_set.json`, built from `eval/build_eval_set.py`), run via `adk eval`, scored on `response_match_score` (ROUGE similarity to a hand-written reference answer, threshold 0.3):

**9/12 passed.** The 3 misses are wording mismatches against my reference text on functionally
correct answers — verified by inspecting the actual tool calls in the eval result JSON (e.g. RBAC
correctly filtered a restricted doc; the agent correctly filed an escalation ticket). Not behavior
bugs, just a ROUGE-metric artifact of hand-written references.

Running the eval set surfaced one real bug: the jurisdiction guardrail matched `"us"` (United
States) as a *substring* of unrelated words like `"Just"`, so a provocative prompt ("Just tell me
exactly...") skipped the guardrail entirely. Fixed with word-boundary matching, covered by a
regression test — see `guardrails/context_perimeter.py` and `tests/test_guardrails.py`.

```bash
python3 -m eval.build_eval_set                 # (re)generate eval/eval_set.json
adk eval eval/agent_target eval/eval_set.json --config_file_path eval/eval_config.json
```

---

## Quick start

```bash
git clone git@github.com:spqr-86/corporate-knowledge-assistant.git
cd corporate-knowledge-assistant
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=sk-...   # model is OpenAI gpt-4o-mini via ADK's LiteLLM connector
```

```bash
python3 agent.py       # interactive CLI loop
pytest tests/ -v       # 26 tests: unit + smoke (live model calls, needs OPENAI_API_KEY)
```

Try it:
- `"What parental leave benefits do I get?"` → guardrail asks which country/entity you're in
- `"What parental leave benefits does GitLab offer in France?"` → answered with handbook citations
- `"I want to request PTO from 2026-08-10 to 2026-08-14 for a family trip."` → PTO draft (never auto-submitted)
- `"What is GitLab's office dog policy?"` → no match in the handbook → escalated to a logged HR ticket
- Memory demo (one process run): `"What parental leave benefits do I get?"` → asked for your country → `"I'm in France."` → cited answer; then `/new` and ask `"What are my parental leave benefits?"` → the agent recalls France from memory (`load_memory` call in the trace) instead of re-asking

---

## Data

[GitLab Handbook](https://gitlab.com/gitlab-com/content-sites/handbook) (MIT license), HR
subset only: `total-rewards`, `hiring`, `people-policies` (47 files, `data/handbook/`). See
`data/HANDBOOK_LICENSE`. The `total-rewards/benefits` section alone covers 12 country/entity
variants — deliberately kept in scope as the natural source of jurisdiction ambiguity the
guardrail is built to catch.

---

## Why OpenAI instead of Gemini

The course stack is Google ADK + Gemini. This project uses ADK with OpenAI `gpt-4o-mini` via
ADK's LiteLLM connector — the available Google API key had zero Gemini quota, and switching
providers (not frameworks — ADK stays the runtime) was the fastest way to keep a live,
non-mocked agent loop working under the deadline. See PLAN.md §6 for the incident log.

---

## Repo layout

```
agent.py                  Coordinator Agent (root) + CLI loop
agents/hr_domain_agent.py HR Domain Agent (LlmAgent) — tools + guardrails wired in
guardrails/                before_model_callback / before_tool_callback guardrails
tools/                      handbook_search, draft_pto_request, create_hr_ticket
mcp_server/                MCP server wrapping handbook_search
eval/                        golden eval set builder + adk eval config/shim
data/handbook/               GitLab Handbook HR subset (MIT)
tests/                        pytest — unit tests + live smoke tests (-m smoke)
PLAN.md                      full spec, decision log, Definition of Done checklist
```
