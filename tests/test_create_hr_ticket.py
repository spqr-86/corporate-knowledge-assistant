import json

from tools.create_hr_ticket import TICKET_LOG_PATH, create_hr_ticket


def test_create_hr_ticket_appends_ticket_to_log(tmp_path, monkeypatch):
    log_path = tmp_path / "hr_tickets.jsonl"
    monkeypatch.setattr("tools.create_hr_ticket.TICKET_LOG_PATH", log_path)

    result = create_hr_ticket(
        question="What's my parental leave in a jurisdiction not in the handbook?",
        reason="Ambiguous jurisdiction, not covered by the handbook subset",
    )

    assert result["status"] == "success"
    assert "ticket_id" in result
    lines = log_path.read_text().strip().splitlines()
    assert len(lines) == 1
    entry = json.loads(lines[0])
    assert entry["question"].startswith("What's my parental leave")
    assert (
        entry["reason"] == "Ambiguous jurisdiction, not covered by the handbook subset"
    )
    assert entry["ticket_id"] == result["ticket_id"]


def test_create_hr_ticket_rejects_empty_question(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "tools.create_hr_ticket.TICKET_LOG_PATH", tmp_path / "hr_tickets.jsonl"
    )
    result = create_hr_ticket(question="", reason="n/a")
    assert result["status"] == "error"


def test_ticket_log_path_default_exists_under_project():
    assert TICKET_LOG_PATH.name == "hr_tickets.jsonl"
