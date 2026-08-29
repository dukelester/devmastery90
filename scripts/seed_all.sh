#!/usr/bin/env bash
# Local / CI bootstrap: migrate + seed all content banks.
# Usage:
#   ./scripts/seed_all.sh
#   ./scripts/seed_all.sh --force
#   FORCE_SEED=1 ./scripts/seed_all.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python}"
if [[ -x "./venv/bin/python" ]]; then
  PYTHON="./venv/bin/python"
elif [[ -x "./.venv/bin/python" ]]; then
  PYTHON="./.venv/bin/python"
fi

ARGS=("$@")
if [[ "${FORCE_SEED:-0}" == "1" || "${FORCE_SEED:-0}" == "true" ]]; then
  ARGS+=(--force)
fi

echo "==> migrate"
"$PYTHON" manage.py migrate --noinput

echo "==> seed_program ${ARGS[*]:-}"
"$PYTHON" manage.py seed_program "${ARGS[@]+"${ARGS[@]}"}"

echo "==> Done. All curriculum + content banks are seeded."
