"""Seed aptitude tests and brain teasers."""
from django.core.management.base import BaseCommand

from training.cognitive_bank import APTITUDE_QUESTIONS, BRAIN_TEASER_QUESTIONS, COGNITIVE_COUNTS
from training.models import CognitiveQuestion


class Command(BaseCommand):
    help = "Seed aptitude tests and brain teaser cognitive challenges"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Replace existing questions")

    def handle(self, *args, **options):
        if CognitiveQuestion.objects.exists() and not options["force"]:
            self.stdout.write("Cognitive questions exist. Use --force to replace.")
            return

        if options["force"]:
            CognitiveQuestion.objects.all().delete()
            self.stdout.write("Removed existing cognitive questions.")

        created = 0
        for order, q in enumerate(APTITUDE_QUESTIONS, start=1):
            CognitiveQuestion.objects.create(
                challenge_type="aptitude",
                category=q["category"],
                order=order,
                difficulty=q.get("difficulty", "medium"),
                question=q["question"],
                answer=q["answer"],
                explanation=q.get("explanation", ""),
                hints=q.get("hints", ""),
            )
            created += 1

        for order, q in enumerate(BRAIN_TEASER_QUESTIONS, start=1):
            CognitiveQuestion.objects.create(
                challenge_type="brain_teaser",
                category=q["category"],
                order=order,
                difficulty=q.get("difficulty", "medium"),
                question=q["question"],
                answer=q["answer"],
                explanation=q.get("explanation", ""),
                hints=q.get("hints", ""),
            )
            created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created} cognitive challenges "
                f"({COGNITIVE_COUNTS['aptitude']} aptitude, "
                f"{COGNITIVE_COUNTS['brain_teaser']} brain teasers)."
            )
        )
