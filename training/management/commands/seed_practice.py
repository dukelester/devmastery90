"""Seed ~100 sequential practice questions per section."""
from django.core.management.base import BaseCommand

from training.models import InterviewQuestion
from training.practice_bank import ALL_PRACTICE_QUESTIONS, SECTION_QUESTION_COUNTS


class Command(BaseCommand):
    help = "Seed sequential practice questions (100 per section)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Replace existing practice questions",
        )

    def handle(self, *args, **options):
        if InterviewQuestion.objects.exists() and not options["force"]:
            self.stdout.write(
                "Practice questions exist. Use --force to replace."
            )
            return

        if options["force"]:
            InterviewQuestion.objects.all().delete()
            self.stdout.write("Removed existing practice questions.")

        created = 0
        for qdata in ALL_PRACTICE_QUESTIONS:
            InterviewQuestion.objects.create(**qdata)
            created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {created} practice questions across "
            f"{len(SECTION_QUESTION_COUNTS)} sections."
        ))
        for slug, count in SECTION_QUESTION_COUNTS.items():
            self.stdout.write(f"  {slug}: {count}")
