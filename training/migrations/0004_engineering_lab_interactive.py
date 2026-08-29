import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0003_engineeringchallenge_careergoal_engineeringattempt_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="engineeringchallenge",
            name="hints",
            field=models.TextField(
                blank=True, help_text="One hint per line, revealed progressively"
            ),
        ),
        migrations.AddField(
            model_name="engineeringchallenge",
            name="lab_steps",
            field=models.JSONField(
                blank=True, default=list, help_text="Ordered checklist steps"
            ),
        ),
        migrations.AddField(
            model_name="engineeringchallenge",
            name="starter_code",
            field=models.TextField(
                blank=True, help_text="Editable starter code for the lab workspace"
            ),
        ),
        migrations.AddField(
            model_name="engineeringchallenge",
            name="success_criteria",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="engineeringattempt",
            name="code_submission",
            field=models.TextField(blank=True),
        ),
        migrations.CreateModel(
            name="EngineeringLabSession",
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
                ("code_workspace", models.TextField(blank=True)),
                ("completed_steps", models.JSONField(default=list)),
                ("hints_revealed", models.PositiveSmallIntegerField(default=0)),
                ("timer_started_at", models.DateTimeField(blank=True, null=True)),
                ("accumulated_minutes", models.PositiveIntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "challenge",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lab_sessions",
                        to="training.engineeringchallenge",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="engineering_lab_sessions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "indexes": [
                    models.Index(
                        fields=["user", "challenge"],
                        name="training_en_user_id_8a1f2c_idx",
                    )
                ],
                "unique_together": {("user", "challenge")},
            },
        ),
    ]
