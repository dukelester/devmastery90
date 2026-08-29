"""Tests for debugging practice section."""
import pytest

from training.models import ProficiencyLevel, PROFICIENCY_ORDER
from training.practice_bank import ALL_PRACTICE_QUESTIONS, SECTION_QUESTION_COUNTS
from training.practice_bank.topics.debugging import DEBUGGING_BY_LEVEL


@pytest.mark.parametrize("level", [lvl.value for lvl in ProficiencyLevel])
def test_debugging_level_has_twenty_topics(level):
    assert len(DEBUGGING_BY_LEVEL[level]) == 20


def test_debugging_section_total_count():
    assert SECTION_QUESTION_COUNTS["debugging"] == 120


def test_debugging_questions_sequential_orders():
    debugging = [q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "debugging"]
    assert len(debugging) == 120
    orders = [q["order"] for q in debugging]
    assert orders == list(range(1, 121))


def test_debugging_questions_have_buggy_code():
    debugging = [q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "debugging"]
    assert all(q.get("buggy_code") for q in debugging)
    assert all(q.get("solution_code") for q in debugging)


def test_debugging_level_progression():
    debugging = [q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "debugging"]
    for level in PROFICIENCY_ORDER:
        level_qs = [q for q in debugging if q["level"] == level]
        assert len(level_qs) == 20
