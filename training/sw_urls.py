"""Service worker URL conf (also importable via include)."""
from django.urls import path

from training.views import service_worker

urlpatterns = [
    path("", service_worker, name="service_worker"),
]
