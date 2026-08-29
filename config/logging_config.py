"""Shared Django logging configuration for DevMastery 90."""
from __future__ import annotations

import os
from pathlib import Path


def build_logging(base_dir: Path) -> dict:
    log_dir = base_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "devmastery.log"
    level = os.environ.get("LOG_LEVEL", "INFO").upper()

    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "[{asctime}] {levelname} {name} {module}:{lineno} — {message}",
                "style": "{",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "simple": {
                "format": "{levelname} {name}: {message}",
                "style": "{",
            },
        },
        "filters": {
            "require_debug_false": {
                "()": "django.utils.log.RequireDebugFalse",
            },
            "require_debug_true": {
                "()": "django.utils.log.RequireDebugTrue",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
                "level": level,
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": str(log_file),
                "maxBytes": 5 * 1024 * 1024,
                "backupCount": 5,
                "formatter": "verbose",
                "level": level,
            },
            "mail_admins": {
                "class": "django.utils.log.AdminEmailHandler",
                "level": "ERROR",
                "filters": ["require_debug_false"],
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console", "file"],
            "level": level,
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": level,
                "propagate": False,
            },
            "django.request": {
                "handlers": ["console", "file", "mail_admins"],
                "level": "WARNING",
                "propagate": False,
            },
            "django.security": {
                "handlers": ["console", "file", "mail_admins"],
                "level": "WARNING",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console"],
                "level": os.environ.get("SQL_LOG_LEVEL", "WARNING").upper(),
                "propagate": False,
            },
            "training": {
                "handlers": ["console", "file"],
                "level": level,
                "propagate": False,
            },
            "training.http": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "gunicorn.error": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
            "gunicorn.access": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": False,
            },
        },
    }
