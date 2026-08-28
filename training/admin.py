"""Admin configuration for training models."""
from django.contrib import admin

from training.models import (
    Assessment,
    AssessmentAttempt,
    CodingProblem,
    DailyReview,
    InterviewAttempt,
    InterviewQuestion,
    Mistake,
    Phase,
    Project,
    Skill,
    StudySession,
    Task,
    TrainingDay,
    UserProfile,
    Week,
    WeeklyReview,
)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "current_score", "target_score"]
    search_fields = ["name"]
    list_filter = ["category"]


@admin.register(Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    ordering = ["order"]


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ["week_number", "title", "phase", "start_date", "end_date"]
    list_filter = ["phase"]
    ordering = ["week_number"]


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ["title", "task_type", "estimated_minutes", "priority", "completed", "order"]


@admin.register(TrainingDay)
class TrainingDayAdmin(admin.ModelAdmin):
    list_display = ["day_number", "title", "focus", "completed", "completion_percentage"]
    list_filter = ["completed", "week"]
    inlines = [TaskInline]
    ordering = ["day_number"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "task_type", "training_day", "completed", "priority"]
    list_filter = ["task_type", "completed", "priority"]
    search_fields = ["title"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "xp", "level", "current_streak", "total_study_minutes"]


@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ["user", "duration_minutes", "started_at", "is_active"]
    list_filter = ["is_active"]


@admin.register(CodingProblem)
class CodingProblemAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "difficulty", "solved", "category"]
    list_filter = ["solved", "difficulty"]


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ["name", "user", "percentage", "completed_at"]
    list_filter = ["category"]


@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ["assessment", "score", "duration", "created_at"]


@admin.register(Mistake)
class MistakeAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "severity", "resolved"]
    list_filter = ["category", "resolved", "severity"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "status", "start_date"]


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ["category", "question", "difficulty"]
    list_filter = ["category", "difficulty"]


@admin.register(InterviewAttempt)
class InterviewAttemptAdmin(admin.ModelAdmin):
    list_display = ["user", "question", "score", "confidence", "needs_review"]


@admin.register(DailyReview)
class DailyReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "training_day", "confidence_score", "created_at"]


@admin.register(WeeklyReview)
class WeeklyReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "week", "tasks_completed", "study_minutes"]
