"""HTTP error handlers with structured logging."""
from __future__ import annotations

import logging

from django.http import HttpRequest, HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.template.loader import render_to_string

logger = logging.getLogger("training.http")


def _username(request: HttpRequest) -> str:
    user = getattr(request, "user", None)
    if user is not None and getattr(user, "is_authenticated", False):
        return user.get_username()
    return "anonymous"


def handler404(request: HttpRequest, exception=None) -> HttpResponse:
    path = getattr(request, "path", "")
    logger.warning(
        "404 Not Found path=%s method=%s user=%s",
        path,
        getattr(request, "method", "?"),
        _username(request),
    )
    return render(
        request,
        "404.html",
        {
            "request_path": path,
            "user_authenticated": getattr(
                getattr(request, "user", None), "is_authenticated", False
            ),
        },
        status=404,
    )


def handler500(request: HttpRequest) -> HttpResponse:
    path = getattr(request, "path", "")
    logger.error(
        "500 Server Error path=%s method=%s user=%s",
        path,
        getattr(request, "method", "?"),
        _username(request),
        exc_info=True,
    )
    try:
        # No request context — avoids DB-backed context processors on hard failures.
        body = render_to_string("500.html")
    except Exception:
        logger.exception("Failed to render 500.html")
        body = (
            "<!DOCTYPE html><html><head><title>500</title></head>"
            "<body><h1>Server Error</h1><p>Something went wrong.</p>"
            "<p><a href='/'>Home</a></p></body></html>"
        )
    return HttpResponseServerError(body)
