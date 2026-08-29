"""Seed data for engineering practice challenges."""
ENGINEERING_CHALLENGES = [
    {
        "challenge_type": "lab",
        "title": "Build a rate-limited API endpoint",
        "description": "Implement token-bucket rate limiting on a Django view using Redis.",
        "instructions": "Work through each step in the lab workspace. Use the code editor to scaffold your solution.",
        "starter_code": """# rate_limit.py — token bucket per IP
from django.http import JsonResponse
from django.views.decorators.http import require_GET

# TODO: connect Redis (cache or redis-py)
# LIMIT = 100 requests per 60 seconds per IP

@require_GET
def limited_api(request):
    ip = request.META.get("REMOTE_ADDR", "unknown")
    # TODO: check bucket, increment, set TTL
    allowed = True  # replace with real check
    if not allowed:
        return JsonResponse(
            {"error": "rate limit exceeded"},
            status=429,
            headers={"Retry-After": "60"},
        )
    return JsonResponse({"ok": True, "ip": ip})
""",
        "lab_steps": [
            "Sketch the token-bucket algorithm (capacity, refill rate, current tokens).",
            "Wire Redis keys: `rate:{ip}` with INCR + EXPIRE or a sliding window counter.",
            "Implement the Django view decorator or middleware hook.",
            "Return 429 with Retry-After when the bucket is empty.",
            "Load-test with 200 concurrent requests and document p95 latency.",
        ],
        "hints": "Redis INCR with EXPIRE gives a simple fixed window.\nUse atomic Lua or WATCH/MULTI for token bucket accuracy.\nPut limiting before heavy view logic to save resources.",
        "success_criteria": "Under load, excess requests get 429; legitimate traffic stays under 100/min/IP; Retry-After header present.",
        "solution_notes": "Use cache or Redis with sliding window; test with concurrent requests.",
        "difficulty": "medium",
        "estimated_minutes": 60,
        "order": 1,
    },
    {
        "challenge_type": "lab",
        "title": "PostgreSQL query optimization lab",
        "description": "Given a slow multi-join query, add indexes and rewrite with EXPLAIN ANALYZE.",
        "instructions": "Optimize the dashboard query using EXPLAIN ANALYZE and targeted indexes.",
        "starter_code": """-- Slow dashboard query (1M orders)
SELECT o.id, o.created_at, u.email, SUM(oi.price * oi.qty) AS total
FROM orders o
JOIN users u ON u.id = o.user_id
JOIN order_items oi ON oi.order_id = o.id
WHERE o.created_at > NOW() - INTERVAL '30 days'
GROUP BY o.id, o.created_at, u.email
ORDER BY o.created_at DESC
LIMIT 50;

-- Run: EXPLAIN (ANALYZE, BUFFERS) <query>
-- Document: seq scans, join order, index candidates
""",
        "lab_steps": [
            "Run EXPLAIN ANALYZE and capture the slowest node (seq scan vs hash join).",
            "Add a composite index on orders (user_id, created_at).",
            "Consider partial index or covering index for the 30-day filter.",
            "Re-run EXPLAIN and compare execution time and buffer hits.",
            "Rewrite query if needed (subquery vs join, LIMIT pushdown).",
        ],
        "hints": "Look for Seq Scan on orders with high row estimate.\nComposite index order matches filter + sort columns.\nAvoid SELECT * in production list endpoints.",
        "success_criteria": "p95 query time under 50ms on representative data; plan uses index scan not seq scan on orders.",
        "solution_notes": "Composite index on (user_id, created_at); avoid SELECT *.",
        "difficulty": "hard",
        "estimated_minutes": 45,
        "order": 2,
    },
    {
        "challenge_type": "lab",
        "title": "Celery retry + idempotency lab",
        "description": "Build a Celery task that processes payments idempotently with retries.",
        "instructions": "Implement idempotent payment processing with Celery retries and a dead-letter path.",
        "starter_code": """# tasks.py
from celery import shared_task
from django.db import transaction

@shared_task(bind=True, max_retries=5, acks_late=True)
def process_payment(self, payment_id: str, idempotency_key: str):
    # TODO: upsert idempotency record before side effects
    # TODO: call payment provider
    # TODO: on transient error: self.retry(countdown=2 ** self.request.retries)
    raise NotImplementedError
""",
        "lab_steps": [
            "Define IdempotencyRecord model (key, status, result payload).",
            "On task start: create record in `pending` or return cached `completed`.",
            "Perform payment only inside transaction after lock acquired.",
            "Configure exponential backoff retries for transient failures.",
            "Route permanent failures to DLQ / admin alert.",
        ],
        "hints": "Store idempotency key before calling the payment API.\nacks_late=True means you must handle duplicate delivery.\nUse get_or_create with select_for_update on the key row.",
        "success_criteria": "Duplicate task delivery does not double-charge; retries succeed on transient errors; permanent failure lands in DLQ with audit trail.",
        "solution_notes": "Store idempotency key before side effects; use acks_late carefully.",
        "difficulty": "hard",
        "estimated_minutes": 75,
        "order": 3,
    },
    {
        "challenge_type": "benchmark",
        "title": "API list endpoint benchmark",
        "description": "Benchmark GET /api/items with 10k rows — baseline vs optimized queryset.",
        "instructions": "Measure baseline vs optimized API performance and document results.",
        "starter_code": """# benchmark script outline
# locust or pytest-benchmark

BASELINE = """
# queryset = Item.objects.all()[:100]
"""

OPTIMIZED = """
# queryset = Item.objects.select_related('owner').only(...)[:100]
"""

# Record: RPS, p50, p95, DB query count (django-debug-toolbar or assertNumQueries)
""",
        "lab_steps": [
            "Establish baseline: requests/sec and p50/p95 with default queryset.",
            "Count SQL queries per request (target: eliminate N+1).",
            "Apply select_related / prefetch_related and pagination.",
            "Compare OFFSET pagination vs keyset/cursor pagination.",
            "Write a short report with numbers and recommendation.",
        ],
        "hints": "django.test.utils.CaptureQueriesContext helps in tests.\nCursor pagination avoids large OFFSET cost.\nCache hot list fragments if reads dominate.",
        "success_criteria": "Documented before/after with ≥2x RPS or ≥50% p95 improvement; query count reduced to O(1) per page.",
        "solution_notes": "select_related + pagination; compare OFFSET vs cursor pagination.",
        "difficulty": "medium",
        "estimated_minutes": 40,
        "order": 1,
    },
    {
        "challenge_type": "benchmark",
        "title": "Python data processing benchmark",
        "description": "Compare list comprehension vs generator for 10M row aggregation.",
        "instructions": "Benchmark memory and speed for large aggregations.",
        "starter_code": """import timeit
import tracemalloc

N = 10_000_000

def with_list():
    data = [i % 7 for i in range(N)]
    return sum(x for x in data)

def with_gen():
    return sum(i % 7 for i in range(N))

# timeit + tracemalloc for each approach
""",
        "lab_steps": [
            "Implement both approaches with identical output.",
            "Measure wall time with timeit (3+ runs).",
            "Measure peak memory with tracemalloc.",
            "Plot or tabulate ops/sec and MB peak.",
            "State when each approach is appropriate.",
        ],
        "hints": "Generators avoid storing 10M ints in a list.\nFor small N, list comprehensions can be faster.\nProfile before optimizing production pipelines.",
        "success_criteria": "Table of time + memory for both; clear recommendation for batch size thresholds.",
        "solution_notes": "Generators win on memory; comprehensions may be faster for small data.",
        "difficulty": "easy",
        "estimated_minutes": 30,
        "order": 2,
    },
    {
        "challenge_type": "debugging",
        "title": "Race condition in counter",
        "description": "Fix a buggy concurrent counter that loses updates under load.",
        "instructions": "Reproduce the race, then fix and verify the counter is exact.",
        "starter_code": """import threading

counter = 0

def increment():
    global counter
    for _ in range(1000):
        counter += 1  # BUG: not atomic

threads = [threading.Thread(target=increment) for _ in range(100)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(counter)  # expected 100000, often lower
""",
        "lab_steps": [
            "Run the buggy script and record actual vs expected count.",
            "Explain lost updates at the bytecode/thread scheduling level.",
            "Fix with threading.Lock or itertools / atomic pattern.",
            "Verify 100 runs all produce exactly 100000.",
            "Note production alternative (Redis INCR, DB counter).",
        ],
        "hints": "counter += 1 is read-modify-write, not atomic.\nLock around the whole loop, not each iteration only if needed.\nFor high throughput use atomic primitives.",
        "success_criteria": "Fixed code prints 100000 consistently across 100 consecutive runs.",
        "solution_notes": "Use threading.Lock or atomic operations; test under contention.",
        "difficulty": "medium",
        "estimated_minutes": 35,
        "order": 1,
    },
    {
        "challenge_type": "debugging",
        "title": "N+1 query in Django view",
        "description": "Find and fix N+1 queries in a list view using debug toolbar.",
        "instructions": "Locate N+1 queries and fix with select_related / prefetch_related.",
        "starter_code": """# views.py (buggy)
def order_list(request):
    orders = Order.objects.filter(user=request.user)[:50]
    rows = [
        {"id": o.id, "email": o.user.email, "total": o.total}
        for o in orders
    ]
    return JsonResponse({"orders": rows})

# TODO: fix queryset; verify query count drops to 1-2
""",
        "lab_steps": [
            "Enable django-debug-toolbar and load the list view.",
            "Identify 1 + N queries on users table.",
            "Apply select_related('user') on the queryset.",
            "Check reverse FK / M2M for prefetch_related needs.",
            "Add a regression test with assertNumQueries.",
        ],
        "hints": "N+1 happens when you access related objects in a loop.\nselect_related for FK; prefetch_related for reverse/M2M.\nUse only() / defer() if columns are heavy.",
        "success_criteria": "List view uses ≤2 queries regardless of row count; test asserts query budget.",
        "solution_notes": "prefetch_related for reverse FK/M2M.",
        "difficulty": "easy",
        "estimated_minutes": 25,
        "order": 2,
    },
    {
        "challenge_type": "system_design",
        "title": "Design a notification system",
        "description": "Email + push + SMS fan-out at scale with retries.",
        "instructions": "Produce architecture diagram notes and component responsibilities.",
        "starter_code": """# Notification system — design workspace

## Event ingress
- API: POST /notifications (template_id, user_id, payload)
- Idempotency-Key header

## Core services
1. Notification API
2. Preference / quiet-hours store
3. Template service
4. Per-channel workers (email, push, sms)
5. DLQ + replay tooling

## Your notes (edit below)
""",
        "lab_steps": [
            "Draw data flow: event → queue → channel workers.",
            "Define idempotency and deduplication strategy.",
            "Specify retry policy and DLQ handling per channel.",
            "Estimate QPS and queue depth for 10M users.",
            "List failure modes and monitoring alerts.",
        ],
        "hints": "Fan-out via queue; never send directly from API request.\nUser preferences filter before enqueue.\nTemplate versioning avoids broken sends.",
        "success_criteria": "Diagram covers API, queue, workers, templates, prefs, DLQ; includes idempotency and rate limits.",
        "solution_notes": "Event → notification service → per-channel workers; template store.",
        "difficulty": "hard",
        "estimated_minutes": 45,
        "order": 1,
    },
    {
        "challenge_type": "system_design",
        "title": "Design URL shortener",
        "description": "Short links with analytics and high read throughput.",
        "instructions": "Design components for shorten, redirect, and analytics at scale.",
        "starter_code": """# URL shortener — design workspace

## Requirements
- Shorten: POST /links { url } -> { code, short_url }
- Redirect: GET /{code} -> 302 to original (p99 < 20ms)
- Analytics: click counts, referrer, geo (async)

## Capacity sketch
- Writes/day: ___
- Reads/day: ___
- Storage (5yr): ___

## Your component list (edit below)
""",
        "lab_steps": [
            "Choose encoding strategy (base62, hash prefix).",
            "Design read path: cache → DB fallback.",
            "Design write path: collision handling.",
            "Sketch analytics pipeline (async, no redirect blocking).",
            "Back-of-envelope QPS and storage estimate.",
        ],
        "hints": "Cache hot codes in Redis/Memcached.\nPre-generate code space or use counter + base62.\nAnalytics via async click stream, not sync on redirect.",
        "success_criteria": "Read-heavy architecture with cache layer; collision strategy documented; storage/QPS estimates filled in.",
        "solution_notes": "Cache hot codes; base62 encoding; collision strategy.",
        "difficulty": "medium",
        "estimated_minutes": 40,
        "order": 2,
    },
]
