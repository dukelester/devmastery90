"""Drop training tables and re-apply migrations (fixes bigint vs UUID schema drift)."""
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


TRAINING_TABLES = [
  "training_practiceprogress",
    "training_weeklyreview",
    "training_dailyreview",
    "training_interviewattempt",
    "training_interviewquestion",
    "training_mistake",
    "training_assessmentattempt",
    "training_assessment",
    "training_studysession",
    "training_codingproblem",
    "training_task",
    "training_trainingday",
    "training_week",
    "training_phase",
    "training_skill",
    "training_userprofile",
    "training_project",
]


class Command(BaseCommand):
    help = "Reset training DB schema to match UUID migrations (destructive)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--seed",
            action="store_true",
            help="Run seed_program after reset",
        )
        parser.add_argument(
            "--no-input",
            action="store_true",
            help="Skip confirmation",
        )

    def handle(self, *args, **options):
        if not options["no_input"]:
            confirm = input(
                "This deletes ALL training data and rebuilds tables. Continue? [y/N] "
            )
            if confirm.lower() != "y":
                self.stdout.write("Aborted.")
                return

        with connection.cursor() as cursor:
            for table in TRAINING_TABLES:
                cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            cursor.execute("DELETE FROM django_migrations WHERE app = %s", ["training"])

        self.stdout.write("Dropped training tables and migration history.")

        call_command("migrate", "training", verbosity=options.get("verbosity", 1))

        if options["seed"]:
            call_command("seed_program")
            self.stdout.write(self.style.SUCCESS("Schema reset and curriculum seeded."))
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "Schema reset. Run: python manage.py seed_program"
                )
            )
