"""URL configuration for training app."""
from django.contrib.auth.views import LogoutView
from django.urls import path

from training import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("today/", views.today_view, name="today"),
    path("coding/", views.coding_view, name="coding"),
    path("interview/", views.interview_view, name="interview"),
    path("analytics/", views.analytics_view, name="analytics"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("calendar/<int:day_number>/", views.calendar_day_detail, name="calendar_day"),
    path("weekly-review/<int:week_number>/", views.weekly_review_view, name="weekly_review"),
    # HTMX task endpoints
    path("tasks/<int:task_id>/complete/", views.task_complete, name="task_complete"),
    path("tasks/<int:task_id>/skip/", views.task_skip, name="task_skip"),
    path("tasks/<int:task_id>/block/", views.task_block, name="task_block"),
    path("tasks/<int:task_id>/notes/", views.task_notes, name="task_notes"),
    # Timer
    path("timer/", views.timer_view, name="timer"),
    path("timer/start/", views.timer_start, name="timer_start"),
    path("timer/stop/", views.timer_stop, name="timer_stop"),
    # Coding
    path("coding/create/", views.coding_create, name="coding_create"),
    path("coding/<int:problem_id>/solve/", views.coding_solve, name="coding_solve"),
    # Interview
    path("interview/<int:question_id>/attempt/", views.interview_attempt, name="interview_attempt"),
    # Daily review
    path("daily-review/", views.daily_review_submit, name="daily_review"),
]
