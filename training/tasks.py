"""Celery tasks for DevMastery."""
from celery import shared_task


@shared_task(name="training.send_due_training_digests")
def send_due_training_digests(force_all: bool = False) -> dict:
    from training.email_digest import send_due_digests

    return send_due_digests(force_all=force_all)


@shared_task(name="training.send_user_training_digest")
def send_user_training_digest(user_id: int, force: bool = True) -> bool:
    from django.contrib.auth import get_user_model

    from training.email_digest import send_training_digest

    User = get_user_model()
    user = User.objects.get(pk=user_id)
    return send_training_digest(user, force=force)
