"""Action tool: draft a PTO request (approve-gate, does not submit anything).

ANCHOR: draft_pto_request
Role: HITL action tool for hr_domain_agent. Generates a PTO request draft
      text for the user to review — never submits it automatically.
Input: start_date, end_date (YYYY-MM-DD strings), reason.
Output: dict with status, draft text, approved=False (approval is a
      separate, out-of-scope step for the capstone).
"""

from __future__ import annotations

from datetime import date


def _parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def draft_pto_request(start_date: str, end_date: str, reason: str) -> dict:
    """Draft a PTO request for the user to review and manually submit.

    Args:
        start_date: PTO start date, YYYY-MM-DD.
        end_date: PTO end date, YYYY-MM-DD.
        reason: short reason for the request.

    Returns:
        dict with 'status' ('success' or 'error'). On success also includes
        'draft' (the request text) and 'approved' (always False — this tool
        only drafts, it never submits).
    """
    start = _parse_date(start_date)
    end = _parse_date(end_date)
    if start is None or end is None:
        return {
            "status": "error",
            "error_message": "start_date and end_date must be YYYY-MM-DD.",
        }
    if end < start:
        return {
            "status": "error",
            "error_message": "end_date must not be before start_date.",
        }

    draft = (
        f"PTO Request Draft\n"
        f"Dates: {start_date} to {end_date}\n"
        f"Reason: {reason}\n"
        "This is a draft — review and submit it yourself via the HR portal."
    )
    return {"status": "success", "draft": draft, "approved": False}
