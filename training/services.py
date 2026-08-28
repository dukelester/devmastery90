"""Business logic services for DevMastery 90."""
from datetime import date, timedelta
from typing import Any

from django.conf import settings
from django.db.models import Avg, Count, Q, Sum
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
)


def get_or_create_profile(user) -> UserProfile:
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def get_current_day_number(user) -> int:
    profile = get_or_create_profile(user)
    if profile.program_start_date:
        delta = (date.today() - profile.program_start_date).days + 1
        return max(1, min(delta, 90))
    return 1


def get_training_day(day_number: int) -> TrainingDay | None:
    return TrainingDay.objects.filter(day_number=day_number).select_related("week").first()


def get_today_training_day(user) -> TrainingDay | None:
    return get_training_day(get_current_day_number(user))


def calculate_progress(user) -> dict[str, Any]:
    """Calculate overall program progress for a user."""
    current_day = get_current_day_number(user)
    total_days = 90
    days_remaining = max(0, total_days - current_day)

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    task_progress = (completed_tasks / total_tasks * 100) if total_tasks else 0.0

    day_progress = (current_day / total_days) * 100

    profile = get_or_create_profile(user)
    study_hours = profile.total_study_minutes / 60

    completed_days = TrainingDay.objects.filter(completed=True).count()

    return {
        "current_day": current_day,
        "total_days": total_days,
        "days_remaining": days_remaining,
        "day_progress": round(day_progress, 1),
        "task_progress": round(task_progress, 1),
        "completed_tasks": completed_tasks,
        "total_tasks": total_tasks,
        "completed_days": completed_days,
        "study_hours": round(study_hours, 1),
        "streak": profile.current_streak,
        "xp": profile.xp,
        "level": profile.level,
        "level_title": profile.level_title,
    }


def calculate_streak(user) -> dict[str, Any]:
    """Calculate current and longest streak based on study activity."""
    profile = get_or_create_profile(user)
    today = date.today()

    sessions = StudySession.objects.filter(
        user=user, ended_at__isnull=False
    ).order_by("-started_at")

    if not sessions.exists():
        return {
            "current_streak": 0,
            "longest_streak": profile.longest_streak,
            "last_activity": None,
        }

    active_dates = set()
    for session in sessions:
        active_dates.add(session.started_at.date())

    current_streak = 0
    check_date = today
    if today not in active_dates:
        check_date = today - timedelta(days=1)

    while check_date in active_dates:
        current_streak += 1
        check_date -= timedelta(days=1)

    longest = profile.longest_streak
    if current_streak > longest:
        longest = current_streak
        profile.longest_streak = longest
        profile.current_streak = current_streak
        profile.save(update_fields=["current_streak", "longest_streak"])

    return {
        "current_streak": current_streak,
        "longest_streak": longest,
        "last_activity": profile.last_activity_date,
    }


def update_streak_on_activity(user) -> None:
    """Update streak when user completes study activity."""
    profile = get_or_create_profile(user)
    today = date.today()

    if profile.last_activity_date == today:
        return

    if profile.last_activity_date == today - timedelta(days=1):
        profile.current_streak += 1
    elif profile.last_activity_date != today:
        profile.current_streak = 1

    profile.last_activity_date = today
    if profile.current_streak > profile.longest_streak:
        profile.longest_streak = profile.current_streak
    profile.save()


def award_xp(user, amount: int) -> UserProfile:
    """Award XP and update level."""
    profile = get_or_create_profile(user)
    profile.xp += amount
    new_level = max(1, (profile.xp // UserProfile.XP_PER_LEVEL) + 1)
    if new_level > profile.level:
        profile.level = min(new_level, 6)
    profile.save()
    return profile


def update_training_day_completion(training_day: TrainingDay) -> None:
    """Update training day completion percentage based on tasks."""
    tasks = training_day.tasks.all()
    total = tasks.count()
    if total == 0:
        return
    completed = tasks.filter(completed=True).count()
    pct = (completed / total) * 100
    training_day.completion_percentage = pct
    training_day.completed = pct >= 100
    training_day.save(update_fields=["completion_percentage", "completed"])


def get_skill_scores(user) -> list[dict[str, Any]]:
    """Get all skill scores for display."""
    skills = Skill.objects.all().order_by("name")
    results = []
    for skill in skills:
        health = calculate_skill_health(user, skill)
        results.append({
            "skill": skill,
            "score": health["score"],
            "trend": health["trend"],
            "weakness_level": health["weakness_level"],
        })
    return results


def calculate_skill_health(user, skill: Skill) -> dict[str, Any]:
    """Calculate skill health based on multiple performance factors."""
    assessments = Assessment.objects.filter(user=user, skill=skill).order_by("-completed_at")
    coding = CodingProblem.objects.filter(user=user, category__icontains=skill.name.split()[0])
    mistakes = Mistake.objects.filter(user=user, skill=skill, resolved=False)
    tasks = Task.objects.filter(skill=skill, completed=True)

    base_score = skill.current_score

    # Assessment performance (40% weight)
    assessment_score = base_score
    if assessments.exists():
        recent = assessments[:3]
        assessment_score = sum(a.percentage / 10 for a in recent) / len(recent)

    # Coding performance (25% weight)
    coding_score = base_score
    if coding.exists():
        solved = coding.filter(solved=True).count()
        total = coding.count()
        coding_score = (solved / total) * 10 if total else base_score

    # Task completion (15% weight)
    total_skill_tasks = Task.objects.filter(skill=skill).count()
    completed_skill_tasks = tasks.count()
    task_score = (
        (completed_skill_tasks / total_skill_tasks) * 10 if total_skill_tasks else base_score
    )

    # Mistake penalty (10% weight)
    mistake_penalty = min(mistakes.count() * 0.3, 3.0)

    # Confidence from coding (10% weight)
    confidence = base_score
    if coding.filter(solved=True).exists():
        confidence = coding.filter(solved=True).aggregate(avg=Avg("confidence"))["avg"] or base_score

    score = (
        assessment_score * 0.4
        + coding_score * 0.25
        + task_score * 0.15
        + confidence * 0.1
        + base_score * 0.1
    ) - mistake_penalty
    score = max(0.0, min(10.0, round(score, 1)))

    # Trend calculation
    trend = "→"
    if assessments.count() >= 2:
        latest = assessments[0].percentage
        previous = assessments[1].percentage
        if latest > previous + 5:
            trend = "↑"
        elif latest < previous - 5:
            trend = "↓"

    weakness_level = "LOW"
    if score < 5.0:
        weakness_level = "HIGH"
    elif score < 7.0:
        weakness_level = "MEDIUM"

    primary_weakness = ""
    if mistakes.exists():
        primary_weakness = mistakes.first().description[:80]
    elif score < 7.0:
        primary_weakness = f"Needs improvement in {skill.name}"

    recommended_action = _get_skill_recommendation(skill, score, mistakes)

    return {
        "score": score,
        "trend": trend,
        "confidence": round(confidence, 1),
        "weakness_level": weakness_level,
        "primary_weakness": primary_weakness,
        "recommended_action": recommended_action,
    }


def _get_skill_recommendation(skill: Skill, score: float, mistakes) -> str:
    recommendations = {
        "postgresql": "Complete EXPLAIN ANALYZE exercises and optimize slow queries.",
        "python": "Solve advanced Python problems focusing on decorators and generators.",
        "algorithms-data-structures": "Practice weak DSA patterns with timed problem sets.",
        "system-design": "Design 2 systems this week and record your answers.",
        "django": "Build a production DRF API with auth and testing.",
        "redis": "Implement cache-aside pattern with TTL and invalidation.",
        "testing": "Write integration tests for your project APIs.",
        "aws": "Complete hands-on exercises with EC2, S3, and RDS.",
    }
    if score < 6.0 and skill.slug in recommendations:
        return recommendations[skill.slug]
    if mistakes.exists():
        return f"Review and resolve: {mistakes.first().description[:60]}"
    return f"Continue structured practice in {skill.name}."


def get_top_weaknesses(user, limit: int = 3) -> list[dict[str, Any]]:
    """Get top weaknesses across all skills."""
    skills = Skill.objects.all()
    weaknesses = []
    for skill in skills:
        health = calculate_skill_health(user, skill)
        if health["weakness_level"] in ("HIGH", "MEDIUM"):
            weaknesses.append({
                "skill": skill,
                "score": health["score"],
                "weakness_level": health["weakness_level"],
                "recommended_action": health["recommended_action"],
            })
    weaknesses.sort(key=lambda x: x["score"])
    return weaknesses[:limit]


def get_daily_recommendations(user) -> list[dict[str, Any]]:
    """Generate prioritized daily recommendations."""
    recommendations = []
    current_day = get_current_day_number(user)
    training_day = get_training_day(current_day)

    # 1. Overdue incomplete tasks from past days
    overdue = Task.objects.filter(
        training_day__day_number__lt=current_day,
        completed=False,
        skipped=False,
    ).select_related("skill", "training_day").order_by("training_day__day_number")[:3]
    for task in overdue:
        recommendations.append({
            "priority": "critical",
            "title": f"Overdue: {task.title}",
            "minutes": task.estimated_minutes,
            "reason": f"From Day {task.training_day.day_number}",
            "task_id": task.id,
            "type": "overdue",
        })

    # 2. Weak skills
    for weakness in get_top_weaknesses(user, 2):
        recommendations.append({
            "priority": "high",
            "title": f"Strengthen {weakness['skill'].name}",
            "minutes": 45,
            "reason": weakness["recommended_action"],
            "skill_slug": weakness["skill"].slug,
            "type": "weakness",
        })

    # 3. Recent assessment failures
    failed = Assessment.objects.filter(user=user, percentage__lt=70).order_by("-completed_at")[:2]
    for assessment in failed:
        recommendations.append({
            "priority": "high",
            "title": f"Review {assessment.name}",
            "minutes": 30,
            "reason": f"Scored {assessment.percentage}% — needs improvement",
            "type": "assessment",
        })

    # 4. Repeated mistakes
    repeated = (
        Mistake.objects.filter(user=user, resolved=False)
        .values("description")
        .annotate(count=Count("id"))
        .filter(count__gte=2)
        .order_by("-count")[:2]
    )
    for mistake in repeated:
        recommendations.append({
            "priority": "medium",
            "title": "Resolve repeated mistake",
            "minutes": 30,
            "reason": mistake["description"][:80],
            "type": "mistake",
        })

    # 5. Today's scheduled tasks
    if training_day:
        today_tasks = training_day.tasks.filter(
            completed=False, skipped=False
        ).select_related("skill")[:4]
        for task in today_tasks:
            recommendations.append({
                "priority": task.priority,
                "title": task.title,
                "minutes": task.estimated_minutes,
                "reason": f"Day {current_day} curriculum",
                "task_id": task.id,
                "type": "scheduled",
            })

    # Sort by priority
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))
    return recommendations[:8]


def get_analytics_data(user) -> dict[str, Any]:
    """Get comprehensive analytics data."""
    profile = get_or_create_profile(user)
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    daily_minutes = StudySession.objects.filter(
        user=user, started_at__date=today, ended_at__isnull=False
    ).aggregate(total=Sum("duration_minutes"))["total"] or 0

    weekly_minutes = StudySession.objects.filter(
        user=user, started_at__date__gte=week_start, ended_at__isnull=False
    ).aggregate(total=Sum("duration_minutes"))["total"] or 0

    monthly_minutes = StudySession.objects.filter(
        user=user, started_at__date__gte=month_start, ended_at__isnull=False
    ).aggregate(total=Sum("duration_minutes"))["total"] or 0

    assessment_avg = Assessment.objects.filter(user=user).aggregate(
        avg=Avg("percentage")
    )["avg"] or 0

    coding_stats = CodingProblem.objects.filter(user=user).aggregate(
        total=Count("id"),
        solved=Count("id", filter=Q(solved=True)),
    )
    coding_rate = (
        (coding_stats["solved"] / coding_stats["total"] * 100)
        if coding_stats["total"] else 0
    )

    mistake_count = Mistake.objects.filter(user=user, resolved=False).count()
    streak_data = calculate_streak(user)

    # Weekly study hours for chart (last 8 weeks)
    weekly_hours = []
    for i in range(7, -1, -1):
        ws = today - timedelta(days=today.weekday() + i * 7)
        we = ws + timedelta(days=6)
        mins = StudySession.objects.filter(
            user=user,
            started_at__date__gte=ws,
            started_at__date__lte=we,
            ended_at__isnull=False,
        ).aggregate(total=Sum("duration_minutes"))["total"] or 0
        weekly_hours.append({"week": ws.isoformat(), "hours": round(mins / 60, 1)})

    return {
        "daily_hours": round(daily_minutes / 60, 1),
        "weekly_hours": round(weekly_minutes / 60, 1),
        "monthly_hours": round(monthly_minutes / 60, 1),
        "total_hours": round(profile.total_study_minutes / 60, 1),
        "assessment_avg": round(assessment_avg, 1),
        "coding_total": coding_stats["total"],
        "coding_solved": coding_stats["solved"],
        "coding_rate": round(coding_rate, 1),
        "mistake_count": mistake_count,
        "streak": streak_data["current_streak"],
        "weekly_hours_chart": weekly_hours,
        "skill_scores": get_skill_scores(user),
    }


def get_coding_stats(user) -> dict[str, Any]:
    """Get coding problem statistics."""
    problems = CodingProblem.objects.filter(user=user)
    total = problems.count()
    solved = problems.filter(solved=True).count()

    categories = (
        problems.values("category")
        .annotate(
            total=Count("id"),
            solved=Count("id", filter=Q(solved=True)),
        )
        .order_by("-total")
    )

    category_stats = []
    for cat in categories:
        if cat["category"]:
            rate = (cat["solved"] / cat["total"] * 100) if cat["total"] else 0
            category_stats.append({
                "category": cat["category"],
                "total": cat["total"],
                "solved": cat["solved"],
                "rate": round(rate, 1),
            })

    avg_time = problems.filter(solved=True, time_taken__isnull=False).aggregate(
        avg=Avg("time_taken")
    )["avg"]

    return {
        "total": total,
        "solved": solved,
        "unsolved": total - solved,
        "success_rate": round((solved / total * 100) if total else 0, 1),
        "avg_solve_time": round(avg_time or 0, 1),
        "categories": category_stats,
        "problems": problems.order_by("-created_at")[:50],
    }


def get_interview_stats(user) -> dict[str, Any]:
    """Get interview practice statistics."""
    from training.models import InterviewAttempt, InterviewQuestion

    attempts = InterviewAttempt.objects.filter(user=user).select_related("question")
    categories = InterviewQuestion.objects.values_list("category", flat=True).distinct()

    category_stats = []
    for category in categories:
        cat_attempts = attempts.filter(question__category=category)
        if cat_attempts.exists():
            avg_score = cat_attempts.aggregate(avg=Avg("score"))["avg"] or 0
            needs_review = cat_attempts.filter(needs_review=True).count()
            category_stats.append({
                "category": category,
                "attempted": cat_attempts.count(),
                "avg_score": round(avg_score, 1),
                "needs_review": needs_review,
            })

    return {
        "total_attempts": attempts.count(),
        "categories": category_stats,
        "recent_attempts": attempts.order_by("-created_at")[:20],
        "questions": InterviewQuestion.objects.all()[:50],
    }
