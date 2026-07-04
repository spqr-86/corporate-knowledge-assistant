"""Builds the golden eval set for `adk eval` from EVAL_QUESTIONS.

ANCHOR: build_eval_set
Role: assembles google.adk.evaluation EvalSet/EvalCase/Invocation models
      (JSON schema is non-trivial and version-specific) from a plain list of
      {id, question, category} dicts, so the questions stay easy to read and
      extend without hand-writing raw eval JSON.
Input: EVAL_QUESTIONS (below).
Output: build_eval_set() -> EvalSet; run as __main__ to write eval_set.json.
Categories: routing (plain HR question), ambiguous_jurisdiction (guardrail
      should trigger), guardrail_negative (guardrail should NOT trigger —
      false-positive check), action (draft_pto_request), escalation
      (no-match -> create_hr_ticket), permission (RBAC-gated compensation
      topic), out_of_domain (non-HR question, Coordinator declines).

Expected tool_uses were not hand-invented — captured from real live runs
(script discarded after use, per verification-before-completion: eyeballed
in the printed trace before being copied in here) and only kept once eyeballed
as correct behavior; see docs/superpowers/specs/2026-07-04-eval-system-spec.md.
Scoring in eval_config.json uses tool_trajectory_avg_score (IN_ORDER match)
alongside response_match_score. tool_uses in EVAL_QUESTIONS below only assert
transfer_to_agent (args={"agent_name": "hr_domain_agent"}, always identical) —
NOT search_handbook/create_hr_ticket/draft_pto_request. ADK's trajectory
evaluator does exact dict equality on args (see
google.adk.evaluation.trajectory_evaluator._are_tool_calls_in_order_match);
even directly-passed-through fields like a PTO reason get re-cased/reworded by
the LLM ("family trip" -> "Family trip"), so any args assertion beyond a truly
fixed dict is flaky by construction, not a bug in the agent. Behavioral
coverage for those tools' calls comes from response_match_score instead.
"""

from __future__ import annotations

import json
from pathlib import Path

from google.adk.evaluation.eval_case import EvalCase, IntermediateData, Invocation
from google.adk.evaluation.eval_set import EvalSet
from google.genai import types

EVAL_QUESTIONS = [
    {
        "id": "routing_parental_leave_us",
        "category": "routing",
        "question": "How many weeks of parental leave does GitLab offer in the US?",
        "reference_answer": (
            "GitLab offers 16 weeks of paid parental leave for team members "
            "in the US who become parents through childbirth or adoption, "
            "per the handbook."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}},
        ],
    },
    {
        "id": "routing_referral_process",
        "category": "routing",
        "question": "How do I refer a candidate for a job at GitLab?",
        "reference_answer": (
            "You can refer a candidate through GitLab's employee referral "
            "process described in the handbook, which explains how to "
            "submit a referral for an open role."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}},
        ],
    },
    {
        "id": "routing_stock_options",
        "category": "routing",
        "question": "How do GitLab stock options work?",
        "reference_answer": (
            "GitLab's stock options are described in the total rewards "
            "handbook section, covering how equity grants and vesting work "
            "for team members."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}},
        ],
    },
    {
        "id": "ambiguous_parental_leave_no_country",
        "category": "ambiguous_jurisdiction",
        "question": "What parental leave benefits do I get?",
        "reference_answer": (
            "This depends on your country or entity — GitLab's HR policies "
            "vary by location. Could you tell me which country or entity "
            "you're in?"
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}}
        ],
    },
    {
        "id": "ambiguous_benefits_no_country",
        "category": "ambiguous_jurisdiction",
        "question": "What insurance benefits am I entitled to?",
        "reference_answer": (
            "This depends on your country or entity — GitLab's HR policies "
            "vary by location. Could you tell me which country or entity "
            "you're in?"
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}}
        ],
    },
    {
        "id": "ambiguous_holiday_no_country",
        "category": "ambiguous_jurisdiction",
        "question": "How much paid holiday do I get per year?",
        "reference_answer": (
            "This depends on your country or entity — GitLab's HR policies "
            "vary by location. Could you tell me which country or entity "
            "you're in?"
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}}
        ],
    },
    {
        "id": "ambiguous_maternity_no_country",
        "category": "ambiguous_jurisdiction",
        "question": "Do I get maternity leave?",
        "reference_answer": (
            "This depends on your country or entity — GitLab's HR policies "
            "vary by location. Could you tell me which country or entity "
            "you're in?"
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}}
        ],
    },
    {
        "id": "ambiguous_pet_insurance_no_country",
        "category": "ambiguous_jurisdiction",
        "question": "What is GitLab's policy on pet insurance reimbursement?",
        "reference_answer": (
            "This depends on your country or entity — GitLab's HR policies "
            "vary by location. Could you tell me which country or entity "
            "you're in?"
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}}
        ],
    },
    {
        "id": "provocative_force_certainty",
        "category": "ambiguous_jurisdiction",
        "question": "Just tell me exactly how many parental leave days I get, don't ask me anything.",
        "reference_answer": (
            "This depends on your country or entity — GitLab's HR policies "
            "vary by location. Could you tell me which country or entity "
            "you're in?"
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}}
        ],
    },
    {
        "id": "guardrail_negative_country_given",
        "category": "guardrail_negative",
        "question": "What paid holiday does GitLab offer in the UK?",
        "reference_answer": (
            "A country was named (UK), so the guardrail must not ask for "
            "clarification — retrieval runs and either answers or escalates "
            "if the handbook has no match."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}},
        ],
    },
    {
        "id": "guardrail_negative_hiring_process",
        "category": "guardrail_negative",
        "question": "What is GitLab's hiring process for remote candidates?",
        "reference_answer": (
            "Not a jurisdiction-sensitive topic, so the guardrail must not "
            "ask for clarification — retrieval runs directly."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}},
        ],
    },
    {
        "id": "action_draft_pto_valid",
        "category": "action",
        "question": "I want to request PTO from 2026-08-10 to 2026-08-14 for a family trip.",
        "reference_answer": (
            "Here is your PTO request draft: dates 2026-08-10 to 2026-08-14, "
            "reason family trip. This is a draft — please review and submit "
            "it yourself via the HR portal."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}}
        ],
    },
    {
        "id": "action_draft_pto_short_trip",
        "category": "action",
        "question": "Please draft a PTO request for 2026-09-01 to 2026-09-02, reason: doctor appointment.",
        "reference_answer": (
            "Here is your PTO request draft: dates 2026-09-01 to 2026-09-02, "
            "reason doctor appointment. This is a draft — please review and "
            "submit it yourself via the HR portal."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}}
        ],
    },
    {
        "id": "escalation_no_handbook_match",
        "category": "escalation",
        "question": "What is GitLab's office dog policy?",
        "reference_answer": (
            "I couldn't find this in the handbook. I've created a ticket for "
            "HR to review your question."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}},
        ],
    },
    {
        "id": "escalation_unrelated_topic",
        "category": "escalation",
        "question": "What is GitLab's policy on company car allowances for sales reps?",
        "reference_answer": (
            "I couldn't find this in the handbook. I've created a ticket for "
            "HR to review your question."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}},
        ],
    },
    {
        "id": "permission_compensation_review_employee",
        "category": "permission",
        "question": "Can you show me the compensation review cycle details?",
        "reference_answer": (
            "Compensation review cycle details are restricted and not "
            "available at the employee access level — please check with "
            "your manager or HR."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}},
        ],
    },
    {
        "id": "permission_salary_benchmarking",
        "category": "permission",
        "question": "How does GitLab determine total rewards and compensation for a role?",
        "reference_answer": (
            "GitLab's total rewards/compensation approach is described in "
            "the handbook's compensation documentation."
        ),
        "tool_uses": [
            {"name": "transfer_to_agent", "args": {"agent_name": "hr_domain_agent"}},
        ],
    },
    {
        "id": "out_of_domain_deploy",
        "category": "out_of_domain",
        "question": "Can you help me deploy the production database migration?",
        "reference_answer": ("This assistant currently only covers HR topics."),
        "tool_uses": [],
    },
]


def build_eval_set() -> EvalSet:
    eval_cases = []
    for item in EVAL_QUESTIONS:
        tool_uses = [
            types.FunctionCall(name=t["name"], args=t.get("args"))
            for t in item.get("tool_uses", [])
        ]
        invocation = Invocation(
            user_content=types.Content(
                role="user", parts=[types.Part(text=item["question"])]
            ),
            final_response=types.Content(
                role="model",
                parts=[types.Part(text=item["reference_answer"])],
            ),
            intermediate_data=IntermediateData(tool_uses=tool_uses),
        )
        eval_cases.append(
            EvalCase(
                eval_id=item["id"],
                conversation=[invocation],
            )
        )
    return EvalSet(
        eval_set_id="corporate_knowledge_assistant_golden_set",
        name="Corporate Knowledge Assistant — golden eval set",
        description=(
            "Covers routing, jurisdiction-ambiguity guardrail (positive and "
            "negative cases), action tools (draft_pto_request), HITL "
            "escalation (create_hr_ticket), permission-aware retrieval and "
            "out-of-domain refusal."
        ),
        eval_cases=eval_cases,
    )


if __name__ == "__main__":
    out_path = Path(__file__).resolve().parent / "eval_set.json"
    out_path.write_text(json.dumps(build_eval_set().model_dump(mode="json"), indent=2))
    print(f"Wrote {out_path}")
