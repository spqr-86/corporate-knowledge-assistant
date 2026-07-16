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

## Review 16.07 (второй пост-сдача раунд — записано, не исправлено)

Два code-reviewer агента (корректность+безопасность / архитектура). Тесты 57 passed, критических нет. Находки НОВЫЕ поверх раунда 11.07; ждут решения Петра, ничего пока не чинилось.

Приоритетное (по убыванию):
1. **Memory-recall кросс-загрязнение юрисдикции** (`guardrails/context_perimeter.py` `_country_from_memory`, ~123-142) — извлекает страну из ЛЮБОГО прошлого memory-события, включая ответы самого агента. Агент упомянул страну в примере в прошлой сессии → подхватится как «названная пользователем». Бьёт по ядру продукта («не угадывает юрисдикцию») и по заявленному в WRITEUP детерминизму (`_extract_country` по frozenset недетерминирован при нескольких странах). Фикс: искать только события role=user / хранить «established country» отдельным state-ключом, не переизвлекать из свободного текста. — **единственный блокер корректности по мнению арх-ревьюера.**
2. **RBAC-гард fail-open** (`guardrails/role_binding.py:23,29-31`) — завязка на строку `_TARGET_TOOL_NAME="search_handbook"`. Второй retrieval-тул или ADK-namespacing → гард молча не сработает, LLM-роль пройдёт насквозь (RBAC bypass). Юнит-тесты дрейф не ловят. Фикс: e2e-тест на реальный toolset + fail-closed дефолт (role=employee для незнакомых retrieval-тулов). Это долг из §49 (RBAC-registry).
3. **RBAC уже обещаний WRITEUP** (`config.py:25-27`) — гейтится только `total-rewards/compensation`; stock-options/incentives/individual-comp открыты роли employee, хотя WRITEUP обещает скрывать comp-документы. Расширить префиксы ИЛИ сузить формулировку.

Помельче: весь `os.environ` в MCP-сабпроцесс (`agents/hr_domain_agent.py:50`, нужен whitelist); sentinel `"For context:"` коллизится с пользовательским вводом (`context_perimeter.py:92`); `_country_from_memory` ловит только ValueError (упадёт весь turn при durable memory-бэкенде); глобальный `last_turn_observer` не concurrency-safe (`agent.py:120,146`); `create_hr_ticket.py:33` `.strip()` без None-guard; observability без session_id/turn_id + завышенный первый latency; `USER_ID="petr"` захардкожен в публичном репо; `eval/report.py:52` float `== 1.0`.

Оценка портфолио: **8/10**. До 9-10 — закрыть п.1-2 и мелкую чистку.

### Fixes 16.07 (вариант «демо-полировка», TDD + adversarial-review)

Исправлено (66/66 non-smoke + live smoke зелёные):
- **Memory-recall** (`context_perimeter.py`): `_country_from_memory` читает только `content.role=="user"` и пропускает свои же `For context:`-заметки — юрисдикция из ответов агента больше не подхватывается. `_extract_country` переписан детерминированно через `_countries_in_text` + канонизацию алиасов (uk/usa/US); при 0 ИЛИ >1 стране возвращает None (сравнение «France vs Canada» не устанавливает юрисдикцию, а не выбирает случайную из frozenset). `search_memory` обёрнут в `except Exception` → деградация в «спросить», а не 500 на durable-бэкенде.
- **Fail-closed RBAC** (`role_binding.py` + `config.py`): бинд роли из session state, если тул в `settings.rbac_gated_tools` ИЛИ его сигнатура декларирует параметр `role` (`_tool_declares_role` — inspect.signature для FunctionTool, `_get_declaration().parameters.properties` для MCP) ИЛИ `role` уже в args. Закрывает дрейф: новый/переименованный retrieval-тул с пермиссивным дефолтом, вызванный LLM БЕЗ role, всё равно перебивается на employee.
- **Чистка**: env-whitelist MCP-сабпроцесса (`_mcp_subprocess_env`) — добавлены TLS (`SSL_CERT_FILE/DIR`, `REQUESTS_CA_BUNDLE`), locale (`LANG/LC_ALL`), `TMPDIR` после adversarial-находки (иначе прод-TLS падал бы при кастомном CA); `USER_ID` default `petr` → `demo-user`.

Осталось в backlog (не блокеры, осознанно отложено):
- Sentinel `For context:` — plaintext-префикс, коллизирует с пользовательским вводом. Нужен структурный metadata-маркер на Content (правит и точку инъекции) — отдельная задача.
- RBAC-обещание WRITEUP шире реализации (stock-options/incentives открыты) — решить: расширить `DEFAULT_RESTRICTED_PREFIXES` или сузить формулировку WRITEUP.
- Мелочь из ревью 16.07: observability без session_id/turn_id; `last_turn_observer` не concurrency-safe; `create_hr_ticket.strip()` без None-guard; `eval/report.py` float `==`.

## Definition of Done (capstone submission)

See PLAN.md §12 for the full checklist. Short version: agent runs end-to-end
live (not mocked), 3+ course concepts demonstrably shown (ADK multi-agent, MCP
server, Agent Skill, security guardrail), tests + smoke test green, eval set
run at least once, README with pitch written, repo pushed.
