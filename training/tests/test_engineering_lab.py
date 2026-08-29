"""Tests for interactive engineering lab workspaces."""
import pytest

from training.models import EngineeringChallenge, EngineeringLabSession


@pytest.fixture
def engineering_challenge(db):
    return EngineeringChallenge.objects.create(
        challenge_type="lab",
        title="Test lab",
        description="A test lab",
        starter_code="# starter",
        lab_steps=["Step one", "Step two"],
        hints="First hint\nSecond hint",
        success_criteria="All steps done",
    )


@pytest.mark.django_db
def test_lab_session_progress(user, engineering_challenge):
    session = EngineeringLabSession.objects.create(
        user=user,
        challenge=engineering_challenge,
        code_workspace=engineering_challenge.starter_code,
    )
    assert session.step_progress_pct == 0.0

    session.completed_steps = [0]
    session.save()
    assert session.step_progress_pct == 50.0

    session.code_workspace = "updated code"
    session.save()
    assert session.code_workspace == "updated code"
