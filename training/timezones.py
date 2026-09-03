"""Timezone helpers — auto-detect from browser, default Africa/Nairobi."""
from __future__ import annotations

from functools import lru_cache
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError, available_timezones

DEFAULT_TIMEZONE = "Africa/Nairobi"

# Prefer these near the top of selects for Kenyan / common training audiences.
PREFERRED_TIMEZONES = (
    "Africa/Nairobi",
    "Africa/Kampala",
    "Africa/Dar_es_Salaam",
    "Africa/Addis_Ababa",
    "Africa/Lagos",
    "Africa/Johannesburg",
    "Africa/Cairo",
    "Europe/London",
    "Europe/Paris",
    "Europe/Berlin",
    "America/New_York",
    "America/Chicago",
    "America/Denver",
    "America/Los_Angeles",
    "America/Toronto",
    "Asia/Dubai",
    "Asia/Kolkata",
    "Asia/Singapore",
    "Asia/Tokyo",
    "Australia/Sydney",
    "UTC",
)


def normalize_timezone(name: str | None) -> str:
    """Return a valid IANA zone, or DEFAULT_TIMEZONE."""
    raw = (name or "").strip()
    if not raw:
        return DEFAULT_TIMEZONE
    try:
        ZoneInfo(raw)
        return raw
    except ZoneInfoNotFoundError:
        return DEFAULT_TIMEZONE


@lru_cache(maxsize=1)
def timezone_choices() -> list[tuple[str, str]]:
    """Choices for profile selects: preferred first, then the rest."""
    all_zones = sorted(available_timezones())
    preferred = [z for z in PREFERRED_TIMEZONES if z in all_zones]
    rest = [z for z in all_zones if z not in preferred]
    return [(z, z.replace("_", " ")) for z in preferred + rest]
