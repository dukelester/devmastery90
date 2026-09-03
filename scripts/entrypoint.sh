#!/usr/bin/env bash
# Docker / production entrypoint: wait for DB, migrate, seed, then exec the app command.
set -euo pipefail

cd /app 2>/dev/null || cd "$(dirname "$0")/.."

PYTHON="${PYTHON:-python}"
if [[ -x "./venv/bin/python" ]]; then
  PYTHON="./venv/bin/python"
elif [[ -x "./.venv/bin/python" ]]; then
  PYTHON="./.venv/bin/python"
fi

echo "==> Waiting for database..."
"$PYTHON" <<'PY'
import os, sys, time
import django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.development"),
)
django.setup()
from django.db import connection
from django.db.utils import OperationalError

for attempt in range(1, 61):
    try:
        connection.ensure_connection()
        print(f"Database ready (attempt {attempt}).")
        break
    except OperationalError as exc:
        if attempt == 60:
            print(f"Database unavailable after 60 attempts: {exc}", file=sys.stderr)
            sys.exit(1)
        time.sleep(1)
PY

echo "==> Repairing migration bookkeeping if needed..."
"$PYTHON" <<'PY'
"""Fix orphan django_migrations_id_seq (table missing, sequence left behind)."""
import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.development"),
)
django.setup()
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute(
        """
        SELECT
          to_regclass('public.django_migrations') IS NOT NULL AS has_table,
          to_regclass('public.django_migrations_id_seq') IS NOT NULL AS has_seq
        """
    )
    has_table, has_seq = cursor.fetchone()
    if has_seq and not has_table:
        print("Found orphan django_migrations_id_seq — dropping so migrate can recreate.")
        cursor.execute("DROP SEQUENCE IF EXISTS public.django_migrations_id_seq CASCADE")
    elif has_table and has_seq:
        # Ensure the sequence is owned by the table column (avoids recreate races).
        cursor.execute(
            """
            SELECT pg_get_serial_sequence('public.django_migrations', 'id')
            """
        )
        owned = cursor.fetchone()[0]
        if not owned:
            print("Re-linking django_migrations.id to django_migrations_id_seq")
            cursor.execute(
                """
                ALTER SEQUENCE public.django_migrations_id_seq
                  OWNED BY public.django_migrations.id
                """
            )
    print(
        f"django_migrations table={'yes' if has_table else 'no'}, "
        f"sequence={'yes' if has_seq else 'no'}"
    )
PY

echo "==> Running migrations (advisory lock)..."
"$PYTHON" <<'PY'
"""Serialize migrate across web/worker/beat so they don't race table creation."""
import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.get("DJANGO_SETTINGS_MODULE", "config.settings.development"),
)
django.setup()
from django.core.management import call_command
from django.db import connection

LOCK_KEY = 90422190  # arbitrary stable key for DevMastery migrate
with connection.cursor() as cursor:
    cursor.execute("SELECT pg_advisory_lock(%s)", [LOCK_KEY])
    try:
        call_command("migrate", interactive=False, verbosity=1)
    finally:
        cursor.execute("SELECT pg_advisory_unlock(%s)", [LOCK_KEY])
PY

SKIP_SEED="${SKIP_SEED:-0}"
if [[ "$SKIP_SEED" != "1" && "$SKIP_SEED" != "true" ]]; then
  FORCE_SEED="${FORCE_SEED:-0}"
  SEED_ARGS=()
  if [[ "$FORCE_SEED" == "1" || "$FORCE_SEED" == "true" ]]; then
    SEED_ARGS+=(--force)
  fi
  echo "==> Seeding program data..."
  if [[ ${#SEED_ARGS[@]} -gt 0 ]]; then
    "$PYTHON" manage.py seed_program "${SEED_ARGS[@]}"
  else
    "$PYTHON" manage.py seed_program
  fi
else
  echo "==> Skipping seed (SKIP_SEED=${SKIP_SEED})."
fi

if [[ "${COLLECTSTATIC:-0}" == "1" || "${COLLECTSTATIC:-0}" == "true" ]]; then
  echo "==> Collecting static files..."
  "$PYTHON" manage.py collectstatic --noinput
fi

echo "==> Bootstrap complete."
if [[ $# -eq 0 ]]; then
  echo "No command provided to entrypoint." >&2
  exit 1
fi
exec "$@"
