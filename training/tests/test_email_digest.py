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
