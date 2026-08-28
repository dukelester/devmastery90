"""Data models for DevMastery 90 training platform."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class SkillCategory(models.TextChoices):
    LANGUAGE = "language", "Language"
    ALGORITHMS = "algorithms", "Algorithms"
    BACKEND = "backend", "Backend"
    DATABASE = "database", "Database"
    INFRASTRUCTURE = "infrastructure", "Infrastructure"
    ARCHITECTURE = "architecture", "Architecture"
    TESTING = "testing", "Testing"
    CLOUD = "cloud", "Cloud"
    AI = "ai", "AI"
    SOFT_SKILLS = "soft_skills", "Soft Skills"


class TaskType(models.TextChoices):
    STUDY = "study", "Study"
    CODING = "coding", "Coding"
    PROJECT = "project", "Project"
    ASSESSMENT = "assessment", "Assessment"
    READING = "reading", "Reading"
    INTERVIEW = "interview", "Interview"
    REVIEW = "review", "Review"
    DEBUGGING = "debugging", "Debugging"
    SYSTEM_DESIGN = "system_design", "System Design"


class MistakeCategory(models.TextChoices):
    KNOWLEDGE_GAP = "knowledge_gap", "Knowledge Gap"
    CARELESS_ERROR = "careless_error", "Careless Error"
    ALGORITHMIC_ERROR = "algorithmic_error", "Algorithmic Error"
    SYNTAX_ERROR = "syntax_error", "Syntax Error"
    DEBUGGING_ERROR = "debugging_error", "Debugging Error"
    TIME_MANAGEMENT = "time_management", "Time Management"
    COMMUNICATION = "communication", "Communication"
    ARCHITECTURE = "architecture", "Architecture"
    DATABASE = "database", "Database"
    TESTING = "testing", "Testing"


class Difficulty(models.TextChoices):
    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD = "hard", "Hard"
    EXPERT = "expert", "Expert"


class Priority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"


class ProjectStatus(models.TextChoices):
    PLANNED = "planned", "Planned"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"
    PAUSED = "paused", "Paused"


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=SkillCategory.choices)
    target_score = models.FloatField(
        default=8.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    current_score = models.FloatField(
        default=5.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    weight = models.FloatField(default=1.0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["category"])]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Phase(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return self.name


class Week(models.Model):
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE, related_name="weeks")
    week_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=200)
    objectives = models.TextField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["week_number"]
        unique_together = ["phase", "week_number"]
        indexes = [models.Index(fields=["week_number"])]

    def __str__(self) -> str:
        return f"Week {self.week_number}: {self.title}"


class TrainingDay(models.Model):
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="days")
    day_number = models.PositiveSmallIntegerField()
    date = models.DateField(null=True, blank=True)
    title = models.CharField(max_length=200)
    focus = models.CharField(max_length=200, blank=True)
    objectives = models.TextField(blank=True)
    target_minutes = models.PositiveIntegerField(default=180)
    completed = models.BooleanField(default=False)
    completion_percentage = models.FloatField(
        default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:
        ordering = ["day_number"]
        unique_together = ["week", "day_number"]
        indexes = [
            models.Index(fields=["day_number"]),
            models.Index(fields=["date"]),
            models.Index(fields=["completed"]),
        ]

    def __str__(self) -> str:
        return f"Day {self.day_number}: {self.title}"


class Task(models.Model):
    training_day = models.ForeignKey(
        TrainingDay, on_delete=models.CASCADE, related_name="tasks"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks"
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    task_type = models.CharField(max_length=20, choices=TaskType.choices)
    estimated_minutes = models.PositiveIntegerField(default=30)
    priority = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM
    )
    order = models.PositiveSmallIntegerField(default=0)
    blocked = models.BooleanField(default=False)
    blocked_reason = models.TextField(blank=True)
    skipped = models.BooleanField(default=False)
    skip_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "id"]
        indexes = [
            models.Index(fields=["completed"]),
            models.Index(fields=["task_type"]),
            models.Index(fields=["training_day", "completed"]),
        ]

    def __str__(self) -> str:
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)
    current_streak = models.PositiveSmallIntegerField(default=0)
    longest_streak = models.PositiveSmallIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    program_start_date = models.DateField(null=True, blank=True)
    total_study_minutes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user"])]

    def __str__(self) -> str:
        return f"Profile: {self.user.username}"

    @property
    def level_title(self) -> str:
        titles = {
            1: "Beginner",
            2: "Intermediate",
            3: "Proficient",
            4: "Advanced",
            5: "Expert",
            6: "Master",
        }
        return titles.get(self.level, "Elite")


class StudySession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="study_sessions"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions"
    )
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, blank=True, related_name="sessions"
    )
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "started_at"]),
            models.Index(fields=["user", "is_active"]),
        ]

    def __str__(self) -> str:
        return f"Session {self.user.username} - {self.duration_minutes}m"


class CodingProblem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="coding_problems"
    )
    title = models.CharField(max_length=300)
    platform = models.CharField(max_length=100, blank=True)
    url = models.URLField(blank=True)
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM
    )
    category = models.CharField(max_length=100, blank=True)
    solved = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)
    time_taken = models.PositiveIntegerField(
        null=True, blank=True, help_text="Time in minutes"
    )
    confidence = models.FloatField(
        default=5.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    notes = models.TextField(blank=True)
    solved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "solved"]),
            models.Index(fields=["user", "category"]),
            models.Index(fields=["difficulty"]),
        ]

    def __str__(self) -> str:
        return self.title


class Assessment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assessments"
    )
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    score = models.FloatField(validators=[MinValueValidator(0)])
    maximum_score = models.FloatField(default=100)
    percentage = models.FloatField(
        default=0.0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    duration_minutes = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="assessments"
    )

    class Meta:
        ordering = ["-completed_at"]
        indexes = [
            models.Index(fields=["user", "completed_at"]),
            models.Index(fields=["user", "category"]),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.percentage}%"


class AssessmentAttempt(models.Model):
    assessment = models.ForeignKey(
        Assessment, on_delete=models.CASCADE, related_name="attempts"
    )
    score = models.FloatField(validators=[MinValueValidator(0)])
    duration = models.PositiveIntegerField(default=0, help_text="Duration in minutes")
    mistakes = models.TextField(blank=True)
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"Attempt for {self.assessment.name}"


class Mistake(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="mistakes"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="mistakes"
    )
    assessment = models.ForeignKey(
        Assessment, on_delete=models.SET_NULL, null=True, blank=True, related_name="mistakes"
    )
    coding_problem = models.ForeignKey(
        CodingProblem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mistakes",
    )
    description = models.TextField()
    category = models.CharField(max_length=30, choices=MistakeCategory.choices)
    severity = models.CharField(
        max_length=10, choices=Priority.choices, default=Priority.MEDIUM
    )
    resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "resolved"]),
            models.Index(fields=["user", "category"]),
        ]

    def __str__(self) -> str:
        return f"Mistake: {self.description[:50]}"


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.PLANNED
    )
    repository_url = models.URLField(blank=True)
    deployed_url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self) -> str:
        return self.name


class InterviewQuestion(models.Model):
    category = models.CharField(max_length=100)
    question = models.TextField()
    ideal_topics = models.TextField(blank=True, help_text="Topics to cover in answer")
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM
    )

    class Meta:
        ordering = ["category", "difficulty"]
        indexes = [models.Index(fields=["category"])]

    def __str__(self) -> str:
        return f"{self.category}: {self.question[:60]}"


class InterviewAttempt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="interview_attempts"
    )
    question = models.ForeignKey(
        InterviewQuestion, on_delete=models.CASCADE, related_name="attempts"
    )
    answer = models.TextField(blank=True)
    confidence = models.FloatField(
        default=5.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    score = models.FloatField(
        default=0.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    notes = models.TextField(blank=True)
    needs_review = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "needs_review"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"Interview attempt by {self.user.username}"


class DailyReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="daily_reviews"
    )
    training_day = models.ForeignKey(
        TrainingDay, on_delete=models.CASCADE, related_name="reviews"
    )
    wins = models.TextField(blank=True)
    challenges = models.TextField(blank=True)
    lessons = models.TextField(blank=True)
    tomorrow_focus = models.TextField(blank=True)
    confidence_score = models.FloatField(
        default=5.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "training_day"]
        indexes = [models.Index(fields=["user", "created_at"])]

    def __str__(self) -> str:
        return f"Review Day {self.training_day.day_number} by {self.user.username}"


class WeeklyReview(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="weekly_reviews"
    )
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name="reviews")
    tasks_completed = models.PositiveIntegerField(default=0)
    tasks_total = models.PositiveIntegerField(default=0)
    study_minutes = models.PositiveIntegerField(default=0)
    assessment_percentage = models.FloatField(default=0.0)
    strongest_skill = models.CharField(max_length=100, blank=True)
    weakest_skill = models.CharField(max_length=100, blank=True)
    repeated_mistake = models.TextField(blank=True)
    learned = models.TextField(blank=True)
    difficult = models.TextField(blank=True)
    went_well = models.TextField(blank=True)
    improve = models.TextField(blank=True)
    next_week_focus = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "week"]

    def __str__(self) -> str:
        return f"Week {self.week.week_number} review by {self.user.username}"
