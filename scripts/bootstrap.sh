#!/usr/bin/env bash
# Convenience local bootstrap (venv optional).
# Usage: ./scripts/bootstrap.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env && -f .env.example ]]; then
  cp .env.example .env
  echo "Created .env from .env.example"
fi

exec "$ROOT/scripts/seed_all.sh" "$@"
