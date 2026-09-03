"""Tests for auth, password reset, and profile."""
from unittest.mock import patch

import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from training.models import UserProfile


@pytest.mark.django_db
def test_register_creates_user_with_email(client):
    response = client.post(
        reverse("register"),
        {
            "username": "newtrainee",
            "first_name": "New",
            "last_name": "Trainee",
            "email": "new@example.com",
            "password1": "complex-enough-pass",
            "password2": "complex-enough-pass",
        },
    )
    assert response.status_code == 302
    user = User.objects.get(username="newtrainee")
    assert user.email == "new@example.com"
    assert user.first_name == "New"
    assert UserProfile.objects.filter(user=user).exists()


@pytest.mark.django_db
def test_password_reset_submits(client):
    User.objects.create_user(
        username="resetme",
        email="reset@example.com",
        password="old-password-123",
    )
    with patch("django.contrib.auth.forms.PasswordResetForm.send_mail") as mock_send:
        response = client.post(reverse("password_reset"), {"email": "reset@example.com"})
    assert response.status_code == 302
    mock_send.assert_called_once()


@pytest.mark.django_db
def test_password_reset_pages_load(client):
    assert client.get(reverse("password_reset")).status_code == 200
    assert client.get(reverse("password_reset_done")).status_code == 200
    assert client.get(reverse("password_reset_complete")).status_code == 200


@pytest.mark.django_db
def test_profile_update(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="profileuser",
        email="profile@example.com",
        password="test-pass-123",
    )
    UserProfile.objects.create(user=user, program_start_date="2026-01-01")
    client.force_login(user)

    response = client.post(
        reverse("profile"),
        {
            "action": "profile",
            "first_name": "Pro",
            "last_name": "File",
            "username": "profileuser",
            "email": "profile@example.com",
            "display_name": "Pro Engineer",
            "bio": "Building depth daily.",
            "location": "Remote",
            "timezone": "Africa/Nairobi",
            "company": "DevMastery",
            "target_role": "Staff Engineer",
            "years_experience": 5,
            "github_url": "https://github.com/profileuser",
            "linkedin_url": "",
            "portfolio_url": "",
        },
    )
    assert response.status_code == 302

    profile = UserProfile.objects.get(user=user)
    user.refresh_from_db()
    assert user.first_name == "Pro"
    assert profile.display_name == "Pro Engineer"
    assert profile.target_role == "Staff Engineer"
    assert profile.github_url == "https://github.com/profileuser"


@pytest.mark.django_db
def test_profile_requires_login(client):
    response = client.get(reverse("profile"))
    assert response.status_code == 302
    assert "/login/" in response.url
