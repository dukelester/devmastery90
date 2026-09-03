"""Context processors for DevMastery templates."""
from training.services import assess_workload, build_milestones, get_or_create_profile


def gamification(request):
    if not request.user.is_authenticated:
        return {}

    profile = get_or_create_profile(request.user)
    milestones = build_milestones(request.user, profile)

    return {
        "user_xp": profile.xp,
        "user_xp_display": profile.xp_display,
        "user_level": profile.level,
        "user_level_title": profile.level_title,
        "user_level_display": profile.level_display,
        "user_streak": profile.current_streak,
        "user_longest_streak": profile.longest_streak,
        "user_xp_into_level": profile.xp_into_level,
        "user_xp_to_next": profile.xp_to_next_level,
        "user_xp_pct": profile.xp_progress_pct,
        "user_next_level_title": profile.next_level_title,
        "user_milestones": milestones["items"],
        "user_milestones_earned": milestones["earned_count"],
        "user_milestones_total": milestones["total_count"],
        "user_milestones_pct": milestones["earned_pct"],
        "workload": assess_workload(request.user),
        "user_timezone": profile.timezone or "Africa/Nairobi",
        "user_timezone_auto": profile.timezone_auto,
    }
