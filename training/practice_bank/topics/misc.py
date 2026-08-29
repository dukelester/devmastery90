"""Topic banks for REST, PostgreSQL, System Design, Testing, DevOps, Cloud, AI, Behavioral."""

REST_TOPICS = [
    {
        "question": "Design RESTful endpoints for a `users` resource with proper HTTP verbs.",
        "ideal_topics": "resources, HTTP methods, CRUD",
        "solution_code": '''# RESTful mapping
GET    /users          → list users
POST   /users          → create user
GET    /users/{id}     → retrieve user
PUT    /users/{id}     → replace user
PATCH  /users/{id}     → partial update
DELETE /users/{id}     → delete user''',
        "solution_explanation": "URLs identify resources; HTTP methods express actions on resources.",
        "hints": "Avoid verbs in URLs like /getUsers.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Return appropriate HTTP status codes for common API outcomes.",
        "ideal_topics": "status codes, 201, 204, 409, 422",
        "solution_code": '''# 200 OK — successful GET/PUT/PATCH with body
# 201 Created — POST created resource (+ Location header)
# 204 No Content — successful DELETE or update without body
# 400 Bad Request — malformed input
# 401 Unauthorized — authentication required
# 403 Forbidden — authenticated but not allowed
# 404 Not Found — resource missing
# 409 Conflict — duplicate or state conflict
# 422 Unprocessable Entity — validation errors
# 429 Too Many Requests — rate limited
# 500 Internal Server Error — unexpected server fault''',
        "solution_explanation": "Consistent status codes help clients branch logic without parsing bodies.",
        "hints": "Include problem details (RFC 7807) in error responses.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Implement cursor-based pagination for stable large datasets.",
        "ideal_topics": "pagination, cursor, stable ordering",
        "solution_code": '''def paginate(queryset, cursor=None, limit=50):
    qs = queryset.order_by("id")
    if cursor:
        qs = qs.filter(id__gt=cursor)
    items = list(qs[: limit + 1])
    next_cursor = items[limit].id if len(items) > limit else None
    return items[:limit], next_cursor''',
        "solution_explanation": "Cursor pagination avoids OFFSET cost and duplicate/skipped rows on live data.",
        "hints": "Encode cursor as opaque base64 for clients.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Design filtering and sorting query parameters safely.",
        "ideal_topics": "filtering, allowlist, SQL injection",
        "solution_code": '''ALLOWED_FILTERS = {"status", "created_after"}
ALLOWED_SORT = {"created_at", "-created_at"}

def apply_filters(params, queryset):
    for key in ALLOWED_FILTERS:
        if key in params:
            queryset = queryset.filter(**{key: params[key]})
    sort = params.get("sort", "-created_at")
    if sort not in ALLOWED_SORT:
        raise ValidationError("invalid sort")
    return queryset.order_by(sort)''',
        "solution_explanation": "Allowlists prevent arbitrary field access and injection via order_by.",
        "hints": "Use django-filter for declarative filters.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Version a REST API using URL path versioning.",
        "ideal_topics": "versioning, backward compatibility",
        "solution_code": '''# urls_v1.py → /api/v1/users/
# urls_v2.py → /api/v2/users/  (new fields, breaking changes)

urlpatterns = [
    path("api/v1/", include("api.v1.urls")),
    path("api/v2/", include("api.v2.urls")),
]''',
        "solution_explanation": "URL versioning is explicit; clients pin to /v1/ until they migrate.",
        "hints": "Header versioning (Accept: application/vnd...) is alternative.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Document error response shape for validation failures.",
        "ideal_topics": "error format, validation, JSON schema",
        "solution_code": '''{
  "type": "validation_error",
  "title": "Invalid request",
  "status": 422,
  "errors": [
    {"field": "email", "message": "invalid format"},
    {"field": "age", "message": "must be >= 18"}
  ]
}''',
        "solution_explanation": "Structured errors let clients display field-level messages.",
        "hints": "Align with RFC 7807 Problem Details.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Implement HATEOAS links in list responses (conceptual).",
        "ideal_topics": "HATEOAS, hypermedia, links",
        "solution_code": '''{
  "data": [{"id": "u1", "name": "Alice"}],
  "links": {
    "self": "/api/users?page=2",
    "next": "/api/users?page=3",
    "prev": "/api/users?page=1"
  }
}''',
        "solution_explanation": "Hypermedia links guide clients without hardcoded URL construction.",
        "hints": "HAL and JSON:API are common link standards.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Handle idempotent POST with Idempotency-Key header.",
        "ideal_topics": "idempotency, payments, retries",
        "solution_code": '''def create_payment(request):
    key = request.headers.get("Idempotency-Key")
    if not key:
        return Response({"error": "missing key"}, status=400)
    existing = Payment.objects.filter(idempotency_key=key).first()
    if existing:
        return Response(serializer(existing).data, status=200)
    payment = Payment.objects.create(...)
    return Response(serializer(payment).data, status=201)''',
        "solution_explanation": "Same key returns same result — safe for client retries.",
        "hints": "Stripe and many payment APIs require this header.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Compare PUT vs PATCH for partial updates.",
        "ideal_topics": "PUT, PATCH, partial update",
        "solution_code": '''# PUT — replace entire resource (missing fields may null out)
# PATCH — apply partial diff

# PATCH example body:
{"status": "shipped"}  # only updates status field''',
        "solution_explanation": "PATCH reduces accidental field wipes; PUT expects full representation.",
        "hints": "Use merge_patch or json_patch for formal patch formats.",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Design bulk operations endpoint with transaction boundaries.",
        "ideal_topics": "bulk, transactions, batch",
        "solution_code": '''@transaction.atomic
def bulk_update(request):
    items = request.data.get("items", [])
    if len(items) > 100:
        return Response({"error": "max 100 items"}, status=400)
    for item in items:
        Order.objects.filter(id=item["id"]).update(status=item["status"])
    return Response({"updated": len(items)})''',
        "solution_explanation": "Cap batch size; atomic block ensures all-or-nothing per request.",
        "hints": "Return per-item errors for partial success pattern.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Explain CORS and configure allowed origins for a browser SPA API.",
        "ideal_topics": "CORS, preflight, Access-Control",
        "solution_code": '''# Django: django-cors-headers
CORS_ALLOWED_ORIGINS = [
    "https://app.example.com",
]
CORS_ALLOW_CREDENTIALS = True
# Browser sends OPTIONS preflight for non-simple requests''',
        "solution_explanation": "CORS is browser-enforced; servers must echo allowed origins on responses.",
        "hints": "Never use CORS_ALLOW_ALL_ORIGINS with credentials.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Secure API with JWT access + refresh token rotation.",
        "ideal_topics": "JWT, refresh tokens, rotation",
        "solution_code": '''# Login → access token (short TTL) + refresh token (longer, stored hashed)
# Refresh endpoint validates refresh, issues new pair, revokes old refresh
# Access token sent: Authorization: Bearer <token>''',
        "solution_explanation": "Short-lived access limits exposure; refresh rotation detects theft.",
        "hints": "Store refresh tokens hashed; bind to device fingerprint optionally.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Implement API request validation layer before business logic.",
        "ideal_topics": "validation, serializers, pydantic",
        "solution_code": '''class CreateUserInput(serializers.Serializer):
    email = serializers.EmailField()
    age = serializers.IntegerField(min_value=18)

def create_user(request):
    ser = CreateUserInput(data=request.data)
    ser.is_valid(raise_exception=True)
    data = ser.validated_data
    ...''',
        "solution_explanation": "Validate early; never pass raw request.data to ORM.",
        "hints": "DRF Serializer or pydantic for non-DRF stacks.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Design webhook delivery with retries and signature verification.",
        "ideal_topics": "webhooks, HMAC, retries",
        "solution_code": '''import hmac, hashlib

def sign_payload(secret, body: bytes) -> str:
    return hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

# Receiver verifies:
# expected = sign_payload(secret, request.body)
# hmac.compare_digest(expected, request.headers["X-Signature"])''',
        "solution_explanation": "HMAC proves payload integrity and origin. Retry with exponential backoff on 5xx.",
        "hints": "Include timestamp to prevent replay with tolerance window.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Rate limit API consumers per API key tier.",
        "ideal_topics": "rate limiting, tiers, quotas",
        "solution_code": '''TIERS = {"free": 100, "pro": 10000}

def check_quota(api_key):
    tier = api_key.tier
    limit = TIERS[tier]
    used = cache.get(f"quota:{api_key.id}", 0)
    if used >= limit:
        raise RateLimitExceeded()
    cache.set(f"quota:{api_key.id}", used + 1, timeout=86400)''',
        "solution_explanation": "Per-key counters with daily window enforce tier quotas.",
        "hints": "Return Retry-After header on 429.",
        "time_estimate_minutes": 16,
    },
]

POSTGRES_TOPICS = [
    {
        "question": "Write a query with INNER JOIN vs LEFT JOIN and explain difference.",
        "ideal_topics": "JOIN, INNER, LEFT, NULL handling",
        "solution_code": '''-- INNER: only matching rows from both tables
SELECT u.email, o.total
FROM users u
INNER JOIN orders o ON o.user_id = u.id;

-- LEFT: all users, NULL order columns if no order
SELECT u.email, o.total
FROM users u
LEFT JOIN orders o ON o.user_id = u.id;''',
        "solution_explanation": "INNER drops non-matching; LEFT preserves left table rows.",
        "hints": "Use LEFT when optional relationship.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Use CTE for readable multi-step analytics query.",
        "ideal_topics": "CTE, WITH, readability",
        "solution_code": '''WITH monthly AS (
    SELECT user_id, date_trunc('month', created_at) AS month, sum(total) AS revenue
    FROM orders
    GROUP BY user_id, date_trunc('month', created_at)
),
ranked AS (
    SELECT *, rank() OVER (PARTITION BY month ORDER BY revenue DESC) AS rnk
    FROM monthly
)
SELECT * FROM ranked WHERE rnk <= 10;''',
        "solution_explanation": "CTEs break complex SQL into named steps; can be optimization fence in PG.",
        "hints": "Recursive CTEs for hierarchies.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Create composite index matching query filter and sort order.",
        "ideal_topics": "composite index, B-tree, column order",
        "solution_code": '''-- Query: WHERE user_id = ? ORDER BY created_at DESC
CREATE INDEX idx_orders_user_created
ON orders (user_id, created_at DESC);

-- Leading column user_id narrows; created_at supports sort without extra sort step''',
        "solution_explanation": "Index column order must match equality filters first, then range/sort columns.",
        "hints": "Use EXPLAIN to verify Index Scan vs Seq Scan.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Interpret EXPLAIN ANALYZE output for a slow query.",
        "ideal_topics": "EXPLAIN, Seq Scan, Index Scan, cost",
        "solution_code": '''EXPLAIN ANALYZE
SELECT * FROM orders WHERE status = 'pending' AND created_at > now() - interval '7 days';

-- Look for:
-- Seq Scan on large tables (bad)
-- Rows Removed by Filter (index not selective enough)
-- actual time vs planning time
-- Buffers: shared hit/read''',
        "solution_explanation": "ANALYZE executes query; compare estimated vs actual rows for planner accuracy.",
        "hints": "Run ANALYZE on table after bulk changes.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Use partial index for hot subset of rows.",
        "ideal_topics": "partial index, WHERE clause on index",
        "solution_code": '''CREATE INDEX idx_orders_open
ON orders (created_at)
WHERE status IN ('pending', 'processing');

-- Smaller index, faster for queries filtering open orders only''',
        "solution_explanation": "Partial indexes target frequent queries on row subsets.",
        "hints": "Predicate must match query WHERE clause.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Demonstrate transaction with explicit BEGIN/COMMIT and rollback.",
        "ideal_topics": "transactions, ACID, rollback",
        "solution_code": '''BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
-- If any step fails:
ROLLBACK;
-- Else:
COMMIT;''',
        "solution_explanation": "Transactions group statements into atomic unit.",
        "hints": "Django: transaction.atomic() wrapper.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Explain isolation levels and phantom reads.",
        "ideal_topics": "isolation, MVCC, phantom read",
        "solution_code": '''-- PostgreSQL defaults to READ COMMITTED
-- REPEATABLE READ — snapshot for transaction duration
-- SERIALIZABLE — strictest, may raise serialization failures

SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;''',
        "solution_explanation": "MVCC gives readers non-blocking view; higher isolation reduces anomalies.",
        "hints": "Retry on serialization_failure in SERIALIZABLE.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Use window functions for running totals.",
        "ideal_topics": "window functions, OVER, running sum",
        "solution_code": '''SELECT
    created_at,
    total,
    sum(total) OVER (ORDER BY created_at) AS running_total
FROM orders
WHERE user_id = 42
ORDER BY created_at;''',
        "solution_explanation": "OVER defines window; ORDER BY in window sets accumulation order.",
        "hints": "PARTITION BY for per-group windows.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Design normalization for orders, order_items, products (3NF).",
        "ideal_topics": "normalization, 3NF, foreign keys",
        "solution_code": '''-- products(id, name, price)
-- orders(id, user_id, status, created_at)
-- order_items(id, order_id, product_id, quantity, unit_price)
-- unit_price snapshotted — product price changes don't affect past orders''',
        "solution_explanation": "Separate entities remove redundancy; snapshot prices preserve history.",
        "hints": "Denormalize selectively for read performance.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Implement optimistic locking with version column.",
        "ideal_topics": "optimistic locking, version, concurrency",
        "solution_code": '''UPDATE products
SET stock = stock - 1, version = version + 1
WHERE id = 5 AND version = 7;
-- If 0 rows updated → concurrent modification, retry''',
        "solution_explanation": "Version check ensures no lost update between read and write.",
        "hints": "Django F() + filter on version in update.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Use JSONB column with GIN index for metadata search.",
        "ideal_topics": "JSONB, GIN, containment",
        "solution_code": '''CREATE INDEX idx_events_meta ON events USING GIN (metadata);

SELECT * FROM events
WHERE metadata @> '{"source": "api"}';

-- jsonb_path_ops for smaller index if only containment queries''',
        "solution_explanation": "JSONB is binary JSON with indexing; @> is containment operator.",
        "hints": "Validate JSON schema at application layer.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Write migration-safe additive schema change (add nullable column).",
        "ideal_topics": "migrations, zero downtime, expand-contract",
        "solution_code": '''-- Step 1: ADD COLUMN new_field TEXT NULL  (online in PG)
-- Step 2: Backfill in batches
-- Step 3: SET DEFAULT / NOT NULL after backfill
-- Step 4: Deploy code reading new_field
-- Step 5: Remove old_field later (contract)''',
        "solution_explanation": "Expand-contract pattern avoids breaking deploys during schema change.",
        "hints": "Avoid locking rewrites on huge tables.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Detect and kill a blocking lock chain.",
        "ideal_topics": "pg_locks, blocking, deadlock",
        "solution_code": '''SELECT blocked.pid AS blocked_pid,
       blocking.pid AS blocking_pid,
       blocked.query AS blocked_query
FROM pg_stat_activity blocked
JOIN pg_locks bl ON bl.pid = blocked.pid
JOIN pg_locks bl_blocking ON bl.locktype = bl_blocking.locktype
 ...
-- pg_cancel_backend(pid) or pg_terminate_backend(pid)''',
        "solution_explanation": "Long transactions holding locks block others; monitor pg_stat_activity.",
        "hints": "log_lock_waits in PostgreSQL surfaces waits.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Configure connection pooling strategy for Django + PostgreSQL.",
        "ideal_topics": "connection pool, pgbouncer, max connections",
        "solution_code": '''# Use PgBouncer in transaction pooling mode
# Django CONN_MAX_AGE = 0 with pgbouncer
# Limit pool size vs postgres max_connections
# Separate pools for web vs worker processes''',
        "solution_explanation": "Pooling reduces connection overhead; mode affects prepared statements.",
        "hints": "pgbouncer + transaction mode: disable server-side cursors.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Use materialized view for expensive reporting query.",
        "ideal_topics": "materialized view, REFRESH, reporting",
        "solution_code": '''CREATE MATERIALIZED VIEW daily_revenue AS
SELECT date_trunc('day', created_at) AS day, sum(total) AS revenue
FROM orders
GROUP BY 1;

CREATE UNIQUE INDEX ON daily_revenue (day);
REFRESH MATERIALIZED VIEW CONCURRENTLY daily_revenue;''',
        "solution_explanation": "Precompute aggregates; CONCURRENTLY requires unique index.",
        "hints": "Schedule REFRESH via cron/Celery.",
        "time_estimate_minutes": 18,
    },
]

SYSTEM_DESIGN_TOPICS = [
    {
        "question": "Design a URL shortener — outline components and data model.",
        "ideal_topics": "hashing, redirect, cache, scale",
        "solution_code": '''# Components: API, redirect service, DB, cache (Redis)
# Short code: base62(hash) or random with collision check
# Table: short_code PK, long_url, user_id, created_at, expires_at
# Read-heavy → cache short_code → long_url (TTL)
# Scale: read replicas, CDN for 302 redirects''',
        "solution_explanation": "Optimize read path; generate codes offline or on create.",
        "hints": "Discuss custom domains and analytics.",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Design real-time chat — message flow and presence.",
        "ideal_topics": "WebSockets, pub/sub, presence",
        "solution_code": '''# WebSocket gateway → message broker (Kafka/RabbitMQ)
# Per-room topic; fan-out to connected clients
# Presence: Redis SET room:user_ids with heartbeat TTL
# Store messages: DB + object storage for media
# Delivery: at-least-once + client dedup by message_id''',
        "solution_explanation": "Separate connection layer from persistence; broker decouples scale.",
        "hints": "Partition rooms across gateway nodes.",
        "time_estimate_minutes": 30,
    },
    {
        "question": "Design payment system with idempotency and reconciliation.",
        "ideal_topics": "idempotency, ledger, reconciliation",
        "solution_code": '''# Idempotency keys on payment API
# Double-entry ledger: debit/credit accounts
# States: initiated → authorized → captured → settled
# Reconciliation job matches provider reports vs internal ledger
# Outbox pattern for reliable webhook processing''',
        "solution_explanation": "Financial systems prioritize correctness over availability.",
        "hints": "Never lose money on duplicate retries.",
        "time_estimate_minutes": 30,
    },
    {
        "question": "Horizontal vs vertical scaling — when to use each.",
        "ideal_topics": "scaling, load balancer, stateless",
        "solution_code": '''# Vertical: bigger machine — simple, limited ceiling
# Horizontal: more nodes — needs stateless app, shared session store
# Load balancer: round-robin / least-conn / consistent hash
# Auto-scale on CPU, latency, queue depth metrics''',
        "solution_explanation": "Stateless services scale horizontally; databases need sharding/replicas.",
        "hints": "Cache and CDN before scaling app tier.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Database read replicas and read-your-writes consistency.",
        "ideal_topics": "replication lag, consistency",
        "solution_code": '''# Primary handles writes; replicas serve reads
# Lag: user may not see own write on replica immediately
# Fixes: read own writes from primary, session stickiness, version tokens''',
        "solution_explanation": "Replication lag is normal; design UX and routing around it.",
        "hints": "CQRS separates read/write models explicitly.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "CDN and object storage for global static and media delivery.",
        "ideal_topics": "CDN, S3, edge caching",
        "solution_code": '''# Upload → API stores in S3, returns CDN URL
# CDN edge caches by URL; cache-control headers set TTL
# Signed URLs for private objects
# Origin shield reduces load on bucket''',
        "solution_explanation": "CDN reduces latency and origin load for immutable assets.",
        "hints": "Invalidate vs versioned filenames for cache busting.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "CAP theorem applied to a distributed cache choice.",
        "ideal_topics": "CAP, AP vs CP, Redis",
        "solution_code": '''# CP: strong consistency (etcd, ZooKeeper) — coordination
# AP: Redis cluster — partition tolerance + availability, eventual consistency
# Choose based on use case: config vs session cache''',
        "solution_explanation": "Partition tolerance is mandatory in distributed systems; pick C or A tradeoff.",
        "hints": "PACELC extends with latency tradeoffs.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Circuit breaker pattern for unreliable downstream services.",
        "ideal_topics": "circuit breaker, timeouts, fallbacks",
        "solution_code": '''# States: CLOSED → OPEN (failures exceed threshold) → HALF_OPEN (probe)
# On OPEN: fail fast or fallback, don't hammer downstream
# Combine with timeouts and bounded retries''',
        "solution_explanation": "Prevents cascade failures; gives dependencies time to recover.",
        "hints": "Libraries: resilience4j, pybreaker.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Design notification system (email, push, SMS).",
        "ideal_topics": "queues, templates, fan-out",
        "solution_code": '''# Event → notification service → per-channel workers
# Template engine + user preferences (opt-out per channel)
# Rate limits per provider; dead letter queue for failures
# Idempotent notification_id prevents duplicates''',
        "solution_explanation": "Async workers isolate provider latency from API.",
        "hints": "Priority queues for transactional vs marketing.",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Sharding strategies for a growing relational dataset.",
        "ideal_topics": "sharding, hash, range, rebalancing",
        "solution_code": '''# Hash shard: user_id % N — even spread, hard range queries
# Range shard: user_id ranges — hotspot risk on new users
# Directory shard map: flexible migration
# Cross-shard queries expensive — design to avoid''',
        "solution_explanation": "Shard key choice dominates query patterns and rebalance cost.",
        "hints": "Vitess/Citus for managed sharding.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Event-driven architecture with outbox pattern.",
        "ideal_topics": "outbox, exactly-once, events",
        "solution_code": '''# Same transaction: update business row + insert outbox event
# Relay process polls outbox → publishes to broker → marks sent
# Consumers idempotent via event_id''',
        "solution_explanation": "Outbox bridges DB and message broker atomically.",
        "hints": "Debezium CDC is alternative to polling outbox.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Design video processing pipeline at scale.",
        "ideal_topics": "async pipeline, workers, object storage",
        "solution_code": '''# Upload raw → S3 → enqueue transcode job
# Workers: extract metadata, transcode resolutions, generate thumbnails
# Status API polls job state; webhook on complete
# Store outputs in S3 + CDN; metadata in DB''',
        "solution_explanation": "Long-running work off API path; horizontal worker pool.",
        "hints": "GPU workers for transcoding; spot instances for cost.",
        "time_estimate_minutes": 28,
    },
    {
        "question": "Load balancer algorithms and health checks.",
        "ideal_topics": "LB, health check, sticky sessions",
        "solution_code": '''# Algorithms: round-robin, least connections, IP hash
# Health checks: HTTP /health every N seconds
# Unhealthy instances removed from pool
# Sticky sessions: cookie or consistent hash — tradeoff with failover''',
        "solution_explanation": "Health checks must validate dependency readiness not just process up.",
        "hints": "L7 vs L4 load balancing.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Multi-region deployment and disaster recovery RPO/RTO.",
        "ideal_topics": "DR, RPO, RTO, failover",
        "solution_code": '''# RPO: max data loss window (replication lag bound)
# RTO: max downtime to restore service
# Active-passive: standby region, DNS failover
# Regular restore drills validate backups''',
        "solution_explanation": "Define SLAs first; architecture follows recovery objectives.",
        "hints": "Backup encryption and cross-region replication costs.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "API gateway responsibilities in microservices.",
        "ideal_topics": "API gateway, auth, routing",
        "solution_code": '''# Gateway: TLS termination, auth, rate limit, routing
# Aggregates multiple backend calls (BFF pattern)
# Not a dump of all business logic — thin orchestration''',
        "solution_explanation": "Centralizes cross-cutting concerns; backends stay focused.",
        "hints": "Kong, AWS API Gateway, Envoy.",
        "time_estimate_minutes": 16,
    },
]

TESTING_TOPICS = [
    {
        "question": "Write a pytest unit test with fixture and parametrize.",
        "ideal_topics": "pytest, fixture, parametrize",
        "solution_code": '''import pytest

@pytest.fixture
def user():
    return User(email="a@b.com")

@pytest.mark.parametrize("age,valid", [(17, False), (18, True)])
def test_age_validation(age, valid):
    if valid:
        User(age=age)  # should not raise
    else:
        with pytest.raises(ValueError):
            User(age=age)''',
        "solution_explanation": "Fixtures provide setup; parametrize runs multiple cases cleanly.",
        "hints": "conftest.py for shared fixtures.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Mock external HTTP calls in tests with responses or unittest.mock.",
        "ideal_topics": "mocking, responses, isolation",
        "solution_code": '''from unittest.mock import patch

@patch("myapp.client.requests.get")
def test_fetch(mock_get):
    mock_get.return_value.json.return_value = {"ok": True}
    mock_get.return_value.status_code = 200
    result = fetch_status()
    assert result == "ok"''',
        "solution_explanation": "Mock at boundary (HTTP client) not deep internals.",
        "hints": "responses library for declarative HTTP mocking.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Use pytest-django db fixture for model integration test.",
        "ideal_topics": "pytest-django, db, transactions",
        "solution_code": '''import pytest

@pytest.mark.django_db
def test_create_order(user):
    order = Order.objects.create(user=user, total=10)
    assert order.status == "pending"
    assert Order.objects.count() == 1''',
        "solution_explanation": "django_db marks test needing database; wraps in transaction rollback.",
        "hints": "Use factory_boy for model factories.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Test Django REST API with APIClient.",
        "ideal_topics": "APIClient, DRF tests, auth",
        "solution_code": '''from rest_framework.test import APIClient

@pytest.mark.django_db
def test_list_orders(user):
    client = APIClient()
    client.force_authenticate(user=user)
    resp = client.get("/api/orders/")
    assert resp.status_code == 200
    assert len(resp.json()) >= 0''',
        "solution_explanation": "APIClient simulates requests without running HTTP server.",
        "hints": "assert resp.json() structure, not full payload if volatile.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Structure tests: unit vs integration vs e2e boundaries.",
        "ideal_topics": "test pyramid, boundaries",
        "solution_code": '''# Unit: pure functions, fast, no I/O
# Integration: DB, cache, message broker with test containers
# E2E: few critical user journeys via browser/HTTP
# Target: many unit, fewer integration, minimal e2e''',
        "solution_explanation": "Pyramid keeps CI fast while covering real integration risks.",
        "hints": "Mark slow tests with @pytest.mark.slow.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Use freezegun or time mocking for time-dependent logic.",
        "ideal_topics": "time, freezegun, determinism",
        "solution_code": '''from freezegun import freeze_time

@freeze_time("2026-01-15")
def test_subscription_expiry():
    sub = create_sub(start="2026-01-01", days=14)
    assert sub.is_expired() is True''',
        "solution_explanation": "Freeze time for deterministic tests of TTL, billing, schedules.",
        "hints": "Patch timezone.now in Django tests.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Test Celery task with eager mode.",
        "ideal_topics": "Celery, CELERY_TASK_ALWAYS_EAGER",
        "solution_code": '''@pytest.fixture
def celery_eager(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True

@pytest.mark.django_db
def test_order_task(celery_eager, order):
    process_order.delay(order.id)
    order.refresh_from_db()
    assert order.status == "processed"''',
        "solution_explanation": "Eager runs tasks synchronously in-process for tests.",
        "hints": "Also set CELERY_TASK_STORE_EAGER_RESULT.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Property-based testing concept with Hypothesis.",
        "ideal_topics": "Hypothesis, property testing",
        "solution_code": '''from hypothesis import given
import hypothesis.strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    assert sorted(sorted(lst)) == sorted(lst)''',
        "solution_explanation": "Generates many inputs to find edge cases humans miss.",
        "hints": "Use strategies for text, decimals, composite types.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Snapshot testing for API JSON responses (concept).",
        "ideal_topics": "snapshots, regression, JSON",
        "solution_code": '''# Store golden JSON file; test compares current response
# Update snapshots deliberately when API changes
# Avoid snapshots for timestamps and random IDs — normalize first''',
        "solution_explanation": "Snapshots catch unintended response changes quickly.",
        "hints": "pytest-snapshot or syrupy libraries.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Test database constraints and unique violations.",
        "ideal_topics": "IntegrityError, constraints",
        "solution_code": '''import pytest
from django.db import IntegrityError

@pytest.mark.django_db
def test_duplicate_email(user):
    User.objects.create(email="dup@test.com")
    with pytest.raises(IntegrityError):
        User.objects.create(email="dup@test.com")''',
        "solution_explanation": "Verify DB enforces rules independent of form validation.",
        "hints": "transaction.atomic() may wrap IntegrityError in Django.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Coverage goals and what not to chase in coverage %.",
        "ideal_topics": "coverage, meaningful tests",
        "solution_code": '''# Aim coverage on business logic modules
# 100% coverage ≠ correct — test behavior not lines
# Exclude migrations, admin, __repr__ from gates
# pytest --cov=app --cov-report=term-missing''',
        "solution_explanation": "Coverage finds untested code; judgment needed on assertions quality.",
        "hints": "Branch coverage > line coverage for conditionals.",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Load testing with Locust — define user scenario.",
        "ideal_topics": "Locust, load test, scenarios",
        "solution_code": '''from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def list_orders(self):
        self.client.get("/api/orders/", headers=self.auth_headers)''',
        "solution_explanation": "Locust simulates concurrent users; measure p95 latency under load.",
        "hints": "Ramp up gradually; monitor DB and CPU during test.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Security testing: SQL injection and auth bypass checks.",
        "ideal_topics": "security testing, OWASP",
        "solution_code": '''# Parameterized queries — ORM protects by default
# Test: unauthenticated access returns 401/403
# Test: user A cannot access user B resource by ID tampering
# Scan dependencies with pip-audit / safety''',
        "solution_explanation": "Automate authz tests per endpoint; never trust client-side checks.",
        "hints": "OWASP ZAP for DAST scanning.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Flaky test diagnosis and quarantine strategy.",
        "ideal_topics": "flaky tests, quarantine, CI",
        "solution_code": '''# Causes: timing, shared state, random data, external deps
# Fix: isolate state, deterministic seeds, retry only as last resort
# Quarantine: mark flaky, track issue, don't block main CI''',
        "solution_explanation": "Flaky tests erode trust; fix or remove quickly.",
        "hints": "pytest-rerun failures mask problems — prefer root cause.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Contract testing between services (consumer-driven).",
        "ideal_topics": "Pact, contracts, microservices",
        "solution_code": '''# Consumer defines expected request/response schema
# Provider verifies against published contracts in CI
# Catches breaking API changes before deploy''',
        "solution_explanation": "Contracts test integration without full e2e environment.",
        "hints": "Pact broker stores contract versions.",
        "time_estimate_minutes": 18,
    },
]

DEVOPS_TOPICS = [
    {
        "question": "Write a multi-stage Dockerfile for Django production.",
        "ideal_topics": "Docker, multi-stage, slim images",
        "solution_code": '''FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir -r requirements.txt -w /wheels

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install /wheels/*
COPY . .
CMD ["gunicorn", "config.wsgi:application", "-b", "0:8000"]''',
        "solution_explanation": "Builder stage compiles wheels; runtime image stays small.",
        "hints": "Run as non-root user; .dockerignore excludes venv.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "docker-compose services for web, db, redis, worker.",
        "ideal_topics": "compose, networking, depends_on",
        "solution_code": '''services:
  web:
    build: .
    depends_on: [postgres, redis]
    environment:
      DATABASE_URL: postgres://...
  postgres:
    image: postgres:16
  redis:
    image: redis:7
  worker:
    build: .
    command: celery -A config worker -l info''',
        "solution_explanation": "Compose orchestrates dev stack; healthchecks improve depends_on.",
        "hints": "Use named volumes for postgres data.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "CI pipeline stages: lint, test, build, deploy.",
        "ideal_topics": "CI/CD, GitHub Actions, gates",
        "solution_code": '''# stages:
# 1. lint (ruff, mypy)
# 2. test (pytest + coverage gate)
# 3. build image (docker build)
# 4. deploy staging (auto on main)
# 5. deploy prod (manual approval)''',
        "solution_explanation": "Fast feedback early; deploy only vetted artifacts.",
        "hints": "Cache pip and docker layers in CI.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Environment-specific configuration with secrets management.",
        "ideal_topics": "secrets, env vars, vault",
        "solution_code": '''# Never commit secrets
# Dev: .env file (gitignored)
# Prod: secret manager (AWS SM, Vault) injected at runtime
# Rotate credentials; audit access logs''',
        "solution_explanation": "Separate config from code; least privilege on secret access.",
        "hints": "12-factor app config principle.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Zero-downtime deploy with rolling updates.",
        "ideal_topics": "rolling deploy, health checks",
        "solution_code": '''# K8s: maxUnavailable 0, maxSurge 1
# New pods pass readiness probe before receiving traffic
# Old pods drain connections on shutdown hook
# DB migrations: backward-compatible expand first''',
        "solution_explanation": "Readiness gates traffic; graceful shutdown prevents dropped requests.",
        "hints": "Blue-green for instant rollback option.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Structured logging and log aggregation pipeline.",
        "ideal_topics": "logging, ELK, JSON logs",
        "solution_code": '''# App logs JSON to stdout
# Collector (Fluent Bit) → Elasticsearch/Loki
# Dashboards in Grafana/Kibana
# Correlate by request_id, trace_id''',
        "solution_explanation": "Centralized logs enable search across replicas.",
        "hints": "Log levels: INFO default prod; DEBUG dev only.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Monitoring: metrics, alerts, and SLOs.",
        "ideal_topics": "Prometheus, SLO, alerting",
        "solution_code": '''# Metrics: request rate, error rate, latency (RED)
# SLO: 99.9% requests < 300ms over 30d
# Alert on burn rate — not every spike
# USE method for resources: Utilization, Saturation, Errors''',
        "solution_explanation": "SLO-driven alerts reduce pager fatigue.",
        "hints": "Grafana dashboards per service.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Infrastructure as Code with Terraform module concept.",
        "ideal_topics": "Terraform, IaC, modules",
        "solution_code": '''# module "vpc" { source = "./modules/vpc" }
# module "rds" { depends_on = [module.vpc] }
# state in remote backend (S3 + lock)
# plan in CI before apply''',
        "solution_explanation": "IaC versions infrastructure; modules reuse patterns.",
        "hints": "Separate state per environment.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Backup strategy for PostgreSQL in production.",
        "ideal_topics": "backup, PITR, restore",
        "solution_code": '''# Daily base backup + continuous WAL archiving
# PITR to any point in retention window
# Test restore monthly to isolated environment
# Encrypt backups at rest''',
        "solution_explanation": "Untested backups are not backups.",
        "hints": "pg_dump for logical; WAL for physical PITR.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Git branching strategy for trunk-based development.",
        "ideal_topics": "git, trunk-based, feature flags",
        "solution_code": '''# Short-lived branches → main via PR
# Feature flags hide incomplete work
# main always deployable
# Release tags for prod snapshots''',
        "solution_explanation": "Trunk-based reduces merge hell; flags decouple deploy from release.",
        "hints": "Conventional commits for changelog automation.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Container security: image scanning and non-root.",
        "ideal_topics": "security, Trivy, non-root",
        "solution_code": '''# Scan images in CI (Trivy, Grype)
# USER app in Dockerfile
# Read-only root filesystem where possible
# Pin base image digests''',
        "solution_explanation": "Supply chain security starts at build pipeline.",
        "hints": "Distroless images reduce attack surface.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Kubernetes probes: liveness vs readiness.",
        "ideal_topics": "k8s, probes, health",
        "solution_code": '''# livenessProbe: restart if deadlocked (careful — false positive kills pod)
# readinessProbe: remove from service endpoints if not ready
# startupProbe: for slow-starting apps''',
        "solution_explanation": "Readiness = can serve traffic; liveness = process should exist.",
        "hints": "Check dependencies in readiness not liveness.",
        "time_estimate_minutes": 14,
    },
]

CLOUD_TOPICS = [
    {
        "question": "AWS EC2 vs containers (ECS/EKS) tradeoffs.",
        "ideal_topics": "EC2, ECS, EKS, compute",
        "solution_code": '''# EC2: full VM control, more ops overhead
# ECS/Fargate: managed containers, less node management
# EKS: Kubernetes portability, higher complexity
# Choose based on team skills and scale''',
        "solution_explanation": "Managed services reduce ops; EC2 for legacy/control needs.",
        "hints": "Fargate removes EC2 node patching.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "S3 storage classes and lifecycle policies.",
        "ideal_topics": "S3, lifecycle, Glacier",
        "solution_code": '''# Standard → IA → Glacier for aging logs/backups
# Lifecycle rules transition after N days
# Versioning protects against accidental delete''',
        "solution_explanation": "Match storage class to access pattern for cost.",
        "hints": "S3 Intelligent-Tiering for unknown patterns.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "RDS Multi-AZ vs read replicas.",
        "ideal_topics": "RDS, Multi-AZ, replicas",
        "solution_code": '''# Multi-AZ: synchronous standby for failover (same region)
# Read replicas: async scaling reads (cross-region possible)
# Failover DNS update on Multi-AZ promotion''',
        "solution_explanation": "Multi-AZ is HA; replicas are scale + DR option.",
        "hints": "Aurora separates storage/compute further.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "IAM least privilege policy design.",
        "ideal_topics": "IAM, policies, least privilege",
        "solution_code": '''{
  "Effect": "Allow",
  "Action": ["s3:GetObject", "s3:PutObject"],
  "Resource": "arn:aws:s3:::my-bucket/uploads/*"
}''',
        "solution_explanation": "Scope actions and resources narrowly; avoid * on production.",
        "hints": "Use IAM roles for services not long-lived keys.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "VPC networking: public vs private subnets.",
        "ideal_topics": "VPC, subnets, NAT",
        "solution_code": '''# Public subnet: LB, NAT gateway
# Private subnet: app servers, databases — no direct internet
# Security groups: stateful firewall per instance
# NACLs: subnet-level (less common)''',
        "solution_explanation": "Layer defense; databases never public.",
        "hints": "VPC endpoints for S3/Dynamo avoid NAT costs.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Auto Scaling Group policies.",
        "ideal_topics": "ASG, scaling policies, CloudWatch",
        "solution_code": '''# Target tracking: maintain 60% CPU
# Step scaling on queue depth
# Cooldown prevents thrashing
# Combine with predictive scaling for daily patterns''',
        "solution_explanation": "Scale on workload signals not just CPU.",
        "hints": "Min instances > 0 for prod availability.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "CloudFront CDN caching behavior.",
        "ideal_topics": "CloudFront, cache behaviors",
        "solution_code": '''# Cache policy: TTL, query string forwarding
# Origin request policy: headers/cookies to origin
# Invalidation costs — prefer versioned asset URLs''',
        "solution_explanation": "Edge caches reduce origin load and latency globally.",
        "hints": "Signed URLs for private content.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "AWS Lambda use cases and limitations.",
        "ideal_topics": "Lambda, serverless, cold start",
        "solution_code": '''# Good: event processing, cron, light APIs
# Limits: 15min timeout, stateless, cold starts
# Provisioned concurrency reduces cold start for latency-sensitive''',
        "solution_explanation": "Serverless ops-light but vendor limits and cold starts matter.",
        "hints": "Step Functions for long workflows.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Secrets Manager vs Parameter Store.",
        "ideal_topics": "secrets, SSM, rotation",
        "solution_code": '''# Secrets Manager: auto rotation, higher cost
# Parameter Store: config parameters, SecureString with KMS
# Inject at runtime; never bake into AMIs''',
        "solution_explanation": "Pick based on rotation needs and cost.",
        "hints": "Cross-account secret access via resource policies.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Well-Architected Framework pillars (overview).",
        "ideal_topics": "AWS WAF, pillars",
        "solution_code": '''# Operational Excellence, Security, Reliability,
# Performance Efficiency, Cost Optimization, Sustainability
# Use reviews to gap-assess workloads''',
        "solution_explanation": "Framework guides balanced architecture decisions.",
        "hints": "Cost anomaly detection in Cost Explorer.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Disaster recovery across regions.",
        "ideal_topics": "cross-region, DR, Route53",
        "solution_code": '''# Backup replication to second region
# Route53 health checks + failover routing
# Runbook for promote secondary region
# Data residency compliance constraints''',
        "solution_explanation": "Cross-region DR costs 2x+; justify with business RTO/RPO.",
        "hints": "Pilot light vs warm standby cost tradeoffs.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Cost optimization strategies on AWS.",
        "ideal_topics": "cost, reserved, spot",
        "solution_code": '''# Right-size instances; Reserved/Savings Plans for baseline
# Spot for batch; auto-stop dev environments
# S3 lifecycle; delete unattached EBS
# Tag resources for cost allocation''',
        "solution_explanation": "Continuous cost review — not one-time exercise.",
        "hints": "AWS Budgets alerts on anomalies.",
        "time_estimate_minutes": 14,
    },
]

AI_TOPICS = [
    {
        "question": "Integrate OpenAI API with retries and timeout.",
        "ideal_topics": "LLM API, retries, timeout",
        "solution_code": '''import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def complete(prompt: str) -> str:
    with httpx.Client(timeout=30.0) as client:
        resp = client.post(
            "https://api.openai.com/v1/chat/completions",
            json={"model": "gpt-4o", "messages": [{"role": "user", "content": prompt}]},
            headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]''',
        "solution_explanation": "Timeouts and retries handle transient API failures; cap tokens for cost.",
        "hints": "Stream responses for UX on long outputs.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "RAG pipeline: retrieve, augment, generate.",
        "ideal_topics": "RAG, embeddings, vector search",
        "solution_code": '''# 1. Chunk documents
# 2. Embed chunks → vector store (pgvector, Pinecone)
# 3. Query: embed user question, similarity search top-k
# 4. Prompt LLM with retrieved context + question
# 5. Cite sources in response''',
        "solution_explanation": "RAG grounds LLM on private data without full fine-tune.",
        "hints": "Chunk size and overlap affect recall.",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Prompt engineering for structured JSON output.",
        "ideal_topics": "prompting, JSON mode, validation",
        "solution_code": '''prompt = """
Extract fields as JSON only:
{"title": string, "priority": "low"|"medium"|"high"}
Text: ...
"""
# Validate with pydantic after parse
# Use response_format json_schema where supported''',
        "solution_explanation": "Constrain output format; validate — models can still hallucinate fields.",
        "hints": "Few-shot examples improve adherence.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Token budgeting and cost control for LLM apps.",
        "ideal_topics": "tokens, cost, budgeting",
        "solution_code": '''# Estimate tokens pre-call; reject over budget
# Cache embeddings and frequent completions
# Smaller model for classification, large for generation
# Per-user daily quota in Redis''',
        "solution_explanation": "Token costs scale with usage; monitor per feature.",
        "hints": "tiktoken for OpenAI token counting.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Evaluate LLM output quality systematically.",
        "ideal_topics": "evals, golden set, regression",
        "solution_code": '''# Golden dataset: input → expected criteria
# Metrics: exact match, ROUGE, LLM-as-judge (careful)
# Regression suite in CI on prompt/model changes
# Human review sample for calibration''',
        "solution_explanation": "Evals prevent silent quality regressions on prompt tweaks.",
        "hints": "LangSmith, promptfoo tools.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Guardrails: input/output filtering.",
        "ideal_topics": "safety, moderation, PII",
        "solution_code": '''# Input: max length, blocklist, PII regex scan
# Output: moderation API, JSON schema validation
# Log prompts with redaction for support''',
        "solution_explanation": "Defense in depth for user-facing AI features.",
        "hints": "OWASP LLM Top 10 risks.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Batch embedding generation for document index.",
        "ideal_topics": "embeddings, batch, throughput",
        "solution_code": '''# Batch texts in groups of 64-256
# asyncio or worker pool for parallel batches
# Store embedding vector + metadata in DB
# Re-embed on document update only''',
        "solution_explanation": "Batching improves throughput and reduces API overhead.",
        "hints": "Normalize vectors for cosine similarity.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Fine-tuning vs RAG decision framework.",
        "ideal_topics": "fine-tuning, RAG, when to use",
        "solution_code": '''# RAG: dynamic knowledge, cite sources, cheaper iteration
# Fine-tune: style/format, domain jargon, latency-sensitive
# Often combine: fine-tuned model + RAG context''',
        "solution_explanation": "RAG updates without retraining; fine-tune for behavior/style.",
        "hints": "Start RAG; fine-tune when evals plateau.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Async worker processing for long LLM jobs.",
        "ideal_topics": "Celery, async jobs, webhooks",
        "solution_code": '''# API accepts job → returns job_id
# Worker calls LLM, stores result
# Client polls GET /jobs/{id} or webhook on complete
# Idempotency key on job creation''',
        "solution_explanation": "LLM latency too high for synchronous HTTP in many cases.",
        "hints": "Progress events via SSE optional.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Vector similarity search with pgvector.",
        "ideal_topics": "pgvector, cosine, index",
        "solution_code": '''CREATE EXTENSION vector;
ALTER TABLE chunks ADD COLUMN embedding vector(1536);
CREATE INDEX ON chunks USING ivfflat (embedding vector_cosine_ops);

SELECT content FROM chunks
ORDER BY embedding <=> query_embedding
LIMIT 5;''',
        "solution_explanation": "<=> is cosine distance in pgvector; index for large tables.",
        "hints": "Tune lists parameter for ivfflat recall.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Observability for LLM traces.",
        "ideal_topics": "tracing, latency, tokens",
        "solution_code": '''# Log: model, prompt hash, latency, input/output tokens, cost
# Trace ID links retrieve + generate steps
# Sample traces for debugging bad outputs''',
        "solution_explanation": "LLM debugging needs prompt/response visibility with privacy controls.",
        "hints": "OpenTelemetry + custom span attributes.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Multi-modal and tool-calling agent pattern.",
        "ideal_topics": "agents, tools, function calling",
        "solution_code": '''# LLM returns tool_call: search(query)
# Runtime executes tool, feeds result back
# Loop until final answer or max steps
# Validate tool args before execution''',
        "solution_explanation": "Agents extend LLM with actions; cap steps to control cost/loops.",
        "hints": "Human approval for destructive tools.",
        "time_estimate_minutes": 20,
    },
]

BEHAVIORAL_TOPICS = [
    {
        "question": "Describe a production incident you resolved (STAR format).",
        "ideal_topics": "STAR, incident, root cause",
        "solution_code": '''# Situation: outage context, impact, timeline
# Task: your responsibility in response
# Action: diagnose (metrics/logs), mitigate, fix, communicate
# Result: restored service, postmortem, preventive measures
# Quantify: downtime minutes, users affected, MTTR''',
        "solution_explanation": "STAR keeps answers structured and evidence-based.",
        "hints": "Focus on your decisions, not only team effort.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Tell me about a technical disagreement and how you resolved it.",
        "ideal_topics": "collaboration, data-driven, consensus",
        "solution_code": '''# Frame disagreement on tradeoffs not personalities
# Action: prototype, benchmark, document options
# Result: decision recorded, relationship preserved
# Show willingness to be wrong with new data''',
        "solution_explanation": "Interviewers assess communication and engineering judgment.",
        "hints": "Avoid blaming; show empathy.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "How do you prioritize when everything is urgent?",
        "ideal_topics": "prioritization, stakeholder, impact",
        "solution_code": '''# Clarify impact vs urgency matrix
# Align with product on business value
# Communicate tradeoffs explicitly
# Protect tech debt budget for stability''',
        "solution_explanation": "Shows maturity under pressure and stakeholder management.",
        "hints": "Give a concrete week with competing demands.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Describe mentoring or uplifting junior engineers.",
        "ideal_topics": "mentoring, leadership, growth",
        "solution_code": '''# Specific person/situation (anonymized)
# Action: pairing, code review style, safe learning tasks
# Result: their growth metric, team benefit
# Leadership without formal title''',
        "solution_explanation": "Senior signals include multiplying others' effectiveness.",
        "hints": "Balance support with autonomy.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "A project that failed or missed deadline — what you learned.",
        "ideal_topics": "failure, learning, accountability",
        "solution_code": '''# Honest scope/estimate/dependency failure
# Your role in the miss — no victim narrative
# Concrete process changes afterward
# Resilience and growth mindset''',
        "solution_explanation": "Failure stories with learning outperform hidden blame.",
        "hints": "End positive with systemic fix.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "How you approach code reviews constructively.",
        "ideal_topics": "code review, feedback, quality",
        "solution_code": '''# Ask questions vs dictate
# Prioritize: correctness, security, maintainability
# Nitpicks separated from blockers
# Praise good patterns; link to standards/docs''',
        "solution_explanation": "Reviews are teaching moments and quality gates.",
        "hints": "Mention automated checks reducing nitpicks.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Explain a complex system to non-technical stakeholders.",
        "ideal_topics": "communication, simplification, analogy",
        "solution_code": '''# Audience-appropriate analogy
# Avoid jargon or define immediately
# Focus on user/business outcome
# Visual if possible; check understanding''',
        "solution_explanation": "Communication skill is evaluated for senior roles.",
        "hints": "Practice 2-minute elevator version.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Handling ambiguous requirements.",
        "ideal_topics": "ambiguity, clarification, discovery",
        "solution_code": '''# Ask clarifying questions before building
# Spike/prototype to reduce unknowns
# Document assumptions; get sign-off
# Iterate with demos early''',
        "solution_explanation": "Shows product partnership not just ticket execution.",
        "hints": "Example where ambiguity caused rework if ignored.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Ethical use of AI in engineering workflow.",
        "ideal_topics": "AI ethics, IP, verification",
        "solution_code": '''# Use AI for drafts, tests, exploration
# Verify outputs; you own shipped code
# Respect IP, privacy, license of generated code
# Transparent with team about AI assistance''',
        "solution_explanation": "Modern interviews expect thoughtful AI usage stance.",
        "hints": "Company policies on confidential data in prompts.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Why this role and company — tailored answer structure.",
        "ideal_topics": "motivation, research, fit",
        "solution_code": '''# Research: product, tech stack, engineering culture
# Connect your goals to their problems
# Specific not generic praise
# What you'll contribute in first 90 days''',
        "solution_explanation": "Shows genuine interest and preparation.",
        "hints": "Avoid only citing compensation.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Conflict with product manager on scope.",
        "ideal_topics": "PM partnership, scope, negotiation",
        "solution_code": '''# Data on effort/risk for scope options
# Propose phased delivery (MVP → v2)
# Shared goal: user value, not winning argument
# Document decision and revisit criteria''',
        "solution_explanation": "Collaboration beats escalation when possible.",
        "hints": "Use user impact metrics in discussion.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Your strongest technical achievement.",
        "ideal_topics": "achievement, impact, metrics",
        "solution_code": '''# Context, technical challenge, your unique contribution
# Metrics: latency -40%, cost -30%, revenue protected
# Scale: requests/day, data size, team size
# Keep depth ready if interviewer probes''',
        "solution_explanation": "Anchor in measurable impact and technical depth.",
        "hints": "2-minute version + deep-dive backup.",
        "time_estimate_minutes": 18,
    },
]
