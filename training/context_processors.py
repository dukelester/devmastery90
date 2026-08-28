"""Context processors for DevMastery templates."""
from training.services import get_or_create_profile


def gamification(request):
    if request.user.is_authenticated:
        profile = get_or_create_profile(request.user)
        return {
            "user_xp": profile.xp,
            "user_level": profile.level,
            "user_level_title": profile.level_title,
            "user_streak": profile.current_streak,
        }
    return {}
