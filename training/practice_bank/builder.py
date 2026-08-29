"""Build sequential practice question sets from topic banks."""
from training.models import ProficiencyLevel, PROFICIENCY_ORDER
from training.practice_bank.sections import QUESTIONS_PER_SECTION, QUESTIONS_PER_LEVEL

TopicDict = dict[str, str | int]


def _level_for_order(order: int) -> str:
    idx = min((order - 1) // QUESTIONS_PER_LEVEL, len(PROFICIENCY_ORDER) - 1)
    return PROFICIENCY_ORDER[idx]


def _difficulty_for_level(level: str) -> str:
    mapping = {
        ProficiencyLevel.BEGINNER: "easy",
        ProficiencyLevel.EASY: "easy",
        ProficiencyLevel.MEDIUM: "medium",
        ProficiencyLevel.HARD: "hard",
        ProficiencyLevel.EXPERT: "expert",
        ProficiencyLevel.ELITE: "expert",
    }
    return mapping.get(level, "medium")


def build_level_section_questions(
    section_slug: str,
    category: str,
    topics_by_level: dict[str, list[TopicDict]],
) -> list[dict]:
    """Build questions with explicit per-level topic lists (e.g. debugging track)."""
    questions: list[dict] = []
    order = 1
    for level in PROFICIENCY_ORDER:
        for topic in topics_by_level.get(level, []):
            questions.append(
                {
                    "section_slug": section_slug,
                    "category": category,
                    "order": order,
                    "level": level,
                    "difficulty": _difficulty_for_level(level),
                    "question": str(topic["question"]),
                    "buggy_code": str(topic.get("buggy_code", "")),
                    "ideal_topics": str(topic.get("ideal_topics", "")),
                    "solution_code": str(topic.get("solution_code", "")),
                    "solution_explanation": str(topic.get("solution_explanation", "")),
                    "hints": str(topic.get("hints", "")),
                    "learning_objectives": str(topic.get("learning_objectives", "")),
                    "time_estimate_minutes": int(topic.get("time_estimate_minutes", 15)),
                    "min_pass_score": float(topic.get("min_pass_score", 6.0)),
                }
            )
            order += 1
    return questions


def build_section_questions(
    section_slug: str,
    category: str,
    topics: list[TopicDict],
    count: int = QUESTIONS_PER_SECTION,
) -> list[dict]:
    """Expand topic bank into sequential questions with level progression."""
    if not topics:
        raise ValueError(f"No topics for section {section_slug}")

    questions: list[dict] = []
    for order in range(1, count + 1):
        topic = topics[(order - 1) % len(topics)]
        level = _level_for_order(order)
        cycle = (order - 1) // len(topics) + 1
        base_question = str(topic["question"])
        if cycle > 1:
            question_text = f"{base_question} (Challenge {cycle})"
        else:
            question_text = base_question

        questions.append(
            {
                "section_slug": section_slug,
                "category": category,
                "order": order,
                "level": level,
                "difficulty": _difficulty_for_level(level),
                "question": question_text,
                "ideal_topics": str(topic.get("ideal_topics", "")),
                "solution_code": str(topic.get("solution_code", "")),
                "solution_explanation": str(topic.get("solution_explanation", "")),
                "hints": str(topic.get("hints", "")),
                "learning_objectives": str(topic.get("learning_objectives", "")),
                "time_estimate_minutes": int(topic.get("time_estimate_minutes", 15)),
                "min_pass_score": float(topic.get("min_pass_score", 6.0)),
            }
        )
    return questions
