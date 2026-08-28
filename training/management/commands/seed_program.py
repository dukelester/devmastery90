"""Seed the complete 90-day DevMastery curriculum."""
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from training.curriculum_data import DAYS, PHASES, SKILLS, WEEKS
from training.models import InterviewQuestion, Phase, Project, Skill, Task, TrainingDay, Week

INTERVIEW_QUESTIONS = [
    ("Python", "Explain Python's object model and MRO.", "types, inheritance, MRO, super()", "medium"),
    ("Python", "How do decorators work internally?", "closures, wrappers, functools", "hard"),
    ("Python", "Difference between generators and iterators?", "yield, lazy evaluation, memory", "medium"),
    ("Django", "Explain Django's request/response cycle.", "middleware, views, URLs", "medium"),
    ("Django", "How do Django migrations work?", "schema changes, squashing, rollback", "medium"),
    ("REST", "Design a RESTful API for a resource.", "resources, HTTP methods, status codes", "medium"),
    ("REST", "How do you handle API versioning?", "URL, header, query param versioning", "medium"),
    ("PostgreSQL", "Explain index types and when to use each.", "B-tree, GIN, GiST, partial indexes", "hard"),
    ("PostgreSQL", "How do you optimize a slow query?", "EXPLAIN ANALYZE, indexes, query rewrite", "hard"),
    ("System Design", "Design a URL shortener.", "hashing, storage, caching, scaling", "hard"),
    ("System Design", "Design a real-time chat system.", "WebSockets, message queues, presence", "hard"),
    ("System Design", "Design a payment processing system.", "idempotency, consistency, fraud", "hard"),
    ("DSA", "Find the longest substring without repeating characters.", "sliding window, hash map", "medium"),
    ("DSA", "Implement LRU cache.", "hash map, doubly linked list", "hard"),
    ("Testing", "How do you test async code?", "pytest-asyncio, mocking, fixtures", "medium"),
    ("DevOps", "Explain CI/CD pipeline stages.", "build, test, deploy, rollback", "medium"),
    ("Cloud", "How does auto-scaling work on AWS?", "EC2, load balancers, CloudWatch", "medium"),
    ("AI", "How do you integrate LLM APIs safely?", "rate limits, retries, cost control", "medium"),
    ("Behavioral", "Describe a production incident you resolved.", "STAR method, root cause, prevention", "medium"),
    ("Behavioral", "How do you handle technical disagreements?", "communication, data-driven decisions", "medium"),
]


class Command(BaseCommand):
    help = "Seed the complete 90-day DevMastery curriculum"

    def handle(self, *args, **options):
        if Phase.objects.exists():
            self.stdout.write("Curriculum already seeded. Skipping.")
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

        self.stdout.write("Seeding interview questions...")
        for category, question, topics, difficulty in INTERVIEW_QUESTIONS:
            InterviewQuestion.objects.get_or_create(
                question=question,
                defaults={
                    "category": category,
                    "ideal_topics": topics,
                    "difficulty": difficulty,
                },
            )

        self.stdout.write("Seeding project...")
        Project.objects.get_or_create(
            name="AI Document Processing Platform",
            defaults={
                "description": "Multi-tenant document processing platform with AI integration, Celery background jobs, and object storage.",
                "status": "planned",
            },
        )

        day_count = TrainingDay.objects.count()
        task_count = Task.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"Seeded {day_count} days, {task_count} tasks, "
            f"{Skill.objects.count()} skills, {InterviewQuestion.objects.count()} interview questions."
        ))
