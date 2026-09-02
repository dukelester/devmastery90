"""Send coaching email digests (sessions, progress, reading)."""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from training.email_digest import send_due_digests, send_training_digest


class Command(BaseCommand):
    help = "Send DevMastery training reminder digests"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Ignore schedule hour/frequency and send to all opted-in users with email",
        )
        parser.add_argument(
            "--username",
            type=str,
            help="Send only to this username (implies force for that user)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Build digests but do not send",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        if options["username"]:
            user = User.objects.get(username=options["username"])
            if options["dry_run"]:
                from training.email_digest import build_email_digest

                ctx = build_email_digest(user)
                self.stdout.write(
                    f"Dry-run for {user.username}: day {ctx['progress']['current_day']}, "
                    f"{len(ctx['today_tasks'])} tasks, {len(ctx['reading'])} resources"
                )
                return
            sent = send_training_digest(user, force=True)
            self.stdout.write(self.style.SUCCESS(f"Sent={sent} to {user.email}"))
            return

        if options["dry_run"]:
            self.stdout.write("Dry-run: use --username to preview one user.")
            return

        result = send_due_digests(force_all=options["force"])
        self.stdout.write(
            self.style.SUCCESS(
                f"Digests — sent={result['sent']} skipped={result['skipped']} errors={result['errors']}"
            )
        )
