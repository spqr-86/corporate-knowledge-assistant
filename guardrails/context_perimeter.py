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


# Aliases that name the same jurisdiction, canonicalized so "uk" and "united
# kingdom" (or "usa"/"united states"/"US") count as ONE country, not several.
_COUNTRY_CANON = {
    "uk": "the united kingdom",
    "united kingdom": "the united kingdom",
    "usa": "the united states",
    "united states": "the united states",
}


def _countries_in_text(text: str) -> set[str]:
    """The set of DISTINCT jurisdictions named in text (canonicalized)."""
    lower = text.lower()
    found: set[str] = set()
    for phrase in _KNOWN_COUNTRIES_MULTI_WORD:
        if phrase in lower:
            found.add(_COUNTRY_CANON.get(phrase, phrase))
    for country in set(tokenize(text)) & _KNOWN_COUNTRIES_SINGLE_WORD:
        found.add(_COUNTRY_CANON.get(country, country))
    if _COUNTRY_CODE_US_RE.search(text):
        found.add("the united states")
    return found


def _extract_country(text: str) -> str | None:
    """The single jurisdiction named in text, or None.

    Returns None when the text names ZERO or MORE THAN ONE country: a
    comparison like "France vs Canada" establishes no single jurisdiction, so
    picking one (nondeterministically, from set order) would guess exactly
    what this guardrail exists to prevent. Deterministic by construction.
    """
    countries = _countries_in_text(text)
    if len(countries) == 1:
        return next(iter(countries))
    return None


async def _country_from_memory(callback_context: CallbackContext) -> str | None:
    """The country a past conversation named, or None.

    The query is the country names themselves, not the word "country" —
    keyword-matching memory backends (InMemoryMemoryService) match query
    words against stored text, and a user saying "I'm based in France"
    never says the word "country".
    """
    query = " ".join(sorted(_KNOWN_COUNTRIES_SINGLE_WORD | _KNOWN_COUNTRIES_MULTI_WORD))
    try:
        response = await callback_context.search_memory(query)
    except Exception:
        # No memory service wired (ValueError on a bare adk eval Runner) or a
        # durable backend failing (network/timeout) — a jurisdiction hint is
        # optional, so degrade to asking the user rather than crashing the
        # whole before_model_callback (which would 500 every ambiguous turn).
        return None
    for memory in response.memories:
        content = memory.content
        # Only the USER establishes their own jurisdiction. Archived memory
        # includes the agent's own past answers (role='model'), which may name
        # a country as an example or comparison — trusting those would let the
        # assistant silently answer for a country the user never stated. Read
        # the user's own messages only.
        if not content or content.role != "user" or not content.parts:
            continue
        text = " ".join(p.text for p in content.parts if p.text)
        # Skip our own injected "For context:" recall notes — a user-role
        # message we synthesized, not something the user actually said.
        if text.startswith("For context:"):
            continue
        country = _extract_country(text)
        if country:
            return country
    return None


async def context_perimeter_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    """before_model_callback: ask for the country before calling the LLM if ambiguous.

    Before short-circuiting, checks cross-session memory: if a past
    conversation already named the country, we inject it into the request
    context so the model answers for that country deterministically —
    rather than relying on the model to volunteer a load_memory call
    (gpt-4o-mini does so unreliably) or re-asking something already answered.
    """
    text = _last_user_text(llm_request)
    if not is_ambiguous_jurisdiction_query(text):
        return None
    remembered = await _country_from_memory(callback_context)
    if remembered:
        # "For context:" prefix so _last_user_text skips this on later turns
        llm_request.contents = list(llm_request.contents or []) + [
            types.Content(
                role="user",
                parts=[
                    types.Part(
                        text=(
                            f"For context: a past conversation established the "
                            f"user is based in {remembered}. Answer for "
                            f"{remembered} without asking again."
                        )
                    )
                ],
            )
        ]
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
