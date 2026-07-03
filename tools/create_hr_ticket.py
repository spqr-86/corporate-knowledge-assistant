"""Action tool: mock HITL escalation — create an HR ticket.

ANCHOR: create_hr_ticket
Role: HITL-as-action tool for hr_domain_agent. When a question can't be
      answered confidently (ambiguous jurisdiction, missing from handbook
      subset), this creates a real artifact (a logged ticket) instead of
      just replying "I don't know" — mock escalation to a human.
Input: question, reason (why escalating).
Output: dict with status, ticket_id. Appends a JSON line to TICKET_LOG_PATH.
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path

TICKET_LOG_PATH = Path(__file__).resolve().parent.parent / "data" / "hr_tickets.jsonl"


def create_hr_ticket(question: str, reason: str) -> dict:
    """Escalate a question to HR by logging a mock ticket.

    Args:
        question: the user's original question.
        reason: why this needs human review (e.g. ambiguous jurisdiction).

    Returns:
        dict with 'status' ('success' or 'error') and, on success,
        'ticket_id' identifying the logged ticket.
    """
    if not question.strip():
        return {"status": "error", "error_message": "question must not be empty."}

    ticket_id = str(uuid.uuid4())
    entry = {"ticket_id": ticket_id, "question": question, "reason": reason}

    TICKET_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TICKET_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    return {"status": "success", "ticket_id": ticket_id}
