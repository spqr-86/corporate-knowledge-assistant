from tools.draft_pto_request import draft_pto_request


def test_draft_pto_request_returns_draft_for_valid_dates():
    result = draft_pto_request(
        start_date="2026-08-10", end_date="2026-08-14", reason="Family trip"
    )
    assert result["status"] == "success"
    assert "2026-08-10" in result["draft"]
    assert "2026-08-14" in result["draft"]
    assert "Family trip" in result["draft"]
    assert result["approved"] is False


def test_draft_pto_request_rejects_end_before_start():
    result = draft_pto_request(
        start_date="2026-08-14", end_date="2026-08-10", reason="Oops"
    )
    assert result["status"] == "error"
    assert "end_date" in result["error_message"].lower()


def test_draft_pto_request_rejects_invalid_date_format():
    result = draft_pto_request(
        start_date="10/08/2026", end_date="2026-08-14", reason="Trip"
    )
    assert result["status"] == "error"
