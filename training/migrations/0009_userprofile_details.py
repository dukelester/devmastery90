from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0008_cognitive_questions"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="bio",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="company",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="display_name",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="github_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="linkedin_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="location",
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="portfolio_url",
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="target_role",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="timezone",
            field=models.CharField(blank=True, default="UTC", max_length=80),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="years_experience",
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
