"""Tests for cognitive aptitude and brain teasers."""
import pytest

from training.cognitive_bank import COGNITIVE_COUNTS
from training.models import CognitiveQuestion


def test_cognitive_bank_size():
    assert COGNITIVE_COUNTS["aptitude"] >= 200
    assert COGNITIVE_COUNTS["brain_teaser"] >= 180
    assert COGNITIVE_COUNTS["total"] >= 400


def test_aptitude_time_limits_by_difficulty():
    easy = CognitiveQuestion(
        challenge_type="aptitude", difficulty="easy", order=1, category="x", question="q", answer="a"
    )
    medium = CognitiveQuestion(
        challenge_type="aptitude", difficulty="medium", order=2, category="x", question="q", answer="a"
    )
    hard = CognitiveQuestion(
        challenge_type="aptitude", difficulty="hard", order=3, category="x", question="q", answer="a"
    )
    assert easy.time_limit_seconds == 45
    assert medium.time_limit_seconds == 75
    assert hard.time_limit_seconds == 90
    assert easy.time_limit_label == "45s"
    assert medium.time_limit_label == "1m 15s"


@pytest.mark.django_db
def test_seed_cognitive_command():
    from django.core.management import call_command

    call_command("seed_cognitive", force=True)
    assert CognitiveQuestion.objects.filter(challenge_type="aptitude").count() == COGNITIVE_COUNTS["aptitude"]
    assert CognitiveQuestion.objects.filter(challenge_type="brain_teaser").count() == COGNITIVE_COUNTS["brain_teaser"]
