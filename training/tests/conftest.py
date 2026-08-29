"""Shared pytest fixtures for training tests."""
import pytest
from datetime import date

from django.contrib.auth import get_user_model

from training.models import UserProfile

User = get_user_model()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def profile(user):
    return UserProfile.objects.create(
        user=user,
        program_start_date=date.today(),
        xp=0,
        level=1,
        current_streak=0,
    )
