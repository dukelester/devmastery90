"""Debugging practice — Expert level (distributed systems and production)."""

TOPICS = [
    {
        "question": "Fix split-brain writes caused by independent regional caches without coordination.",
        "buggy_code": '''# Production config — two regions write locally first
def update_feature_flag(name, enabled):
    local_cache.set(name, enabled)  # us-east
    replicate_async(name, enabled)  # best-effort to eu-west
    return enabled

# Reads may see different values per region during partition''',
        "solution_code": '''# Use versioned writes with central authority or consensus store
def update_feature_flag(name, enabled):
    version = flag_store.compare_and_set(name, enabled)  # single source of truth
    fanout.invalidate(name, version)  # regions drop stale entries
    return enabled''',
        "solution_explanation": "Independent writable caches diverge under partition; designate authority or use versioned invalidation.",
        "ideal_topics": "split brain, distributed cache, eventual consistency",
        "hints": "Who is the source of truth when regions disagree?",
        "learning_objectives": "Diagnose split-brain in multi-region cache architectures",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Fix read-your-writes failure after profile update in a replicated database.",
        "buggy_code": '''def update_profile(user_id, data):
    primary.execute("UPDATE profiles SET ... WHERE user_id=%s", [user_id])
    return {"ok": True}

def get_profile(user_id):
    return replica.query("SELECT ... FROM profiles WHERE user_id=%s", [user_id])''',
        "solution_code": '''def update_profile(user_id, data):
    primary.execute("UPDATE profiles SET ... WHERE user_id=%s", [user_id])
    session["sticky_primary_until"] = time.time() + 5  # short primary stickiness
    return {"ok": True}

def get_profile(user_id):
    if session.get("sticky_primary_until", 0) > time.time():
        return primary.query("SELECT ... FROM profiles WHERE user_id=%s", [user_id])
    return replica.query("SELECT ... FROM profiles WHERE user_id=%s", [user_id])''',
        "solution_explanation": "Replica lag causes stale reads immediately after writes; route recent writes to primary or use session stickiness.",
        "ideal_topics": "read-your-writes, replication lag, session stickiness",
        "hints": "Does the read path always hit the same node that served the write?",
        "learning_objectives": "Guarantee read-your-writes under asynchronous replication",
        "time_estimate_minutes": 24,
    },
    {
        "question": "Fix Kafka consumer that commits offsets before processing completes.",
        "buggy_code": '''consumer = KafkaConsumer("orders", enable_auto_commit=True)

for msg in consumer:
    process_order(msg.value)  # may fail after auto-commit''',
        "solution_code": '''consumer = KafkaConsumer("orders", enable_auto_commit=False)

for msg in consumer:
    try:
        process_order(msg.value)
    except Exception:
        log.exception("processing failed")
        raise
    else:
        consumer.commit()  # commit only after successful processing''',
        "solution_explanation": "Auto-commit before handler success loses messages on crash; commit manually after idempotent processing.",
        "ideal_topics": "Kafka, offset commit, at-least-once delivery",
        "hints": "When should offsets advance relative to side effects?",
        "learning_objectives": "Align Kafka offset commits with successful processing",
        "time_estimate_minutes": 23,
    },
    {
        "question": "Fix circuit breaker that flaps open/closed under partial downstream slowness.",
        "buggy_code": '''breaker = CircuitBreaker(failure_threshold=5, reset_timeout=5)

@breaker
def call_payments():
    return requests.post(PAYMENTS_URL, timeout=0.2)  # too aggressive''',
        "solution_code": '''breaker = CircuitBreaker(
    failure_threshold=5,
    reset_timeout=30,
    half_open_max_calls=3,
)

@breaker
def call_payments():
    return requests.post(PAYMENTS_URL, timeout=2.0)  # realistic SLO timeout''',
        "solution_explanation": "Overly short timeouts inflate failure counts; tune thresholds and half-open probe limits.",
        "ideal_topics": "circuit breaker, timeouts, cascading failures",
        "hints": "Are timeouts causing false failures that trip the breaker?",
        "learning_objectives": "Tune circuit breakers to avoid flapping on slow dependencies",
        "time_estimate_minutes": 24,
    },
    {
        "question": "Fix blue-green deployment that drops sessions because load balancer stickiness targets old pool.",
        "buggy_code": '''# Deploy script switches 100% traffic instantly
lb.set_backend("green")
# Sessions stored in-memory on blue workers are lost''',
        "solution_code": '''# Drain blue with sticky cookie honoring existing sessions
lb.enable_dual_backend(blue_weight=0, green_weight=100, drain_blue=True)
session_store = RedisSessionBackend()  # shared store across colors
lb.set_backend("green")  # after blue connections drain''',
        "solution_explanation": "Instant cutover with in-memory sessions breaks users; drain connections and externalize session state.",
        "ideal_topics": "blue-green deployment, session stickiness, zero-downtime",
        "hints": "Where are sessions stored and does the LB drain existing connections?",
        "learning_objectives": "Preserve sessions during blue-green traffic shifts",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Fix broken distributed tracing where child spans detach from parent context.",
        "buggy_code": '''def handle_request(request):
    with tracer.start_span("http") as span:
        ctx = span.context
        executor.submit(process_async, request.body)  # context not propagated

def process_async(body):
    with tracer.start_span("worker"):  # orphan span
        ...''',
        "solution_code": '''def handle_request(request):
    with tracer.start_span("http") as span:
        ctx = span.context
        executor.submit(process_async, request.body, ctx)

def process_async(body, parent_ctx):
    with tracer.start_span("worker", child_of=parent_ctx):  # linked trace
        ...''',
        "solution_explanation": "Span context must be passed across threads/processes; otherwise traces fragment.",
        "ideal_topics": "distributed tracing, span context, async propagation",
        "hints": "How does the worker inherit the HTTP span id?",
        "learning_objectives": "Propagate trace context across async boundaries",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Fix S3 listing logic that misses recently uploaded objects due to eventual consistency assumptions.",
        "buggy_code": '''def list_and_process(prefix):
    keys = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)["Contents"]
    for obj in keys:
        process(obj["Key"])  # assumes list is immediately complete''',
        "solution_code": '''def list_and_process(prefix):
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            if head_object_exists(obj["Key"]):  # verify before processing
                process(obj["Key"])''',
        "solution_explanation": "Listing may lag behind PUT; verify existence or retry with backoff for critical pipelines.",
        "ideal_topics": "S3, eventual consistency, list pagination",
        "hints": "Can an object exist before it appears in list results?",
        "learning_objectives": "Handle object storage listing lag in pipelines",
        "time_estimate_minutes": 23,
    },
    {
        "question": "Fix leader election that allows dual leaders during network partition.",
        "buggy_code": '''def acquire_leadership():
    if redis.set("leader", NODE_ID, nx=True, ex=30):
        return True
    return redis.get("leader") == NODE_ID  # no renewal/fencing''',
        "solution_code": '''def acquire_leadership():
    token = uuid4().hex
    if redis.set("leader", token, nx=True, ex=10):
        schedule_renew(token)
        return token
    return None

def renew(token):
    # renew only if value matches token — lost leadership if key changed
    if not redis.eval(RENEW_SCRIPT, 1, "leader", token, NODE_ID):
        stop_work()  # fence stale leader''',
        "solution_explanation": "TTL locks without fencing tokens allow split leadership; renew with token verification and stop on loss.",
        "ideal_topics": "leader election, Redis locks, fencing tokens",
        "hints": "What happens when two nodes both believe they hold the lock?",
        "learning_objectives": "Implement safe leader election with fencing",
        "time_estimate_minutes": 26,
    },
    {
        "question": "Fix graceful shutdown that drops in-flight HTTP requests during deploy.",
        "buggy_code": '''# SIGTERM handler
def on_sigterm(*_):
    sys.exit(0)  # immediate exit''',
        "solution_code": '''def on_sigterm(*_):
    server.stop_accepting()
    deadline = time.time() + 30
    while in_flight_requests > 0 and time.time() < deadline:
        time.sleep(0.2)
    server.close()
    sys.exit(0)''',
        "solution_explanation": "Immediate exit on SIGTERM aborts active connections; drain in-flight work within termination grace.",
        "ideal_topics": "graceful shutdown, SIGTERM, Kubernetes terminationGracePeriod",
        "hints": "Stop accepting new work, wait for active requests, then exit.",
        "learning_objectives": "Drain in-flight requests during graceful shutdown",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Fix feature flag cache invalidation that serves stale flags for hours.",
        "buggy_code": '''def get_flag(name):
    val = local_cache.get(name)
    if val is None:
        val = remote_flags.fetch(name)
        local_cache.set(name, val, ttl=86400)  # 24h
    return val''',
        "solution_code": '''def get_flag(name):
    val = local_cache.get(name)
    if val is None:
        val = remote_flags.fetch(name)
        local_cache.set(name, val, ttl=60)  # short TTL
    return val

# plus pub/sub invalidation on admin updates
def on_flag_update(event):
    local_cache.delete(event.name)''',
        "solution_explanation": "Long TTL without pub/sub invalidation hides flag changes; combine short TTL with push invalidation.",
        "ideal_topics": "feature flags, cache invalidation, pub/sub",
        "hints": "How quickly must flag changes propagate to all pods?",
        "learning_objectives": "Invalidate feature flag caches on configuration changes",
        "time_estimate_minutes": 21,
    },
    {
        "question": "Fix database migration that locks production table indefinitely.",
        "buggy_code": '''-- SQL migration (PostgreSQL)
ALTER TABLE orders ADD COLUMN tax_cents integer NOT NULL DEFAULT 0;
-- full table rewrite + ACCESS EXCLUSIVE lock on large table''',
        "solution_code": '''-- Expand-contract pattern
ALTER TABLE orders ADD COLUMN tax_cents integer;  -- nullable first
UPDATE orders SET tax_cents = 0 WHERE tax_cents IS NULL;  -- batched backfill
ALTER TABLE orders ALTER COLUMN tax_cents SET DEFAULT 0;
ALTER TABLE orders ALTER COLUMN tax_cents SET NOT NULL;  -- after backfill''',
        "solution_explanation": "Adding NOT NULL DEFAULT in one step rewrites huge tables; use expand/backfill/contract to limit locking.",
        "ideal_topics": "PostgreSQL migrations, lock duration, expand-contract",
        "hints": "Can the column be added nullable and backfilled in batches?",
        "learning_objectives": "Run zero-downtime schema migrations on large tables",
        "time_estimate_minutes": 26,
    },
    {
        "question": "Fix Prometheus metrics explosion from unbounded label cardinality.",
        "buggy_code": '''def record_request(path, user_id):
    REQUESTS.labels(path=path, user_id=user_id).inc()  # unique label per user''',
        "solution_code": '''def record_request(path, user_id):
    REQUESTS.labels(path=normalize_path(path)).inc()  # bounded path labels only
    # track per-user metrics separately via logs/traces, not Prometheus labels''',
        "solution_explanation": "High-cardinality labels create millions of time series and crash metrics backends.",
        "ideal_topics": "Prometheus, cardinality, observability cost",
        "hints": "Are label values bounded or unbounded?",
        "learning_objectives": "Prevent metrics cardinality explosions in production",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Fix retry storm that amplifies outage traffic to a failing dependency.",
        "buggy_code": '''@retry(max_attempts=10, backoff=0.1)
def fetch_inventory(sku):
    return inventory_client.get(sku)  # all callers retry aggressively''',
        "solution_code": '''@retry(max_attempts=3, backoff=1.0, jitter=True)
def fetch_inventory(sku):
    if breaker.open:
        raise ServiceUnavailable()
    return inventory_client.get(sku)''',
        "solution_explanation": "Synchronized retries multiply load; cap attempts, add jitter, and honor circuit breaker open state.",
        "ideal_topics": "retry storms, jitter, circuit breaker, cascading failure",
        "hints": "Do all clients retry at the same interval?",
        "learning_objectives": "Mitigate retry storms during dependency outages",
        "time_estimate_minutes": 23,
    },
    {
        "question": "Fix idempotency key handling that treats collisions as success.",
        "buggy_code": '''def create_payment(idempotency_key, payload):
    if cache.get(idempotency_key):
        return cache.get(idempotency_key)  # returns prior response even if payload differs
    result = gateway.charge(payload)
    cache.set(idempotency_key, result, ttl=86400)
    return result''',
        "solution_code": '''def create_payment(idempotency_key, payload):
    cached = cache.get(idempotency_key)
    if cached:
        if cached.request_hash != hash_payload(payload):
            raise IdempotencyConflict()
        return cached.response
    result = gateway.charge(payload)
    cache.set(idempotency_key, IdempotencyRecord(hash_payload(payload), result))
    return result''',
        "solution_explanation": "Idempotency keys must bind to request body hash; mismatched replays should 409, not return wrong result.",
        "ideal_topics": "idempotency keys, payment APIs, conflict handling",
        "hints": "Same key with different payload — safe to return cached response?",
        "learning_objectives": "Implement idempotency keys with payload fingerprinting",
        "time_estimate_minutes": 24,
    },
    {
        "question": "Fix multi-region replication lag causing duplicate order fulfillment.",
        "buggy_code": '''def fulfill(order_id):
    order = db_replica.get(order_id)
    if order.status == "paid":
        ship(order)
        order.status = "shipped"
        db_primary.save(order)''',
        "solution_code": '''def fulfill(order_id):
    updated = db_primary.execute(
        "UPDATE orders SET status='shipped' WHERE id=%s AND status='paid'",
        [order_id],
    )
    if updated.rowcount == 1:
        order = db_primary.get(order_id)
        ship(order)  # conditional write prevents double ship''',
        "solution_explanation": "Read-modify-write on lagging replica races; use conditional atomic update on primary.",
        "ideal_topics": "replication lag, compare-and-swap, fulfillment idempotency",
        "hints": "Can two workers read `paid` from stale replicas simultaneously?",
        "learning_objectives": "Prevent duplicate side effects under replication lag",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Fix health check that reports healthy while dependency is degraded.",
        "buggy_code": '''def health():
    return {"status": "ok"}  # never checks database''',
        "solution_code": '''def health():
    checks = {
        "database": check_db(timeout=0.5),
        "cache": check_redis(timeout=0.5),
    }
    status = "ok" if all(checks.values()) else "degraded"
    code = 200 if status == "ok" else 503
    return JsonResponse({"status": status, "checks": checks}, status=code)''',
        "solution_explanation": "Liveness-only endpoints hide broken dependencies; readiness must fail when critical deps are down.",
        "ideal_topics": "health checks, readiness vs liveness, load balancer routing",
        "hints": "Should traffic route to pods that cannot reach the database?",
        "learning_objectives": "Build readiness checks that reflect dependency health",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Fix secrets rotation leaving stale credentials in process memory cache.",
        "buggy_code": '''API_KEY = os.environ["API_KEY"]  # loaded once at import

def client():
    return ExternalClient(api_key=API_KEY)''',
        "solution_code": '''def current_api_key():
    return secrets_manager.get("API_KEY")  # fetch on demand or subscribe to rotation

def client():
    return ExternalClient(api_key=current_api_key())''',
        "solution_explanation": "Import-time env vars never refresh after rotation; reload from secret store or signal handlers.",
        "ideal_topics": "secrets rotation, configuration reload, twelve-factor",
        "hints": "When was the secret read relative to rotation events?",
        "learning_objectives": "Reload secrets dynamically after rotation",
        "time_estimate_minutes": 21,
    },
    {
        "question": "Fix sticky session leak on load balancer after scale-down event.",
        "buggy_code": '''# ALB stickiness cookie points to terminated instance ip-10-0-1-12
# Users with old cookies get 502 until cookie expires''',
        "solution_code": '''# Reduce stickiness duration + connection draining on scale-in
# Target group deregistration delay = 300s
# Stickiness enabled with duration=86400 -> reduce to 3600 and drain on shutdown''',
        "solution_explanation": "Long-lived stickiness cookies reference removed targets; shorten duration and drain on deregistration.",
        "ideal_topics": "load balancer stickiness, scale-in, connection draining",
        "hints": "What happens to cookies bound to removed backend targets?",
        "learning_objectives": "Prevent sticky session failures during scale-down",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Fix outbox pattern duplicate publish when relay crashes mid-flight.",
        "buggy_code": '''def relay_events():
    rows = Outbox.objects.filter(published=False)[:100]
    for row in rows:
        broker.publish(row.topic, row.payload)
        row.published = True
        row.save()  # crash here republishes same event''',
        "solution_code": '''def relay_events():
    rows = Outbox.objects.select_for_update(skip_locked=True).filter(published=False)[:100]
    for row in rows:
        broker.publish(row.topic, row.payload)
        row.published = True
        row.published_at = timezone.now()
        row.save()
        # consumers must dedupe on event_id''',
        "solution_explanation": "Mark published only after broker ack or make consumers idempotent on event_id; use row locks to avoid double relay.",
        "ideal_topics": "transactional outbox, at-least-once delivery, idempotent consumers",
        "hints": "Can the relay crash between publish and DB update?",
        "learning_objectives": "Make outbox relays safe under crash and retry",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Fix incorrect CAP assumption that AP cache can provide strong inventory counts.",
        "buggy_code": '''def available_units(sku):
    return cache.get(f"stock:{sku}")  # async replicated cache

def purchase(sku, qty):
    if available_units(sku) >= qty:
        decrement_cache(sku, qty)
        create_order(sku, qty)  # oversell under partition''',
        "solution_code": '''def purchase(sku, qty):
    reserved = inventory_service.reserve(sku, qty)  # authoritative CP store
    if not reserved:
        raise OutOfStock()
    create_order(sku, qty)''',
        "solution_explanation": "Eventually consistent caches cannot enforce global invariants; inventory authority needs strong consistency.",
        "ideal_topics": "CAP theorem, inventory, strong vs eventual consistency",
        "hints": "Can two partitions both believe stock remains?",
        "learning_objectives": "Choose consistency models appropriate to business invariants",
        "time_estimate_minutes": 26,
    },
]
