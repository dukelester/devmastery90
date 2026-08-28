"""DRF API URL configuration."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from training.api_views import (
    AssessmentViewSet,
    analytics_view,
    CodingProblemViewSet,
    progress_view,
    recommendations_view,
    SkillViewSet,
    streak_view,
    skill_health_view,
    StudySessionViewSet,
    TaskViewSet,
)

router = DefaultRouter()
router.register("skills", SkillViewSet)
router.register("tasks", TaskViewSet)
router.register("study-sessions", StudySessionViewSet, basename="studysession")
router.register("assessments", AssessmentViewSet, basename="assessment")
router.register("coding-problems", CodingProblemViewSet, basename="codingproblem")

urlpatterns = [
    path("", include(router.urls)),
    path("progress/", progress_view, name="api-progress"),
    path("analytics/", analytics_view, name="api-analytics"),
    path("recommendations/", recommendations_view, name="api-recommendations"),
    path("streak/", streak_view, name="api-streak"),
    path("skill-health/", skill_health_view, name="api-skill-health"),
]
