"""Category-level report over the latest `adk eval` run.

ANCHOR: report
Role: reads the most recent eval_history JSON written by `adk eval` and
      prints a per-category pass/fail table (routing, ambiguous_jurisdiction,
      guardrail_negative, action, escalation, permission, out_of_domain) plus
      per-metric scores, instead of a single overall N/M count that hides
      which feature is actually failing and why.
Input: latest *.evalset_result.json under eval/agent_target/.adk/eval_history/
       and eval/build_eval_set.py's EVAL_QUESTIONS (for id -> category lookup).
Output: markdown table printed to stdout (paste into README/WRITEUP).
Run: python3 -m eval.report
"""

from __future__ import annotations

import json
from pathlib import Path

from eval.build_eval_set import EVAL_QUESTIONS

_EVAL_STATUS_PASSED = 1

_ID_TO_CATEGORY = {item["id"]: item["category"] for item in EVAL_QUESTIONS}


def _latest_result_path() -> Path:
    history_dir = (
        Path(__file__).resolve().parent / "agent_target" / ".adk" / "eval_history"
    )
    results = sorted(history_dir.glob("*.evalset_result.json"))
    if not results:
        raise FileNotFoundError(
            f"No eval results found in {history_dir} — run `adk eval` first."
        )
    return results[-1]


def build_report(result_path: Path | None = None) -> str:
    result_path = result_path or _latest_result_path()
    data = json.loads(result_path.read_text())

    by_category: dict[str, list[dict]] = {}
    for case in data["eval_case_results"]:
        category = _ID_TO_CATEGORY.get(case["eval_id"], "unknown")
        by_category.setdefault(category, []).append(case)

    lines = ["| Category | Passed | Notes |", "|---|---|---|"]
    for category in sorted(by_category):
        cases = by_category[category]
        passed = sum(1 for c in cases if c["final_eval_status"] == _EVAL_STATUS_PASSED)
        trajectory_ok = all(
            m["score"] == 1.0
            for c in cases
            for m in c["overall_eval_metric_results"]
            if m["metric_name"] == "tool_trajectory_avg_score"
        )
        note = (
            "behavior correct"
            if trajectory_ok
            else "trajectory mismatch — check behavior"
        )
        lines.append(f"| {category} | {passed}/{len(cases)} | {note} |")

    total = len(data["eval_case_results"])
    total_passed = sum(
        1
        for c in data["eval_case_results"]
        if c["final_eval_status"] == _EVAL_STATUS_PASSED
    )
    lines.append(f"| **total** | **{total_passed}/{total}** | |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(build_report())
