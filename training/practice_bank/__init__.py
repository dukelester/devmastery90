"""Aggregate topic banks and build all practice questions."""
from training.practice_bank.builder import build_level_section_questions, build_section_questions
from training.practice_bank.topics.debugging import DEBUGGING_BY_LEVEL
from training.practice_bank.topics.django import DJANGO_TOPICS
from training.practice_bank.topics.dsa import DSA_TOPICS
from training.practice_bank.topics.misc import (
    AI_TOPICS,
    BEHAVIORAL_TOPICS,
    CLOUD_TOPICS,
    DEVOPS_TOPICS,
    POSTGRES_TOPICS,
    REST_TOPICS,
    SYSTEM_DESIGN_TOPICS,
    TESTING_TOPICS,
)
from training.practice_bank.topics.python import PYTHON_TOPICS

ALL_PRACTICE_QUESTIONS: list[dict] = [
    *build_section_questions("python", "Python", PYTHON_TOPICS),
    *build_section_questions("django", "Django", DJANGO_TOPICS),
    *build_section_questions("rest", "REST APIs", REST_TOPICS),
    *build_section_questions("postgresql", "PostgreSQL", POSTGRES_TOPICS),
    *build_section_questions("system-design", "System Design", SYSTEM_DESIGN_TOPICS),
    *build_section_questions("dsa", "DSA", DSA_TOPICS),
    *build_section_questions("testing", "Testing", TESTING_TOPICS),
    *build_section_questions("devops", "DevOps", DEVOPS_TOPICS),
    *build_section_questions("cloud", "Cloud", CLOUD_TOPICS),
    *build_section_questions("ai", "AI Engineering", AI_TOPICS),
    *build_section_questions("behavioral", "Behavioral", BEHAVIORAL_TOPICS),
    *build_level_section_questions("debugging", "Debugging", DEBUGGING_BY_LEVEL),
]

SECTION_QUESTION_COUNTS = {
    "python": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "python"]),
    "django": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "django"]),
    "rest": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "rest"]),
    "postgresql": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "postgresql"]),
    "system-design": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "system-design"]),
    "dsa": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "dsa"]),
    "testing": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "testing"]),
    "devops": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "devops"]),
    "cloud": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "cloud"]),
    "ai": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "ai"]),
    "behavioral": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "behavioral"]),
    "debugging": len([q for q in ALL_PRACTICE_QUESTIONS if q["section_slug"] == "debugging"]),
}
