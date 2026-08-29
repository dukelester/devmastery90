from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from training import error_handlers
from training.views import service_worker

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sw.js", service_worker, name="service_worker"),
    path("", include("training.urls")),
    path("api/", include("training.api_urls")),
]

handler404 = "training.error_handlers.handler404"
handler500 = "training.error_handlers.handler500"

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

    urlpatterns += [
        path(
            "__errors__/404/",
            lambda request: error_handlers.handler404(request, exception=None),
            name="preview_404",
        ),
        path(
            "__errors__/500/",
            lambda request: error_handlers.handler500(request),
            name="preview_500",
        ),
    ]
