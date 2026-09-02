"""Data models for DevMastery 90 training platform."""
import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


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


class ProficiencyLevel(models.TextChoices):
    BEGINNER = "beginner", "Beginner"
    EASY = "easy", "Easy"
    MEDIUM = "medium", "Medium"
    HARD = "hard", "Hard"
    EXPERT = "expert", "Expert"
    ELITE = "elite", "Elite"


PROFICIENCY_ORDER = [
    ProficiencyLevel.BEGINNER,
    ProficiencyLevel.EASY,
    ProficiencyLevel.MEDIUM,
    ProficiencyLevel.HARD,
    ProficiencyLevel.EXPERT,
    ProficiencyLevel.ELITE,
]


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


class Skill(UUIDModel):
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


class ResourceType(models.TextChoices):
    ARTICLE = "article", "Article"
    DOCS = "docs", "Official docs"
    COURSE = "course", "Course"
    VIDEO = "video", "Video"
    BOOK = "book", "Book"
    TOOL = "tool", "Tool"


class LearningResource(UUIDModel):
    """Curated external resources tied to skills and/or curriculum days."""

    title = models.CharField(max_length=240)
    url = models.URLField()
    resource_type = models.CharField(
        max_length=20, choices=ResourceType.choices, default=ResourceType.ARTICLE
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resources",
    )
    day_number = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Optional curriculum day this resource supports.",
    )
    week_number = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_primary = models.BooleanField(
        default=False,
        help_text="Highlight as the first recommended read for the skill/day.",
    )
    order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "title"]
        indexes = [
            models.Index(fields=["day_number"]),
            models.Index(fields=["skill", "order"]),
            models.Index(fields=["resource_type"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["url", "day_number", "skill"],
                name="uniq_resource_url_day_skill",
            ),
        ]

    def __str__(self) -> str:
        return self.title


class Phase(UUIDModel):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return self.name


class Week(UUIDModel):
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


class TrainingDay(UUIDModel):
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


class Task(UUIDModel):
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


class UserProfile(UUIDModel):
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
    display_name = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    timezone = models.CharField(max_length=80, blank=True, default="UTC")
    company = models.CharField(max_length=200, blank=True)
    target_role = models.CharField(max_length=200, blank=True)
    years_experience = models.PositiveSmallIntegerField(null=True, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["user"])]

    def __str__(self) -> str:
        return f"Profile: {self.user.username}"

    XP_PER_LEVEL = 1000

    @property
    def level_title(self) -> str:
        titles = {
            1: "Apprentice",
            2: "Operator",
            3: "Engineer",
            4: "Advanced",
            5: "Principal",
            6: "Architect",
        }
        return titles.get(min(self.level, 6), "Architect")

    @property
    def xp_into_level(self) -> int:
        return self.xp % self.XP_PER_LEVEL

    @property
    def xp_to_next_level(self) -> int:
        return self.XP_PER_LEVEL - self.xp_into_level

    @property
    def xp_progress_pct(self) -> float:
        return round((self.xp_into_level / self.XP_PER_LEVEL) * 100, 1)

    @property
    def next_level_title(self) -> str:
        titles = {
            1: "Apprentice",
            2: "Operator",
            3: "Engineer",
            4: "Advanced",
            5: "Principal",
            6: "Architect",
            7: "Architect",
        }
        return titles.get(min(self.level + 1, 7), "Architect")

    @property
    def level_display(self) -> str:
        return f"LEVEL {self.level} — {self.level_title.upper()}"

    @property
    def xp_display(self) -> str:
        return f"{self.xp:,}"

    @property
    def public_name(self) -> str:
        if self.display_name:
            return self.display_name
        full = self.user.get_full_name().strip()
        if full:
            return full
        return self.user.username


class StudySession(UUIDModel):
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
    mode = models.CharField(
        max_length=10,
        choices=[("elapsed", "Elapsed"), ("focus", "Focus")],
        default="elapsed",
    )
    target_minutes = models.PositiveIntegerField(null=True, blank=True)
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


class CodingProblem(UUIDModel):
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


class Assessment(UUIDModel):
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


class AssessmentAttempt(UUIDModel):
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


class Mistake(UUIDModel):
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


class Project(UUIDModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    tagline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    problem_statement = models.TextField(blank=True)
    overview = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.PLANNED
    )
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.HARD
    )
    estimated_hours = models.PositiveSmallIntegerField(default=40)
    week_focus = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="Suggested curriculum week"
    )
    tech_stack = models.JSONField(default=list, blank=True)
    learning_outcomes = models.JSONField(default=list, blank=True)
    features = models.JSONField(default=list, blank=True)
    functional_requirements = models.JSONField(default=list, blank=True)
    non_functional_requirements = models.JSONField(default=list, blank=True)
    acceptance_criteria = models.JSONField(
        default=list,
        blank=True,
        help_text='List of {"id": "ac-1", "text": "...", "required": true}',
    )
    milestones = models.JSONField(default=list, blank=True)
    deliverables = models.JSONField(default=list, blank=True)
    getting_started = models.TextField(blank=True)
    architecture_notes = models.TextField(blank=True)
    resources = models.JSONField(default=list, blank=True)
    repository_url = models.URLField(blank=True)
    deployed_url = models.URLField(blank=True)
    start_date = models.DateField(null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_catalog = models.BooleanField(
        default=False,
        help_text="Published in the Projects hub (curriculum / portfolio briefs)",
    )
    is_featured = models.BooleanField(default=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["order", "name"]
        indexes = [
            models.Index(fields=["is_catalog", "order"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify

            base = slugify(self.name)[:200] or "project"
            candidate = base
            n = 2
            while Project.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{n}"
                n += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    @property
    def required_criteria(self) -> list:
        return [c for c in (self.acceptance_criteria or []) if c.get("required", True)]

    @property
    def criteria_count(self) -> int:
        return len(self.acceptance_criteria or [])


class ProjectProgress(UUIDModel):
    """Tracks a learner's work against a catalog project brief."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="project_progress",
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="progress_rows"
    )
    status = models.CharField(
        max_length=20, choices=ProjectStatus.choices, default=ProjectStatus.PLANNED
    )
    checked_criteria = models.JSONField(default=list, blank=True)
    notes = models.TextField(blank=True)
    repository_url = models.URLField(blank=True)
    deployed_url = models.URLField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "project"]
        ordering = ["-updated_at"]
        indexes = [models.Index(fields=["user", "status"])]

    def __str__(self) -> str:
        return f"{self.user.username} — {self.project.name}"

    @property
    def checked_count(self) -> int:
        return len(self.checked_criteria or [])

    @property
    def pass_pct(self) -> float:
        total = self.project.criteria_count
        if not total:
            return 0.0
        return round((self.checked_count / total) * 100, 1)

    @property
    def is_passing(self) -> bool:
        required = self.project.required_criteria
        if not required:
            return self.status == ProjectStatus.COMPLETED
        checked = set(self.checked_criteria or [])
        return all(c.get("id") in checked for c in required)


class InterviewQuestion(UUIDModel):
    section_slug = models.SlugField(max_length=50, db_index=True, default="python")
    category = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1)
    level = models.CharField(
        max_length=10,
        choices=ProficiencyLevel.choices,
        default=ProficiencyLevel.BEGINNER,
    )
    question = models.TextField()
    buggy_code = models.TextField(
        blank=True,
        help_text="Broken code snippet for debugging exercises",
    )
    ideal_topics = models.TextField(blank=True, help_text="Topics to cover in answer")
    solution_code = models.TextField(blank=True, help_text="Reference solution with comments")
    solution_explanation = models.TextField(blank=True)
    hints = models.TextField(blank=True)
    learning_objectives = models.TextField(blank=True)
    time_estimate_minutes = models.PositiveSmallIntegerField(default=15)
    min_pass_score = models.FloatField(
        default=6.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM
    )

    class Meta:
        ordering = ["section_slug", "order"]
        indexes = [
            models.Index(fields=["section_slug"]),
            models.Index(fields=["section_slug", "order"]),
            models.Index(fields=["category"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["section_slug", "order"],
                name="unique_section_question_order",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.category} #{self.order}: {self.question[:60]}"

    @property
    def level_display(self) -> str:
        return self.get_level_display()

    @property
    def ideal_topics_list(self) -> list[str]:
        if not self.ideal_topics:
            return []
        return [part.strip() for part in self.ideal_topics.split(",") if part.strip()]


class PracticeProgress(UUIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="practice_progress",
    )
    section_slug = models.SlugField(max_length=50)
    unlocked_through_order = models.PositiveIntegerField(default=1)
    completed_count = models.PositiveIntegerField(default=0)
    last_activity_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["user", "section_slug"]
        indexes = [models.Index(fields=["user", "section_slug"])]

    def __str__(self) -> str:
        return f"{self.user.username} — {self.section_slug} (unlocked #{self.unlocked_through_order})"


class InterviewAttempt(UUIDModel):
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
    passed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "needs_review"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self) -> str:
        return f"Interview attempt by {self.user.username}"


class DailyReview(UUIDModel):
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


class WeeklyReview(UUIDModel):
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


class ApplicationStatus(models.TextChoices):
    WISHLIST = "wishlist", "Wishlist"
    APPLIED = "applied", "Applied"
    INTERVIEWING = "interviewing", "Interviewing"
    OFFER = "offer", "Offer"
    REJECTED = "rejected", "Rejected"


class EngineeringChallengeType(models.TextChoices):
    LAB = "lab", "Lab"
    BENCHMARK = "benchmark", "Benchmark"
    DEBUGGING = "debugging", "Debugging"
    SYSTEM_DESIGN = "system_design", "System Design"


class ReviewCard(UUIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="review_cards"
    )
    skill = models.ForeignKey(
        Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name="review_cards"
    )
    concept = models.CharField(max_length=200)
    content = models.TextField()
    next_review = models.DateField()
    interval_days = models.PositiveIntegerField(default=1)
    repetition = models.PositiveIntegerField(default=0)
    ease_factor = models.FloatField(default=2.5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["next_review"]
        indexes = [
            models.Index(fields=["user", "next_review"]),
        ]

    def __str__(self) -> str:
        return f"{self.concept} (review {self.next_review})"


class EngineeringChallenge(UUIDModel):
    challenge_type = models.CharField(max_length=20, choices=EngineeringChallengeType.choices)
    title = models.CharField(max_length=300)
    description = models.TextField()
    instructions = models.TextField(blank=True, help_text="Steps or code scaffold")
    starter_code = models.TextField(blank=True, help_text="Editable starter code for the lab workspace")
    lab_steps = models.JSONField(default=list, blank=True, help_text="Ordered checklist steps")
    hints = models.TextField(blank=True, help_text="One hint per line, revealed progressively")
    success_criteria = models.TextField(blank=True)
    solution_notes = models.TextField(blank=True)
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM
    )
    estimated_minutes = models.PositiveIntegerField(default=45)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["challenge_type", "order"]
        indexes = [models.Index(fields=["challenge_type"])]

    def __str__(self) -> str:
        return f"{self.get_challenge_type_display()}: {self.title}"


class EngineeringAttempt(UUIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="engineering_attempts",
    )
    challenge = models.ForeignKey(
        EngineeringChallenge, on_delete=models.CASCADE, related_name="attempts"
    )
    score = models.FloatField(
        default=0.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    time_minutes = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    code_submission = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "created_at"])]

    def __str__(self) -> str:
        return f"{self.challenge.title} by {self.user.username}"


class EngineeringLabSession(UUIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="engineering_lab_sessions",
    )
    challenge = models.ForeignKey(
        EngineeringChallenge, on_delete=models.CASCADE, related_name="lab_sessions"
    )
    code_workspace = models.TextField(blank=True)
    completed_steps = models.JSONField(default=list)
    hints_revealed = models.PositiveSmallIntegerField(default=0)
    timer_started_at = models.DateTimeField(null=True, blank=True)
    accumulated_minutes = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "challenge"]
        indexes = [models.Index(fields=["user", "challenge"])]

    def __str__(self) -> str:
        return f"Lab session: {self.challenge.title}"

    @property
    def step_progress_pct(self) -> float:
        total = len(self.challenge.lab_steps) or 1
        return round(len(self.completed_steps) / total * 100, 1)


class JobApplication(UUIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_applications",
    )
    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=ApplicationStatus.choices,
        default=ApplicationStatus.APPLIED,
    )
    applied_date = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-applied_date", "-created_at"]
        indexes = [models.Index(fields=["user", "status"])]

    def __str__(self) -> str:
        return f"{self.role} at {self.company}"


class CareerGoal(UUIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="career_goals",
    )
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=50, default="learning")
    target_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["completed", "target_date"]
        indexes = [models.Index(fields=["user", "completed"])]

    def __str__(self) -> str:
        return self.title


class MockInterviewRound(UUIDModel):
    round_number = models.PositiveSmallIntegerField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    unlock_day = models.PositiveIntegerField()
    period_end_day = models.PositiveIntegerField()
    duration_minutes = models.PositiveIntegerField(default=90)
    focus_areas = models.TextField(blank=True)

    class Meta:
        ordering = ["round_number"]

    def __str__(self) -> str:
        return f"Mock {self.round_number}: {self.title}"


class MockInterviewQuestion(UUIDModel):
    round = models.ForeignKey(
        MockInterviewRound, on_delete=models.CASCADE, related_name="questions"
    )
    order = models.PositiveSmallIntegerField()
    interview_type = models.CharField(
        max_length=20,
        choices=[
            ("behavioral", "Behavioral"),
            ("technical", "Technical"),
            ("coding", "Coding"),
            ("system_design", "System Design"),
        ],
    )
    difficulty = models.CharField(max_length=10, choices=Difficulty.choices)
    question = models.TextField()
    time_limit_minutes = models.PositiveSmallIntegerField(default=10)
    rubric = models.TextField(blank=True)
    sample_answer = models.TextField(blank=True)
    hints = models.TextField(blank=True)
    starter_code = models.TextField(blank=True)
    function_name = models.CharField(max_length=80, blank=True)
    test_cases = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ["round", "order"]
        unique_together = ["round", "order"]
        indexes = [models.Index(fields=["round", "order"])]

    def __str__(self) -> str:
        return f"Mock {self.round.round_number} Q{self.order}"

    @property
    def is_runnable(self) -> bool:
        return (
            self.interview_type == "coding"
            and bool(self.function_name)
            and bool(self.test_cases)
        )

    @property
    def public_test_cases(self) -> list:
        return [c for c in (self.test_cases or []) if not c.get("hidden")]


class MockInterviewSession(UUIDModel):
    class Status(models.TextChoices):
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mock_interview_sessions",
    )
    round = models.ForeignKey(
        MockInterviewRound, on_delete=models.CASCADE, related_name="sessions"
    )
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.IN_PROGRESS
    )
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    current_order = models.PositiveSmallIntegerField(default=1)
    question_started_at = models.DateTimeField(null=True, blank=True)
    total_score = models.FloatField(default=0.0)
    max_score = models.FloatField(default=0.0)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "round"]),
        ]

    def __str__(self) -> str:
        return f"Mock session {self.round.round_number} — {self.user.username}"


class MockInterviewResponse(UUIDModel):
    session = models.ForeignKey(
        MockInterviewSession, on_delete=models.CASCADE, related_name="responses"
    )
    question = models.ForeignKey(
        MockInterviewQuestion, on_delete=models.CASCADE, related_name="responses"
    )
    order = models.PositiveSmallIntegerField()
    answer = models.TextField(blank=True)
    score = models.FloatField(
        null=True, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    confidence = models.FloatField(
        default=5.0, validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    time_spent_seconds = models.PositiveIntegerField(default=0)
    tests_passed = models.PositiveSmallIntegerField(null=True, blank=True)
    tests_total = models.PositiveSmallIntegerField(null=True, blank=True)
    auto_scored = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]
        unique_together = ["session", "order"]

    def __str__(self) -> str:
        return f"Response Q{self.order} — {self.session_id}"


class CognitiveQuestionType(models.TextChoices):
    APTITUDE = "aptitude", "Aptitude"
    BRAIN_TEASER = "brain_teaser", "Brain Teaser"


class CognitiveQuestion(UUIDModel):
    challenge_type = models.CharField(max_length=20, choices=CognitiveQuestionType.choices)
    category = models.CharField(max_length=80)
    order = models.PositiveIntegerField()
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM
    )
    question = models.TextField()
    answer = models.TextField()
    explanation = models.TextField(blank=True)
    hints = models.TextField(blank=True)

    class Meta:
        ordering = ["challenge_type", "order"]
        indexes = [
            models.Index(fields=["challenge_type"]),
            models.Index(fields=["challenge_type", "category"]),
            models.Index(fields=["challenge_type", "order"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["challenge_type", "order"],
                name="unique_cognitive_type_order",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.challenge_type} #{self.order}: {self.question[:50]}"

    # Per-question think-fast limits (seconds) by type + difficulty.
    TIME_LIMITS = {
        "aptitude": {
            "easy": 45,
            "medium": 75,
            "hard": 90,
            "expert": 120,
        },
        "brain_teaser": {
            "easy": 90,
            "medium": 120,
            "hard": 150,
            "expert": 180,
        },
    }

    @property
    def time_limit_seconds(self) -> int:
        by_type = self.TIME_LIMITS.get(self.challenge_type, self.TIME_LIMITS["aptitude"])
        return by_type.get(self.difficulty, by_type["medium"])

    @property
    def time_limit_label(self) -> str:
        secs = self.time_limit_seconds
        if secs < 60:
            return f"{secs}s"
        mins, rem = divmod(secs, 60)
        return f"{mins}m" if rem == 0 else f"{mins}m {rem}s"


class CognitiveProgress(UUIDModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cognitive_progress",
    )
    question = models.ForeignKey(
        CognitiveQuestion, on_delete=models.CASCADE, related_name="progress"
    )
    revealed = models.BooleanField(default=False)
    revealed_at = models.DateTimeField(null=True, blank=True)
    attempted_answer = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    time_spent_seconds = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["user", "question"]
        indexes = [models.Index(fields=["user", "revealed"])]

    def __str__(self) -> str:
        return f"{self.user.username} — {self.question_id}"
