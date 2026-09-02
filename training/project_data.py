"""Detailed curriculum / portfolio project briefs for the Projects hub."""

PROJECTS = [
    {
        "slug": "ai-document-processing-platform",
        "name": "AI Document Processing Platform",
        "tagline": "Multi-tenant document ingestion, OCR/LLM extraction, and async workflows.",
        "overview": (
            "Build a production-shaped SaaS that accepts document uploads, runs background "
            "extraction jobs, stores artifacts in object storage, and exposes a tenant-safe API."
        ),
        "problem_statement": (
            "Teams drown in PDFs and scans. They need a secure multi-tenant system that "
            "ingests files, extracts structured fields with AI assistance, and notifies "
            "downstream systems without blocking the request path."
        ),
        "difficulty": "expert",
        "estimated_hours": 80,
        "week_focus": 9,
        "order": 1,
        "is_featured": True,
        "tech_stack": [
            "Python 3.12",
            "Django / DRF",
            "PostgreSQL",
            "Redis",
            "Celery",
            "S3-compatible storage",
            "Docker",
        ],
        "learning_outcomes": [
            "Design multi-tenant data isolation",
            "Model async job lifecycles with Celery",
            "Secure file upload and signed download flows",
            "Ship observability (logs, metrics, correlation IDs)",
            "Write acceptance tests for critical paths",
        ],
        "features": [
            {"title": "Tenant workspaces", "description": "Org-scoped users, roles, and data boundaries."},
            {"title": "Upload pipeline", "description": "Direct-to-storage or proxied uploads with virus-scan hook points."},
            {"title": "Extraction jobs", "description": "Queued OCR/LLM extraction with retries and dead-letter handling."},
            {"title": "Review UI", "description": "Human-in-the-loop correction of extracted fields."},
            {"title": "Webhooks", "description": "Signed outbound events when jobs complete or fail."},
        ],
        "functional_requirements": [
            "Users can create/join an organization and invite members",
            "Authenticated users can upload documents within quota limits",
            "Uploads enqueue an extraction job within 2 seconds",
            "Job status is queryable (queued, running, succeeded, failed)",
            "Extracted fields are editable and versioned",
            "Admins can revoke access and soft-delete documents",
        ],
        "non_functional_requirements": [
            "P95 upload ACK under 500ms excluding transfer time",
            "Tenant isolation enforced at the query layer (no cross-tenant leaks)",
            "Idempotent webhook delivery with signature verification",
            "Structured JSON logs with request/job correlation IDs",
            "Horizontal worker scale without duplicate side effects",
            "Defined SLOs: availability ≥ 99.5%, extraction success ≥ 98% excluding poison files",
            "Chaos: kill a worker mid-job; job recovers or fails cleanly with DLQ path",
            "Cost envelope documented for 10× document volume (storage + worker hours)",
            "Security: virus-scan hook or documented compensating control; signed download URLs expire",
        ],
        "acceptance_criteria": [
            {"id": "ac-tenant", "text": "Two tenants cannot read each other's documents via API or UI", "required": True},
            {"id": "ac-upload", "text": "Upload creates a Document row and an ExtractionJob in queued state", "required": True},
            {"id": "ac-async", "text": "Extraction runs in a Celery worker, not the web request thread", "required": True},
            {"id": "ac-retry", "text": "Failed jobs retry with backoff and land in a failed terminal state", "required": True},
            {"id": "ac-authz", "text": "Role-based permissions cover owner/admin/member for mutations", "required": True},
            {"id": "ac-tests", "text": "Automated tests cover isolation, upload→job, and webhook signing", "required": True},
            {"id": "ac-docs", "text": "README documents local run, env vars, and architecture diagram", "required": True},
            {"id": "ac-load", "text": "Load-test notes show p95 job enqueue latency and worker saturation point", "required": True},
            {"id": "ac-postmortem", "text": "One tabletop/postmortem for a simulated extraction outage is in the repo", "required": True},
            {"id": "ac-adr", "text": "At least two ADRs cover tenancy and async job design", "required": True},
            {"id": "ac-docker", "text": "docker compose brings up web, worker, postgres, redis, and storage", "required": False},
        ],
        "milestones": [
            {"title": "M1 — Foundations", "hours": 12, "deliverables": ["Repo scaffold", "Auth + orgs", "CI green"]},
            {"title": "M2 — Ingestion", "hours": 16, "deliverables": ["Upload API", "Object storage", "Quotas"]},
            {"title": "M3 — Async extraction", "hours": 20, "deliverables": ["Celery jobs", "Retries", "Status API"]},
            {"title": "M4 — Product polish", "hours": 16, "deliverables": ["Review UI", "Webhooks", "Hardening"]},
            {"title": "M5 — Ship", "hours": 16, "deliverables": ["Tests", "Docs", "Demo script"]},
        ],
        "deliverables": [
            "Source repository with clear module boundaries",
            "OpenAPI or documented REST endpoints",
            "Seed data + demo script for a 5-minute walkthrough",
            "Architecture notes covering tenancy and failure modes",
        ],
        "getting_started": (
            "1. Scaffold Django + DRF with org/user models.\n"
            "2. Add S3 (or MinIO) storage backend and Document model.\n"
            "3. Wire Celery + Redis; create ExtractionJob state machine.\n"
            "4. Implement tenant-scoped querysets and permission classes.\n"
            "5. Add review UI and webhook dispatcher last."
        ),
        "architecture_notes": (
            "Prefer org_id on every tenant-owned row. Keep extraction workers "
            "idempotent by job_id. Store raw files immutably; write extraction "
            "results as new versions. Use outbox or signed retry-safe webhooks."
        ),
        "resources": [
            {"title": "Celery first steps", "url": "https://docs.celeryq.dev/en/stable/getting-started/"},
            {"title": "Django multi-tenancy patterns", "url": "https://docs.djangoproject.com/en/stable/"},
        ],
    },
    {
        "slug": "url-shortener-at-scale",
        "name": "URL Shortener at Scale",
        "tagline": "Low-latency redirects with analytics, custom domains, and abuse controls.",
        "overview": (
            "Implement a short-link service optimized for redirect hot path, with click "
            "analytics shipped asynchronously and admin tooling for abuse."
        ),
        "problem_statement": (
            "Marketing and product teams need shareable short links that redirect in "
            "milliseconds, track campaigns, and survive traffic spikes without melting the DB."
        ),
        "difficulty": "hard",
        "estimated_hours": 35,
        "week_focus": 8,
        "order": 2,
        "is_featured": True,
        "tech_stack": ["Python", "Django/FastAPI", "PostgreSQL", "Redis", "CDN"],
        "learning_outcomes": [
            "Separate write path from ultra-hot read/redirect path",
            "Use caching and key design for collision-safe codes",
            "Stream analytics off the critical path",
        ],
        "features": [
            {"title": "Shorten API", "description": "Create codes with optional custom alias and TTL."},
            {"title": "Redirect", "description": "301/302 with cacheable responses."},
            {"title": "Analytics", "description": "Click counts and referrer aggregates (async)."},
            {"title": "Abuse tools", "description": "Disable links and rate-limit creators."},
        ],
        "functional_requirements": [
            "Create short links with unique codes",
            "Resolve codes to destination URLs",
            "Record clicks without blocking redirect beyond a small budget",
            "Owner can disable a link",
        ],
        "non_functional_requirements": [
            "Redirect P95 under 50ms from warm cache",
            "No duplicate codes under concurrent creates",
            "Analytics eventual consistency acceptable within seconds",
            "Hot-path stays online if analytics queue is down (degrade gracefully)",
            "Abuse: creator rate limits + disable-link kill switch under 1s effect",
            "Capacity sheet for 10k QPS redirect with cache hit-ratio assumptions",
        ],
        "acceptance_criteria": [
            {"id": "ac-create", "text": "POST create returns code and fully qualified short URL", "required": True},
            {"id": "ac-redirect", "text": "GET /{code} redirects to destination with correct status", "required": True},
            {"id": "ac-cache", "text": "Hot codes are served from Redis (or equivalent) cache", "required": True},
            {"id": "ac-analytics", "text": "Click events are persisted asynchronously", "required": True},
            {"id": "ac-disable", "text": "Disabled links return 410/404 and stop counting", "required": True},
            {"id": "ac-tests", "text": "Concurrency test proves unique code allocation", "required": True},
            {"id": "ac-bench", "text": "Benchmark doc includes methodology and p95 redirect numbers", "required": True},
            {"id": "ac-degrade", "text": "Demo or test shows redirects succeed when analytics worker is stopped", "required": True},
        ],
        "milestones": [
            {"title": "M1 — Core API", "hours": 10, "deliverables": ["Models", "Create/resolve"]},
            {"title": "M2 — Speed", "hours": 10, "deliverables": ["Cache layer", "Benchmarks"]},
            {"title": "M3 — Analytics + abuse", "hours": 15, "deliverables": ["Async pipeline", "Admin disable"]},
        ],
        "deliverables": ["Repo", "Load-test notes", "README with latency methodology"],
        "getting_started": (
            "Start with the redirect path. Prove uniqueness. Add Redis. Only then pipe "
            "analytics through a queue."
        ),
        "architecture_notes": (
            "Treat redirect as read-mostly. Prefer cache-aside. Persist clicks via queue "
            "to avoid write amplification on the hot path."
        ),
        "resources": [
            {"title": "HTTP caching", "url": "https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching"},
        ],
    },
    {
        "slug": "observability-ready-api",
        "name": "Observability-Ready REST API",
        "tagline": "A Django API with tracing, structured logs, SLOs, and chaos-friendly health checks.",
        "overview": (
            "Take a small domain API and harden it for production operations: correlation IDs, "
            "metrics, health/readiness, and error budgets documented in an SLO sheet."
        ),
        "problem_statement": (
            "Features ship faster than operators can debug them. Build an API that is "
            "operable on day one with clear signals when it is healthy, degraded, or down."
        ),
        "difficulty": "hard",
        "estimated_hours": 36,
        "week_focus": 10,
        "order": 3,
        "is_featured": False,
        "tech_stack": ["Django", "DRF", "PostgreSQL", "Prometheus/OpenTelemetry", "Docker"],
        "learning_outcomes": [
            "Instrument request lifecycle with correlation IDs",
            "Define SLIs/SLOs for latency and error rate",
            "Separate liveness vs readiness probes",
        ],
        "features": [
            {"title": "CRUD domain API", "description": "At least one resource with list/detail/create/update."},
            {"title": "Correlation", "description": "Propagate X-Request-ID across logs."},
            {"title": "Health endpoints", "description": "/healthz and /readyz with dependency checks."},
            {"title": "Metrics", "description": "Request count, latency histogram, error counter."},
        ],
        "functional_requirements": [
            "CRUD endpoints with auth",
            "Health endpoints return machine-readable JSON",
            "Every response includes a request id header",
        ],
        "non_functional_requirements": [
            "Documented SLO for availability and latency with error-budget policy",
            "Logs are structured JSON with correlation IDs",
            "Readiness fails when DB is unreachable",
            "Chaos: dependency failure surfaces on /readyz without crashing the process",
            "Alert definitions are actionable (symptom + next step), not raw metric noise",
            "p95 latency budget stated and verified under a small load test",
        ],
        "acceptance_criteria": [
            {"id": "ac-crud", "text": "Authenticated CRUD works with validation errors as 400", "required": True},
            {"id": "ac-rid", "text": "Responses include X-Request-ID and logs contain the same id", "required": True},
            {"id": "ac-ready", "text": "/readyz fails closed when database is down", "required": True},
            {"id": "ac-metrics", "text": "Metrics endpoint or exporter exposes latency + errors", "required": True},
            {"id": "ac-slo", "text": "SLO sheet checked into repo with error-budget policy", "required": True},
            {"id": "ac-runbook", "text": "On-call runbook covers SEV definitions and first 15 minutes", "required": True},
            {"id": "ac-chaos", "text": "Documented chaos check for DB down / high latency path", "required": True},
        ],
        "milestones": [
            {"title": "M1 — API", "hours": 8, "deliverables": ["Resource + auth"]},
            {"title": "M2 — Signals", "hours": 10, "deliverables": ["Logs", "Metrics", "Health"]},
            {"title": "M3 — Ops pack", "hours": 10, "deliverables": ["SLO doc", "Runbook"]},
        ],
        "deliverables": ["API", "Runbook", "SLO sheet", "Docker compose"],
        "getting_started": "Implement CRUD first, then middleware for request IDs, then probes and metrics.",
        "architecture_notes": "Keep probe handlers cheap. Never block readiness on non-critical deps.",
        "resources": [
            {"title": "Google SRE — SLOs", "url": "https://sre.google/sre-book/service-level-objectives/"},
        ],
    },
    {
        "slug": "realtime-collab-notes",
        "name": "Realtime Collaborative Notes",
        "tagline": "Presence, conflict-aware edits, and websocket fanout for shared documents.",
        "overview": (
            "Build a notes app where multiple users see presence and near-realtime updates, "
            "with a clear story for conflict resolution and reconnect."
        ),
        "problem_statement": (
            "Async docs lose the room energy of pair work. Provide a lightweight collaborative "
            "surface that stays correct under reconnects and overlapping edits."
        ),
        "difficulty": "hard",
        "estimated_hours": 45,
        "week_focus": 7,
        "order": 4,
        "is_featured": True,
        "tech_stack": ["Django Channels / WS", "Redis", "PostgreSQL", "HTMX or SPA client"],
        "learning_outcomes": [
            "Model presence and ephemeral sessions",
            "Broadcast events safely through a channel layer",
            "Handle reconnect, ordering, and basic conflict policy",
        ],
        "features": [
            {"title": "Documents", "description": "Create/share notes with roles."},
            {"title": "Presence", "description": "See who is viewing/editing."},
            {"title": "Live updates", "description": "Propagate patches or snapshots over WS."},
            {"title": "History", "description": "Simple revision list or snapshot restore."},
        ],
        "functional_requirements": [
            "Users can create and share a document",
            "Editors receive remote changes without full page reload",
            "Presence list updates on join/leave",
            "Unauthorized users cannot subscribe to a document channel",
        ],
        "non_functional_requirements": [
            "Authn on websocket connect",
            "Reconnect restores recent state within documented bounds",
            "Server rejects oversized patches",
        ],
        "acceptance_criteria": [
            {"id": "ac-share", "text": "Owner can grant editor/viewer access", "required": True},
            {"id": "ac-live", "text": "Two browsers show remote edits without refresh", "required": True},
            {"id": "ac-presence", "text": "Presence updates within a few seconds of join/leave", "required": True},
            {"id": "ac-authws", "text": "Unauthenticated websocket upgrade is rejected", "required": True},
            {"id": "ac-conflict", "text": "Conflict policy documented and covered by a test or demo", "required": True},
        ],
        "milestones": [
            {"title": "M1 — Docs CRUD", "hours": 10, "deliverables": ["Models", "Permissions"]},
            {"title": "M2 — Realtime", "hours": 20, "deliverables": ["WS", "Presence", "Broadcast"]},
            {"title": "M3 — Resilience", "hours": 15, "deliverables": ["Reconnect", "Tests", "Docs"]},
        ],
        "deliverables": ["Working demo", "Sequence diagram", "Threat notes for WS auth"],
        "getting_started": "Ship CRUD + permissions before websockets. Add presence next, then patches.",
        "architecture_notes": "Authorize every subscribe. Prefer room names that embed document id + ACL check.",
        "resources": [
            {"title": "Django Channels", "url": "https://channels.readthedocs.io/"},
        ],
    },
    {
        "slug": "interview-ready-portfolio-api",
        "name": "Interview-Ready Portfolio API",
        "tagline": "A polished personal API + docs site you can defend in system design interviews.",
        "overview": (
            "Create a personal portfolio backend with projects, skills, and case studies, "
            "complete with OpenAPI, seed data, and a story for scaling reads."
        ),
        "problem_statement": (
            "Interviewers ask you to show production judgment. Ship a small but complete "
            "API that demonstrates modeling, auth, caching, and documentation quality."
        ),
        "difficulty": "medium",
        "estimated_hours": 24,
        "week_focus": 12,
        "order": 5,
        "is_featured": False,
        "tech_stack": ["Django", "DRF", "PostgreSQL", "OpenAPI", "Whitenoise/CDN"],
        "learning_outcomes": [
            "Design clean resource models",
            "Publish OpenAPI that matches reality",
            "Explain caching and pagination choices",
        ],
        "features": [
            {"title": "Projects API", "description": "List/detail with tech tags and case-study fields."},
            {"title": "Skills API", "description": "Categorized skills with proficiency."},
            {"title": "Public docs", "description": "Browsable OpenAPI / Redoc."},
        ],
        "functional_requirements": [
            "Public read endpoints for published content",
            "Authenticated write endpoints for the owner",
            "Pagination on list endpoints",
        ],
        "non_functional_requirements": [
            "OpenAPI stays in sync with serializers",
            "List endpoints support filtering by tag",
            "Cache-Control or Redis cache for public lists",
        ],
        "acceptance_criteria": [
            {"id": "ac-public", "text": "Anonymous clients can list published projects", "required": True},
            {"id": "ac-auth", "text": "Writes require authentication and ownership checks", "required": True},
            {"id": "ac-openapi", "text": "OpenAPI documents all public endpoints accurately", "required": True},
            {"id": "ac-page", "text": "List endpoints paginate and return stable ordering", "required": True},
            {"id": "ac-story", "text": "README includes a 2-minute interview talking track", "required": True},
        ],
        "milestones": [
            {"title": "M1 — Models + API", "hours": 10, "deliverables": ["Resources", "Auth"]},
            {"title": "M2 — Docs + polish", "hours": 14, "deliverables": ["OpenAPI", "Cache", "Talk track"]},
        ],
        "deliverables": ["Repo", "Seed command", "Interview talking track"],
        "getting_started": "Model Project and Skill, add DRF viewsets, then OpenAPI and seed data.",
        "architecture_notes": "Keep public serializers lean. Don't leak draft content.",
        "resources": [
            {"title": "DRF spectacular / OpenAPI", "url": "https://www.django-rest-framework.org/"},
        ],
    },
]
