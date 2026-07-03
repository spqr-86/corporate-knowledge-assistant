"""Shared word tokenizer — used by retrieval and guardrail keyword matching.

ANCHOR: text_utils
Role: single source of truth for "what counts as a word" so
      tools/handbook_search.py and guardrails/context_perimeter.py can't
      silently drift out of sync on tokenization rules.
"""

from __future__ import annotations

import re

WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z\-']+")


def tokenize(text: str) -> list[str]:
    return [w.lower() for w in WORD_RE.findall(text)]
