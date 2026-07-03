from eval.build_eval_set import EVAL_QUESTIONS, build_eval_set


def test_eval_set_has_at_least_ten_cases():
    assert len(EVAL_QUESTIONS) >= 10


def test_eval_set_covers_required_categories():
    categories = {q["category"] for q in EVAL_QUESTIONS}
    assert {"routing", "ambiguous_jurisdiction", "action", "escalation"} <= categories


def test_build_eval_set_produces_valid_eval_set():
    eval_set = build_eval_set()
    assert len(eval_set.eval_cases) == len(EVAL_QUESTIONS)
    # round-trips through the pydantic model without validation errors
    dumped = eval_set.model_dump(mode="json")
    assert dumped["eval_set_id"] == eval_set.eval_set_id
