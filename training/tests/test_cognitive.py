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


@pytest.mark.django_db
def test_cognitive_queue_hides_revealed_by_default(django_user_model):
    from training.models import CognitiveProgress
    from training.services import get_cognitive_list_data, get_cognitive_question_data, reveal_cognitive_answer

    user = django_user_model.objects.create_user(username="cog", password="x")
    q1 = CognitiveQuestion.objects.create(
        challenge_type="aptitude",
        category="num",
        difficulty="easy",
        order=1,
        question="Q1",
        answer="A",
    )
    q2 = CognitiveQuestion.objects.create(
        challenge_type="aptitude",
        category="num",
        difficulty="easy",
        order=2,
        question="Q2",
        answer="B",
    )
    CognitiveQuestion.objects.create(
        challenge_type="aptitude",
        category="num",
        difficulty="easy",
        order=3,
        question="Q3",
        answer="C",
    )
    reveal_cognitive_answer(user, q1.id, attempted_answer="A")

    open_list = get_cognitive_list_data(user, "aptitude", show="open")
    assert [q.order for q in open_list["questions"]] == [2, 3]
    assert open_list["open_count"] == 2
    assert open_list["revealed_count"] == 1

    all_list = get_cognitive_list_data(user, "aptitude", show="all")
    assert len(all_list["questions"]) == 3

    data = get_cognitive_question_data(user, q2.id)
    assert data["next_question"].order == 3
    assert data["prev_question"] is None  # q1 revealed

    revealed = reveal_cognitive_answer(user, q2.id, attempted_answer="B")
    assert revealed["next_question"].order == 3
    assert CognitiveProgress.objects.filter(user=user, revealed=True).count() == 2
