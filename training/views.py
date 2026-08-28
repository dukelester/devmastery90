"""Views for DevMastery 90."""
from datetime import date

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from training.models import (
    CodingProblem,
    DailyReview,
    InterviewAttempt,
    InterviewQuestion,
    StudySession,
    Task,
    TrainingDay,
    WeeklyReview,
)
from training.services import (
    award_xp,
    calculate_progress,
    calculate_streak,
    get_analytics_data,
    get_coding_stats,
    get_daily_recommendations,
    get_interview_stats,
    get_or_create_profile,
    get_skill_scores,
    get_today_training_day,
    get_top_weaknesses,
    get_training_day,
    update_streak_on_activity,
    update_training_day_completion,
)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        profile = get_or_create_profile(request.user)
        if not profile.program_start_date:
            profile.program_start_date = date.today()
            profile.save()
        return redirect("dashboard")
    return render(request, "registration/login.html", {"form": form})


def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        profile = get_or_create_profile(user)
        profile.program_start_date = date.today()
        profile.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    progress = calculate_progress(request.user)
    training_day = get_today_training_day(request.user)
    today_tasks = []
    completed_today = []
    tomorrow_day = None
    tomorrow_tasks = []
    day_complete = False

    if training_day:
        all_tasks = list(training_day.tasks.select_related("skill").order_by("order"))
        today_tasks = [t for t in all_tasks if not t.completed and not t.skipped][:8]
        completed_today = [t for t in all_tasks if t.completed]
        open_count = len([t for t in all_tasks if not t.completed and not t.skipped])
        day_complete = open_count == 0 and len(all_tasks) > 0

        if day_complete or not today_tasks:
            from training.services import get_training_day

            tomorrow_day = get_training_day(progress["current_day"] + 1)
            if tomorrow_day:
                tomorrow_tasks = list(
                    tomorrow_day.tasks.filter(completed=False, skipped=False)
                    .select_related("skill")
                    .order_by("order")[:5]
                )

    context = {
        "progress": progress,
        "training_day": training_day,
        "today_tasks": today_tasks,
        "completed_today": completed_today,
        "day_complete": day_complete,
        "tomorrow_day": tomorrow_day,
        "tomorrow_tasks": tomorrow_tasks,
        "weaknesses": get_top_weaknesses(request.user),
        "recommendations": get_daily_recommendations(request.user),
        "skill_scores": get_skill_scores(request.user),
        "recent_assessments": request.user.assessments.all()[:5],
    }
    if request.htmx:
        partial = request.GET.get("partial")
        if partial == "stats":
            return render(request, "dashboard/_stats.html", context)
        if partial == "tasks":
            return render(request, "dashboard/_today_tasks.html", context)
        if partial == "skills":
            return render(request, "dashboard/_skill_progress.html", context)
        if partial == "recommendations":
            return render(request, "dashboard/_recommendations.html", context)
    return render(request, "dashboard/index.html", context)


@login_required
def today_view(request: HttpRequest) -> HttpResponse:
    progress = calculate_progress(request.user)
    training_day = get_today_training_day(request.user)
    from django.db.models import Sum

    active_session = StudySession.objects.filter(
        user=request.user, is_active=True
    ).select_related("task", "skill").first()

    daily_total = StudySession.objects.filter(
        user=request.user,
        started_at__date=date.today(),
        ended_at__isnull=False,
    ).aggregate(total=Sum("duration_minutes"))["total"] or 0

    context = {
        "progress": progress,
        "training_day": training_day,
        "tasks": training_day.tasks.select_related("skill").all() if training_day else [],
        "active_session": active_session,
        "daily_total_minutes": daily_total,
    }
    return render(request, "today/index.html", context)


@login_required
@require_POST
def task_complete(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.completed_at = timezone.now()
    task.save()
    update_training_day_completion(task.training_day)
    award_xp(request.user, 10)
    update_streak_on_activity(request.user)
    if request.htmx:
        return render(request, "tasks/_task.html", {"task": task})
    return redirect("today")


@login_required
@require_POST
def task_skip(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    task.skipped = True
    task.skip_reason = request.POST.get("reason", "")
    task.save()
    if request.htmx:
        return render(request, "tasks/_task.html", {"task": task})
    return redirect("today")


@login_required
@require_POST
def task_block(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    task.blocked = True
    task.blocked_reason = request.POST.get("reason", "")
    task.save()
    if request.htmx:
        return render(request, "tasks/_task.html", {"task": task})
    return redirect("today")


@login_required
@require_POST
def task_notes(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    task.notes = request.POST.get("notes", "")
    task.save()
    if request.htmx:
        return render(request, "tasks/_task.html", {"task": task})
    return redirect("today")


@login_required
def timer_view(request: HttpRequest) -> HttpResponse:
    active = StudySession.objects.filter(
        user=request.user, is_active=True
    ).select_related("task", "skill").first()
    return render(request, "study/_timer.html", {"active_session": active})


@login_required
@require_POST
def timer_start(request: HttpRequest) -> HttpResponse:
    StudySession.objects.filter(user=request.user, is_active=True).update(
        is_active=False, ended_at=timezone.now()
    )
    task_id = request.POST.get("task_id")
    skill_id = request.POST.get("skill_id")
    session = StudySession.objects.create(
        user=request.user,
        task_id=task_id or None,
        skill_id=skill_id or None,
        started_at=timezone.now(),
        is_active=True,
    )
    return render(request, "study/_timer.html", {"active_session": session})


@login_required
@require_POST
def timer_stop(request: HttpRequest) -> HttpResponse:
    session = StudySession.objects.filter(user=request.user, is_active=True).first()
    if session:
        session.ended_at = timezone.now()
        session.is_active = False
        delta = session.ended_at - session.started_at
        session.duration_minutes = max(1, int(delta.total_seconds() / 60))
        session.save()
        profile = get_or_create_profile(request.user)
        profile.total_study_minutes += session.duration_minutes
        profile.save()
        update_streak_on_activity(request.user)
    return render(request, "study/_timer.html", {"active_session": None})


@login_required
def coding_view(request: HttpRequest) -> HttpResponse:
    stats = get_coding_stats(request.user)
    return render(request, "coding/index.html", stats)


@login_required
@require_POST
def coding_create(request: HttpRequest) -> HttpResponse:
    problem = CodingProblem.objects.create(
        user=request.user,
        title=request.POST.get("title", ""),
        platform=request.POST.get("platform", ""),
        url=request.POST.get("url", ""),
        difficulty=request.POST.get("difficulty", "medium"),
        category=request.POST.get("category", ""),
    )
    if request.htmx:
        return render(request, "coding/_problem.html", {"problem": problem})
    return redirect("coding")


@login_required
@require_POST
def coding_solve(request: HttpRequest, problem_id: int) -> HttpResponse:
    problem = get_object_or_404(CodingProblem, id=problem_id, user=request.user)
    problem.solved = True
    problem.solved_at = timezone.now()
    problem.attempts += 1
    problem.time_taken = int(request.POST.get("time_taken", 0)) or None
    problem.confidence = float(request.POST.get("confidence", 5))
    problem.notes = request.POST.get("notes", "")
    problem.save()
    award_xp(request.user, 25)
    if request.htmx:
        return render(request, "coding/_problem.html", {"problem": problem})
    return redirect("coding")


@login_required
def interview_view(request: HttpRequest) -> HttpResponse:
    stats = get_interview_stats(request.user)
    return render(request, "interview/index.html", stats)


@login_required
@require_POST
def interview_attempt(request: HttpRequest, question_id: int) -> HttpResponse:
    question = get_object_or_404(InterviewQuestion, id=question_id)
    attempt = InterviewAttempt.objects.create(
        user=request.user,
        question=question,
        answer=request.POST.get("answer", ""),
        confidence=float(request.POST.get("confidence", 5)),
        score=float(request.POST.get("score", 0)),
        notes=request.POST.get("notes", ""),
        needs_review=request.POST.get("needs_review") == "on",
    )
    if request.htmx:
        return render(request, "interview/_attempt.html", {"attempt": attempt})
    return redirect("interview")


@login_required
def analytics_view(request: HttpRequest) -> HttpResponse:
    data = get_analytics_data(request.user)
    return render(request, "analytics/index.html", data)


@login_required
def calendar_view(request: HttpRequest) -> HttpResponse:
    days = TrainingDay.objects.select_related("week").order_by("day_number")
    current = calculate_progress(request.user)["current_day"]
    return render(request, "calendar/index.html", {"days": days, "current_day": current})


@login_required
def calendar_day_detail(request: HttpRequest, day_number: int) -> HttpResponse:
    day = get_object_or_404(TrainingDay.objects.prefetch_related("tasks"), day_number=day_number)
    return render(request, "calendar/_day_detail.html", {"day": day})


@login_required
def weekly_review_view(request: HttpRequest, week_number: int) -> HttpResponse:
    from training.models import Week
    from django.db.models import Sum, Count

    week = get_object_or_404(Week, week_number=week_number)
    days = week.days.prefetch_related("tasks")
    tasks_total = Task.objects.filter(training_day__week=week).count()
    tasks_completed = Task.objects.filter(training_day__week=week, completed=True).count()
    study_minutes = StudySession.objects.filter(
        user=request.user,
        started_at__date__gte=week.start_date,
        started_at__date__lte=week.end_date,
        ended_at__isnull=False,
    ).aggregate(total=Sum("duration_minutes"))["total"] or 0

    skills = get_skill_scores(request.user)
    strongest = max(skills, key=lambda s: s["score"]) if skills else None
    weakest = min(skills, key=lambda s: s["score"]) if skills else None

    review, _ = WeeklyReview.objects.get_or_create(user=request.user, week=week)
    context = {
        "week": week,
        "tasks_completed": tasks_completed,
        "tasks_total": tasks_total,
        "study_minutes": study_minutes,
        "strongest": strongest,
        "weakest": weakest,
        "review": review,
    }
    if request.method == "POST":
        review.learned = request.POST.get("learned", "")
        review.difficult = request.POST.get("difficult", "")
        review.went_well = request.POST.get("went_well", "")
        review.improve = request.POST.get("improve", "")
        review.next_week_focus = request.POST.get("next_week_focus", "")
        review.tasks_completed = tasks_completed
        review.tasks_total = tasks_total
        review.study_minutes = study_minutes
        review.save()
        messages.success(request, "Weekly review saved.")
        return redirect("weekly_review", week_number=week_number)
    return render(request, "weekly_review/index.html", context)


@login_required
@require_POST
def daily_review_submit(request: HttpRequest) -> HttpResponse:
    training_day = get_today_training_day(request.user)
    if not training_day:
        return HttpResponse(status=400)
    review, _ = DailyReview.objects.update_or_create(
        user=request.user,
        training_day=training_day,
        defaults={
            "wins": request.POST.get("wins", ""),
            "challenges": request.POST.get("challenges", ""),
            "lessons": request.POST.get("lessons", ""),
            "tomorrow_focus": request.POST.get("tomorrow_focus", ""),
            "confidence_score": float(request.POST.get("confidence_score", 5)),
        },
    )
    return render(request, "today/_daily_review.html", {"review": review})
