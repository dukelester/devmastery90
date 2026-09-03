"""Tests for coaching email digests."""
import pytest
from django.core import mail

from training.email_digest import build_email_digest, send_training_digest
from training.services import get_or_create_profile


@pytest.mark.django_db
def test_build_email_digest(user, profile):
    profile.program_start_date = profile.program_start_date or __import__("datetime").date.today()
    profile.save()
    user.email = "coach@example.com"
    user.save()
    ctx = build_email_digest(user)
    assert ctx["progress"]["current_day"] >= 1
    assert "urls" in ctx
    assert ctx["urls"]["today"].startswith("http")


@pytest.mark.django_db
def test_send_training_digest_force(user, profile, settings):
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    user.email = "coach@example.com"
    user.save()
    profile.email_reminders_enabled = True
    profile.save()
    assert send_training_digest(user, force=True) is True
    assert len(mail.outbox) == 1
    assert "DevMastery" in mail.outbox[0].subject
    profile.refresh_from_db()
    assert profile.last_reminder_sent_at is not None


@pytest.mark.django_db
def test_profile_timezone_defaults_to_nairobi(user):
    from training.services import get_or_create_profile
    from training.timezones import DEFAULT_TIMEZONE, normalize_timezone

    profile = get_or_create_profile(user)
    assert profile.timezone == DEFAULT_TIMEZONE
    assert profile.timezone_auto is True
    assert normalize_timezone("") == "Africa/Nairobi"
    assert normalize_timezone("Not/AZone") == "Africa/Nairobi"


@pytest.mark.django_db
def test_profile_timezone_sync_endpoint(client, user, profile):
    from django.urls import reverse

    client.force_login(user)
    profile.timezone_auto = True
    profile.timezone = "Africa/Nairobi"
    profile.save(update_fields=["timezone", "timezone_auto"])

    response = client.post(
        reverse("profile_timezone_sync"),
        {"timezone": "Europe/London"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True
    assert data["timezone"] == "Europe/London"
    profile.refresh_from_db()
    assert profile.timezone == "Europe/London"
    assert profile.timezone_auto is True

    # Manual lock skips auto sync
    profile.timezone_auto = False
    profile.timezone = "UTC"
    profile.save(update_fields=["timezone", "timezone_auto"])
    response = client.post(
        reverse("profile_timezone_sync"),
        {"timezone": "Asia/Tokyo"},
    )
    assert response.json()["skipped"] is True
    profile.refresh_from_db()
    assert profile.timezone == "UTC"
