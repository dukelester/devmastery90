"""Seed aptitude tests and brain teaser cognitive challenges."""
from django.core.management.base import BaseCommand
from django.db.models import Max

from training.cognitive_bank import APTITUDE_QUESTIONS, BRAIN_TEASER_QUESTIONS, COGNITIVE_COUNTS
from training.cognitive_bank.shape_patterns import (
    build_shape_brain_teasers,
    build_shape_pattern_questions,
)
from training.models import CognitiveQuestion


class Command(BaseCommand):
    help = "Seed aptitude tests and brain teaser cognitive challenges"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Replace existing questions")
        parser.add_argument(
            "--append-new",
            action="store_true",
            help="Append any bank questions missing by question text",
        )

    def handle(self, *args, **options):
        if options["force"]:
            CognitiveQuestion.objects.all().delete()
            self.stdout.write("Removed existing cognitive questions.")
            self._seed_full()
            return

        if not CognitiveQuestion.objects.exists():
            self._seed_full()
            return

        if options["append_new"]:
            added = self._append_by_text()
            self.stdout.write(self.style.SUCCESS(f"Appended {added} new cognitive questions."))
            return

        added = self._ensure_shape_bank()
        if added:
            self.stdout.write(
                self.style.SUCCESS(f"Added {added} shape / spatial cognitive questions.")
            )
        else:
            self.stdout.write(
                "Cognitive questions up to date. Use --force to fully replace, "
                "or --append-new to sync the whole bank."
            )

    def _seed_full(self):
        created = 0
        created += self._bulk_create("aptitude", APTITUDE_QUESTIONS, start_order=1)
        created += self._bulk_create("brain_teaser", BRAIN_TEASER_QUESTIONS, start_order=1)
        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {created} cognitive challenges "
                f"({COGNITIVE_COUNTS['aptitude']} aptitude, "
                f"{COGNITIVE_COUNTS['brain_teaser']} brain teasers)."
            )
        )

    def _bulk_create(self, challenge_type: str, questions: list, start_order: int) -> int:
        objs = [
            CognitiveQuestion(
                challenge_type=challenge_type,
                category=q["category"],
                order=start_order + i,
                difficulty=q.get("difficulty", "medium"),
                question=q["question"],
                answer=q["answer"],
                explanation=q.get("explanation", ""),
                hints=q.get("hints", ""),
                choices=q.get("choices") or [],
            )
            for i, q in enumerate(questions)
        ]
        CognitiveQuestion.objects.bulk_create(objs, batch_size=500)
        return len(objs)

    def _next_order(self, challenge_type: str) -> int:
        return (
            CognitiveQuestion.objects.filter(challenge_type=challenge_type).aggregate(
                m=Max("order")
            )["m"]
            or 0
        ) + 1

    def _ensure_shape_bank(self) -> int:
        added = 0
        shape_bank = build_shape_pattern_questions()
        have = CognitiveQuestion.objects.filter(
            challenge_type="aptitude", category="shape_patterns"
        ).count()
        with_choices = CognitiveQuestion.objects.filter(
            challenge_type="aptitude",
            category="shape_patterns",
        ).exclude(choices=[]).count()
        needs_refresh = have < len(shape_bank) or with_choices < have or have == 0
        if needs_refresh:
            CognitiveQuestion.objects.filter(
                challenge_type="aptitude", category="shape_patterns"
            ).delete()
            # Also clear spatial MCQ shape teasers we own (matched by question text)
            teaser_bank = build_shape_brain_teasers()
            teaser_texts = [q["question"] for q in teaser_bank]
            CognitiveQuestion.objects.filter(
                challenge_type="brain_teaser", question__in=teaser_texts
            ).delete()
            added += self._bulk_create(
                "aptitude", shape_bank, start_order=self._next_order("aptitude")
            )
            added += self._bulk_create(
                "brain_teaser", teaser_bank, start_order=self._next_order("brain_teaser")
            )
            return added

        teasers = build_shape_brain_teasers()
        existing = set(
            CognitiveQuestion.objects.filter(challenge_type="brain_teaser").values_list(
                "question", flat=True
            )
        )
        missing = [q for q in teasers if q["question"] not in existing]
        if missing:
            added += self._bulk_create(
                "brain_teaser", missing, start_order=self._next_order("brain_teaser")
            )
        return added

    def _append_by_text(self) -> int:
        added = 0
        for challenge_type, bank in (
            ("aptitude", APTITUDE_QUESTIONS),
            ("brain_teaser", BRAIN_TEASER_QUESTIONS),
        ):
            existing = set(
                CognitiveQuestion.objects.filter(challenge_type=challenge_type).values_list(
                    "question", flat=True
                )
            )
            missing = [q for q in bank if q["question"] not in existing]
            if missing:
                added += self._bulk_create(
                    challenge_type, missing, start_order=self._next_order(challenge_type)
                )
        return added
