# DevMastery 90

A production-quality Django + HTMX adaptive software engineering training platform for 90-day mastery and interview preparation.

## Features

- **90-day structured curriculum** — Python, DSA, Django, PostgreSQL, Redis, System Design, and interview prep
- **Adaptive weakness engine** — Skill health scoring based on assessments, coding, mistakes, and confidence
- **Daily recommendations** — Prioritized study plan based on weaknesses, overdue tasks, and curriculum
- **HTMX-powered UI** — Task completion, timer, coding tracker, interview practice without page reloads
- **Study timer** — Track sessions linked to tasks and skills
- **Coding tracker** — Pattern-based performance analysis
- **Interview system** — Practice questions with self-scoring across 11 categories
- **Analytics dashboard** — Study hours, skill trends, assessment performance
- **90-day calendar** — Visual progress with HTMX day details
- **Gamification** — XP, levels, streaks (professional, not childish)
- **DRF API** — Full REST API with authentication and filtering
- **Docker Compose** — PostgreSQL, Redis, Celery, Nginx, Gunicorn

## Quick Start

### Docker (recommended)

```bash
cp .env.example .env
docker compose up --build
```

The app runs at http://localhost:8000 (or http://localhost via Nginx).

On every web container start the entrypoint automatically:
1. Waits for PostgreSQL
2. Runs `migrate`
3. Runs `seed_program` (curriculum + practice + engineering labs + mock interviews + cognitive)

Idempotent by default. To force-refresh content banks:

```bash
FORCE_SEED=1 docker compose up web
```

### Local Development

Requirements: Python 3.12+, PostgreSQL 16+, Redis (optional for dev).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Start PostgreSQL (and Redis) — e.g. docker compose up postgres redis -d
./scripts/bootstrap.sh          # migrate + seed everything
# or: ./scripts/seed_all.sh --force

python manage.py createsuperuser
python manage.py runserver
```

Equivalent one-liner:

```bash
python manage.py migrate && python manage.py seed_program
```

`seed_program` seeds all of:
- 90-day curriculum (phases, weeks, days, tasks, skills)
- Practice interview bank (`seed_practice`)
- Engineering labs (`seed_engineering`)
- Mock interviews (`seed_mock_interviews`)
- Aptitude & brain teasers (`seed_cognitive`)

Flags: `--force` (refresh content banks), `--content-only`, `--curriculum-only`.

## Usage

1. Register or login at `/register/` or `/login/`
2. **Dashboard** (`/dashboard/`) — Overview, today's mission, weaknesses, recommendations
3. **Today** (`/today/`) — Execute daily tasks with HTMX completion, timer, and daily review
4. **Coding** (`/coding/`) — Track problems by pattern and difficulty
5. **Interview** (`/interview/`) — Practice and self-score interview questions
6. **Analytics** (`/analytics/`) — Study hours, skill trends, performance
7. **Calendar** (`/calendar/`) — 90-day visual calendar

## API Endpoints

All endpoints require authentication (session-based).

| Endpoint | Description |
|----------|-------------|
| `/api/skills/` | List skills |
| `/api/tasks/` | CRUD tasks |
| `/api/study-sessions/` | Study sessions |
| `/api/assessments/` | Assessments |
| `/api/coding-problems/` | Coding problems |
| `/api/progress/` | Overall progress |
| `/api/analytics/` | Analytics data |
| `/api/recommendations/` | Daily recommendations |
| `/api/streak/` | Streak data |
| `/api/skill-health/` | Skill health scores |

## Testing

```bash
pytest
pytest --cov=training
```

## Architecture

```
config/          Django settings, URLs, Celery
training/        Main app
  models.py      15 data models
  services.py    Business logic (progress, skill health, recommendations)
  views.py       HTMX views
  api_views.py   DRF viewsets
  curriculum_data.py  90-day curriculum definitions
templates/       Django templates with HTMX partials
```

## Production (server IP, web access)

Deploy with Docker so the app is reachable at `http://YOUR_SERVER_IP/` on port 80.

### 1. On the server

```bash
# Install Docker + Compose plugin, then clone/copy the project
git clone <your-repo-url> DevMastery && cd DevMastery

# One-shot deploy (writes .env, builds, starts nginx + app + db)
chmod +x scripts/deploy.sh
./scripts/deploy.sh YOUR_SERVER_IP
```

Or manually:

```bash
cp .env.production.example .env
# Edit .env — set SECRET_KEY, POSTGRES_PASSWORD, and replace YOUR_SERVER_IP
docker compose -f docker-compose.prod.yml --env-file .env up -d --build
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
```

### 2. Firewall

Allow inbound HTTP (and SSH):

```bash
# ufw example
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw enable
```

Cloud providers: open **TCP 80** in the security group / firewall for the instance.

### 3. Verify

- Browser: `http://YOUR_SERVER_IP/`
- Health / logs: `docker compose -f docker-compose.prod.yml logs -f web nginx`

### Important `.env` values

| Variable | Purpose |
|----------|---------|
| `ALLOWED_HOSTS` | Must include the server IP |
| `CSRF_TRUSTED_ORIGINS` | `http://YOUR_SERVER_IP` (required for login forms) |
| `SECRET_KEY` | Long random string |
| `POSTGRES_PASSWORD` | Strong password |
| `SECURE_SSL_REDIRECT` | Keep `False` until you add HTTPS |

HTTPS later: put a domain on the IP, terminate TLS (Caddy/Certbot/Cloudflare), then set `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, and `CSRF_TRUSTED_ORIGINS=https://your.domain`.

## Curriculum Structure

- **Phase 1** (Days 1–30): Python + Problem Solving
- **Phase 2** (Days 31–60): Production Backend Engineering
- **Phase 3** (Days 61–90): Elite Engineering + Interview Prep

12 weeks, 90 days, 300+ actionable tasks seeded via `python manage.py seed_program`.
