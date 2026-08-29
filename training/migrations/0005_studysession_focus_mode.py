from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0004_engineering_lab_interactive"),
    ]

    operations = [
        migrations.AddField(
            model_name="studysession",
            name="mode",
            field=models.CharField(
                choices=[("elapsed", "Elapsed"), ("focus", "Focus")],
                default="elapsed",
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name="studysession",
            name="target_minutes",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
