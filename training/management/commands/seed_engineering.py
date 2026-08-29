"""Seed engineering practice challenges."""
from django.core.management.base import BaseCommand

from training.engineering_data import ENGINEERING_CHALLENGES
from training.models import EngineeringChallenge


class Command(BaseCommand):
    help = "Seed engineering labs, benchmarks, debugging, and system design challenges"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Update existing challenges with latest lab steps and starter code",
        )

    def handle(self, *args, **options):
        force = options["force"]
        if EngineeringChallenge.objects.exists() and not force:
            self.stdout.write("Engineering challenges already seeded. Use --force to refresh.")
            return

        created = 0
        updated = 0
        for data in ENGINEERING_CHALLENGES:
            lookup = {
                "challenge_type": data["challenge_type"],
                "title": data["title"],
            }
            obj, was_created = EngineeringChallenge.objects.update_or_create(
                defaults=data,
                **lookup,
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Engineering challenges: {created} created, {updated} updated "
                f"({EngineeringChallenge.objects.count()} total)."
            )
        )
