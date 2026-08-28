"""Tests for DevMastery 90 training platform."""
import pytest
from datetime import date, timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone

from training.models import (
    Assessment,
    CodingProblem,
    Mistake,
    Skill,
    StudySession,
    Task,
    TrainingDay,
    UserProfile,
    Week,
)
from training.services import (
    award_xp,
    calculate_progress,
    calculate_skill_health,
    calculate_streak,
    get_daily_recommendations,
    get_or_create_profile,
    get_top_weaknesses,
    update_streak_on_activity,
    update_training_day_completion,
)

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


@pytest.fixture
def skill(db):
    return Skill.objects.create(
        name="Python",
        slug="python",
        category="language",
        current_score=5.0,
        target_score=8.0,
    )


@pytest.fixture
def postgres_skill(db):
    return Skill.objects.create(
        name="PostgreSQL",
        slug="postgresql",
        category="database",
        current_score=5.0,
        target_score=8.0,
    )


@pytest.fixture
def training_day(db):
    from training.models import Phase
    phase = Phase.objects.create(name="Phase 1", order=1)
    week = Week.objects.create(phase=phase, week_number=1, title="Week 1")
    day = TrainingDay.objects.create(
        week=week, day_number=1, title="Day 1", focus="Python", target_minutes=180
    )
    return day


@pytest.fixture
def task(training_day, skill):
    return Task.objects.create(
        training_day=training_day,
        skill=skill,
        title="Study Python",
        task_type="study",
        estimated_minutes=45,
        order=1,
    )


@pytest.mark.django_db
class TestProgress:
    def test_calculate_progress(self, user, profile, task):
        progress = calculate_progress(user)
        assert progress["current_day"] == 1
        assert progress["total_days"] == 90
        assert progress["days_remaining"] == 89
        assert progress["streak"] == 0

    def test_progress_with_completed_tasks(self, user, profile, task):
        task.completed = True
        task.save()
        progress = calculate_progress(user)
        assert progress["completed_tasks"] == 1

    def test_day_number_caps_at_90(self, user, profile):
        profile.program_start_date = date.today() - timedelta(days=100)
        profile.save()
        progress = calculate_progress(user)
        assert progress["current_day"] == 90


@pytest.mark.django_db
class TestStreak:
    def test_calculate_streak_no_sessions(self, user, profile):
        result = calculate_streak(user)
        assert result["current_streak"] == 0

    def test_streak_with_today_session(self, user, profile):
        now = timezone.now()
        StudySession.objects.create(
            user=user,
            started_at=now - timedelta(hours=1),
            ended_at=now,
            duration_minutes=60,
            is_active=False,
        )
        update_streak_on_activity(user)
        profile.refresh_from_db()
        assert profile.current_streak == 1

    def test_streak_consecutive_days(self, user, profile):
        for i in range(3):
            day = date.today() - timedelta(days=i)
            StudySession.objects.create(
                user=user,
                started_at=timezone.make_aware(
                    timezone.datetime(day.year, day.month, day.day, 10, 0)
                ),
                ended_at=timezone.make_aware(
                    timezone.datetime(day.year, day.month, day.day, 11, 0)
                ),
                duration_minutes=60,
                is_active=False,
            )
        result = calculate_streak(user)
        assert result["current_streak"] == 3


@pytest.mark.django_db
class TestSkillHealth:
    def test_calculate_skill_health_default(self, user, skill):
        health = calculate_skill_health(user, skill)
        assert 0 <= health["score"] <= 10
        assert health["trend"] in ("↑", "↓", "→")
        assert health["weakness_level"] in ("LOW", "MEDIUM", "HIGH")

    def test_skill_health_with_assessments(self, user, skill):
        Assessment.objects.create(
            user=user, skill=skill, name="Python Test", category="python",
            score=80, maximum_score=100, percentage=80,
            duration_minutes=60, completed_at=timezone.now(),
        )
        Assessment.objects.create(
            user=user, skill=skill, name="Python Test 2", category="python",
            score=90, maximum_score=100, percentage=90,
            duration_minutes=60, completed_at=timezone.now(),
        )
        health = calculate_skill_health(user, skill)
        assert health["score"] > 5.0
        assert health["trend"] == "↑"

    def test_skill_health_with_mistakes(self, user, skill):
        Mistake.objects.create(
            user=user, skill=skill, description="Forgot decorator syntax",
            category="knowledge_gap", severity="high",
        )
        health = calculate_skill_health(user, skill)
        assert health["weakness_level"] in ("MEDIUM", "HIGH")

    def test_top_weaknesses(self, user, skill, postgres_skill):
        Mistake.objects.create(
            user=user, skill=postgres_skill, description="Slow query",
            category="database", severity="high",
        )
        weaknesses = get_top_weaknesses(user, limit=3)
        assert len(weaknesses) >= 1
        assert weaknesses[0]["score"] <= weaknesses[-1]["score"] if len(weaknesses) > 1 else True


@pytest.mark.django_db
class TestRecommendations:
    def test_get_daily_recommendations(self, user, profile, task, training_day):
        recs = get_daily_recommendations(user)
        assert isinstance(recs, list)
        assert len(recs) > 0

    def test_recommendations_include_scheduled_tasks(self, user, profile, task, training_day):
        recs = get_daily_recommendations(user)
        scheduled = [r for r in recs if r["type"] == "scheduled"]
        assert len(scheduled) >= 1

    def test_recommendations_overdue_tasks(self, user, profile, skill):
        from training.models import Phase
        phase = Phase.objects.create(name="Phase 1", order=1)
        week = Week.objects.create(phase=phase, week_number=1, title="Week 1")
        old_day = TrainingDay.objects.create(
            week=week, day_number=1, title="Old Day", focus="Python", target_minutes=60
        )
        Task.objects.create(
            training_day=old_day, skill=skill, title="Overdue task",
            task_type="study", estimated_minutes=30, order=1,
        )
        profile.program_start_date = date.today() - timedelta(days=5)
        profile.save()
        recs = get_daily_recommendations(user)
        overdue = [r for r in recs if r["type"] == "overdue"]
        assert len(overdue) >= 1


@pytest.mark.django_db
class TestGamification:
    def test_award_xp(self, user, profile):
        award_xp(user, 500)
        profile.refresh_from_db()
        assert profile.xp == 500
        assert profile.level >= 1

    def test_level_up(self, user, profile):
        award_xp(user, 1500)
        profile.refresh_from_db()
        assert profile.level >= 2


@pytest.mark.django_db
class TestTaskCompletion:
    def test_update_training_day_completion(self, training_day, skill):
        Task.objects.create(
            training_day=training_day, skill=skill, title="Task 1",
            task_type="study", estimated_minutes=30, order=1, completed=True,
        )
        Task.objects.create(
            training_day=training_day, skill=skill, title="Task 2",
            task_type="study", estimated_minutes=30, order=2,
        )
        update_training_day_completion(training_day)
        training_day.refresh_from_db()
        assert training_day.completion_percentage == 50.0
        assert not training_day.completed

    def test_full_day_completion(self, training_day, skill):
        Task.objects.create(
            training_day=training_day, skill=skill, title="Task 1",
            task_type="study", estimated_minutes=30, order=1, completed=True,
        )
        update_training_day_completion(training_day)
        training_day.refresh_from_db()
        assert training_day.completed


@pytest.mark.django_db
class TestModels:
    def test_skill_slug_auto_generated(self, db):
        skill = Skill.objects.create(name="Test Skill", category="language")
        assert skill.slug == "test-skill"

    def test_user_profile_creation(self, user):
        profile = get_or_create_profile(user)
        assert profile.user == user
        assert profile.xp == 0


@pytest.mark.django_db
class TestAPI:
    def test_progress_api(self, client, user, profile):
        client.force_login(user)
        response = client.get("/api/progress/")
        assert response.status_code == 200
        data = response.json()
        assert "current_day" in data

    def test_skills_api(self, client, user, skill):
        client.force_login(user)
        response = client.get("/api/skills/")
        assert response.status_code == 200

    def test_recommendations_api(self, client, user, profile, task, training_day):
        client.force_login(user)
        response = client.get("/api/recommendations/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_unauthenticated_api(self, client):
        response = client.get("/api/progress/")
        assert response.status_code in (401, 403)


@pytest.mark.django_db
class TestHTMXViews:
    @property
    def htmx_headers(self):
        return {"HTTP_HX_REQUEST": "true"}

    def test_task_complete(self, client, user, task):
        client.force_login(user)
        response = client.post(f"/tasks/{task.id}/complete/", **self.htmx_headers)
        assert response.status_code == 200
        task.refresh_from_db()
        assert task.completed

    def test_timer_start_stop(self, client, user, profile):
        client.force_login(user)
        start = client.post("/timer/start/", **self.htmx_headers)
        assert start.status_code == 200
        assert StudySession.objects.filter(user=user, is_active=True).exists()
        stop = client.post("/timer/stop/", **self.htmx_headers)
        assert stop.status_code == 200
        assert not StudySession.objects.filter(user=user, is_active=True).exists()

    def test_coding_create_and_solve(self, client, user):
        client.force_login(user)
        create = client.post("/coding/create/", {
            "title": "Two Sum", "category": "Arrays", "difficulty": "easy",
        }, **self.htmx_headers)
        assert create.status_code == 200
        problem = CodingProblem.objects.get(user=user, title="Two Sum")
        solve = client.post(f"/coding/{problem.id}/solve/", {
            "time_taken": 15, "confidence": 8,
        }, **self.htmx_headers)
        assert solve.status_code == 200
        problem.refresh_from_db()
        assert problem.solved
