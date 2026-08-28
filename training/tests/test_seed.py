"""Tests for seed_program command."""
import pytest
from django.core.management import call_command

from training.models import Phase, Skill, Task, TrainingDay


@pytest.mark.django_db
class TestSeedProgram:
    def test_seed_program_creates_curriculum(self):
        call_command("seed_program")
        assert Phase.objects.count() == 3
        assert Skill.objects.count() == 19
        assert TrainingDay.objects.count() == 90
        assert Task.objects.count() > 300

    def test_seed_program_idempotent(self):
        call_command("seed_program")
        count = TrainingDay.objects.count()
        call_command("seed_program")
        assert TrainingDay.objects.count() == count

    def test_all_days_have_tasks(self):
        call_command("seed_program")
        for day in TrainingDay.objects.all():
            assert day.tasks.count() > 0

    def test_day_numbers_sequential(self):
        call_command("seed_program")
        day_numbers = list(TrainingDay.objects.order_by("day_number").values_list("day_number", flat=True))
        assert day_numbers == list(range(1, 91))
