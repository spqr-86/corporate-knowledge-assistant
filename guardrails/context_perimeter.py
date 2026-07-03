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

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

_JURISDICTION_SENSITIVE_TERMS = {
    "leave",
    "benefit",
    "benefits",
    "parental",
    "insurance",
    "holiday",
    "vacation",
}

# Single-word country names/codes must match a whole tokenized word — "us"
# is a substring of "just", so plain `in lower` containment false-positives.
_KNOWN_COUNTRIES_SINGLE_WORD = {
    "france",
    "uk",
    "canada",
    "singapore",
    "korea",
    "australia",
    "ireland",
    "belgium",
    "netherlands",
    "finland",
    "us",
    "usa",
    "india",
}
# Multi-word names can't be single tokens, so a substring check is safe here.
_KNOWN_COUNTRIES_MULTI_WORD = {"united kingdom", "new zealand", "united states"}

_WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z\-']+")


def is_ambiguous_jurisdiction_query(text: str) -> bool:
    """True if the query touches jurisdiction-sensitive HR topics but names no country."""
    lower = text.lower()
    words = set(_WORD_RE.findall(lower))
    if not words & _JURISDICTION_SENSITIVE_TERMS:
        return False
    if words & _KNOWN_COUNTRIES_SINGLE_WORD:
        return False
    return not any(phrase in lower for phrase in _KNOWN_COUNTRIES_MULTI_WORD)


def _first_user_text(llm_request: LlmRequest) -> str:
    """The original user question — the first 'user' content in the request.

    After transfer_to_agent, later 'user'-role contents are synthesized
    tool-transfer notes ("For context: ... called tool ..."), not the
    original question, so we can't just take the last user-role content.
    """
    for content in llm_request.contents or []:
        if content.role != "user":
            continue
        return " ".join(part.text for part in (content.parts or []) if part.text)
    return ""


def context_perimeter_guardrail(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    """before_model_callback: ask for the country before calling the LLM if ambiguous."""
    text = _first_user_text(llm_request)
    if not is_ambiguous_jurisdiction_query(text):
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
