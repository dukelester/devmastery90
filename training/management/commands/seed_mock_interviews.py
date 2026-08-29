"""Seed bi-weekly mock interview rounds and questions."""
from django.core.management.base import BaseCommand

from training.mock_interview_data import build_mock_questions_for_round, build_mock_rounds
from training.models import MockInterviewQuestion, MockInterviewRound


class Command(BaseCommand):
    help = "Seed bi-weekly mock interview rounds (7 rounds × 7 structured questions)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Replace existing mock interview data",
        )

    def handle(self, *args, **options):
        if MockInterviewRound.objects.exists() and not options["force"]:
            self.stdout.write("Mock interviews already seeded. Use --force to replace.")
            return

        if options["force"]:
            MockInterviewQuestion.objects.all().delete()
            MockInterviewRound.objects.all().delete()
            self.stdout.write("Removed existing mock interview data.")

        for round_meta in build_mock_rounds():
            theme = round_meta.pop("theme")
            rnd = MockInterviewRound.objects.create(**round_meta)
            round_meta["theme"] = theme
            for qdata in build_mock_questions_for_round(round_meta):
                MockInterviewQuestion.objects.create(round=rnd, **qdata)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {MockInterviewRound.objects.count()} mock rounds, "
                f"{MockInterviewQuestion.objects.count()} questions."
            )
        )
