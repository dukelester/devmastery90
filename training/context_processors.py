"""Context processors for DevMastery templates."""
from training.services import assess_workload, get_or_create_profile


def gamification(request):
    if not request.user.is_authenticated:
        return {}

    profile = get_or_create_profile(request.user)
    current_day = 1
    if profile.program_start_date:
        from datetime import date

        current_day = max(1, min((date.today() - profile.program_start_date).days + 1, 90))

    milestones = [
        {"key": "week1", "label": "Week 1", "earned": current_day >= 7},
        {"key": "month1", "label": "Month 1", "earned": current_day >= 30},
        {"key": "month2", "label": "Month 2", "earned": current_day >= 60},
        {"key": "streak7", "label": "7-day streak", "earned": profile.current_streak >= 7 or profile.longest_streak >= 7},
        {"key": "streak14", "label": "14-day streak", "earned": profile.current_streak >= 14 or profile.longest_streak >= 14},
        {"key": "xp1k", "label": "1K XP", "earned": profile.xp >= 1000},
        {"key": "xp5k", "label": "5K XP", "earned": profile.xp >= 5000},
        {"key": "day90", "label": "Day 90", "earned": current_day >= 90},
    ]

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
        "user_milestones": milestones,
        "workload": assess_workload(request.user),
    }
