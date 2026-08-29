"""Seed detailed catalog projects for the Projects hub."""
from django.core.management.base import BaseCommand

from training.models import Project
from training.project_data import PROJECTS


class Command(BaseCommand):
    help = "Seed well-documented catalog projects with acceptance criteria."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Update existing catalog projects by slug",
        )

    def handle(self, *args, **options):
        force = options["force"]
        created = 0
        updated = 0
        for raw in PROJECTS:
            defaults = {
                "name": raw["name"],
                "tagline": raw.get("tagline", ""),
                "description": raw.get("overview", ""),
                "overview": raw.get("overview", ""),
                "problem_statement": raw.get("problem_statement", ""),
                "difficulty": raw.get("difficulty", "hard"),
                "estimated_hours": raw.get("estimated_hours", 40),
                "week_focus": raw.get("week_focus"),
                "tech_stack": raw.get("tech_stack", []),
                "learning_outcomes": raw.get("learning_outcomes", []),
                "features": raw.get("features", []),
                "functional_requirements": raw.get("functional_requirements", []),
                "non_functional_requirements": raw.get("non_functional_requirements", []),
                "acceptance_criteria": raw.get("acceptance_criteria", []),
                "milestones": raw.get("milestones", []),
                "deliverables": raw.get("deliverables", []),
                "getting_started": raw.get("getting_started", ""),
                "architecture_notes": raw.get("architecture_notes", ""),
                "resources": raw.get("resources", []),
                "order": raw.get("order", 0),
                "is_catalog": True,
                "is_featured": raw.get("is_featured", False),
                "status": "planned",
                "user": None,
            }
            obj = Project.objects.filter(slug=raw["slug"]).first()
            if obj is None:
                Project.objects.create(slug=raw["slug"], **defaults)
                created += 1
            elif force:
                for key, value in defaults.items():
                    setattr(obj, key, value)
                obj.slug = raw["slug"]
                obj.save()
                updated += 1
        self.stdout.write(
            self.style.SUCCESS(
                f"Projects seed complete — created {created}, updated {updated} "
                f"({Project.objects.filter(is_catalog=True).count()} catalog total)."
            )
        )
