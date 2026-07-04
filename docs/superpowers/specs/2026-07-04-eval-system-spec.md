# Spec: Eval-система капстона (v2)

**Дата:** 2026-07-04
**Статус:** draft — на одобрение
**Контекст:** сейчас 12 кейсов, единственная метрика `response_match_score` (ROUGE, threshold 0.3),
результат 9/12, все 3 фейла — ложные (ROUGE-артефакт на функционально верных ответах).
Меряем похожесть текста, а надо — категорию решения (лекция 4 ШАД, PLAN.md §3.5).

## Цель

Eval, который (а) не даёт ложных фейлов на верном поведении, (б) даёт судьям капстона
читаемые цифры по каждой фиче (guardrail, RBAC, HITL, actions), (в) воспроизводим одной командой.

## Не-цели

- LLM-as-judge, RAGAS, калибровка Cohen's κ — не окупятся до дедлайна 06.07.
- Расширение датасета свыше ~20 кейсов.
- CI-интеграция eval (юнит-тесты в CI уже есть; eval — ручной прогон перед сдачей).

## Дизайн

### 1. Скоринг: trajectory + response (два критерия вместо одного)

`eval_config.json`:

```json
{
  "criteria": {
    "tool_trajectory_avg_score": 0.8,
    "response_match_score": 0.2
  }
}
```

- **`tool_trajectory_avg_score`** — главный критерий. В каждый EvalCase добавляем ожидаемые
  `intermediate_data.tool_uses` (имя tool + ключевые аргументы). Проверяет поведение:
  - routing-кейсы → `transfer_to_agent(hr_domain_agent)` + `search_handbook`
  - action → `draft_pto_request` с датами
  - escalation → `create_hr_ticket`
  - ambiguous_jurisdiction → **отсутствие** retrieval-вызова (guardrail short-circuit до LLM)
  - permission → `search_handbook` (RBAC-фильтр проверяется юнит-тестами, тут — что flow не упал)
- **`response_match_score`** понижаем до 0.2 — остаётся как sanity-check на пустой/бредовый ответ,
  перестаёт быть источником ложных фейлов.
- Риск: точный формат ожидаемой trajectory в ADK 2.3.0 надо сверить с исходниками
  `google.adk.evaluation` (partial match аргументов может не поддерживаться — тогда указываем
  только имена tools без аргументов).

### 2. Датасет: 12 → ~18 кейсов

Добавить (все — через `EVAL_QUESTIONS` в `build_eval_set.py`, категория указана):

| # | Категория | Что проверяет |
|---|---|---|
| +1..2 | `guardrail_negative` (новая) | Обычные вопросы с явной страной / без sensitive-темы — guardrail НЕ должен сработать (false positive rate) |
| +3..4 | `ambiguous_jurisdiction` | Ещё 2 неоднозначных формулировки (false negative rate; сейчас кейса всего 2-3 — мало для rate) |
| +5 | `escalation` | Вопрос вне корпуса, но HR-тематики ("relocation to Mars policy") |
| +6 | `out_of_domain` (новая) | Не-HR вопрос ("deploy к prod") — Coordinator должен ответить "only HR", без transfer |

### 3. Отчёт: по категориям, не общим счётом

Новый `eval/report.py`: читает JSON-результаты `adk eval` (директория результатов),
агрегирует по категориям (категория берётся из префикса `eval_id`), печатает markdown-таблицу:

```
| Category | Pass | Metric meaning |
| routing | 3/3 | правильный transfer + retrieval + ответ |
| ambiguous_jurisdiction | 4/4 | guardrail поймал (false negative rate 0%) |
| guardrail_negative | 2/2 | guardrail не мешает (false positive rate 0%) |
| action | 1/1 | draft_pto_request вызван с датами |
| escalation | 3/3 | create_hr_ticket создан |
| permission | 2/2 | RBAC flow цел |
| out_of_domain | 1/1 | отказ без transfer |
```

Таблица идёт в README (заменяет "9/12") и в WRITEUP.

### 4. Стабильность (если останется время — вычёркиваемо)

`eval/run_stability.sh`: 3 прогона `adk eval` подряд, `report.py --stability` считает
per-case consistency (сколько кейсов дали одинаковый вердикт во всех 3 прогонах).
Одна строка в README: "consistency: N/18 cases stable across 3 runs". Стоимость: ~54 LLM-вызова
× $0.0004 — копейки, единственная цена — время прогона (~5 мин).

## Порядок работ (TDD где применимо)

1. Сверить формат trajectory-скоринга с исходниками ADK 2.3.0 → обновить `build_eval_set.py`
   (tool_uses в Invocation) + `eval_config.json`. Прогон → ожидание: 12/12 или объяснимые фейлы.
2. Добавить 6 кейсов (п.2) → прогон → зафиксировать результат.
3. `eval/report.py` + таблица в README/WRITEUP.
4. (опция) стабильность ×3.

## Definition of Done

- [ ] `adk eval` проходит с двумя критериями, ложных ROUGE-фейлов нет
- [ ] ~18 кейсов, каждая фича проекта покрыта своей категорией
- [ ] `eval/report.py` печатает категорийную таблицу, она вставлена в README + WRITEUP
- [ ] Все юнит-тесты по-прежнему зелёные (48+)
- [ ] Результаты честно зафиксированы, включая фейлы, с разбором причин
