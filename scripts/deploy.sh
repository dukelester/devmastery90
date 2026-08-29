#!/usr/bin/env bash
# Deploy DevMastery 90 for access via a server IP (HTTP :80).
#
# Usage:
#   ./scripts/deploy.sh 203.0.113.10
#   ./scripts/deploy.sh 203.0.113.10 --force-seed
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

SERVER_IP=""
FORCE_SEED_FLAG=0
for arg in "$@"; do
  case "$arg" in
    --force-seed) FORCE_SEED_FLAG=1 ;;
    --help|-h)
      echo "Usage: $0 <SERVER_IP> [--force-seed]"
      exit 0
      ;;
    *)
      if [[ -z "$SERVER_IP" && "$arg" != --* ]]; then
        SERVER_IP="$arg"
      fi
      ;;
  esac
done

if [[ -z "$SERVER_IP" ]]; then
  echo "Usage: $0 <SERVER_IP> [--force-seed]" >&2
  echo "Example: $0 203.0.113.10" >&2
  exit 1
fi

if [[ ! -f .env ]]; then
  if [[ -f .env.production.example ]]; then
    echo "==> Creating .env from .env.production.example"
    cp .env.production.example .env
  else
    echo "Missing .env — copy .env.production.example to .env first." >&2
    exit 1
  fi
fi

echo "==> Applying server IP ${SERVER_IP} to .env (if placeholders present)"
python3 - <<PY
import re
import secrets
from pathlib import Path

ip = "${SERVER_IP}"
path = Path(".env")
text = path.read_text()

if "REPLACE_WITH_A_LONG_RANDOM_STRING" in text or re.search(
    r"^SECRET_KEY=(change-me-in-production|REPLACE_)", text, re.M
):
    key = secrets.token_urlsafe(50)
    text = re.sub(r"^SECRET_KEY=.*$", f"SECRET_KEY={key}", text, count=1, flags=re.M)
    print("Generated SECRET_KEY")

if "REPLACE_WITH_STRONG_DB_PASSWORD" in text:
    text = text.replace("REPLACE_WITH_STRONG_DB_PASSWORD", secrets.token_urlsafe(24))
    print("Generated POSTGRES_PASSWORD")

text = text.replace("YOUR_SERVER_IP", ip)

# Ensure ALLOWED_HOSTS / CSRF include this IP even if placeholders were already replaced
if f"ALLOWED_HOSTS=" in text and ip not in text:
    text = re.sub(
        r"^ALLOWED_HOSTS=.*$",
        f"ALLOWED_HOSTS={ip},localhost,127.0.0.1",
        text,
        count=1,
        flags=re.M,
    )
if "CSRF_TRUSTED_ORIGINS=" in text and f"http://{ip}" not in text:
    text = re.sub(
        r"^CSRF_TRUSTED_ORIGINS=.*$",
        f"CSRF_TRUSTED_ORIGINS=http://{ip}",
        text,
        count=1,
        flags=re.M,
    )

# Production defaults
text = re.sub(r"^DEBUG=.*$", "DEBUG=False", text, count=1, flags=re.M)
if "DJANGO_SETTINGS_MODULE=" in text:
    text = re.sub(
        r"^DJANGO_SETTINGS_MODULE=.*$",
        "DJANGO_SETTINGS_MODULE=config.settings.production",
        text,
        count=1,
        flags=re.M,
    )
else:
    text += "\nDJANGO_SETTINGS_MODULE=config.settings.production\n"

path.write_text(text)
print("Wrote .env")
PY

export FORCE_SEED=0
if [[ "$FORCE_SEED_FLAG" == "1" ]]; then
  export FORCE_SEED=1
fi

echo "==> Building and starting production stack"
docker compose -f docker-compose.prod.yml --env-file .env up -d --build

echo "==> Waiting for containers..."
sleep 8
docker compose -f docker-compose.prod.yml ps

echo ""
echo "Open in a browser:  http://${SERVER_IP}/"
echo ""
echo "Create admin user:"
echo "  docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser"
echo ""
echo "Follow logs:"
echo "  docker compose -f docker-compose.prod.yml logs -f web nginx"
