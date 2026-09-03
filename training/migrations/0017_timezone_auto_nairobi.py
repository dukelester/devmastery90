# Generated manually for timezone auto-detect + Nairobi default

from django.db import migrations, models
from django.db.models import Q


def forwards_timezone_defaults(apps, schema_editor):
    UserProfile = apps.get_model("training", "UserProfile")
    UserProfile.objects.filter(Q(timezone="") | Q(timezone="UTC")).update(
        timezone="Africa/Nairobi",
        timezone_auto=True,
    )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("training", "0016_email_reminders"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="timezone_auto",
            field=models.BooleanField(
                default=True,
                help_text="When true, timezone is kept in sync with the browser.",
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="timezone",
            field=models.CharField(
                blank=True,
                default="Africa/Nairobi",
                help_text="IANA timezone. Auto-detected from the browser; defaults to Africa/Nairobi.",
                max_length=80,
            ),
        ),
        migrations.RunPython(forwards_timezone_defaults, noop_reverse),
    ]
