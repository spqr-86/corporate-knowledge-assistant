# Memory — Design Spec

**Date:** 2026-07-04
**Status:** approved (Petr, Telegram, 2026-07-04)
**Scope:** session-level multi-turn memory + cross-session memory via ADK MemoryService.

## Why

The agent is currently stateless: `ask()` builds a fresh `InMemorySessionService`
per call, so every question is the first question. Two consequences:

- The context-perimeter guardrail's clarifying question is a dead end — the
  user answers "France" into a brand-new session that never saw the question.
- Day 1 of the course names Memory as one of the five agent components
  (Model / Tools / Memory / Orchestration / Deployment); we demonstrate four.

## Decisions (with alternatives considered)

1. **Both layers, not just one** — session multi-turn AND cross-session memory.
   Session memory alone was the cheap option, but cross-session memory is
   pointless without it (MemoryService indexes completed sessions), and it
   adds a demonstrable course concept.
2. **`load_memory` tool, not `preload_memory`** — researched: official ADK
   docs treat both as equal options; Google samples lean Preload; but Load
   produces a visible tool call in the trace, which is what course judges
   inspect. Instruction must nudge the model to use it (official docs'
   pattern).
3. **`/new` CLI command + save-on-exit** — demo works in a single process
   run: talk → `/new` (session → `add_session_to_memory`, fresh session
   starts) → agent recalls facts via `load_memory`. Ctrl+C also saves as
   insurance; honest code that gains persistence for free if
   InMemoryMemoryService is later swapped for Vertex AI Memory Bank.
4. **In-process memory only** — `InMemoryMemoryService`; no disk/DB
   persistence. Memory Bank / DB is out of scope for the capstone.

## Design

### 1. Session multi-turn (`agent.py`)

- `session_service: InMemorySessionService` and `runner: Runner` move from
  `ask()` locals to process level (module-level lazy or created in `main()`
  and passed down).
- `ask(question, role=..., session_id=...)` gains a `session_id` param;
  creates the session only if it doesn't exist yet (state seeded with
  `user_role` at creation).
- CLI keeps one live session across loop iterations.

**Guardrail fix that this forces:** `context_perimeter._first_user_text`
currently reads the FIRST user content in the request. In a multi-turn
session, request contents accumulate history, so the guardrail would forever
re-judge turn 1's text (confirmed almost-bug from the code review — it was
unreachable only because sessions were single-turn). Change to "last real
user message", where "real" excludes the synthesized `For context:`
tool-transfer notes that transfer_to_agent injects as user-role contents.

### 2. Cross-session memory

- `Runner(..., memory_service=InMemoryMemoryService())`.
- `hr_domain_agent.tools += [load_memory]` (ADK built-in).
- Instruction addition: before asking the user which country/entity they're
  in, call `load_memory` first — they may have said it in a past
  conversation; only ask if memory has nothing.

### 3. CLI (`main()`)

- `/new` command: `await memory_save(current_session)`; start a fresh
  session (new session_id, same role/state seeding).
- Ctrl+C / EOF: save current session to memory before exit.
- Print a hint line at startup: commands `/new`, Ctrl+C.

### 4. Testing

- Unit: multi-turn session accumulates history (two `ask()` calls, same
  session_id, second sees first's content); `/new` flow calls
  `add_session_to_memory`; `_last_user_text` regression tests (multi-turn +
  transfer-notes filtering, replacing the `_first_user_text` ones).
- Smoke (live, `-m smoke`): conversation 1 "I'm in France — what parental
  leave do I get?" → save to memory → new session → "What are my parental
  leave benefits?" → assert the reply does NOT re-ask for country (memory
  recall worked end-to-end).
- `adk eval` re-run: existing 12 golden cases must not regress (each eval
  case is single-invocation, so last-vs-first user text is equivalent
  there).

### Risks

- `load_memory` reliance on instruction-following (documented 15-18%
  variance) — mitigated by explicit instruction rule; smoke test catches
  total failure, eval keeps baseline honest.
- Changing `_first_user_text` → `_last_user_text` touches guardrail
  behavior; the existing 9 guardrail unit tests plus new regression tests
  gate this.

### Out of scope

- Disk/DB-persistent memory (Vertex AI Memory Bank, sqlite session service).
- Memory for action tools' artifacts (tickets already persist to JSONL).
- README/PLAN.md updates land with the implementation commit.
