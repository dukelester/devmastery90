"""DRF API views for DevMastery."""
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from training.models import Assessment, CodingProblem, Skill, StudySession, Task
from training.serializers import (
    AssessmentSerializer,
    CodingProblemSerializer,
    SkillSerializer,
    StudySessionSerializer,
    TaskSerializer,
)
from training.services import (
    calculate_progress,
    calculate_streak,
    get_analytics_data,
    get_daily_recommendations,
    get_skill_scores,
)


class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["category"]
    search_fields = ["name"]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("skill", "training_day").all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["completed", "task_type", "priority", "training_day"]
    search_fields = ["title"]

    def get_queryset(self):
        return Task.objects.select_related("skill", "training_day").all()


class StudySessionViewSet(viewsets.ModelViewSet):
    serializer_class = StudySessionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["is_active", "skill"]

    def get_queryset(self):
        return StudySession.objects.filter(user=self.request.user).select_related("skill", "task")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AssessmentViewSet(viewsets.ModelViewSet):
    serializer_class = AssessmentSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["category", "skill"]

    def get_queryset(self):
        return Assessment.objects.filter(user=self.request.user).select_related("skill")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CodingProblemViewSet(viewsets.ModelViewSet):
    serializer_class = CodingProblemSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["solved", "difficulty", "category"]
    search_fields = ["title", "category"]

    def get_queryset(self):
        return CodingProblem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def progress_view(request):
    return Response(calculate_progress(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analytics_view(request):
    return Response(get_analytics_data(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommendations_view(request):
    return Response(get_daily_recommendations(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def streak_view(request):
    return Response(calculate_streak(request.user))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def skill_health_view(request):
    return Response(get_skill_scores(request.user))
