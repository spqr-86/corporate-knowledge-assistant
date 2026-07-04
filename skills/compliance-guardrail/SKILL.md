---
name: compliance-guardrail
description: >
  Escalation and clarification criteria for jurisdiction-sensitive HR
  questions. Used by the Context-as-a-Perimeter guardrail
  (guardrails/context_perimeter.py) to decide whether a question can be
  answered directly, needs a clarifying question about the user's
  country/entity, or must be escalated to a human. Load references/ only
  when evaluating a concrete query — progressive disclosure, keep this
  file small.
---

# Compliance Guardrail — when to clarify or escalate

## Decision rules

1. **Explicit dates → action, not lookup.** A query containing an explicit
   `YYYY-MM-DD` date is a booking/action request (PTO draft), never a
   jurisdiction-dependent policy lookup. Let it through.
2. **Jurisdiction-sensitive topic + no country → clarify.** If the query
   touches any term in `references/jurisdiction_sensitive_terms.txt` and
   names no country/entity, ask which country the user is in — GitLab HR
   policies differ per entity, and answering for the wrong jurisdiction is
   worse than asking.
3. **Country detection is word-boundary based.** Single-word country names
   (`references/countries_single_word.txt`) must match a whole word —
   substring matching false-positives ("us" inside "just"). The bare code
   "US" only counts when uppercase (lowercase "us" is a pronoun).
   Multi-word names (`references/countries_multi_word.txt`) match as
   phrases.
4. **Check memory before re-asking.** If a past conversation already named
   the user's country (cross-session memory), do not re-ask — recall it.
5. **No answer in the handbook → escalate, don't dead-end.** When retrieval
   finds nothing relevant, create an HR ticket (a real artifact) instead of
   replying "I don't know".

## References (progressive disclosure — load on demand)

- `references/jurisdiction_sensitive_terms.txt` — one term per line;
  topics whose answer depends on the employee's country/entity.
- `references/countries_single_word.txt` — one name/code per line;
  single-token country names matched at word boundaries.
- `references/countries_multi_word.txt` — one name per line; multi-word
  country names matched as phrases.

Editing a reference file changes guardrail behavior directly — the
deterministic detector in `guardrails/context_perimeter.py` loads these
files at import time; no Python change needed to add a term or a country.
