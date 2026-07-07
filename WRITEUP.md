# Corporate Knowledge Assistant — an HR agent that knows when it doesn't know

**Track: Agents for Business**

Internal knowledge bots cost companies money when they're confidently wrong
or quietly useless — an HR agent that guesses a jurisdiction or dead-ends on
"I don't know" is a liability, not a product. Corporate Knowledge Assistant
is an HR agent for employees and HR teams that does the opposite: it asks
when it's unsure, remembers the answer, and takes real action instead of
just talking.

## What it does

It answers employee questions over GitLab's public HR Handbook (benefits,
leave, hiring — 47 files, MIT license). Concretely, it:

1. **Answers from the handbook with citations** — every answer names the
   source file, never guesses from memory.
2. **Asks for clarification instead of guessing** — if the answer depends on
   the employee's country/entity and none was named, it asks, rather than
   picking one jurisdiction and hoping.
3. **Remembers the country across conversations** — say it once, it's not
   asked again next session.
4. **Drafts a PTO request** — dates and reason in, a ready-to-submit draft
   out (never auto-submitted — the employee still files it).
5. **Escalates to a real HR ticket when the handbook has no answer** — not
   a dead-end "I don't know."
6. **Gates access by role, not by what the user claims to be** — a
   compensation-review document is invisible to an "employee" session even
   if the model is told "I'm a manager" in the prompt.

## The problem

Most internal knowledge bots — and a chunk of enterprise products (Glean,
Rovo, Copilot) — fail in one of two ways: they answer confidently on
questions they shouldn't (wrong-jurisdiction HR advice, hallucinated
policy), or they never do anything beyond pointing at a document. Both
failure modes are expensive in HR specifically: a March 2025 industry
incident where an agent auto-closed an escalation instead of routing it to
a human reportedly cost a $280K contract. Refusing to guess and taking real
action are not table stakes for these products — they're the differentiator
this project is built around.

## Value proposition

Permission-aware retrieval is table stakes now (Glean/Rovo do it). What
isn't commoditized is HITL triggered by *confidence and ambiguity*, not
just write-approval — Moveworks deliberately limits agent autonomy on
sensitive HR cases (grievances) to intake/routing only, direct industry
confirmation that "less confidence" is a feature here, not a limitation.
For the **Agents for Business** track specifically: this is expense-report-
adjacent HR ops — a document Q&A system that also files real HR/PTO
paperwork, so the business value isn't just "faster search," it's fewer
wrong-jurisdiction answers and fewer questions that silently die instead of
reaching a human.

## Course concepts used (6, course requires 3+)

| Concept | Implementation |
|---|---|
| **ADK multi-agent** | `Coordinator` agent (root) delegates to an `hr_domain_agent` sub-agent via ADK's `sub_agents`/`transfer_to_agent` |
| **MCP server** | Retrieval (`search_handbook`) is wrapped as a stdio MCP server (FastMCP) and consumed via ADK's `McpToolset` — a real subprocess round-trip, not an internal `FunctionTool` |
| **Agent Skill** | `skills/compliance-guardrail/` — SKILL.md + `references/*.txt` (Day3 progressive disclosure); the guardrail loads its escalation criteria from these files at import time, so behavior changes by editing text, not Python |
| **Security guardrails** | Two deterministic `before_model_callback`/`before_tool_callback` hooks, not LLM judgment: **Context-as-a-Perimeter** (asks for missing jurisdiction) and **Denial-of-Wallet** (caps tool calls per session) |
| **HITL as action** | `create_hr_ticket` produces a logged artifact on a no-match, not a text refusal; `draft_pto_request` is an approve-gated action tool |
| **Memory** | Process-level session (multi-turn) + `InMemoryMemoryService` for cross-session recall (`load_memory` tool; the perimeter guardrail also reads memory and injects the remembered country so recall is deterministic, not model-whim) — the 5th agent component from Day1 (Model/Tools/Memory/Orchestration/Deployment) |

## Architecture

```
User query
    v
Coordinator Agent  --sub_agents-->  HR Domain Agent (LlmAgent)
                                      |-- before_model_callback: context_perimeter_guardrail
                                      |     jurisdiction-sensitive + no country -> check memory -> ask or proceed
                                      |-- before_tool_callback: [bind_role_from_session, dow_guardrail]
                                      |     role from session.state (never from the LLM) + tool-call rate limit
                                      `-- tools:
                                            search_handbook   (MCP stdio server, permission-filtered)
                                            draft_pto_request (approve-gated action)
                                            create_hr_ticket  (HITL escalation as artifact)
                                            load_memory       (cross-session recall)
```

Guardrails are plain Python callbacks, never separate LLM agents — a
guardrail implemented as an LLM call can be talked out of firing; a
callback cannot. `context_perimeter_guardrail` checks cross-session memory
*before* asking the clarifying question, so a returning user isn't re-asked
what they already said.

```python
async def context_perimeter_guardrail(callback_context, llm_request):
    text = _last_user_text(llm_request)
    if not is_ambiguous_jurisdiction_query(text):
        return None  # let the LLM answer normally
    remembered = await _country_from_memory(callback_context)
    if remembered:
        inject_context(llm_request, remembered)  # answer for it, no re-ask
        return None
    return LlmResponse(content=...)  # ask for the country
```

Recall is deterministic on purpose: the guardrail reads the country from
memory and injects it into the request itself, rather than hoping the model
volunteers a `load_memory` call (gpt-4o-mini did so unreliably).

## Built the agentic-engineering way, not vibed

Day1 draws a spectrum from vibe coding to agentic engineering, and the
difference isn't whether AI writes the code — it's how much structure and
verification surrounds its output. Every feature here went through
brainstorm -> spec -> TDD -> live verification -> code review, with Claude
Code as the driver, not a one-shot prompt. That process is what actually
caught the bugs below — not a user filing an issue later.

## What we found (evidence, not just design)

A code review (8 automated finder passes + adversarial verification) and
live testing surfaced real bugs, each closed with a regression test:

- **RBAC bypass**: `role` was originally an LLM-controllable tool
  argument — a prompt like "I'm a manager" could grant access to a
  restricted document. Fixed by binding `role` to `session.state`
  (set once at session creation) via a `before_tool_callback` that
  overwrites whatever the model tries to pass — closes the exploit
  *and* keeps the feature demoable (start a session as a real manager).
- **Guardrail false negative**: `"us"` (United States) matched as a
  *substring* of `"just"`, so a provocative query ("Just tell me
  exactly...") skipped the jurisdiction check entirely. Fixed with
  word-boundary + case-sensitive matching (lowercase "us" is usually a
  pronoun, not a country).
- **Guardrail false positive**: `"leave"` is a jurisdiction-sensitive
  term, but the agent's own instructions route "take leave" bookings
  to `draft_pto_request` — the guardrail was blocking its own action
  tool. Fixed generally: an explicit date in the query now signals an
  action request, not a lookup.
- **Memory recall flake**: cross-session recall depended on the model
  volunteering a `load_memory` call, which gpt-4o-mini did unreliably, so a
  returning user got a generic answer instead of their remembered country.
  Fixed by making it deterministic — the perimeter guardrail reads the
  country from memory and injects it into the request itself; recall went
  from intermittent to a stable pass.

## Engineering practice

- **TDD throughout** — 56 tests, written before each tool/callback, not
  after; every bug above was caught because a test failed for the *wrong*
  reason first (proving it tested real behavior).
- **`adk eval` golden set** — 18 cases across routing/ambiguous-jurisdiction/
  action/escalation/permission categories; 18/18 on tool-trajectory match
  (did the agent call the right tools in the right order), the metric that
  actually captures correct agent behavior here.
- **Spec-driven** — `PLAN.md` is a living spec (Day5 pattern): constitution,
  architecture, decision log, and a checked-off Definition of Done.

## Limitations & next steps

- Retrieval is embedding-based (OpenAI `text-embedding-3-small`, cosine over
  a disk-cached index) — good for this 47-file subset; a full handbook would
  want a managed vector store (e.g. Vertex AI Vector Search) rather than an
  in-process matrix.
- Memory is in-process (`InMemoryMemoryService`) — swapping in Vertex AI
  Memory Bank is a drop-in replacement, no logic changes needed (the code
  already talks to the `BaseMemoryService` interface).
- One domain (HR) — the Coordinator/sub-agent structure is built to add
  more (`sub_agents=[hr_domain_agent, eng_domain_agent, ...]`) without
  changing this file.

## Links

- **Code**: [github.com/spqr-86/corporate-knowledge-assistant](https://github.com/spqr-86/corporate-knowledge-assistant) — full test suite (`pytest tests/`), `PLAN.md` for the complete spec and decision log, `README.md` for setup instructions.
- **Demo video**: [youtu.be/xOeH6O2ecpM](https://youtu.be/xOeH6O2ecpM)
