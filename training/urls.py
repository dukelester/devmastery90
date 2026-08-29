"""URL configuration for training app."""
from django.contrib.auth.views import (
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path

from training import views
from training.forms import DevMasteryPasswordResetForm, DevMasterySetPasswordForm

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.register_view, name="register"),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            form_class=DevMasteryPasswordResetForm,
            success_url="/password-reset/done/",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            form_class=DevMasterySetPasswordForm,
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
    path("profile/", views.profile_view, name="profile"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("today/", views.today_view, name="today"),
    path("today/daily-review/", views.daily_review_submit, name="daily_review"),
    path("coding/", views.coding_view, name="coding"),
    path("interview/", views.interview_view, name="interview"),
    path("interview/<slug:section_slug>/", views.practice_section, name="practice_section"),
    path(
        "interview/<slug:section_slug>/<uuid:question_id>/",
        views.practice_question,
        name="practice_question",
    ),
    path(
        "interview/<slug:section_slug>/<uuid:question_id>/submit/",
        views.practice_submit,
        name="practice_submit",
    ),
    path("analytics/", views.analytics_view, name="analytics"),
    path("reports/", views.analytics_view, name="reports"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("calendar/<uuid:day_id>/", views.calendar_day_detail, name="calendar_day"),
    path("weekly-review/<uuid:week_id>/", views.weekly_review_view, name="weekly_review"),
    # HTMX task endpoints
    path("tasks/<uuid:task_id>/complete/", views.task_complete, name="task_complete"),
    path("tasks/<uuid:task_id>/skip/", views.task_skip, name="task_skip"),
    path("tasks/<uuid:task_id>/block/", views.task_block, name="task_block"),
    path("tasks/<uuid:task_id>/notes/", views.task_notes, name="task_notes"),
    # Timer
    path("timer/", views.timer_view, name="timer"),
    path("timer/start/", views.timer_start, name="timer_start"),
    path("timer/stop/", views.timer_stop, name="timer_stop"),
    path("focus/", views.focus_mode_view, name="focus_mode"),
    path("tasks/<uuid:task_id>/focus/", views.focus_start, name="focus_start"),
    # Coding
    path("coding/create/", views.coding_create, name="coding_create"),
    path("coding/<uuid:problem_id>/solve/", views.coding_solve, name="coding_solve"),
    # Interview
    path("interview/<uuid:question_id>/attempt/", views.interview_attempt, name="interview_attempt"),
    # Daily review
    path("onboarding/", views.onboarding_view, name="onboarding"),
    path("mistakes/", views.mistakes_view, name="mistakes"),
    path("mistakes/<uuid:mistake_id>/resolve/", views.mistake_resolve, name="mistake_resolve"),
    path("review/", views.review_view, name="review"),
    path("review/<uuid:card_id>/submit/", views.review_submit, name="review_submit"),
    path("assessments/", views.assessments_view, name="assessments"),
    path("mock-interviews/", views.mock_interviews_view, name="mock_interviews"),
    path(
        "mock-interviews/<uuid:round_id>/start/",
        views.mock_interview_start,
        name="mock_interview_start",
    ),
    path(
        "mock-interviews/session/<uuid:session_id>/",
        views.mock_interview_session,
        name="mock_interview_session",
    ),
    path(
        "mock-interviews/session/<uuid:session_id>/run/",
        views.mock_interview_run,
        name="mock_interview_run",
    ),
    path(
        "mock-interviews/session/<uuid:session_id>/submit/",
        views.mock_interview_submit,
        name="mock_interview_submit",
    ),
    path(
        "mock-interviews/session/<uuid:session_id>/results/",
        views.mock_interview_results,
        name="mock_interview_results",
    ),
    path("engineering/", views.engineering_view, name="engineering"),
    path(
        "engineering/<uuid:challenge_id>/",
        views.engineering_lab,
        name="engineering_lab",
    ),
    path(
        "engineering/<uuid:challenge_id>/code/",
        views.engineering_save_code,
        name="engineering_save_code",
    ),
    path(
        "engineering/<uuid:challenge_id>/step/<int:step_index>/toggle/",
        views.engineering_toggle_step,
        name="engineering_toggle_step",
    ),
    path(
        "engineering/<uuid:challenge_id>/hint/",
        views.engineering_reveal_hint,
        name="engineering_reveal_hint",
    ),
    path(
        "engineering/<uuid:challenge_id>/timer/start/",
        views.engineering_lab_timer_start,
        name="engineering_lab_timer_start",
    ),
    path(
        "engineering/<uuid:challenge_id>/timer/stop/",
        views.engineering_lab_timer_stop,
        name="engineering_lab_timer_stop",
    ),
    path(
        "engineering/<uuid:challenge_id>/attempt/",
        views.engineering_attempt,
        name="engineering_attempt",
    ),
    path("career/", views.career_view, name="career"),
    path("cognitive/", views.cognitive_hub, name="cognitive_hub"),
    path("cognitive/<slug:type_slug>/", views.cognitive_list, name="cognitive_list"),
    path(
        "cognitive/<slug:type_slug>/<uuid:question_id>/",
        views.cognitive_question,
        name="cognitive_question",
    ),
    path(
        "cognitive/<slug:type_slug>/<uuid:question_id>/reveal/",
        views.cognitive_reveal,
        name="cognitive_reveal",
    ),
]
