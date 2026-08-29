"""Aggregate cognitive challenge banks."""
from training.cognitive_bank.aptitude import build_aptitude_questions
from training.cognitive_bank.brain_teasers import build_brain_teasers

APTITUDE_QUESTIONS = build_aptitude_questions()
BRAIN_TEASER_QUESTIONS = build_brain_teasers()

COGNITIVE_COUNTS = {
    "aptitude": len(APTITUDE_QUESTIONS),
    "brain_teaser": len(BRAIN_TEASER_QUESTIONS),
    "total": len(APTITUDE_QUESTIONS) + len(BRAIN_TEASER_QUESTIONS),
}
