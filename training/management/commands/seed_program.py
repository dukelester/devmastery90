"""Seed the complete 90-day DevMastery curriculum and all content banks."""
from datetime import date, timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from training.curriculum_data import DAYS, PHASES, SKILLS, WEEKS
from training.models import (
    CognitiveQuestion,
    EngineeringChallenge,
    InterviewQuestion,
    MockInterviewRound,
    Phase,
    Project,
    Skill,
    Task,
    TrainingDay,
    Week,
)

# Content banks seeded after (or even when) curriculum already exists.
CONTENT_SEEDS = (
    ("seed_practice", True),
    ("seed_engineering", True),
    ("seed_mock_interviews", True),
    ("seed_cognitive", True),
)


class Command(BaseCommand):
    help = (
        "Seed curriculum + practice, engineering labs, mock interviews, "
        "and cognitive banks. Safe to re-run; use --force to replace content."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-seed content banks (practice, labs, mocks, cognitive)",
        )
        parser.add_argument(
            "--curriculum-only",
            action="store_true",
            help="Only seed the 90-day curriculum (skip content banks)",
        )
        parser.add_argument(
            "--content-only",
            action="store_true",
            help="Only seed practice/labs/mocks/cognitive (skip curriculum)",
        )

    def handle(self, *args, **options):
        force = options["force"]
        curriculum_only = options["curriculum_only"]
        content_only = options["content_only"]

        if not content_only:
            self._seed_curriculum()

        if not curriculum_only:
            self._seed_content_banks(force=force)

        if not content_only:
            self._seed_project()

        self._print_summary()

    def _seed_curriculum(self):
        if Phase.objects.exists():
            self.stdout.write("Curriculum already seeded. Skipping curriculum.")
            return

        self.stdout.write("Seeding skills...")
        skill_map = {}
        for name, category in SKILLS:
            slug = slugify(name)
            skill, _ = Skill.objects.get_or_create(
                slug=slug,
                defaults={
                    "name": name,
                    "category": category,
                    "target_score": 8.0,
                    "current_score": 5.0,
                },
            )
            skill_map[slug] = skill

        self.stdout.write("Seeding phases and weeks...")
        phase_map = {}
        for phase_data in PHASES:
            phase = Phase.objects.create(
                name=phase_data["name"],
                description=phase_data["description"],
                order=phase_data["order"],
            )
            phase_map[phase_data["order"]] = phase

        week_map = {}
        start = date.today()
        for week_data in WEEKS:
            phase = phase_map[week_data["phase_order"]]
            week_start = start + timedelta(days=(week_data["week_number"] - 1) * 7)
            week_end = week_start + timedelta(days=6)
            week = Week.objects.create(
                phase=phase,
                week_number=week_data["week_number"],
                title=week_data["title"],
                objectives=week_data["objectives"],
                start_date=week_start,
                end_date=week_end,
            )
            week_map[week_data["week_number"]] = week

        self.stdout.write("Seeding 90 training days and tasks...")
        for day_data in DAYS:
            week = week_map[day_data["week_number"]]
            day_date = start + timedelta(days=day_data["day_number"] - 1)
            training_day = TrainingDay.objects.create(
                week=week,
                day_number=day_data["day_number"],
                date=day_date,
                title=day_data["title"],
                focus=day_data["focus"],
                objectives=day_data.get("objectives", ""),
                target_minutes=day_data["target_minutes"],
            )
            for task_data in day_data["tasks"]:
                title, desc, task_type, skill_slug, est, diff, prio, order = task_data
                skill = skill_map.get(skill_slug)
                Task.objects.create(
                    training_day=training_day,
                    skill=skill,
                    title=title,
                    description=desc,
                    task_type=task_type,
                    estimated_minutes=est,
                    difficulty=diff,
                    priority=prio,
                    order=order,
                )

        self.stdout.write(self.style.SUCCESS("Curriculum seeded."))

    def _seed_content_banks(self, force: bool = False):
        self.stdout.write("Seeding content banks (practice, labs, mocks, cognitive)...")
        for command_name, supports_force in CONTENT_SEEDS:
            kwargs = {}
            if supports_force and force:
                kwargs["force"] = True
            self.stdout.write(f"  → {command_name}" + (" --force" if kwargs.get("force") else ""))
            call_command(command_name, **kwargs)

    def _seed_project(self):
        Project.objects.get_or_create(
            name="AI Document Processing Platform",
            defaults={
                "description": (
                    "Multi-tenant document processing platform with AI integration, "
                    "Celery background jobs, and object storage."
                ),
                "status": "planned",
            },
        )

    def _print_summary(self):
        self.stdout.write(
            self.style.SUCCESS(
                "Seed complete — "
                f"{TrainingDay.objects.count()} days, "
                f"{Task.objects.count()} tasks, "
                f"{Skill.objects.count()} skills, "
                f"{InterviewQuestion.objects.count()} practice questions, "
                f"{EngineeringChallenge.objects.count()} engineering challenges, "
                f"{MockInterviewRound.objects.count()} mock rounds, "
                f"{CognitiveQuestion.objects.count()} cognitive questions."
            )
        )
