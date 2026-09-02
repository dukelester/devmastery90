"""Business logic services for DevMastery 90."""
from datetime import date, timedelta
from typing import Any

from django.conf import settings
from django.db.models import Avg, Count, Max, Q, Sum
from django.utils import timezone

from training.constants import PROGRAM_CORE_DAYS, PROGRAM_ELITE_DAYS
from training.models import (
    Assessment,
    CodingProblem,
    LearningResource,
    Mistake,
    Skill,
    StudySession,
    Task,
    TrainingDay,
    UserProfile,
)


def get_program_total_days() -> int:
    """Return seeded program length (90 core, 120 with Phase 4)."""
    max_day = TrainingDay.objects.aggregate(m=Max("day_number"))["m"]
    if max_day and max_day >= PROGRAM_CORE_DAYS:
        return int(max_day)
    return PROGRAM_CORE_DAYS


def get_or_create_profile(user) -> UserProfile:
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def get_current_day_number(user) -> int:
    profile = get_or_create_profile(user)
    total = get_program_total_days()
    if profile.program_start_date:
        delta = (date.today() - profile.program_start_date).days + 1
        return max(1, min(delta, total))
    return 1


def get_training_day(day_number: int) -> TrainingDay | None:
    return TrainingDay.objects.filter(day_number=day_number).select_related("week").first()


def get_today_training_day(user) -> TrainingDay | None:
    return get_training_day(get_current_day_number(user))


def calculate_progress(user) -> dict[str, Any]:
    """Calculate overall program progress for a user."""
    current_day = get_current_day_number(user)
    total_days = get_program_total_days()
    days_remaining = max(0, total_days - current_day)

    total_tasks = Task.objects.count()
    completed_tasks = Task.objects.filter(completed=True).count()
    task_progress = (completed_tasks / total_tasks * 100) if total_tasks else 0.0

    day_progress = (current_day / total_days) * 100

    profile = get_or_create_profile(user)
    study_hours = profile.total_study_minutes / 60

    completed_days = TrainingDay.objects.filter(completed=True).count()
    in_mastery = current_day > PROGRAM_CORE_DAYS and total_days >= PROGRAM_ELITE_DAYS

    return {
        "current_day": current_day,
        "total_days": total_days,
        "core_days": PROGRAM_CORE_DAYS,
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
        "in_mastery_track": in_mastery,
        "phase_label": "Phase 4 — Elite Mastery" if in_mastery else "Core 90",
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


def build_milestones(user, profile: UserProfile | None = None) -> dict[str, Any]:
    """Computed achievement milestones for gamification UI."""
    profile = profile or get_or_create_profile(user)
    current_day = get_current_day_number(user)
    coding_solved = CodingProblem.objects.filter(user=user, solved=True).count()
    from training.models import MockInterviewSession

    mocks_done = MockInterviewSession.objects.filter(
        user=user, status=MockInterviewSession.Status.COMPLETED
    ).count()
    study_hours = profile.total_study_minutes / 60
    tasks_done = Task.objects.filter(completed=True).count()

    milestones = [
        {"key": "week1", "label": "Week 1", "hint": "Reach day 7", "earned": current_day >= 7},
        {"key": "month1", "label": "Month 1", "hint": "Reach day 30", "earned": current_day >= 30},
        {"key": "month2", "label": "Month 2", "hint": "Reach day 60", "earned": current_day >= 60},
        {"key": "day90", "label": "Day 90", "hint": "Finish the core program", "earned": current_day >= 90},
        {"key": "day120", "label": "Day 120", "hint": "Complete elite mastery track", "earned": current_day >= 120},
        {
            "key": "streak7",
            "label": "7-day streak",
            "hint": "Stay consistent for a week",
            "earned": profile.current_streak >= 7 or profile.longest_streak >= 7,
        },
        {
            "key": "streak14",
            "label": "14-day streak",
            "hint": "Two weeks locked in",
            "earned": profile.current_streak >= 14 or profile.longest_streak >= 14,
        },
        {
            "key": "streak30",
            "label": "30-day streak",
            "hint": "A full month of fire",
            "earned": profile.current_streak >= 30 or profile.longest_streak >= 30,
        },
        {"key": "xp1k", "label": "1K XP", "hint": "Earn 1,000 XP", "earned": profile.xp >= 1000},
        {"key": "xp3k", "label": "3K XP", "hint": "Earn 3,000 XP", "earned": profile.xp >= 3000},
        {"key": "xp5k", "label": "5K XP", "hint": "Earn 5,000 XP", "earned": profile.xp >= 5000},
        {
            "key": "study10h",
            "label": "10h studied",
            "hint": "Log 10 hours of focus",
            "earned": study_hours >= 10,
        },
        {
            "key": "study50h",
            "label": "50h studied",
            "hint": "Log 50 hours of focus",
            "earned": study_hours >= 50,
        },
        {
            "key": "coding10",
            "label": "10 solves",
            "hint": "Solve 10 coding problems",
            "earned": coding_solved >= 10,
        },
        {
            "key": "mock1",
            "label": "First mock",
            "hint": "Complete a mock interview",
            "earned": mocks_done >= 1,
        },
        {
            "key": "tasks50",
            "label": "50 tasks",
            "hint": "Complete 50 curriculum tasks",
            "earned": tasks_done >= 50,
        },
    ]
    earned = sum(1 for m in milestones if m["earned"])
    return {
        "items": milestones,
        "earned_count": earned,
        "total_count": len(milestones),
        "earned_pct": round((earned / len(milestones)) * 100, 1) if milestones else 0,
    }


def get_day_planned_minutes(training_day: TrainingDay | None) -> int:
    """Planned workload for a day: max of target vs sum of task estimates."""
    if training_day is None:
        return 0
    task_minutes = (
        training_day.tasks.aggregate(total=Sum("estimated_minutes"))["total"] or 0
    )
    return max(training_day.target_minutes, task_minutes)


def assess_workload(user) -> dict[str, Any]:
    """
    Detect sustained high planned (or logged) workload.

    Encourages sustainable pace — does not push longer hours.
    """
    high = getattr(settings, "WORKLOAD_HIGH_MINUTES", 240)
    excessive = getattr(settings, "WORKLOAD_EXCESSIVE_MINUTES", 300)
    consecutive_needed = getattr(settings, "WORKLOAD_CONSECUTIVE_DAYS", 3)
    sustainable = getattr(settings, "WORKLOAD_SUSTAINABLE_MINUTES", 210)
    actual_high = getattr(settings, "WORKLOAD_ACTUAL_HIGH_MINUTES", 300)

    current = get_current_day_number(user)
    window_start = max(1, current - consecutive_needed + 1)
    day_numbers = list(range(window_start, current + 1))

    days = {
        d.day_number: d
        for d in TrainingDay.objects.filter(day_number__in=day_numbers).prefetch_related(
            "tasks"
        )
    }

    recent: list[dict[str, Any]] = []
    consecutive_high = 0
    for day_num in reversed(day_numbers):
        day = days.get(day_num)
        planned = get_day_planned_minutes(day)
        is_high = planned >= high
        recent.append(
            {
                "day_number": day_num,
                "planned_minutes": planned,
                "planned_hours": round(planned / 60, 1),
                "is_high": is_high,
                "is_excessive": planned >= excessive,
            }
        )
        if is_high:
            consecutive_high += 1
        else:
            break

    recent.reverse()

    # Logged study overload (actual hours)
    lookback = date.today() - timedelta(days=consecutive_needed - 1)
    actual_by_day = (
        StudySession.objects.filter(
            user=user,
            ended_at__isnull=False,
            started_at__date__gte=lookback,
        )
        .values("started_at__date")
        .annotate(total=Sum("duration_minutes"))
    )
    heavy_logged_days = sum(1 for row in actual_by_day if (row["total"] or 0) >= actual_high)

    planned_alert = consecutive_high >= consecutive_needed
    actual_alert = heavy_logged_days >= consecutive_needed
    alert = planned_alert or actual_alert

    today_planned = recent[-1]["planned_minutes"] if recent else 0

    reason = "planned"
    if actual_alert and not planned_alert:
        reason = "logged"
    elif actual_alert and planned_alert:
        reason = "both"

    return {
        "alert": alert,
        "reason": reason,
        "consecutive_high_days": consecutive_high,
        "heavy_logged_days": heavy_logged_days,
        "threshold_minutes": high,
        "sustainable_minutes": sustainable,
        "today_planned_minutes": today_planned,
        "today_planned_hours": round(today_planned / 60, 1),
        "recent_days": recent,
        "suggestions": [
            "moving low-priority tasks",
            "reducing today's workload",
            "continuing at the normal pace",
        ],
    }


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
    """Generate prioritized daily recommendations.

    When workload is elevated, prefer a lighter list and do not stack
    extra practice on top of an already heavy day.
    """
    recommendations = []
    current_day = get_current_day_number(user)
    training_day = get_training_day(current_day)
    workload = assess_workload(user)
    light_mode = workload["alert"]

    # 1. Overdue incomplete tasks from past days
    overdue_limit = 1 if light_mode else 3
    overdue = Task.objects.filter(
        training_day__day_number__lt=current_day,
        completed=False,
        skipped=False,
    ).select_related("skill", "training_day").order_by("training_day__day_number")[:overdue_limit]
    for task in overdue:
        recommendations.append({
            "priority": "critical",
            "title": f"Overdue: {task.title}",
            "minutes": task.estimated_minutes,
            "reason": f"From Day {task.training_day.day_number}",
            "task_id": task.id,
            "type": "overdue",
        })

    # 2. Weak skills — skip stacking when workload is already high
    if not light_mode:
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
    if not light_mode:
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
    if not light_mode:
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

    # 5. Today's scheduled tasks (cap when protecting workload)
    if training_day:
        task_limit = 2 if light_mode else 4
        today_tasks = training_day.tasks.filter(
            completed=False, skipped=False
        ).select_related("skill").order_by("order")[:task_limit]
        for task in today_tasks:
            recommendations.append({
                "priority": task.priority,
                "title": task.title,
                "minutes": task.estimated_minutes,
                "reason": f"Day {current_day} curriculum",
                "task_id": task.id,
                "type": "scheduled",
            })

    # 6. Curated resources for today / weak skills
    if not light_mode:
        for resource in get_day_resources(current_day)[:2]:
            recommendations.append({
                "priority": "medium",
                "title": f"Read: {resource.title}",
                "minutes": 20,
                "reason": resource.description or resource.get_resource_type_display(),
                "type": "resource",
                "url": resource.url,
                "skill_slug": resource.skill.slug if resource.skill_id else "",
            })
        for weakness in get_top_weaknesses(user, 1):
            skill_resources = LearningResource.objects.filter(
                skill=weakness["skill"]
            ).order_by("-is_primary", "order")[:1]
            for resource in skill_resources:
                recommendations.append({
                    "priority": "medium",
                    "title": f"Resource: {resource.title}",
                    "minutes": 25,
                    "reason": f"Supports weak skill — {weakness['skill'].name}",
                    "type": "resource",
                    "url": resource.url,
                    "skill_slug": weakness["skill"].slug,
                })

    if light_mode:
        recommendations.insert(0, {
            "priority": "high",
            "title": "Protect sustainable pace",
            "minutes": 0,
            "reason": "Workload has been high. Prefer quality over volume today.",
            "type": "workload",
        })

    # Sort by priority
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))
    return recommendations[: (5 if light_mode else 8)]


def get_day_resources(day_number: int) -> list[LearningResource]:
    """Curated resources for a curriculum day (plus week-level fallbacks)."""
    day = get_training_day(day_number)
    qs = LearningResource.objects.filter(day_number=day_number).select_related("skill")
    resources = list(qs.order_by("-is_primary", "order", "title"))
    if day and day.week_id and len(resources) < 3:
        week_extras = (
            LearningResource.objects.filter(week_number=day.week.week_number)
            .exclude(id__in=[r.id for r in resources])
            .select_related("skill")
            .order_by("-is_primary", "order")[: 3 - len(resources)]
        )
        resources.extend(week_extras)
    return resources


def get_analytics_data(user) -> dict[str, Any]:
    """Get comprehensive analytics / reports data with visual progress series."""
    from training.models import MockInterviewSession, Week, WeeklyReview

    profile = get_or_create_profile(user)
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    progress = calculate_progress(user)
    streak_data = calculate_streak(user)
    milestones = build_milestones(user, profile)

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
        if coding_stats["total"]
        else 0
    )

    mistake_count = Mistake.objects.filter(user=user, resolved=False).count()
    mistake_total = Mistake.objects.filter(user=user).count()
    mistake_resolved = Mistake.objects.filter(user=user, resolved=True).count()

    mocks = MockInterviewSession.objects.filter(user=user)
    mocks_completed = mocks.filter(status=MockInterviewSession.Status.COMPLETED).count()
    completed_mocks = mocks.filter(
        status=MockInterviewSession.Status.COMPLETED, max_score__gt=0
    )
    mock_avg = completed_mocks.aggregate(avg=Avg("total_score"))["avg"] or 0
    mock_max_avg = completed_mocks.aggregate(avg=Avg("max_score"))["avg"] or 0
    mock_pct = round((mock_avg / mock_max_avg) * 100, 1) if mock_max_avg else 0

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
        weekly_hours.append(
            {
                "week": ws.isoformat(),
                "label": f"W{ws.isocalendar()[1]}",
                "hours": round(mins / 60, 1),
            }
        )
    max_week_h = max((w["hours"] for w in weekly_hours), default=0) or 1
    for w in weekly_hours:
        w["height_pct"] = max(4, round((w["hours"] / max_week_h) * 100)) if w["hours"] else 2

    # Daily study minutes (last 14 days)
    daily_chart = []
    for i in range(13, -1, -1):
        d = today - timedelta(days=i)
        mins = StudySession.objects.filter(
            user=user, started_at__date=d, ended_at__isnull=False
        ).aggregate(total=Sum("duration_minutes"))["total"] or 0
        daily_chart.append(
            {
                "date": d.isoformat(),
                "label": d.strftime("%a"),
                "day_num": d.day,
                "minutes": mins,
                "hours": round(mins / 60, 1),
            }
        )
    max_day_m = max((d["minutes"] for d in daily_chart), default=0) or 1
    for d in daily_chart:
        d["height_pct"] = max(4, round((d["minutes"] / max_day_m) * 100)) if d["minutes"] else 2

    # Activity heatmap (last 28 days)
    heatmap = []
    for i in range(27, -1, -1):
        d = today - timedelta(days=i)
        mins = StudySession.objects.filter(
            user=user, started_at__date=d, ended_at__isnull=False
        ).aggregate(total=Sum("duration_minutes"))["total"] or 0
        if mins <= 0:
            level = 0
        elif mins < 30:
            level = 1
        elif mins < 90:
            level = 2
        elif mins < 180:
            level = 3
        else:
            level = 4
        heatmap.append(
            {
                "date": d.isoformat(),
                "label": d.strftime("%b %d"),
                "minutes": mins,
                "level": level,
            }
        )

    skill_scores = get_skill_scores(user)
    for s in skill_scores:
        score = float(s.get("score") or 0)
        s["bar_pct"] = max(0, min(100, round(score * 10)))

    # Weekly review links (current + recent)
    current_week_num = max(1, min(13, ((progress["current_day"] - 1) // 7) + 1))
    weeks = list(Week.objects.order_by("week_number")[:13])
    current_week = next((w for w in weeks if w.week_number == current_week_num), weeks[0] if weeks else None)
    reviews_by_week = {
        r.week_id: r
        for r in WeeklyReview.objects.filter(user=user).select_related("week")
    }
    week_reports = []
    for week in weeks:
        review = reviews_by_week.get(week.id)
        week_reports.append(
            {
                "id": week.id,
                "week_number": week.week_number,
                "title": week.title,
                "is_current": week.week_number == current_week_num,
                "has_review": bool(
                    review
                    and (
                        review.learned
                        or review.went_well
                        or review.improve
                        or review.next_week_focus
                    )
                ),
                "study_minutes": review.study_minutes if review else 0,
            }
        )

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
        "mistake_total": mistake_total,
        "mistake_resolved": mistake_resolved,
        "streak": streak_data["current_streak"],
        "longest_streak": streak_data["longest_streak"],
        "weekly_hours_chart": weekly_hours,
        "daily_chart": daily_chart,
        "heatmap": heatmap,
        "skill_scores": skill_scores,
        "progress": progress,
        "milestones": milestones,
        "mocks_completed": mocks_completed,
        "mock_pct": mock_pct,
        "week_reports": week_reports,
        "current_week_num": current_week_num,
        "current_week_id": current_week.id if current_week else None,
        "report_generated": today.isoformat(),
        "xp": profile.xp,
        "xp_display": profile.xp_display,
        "xp_into_level": profile.xp_into_level,
        "xp_to_next": profile.xp_to_next_level,
        "xp_pct": profile.xp_progress_pct,
        "level": profile.level,
        "level_title": profile.level_title,
        "level_display": profile.level_display,
        "next_level_title": profile.next_level_title,
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
    """Get interview/practice statistics for legacy template compatibility."""
    return get_practice_hub_data(user)


def get_unlocked_order(user, section_slug: str) -> int:
    from training.models import PracticeProgress

    progress = PracticeProgress.objects.filter(
        user=user, section_slug=section_slug
    ).first()
    return progress.unlocked_through_order if progress else 1


def can_access_practice_question(user, question) -> bool:
    return question.order <= get_unlocked_order(user, question.section_slug)


def get_section_progress(user, section_slug: str) -> dict[str, Any]:
    from training.models import InterviewAttempt, InterviewQuestion, PracticeProgress

    total = InterviewQuestion.objects.filter(section_slug=section_slug).count()
    unlocked_order = get_unlocked_order(user, section_slug)
    passed_orders = set(
        InterviewAttempt.objects.filter(
            user=user,
            question__section_slug=section_slug,
            passed=True,
        ).values_list("question__order", flat=True)
    )
    completed_count = len(passed_orders)
    progress = PracticeProgress.objects.filter(
        user=user, section_slug=section_slug
    ).first()

    return {
        "total": total,
        "unlocked_order": unlocked_order,
        "completed_count": completed_count,
        "percent": round((completed_count / total * 100) if total else 0, 1),
        "last_activity_at": progress.last_activity_at if progress else None,
    }


def get_practice_hub_data(user) -> dict[str, Any]:
    from training.models import InterviewAttempt, InterviewQuestion
    from training.practice_bank.sections import PRACTICE_SECTIONS

    attempts = InterviewAttempt.objects.filter(user=user).select_related("question")
    sections = []
    for section in PRACTICE_SECTIONS:
        prog = get_section_progress(user, section["slug"])
        sections.append({**section, **prog})

    return {
        "total_attempts": attempts.count(),
        "sections": sections,
        "recent_attempts": attempts.order_by("-created_at")[:15],
        "total_questions": InterviewQuestion.objects.count(),
    }


def get_practice_section_data(user, section_slug: str) -> dict[str, Any]:
    from training.models import InterviewQuestion, ProficiencyLevel
    from training.practice_bank.sections import PRACTICE_SECTIONS

    section_meta = next(
        (s for s in PRACTICE_SECTIONS if s["slug"] == section_slug), None
    )
    if not section_meta:
        return {}

    questions = list(
        InterviewQuestion.objects.filter(section_slug=section_slug).order_by("order")
    )
    unlocked_order = get_unlocked_order(user, section_slug)
    progress = get_section_progress(user, section_slug)

    level_stats = []
    from training.models import InterviewAttempt, ProficiencyLevel

    for level in ProficiencyLevel:
        level_qs = [q for q in questions if q.level == level]
        if not level_qs:
            continue
        passed_count = InterviewAttempt.objects.filter(
            user=user,
            question__section_slug=section_slug,
            question__level=level,
            passed=True,
        ).count()
        level_stats.append({
            "level": level,
            "label": level.label,
            "total": len(level_qs),
            "passed": passed_count,
        })

    current_question = next(
        (q for q in questions if q.order == unlocked_order),
        None,
    )

    question_states = []
    for q in questions:
        question_states.append({
            "question": q,
            "is_unlocked": q.order <= unlocked_order,
            "is_passed": q.order < unlocked_order,
            "is_current": q.order == unlocked_order,
        })

    return {
        "section": section_meta,
        "progress": progress,
        "level_stats": level_stats,
        "current_question": current_question,
        "question_states": question_states,
        "unlocked_order": unlocked_order,
    }


def submit_practice_attempt(user, question, data: dict[str, Any]) -> dict[str, Any]:
    from django.utils import timezone

    from training.models import InterviewAttempt, PracticeProgress

    if not can_access_practice_question(user, question):
        return {"error": "Question is locked. Complete previous questions first.", "passed": False}

    score = float(data.get("score", 0))
    confidence = float(data.get("confidence", 5))
    passed = score >= question.min_pass_score

    attempt = InterviewAttempt.objects.create(
        user=user,
        question=question,
        answer=data.get("answer", ""),
        confidence=confidence,
        score=score,
        notes=data.get("notes", ""),
        needs_review=data.get("needs_review", False) or (not passed),
        passed=passed,
    )

    if passed:
        progress, _ = PracticeProgress.objects.get_or_create(
            user=user,
            section_slug=question.section_slug,
            defaults={"unlocked_through_order": 1},
        )
        if question.order >= progress.unlocked_through_order:
            progress.unlocked_through_order = question.order + 1
        progress.completed_count = InterviewAttempt.objects.filter(
            user=user,
            question__section_slug=question.section_slug,
            passed=True,
        ).count()
        progress.last_activity_at = timezone.now()
        progress.save()
        award_xp(user, 15)
        update_streak_on_activity(user)

    return {
        "attempt": attempt,
        "passed": passed,
        "unlocked_order": get_unlocked_order(user, question.section_slug),
        "error": None,
    }


def needs_onboarding(user) -> bool:
    profile = get_or_create_profile(user)
    return profile.program_start_date is None


def get_repeated_mistakes(user, limit: int = 5) -> list[dict[str, Any]]:
    rows = (
        Mistake.objects.filter(user=user, resolved=False)
        .values("description", "category")
        .annotate(count=Count("id"))
        .filter(count__gte=2)
        .order_by("-count")[:limit]
    )
    return list(rows)


def get_improvement_snapshot(user) -> dict[str, Any]:
    """Compare recent vs prior window for assessments, study, and tasks."""
    now = timezone.now()
    week_ago = now - timedelta(days=7)
    two_weeks = now - timedelta(days=14)
    today = date.today()
    week_start = today - timedelta(days=today.weekday())

    recent_assess = Assessment.objects.filter(
        user=user, completed_at__gte=week_ago
    ).aggregate(avg=Avg("percentage"), count=Count("id"))
    prior_assess = Assessment.objects.filter(
        user=user, completed_at__gte=two_weeks, completed_at__lt=week_ago
    ).aggregate(avg=Avg("percentage"), count=Count("id"))

    study_recent = StudySession.objects.filter(
        user=user, ended_at__isnull=False, started_at__gte=week_ago
    ).aggregate(total=Sum("duration_minutes"))["total"] or 0
    study_prior = StudySession.objects.filter(
        user=user,
        ended_at__isnull=False,
        started_at__gte=two_weeks,
        started_at__lt=week_ago,
    ).aggregate(total=Sum("duration_minutes"))["total"] or 0

    tasks_recent = Task.objects.filter(
        completed=True, completed_at__gte=week_ago
    ).count()
    tasks_prior = Task.objects.filter(
        completed=True,
        completed_at__gte=two_weeks,
        completed_at__lt=week_ago,
    ).count()

    assess_delta = None
    if recent_assess["avg"] and prior_assess["avg"]:
        assess_delta = round(recent_assess["avg"] - prior_assess["avg"], 1)

    study_delta = study_recent - study_prior
    task_delta = tasks_recent - tasks_prior

    signals = []
    if assess_delta is not None and assess_delta > 0:
        signals.append(f"Assessment scores up {assess_delta}% vs last week")
    if study_delta > 30:
        signals.append(f"Study time up {study_delta} min vs last week")
    if task_delta > 0:
        signals.append(f"{task_delta} more tasks completed than last week")

    profile = get_or_create_profile(user)
    is_improving = bool(signals) or profile.current_streak >= 3

    return {
        "is_improving": is_improving,
        "signals": signals,
        "assessment_avg_recent": round(recent_assess["avg"] or 0, 1),
        "assessment_avg_prior": round(prior_assess["avg"] or 0, 1),
        "assessment_delta": assess_delta,
        "study_minutes_recent": study_recent,
        "study_minutes_prior": study_prior,
        "tasks_recent": tasks_recent,
        "tasks_prior": tasks_prior,
        "streak": profile.current_streak,
    }


SKILL_PRACTICE_SLUG: dict[str, str] = {
    "python": "python",
    "algorithms-data-structures": "dsa",
    "django": "django",
    "postgresql": "postgresql",
    "system-design": "system-design",
    "testing": "testing",
    "aws": "cloud",
    "redis": "devops",
}


def get_coaching_briefing(user) -> dict[str, Any]:
    """Answer the seven daily coaching questions in one structured briefing."""
    progress = calculate_progress(user)
    training_day = get_today_training_day(user)
    recommendations = get_daily_recommendations(user)
    weaknesses = get_top_weaknesses(user, limit=3)
    repeated = get_repeated_mistakes(user)
    improving = get_improvement_snapshot(user)

    today_tasks = []
    if training_day:
        for task in training_day.tasks.filter(completed=False, skipped=False).select_related(
            "skill"
        )[:6]:
            today_tasks.append({
                "id": task.id,
                "title": task.title,
                "minutes": task.estimated_minutes,
                "type": task.task_type,
                "skill": task.skill.name if task.skill else "",
            })

    primary_rec = recommendations[0] if recommendations else None
    phase_name = ""
    if training_day and training_day.week_id:
        phase_name = training_day.week.phase.name

    performance_summary = (
        f"{progress['completed_tasks']} tasks done · "
        f"{progress['study_hours']}h studied · "
        f"Day {progress['current_day']} of {progress['total_days']}"
    )

    recent_assess = Assessment.objects.filter(user=user).order_by("-completed_at").first()
    if recent_assess:
        performance_summary += f" · Last assessment {recent_assess.percentage}%"

    next_actions = []
    from django.urls import reverse

    for rec in recommendations[:4]:
        action = {
            "title": rec["title"],
            "reason": rec["reason"],
            "minutes": rec.get("minutes"),
            "priority": rec["priority"],
            "type": rec.get("type"),
            "url": None,
        }
        if rec.get("type") == "resource" and rec.get("url"):
            action["url"] = rec["url"]
            action["external"] = True
        elif rec.get("task_id"):
            action["url"] = reverse("today")
        elif rec.get("type") == "weakness":
            slug = rec.get("skill_slug", "python")
            section = SKILL_PRACTICE_SLUG.get(slug, "python")
            action["url"] = reverse("practice_section", kwargs={"section_slug": section})
        elif rec.get("type") == "mistake":
            action["url"] = reverse("mistakes")
        elif rec.get("type") == "assessment":
            action["url"] = reverse("assessments")
        else:
            action["url"] = reverse("today")
        next_actions.append(action)

    return {
        "what_today": {
            "tasks": today_tasks,
            "primary": primary_rec,
            "mission_title": training_day.title if training_day else "Rest / review day",
            "target_minutes": training_day.target_minutes if training_day else 0,
        },
        "why": {
            "focus": training_day.focus if training_day else "",
            "objectives": training_day.objectives if training_day else "",
            "phase": phase_name,
            "day_number": progress["current_day"],
        },
        "performance": {
            "summary": performance_summary,
            "progress": progress,
            "recent_assessment": recent_assess,
        },
        "weaknesses": weaknesses,
        "repeated_mistakes": repeated,
        "improving": improving,
        "next_actions": next_actions,
    }


def get_due_review_cards(user) -> list:
    from training.models import ReviewCard

    return list(
        ReviewCard.objects.filter(user=user, next_review__lte=date.today())
        .select_related("skill")
        .order_by("next_review")[:20]
    )


def schedule_review_card(user, concept: str, content: str, skill=None) -> "ReviewCard":
    from training.models import ReviewCard

    return ReviewCard.objects.create(
        user=user,
        skill=skill,
        concept=concept,
        content=content,
        next_review=date.today(),
        interval_days=1,
    )


def process_review_quality(user, card_id, quality: int) -> dict[str, Any]:
    """SM-2 style interval update. Quality 0-5."""
    from training.models import ReviewCard

    card = ReviewCard.objects.get(id=card_id, user=user)
    q = max(0, min(5, quality))

    if q < 3:
        card.repetition = 0
        card.interval_days = 1
    else:
        if card.repetition == 0:
            card.interval_days = 1
        elif card.repetition == 1:
            card.interval_days = 3
        else:
            card.interval_days = max(1, int(card.interval_days * card.ease_factor))
        card.repetition += 1
        card.ease_factor = max(
            1.3, card.ease_factor + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        )

    card.next_review = date.today() + timedelta(days=card.interval_days)
    card.save()
    award_xp(user, 5)
    update_streak_on_activity(user)
    return {"card": card, "next_review": card.next_review}


def create_mistake_from_form(user, data: dict[str, Any]) -> Mistake:
    mistake = Mistake.objects.create(
        user=user,
        description=data["description"],
        category=data.get("category", "knowledge_gap"),
        severity=data.get("severity", "medium"),
        skill_id=data.get("skill_id") or None,
    )
    schedule_review_card(
        user,
        concept=data["description"][:200],
        content=f"Mistake to review: {data['description']}",
        skill=mistake.skill,
    )
    return mistake


def get_mock_interview_hub(user) -> dict[str, Any]:
    from training.models import MockInterviewRound, MockInterviewSession

    current_day = get_current_day_number(user)
    rounds = list(
        MockInterviewRound.objects.prefetch_related("questions").order_by("round_number")
    )
    sessions = MockInterviewSession.objects.filter(user=user).select_related("round")
    completed_ids = {
        s.round_id
        for s in sessions
        if s.status == MockInterviewSession.Status.COMPLETED
    }
    in_progress = {
        s.round_id: s
        for s in sessions
        if s.status == MockInterviewSession.Status.IN_PROGRESS
    }

    round_cards = []
    for rnd in rounds:
        round_cards.append(
            {
                "round": rnd,
                "unlocked": current_day >= rnd.unlock_day,
                "completed": rnd.id in completed_ids,
                "in_progress_session": in_progress.get(rnd.id),
                "is_current_period": rnd.unlock_day <= current_day <= rnd.period_end_day,
                "question_count": rnd.questions.count(),
            }
        )

    recent_sessions = sessions.filter(
        status=MockInterviewSession.Status.COMPLETED
    ).order_by("-completed_at")[:6]

    return {
        "round_cards": round_cards,
        "current_day": current_day,
        "recent_sessions": recent_sessions,
    }


def start_mock_session(user, round_id) -> tuple[Any, str | None]:
    from training.models import MockInterviewRound, MockInterviewSession

    try:
        rnd = MockInterviewRound.objects.prefetch_related("questions").get(id=round_id)
    except MockInterviewRound.DoesNotExist:
        return None, "not_found"
    current_day = get_current_day_number(user)
    if current_day < rnd.unlock_day:
        return None, "not_unlocked"

    existing = MockInterviewSession.objects.filter(
        user=user,
        round=rnd,
        status=MockInterviewSession.Status.IN_PROGRESS,
    ).first()
    if existing:
        return existing, None

    q_count = rnd.questions.count()
    session = MockInterviewSession.objects.create(
        user=user,
        round=rnd,
        started_at=timezone.now(),
        question_started_at=timezone.now(),
        max_score=float(q_count * 10),
    )
    return session, None


def get_mock_session_state(session) -> dict[str, Any]:
    from training.models import MockInterviewSession

    total = session.round.questions.count()
    question = session.round.questions.filter(order=session.current_order).first()
    responses = list(
        session.responses.select_related("question").order_by("order")
    )
    structure = list(session.round.questions.order_by("order"))
    return {
        "session": session,
        "question": question,
        "total_questions": total,
        "responses": responses,
        "structure": structure,
        "progress_pct": round(
            (session.current_order - 1) / total * 100, 1
        ) if total else 0,
        "is_complete": session.status == MockInterviewSession.Status.COMPLETED,
    }


def submit_mock_response(
    user,
    session_id,
    answer: str,
    score: float,
    confidence: float,
    time_spent_seconds: int,
) -> dict[str, Any]:
    from training.code_runner import score_from_full_suite
    from training.models import MockInterviewResponse, MockInterviewSession

    session = MockInterviewSession.objects.select_related("round").get(
        id=session_id, user=user
    )
    if session.status == MockInterviewSession.Status.COMPLETED:
        return {"session": session, "completed": True}

    question = session.round.questions.filter(order=session.current_order).first()
    if not question:
        return {"session": session, "completed": True}

    tests_passed = None
    tests_total = None
    auto_scored = False
    final_score = float(score)

    if question.is_runnable:
        run = score_from_full_suite(
            answer, question.function_name, question.test_cases or []
        )
        tests_passed = run["passed"]
        tests_total = run["total"]
        auto_scored = True
        final_score = float(run["score"])

    MockInterviewResponse.objects.update_or_create(
        session=session,
        order=session.current_order,
        defaults={
            "question": question,
            "answer": answer,
            "score": final_score,
            "confidence": confidence,
            "time_spent_seconds": time_spent_seconds,
            "tests_passed": tests_passed,
            "tests_total": tests_total,
            "auto_scored": auto_scored,
        },
    )
    session.total_score += final_score

    total = session.round.questions.count()
    if session.current_order >= total:
        session.status = MockInterviewSession.Status.COMPLETED
        session.completed_at = timezone.now()
        session.save()

        pct = round((session.total_score / session.max_score) * 100, 1) if session.max_score else 0
        Assessment.objects.create(
            user=user,
            name=f"Mock Interview {session.round.round_number}: {session.round.title}",
            category="mock_interview",
            score=session.total_score,
            maximum_score=session.max_score,
            percentage=pct,
            duration_minutes=max(
                1,
                int((session.completed_at - session.started_at).total_seconds() / 60),
            ),
            completed_at=session.completed_at,
            notes=f"Bi-weekly mock round {session.round.round_number}",
        )
        award_xp(user, 50)
        update_streak_on_activity(user)
        return {"session": session, "completed": True, "score": final_score}

    session.current_order += 1
    session.question_started_at = timezone.now()
    session.save()
    return {"session": session, "completed": False, "score": final_score}


def run_mock_coding_tests(
    user, session_id, code: str, custom_cases: list | None = None
) -> dict[str, Any]:
    """Run public (+ optional custom) tests for the current coding question."""
    from training.code_runner import merge_run_cases, run_coding_tests
    from training.models import MockInterviewSession

    session = MockInterviewSession.objects.select_related("round").get(
        id=session_id, user=user
    )
    if session.status == MockInterviewSession.Status.COMPLETED:
        return {"ok": False, "error": "Session already completed.", "results": [], "status": "empty"}

    question = session.round.questions.filter(order=session.current_order).first()
    if not question or not question.is_runnable:
        return {
            "ok": False,
            "error": "Current question is not a runnable coding problem.",
            "results": [],
            "status": "empty",
        }

    cases = merge_run_cases(
        question.test_cases or [],
        custom_cases or [],
        include_hidden=False,
    )
    return run_coding_tests(
        code,
        question.function_name,
        cases,
        include_hidden=True,
    )


def get_mock_results_breakdown(session) -> dict[str, Any]:
    responses = list(
        session.responses.select_related("question").order_by("order")
    )
    by_difficulty: dict[str, dict[str, Any]] = {}
    for resp in responses:
        diff = resp.question.difficulty
        bucket = by_difficulty.setdefault(
            diff, {"total_score": 0.0, "max_score": 0.0, "count": 0, "items": []}
        )
        bucket["total_score"] += resp.score or 0
        bucket["max_score"] += 10
        bucket["count"] += 1
        bucket["items"].append(resp)

    summary = []
    for diff in ["easy", "medium", "hard", "expert"]:
        if diff in by_difficulty:
            b = by_difficulty[diff]
            pct = round(b["total_score"] / b["max_score"] * 100, 1) if b["max_score"] else 0
            summary.append(
                {
                    "difficulty": diff,
                    "label": "Hardest" if diff == "expert" else diff.capitalize(),
                    "score": b["total_score"],
                    "max_score": b["max_score"],
                    "percent": pct,
                    "count": b["count"],
                }
            )

    pct = round(
        (session.total_score / session.max_score) * 100, 1
    ) if session.max_score else 0

    return {
        "session": session,
        "responses": responses,
        "by_difficulty": summary,
        "percent": pct,
    }


COGNITIVE_TYPE_SLUGS = {
    "aptitude": "aptitude",
    "brain-teasers": "brain_teaser",
}


def get_cognitive_hub(user) -> dict[str, Any]:
    from training.cognitive_bank import COGNITIVE_COUNTS
    from training.models import CognitiveProgress, CognitiveQuestion

    revealed = CognitiveProgress.objects.filter(user=user, revealed=True).count()
    aptitude_revealed = CognitiveProgress.objects.filter(
        user=user, revealed=True, question__challenge_type="aptitude"
    ).count()
    teaser_revealed = CognitiveProgress.objects.filter(
        user=user, revealed=True, question__challenge_type="brain_teaser"
    ).count()
    return {
        "counts": COGNITIVE_COUNTS,
        "revealed_total": revealed,
        "aptitude_revealed": aptitude_revealed,
        "teaser_revealed": teaser_revealed,
        "aptitude_categories": (
            CognitiveQuestion.objects.filter(challenge_type="aptitude")
            .values("category")
            .annotate(count=Count("id"))
            .order_by("category")
        ),
        "teaser_categories": (
            CognitiveQuestion.objects.filter(challenge_type="brain_teaser")
            .values("category")
            .annotate(count=Count("id"))
            .order_by("category")
        ),
    }


def get_cognitive_list_data(
    user, challenge_type: str, category: str | None = None, difficulty: str | None = None
) -> dict[str, Any]:
    from training.models import CognitiveProgress, CognitiveQuestion

    qs = CognitiveQuestion.objects.filter(challenge_type=challenge_type)
    if category:
        qs = qs.filter(category=category)
    if difficulty:
        qs = qs.filter(difficulty=difficulty)

    revealed_ids = set(
        CognitiveProgress.objects.filter(user=user, revealed=True).values_list(
            "question_id", flat=True
        )
    )
    questions = list(qs.order_by("order"))
    for q in questions:
        q.is_revealed = q.id in revealed_ids

    categories = (
        CognitiveQuestion.objects.filter(challenge_type=challenge_type)
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    return {
        "questions": questions,
        "challenge_type": challenge_type,
        "category_filter": category,
        "difficulty_filter": difficulty,
        "categories": categories,
        "revealed_count": sum(1 for q in questions if q.is_revealed),
    }


def get_cognitive_question_data(user, question_id) -> dict[str, Any]:
    from training.models import CognitiveProgress, CognitiveQuestion

    question = CognitiveQuestion.objects.get(id=question_id)
    progress, _ = CognitiveProgress.objects.get_or_create(
        user=user, question=question
    )
    prev_q = (
        CognitiveQuestion.objects.filter(
            challenge_type=question.challenge_type, order__lt=question.order
        )
        .order_by("-order")
        .first()
    )
    next_q = (
        CognitiveQuestion.objects.filter(
            challenge_type=question.challenge_type, order__gt=question.order
        )
        .order_by("order")
        .first()
    )
    choices = question.choices if isinstance(question.choices, list) else []
    is_correct = None
    if progress.revealed and progress.attempted_answer and choices:
        attempt = progress.attempted_answer.strip().upper()
        correct = (question.answer or "").strip().upper()
        is_correct = attempt == correct
    return {
        "question": question,
        "progress": progress,
        "prev_question": prev_q,
        "next_question": next_q,
        "choices": choices,
        "is_multiple_choice": bool(choices),
        "is_correct": is_correct,
    }


def reveal_cognitive_answer(
    user, question_id, attempted_answer: str = "", notes: str = "", time_spent_seconds: int = 0
) -> dict[str, Any]:
    from training.models import CognitiveProgress, CognitiveQuestion

    question = CognitiveQuestion.objects.get(id=question_id)
    progress, _ = CognitiveProgress.objects.get_or_create(
        user=user, question=question
    )
    progress.revealed = True
    progress.revealed_at = timezone.now()
    if attempted_answer:
        progress.attempted_answer = attempted_answer.strip()
    if notes:
        progress.notes = notes
    if time_spent_seconds > 0:
        progress.time_spent_seconds = min(time_spent_seconds, 3600)
    progress.save()
    update_streak_on_activity(user)
    award_xp(user, 3)

    choices = question.choices if isinstance(question.choices, list) else []
    attempt = (progress.attempted_answer or "").strip().upper()
    correct = (question.answer or "").strip().upper()
    # Accept "A" or full choice text match
    is_correct = False
    if attempt and correct:
        if attempt == correct or attempt.startswith(correct + " ") or correct.startswith(attempt):
            is_correct = True
        else:
            for c in choices:
                key = str(c.get("key", "")).upper()
                text = str(c.get("text", "")).strip()
                if key == correct and (attempt == key or attempt == text.upper()):
                    is_correct = True
                    break
                if key == attempt and key == correct:
                    is_correct = True
                    break

    return {
        "question": question,
        "progress": progress,
        "choices": choices,
        "is_multiple_choice": bool(choices),
        "is_correct": is_correct if attempt else None,
    }
