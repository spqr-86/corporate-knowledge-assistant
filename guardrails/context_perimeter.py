"""Context-as-a-Perimeter guardrail (Day4) — before_model_callback.

ANCHOR: context_perimeter
Role: before_model_callback for hr_domain_agent. Inspects the incoming
      request text (not a static RBAC list) and decides whether to let the
      LLM call proceed or short-circuit with a clarifying question, when a
      jurisdiction-sensitive HR question doesn't name a country/entity.
Input: query text (pure detector) / CallbackContext + LlmRequest (ADK hook).
Output: bool (pure detector) / Optional[LlmResponse] (ADK hook — None lets
      the LLM call proceed, a response short-circuits it).
"""

from __future__ import annotations

import re
from pathlib import Path

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

from text_utils import tokenize


# Escalation criteria live in the compliance-guardrail Agent Skill
# (skills/compliance-guardrail/ — SKILL.md + references/, Day3 progressive-
# disclosure pattern), not hardcoded here: edit a reference file to change
# behavior, no Python change needed.
_SKILL_REFERENCES = (
    Path(__file__).resolve().parent.parent
    / "skills"
    / "compliance-guardrail"
    / "references"
)


def _load_reference(filename: str) -> frozenset[str]:
    lines = (_SKILL_REFERENCES / filename).read_text(encoding="utf-8").splitlines()
    return frozenset(line.strip().lower() for line in lines if line.strip())


_JURISDICTION_SENSITIVE_TERMS = _load_reference("jurisdiction_sensitive_terms.txt")

# Single-word country names/codes must match a whole tokenized word — "us"
# is a substring of "just", so plain `in lower` containment false-positives.
# "us" itself is excluded from the reference file (see _COUNTRY_CODE_US_RE
# below) — it's also a common English pronoun ("offered to us"), so
# case-insensitive whole-word matching alone still false-positives.
_KNOWN_COUNTRIES_SINGLE_WORD = _load_reference("countries_single_word.txt")
# Multi-word names can't be single tokens, so a substring check is safe here.
_KNOWN_COUNTRIES_MULTI_WORD = _load_reference("countries_multi_word.txt")

# Only an uppercase standalone "US" counts as the country code — lowercase
# "us" is far more often the pronoun than the country in normal writing.
_COUNTRY_CODE_US_RE = re.compile(r"\bUS\b")

# A query naming explicit YYYY-MM-DD dates is a booking/action request
# (-> draft_pto_request), not a jurisdiction-dependent policy lookup, even
# if phrased with a sensitive word like "leave" or "PTO".
_EXPLICIT_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}")


def is_ambiguous_jurisdiction_query(text: str) -> bool:
    """True if the query touches jurisdiction-sensitive HR topics but names no country."""
    if _EXPLICIT_DATE_RE.search(text):
        return False
    lower = text.lower()
    words = set(tokenize(text))
    if not words & _JURISDICTION_SENSITIVE_TERMS:
        return False
    if words & _KNOWN_COUNTRIES_SINGLE_WORD:
        return False
    if _COUNTRY_CODE_US_RE.search(text):
        return False
    return not any(phrase in lower for phrase in _KNOWN_COUNTRIES_MULTI_WORD)


def _last_user_text(llm_request: LlmRequest) -> str:
    """The current user question — the last REAL 'user' content.

    Two traps: (1) transfer_to_agent injects synthesized 'user'-role
    tool-transfer notes ("For context: ... called tool ..."), which must be
    skipped; (2) with a process-level session, contents accumulate the whole
    conversation, so taking the FIRST user message would forever re-judge
    turn 1 instead of the question actually being asked now.
    """
    for content in reversed(llm_request.contents or []):
        if content.role != "user":
            continue
        text = " ".join(part.text for part in (content.parts or []) if part.text)
        if not text or text.startswith("For context:"):
            continue
        return text
    return ""


def _text_names_known_country(text: str) -> bool:
    lower = text.lower()
    words = set(tokenize(text))
    if words & _KNOWN_COUNTRIES_SINGLE_WORD:
        return True
    if _COUNTRY_CODE_US_RE.search(text):
        return True
    return any(phrase in lower for phrase in _KNOWN_COUNTRIES_MULTI_WORD)


async def _memory_knows_country(callback_context: CallbackContext) -> bool:
    """True if a past conversation in memory names the user's country.

    The query is the country names themselves, not the word "country" —
    keyword-matching memory backends (InMemoryMemoryService) match query
    words against stored text, and a user saying "I'm based in France"
    never says the word "country".
    """
    query = " ".join(sorted(_KNOWN_COUNTRIES_SINGLE_WORD | _KNOWN_COUNTRIES_MULTI_WORD))
    try:
        response = await callback_context.search_memory(query)
    except ValueError:  # no memory service wired (e.g. bare adk eval Runner)
        return False
    for memory in response.memories:
        if memory.content and memory.content.parts:
            text = " ".join(p.text for p in memory.content.parts if p.text)
            if _text_names_known_country(text):
                return True
    return False


async def context_perimeter_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    """before_model_callback: ask for the country before calling the LLM if ambiguous.

    Before short-circuiting, checks cross-session memory: if a past
    conversation already named the country, the LLM gets the turn (its
    instruction tells it to recall the country via load_memory) instead of
    the user being re-asked something they already answered.
    """
    text = _last_user_text(llm_request)
    if not is_ambiguous_jurisdiction_query(text):
        return None
    if await _memory_knows_country(callback_context):
        return None
    return LlmResponse(
        content=types.Content(
            role="model",
            parts=[
                types.Part(
                    text=(
                        "This depends on your country/entity — GitLab's HR "
                        "policies vary by location. Could you tell me which "
                        "country or entity you're in?"
                    )
                )
            ],
        )
    )
