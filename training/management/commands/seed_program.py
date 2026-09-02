"""Seed the DevMastery curriculum (90-day core + Phase 4 elite track) and content banks."""
from datetime import date, timedelta

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from training.curriculum_data import DAYS, PHASES, SKILLS, WEEKS
from training.curriculum_phase4 import PHASE4, PHASE4_DAYS, WEEKS_13_16
from training.models import (
    CognitiveQuestion,
    EngineeringChallenge,
    InterviewQuestion,
    LearningResource,
    MockInterviewRound,
    Phase,
    Project,
    Skill,
    Task,
    TrainingDay,
    Week,
)
from training.resource_data import RESOURCES

CONTENT_SEEDS = (
    ("seed_practice", True),
    ("seed_engineering", True),
    ("seed_mock_interviews", True),
    ("seed_cognitive", True),
    ("seed_projects", True),
)


class Command(BaseCommand):
    help = (
        "Seed curriculum (incl. Phase 4 days 91–120) + practice, labs, mocks, "
        "cognitive banks, and curated learning resources."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Re-seed content banks (practice, labs, mocks, cognitive, projects)",
        )
        parser.add_argument(
            "--curriculum-only",
            action="store_true",
            help="Only seed curriculum + resources (skip content banks)",
        )
        parser.add_argument(
            "--content-only",
            action="store_true",
            help="Only seed practice/labs/mocks/cognitive (skip curriculum)",
        )
        parser.add_argument(
            "--extend-phase4",
            action="store_true",
            help="Add Phase 4 (days 91–120) if missing on an existing 90-day DB",
        )

    def handle(self, *args, **options):
        force = options["force"]
        curriculum_only = options["curriculum_only"]
        content_only = options["content_only"]
        extend_phase4 = options["extend_phase4"]

        if not content_only:
            if extend_phase4 and Phase.objects.exists():
                self._extend_phase4()
            else:
                self._seed_curriculum()
            self._seed_resources()

        if not curriculum_only:
            self._seed_content_banks(force=force)

        if not content_only:
            self._seed_project()

        self._print_summary()

    def _skill_map(self) -> dict[str, Skill]:
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
        return skill_map

    def _seed_curriculum(self):
        if Phase.objects.exists():
            self.stdout.write("Curriculum already seeded. Use --extend-phase4 to add days 91–120.")
            self._extend_phase4()
            return

        self.stdout.write("Seeding skills...")
        skill_map = self._skill_map()

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

        self.stdout.write("Seeding training days and tasks (incl. Phase 4)...")
        self._create_days(DAYS, week_map, skill_map, start)
        self.stdout.write(self.style.SUCCESS("Curriculum seeded."))

    def _extend_phase4(self):
        if TrainingDay.objects.filter(day_number=120).exists():
            self.stdout.write("Phase 4 already present. Skipping extend.")
            return

        self.stdout.write("Extending curriculum with Phase 4 (days 91–120)...")
        skill_map = self._skill_map()

        phase, _ = Phase.objects.get_or_create(
            order=PHASE4["order"],
            defaults={
                "name": PHASE4["name"],
                "description": PHASE4["description"],
            },
        )

        start = date.today()
        first = TrainingDay.objects.order_by("day_number").first()
        if first and first.date:
            start = first.date - timedelta(days=first.day_number - 1)

        week_map = {}
        for week_data in WEEKS_13_16:
            week_start = start + timedelta(days=(week_data["week_number"] - 1) * 7)
            week_end = week_start + timedelta(days=6)
            week, _ = Week.objects.get_or_create(
                phase=phase,
                week_number=week_data["week_number"],
                defaults={
                    "title": week_data["title"],
                    "objectives": week_data["objectives"],
                    "start_date": week_start,
                    "end_date": week_end,
                },
            )
            week_map[week_data["week_number"]] = week

        self._create_days(PHASE4_DAYS, week_map, skill_map, start)
        self.stdout.write(self.style.SUCCESS("Phase 4 extended."))

    def _create_days(self, days, week_map, skill_map, start: date):
        for day_data in days:
            if TrainingDay.objects.filter(day_number=day_data["day_number"]).exists():
                continue
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

    def _seed_resources(self):
        self.stdout.write("Seeding curated learning resources...")
        skill_map = {s.slug: s for s in Skill.objects.all()}
        created = 0
        for item in RESOURCES:
            skill = skill_map.get(item.get("skill_slug") or "")
            defaults = {
                "title": item["title"],
                "resource_type": item["resource_type"],
                "description": item.get("description", ""),
                "is_primary": item.get("is_primary", False),
                "order": item.get("order", 0),
                "week_number": item.get("week_number"),
            }
            obj, was_created = LearningResource.objects.update_or_create(
                url=item["url"],
                day_number=item.get("day_number"),
                skill=skill,
                defaults=defaults,
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Resources ready ({created} new)."))

    def _seed_content_banks(self, force: bool = False):
        self.stdout.write("Seeding content banks (practice, labs, mocks, cognitive)...")
        for command_name, supports_force in CONTENT_SEEDS:
            kwargs = {}
            if supports_force and force:
                kwargs["force"] = True
            self.stdout.write(f"  → {command_name}" + (" --force" if kwargs.get("force") else ""))
            call_command(command_name, **kwargs)

    def _seed_project(self):
        call_command("seed_projects")

    def _print_summary(self):
        self.stdout.write(
            self.style.SUCCESS(
                "Seed complete — "
                f"{TrainingDay.objects.count()} days, "
                f"{Task.objects.count()} tasks, "
                f"{Skill.objects.count()} skills, "
                f"{LearningResource.objects.count()} resources, "
                f"{InterviewQuestion.objects.count()} practice questions, "
                f"{EngineeringChallenge.objects.count()} engineering challenges, "
                f"{MockInterviewRound.objects.count()} mock rounds, "
                f"{CognitiveQuestion.objects.count()} cognitive questions, "
                f"{Project.objects.filter(is_catalog=True).count()} catalog projects."
            )
        )
