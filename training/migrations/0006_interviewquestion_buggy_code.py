from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0005_studysession_focus_mode"),
    ]

    operations = [
        migrations.AddField(
            model_name="interviewquestion",
            name="buggy_code",
            field=models.TextField(
                blank=True,
                help_text="Broken code snippet for debugging exercises",
            ),
        ),
    ]
