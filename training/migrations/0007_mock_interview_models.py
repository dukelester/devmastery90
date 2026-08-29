import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0006_interviewquestion_buggy_code"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="MockInterviewRound",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("round_number", models.PositiveSmallIntegerField(unique=True)),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("unlock_day", models.PositiveIntegerField()),
                ("period_end_day", models.PositiveIntegerField()),
                ("duration_minutes", models.PositiveIntegerField(default=90)),
                ("focus_areas", models.TextField(blank=True)),
            ],
            options={"ordering": ["round_number"]},
        ),
        migrations.CreateModel(
            name="MockInterviewSession",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                        ],
                        default="in_progress",
                        max_length=20,
                    ),
                ),
                ("started_at", models.DateTimeField()),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("current_order", models.PositiveSmallIntegerField(default=1)),
                ("question_started_at", models.DateTimeField(blank=True, null=True)),
                ("total_score", models.FloatField(default=0.0)),
                ("max_score", models.FloatField(default=0.0)),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sessions",
                        to="training.mockinterviewround",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="mock_interview_sessions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-started_at"]},
        ),
        migrations.CreateModel(
            name="MockInterviewQuestion",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("order", models.PositiveSmallIntegerField()),
                (
                    "interview_type",
                    models.CharField(
                        choices=[
                            ("behavioral", "Behavioral"),
                            ("technical", "Technical"),
                            ("coding", "Coding"),
                            ("system_design", "System Design"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("easy", "Easy"),
                            ("medium", "Medium"),
                            ("hard", "Hard"),
                            ("expert", "Expert"),
                        ],
                        max_length=10,
                    ),
                ),
                ("question", models.TextField()),
                ("time_limit_minutes", models.PositiveSmallIntegerField(default=10)),
                ("rubric", models.TextField(blank=True)),
                ("sample_answer", models.TextField(blank=True)),
                ("hints", models.TextField(blank=True)),
                (
                    "round",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="questions",
                        to="training.mockinterviewround",
                    ),
                ),
            ],
            options={
                "ordering": ["round", "order"],
                "unique_together": {("round", "order")},
            },
        ),
        migrations.CreateModel(
            name="MockInterviewResponse",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("order", models.PositiveSmallIntegerField()),
                ("answer", models.TextField(blank=True)),
                (
                    "score",
                    models.FloatField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                (
                    "confidence",
                    models.FloatField(
                        default=5.0,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                ("time_spent_seconds", models.PositiveIntegerField(default=0)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responses",
                        to="training.mockinterviewquestion",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="responses",
                        to="training.mockinterviewsession",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
                "unique_together": {("session", "order")},
            },
        ),
        migrations.AddIndex(
            model_name="mockinterviewquestion",
            index=models.Index(
                fields=["round", "order"], name="training_mo_round_i_4a8f21_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="mockinterviewsession",
            index=models.Index(
                fields=["user", "status"], name="training_mo_user_id_91c2a4_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="mockinterviewsession",
            index=models.Index(
                fields=["user", "round"], name="training_mo_user_id_2b7e18_idx"
            ),
        ),
    ]
