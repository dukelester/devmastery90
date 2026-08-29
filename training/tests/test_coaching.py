"""Tests for coaching briefing."""
import pytest

from training.services import get_coaching_briefing, needs_onboarding


@pytest.mark.django_db
class TestCoachingBriefing:
    def test_briefing_has_seven_sections(self, user, profile):
        briefing = get_coaching_briefing(user)
        assert "what_today" in briefing
        assert "why" in briefing
        assert "performance" in briefing
        assert "weaknesses" in briefing
        assert "repeated_mistakes" in briefing
        assert "improving" in briefing
        assert "next_actions" in briefing

    def test_needs_onboarding_without_start_date(self, user):
        assert needs_onboarding(user)

    def test_no_onboarding_with_start_date(self, user, profile):
        assert not needs_onboarding(user)
