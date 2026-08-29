from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0009_userprofile_details"),
    ]

    operations = [
        migrations.AddField(
            model_name="cognitiveprogress",
            name="time_spent_seconds",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
