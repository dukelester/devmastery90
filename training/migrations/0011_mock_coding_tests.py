from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0010_cognitiveprogress_time_spent"),
    ]

    operations = [
        migrations.AddField(
            model_name="mockinterviewquestion",
            name="function_name",
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AddField(
            model_name="mockinterviewquestion",
            name="starter_code",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="mockinterviewquestion",
            name="test_cases",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="mockinterviewresponse",
            name="auto_scored",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="mockinterviewresponse",
            name="tests_passed",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="mockinterviewresponse",
            name="tests_total",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
