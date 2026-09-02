"""Views for DevMastery 90."""
from datetime import date
from uuid import UUID

from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.contrib.staticfiles import finders
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from training.models import (
    Assessment,
    CareerGoal,
    CodingProblem,
    DailyReview,
    EngineeringChallenge,
    EngineeringAttempt,
    EngineeringLabSession,
    InterviewAttempt,
    InterviewQuestion,
    JobApplication,
    Mistake,
    CognitiveQuestion,
    CognitiveProgress,
    MockInterviewRound,
    MockInterviewSession,
    Project,
    ProjectProgress,
    ReviewCard,
    Skill,
    StudySession,
    Task,
    TrainingDay,
    WeeklyReview,
)
from training.services import (
    award_xp,
    calculate_progress,
    calculate_streak,
    create_mistake_from_form,
    get_analytics_data,
    get_coaching_briefing,
    get_coding_stats,
    get_daily_recommendations,
    get_day_resources,
    get_due_review_cards,
    get_interview_stats,
    get_practice_hub_data,
    get_practice_section_data,
    can_access_practice_question,
    submit_practice_attempt,
    get_or_create_profile,
    get_skill_scores,
    get_mock_interview_hub,
    start_mock_session,
    get_mock_session_state,
    submit_mock_response,
    get_mock_results_breakdown,
    run_mock_coding_tests,
    get_cognitive_hub,
    get_cognitive_list_data,
    get_cognitive_question_data,
    reveal_cognitive_answer,
    COGNITIVE_TYPE_SLUGS,
    get_today_training_day,
    get_top_weaknesses,
    get_training_day,
    needs_onboarding,
    process_review_quality,
    update_streak_on_activity,
    update_training_day_completion,
)
from training.forms import (
    DevMasteryAuthenticationForm,
    DevMasteryPasswordChangeForm,
    DevMasteryUserCreationForm,
    ProfileDetailsForm,
    UserAccountForm,
)


@require_GET
@never_cache
def service_worker(request: HttpRequest) -> HttpResponse:
    """Serve the PWA service worker from the site root so scope covers `/`."""
    path = finders.find("js/sw.js")
    if not path:
        return HttpResponseNotFound("service worker missing")
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    response = HttpResponse(body, content_type="application/javascript; charset=utf-8")
    response["Service-Worker-Allowed"] = "/"
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = DevMasteryAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        get_or_create_profile(request.user)
        if needs_onboarding(request.user):
            return redirect("onboarding")
        return redirect("dashboard")
    return render(request, "registration/login.html", {"form": form})


def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = DevMasteryUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        get_or_create_profile(user)
        login(request, user)
        return redirect("onboarding")
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile_view(request: HttpRequest) -> HttpResponse:
    profile = get_or_create_profile(request.user)
    progress = calculate_progress(request.user)
    tab = request.GET.get("tab", "profile")

    account_form = UserAccountForm(instance=request.user)
    profile_form = ProfileDetailsForm(instance=profile)
    password_form = DevMasteryPasswordChangeForm(request.user)

    if request.method == "POST":
        action = request.POST.get("action", "profile")
        if action == "profile":
            account_form = UserAccountForm(request.POST, instance=request.user)
            profile_form = ProfileDetailsForm(request.POST, instance=profile)
            if account_form.is_valid() and profile_form.is_valid():
                account_form.save()
                profile_form.save()
                messages.success(request, "Profile updated.")
                return redirect("profile")
            tab = "profile"
        elif action == "password":
            password_form = DevMasteryPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated.")
                return redirect(reverse("profile") + "?tab=security")
            tab = "security"

    return render(
        request,
        "profile/index.html",
        {
            "profile": profile,
            "progress": progress,
            "tab": tab,
            "account_form": account_form,
            "profile_form": profile_form,
            "password_form": password_form,
        },
    )


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    if needs_onboarding(request.user):
        return redirect("onboarding")

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
        "recent_assessments": request.user.assessments.all()[:5],
        "coaching": get_coaching_briefing(request.user),
        "focus_recommendations": [
            r for r in get_daily_recommendations(request.user)
            if r.get("type") not in ("scheduled", "workload")
        ][:4],
        "weakest_skills": sorted(get_skill_scores(request.user), key=lambda s: s["score"])[:6],
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
        "day_resources": get_day_resources(progress["current_day"]) if training_day else [],
    }
    return render(request, "today/index.html", context)


@login_required
@require_POST
def task_complete(request: HttpRequest, task_id: UUID) -> HttpResponse:
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
def task_skip(request: HttpRequest, task_id: UUID) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    task.skipped = True
    task.skip_reason = request.POST.get("reason", "")
    task.save()
    if request.htmx:
        return render(request, "tasks/_task.html", {"task": task})
    return redirect("today")


@login_required
@require_POST
def task_block(request: HttpRequest, task_id: UUID) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)
    task.blocked = True
    task.blocked_reason = request.POST.get("reason", "")
    task.save()
    if request.htmx:
        return render(request, "tasks/_task.html", {"task": task})
    return redirect("today")


@login_required
@require_POST
def task_notes(request: HttpRequest, task_id: UUID) -> HttpResponse:
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


def _stop_active_sessions(user) -> None:
    for session in StudySession.objects.filter(user=user, is_active=True):
        session.ended_at = timezone.now()
        session.is_active = False
        delta = session.ended_at - session.started_at
        session.duration_minutes = max(1, int(delta.total_seconds() / 60))
        session.save()


@login_required
@require_POST
def timer_start(request: HttpRequest) -> HttpResponse:
    _stop_active_sessions(request.user)
    task_id = request.POST.get("task_id")
    skill_id = request.POST.get("skill_id")
    mode = request.POST.get("mode", "elapsed")
    task = None
    target_minutes = None
    if task_id:
        task = Task.objects.filter(id=task_id).select_related("skill").first()
        if task and mode == "focus":
            target_minutes = task.estimated_minutes
    session = StudySession.objects.create(
        user=request.user,
        task=task,
        skill_id=skill_id or (task.skill_id if task else None),
        started_at=timezone.now(),
        is_active=True,
        mode="focus" if mode == "focus" else "elapsed",
        target_minutes=target_minutes,
    )
    if request.POST.get("redirect") == "focus":
        return redirect("focus_mode")
    session = StudySession.objects.select_related("task", "skill").get(pk=session.pk)
    return render(request, "study/_timer.html", {"active_session": session})


@login_required
@require_POST
def focus_start(request: HttpRequest, task_id: UUID) -> HttpResponse:
    task = get_object_or_404(Task.objects.select_related("skill"), id=task_id)
    _stop_active_sessions(request.user)
    StudySession.objects.create(
        user=request.user,
        task=task,
        skill=task.skill,
        started_at=timezone.now(),
        is_active=True,
        mode="focus",
        target_minutes=task.estimated_minutes,
    )
    return redirect("focus_mode")


@login_required
def focus_mode_view(request: HttpRequest) -> HttpResponse:
    session = (
        StudySession.objects.filter(user=request.user, is_active=True, mode="focus")
        .select_related("task", "skill")
        .first()
    )
    if not session:
        return redirect("today")
    return render(request, "study/focus.html", {"session": session})


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
    redirect_target = request.POST.get("redirect")
    if redirect_target == "today":
        return redirect("today")
    if redirect_target == "focus":
        return redirect("focus_mode")
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
def coding_solve(request: HttpRequest, problem_id: UUID) -> HttpResponse:
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
    data = get_practice_hub_data(request.user)
    return render(request, "practice/index.html", data)


@login_required
def practice_section(request: HttpRequest, section_slug: str) -> HttpResponse:
    data = get_practice_section_data(request.user, section_slug)
    if not data:
        return redirect("interview")
    return render(request, "practice/section.html", data)


@login_required
def practice_question(request: HttpRequest, section_slug: str, question_id: UUID) -> HttpResponse:
    question = get_object_or_404(
        InterviewQuestion.objects.filter(section_slug=section_slug),
        id=question_id,
    )
    if not can_access_practice_question(request.user, question):
        return render(
            request,
            "practice/_locked.html",
            {"question": question, "section_slug": section_slug},
            status=403,
        )
    section_data = get_practice_section_data(request.user, section_slug)
    return render(
        request,
        "practice/question.html",
        {
            "question": question,
            "section": section_data.get("section"),
            "progress": section_data.get("progress"),
            "unlocked_order": section_data.get("unlocked_order"),
        },
    )


@login_required
@require_POST
def practice_submit(request: HttpRequest, section_slug: str, question_id: UUID) -> HttpResponse:
    question = get_object_or_404(
        InterviewQuestion.objects.filter(section_slug=section_slug),
        id=question_id,
    )
    result = submit_practice_attempt(
        request.user,
        question,
        {
            "answer": request.POST.get("answer", ""),
            "score": request.POST.get("score", 0),
            "confidence": request.POST.get("confidence", 5),
            "notes": request.POST.get("notes", ""),
            "needs_review": request.POST.get("needs_review") == "on",
        },
    )
    if result.get("error") and not result.get("passed"):
        if request.htmx:
            return render(
                request,
                "practice/_submit_error.html",
                {"error": result["error"], "question": question},
                status=403,
            )
        messages.error(request, result["error"])
        return redirect("practice_question", section_slug=section_slug, question_id=question_id)

    if request.htmx:
        return render(
            request,
            "practice/_submit_result.html",
            {
                "attempt": result["attempt"],
                "question": question,
                "passed": result["passed"],
                "unlocked_order": result["unlocked_order"],
                "section_slug": section_slug,
            },
        )
    return redirect("practice_section", section_slug=section_slug)


@login_required
@require_POST
def interview_attempt(request: HttpRequest, question_id: UUID) -> HttpResponse:
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
def calendar_day_detail(request: HttpRequest, day_id: UUID) -> HttpResponse:
    day = get_object_or_404(TrainingDay.objects.prefetch_related("tasks"), id=day_id)
    return render(request, "calendar/_day_detail.html", {"day": day})


@login_required
@login_required
def weekly_review_view(request: HttpRequest, week_id: UUID) -> HttpResponse:
    from training.models import Week
    from django.db.models import Sum

    week = get_object_or_404(Week, id=week_id)
    days = week.days.prefetch_related("tasks")
    tasks_total = Task.objects.filter(training_day__week=week).count()
    tasks_completed = Task.objects.filter(training_day__week=week, completed=True).count()
    study_minutes = 0
    if week.start_date and week.end_date:
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
        return redirect("weekly_review", week_id=week.id)
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


@login_required
def onboarding_view(request: HttpRequest) -> HttpResponse:
    profile = get_or_create_profile(request.user)
    if request.method == "POST":
        start = request.POST.get("program_start_date")
        if start:
            profile.program_start_date = date.fromisoformat(start)
            profile.save()
            messages.success(request, "Your 90-day program is initialized.")
            return redirect("dashboard")
    return render(
        request,
        "onboarding/index.html",
        {"profile": profile, "today": date.today()},
    )


@login_required
def mistakes_view(request: HttpRequest) -> HttpResponse:
    mistakes = Mistake.objects.filter(user=request.user).select_related("skill")[:50]
    repeated = (
        Mistake.objects.filter(user=request.user, resolved=False)
        .values("description", "category")
        .annotate(count=Count("id"))
        .filter(count__gte=2)
        .order_by("-count")
    )
    skills = Skill.objects.all()
    if request.method == "POST":
        create_mistake_from_form(
            request.user,
            {
                "description": request.POST.get("description", ""),
                "category": request.POST.get("category", "knowledge_gap"),
                "severity": request.POST.get("severity", "medium"),
                "skill_id": request.POST.get("skill_id"),
            },
        )
        if request.htmx:
            mistakes = Mistake.objects.filter(user=request.user).select_related("skill")[:50]
            return render(request, "mistakes/_list.html", {"mistakes": mistakes})
        return redirect("mistakes")
    return render(
        request,
        "mistakes/index.html",
        {"mistakes": mistakes, "repeated": repeated, "skills": skills},
    )


@login_required
@require_POST
def mistake_resolve(request: HttpRequest, mistake_id: UUID) -> HttpResponse:
    mistake = get_object_or_404(Mistake, id=mistake_id, user=request.user)
    mistake.resolved = True
    mistake.resolution_notes = request.POST.get("notes", "")
    mistake.save()
    mistakes = Mistake.objects.filter(user=request.user).select_related("skill")[:50]
    return render(request, "mistakes/_list.html", {"mistakes": mistakes})


@login_required
def review_view(request: HttpRequest) -> HttpResponse:
    due_cards = get_due_review_cards(request.user)
    upcoming = ReviewCard.objects.filter(
        user=request.user, next_review__gt=date.today()
    ).order_by("next_review")[:10]
    return render(
        request,
        "review/index.html",
        {"due_cards": due_cards, "upcoming": upcoming},
    )


@login_required
@require_POST
def review_submit(request: HttpRequest, card_id: UUID) -> HttpResponse:
    quality = int(request.POST.get("quality", 3))
    result = process_review_quality(request.user, card_id, quality)
    due_cards = get_due_review_cards(request.user)
    return render(
        request,
        "review/_due_list.html",
        {"due_cards": due_cards, "last_reviewed": result["card"]},
    )


@login_required
def assessments_view(request: HttpRequest) -> HttpResponse:
    assessments = Assessment.objects.filter(user=request.user).select_related("skill")[:30]
    skills = Skill.objects.all()
    if request.method == "POST":
        score = _post_float(request.POST.get("score"))
        maximum = _post_float(request.POST.get("maximum_score"), 100.0)
        pct = round((score / maximum) * 100, 1) if maximum else 0
        duration = _post_int(request.POST.get("duration_minutes"))
        Assessment.objects.create(
            user=request.user,
            name=request.POST.get("name", "Assessment"),
            category=request.POST.get("category", "general"),
            score=score,
            maximum_score=maximum,
            percentage=pct,
            duration_minutes=duration,
            completed_at=timezone.now(),
            notes=request.POST.get("notes", ""),
            skill_id=request.POST.get("skill_id") or None,
        )
        award_xp(request.user, 20)
        update_streak_on_activity(request.user)
        return redirect("assessments")
    return render(
        request,
        "assessments/index.html",
        {"assessments": assessments, "skills": skills},
    )


@login_required
def engineering_view(request: HttpRequest) -> HttpResponse:
    challenges = list(EngineeringChallenge.objects.all())
    by_type: dict[str, list] = {}
    for ch in challenges:
        by_type.setdefault(ch.challenge_type, []).append(ch)
    sessions = {
        s.challenge_id: s
        for s in EngineeringLabSession.objects.filter(
            user=request.user, challenge__in=challenges
        )
    }
    in_progress = 0
    completed_labs = 0
    for ch in challenges:
        session = sessions.get(ch.id)
        ch.lab_session = session
        steps = ch.lab_steps or []
        if session and steps:
            done = len(session.completed_steps or [])
            if done >= len(steps):
                completed_labs += 1
            elif done > 0 or session.accumulated_minutes or session.timer_started_at:
                in_progress += 1
        elif session and (session.accumulated_minutes or session.code_workspace):
            in_progress += 1

    attempts = list(
        EngineeringAttempt.objects.filter(user=request.user)
        .select_related("challenge")[:12]
    )
    type_meta = [
        {
            "key": key,
            "label": items[0].get_challenge_type_display(),
            "count": len(items),
            "items": items,
        }
        for key, items in by_type.items()
    ]
    stats = {
        "total": len(challenges),
        "in_progress": in_progress,
        "completed": completed_labs,
        "attempts": EngineeringAttempt.objects.filter(user=request.user).count(),
        "types": len(by_type),
    }
    return render(
        request,
        "engineering/index.html",
        {
            "by_type": by_type,
            "type_meta": type_meta,
            "attempts": attempts,
            "stats": stats,
        },
    )


def _get_or_create_lab_session(user, challenge: EngineeringChallenge) -> EngineeringLabSession:
    session, created = EngineeringLabSession.objects.get_or_create(
        user=user,
        challenge=challenge,
    )
    if created:
        session.code_workspace = challenge.starter_code or challenge.instructions or ""
        session.save(update_fields=["code_workspace", "updated_at"])
    return session


def _lab_timer_minutes(session: EngineeringLabSession) -> int:
    total = session.accumulated_minutes
    if session.timer_started_at:
        delta = timezone.now() - session.timer_started_at
        total += max(0, int(delta.total_seconds() / 60))
    return total


@login_required
def engineering_lab(request: HttpRequest, challenge_id: UUID) -> HttpResponse:
    challenge = get_object_or_404(EngineeringChallenge, id=challenge_id)
    session = _get_or_create_lab_session(request.user, challenge)
    hints = [h.strip() for h in challenge.hints.splitlines() if h.strip()]
    attempts = EngineeringAttempt.objects.filter(
        user=request.user, challenge=challenge
    )[:5]
    return render(
        request,
        "engineering/lab.html",
        {
            "challenge": challenge,
            "session": session,
            "hints": hints,
            "timer_minutes": _lab_timer_minutes(session),
            "timer_running": session.timer_started_at is not None,
            "attempts": attempts,
        },
    )


@login_required
@require_POST
def engineering_save_code(request: HttpRequest, challenge_id: UUID) -> HttpResponse:
    challenge = get_object_or_404(EngineeringChallenge, id=challenge_id)
    session = _get_or_create_lab_session(request.user, challenge)
    session.code_workspace = request.POST.get("code", "")
    session.save(update_fields=["code_workspace", "updated_at"])
    if request.htmx:
        return render(request, "engineering/_save_status.html")
    return redirect("engineering_lab", challenge_id=challenge.id)


@login_required
@require_POST
def engineering_toggle_step(request: HttpRequest, challenge_id: UUID, step_index: int) -> HttpResponse:
    challenge = get_object_or_404(EngineeringChallenge, id=challenge_id)
    session = _get_or_create_lab_session(request.user, challenge)
    steps = set(session.completed_steps or [])
    if step_index in steps:
        steps.discard(step_index)
    else:
        steps.add(step_index)
    session.completed_steps = sorted(steps)
    session.save(update_fields=["completed_steps", "updated_at"])
    return render(
        request,
        "engineering/_lab_steps.html",
        {"challenge": challenge, "session": session},
    )


@login_required
@require_POST
def engineering_reveal_hint(request: HttpRequest, challenge_id: UUID) -> HttpResponse:
    challenge = get_object_or_404(EngineeringChallenge, id=challenge_id)
    session = _get_or_create_lab_session(request.user, challenge)
    hints = [h.strip() for h in challenge.hints.splitlines() if h.strip()]
    if session.hints_revealed < len(hints):
        session.hints_revealed += 1
        session.save(update_fields=["hints_revealed", "updated_at"])
    return render(
        request,
        "engineering/_lab_hints.html",
        {"challenge": challenge, "session": session, "hints": hints},
    )


@login_required
@require_POST
def engineering_lab_timer_start(request: HttpRequest, challenge_id: UUID) -> HttpResponse:
    challenge = get_object_or_404(EngineeringChallenge, id=challenge_id)
    session = _get_or_create_lab_session(request.user, challenge)
    if not session.timer_started_at:
        session.timer_started_at = timezone.now()
        session.save(update_fields=["timer_started_at", "updated_at"])
    return render(
        request,
        "engineering/_lab_timer.html",
        {
            "challenge": challenge,
            "session": session,
            "timer_minutes": _lab_timer_minutes(session),
            "timer_running": True,
        },
    )


@login_required
@require_POST
def engineering_lab_timer_stop(request: HttpRequest, challenge_id: UUID) -> HttpResponse:
    challenge = get_object_or_404(EngineeringChallenge, id=challenge_id)
    session = _get_or_create_lab_session(request.user, challenge)
    if session.timer_started_at:
        delta = timezone.now() - session.timer_started_at
        session.accumulated_minutes += max(0, int(delta.total_seconds() / 60))
        session.timer_started_at = None
        session.save(
            update_fields=["accumulated_minutes", "timer_started_at", "updated_at"]
        )
    return render(
        request,
        "engineering/_lab_timer.html",
        {
            "challenge": challenge,
            "session": session,
            "timer_minutes": _lab_timer_minutes(session),
            "timer_running": False,
        },
    )


@login_required
@require_POST
def engineering_attempt(request: HttpRequest, challenge_id: UUID) -> HttpResponse:
    challenge = get_object_or_404(EngineeringChallenge, id=challenge_id)
    session = EngineeringLabSession.objects.filter(
        user=request.user, challenge=challenge
    ).first()
    code = request.POST.get("code_submission", "")
    if not code and session:
        code = session.code_workspace
    time_minutes = _post_int(request.POST.get("time_minutes"))
    if time_minutes == 0 and session:
        time_minutes = _lab_timer_minutes(session)
    EngineeringAttempt.objects.create(
        user=request.user,
        challenge=challenge,
        score=_post_float(request.POST.get("score")),
        time_minutes=time_minutes,
        completed=request.POST.get("completed") == "on",
        code_submission=code,
        notes=request.POST.get("notes", ""),
    )
    award_xp(request.user, 20)
    update_streak_on_activity(request.user)
    if request.htmx:
        return render(
            request,
            "engineering/_attempt_success.html",
            {"challenge": challenge},
        )
    return redirect("engineering_lab", challenge_id=challenge.id)


def _post_float(value: str | None, default: float = 0.0) -> float:
    if value is None or str(value).strip() == "":
        return default
    return float(value)


def _post_int(value: str | None, default: int = 0) -> int:
    if value is None or str(value).strip() == "":
        return default
    return int(value)


@login_required
def career_view(request: HttpRequest) -> HttpResponse:
    applications = JobApplication.objects.filter(user=request.user)[:30]
    goals = CareerGoal.objects.filter(user=request.user)
    portfolio = Project.objects.filter(
        Q(user=request.user) | Q(user__isnull=True)
    ).distinct()[:20]
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        if form_type == "application":
            JobApplication.objects.create(
                user=request.user,
                company=request.POST.get("company", ""),
                role=request.POST.get("role", ""),
                status=request.POST.get("status", "applied"),
                applied_date=request.POST.get("applied_date") or None,
                url=request.POST.get("url", ""),
                notes=request.POST.get("notes", ""),
            )
        elif form_type == "goal":
            CareerGoal.objects.create(
                user=request.user,
                title=request.POST.get("title", ""),
                category=request.POST.get("category", "learning"),
                target_date=request.POST.get("target_date") or None,
                notes=request.POST.get("notes", ""),
            )
        elif form_type == "portfolio":
            Project.objects.create(
                user=request.user,
                name=request.POST.get("name", ""),
                description=request.POST.get("description", ""),
                repository_url=request.POST.get("repository_url", ""),
                deployed_url=request.POST.get("deployed_url", ""),
                status=request.POST.get("status", "in_progress"),
            )
        return redirect("career")
    return render(
        request,
        "career/index.html",
        {
            "applications": applications,
            "goals": goals,
            "portfolio": portfolio,
        },
    )


@login_required
def mock_interviews_view(request: HttpRequest) -> HttpResponse:
    hub = get_mock_interview_hub(request.user)
    return render(request, "mock_interviews/index.html", hub)


@login_required
@require_POST
def mock_interview_start(request: HttpRequest, round_id: UUID) -> HttpResponse:
    session, error = start_mock_session(request.user, round_id)
    if error == "not_unlocked":
        messages.warning(request, "This mock interview unlocks later in your program.")
        return redirect("mock_interviews")
    if not session:
        return redirect("mock_interviews")
    return redirect("mock_interview_session", session_id=session.id)


@login_required
def mock_interview_session(request: HttpRequest, session_id: UUID) -> HttpResponse:
    session = get_object_or_404(
        MockInterviewSession.objects.select_related("round").prefetch_related(
            "round__questions"
        ),
        id=session_id,
        user=request.user,
    )
    if session.status == MockInterviewSession.Status.COMPLETED:
        return redirect("mock_interview_results", session_id=session.id)
    state = get_mock_session_state(session)
    return render(request, "mock_interviews/session.html", state)


@login_required
@require_POST
def mock_interview_run(request: HttpRequest, session_id: UUID) -> HttpResponse:
    from training.code_runner import parse_custom_test_cases

    session = get_object_or_404(
        MockInterviewSession.objects.select_related("round"),
        id=session_id,
        user=request.user,
    )
    if session.status == MockInterviewSession.Status.COMPLETED:
        return redirect("mock_interview_results", session_id=session.id)

    custom_cases = parse_custom_test_cases(request.POST.get("custom_cases", ""))
    result = run_mock_coding_tests(
        request.user,
        session_id,
        request.POST.get("code", ""),
        custom_cases=custom_cases,
    )
    state = get_mock_session_state(session)
    state["run_result"] = result
    state["editor_code"] = request.POST.get("code", "")
    state["custom_cases"] = custom_cases
    state["custom_cases_json"] = request.POST.get("custom_cases", "[]")
    return render(request, "mock_interviews/session.html", state)


@login_required
@require_POST
def mock_interview_submit(request: HttpRequest, session_id: UUID) -> HttpResponse:
    session = get_object_or_404(
        MockInterviewSession.objects.select_related("round"),
        id=session_id,
        user=request.user,
    )
    answer = request.POST.get("answer") or request.POST.get("code", "")
    result = submit_mock_response(
        request.user,
        session_id,
        answer,
        float(request.POST.get("score", 5) or 5),
        float(request.POST.get("confidence", 5) or 5),
        int(request.POST.get("time_spent_seconds", 0) or 0),
    )
    if result["completed"]:
        return redirect("mock_interview_results", session_id=session.id)
    return redirect("mock_interview_session", session_id=session.id)


@login_required
def mock_interview_results(request: HttpRequest, session_id: UUID) -> HttpResponse:
    session = get_object_or_404(
        MockInterviewSession.objects.select_related("round").prefetch_related(
            "round__questions"
        ),
        id=session_id,
        user=request.user,
        status=MockInterviewSession.Status.COMPLETED,
    )
    results = get_mock_results_breakdown(session)
    return render(request, "mock_interviews/results.html", results)


@login_required
def cognitive_hub(request: HttpRequest) -> HttpResponse:
    return render(request, "cognitive/index.html", get_cognitive_hub(request.user))


@login_required
def cognitive_list(request: HttpRequest, type_slug: str) -> HttpResponse:
    challenge_type = COGNITIVE_TYPE_SLUGS.get(type_slug)
    if not challenge_type:
        return redirect("cognitive_hub")
    category = request.GET.get("category") or None
    difficulty = request.GET.get("difficulty") or None
    data = get_cognitive_list_data(
        request.user, challenge_type, category=category, difficulty=difficulty
    )
    data["type_slug"] = type_slug
    data["type_label"] = "Aptitude Tests" if challenge_type == "aptitude" else "Brain Teasers"
    return render(request, "cognitive/list.html", data)


@login_required
def cognitive_question(request: HttpRequest, type_slug: str, question_id: UUID) -> HttpResponse:
    challenge_type = COGNITIVE_TYPE_SLUGS.get(type_slug)
    if not challenge_type:
        return redirect("cognitive_hub")
    question = get_object_or_404(CognitiveQuestion, id=question_id, challenge_type=challenge_type)
    data = get_cognitive_question_data(request.user, question.id)
    data["type_slug"] = type_slug
    data["type_label"] = "Aptitude Tests" if challenge_type == "aptitude" else "Brain Teasers"
    return render(request, "cognitive/question.html", data)


@login_required
@require_POST
def cognitive_reveal(request: HttpRequest, type_slug: str, question_id: UUID) -> HttpResponse:
    challenge_type = COGNITIVE_TYPE_SLUGS.get(type_slug)
    if not challenge_type:
        return redirect("cognitive_hub")
    question = get_object_or_404(CognitiveQuestion, id=question_id, challenge_type=challenge_type)
    try:
        time_spent = int(request.POST.get("time_spent_seconds") or 0)
    except (TypeError, ValueError):
        time_spent = 0
    data = reveal_cognitive_answer(
        request.user,
        question.id,
        attempted_answer=request.POST.get("attempted_answer", ""),
        notes=request.POST.get("notes", ""),
        time_spent_seconds=max(0, time_spent),
    )
    if request.htmx:
        return render(request, "cognitive/_answer.html", data)
    return redirect("cognitive_question", type_slug=type_slug, question_id=question.id)


def home(request: HttpRequest) -> HttpResponse:
    """Public landing for guests; authenticated users go to the dashboard."""
    if request.user.is_authenticated:
        return redirect("dashboard")
    return landing_view(request)


def landing_view(request: HttpRequest) -> HttpResponse:
    from training.quotes import carousel_quotes, quote_of_the_day

    featured = Project.objects.filter(is_catalog=True, is_featured=True).order_by("order")[:3]
    return render(
        request,
        "landing/index.html",
        {
            "quote_of_the_day": quote_of_the_day(),
            "carousel_quotes": carousel_quotes(8),
            "featured_projects": featured,
            "feature_highlights": FEATURE_HIGHLIGHTS[:6],
        },
    )


def features_view(request: HttpRequest) -> HttpResponse:
    from training.quotes import quote_of_the_day

    return render(
        request,
        "marketing/features.html",
        {"feature_groups": FEATURE_GROUPS, "quote_of_the_day": quote_of_the_day()},
    )


@login_required
def projects_view(request: HttpRequest) -> HttpResponse:
    projects = Project.objects.filter(is_catalog=True).order_by("order", "name")
    progress_map = {
        str(p.project_id): p
        for p in ProjectProgress.objects.filter(user=request.user, project__in=projects)
    }
    cards = []
    for project in projects:
        prog = progress_map.get(str(project.id))
        cards.append(
            {
                "project": project,
                "progress": prog,
                "pass_pct": prog.pass_pct if prog else 0,
                "status": prog.status if prog else "planned",
            }
        )
    return render(request, "projects/index.html", {"cards": cards})


@login_required
def project_detail(request: HttpRequest, project_id: UUID) -> HttpResponse:
    project = get_object_or_404(Project, id=project_id, is_catalog=True)
    progress, _ = ProjectProgress.objects.get_or_create(user=request.user, project=project)
    if request.method == "POST":
        action = request.POST.get("action", "save")
        was_passing = progress.is_passing
        if action == "toggle_criterion":
            cid = request.POST.get("criterion_id", "").strip()
            checked = list(progress.checked_criteria or [])
            if cid:
                if cid in checked:
                    checked.remove(cid)
                else:
                    checked.append(cid)
                progress.checked_criteria = checked
                if progress.status == "planned":
                    progress.status = "in_progress"
                    progress.started_at = progress.started_at or timezone.now()
        else:
            progress.notes = request.POST.get("notes", progress.notes)
            progress.repository_url = request.POST.get("repository_url", progress.repository_url)
            progress.deployed_url = request.POST.get("deployed_url", progress.deployed_url)
            progress.status = request.POST.get("status", progress.status)
            if progress.status == "in_progress" and not progress.started_at:
                progress.started_at = timezone.now()

        if progress.is_passing:
            progress.status = "completed"
            progress.completed_at = progress.completed_at or timezone.now()
            if not was_passing:
                award_xp(request.user, 75)
                messages.success(request, "All required criteria met — +75 XP.")
        progress.save()
        if action != "toggle_criterion":
            messages.success(request, "Project progress saved.")
        return redirect("project_detail", project_id=project.id)

    criteria = []
    checked = set(progress.checked_criteria or [])
    for c in project.acceptance_criteria or []:
        criteria.append({**c, "checked": c.get("id") in checked})

    return render(
        request,
        "projects/detail.html",
        {
            "project": project,
            "progress": progress,
            "criteria": criteria,
            "is_passing": progress.is_passing,
        },
    )


FEATURE_HIGHLIGHTS = [
    {"title": "90-day core + Phase 4", "copy": "Core mastery through day 90, then elite remediation and failure drills to 120."},
    {"title": "Adaptive coaching", "copy": "Weakness signals, repeating mistakes, and next actions on the dashboard."},
    {"title": "Curated resources", "copy": "Articles, docs, and courses mapped to each skill and training day."},
    {"title": "Mock interviews", "copy": "Timed rounds with coding run/tests and scored feedback."},
    {"title": "Engineering labs", "copy": "Hands-on challenges with steps, hints, and timers."},
    {"title": "Elite project NFRs", "copy": "Production briefs with SLOs, chaos, load evidence, and ADRs."},
]

FEATURE_GROUPS = [
    {
        "title": "Training core",
        "items": [
            {"name": "90-day core + Phase 4", "detail": "Phases 1–3 through day 90; elite mastery track days 91–120."},
            {"name": "Today execution", "detail": "Mission view, curated resources, timer, daily review, and streaks."},
            {"name": "Focus mode", "detail": "Distraction-light sessions tied to tasks and XP."},
            {"name": "Calendar", "detail": "Visual program map with day detail drawers."},
        ],
    },
    {
        "title": "Skill engines",
        "items": [
            {"name": "Adaptive recommendations", "detail": "Daily coaching from weaknesses, overdue work, resources, and curriculum."},
            {"name": "Skill health", "detail": "Scores and trends from assessments, coding, and mistakes."},
            {"name": "Curated resources", "detail": "Docs, articles, and courses linked to skills and days."},
            {"name": "Mistakes log", "detail": "Capture, categorize, and resolve repeating errors."},
        ],
    },
    {
        "title": "Interview & coding",
        "items": [
            {"name": "Practice interview bank", "detail": "Sectioned questions with objectives, hints, and solutions."},
            {"name": "Mock interviews", "detail": "Multi-round sessions, coding sandbox, and results."},
            {"name": "Coding tracker", "detail": "Pattern performance and solve rate analytics."},
            {"name": "Cognitive drills", "detail": "Aptitude and brain teasers with countdown timers."},
        ],
    },
    {
        "title": "Build & operate",
        "items": [
            {"name": "Engineering labs", "detail": "Interactive labs with checklists, hints, and workspaces."},
            {"name": "Projects hub", "detail": "Detailed briefs, NFRs, milestones, and passing criteria."},
            {"name": "Career toolkit", "detail": "Applications, goals, and portfolio entries."},
            {"name": "Reports", "detail": "Heatmaps, study charts, XP, achievements, weekly reviews."},
        ],
    },
    {
        "title": "Platform",
        "items": [
            {"name": "Gamification", "detail": "XP, levels, streaks, and unlockable milestones."},
            {"name": "Dark mode", "detail": "Theme toggle with accessible contrast."},
            {"name": "PWA", "detail": "Installable app shell with offline-friendly static caching."},
            {"name": "API", "detail": "Authenticated DRF endpoints for progress and analytics."},
        ],
    },
]
