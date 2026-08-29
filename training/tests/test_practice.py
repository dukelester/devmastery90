"""Tests for sequential practice question system."""
import pytest

from training.models import InterviewQuestion, PracticeProgress
from training.practice_bank import ALL_PRACTICE_QUESTIONS, SECTION_QUESTION_COUNTS
from training.services import (
    can_access_practice_question,
    get_unlocked_order,
    submit_practice_attempt,
)


@pytest.fixture
def practice_questions(db):
    if InterviewQuestion.objects.count() < 10:
        for q in ALL_PRACTICE_QUESTIONS[:20]:
            InterviewQuestion.objects.create(**q)
    return InterviewQuestion.objects.filter(section_slug="python").order_by("order")


@pytest.mark.django_db
class TestPracticeBank:
    def test_total_question_count(self):
        assert len(ALL_PRACTICE_QUESTIONS) == 1100
        assert all(c == 100 for c in SECTION_QUESTION_COUNTS.values())

    def test_questions_have_solution_code(self):
        with_code = sum(1 for q in ALL_PRACTICE_QUESTIONS if q.get("solution_code"))
        assert with_code > 1000


@pytest.mark.django_db
class TestPracticeSequential:
    def test_first_question_unlocked(self, user, practice_questions):
        q1 = practice_questions.first()
        assert can_access_practice_question(user, q1)
        assert get_unlocked_order(user, "python") == 1

    def test_second_question_locked_until_first_passed(self, user, practice_questions):
        q1, q2 = list(practice_questions[:2])
        assert not can_access_practice_question(user, q2)

        result = submit_practice_attempt(
            user, q1, {"answer": "test", "score": 7, "confidence": 6}
        )
        assert result["passed"]
        assert get_unlocked_order(user, "python") == 2
        assert can_access_practice_question(user, q2)

    def test_fail_does_not_unlock(self, user, practice_questions):
        q1 = practice_questions.first()
        result = submit_practice_attempt(
            user, q1, {"answer": "weak", "score": 3, "confidence": 4}
        )
        assert not result["passed"]
        assert get_unlocked_order(user, "python") == 1

    def test_locked_submit_rejected(self, user, practice_questions):
        q2 = practice_questions[1]
        result = submit_practice_attempt(
            user, q2, {"answer": "skip", "score": 9, "confidence": 9}
        )
        assert result["error"]
        assert not result["passed"]

    def test_practice_progress_created(self, user, practice_questions):
        q1 = practice_questions.first()
        submit_practice_attempt(user, q1, {"answer": "ok", "score": 8, "confidence": 7})
        assert PracticeProgress.objects.filter(user=user, section_slug="python").exists()


@pytest.mark.django_db
class TestPracticeHTMX:
    @property
    def htmx_headers(self):
        return {"HTTP_HX_REQUEST": "true"}

    def test_practice_submit_htmx(self, client, user, practice_questions):
        client.force_login(user)
        q1 = practice_questions.first()
        response = client.post(
            f"/interview/python/{q1.id}/submit/",
            {"answer": "solution", "score": 8, "confidence": 7},
            **self.htmx_headers,
        )
        assert response.status_code == 200
        assert "Reference solution" in response.content.decode() or "Passed" in response.content.decode()
