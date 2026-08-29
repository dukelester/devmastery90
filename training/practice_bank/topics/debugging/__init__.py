"""Debugging practice topic bank — per-level exports."""

from training.practice_bank.topics.debugging.beginner import TOPICS as BEGINNER_TOPICS
from training.practice_bank.topics.debugging.easy import TOPICS as EASY_TOPICS
from training.practice_bank.topics.debugging.medium import TOPICS as MEDIUM_TOPICS
from training.practice_bank.topics.debugging.hard import TOPICS as HARD_TOPICS
from training.practice_bank.topics.debugging.expert import TOPICS as EXPERT_TOPICS
from training.practice_bank.topics.debugging.elite import TOPICS as ELITE_TOPICS

DEBUGGING_BY_LEVEL: dict[str, list[dict]] = {
    "beginner": BEGINNER_TOPICS,
    "easy": EASY_TOPICS,
    "medium": MEDIUM_TOPICS,
    "hard": HARD_TOPICS,
    "expert": EXPERT_TOPICS,
    "elite": ELITE_TOPICS,
}

__all__ = ["DEBUGGING_BY_LEVEL"]
