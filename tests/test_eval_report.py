"""Tests for eval/report.py's category aggregation.

ANCHOR: test_eval_report
Role: TDD for build_report() — verifies category grouping, pass counts and
      the trajectory-mismatch note, using a synthetic result file so this
      test doesn't depend on `adk eval` having been run.
"""

import json

from eval.report import build_report

_PASSED = 1
_FAILED = 2


def _write_fake_result(tmp_path, cases):
    path = tmp_path / "fake.evalset_result.json"
    path.write_text(json.dumps({"eval_case_results": cases}))
    return path


def _case(eval_id, status, trajectory_score=1.0):
    return {
        "eval_id": eval_id,
        "final_eval_status": status,
        "overall_eval_metric_results": [
            {"metric_name": "tool_trajectory_avg_score", "score": trajectory_score},
            {"metric_name": "response_match_score", "score": 0.5},
        ],
    }


def test_groups_by_category_from_eval_questions(tmp_path):
    cases = [
        _case("routing_parental_leave_us", _PASSED),
        _case("routing_stock_options", _FAILED),
    ]
    report = build_report(_write_fake_result(tmp_path, cases))
    assert "| routing | 1/2 |" in report


def test_total_row_sums_all_categories(tmp_path):
    cases = [
        _case("routing_parental_leave_us", _PASSED),
        _case("action_draft_pto_valid", _PASSED),
    ]
    report = build_report(_write_fake_result(tmp_path, cases))
    assert "**2/2**" in report


def test_flags_trajectory_mismatch(tmp_path):
    cases = [_case("routing_parental_leave_us", _FAILED, trajectory_score=0.0)]
    report = build_report(_write_fake_result(tmp_path, cases))
    assert "trajectory mismatch" in report
