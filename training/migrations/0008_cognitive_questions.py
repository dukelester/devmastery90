import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0007_mock_interview_models"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CognitiveQuestion",
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
                    "challenge_type",
                    models.CharField(
                        choices=[
                            ("aptitude", "Aptitude"),
                            ("brain_teaser", "Brain Teaser"),
                        ],
                        max_length=20,
                    ),
                ),
                ("category", models.CharField(max_length=80)),
                ("order", models.PositiveIntegerField()),
                (
                    "difficulty",
                    models.CharField(
                        choices=[
                            ("easy", "Easy"),
                            ("medium", "Medium"),
                            ("hard", "Hard"),
                            ("expert", "Expert"),
                        ],
                        default="medium",
                        max_length=10,
                    ),
                ),
                ("question", models.TextField()),
                ("answer", models.TextField()),
                ("explanation", models.TextField(blank=True)),
                ("hints", models.TextField(blank=True)),
            ],
            options={
                "ordering": ["challenge_type", "order"],
                "indexes": [
                    models.Index(
                        fields=["challenge_type"],
                        name="training_co_challen_91a2b1_idx",
                    ),
                    models.Index(
                        fields=["challenge_type", "category"],
                        name="training_co_challen_4c8e22_idx",
                    ),
                    models.Index(
                        fields=["challenge_type", "order"],
                        name="training_co_challen_7f3a19_idx",
                    ),
                ],
                "constraints": [
                    models.UniqueConstraint(
                        fields=("challenge_type", "order"),
                        name="unique_cognitive_type_order",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="CognitiveProgress",
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
                ("revealed", models.BooleanField(default=False)),
                ("revealed_at", models.DateTimeField(blank=True, null=True)),
                ("attempted_answer", models.TextField(blank=True)),
                ("notes", models.TextField(blank=True)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="progress",
                        to="training.cognitivequestion",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cognitive_progress",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["user", "revealed"],
                        name="training_co_user_id_2e8f44_idx",
                    )
                ],
                "unique_together": {("user", "question")},
            },
        ),
    ]
