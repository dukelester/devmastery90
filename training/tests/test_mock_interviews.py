"""Tests for bi-weekly mock interview system and coding runner."""
import pytest

from training.code_runner import run_coding_tests, score_from_full_suite
from training.mock_interview_data import build_mock_questions_for_round, build_mock_rounds
from training.models import MockInterviewQuestion, MockInterviewRound


@pytest.mark.django_db
def test_mock_round_seed_structure():
    rounds = build_mock_rounds()
    assert len(rounds) == 7
    assert rounds[0]["unlock_day"] == 1
    assert rounds[1]["unlock_day"] == 15


@pytest.mark.django_db
def test_seed_mock_interviews_command():
    from django.core.management import call_command

    call_command("seed_mock_interviews", force=True)
    assert MockInterviewRound.objects.count() == 7
    assert MockInterviewQuestion.objects.count() == 49

    round_one = MockInterviewRound.objects.get(round_number=1)
    questions = list(round_one.questions.order_by("order"))
    assert len(questions) == 7
    assert questions[0].difficulty == "easy"
    assert questions[-1].difficulty == "expert"

    coding = [q for q in questions if q.interview_type == "coding"]
    assert len(coding) == 2
    for q in coding:
        assert q.is_runnable
        assert q.function_name
        assert q.starter_code
        assert len(q.public_test_cases) >= 1


def test_coding_questions_have_harnesses():
    for round_meta in build_mock_rounds():
        for q in build_mock_questions_for_round(round_meta):
            if q["interview_type"] == "coding":
                assert q["function_name"], q["question"]
                assert q["starter_code"], q["question"]
                assert q["test_cases"], q["question"]


def test_runner_sum_positive():
    code = "def sum_positive(nums):\n    return sum(x for x in nums if x > 0)\n"
    cases = [
        {"name": "mixed", "args": [[1, -2, 3]], "expected": 4},
        {"name": "empty", "args": [[]], "expected": 0},
        {"name": "hidden", "args": [[-1]], "expected": 0, "hidden": True},
    ]
    public = run_coding_tests(code, "sum_positive", cases, include_hidden=False)
    assert public["passed"] == 2
    assert public["total"] == 2

    full = score_from_full_suite(code, "sum_positive", cases)
    assert full["passed"] == 3
    assert full["score"] == 10.0


def test_runner_rejects_bad_code():
    result = run_coding_tests("def nope():\n    return 1\n", "sum_positive", [
        {"name": "x", "args": [[]], "expected": 0}
    ])
    assert result["ok"] is False
    assert "sum_positive" in result["error"]
