"""Central runtime configuration for the Corporate Knowledge Assistant.

ANCHOR: config
Role: single source of defaults previously scattered across modules
      (model id, handbook data/index paths, retrieval threshold, mock RBAC
      prefixes, ticket log path, pricing table, dev user id). Modules read
      the module-level `settings` singleton at import; scalar values can be
      overridden via environment variables (documented in .env.example).
Input: os.environ at import time (or an explicit load() call).
Output: frozen Settings dataclass — treat as read-only; tests that need to
      vary values monkeypatch the consuming module's own name, not this.
Note: dict-valued defaults (RBAC prefixes, pricing) intentionally have no
      env override — they are code-level policy, not deployment knobs.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent

# mock RBAC: relative-path prefixes gated to a minimum role
DEFAULT_RESTRICTED_PREFIXES: dict[str, str] = {
    "total-rewards/compensation": "manager",
}

# Retrieval tools whose `role` argument must be bound from trusted session
# state, never trusted from the LLM. The role-binding guardrail also applies
# fail-closed to any *other* tool that carries a `role` arg (see
# guardrails/role_binding.py), so renaming or adding a retrieval tool cannot
# silently reopen the RBAC bypass — this set is the explicit, known list.
RBAC_GATED_TOOLS: frozenset[str] = frozenset({"search_handbook"})

# gpt-4o-mini list price (per 1M tokens) as of the model's release —
# approximation for the pitch, not a billing-accurate figure
DEFAULT_GPT_4O_MINI_PRICING: dict[str, float] = {
    "prompt_per_million": 0.15,
    "candidates_per_million": 0.60,
}


@dataclass(frozen=True)
class Settings:
    """Immutable snapshot of runtime configuration."""

    model_id: str = "openai/gpt-4o-mini"
    data_dir: Path = _PROJECT_ROOT / "data" / "handbook"
    index_path: Path = _PROJECT_ROOT / "data" / ".handbook_index.npz"
    score_threshold: float = 0.30
    restricted_prefixes: dict[str, str] = field(
        default_factory=lambda: dict(DEFAULT_RESTRICTED_PREFIXES)
    )
    rbac_gated_tools: frozenset[str] = RBAC_GATED_TOOLS
    ticket_log_path: Path = _PROJECT_ROOT / "data" / "hr_tickets.jsonl"
    pricing: dict[str, float] = field(
        default_factory=lambda: dict(DEFAULT_GPT_4O_MINI_PRICING)
    )
    user_id: str = "demo-user"


def load() -> Settings:
    """Build Settings from environment overrides falling back to defaults."""
    defaults = Settings()
    return Settings(
        model_id=os.environ.get("CKA_MODEL_ID", defaults.model_id),
        data_dir=Path(os.environ.get("CKA_DATA_DIR", str(defaults.data_dir))),
        index_path=Path(os.environ.get("CKA_INDEX_PATH", str(defaults.index_path))),
        score_threshold=float(
            os.environ.get("CKA_SCORE_THRESHOLD", str(defaults.score_threshold))
        ),
        ticket_log_path=Path(
            os.environ.get("CKA_TICKET_LOG_PATH", str(defaults.ticket_log_path))
        ),
        user_id=os.environ.get("CKA_USER_ID", defaults.user_id),
    )


settings: Settings = load()
