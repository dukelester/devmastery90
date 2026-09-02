"""Build and send DevMastery coaching email digests."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.db.models import Sum
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from training.models import LearningResource, StudySession, UserProfile
from training.services import (
    calculate_progress,
    calculate_skill_health,
    get_coaching_briefing,
    get_day_resources,
    get_or_create_profile,
    get_today_training_day,
    get_top_weaknesses,
    get_training_day,
)

logger = logging.getLogger(__name__)


def site_base_url() -> str:
    return getattr(settings, "SITE_URL", "http://localhost:8000").rstrip("/")


def absolute_url(path: str) -> str:
    if path.startswith("http"):
        return path
    return f"{site_base_url()}{path}"


def _user_local_now(profile: UserProfile):
    try:
        tz = ZoneInfo(profile.timezone or "UTC")
    except ZoneInfoNotFoundError:
        tz = ZoneInfo("UTC")
    return timezone.now().astimezone(tz)


def should_send_digest_now(profile: UserProfile, force: bool = False) -> bool:
    if force:
        return True
    if not profile.email_reminders_enabled:
        return False
    user = profile.user
    if not user.email or not user.is_active:
        return False

    local_now = _user_local_now(profile)
    if local_now.hour != int(profile.email_reminder_hour):
        return False

    if profile.last_reminder_sent_at:
        last_local = profile.last_reminder_sent_at.astimezone(local_now.tzinfo)
        if last_local.date() == local_now.date():
            return False

    freq = profile.email_digest_frequency
    weekday = local_now.weekday()  # Mon=0
    if freq == "weekdays" and weekday >= 5:
        return False
    if freq == "weekly" and weekday != 0:
        return False
    return True


def build_email_digest(user) -> dict[str, Any]:
    """Assemble coaching digest payload for templates."""
    profile = get_or_create_profile(user)
    progress = calculate_progress(user)
    training_day = get_today_training_day(user)
    tomorrow = get_training_day(progress["current_day"] + 1)
    coaching = get_coaching_briefing(user)
    weaknesses = get_top_weaknesses(user, limit=3)

    # Strengths: skills not in weakness list with decent scores
    weak_ids = {w["skill"].id for w in weaknesses}
    from training.models import Skill

    strengths = []
    for skill in Skill.objects.all()[:40]:
        if skill.id in weak_ids:
            continue
        health = calculate_skill_health(user, skill)
        if health["score"] >= 7.0 and health["weakness_level"] == "LOW":
            strengths.append(
                {
                    "name": skill.name,
                    "score": health["score"],
                    "trend": health["trend"],
                }
            )
        if len(strengths) >= 3:
            break
    if not strengths:
        strengths = [
            {
                "name": "Consistency",
                "score": progress["streak"],
                "trend": "up" if progress["streak"] else "flat",
            }
        ]

    today_tasks = []
    if training_day:
        for task in training_day.tasks.filter(completed=False, skipped=False).order_by("order")[:6]:
            today_tasks.append(
                {
                    "title": task.title,
                    "minutes": task.estimated_minutes,
                    "type": task.get_task_type_display(),
                    "skill": task.skill.name if task.skill else "",
                }
            )

    upcoming = []
    if tomorrow:
        upcoming.append(
            {
                "label": f"Day {tomorrow.day_number}",
                "title": tomorrow.title,
                "focus": tomorrow.focus,
                "minutes": tomorrow.target_minutes,
            }
        )

    day_num = progress["current_day"]
    reading = []
    for resource in get_day_resources(day_num)[:4]:
        reading.append(
            {
                "title": resource.title,
                "url": resource.url,
                "type": resource.get_resource_type_display(),
                "description": resource.description,
            }
        )
    if len(reading) < 4 and weaknesses:
        for w in weaknesses:
            extras = (
                LearningResource.objects.filter(skill=w["skill"])
                .order_by("-is_primary", "order")[: 4 - len(reading)]
            )
            for resource in extras:
                reading.append(
                    {
                        "title": resource.title,
                        "url": resource.url,
                        "type": resource.get_resource_type_display(),
                        "description": resource.description or f"For {w['skill'].name}",
                    }
                )
            if len(reading) >= 4:
                break

    week_ago = timezone.now() - timedelta(days=7)
    week_minutes = (
        StudySession.objects.filter(
            user=user, started_at__gte=week_ago, ended_at__isnull=False
        ).aggregate(total=Sum("duration_minutes"))["total"]
        or 0
    )

    name = profile.display_name or user.first_name or user.username
    return {
        "user": user,
        "profile": profile,
        "name": name,
        "progress": progress,
        "training_day": training_day,
        "today_tasks": today_tasks,
        "upcoming": upcoming,
        "weaknesses": weaknesses,
        "strengths": strengths,
        "reading": reading,
        "coaching": coaching,
        "week_minutes": week_minutes,
        "week_hours": round(week_minutes / 60, 1),
        "urls": {
            "today": absolute_url(reverse("today")),
            "dashboard": absolute_url(reverse("dashboard")),
            "analytics": absolute_url(reverse("analytics")),
            "profile": absolute_url(reverse("profile") + "?tab=reminders"),
            "resources_home": absolute_url(reverse("today")),
        },
        "site_url": site_base_url(),
        "generated_at": timezone.now(),
    }


def send_training_digest(user, force: bool = False) -> bool:
    """Send one coaching digest. Returns True if sent."""
    profile = get_or_create_profile(user)
    if not should_send_digest_now(profile, force=force):
        return False
    if not user.email:
        logger.info("Skip digest for %s — no email", user.username)
        return False

    context = build_email_digest(user)
    subject = (
        f"DevMastery — Day {context['progress']['current_day']}/"
        f"{context['progress']['total_days']}: "
        f"{context['training_day'].title if context['training_day'] else 'Your coaching digest'}"
    )
    text_body = render_to_string("emails/training_digest.txt", context)
    html_body = render_to_string("emails/training_digest.html", context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send(fail_silently=False)

    profile.last_reminder_sent_at = timezone.now()
    profile.save(update_fields=["last_reminder_sent_at", "updated_at"])
    logger.info("Sent training digest to %s <%s>", user.username, user.email)
    return True


def send_due_digests(*, force_all: bool = False) -> dict[str, int]:
    """Send digests to all eligible users. Used by Celery beat / management command."""
    sent = 0
    skipped = 0
    errors = 0
    qs = UserProfile.objects.select_related("user").filter(
        email_reminders_enabled=True,
        user__is_active=True,
    ).exclude(user__email="")
    for profile in qs.iterator():
        try:
            if send_training_digest(profile.user, force=force_all):
                sent += 1
            else:
                skipped += 1
        except Exception:
            errors += 1
            logger.exception("Failed digest for user_id=%s", profile.user_id)
    return {"sent": sent, "skipped": skipped, "errors": errors}
