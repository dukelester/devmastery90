"""Context processors for DevMastery templates."""
from training.services import get_or_create_profile


def gamification(request):
    if not request.user.is_authenticated:
        return {}

    profile = get_or_create_profile(request.user)
    milestones = [
        {"key": "week1", "label": "Week 1", "earned": profile.xp >= 100 or profile.current_streak >= 7},
        {"key": "month1", "label": "Month 1", "earned": False},
        {"key": "streak7", "label": "7-day chain", "earned": profile.current_streak >= 7 or profile.longest_streak >= 7},
        {"key": "streak14", "label": "14-day chain", "earned": profile.current_streak >= 14 or profile.longest_streak >= 14},
        {"key": "xp1k", "label": "1K XP", "earned": profile.xp >= 1000},
        {"key": "xp5k", "label": "5K XP", "earned": profile.xp >= 5000},
    ]

    return {
        "user_xp": profile.xp,
        "user_level": profile.level,
        "user_level_title": profile.level_title,
        "user_streak": profile.current_streak,
        "user_longest_streak": profile.longest_streak,
        "user_xp_into_level": profile.xp_into_level,
        "user_xp_to_next": profile.xp_to_next_level,
        "user_xp_pct": profile.xp_progress_pct,
        "user_next_level_title": profile.next_level_title,
        "user_milestones": milestones,
    }
