from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from training.views import service_worker

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sw.js", service_worker, name="service_worker"),
    path("", include("training.urls")),
    path("api/", include("training.api_urls")),
]

if settings.DEBUG:
    try:
        import debug_toolbar

        urlpatterns = [
            path("__debug__/", include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass
