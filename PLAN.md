# Corporate Knowledge Assistant — Capstone Plan

**Дедлайн:** 06.07.2026 23:59 PT
**Курс:** Google AI Agents (ШАД/Kaggle), трек Agents for Business
**Обязательные концепции курса (3+):** ADK multi-agent ✅, MCP-сервер ✅, agent skills ✅, security/guardrail ✅

---

## 0. Constitution (неизменные правила проекта — пишется первой, не менять без явного решения)

- Стек фиксирован: Python + Google ADK + OpenAI (LiteLLM). Не переключаться на другой фреймворк
  посреди капстона, даже если что-то покажется удобнее.
- TDD на каждый новый tool/callback — тест до кода, без исключений даже под дедлайном.
- Guardrails — только callbacks, не отдельные LLM-агенты и не ADK Plugins (см. AGENTS.md).
- Данные — HR-подкорпус GitLab Handbook (47 файлов), не расширять до капстона без явного решения.
- Commit сразу после зелёных тестов, push сразу после коммита — backup важнее аккуратности батчей.
- Полный список agent-specific dev-практик — §3.5. Полный список dev-практик фундамента проекта
  (AGENTS.md/CLAUDE.md, smoke-first, DoD) — этот раздел + §12.

## 1. Идея (зафиксировано)

Корпоративный ассистент по внутренней документации. Демо-вертикаль на старте — HR-политики (GitLab Handbook, публичные данные), архитектура рассчитана на расширение на другие домены после капстона. Название проекта — **Corporate Knowledge Assistant**, HR — первый domain-plugin, не финальный скоуп.

**Питч:** "Корпоративный ассистент, который умеет сказать «не знаю, зову человека» и реально исполняет действия (черновик заявки, эскалация), а не просто отвечает по документам — то, что 90% демо-ботов и даже часть enterprise-продуктов (Glean/Rovo/Copilot) делают плохо."

## 2. Данные

- Источник: `git clone --depth 1 https://gitlab.com/gitlab-com/content-sites/handbook.git`
- Лицензия: MIT (см. `data/HANDBOOK_LICENSE`) — реюз свободный, с указанием источника
- Взятый подкорпус: `content/handbook/{total-rewards,hiring,people-policies}` → скопирован в `data/handbook/` (47 md-файлов, 1.1 МБ)
- total-rewards включает бенефиты по 12 странам/юрлицам отдельными файлами (US, UK, Канада, Франция, Сингапур, Корея, Австралия, Новая Зеландия, Ирландия, Бельгия, Нидерланды, Финляндия) — источник естественной многозначности "зависит от юрисдикции", топливо для HITL
- Расширение на другие разделы (security, engineering, product и т.д.) — after капстона, не сейчас

## 3. Архитектура (multi-agent, ADK — конкретные примитивы)

Идиоматичный ADK-паттерн: НЕ отдельный "guardrail-агент" как LLM, а **callbacks**
(`before_model_callback`, `before_tool_callback`) на уровне агента + **sub_agents**
для роутинга (Coordinator/Dispatcher pattern). Так безопаснее и дешевле —
guardrail не может "уговорить себя" пропустить проверку, т.к. это код, не LLM-вызов.

```
                        ┌───────────────────────────┐
    user query   ───▶   │   Coordinator Agent         │
                        │   (root, sub_agents=[hr])   │  ← расширяемо: sub_agents=[hr, eng, security, ...]
                        └─────────────┬───────────────┘
                                      │ delegates (транзит вопроса в домен)
                                      ▼
                        ┌───────────────────────────┐
                        │   HR Domain Agent (LlmAgent)│
                        │   tools:                    │
                        │   - search_handbook           (retrieval, уже есть)
                        │   - draft_pto_request          (action)
                        │   - create_hr_ticket            (HITL-эскалация как action)
                        │                              │
                        │   before_model_callback:      │
                        │     context_perimeter_guardrail │ ← Day4 "Context-as-a-Perimeter":
                        │     (страна не указана + затронут   проверяет ВХОД до вызова LLM
                        │      country-specific доклад →       (юрисдикция, чувствительность)
                        │      просит уточнение/эскалирует) │
                        │                              │
                        │   before_tool_callback:       │
                        │     dow_guardrail                │ ← Day4 Denial-of-Wallet защита:
                        │     (счётчик tool-вызовов за      счётчик в session.state,
                        │      сессию, лимит N → блок)      блокирует бесконечные петли
                        └───────────────────────────┘
```

**Компоненты и файлы:**

1. **Retrieval tool** — готово: `tools/handbook_search.py` (keyword search, 3 теста). To-do: permission-aware — параметр `role` (employee/manager/hr_admin) фильтрует под-раздел до поиска (мок RBAC, рыночный стандарт).
2. **Coordinator Agent** (`agent.py`, переименовать текущий `root_agent`) — `Agent(sub_agents=[hr_domain_agent])`, инструкция "delegate HR questions to hr_domain_agent". Сейчас один sub-agent, архитектурно готов к добавлению доменов.
3. **HR Domain Agent** — текущий агент с tools, становится sub-agent коордиантора, а не root.
4. **`context_perimeter_guardrail`** (`guardrails/context_perimeter.py`) — `before_model_callback`: смотрит на текст запроса + retrieval-результаты (если уже были вызваны), решает: пропустить / попросить уточнить страну / сразу эскалировать. Реализация — Agent Skill (см. 4.5), не хардкод в промпте.
5. **`dow_guardrail`** (`guardrails/dow_limit.py`) — `before_tool_callback`: инкремент счётчика в `tool_context.state`, при превышении лимита (напр. 5 tool-вызовов за сессию) — блокирует и возвращает явную ошибку вместо бесконечной петли. Простая, но явно названная Day4-концепция.
6. **Action tools** — новые `FunctionTool`:
   - `draft_pto_request(start_date, end_date, reason)` — генерирует текст заявки + ссылку на policy, возвращает draft (approve-gate — не отправляет автоматически)
   - `create_hr_ticket(question, reason)` — mock-эскалация: пишет запись в лог/файл "тикет создан", это и есть HITL как действие, не текстовый отказ
7. **(Stretch)** Multi-step orchestrator "spланируй parental leave" — `SequentialAgent` из retrieve → check accrued (мок) → draft → notify (мок).
8. **MCP-сервер** — обернуть `search_handbook` (и по возможности action tools) как MCP tools через `google.adk.tools.mcp_tool` — курс явно требует показать MCP, не только внутренние FunctionTool.
9. **Agent Skill** (`skills/compliance-guardrail/SKILL.md`) — сама логика "когда эскалировать" живёт как markdown-скилл с прогрессивным раскрытием (Day3-паттерн), `context_perimeter_guardrail` читает из неё критерии, а не хардкодит их в Python.

## 3.5. Agentic-специфичные dev-практики (приоритет №2, после 4.5)

Из ресёрча индустриальных best practices для agent-систем — не общий software engineering
(TDD/коммиты уже соблюдаются), а то, что специфично для LLM-агентов:

1. [ ] **`adk eval` c golden dataset 5-10 кейсов** — единственный пункт, который явно ждут судьи
   хакатона на ADK. Покрыть: правильный routing (Coordinator→HR), guardrail-триггер срабатывает
   на неоднозначный юрисдикционный вопрос, happy-path каждого tool. Перед фиксацией "правильного"
   ответа в датасет — проверить в Trace view, что агент пришёл к нему не случайно.
2. [ ] **Doработать `dow_guardrail` до настоящего loop-detector**, не просто счётчик: "N попыток
   ИЛИ escalate_to_human" + структурированный лог причины остановки (limit vs error vs loop).
   Закрывает самый частый failure mode в индустрии (68% практиков ограничивают агента ≤10 шагов).
3. [ ] **Pydantic-валидация аргументов tool-вызовов** перед выполнением — защита от "агент вызвал
   tool с кривыми параметрами" (частый failure mode: tool call hallucination).
4. [ ] **Структурированный лог каждого шага** — structlog (не print), поля: tool_name, args,
   latency, decision_reason. Не полноценный OTel-стек — overkill для 3 дней. Достаточно для демо
   + материал для наполнения golden dataset реальными примерами.
5. [ ] (Если время останется) **multi-sample smoke test на guardrail** — 5-10 неоднозначных
   промптов по 3 прогона каждый, зафиксировать % срабатывания — конкретная цифра для питча вместо
   "работает на глаз".

**Важно про тестирование:** LLM-решения (routing, guardrail-триггер) недетерминированы даже при
temperature=0 (до 15-18% variance между запусками). Тестировать не exact-match на текст ответа, а
категорию решения ("вызван ли правильный tool", "сработал ли guardrail") — иначе тесты будут
давать false negatives на ровном месте.

**Подтверждено ресёрчем:** guardrails как callbacks (before_model/before_tool), не как ADK Plugin —
правильный выбор архитектуры (п.3). Plugin-based guardrails молча не работают в ADK Web UI, только
в CLI (`adk run`) — у нас так не сделано, но важно проверить сборку именно через CLI, не полагаться
только на web UI при демо.

**Явно НЕ тратить время:** полноценный OpenTelemetry-стек, калибровка LLM-as-judge, conformance
testing — не окупятся за 1.5 оставшихся дня, судьи капстона не оценят пропорционально затратам.

## 4. Почему это дифференцирует (из ресёрча рынка)

- Permission-aware retrieval — commodity-ожидание рынка (Glean, Rovo) — обязателен, иначе демо наивно.
- HITL по confidence/неоднозначности (не только write-approval) — по нескольким источникам (elementum.ai, galileo.ai) это НЕ commoditized, реальный дифференциатор.
- Moveworks намеренно ограничивает agency на чувствительных HR-кейсах (grievances) — только intake/routing, решение остаётся за человеком — прямое индустриальное подтверждение нашего guardrail-подхода как best practice, не недоделки.
- Реальный кейс-аргумент для питча: агент автозакрыл тикет вместо эскалации → потеря контракта $280K (март 2025, индустриальный инцидент) — конкретика "почему это важно", не абстракция.
- Explicit "не знаю" вместо галлюцинации на низком retrieval score — то, что рынку тоже плохо даётся.

## 4.5. Соответствие курсу (проверено против Day1-5, приоритет №1 перед остальным)

Прямое картирование архитектуры на материалы курса:

| День курса | Концепция | Где в проекте |
|---|---|---|
| Day1 | Harness = Agent, context engineering | Router/guardrail-дизайн — это и есть harness |
| Day2 | MCP как протокол (USB-C аналогия) | MCP-обёртка над retrieval в плане |
| Day3 | Agent Skills (SKILL.md + прогрессивное раскрытие) | **ДЫРА — не оформлено как настоящая структура** |
| Day4 | Security: Effective Trust, Context-as-a-Perimeter, Denial-of-Wallet | Guardrail есть механически, нет терминологии/DoW-защиты |
| Day5 | Spec-Driven Development | PLAN.md и есть спека — уже верно по духу |

**Приоритет №1 (быстрые правки для явного соответствия, перед остальной доработкой):**

1. [ ] Оформить guardrail-логику как настоящую Agent Skill по паттерну Day3:
   ```
   skills/compliance-guardrail/
   ├── SKILL.md          # YAML frontmatter + инструкции когда эскалировать/отказывать
   ├── scripts/           # confidence scoring, ambiguity detection (детерминированный код)
   └── references/        # список country-specific доков, критерии эскалации
   ```
   Загружается по требованию (не в основном system prompt) — прогрессивное раскрытие, не context rot.

2. [ ] Явно назвать security-слой терминами курса в README/питче:
   - Guardrail = реализация **Context-as-a-Perimeter** (Day4): агент проверяет контекст запроса (страна, тип вопроса), не полагается на статичный RBAC
   - Добавить простую защиту от **Denial-of-Wallet** (Day4): rate-limit / max-iterations на agent loop, чтобы предотвратить дорогостоящие бесконечные петли — механика простая (счётчик вызовов LLM/tool за сессию), но явно называется термином курса

Остальное (permission-aware retrieval, action-agent, multi-step orchestrator, MCP-сервер полностью) — доработка после этих двух пунктов, не блокирует "3+ концепции засчитаны".

## 5. Верификация / eval

- ADK имеет свой `adk eval` — гоняет агента против eval-сетов (вопрос → ожидаемая trajectory/ответ).
- To-do: собрать eval-сет 10–15 вопросов: обычные HR-вопросы + пограничные юрисдикционные ("какой у меня декретный отпуск" без указания страны) + провокационные ("скажи точно" на неоднозначном вопросе, проверка что guardrail не галлюцинирует).
- Параллель с прежним подходом на regulatory-rag (датасет + eval) — знакомый Петру паттерн.

## 6. Технический статус на 03.07 (что уже сделано)

- `~/projects/ai/corporate-knowledge-assistant/` — venv, `google-adk==2.3.0` установлен и работает
- `data/handbook/` — 47 файлов скопированы, лицензия сохранена
- `tools/handbook_search.py` — keyword-retriever, 3 pytest теста зелёные
- `agent.py` — рабочий MVP: один ADK `Agent` с `FunctionTool(search_handbook)`, `Runner` + `InMemorySessionService`, async loop
- **Реальный сквозной прогон подтверждён** (после переключения на OpenAI gpt-4o-mini через LiteLLM): вопрос "What parental leave benefits does GitLab offer in France?" → агент вызвал `search_handbook`, ответил с цитатами на конкретные handbook-файлы. Gemini-блокер (квота 0) снят сменой провайдера, не сменой ключа.
- To-do: оформить этот прогон как воспроизводимый smoke-тест (`tests/test_agent_e2e.py`, `pytest -m smoke`) — сейчас это был разовый ручной прогон, не автоматизированная проверка.
- `AGENTS.md` + `CLAUDE.md` (= `@AGENTS.md` + Claude-специфика) — созданы 03.07, фундамент проекта разделён по конвенции 2026 года.

## 7. Следующие шаги (порядок)

1. [x] Получить/подтвердить рабочий API-ключ — снято: переключились на OpenAI (LiteLLM), ключ из regulatory-rag/.env, первый сквозной прогон подтверждён
2. [x] Coordinator Agent + HR Domain sub-agent — реализовано (`agent.py` = Coordinator, `agents/hr_domain_agent.py` = HR sub-agent), delegation через ADK `sub_agents`/`transfer_to_agent`, подтверждено живым прогоном + routing-тестом (`tests/test_coordinator_routing.py`). 5/5 тестов зелёные.
3. [ ] Добавить permission-aware слой в `handbook_search` (роль пользователя → фильтр по под-разделу)
3. [ ] Guardrail-агент: confidence scoring по retrieval score + ambiguity-детектор (юрисдикция не указана + затронуты country-specific доки)
4. [ ] HITL как action-tool (mock "create_hr_ticket" tool), не текстовый ответ
5. [ ] Domain Router agent (пока один plugin: HR), сформировать как SequentialAgent/routing pattern ADK
6. [ ] Action Agent: draft_pto_request tool
7. [ ] (Stretch, если время останется) Multi-step parental leave orchestrator
8. [ ] Обернуть retrieval (+ по возможности actions) в MCP-сервер
9. [ ] Eval-сет 10-15 вопросов + `adk eval` прогон
10. [ ] Демо-скрипт/питч на 2 минуты (перекликается с общей карьерной задачей "питч SIA+WTA")

## 9. Структура репозитория

```
corporate-knowledge-assistant/
├── CLAUDE.md                    # локальный контекст проекта (см. ниже)
├── PLAN.md                      # этот файл — живая спека, обновляется по ходу
├── README.md                    # питч + запуск для судей курса (написать последним)
├── agent.py                     # Coordinator Agent (root) + запуск CLI-луп
├── agents/
│   └── hr_domain_agent.py       # HR Domain Agent (LlmAgent) — вынести из agent.py
├── guardrails/
│   ├── context_perimeter.py     # before_model_callback — Day4 Context-as-a-Perimeter
│   └── dow_limit.py             # before_tool_callback — Denial-of-Wallet защита
├── tools/
│   ├── __init__.py
│   ├── handbook_search.py       # retrieval (готово)
│   ├── draft_pto_request.py     # action tool (to-do)
│   └── create_hr_ticket.py      # HITL-эскалация как action (to-do)
├── skills/
│   └── compliance-guardrail/
│       ├── SKILL.md             # критерии эскалации, YAML frontmatter
│       ├── scripts/              # confidence scoring, ambiguity detection
│       └── references/           # список country-specific доков
├── mcp/
│   └── handbook_mcp_server.py    # MCP-обёртка над retrieval (to-do, п.8 плана)
├── data/
│   ├── HANDBOOK_LICENSE
│   └── handbook/                 # 47 md-файлов (готово)
├── tests/
│   ├── __init__.py
│   ├── test_handbook_search.py   # готово, 3 теста зелёные
│   ├── test_guardrails.py        # to-do
│   └── test_agent_e2e.py         # to-do — реальный прогон через ask()
├── eval/
│   └── eval_set.json             # 10-15 вопросов для `adk eval` (п.9 плана)
├── .gitignore                    # venv/, __pycache__/, .pytest_cache/, .ruff_cache/, .env
├── .env.example                  # OPENAI_API_KEY=, без реального значения
└── requirements.txt              # google-adk, litellm, pytest (заморозить версии перед сдачей)
```

**Git:** новый репозиторий `spqr-86/corporate-knowledge-assistant` (приватный на старте, можно открыть публично к сдаче — курс может требовать публичный репо, проверить в email). Push по SSH (git@github.com:spqr-86/...), как остальные личные репо Петра.

**Коммиты:** conventional commits, английский (по общему стандарту coding-standards.md). Примерная последовательность:
1. `chore: init project structure, venv, google-adk`
2. `feat: add handbook retrieval tool with tests`
3. `feat: minimal ADK agent with handbook_search tool (Gemini)`
4. `fix: switch to OpenAI via LiteLLM (Gemini quota blocked)`
5. `feat: coordinator agent with HR domain sub-agent`
6. `feat: add context-perimeter guardrail (before_model_callback)`
7. `feat: add denial-of-wallet guardrail (before_tool_callback)`
8. `feat: add compliance-guardrail agent skill (SKILL.md)`
9. `feat: add draft_pto_request and create_hr_ticket action tools`
10. `feat: wrap retrieval as MCP server`
11. `test: add eval set and adk eval integration`
12. `docs: add README with pitch and demo instructions`

Не обязательно один коммит на пункт — группировать логически, но не смешивать guardrails/tools/agent-структуру в один огромный коммит (легче ревьюить и легче отступить, если что-то сломается за 2 дня до дедлайна).

## 10. CLAUDE.md проекта (создать сейчас)

Короткий локальный контекст (источник приоритета 3 по личной иерархии Петра). Черновик:

```markdown
# Corporate Knowledge Assistant — Capstone (Google AI Agents course)

Дедлайн: 06.07.2026 23:59 PT. Трек Agents for Business.
Полная спека и статус — см. PLAN.md (обновляется по ходу, читать целиком при возврате к проекту).

## Стек
- Google ADK 2.3.0, модель — OpenAI gpt-4o-mini через LiteLLM (не Gemini — квота 0 на текущем ключе)
- Ключ: `export OPENAI_API_KEY=$(grep '^OPENAI_API_KEY=' ~/projects/ai/regulatory-rag/.env | cut -d= -f2-)`
- venv в проекте: `source venv/bin/activate`

## Данные
- GitLab Handbook (MIT license), подкорпус HR: total-rewards+hiring+people-policies, 47 файлов
- data/HANDBOOK_LICENSE — обязательно упомянуть в README/питче

## Архитектура
Coordinator Agent → HR Domain Agent (sub-agent) → tools (retrieval + actions)
Guardrails — before_model_callback/before_tool_callback, НЕ отдельные LLM-агенты.
Детали — PLAN.md раздел 3.

## Запуск
`python3 agent.py` — интерактивный CLI-луп (после экспорта ключа и активации venv)
`pytest tests/ -v` — тесты

## Курс — обязательно показать 3+ концепции
ADK multi-agent, MCP-сервер, Agent Skills (SKILL.md), security features (Context-as-a-Perimeter + DoW)
```

## 11. Открытые решения (не финализированы)

- Список стран/юрисдикций для permission-aware/routing демо — взять все 12 из данных или подмножество для наглядности?
- Формат MCP-сервера: локальный stdio-сервер для демо или что-то показательнее?
- Multi-step orchestrator (п.7 stretch) — включать в основной демо-путь или как "если успеем"?

## 12. Definition of Done (капстон сдан)

Явный проверяемый чеклист — не "работает на глаз". Капстон готов к сдаче, когда:

- [ ] Агент реально отвечает на вопросы live (не мок), через реальный ADK Runner + OpenAI API
- [ ] Показаны 3+ концепции курса явно, не только "технически используются":
  - [ ] ADK multi-agent (Coordinator + HR sub-agent) — работает end-to-end
  - [ ] MCP-сервер — retrieval обёрнут как MCP tool, не просто внутренний FunctionTool
  - [ ] Agent Skill — `skills/compliance-guardrail/SKILL.md` реально читается/используется guardrail-логикой
  - [ ] Security feature — guardrails именованы и работают как Context-as-a-Perimeter + Denial-of-Wallet защита
- [ ] `pytest tests/ -v` — все тесты зелёные
- [ ] Smoke-тест (`pytest -m smoke`) зелёный — воспроизводимый end-to-end прогон, не разовый ручной
- [ ] `adk eval` прогнан хотя бы раз на golden dataset (5-10 кейсов) — результат зафиксирован (не обязательно 100%, но известен)
- [ ] README.md с питчем (2 мин версия) + инструкция запуска для судей
- [ ] Репозиторий запушен на GitHub (публичный или приватный — уточнить требование трека в письме)
- [ ] Лицензия/источник данных явно указаны (data/HANDBOOK_LICENSE, ссылка на исходный репо)

Если что-то из списка не успеваем — явно вычеркнуть с пометкой "not in scope for capstone,
post-deadline backlog", не оставлять молча недоделанным.
