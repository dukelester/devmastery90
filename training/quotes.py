"""Motivational quotes for landing carousel and quote-of-the-day."""
from __future__ import annotations

import hashlib
from datetime import date
from typing import Any


QUOTES: list[dict[str, str]] = [
    {
        "text": "Discipline is choosing what you want most over what you want now.",
        "author": "Training floor",
    },
    {
        "text": "Ship small, learn fast, then raise the bar.",
        "author": "DevMastery",
    },
    {
        "text": "Clarity beats cleverness in production systems.",
        "author": "Engineering craft",
    },
    {
        "text": "Your future self is watching how you practice today.",
        "author": "DevMastery",
    },
    {
        "text": "Consistency compounds harder than intensity.",
        "author": "Deliberate practice",
    },
    {
        "text": "Debug the process before you debug the talent myth.",
        "author": "DevMastery",
    },
    {
        "text": "Write code your teammate can trust at 2 a.m.",
        "author": "On-call wisdom",
    },
    {
        "text": "Mastery is a streak of ordinary days protected fiercely.",
        "author": "DevMastery 90",
    },
    {
        "text": "Tests are letters to your future self.",
        "author": "Quality engineering",
    },
    {
        "text": "Progress is a logged session, not a mood.",
        "author": "DevMastery",
    },
    {
        "text": "Design for failure, celebrate recovery.",
        "author": "SRE mindset",
    },
    {
        "text": "The interview rewards depth you earned in quiet hours.",
        "author": "Career track",
    },
    {
        "text": "Simplify until it hurts, then add back only what earns its keep.",
        "author": "Systems design",
    },
    {
        "text": "A strong engineer leaves the codebase kinder than they found it.",
        "author": "DevMastery",
    },
]


def quote_of_the_day(for_day: date | None = None) -> dict[str, Any]:
    day = for_day or date.today()
    digest = hashlib.sha256(day.isoformat().encode()).hexdigest()
    idx = int(digest[:8], 16) % len(QUOTES)
    q = QUOTES[idx]
    return {
        "text": q["text"],
        "author": q["author"],
        "date": day.isoformat(),
        "index": idx,
    }


def carousel_quotes(limit: int = 8) -> list[dict[str, str]]:
    qotd = quote_of_the_day()
    ordered = QUOTES[qotd["index"] :] + QUOTES[: qotd["index"]]
    return ordered[:limit]
