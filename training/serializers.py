"""DRF serializers for DevMastery API."""
from rest_framework import serializers

from training.models import (
    Assessment,
    CodingProblem,
    Skill,
    StudySession,
    Task,
    TrainingDay,
)


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = [
            "id", "name", "slug", "description", "category",
            "target_score", "current_score", "weight",
        ]


class TaskSerializer(serializers.ModelSerializer):
    skill_name = serializers.CharField(source="skill.name", read_only=True, default="")

    class Meta:
        model = Task
        fields = [
            "id", "training_day", "skill", "skill_name", "title", "description",
            "task_type", "estimated_minutes", "priority", "completed",
            "completed_at", "difficulty", "order", "blocked", "skipped", "notes",
        ]
        read_only_fields = ["completed_at"]


class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = [
            "id", "skill", "task", "started_at", "ended_at",
            "duration_minutes", "notes", "is_active",
        ]
        read_only_fields = ["started_at"]


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "id", "name", "category", "score", "maximum_score",
            "percentage", "duration_minutes", "completed_at", "notes", "skill",
        ]


class CodingProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodingProblem
        fields = [
            "id", "title", "platform", "url", "difficulty", "category",
            "solved", "attempts", "time_taken", "confidence", "notes", "solved_at",
        ]


class TrainingDaySerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = TrainingDay
        fields = [
            "id", "day_number", "title", "focus", "objectives",
            "target_minutes", "completed", "completion_percentage", "tasks",
        ]
