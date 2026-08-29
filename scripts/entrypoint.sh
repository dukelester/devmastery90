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

echo "==> Running migrations..."
"$PYTHON" manage.py migrate --noinput

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
