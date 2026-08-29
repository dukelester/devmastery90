"""Tests for bi-weekly mock interview system."""
import pytest

from training.mock_interview_data import build_mock_rounds
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
    questions = round_one.questions.order_by("order")
    assert questions.count() == 7
    assert questions.first().difficulty == "easy"
    assert questions.last().difficulty == "expert"
