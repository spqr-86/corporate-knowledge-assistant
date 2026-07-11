# AGENTS.md — Corporate Knowledge Assistant

Cross-tool agent instructions (AGENTS.md convention). Full spec/status lives in
PLAN.md — read it whenever returning to this project after a gap.

## Stack

- Python 3.12, Google ADK 2.3.0
- Model: OpenAI `gpt-4o-mini` via ADK's LiteLLM connector (not Gemini — quota
  blocked, limit 0, on the current Google API key)
- venv in project root: `source venv/bin/activate`

## Commands

- Run agent (interactive CLI): `python3 agent.py`
- Run tests: `pytest tests/ -v`
- Run smoke test (fast end-to-end sanity check, run after every commit):
  `pytest tests/test_agent_e2e.py -v -m smoke`
- Format/lint (auto via hook on Claude Code, run manually otherwise): `ruff format . && ruff check --fix .`
- Export OpenAI key before running anything live:
  `export OPENAI_API_KEY=$(grep '^OPENAI_API_KEY=' ~/projects/ai/regulatory-rag/.env | cut -d= -f2-)`

## Conventions

- TDD: test before implementation for any new tool/callback
- Conventional commits, English, one logical unit per commit (see PLAN.md §9
  for the planned commit sequence) — commit right after tests go green, push
  immediately after (backup priority over batching, given the tight deadline)
- Guardrails are ADK callbacks (`before_model_callback`/`before_tool_callback`),
  NOT separate LLM agents and NOT ADK Plugins (Plugins silently don't fire in
  ADK Web UI, only in `adk run` CLI)
- Structured logging (structlog) for agent steps once added — not print()
- Type hints on all new functions

## Boundaries — don't touch without asking

- `data/handbook/` — do not regenerate/re-clone without confirming scope with Petr
  (subset choice was a deliberate decision, see PLAN.md §2)
- `.env` — never commit, never print its contents
- GitHub repo creation/push to a shared or public remote — confirm before first push

## Post-submission hardening (11.07, post-capstone review)

Capstone уже сдан (07.07); это — ревью/дебаг/рефакторинг по запросу Петра поверх сданной версии, не блокирует ничего.
- `dc32210`/`ff0c485`: search_handbook возвращает `{"status":"error"}` вместо raise на сбое OpenAI; DoW-счётчик на `temp:`-state (сброс каждый ход, не копится на всю сессию); `ensure_session` кидает ValueError на mismatch role.
- `38f5db8`: MCP-сабпроцесс спавнился `"python3"` (резолвится по PATH, терял venv) → `sys.executable`.
- `e354415`/`95379ef`: embedder seam (`_embed` подменяемый провайдер) + fake bag-of-words эмбеддер в тестах — retrieval-тесты (11 шт.) идут без `OPENAI_API_KEY`; центральный `config.py` (frozen `Settings` + `CKA_*` env-оверрайды) вместо констант в 5 файлах.
- Тесты: 59/59 non-e2e зелёные. Известный флейк — `test_coordinator_routing` (живой LLM-вызов), не связан с изменениями.
- Осталось опционально (не сделано, ждёт запроса): RBAC-registry вместо хардкода имени тула в role_binding; RBAC не закрывает stock-options/incentives (решить осознанно ли); os.environ целиком в MCP-сабпроцесс; importlib-хак в eval/agent_target.

## Definition of Done (capstone submission)

See PLAN.md §12 for the full checklist. Short version: agent runs end-to-end
live (not mocked), 3+ course concepts demonstrably shown (ADK multi-agent, MCP
server, Agent Skill, security guardrail), tests + smoke test green, eval set
run at least once, README with pitch written, repo pushed.
