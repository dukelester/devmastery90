"""Admin configuration for training models."""
from django.contrib import admin

from training.models import (
    Assessment,
    AssessmentAttempt,
    CodingProblem,
    DailyReview,
    InterviewAttempt,
    InterviewQuestion,
    LearningResource,
    Mistake,
    Phase,
    PracticeProgress,
    Project,
    ProjectProgress,
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


@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ["title", "resource_type", "skill", "day_number", "is_primary", "order"]
    list_filter = ["resource_type", "is_primary", "skill"]
    search_fields = ["title", "url", "description"]
    autocomplete_fields = ["skill"]


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
    list_display = [
        "user",
        "xp",
        "level",
        "current_streak",
        "email_reminders_enabled",
        "email_digest_frequency",
        "total_study_minutes",
    ]
    list_filter = ["email_reminders_enabled", "email_digest_frequency"]
    search_fields = ["user__username", "user__email", "display_name"]
    readonly_fields = ["last_reminder_sent_at"]


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
    list_display = ["name", "is_catalog", "difficulty", "status", "order", "is_featured"]
    list_filter = ["is_catalog", "difficulty", "status", "is_featured"]
    search_fields = ["name", "slug", "tagline"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(ProjectProgress)
class ProjectProgressAdmin(admin.ModelAdmin):
    list_display = ["user", "project", "status", "updated_at"]
    list_filter = ["status"]


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ["section_slug", "order", "category", "level", "difficulty"]
    list_filter = ["section_slug", "level", "difficulty"]
    search_fields = ["question"]
    ordering = ["section_slug", "order"]


@admin.register(PracticeProgress)
class PracticeProgressAdmin(admin.ModelAdmin):
    list_display = ["user", "section_slug", "unlocked_through_order", "completed_count"]
    list_filter = ["section_slug"]


@admin.register(InterviewAttempt)
class InterviewAttemptAdmin(admin.ModelAdmin):
    list_display = ["user", "question", "score", "confidence", "passed", "needs_review"]


@admin.register(DailyReview)
class DailyReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "training_day", "confidence_score", "created_at"]


@admin.register(WeeklyReview)
class WeeklyReviewAdmin(admin.ModelAdmin):
    list_display = ["user", "week", "tasks_completed", "study_minutes"]
