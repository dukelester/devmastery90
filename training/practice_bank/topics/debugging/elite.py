"""Debugging practice — Elite level (architecture and incident response)."""

TOPICS = [
    {
        "question": "Fix microservice timeout cascade that collapses checkout during catalog slowness.",
        "buggy_code": '''# API gateway — synchronous fan-out
def checkout(cart_id):
    cart = cart_service.get(cart_id, timeout=30)
    catalog = catalog_service.validate(cart.items, timeout=30)
    payment = payment_service.charge(cart.total, timeout=30)
    return {"status": "ok"}  # 90s worst case, threads exhausted''',
        "solution_code": '''def checkout(cart_id):
    cart = cart_service.get(cart_id, timeout=2)
    catalog = catalog_service.validate(cart.items, timeout=2)
    if not catalog.ok:
        return fail_fast(catalog)
    payment = payment_service.charge(cart.total, timeout=5)
    return {"status": "ok"}
# bulkheads + async saga for non-critical steps''',
        "solution_explanation": "Deep synchronous chains multiply latency; enforce tight budgets, fail fast, and isolate thread pools.",
        "ideal_topics": "timeout cascade, bulkheads, microservices, SLOs",
        "hints": "What is the p99 budget per hop and total?",
        "learning_objectives": "Break synchronous timeout cascades in service meshes",
        "time_estimate_minutes": 30,
    },
    {
        "question": "Fix data migration script that corrupted production rows by swapping columns silently.",
        "buggy_code": '''# one-shot migration run against prod by mistake
UPDATE users SET email = username, username = email;
-- ran without WHERE, without transaction, without backup verification''',
        "solution_code": '''BEGIN;
CREATE TABLE users_backup AS SELECT * FROM users;
UPDATE users u
SET email = b.email, username = b.username
FROM staging_user_fix b
WHERE u.id = b.id AND b.validated = true;
-- verify counts, then COMMIT or ROLLBACK''',
        "solution_explanation": "Blind cross-column updates without backup, filter, or transaction are irreversible incident fuel.",
        "ideal_topics": "data migration safety, backups, transactions, incident response",
        "hints": "Was there a dry run, backup, and row-level join key?",
        "learning_objectives": "Execute production data fixes with verifiable rollback paths",
        "time_estimate_minutes": 30,
    },
    {
        "question": "Fix memory leak in long-running Celery worker processing large payloads.",
        "buggy_code": '''@shared_task
def process_blob(blob_id):
    data = download_entire_blob(blob_id)  # 500MB
    result = transform(data)
    GLOBAL_CACHE[blob_id] = result  # unbounded in-process cache
    return result''',
        "solution_code": '''@shared_task
def process_blob(blob_id):
    with download_blob_stream(blob_id) as stream:
        result = transform_stream(stream)
    store_result(blob_id, result)  # external store with TTL
    return result
# recycle workers: celery worker --max-tasks-per-child=100''',
        "solution_explanation": "Unbounded in-process caches and large objects retained across tasks leak memory; stream and recycle workers.",
        "ideal_topics": "memory leaks, Celery workers, streaming, max-tasks-per-child",
        "hints": "Does memory return to OS after task completion?",
        "learning_objectives": "Eliminate worker memory leaks in batch processors",
        "time_estimate_minutes": 28,
    },
    {
        "question": "Fix thundering herd when hot cache key expires simultaneously across pods.",
        "buggy_code": '''@cache(ttl=60)
def homepage_feed():
    return expensive_aggregate()  # all pods miss at T+60''',
        "solution_code": '''@cache(ttl=60, jitter=15)
def homepage_feed():
    return expensive_aggregate()

# plus early refresh lock:
def get_homepage_feed():
    val = cache.get("homepage")
    if val and cache.ttl("homepage") < 10:
        refresh_async_if_lock("homepage")
    if val is None:
        val = rebuild_with_lock("homepage")
    return val''',
        "solution_explanation": "Fixed TTL expires synchronously; add jitter and probabilistic early refresh with single-flight rebuild.",
        "ideal_topics": "thundering herd, cache TTL jitter, single-flight",
        "hints": "Do all clients expire the same key at the same second?",
        "learning_objectives": "Design cache expiration strategies that avoid synchronized misses",
        "time_estimate_minutes": 27,
    },
    {
        "question": "Fix split transaction across payment and inventory services without compensation.",
        "buggy_code": '''def place_order(order):
    payment_service.charge(order.total)
    inventory_service.reserve(order.items)  # fails after charge — money captured, no stock''',
        "solution_code": '''def place_order(order):
    saga = OrderSaga(order)
    saga.run([
        ("reserve", inventory_service.reserve, inventory_service.release),
        ("charge", payment_service.charge, payment_service.refund),
    ])
    # each step has compensating action on downstream failure''',
        "solution_explanation": "Cross-service workflows need sagas with compensating transactions, not sequential calls without rollback.",
        "ideal_topics": "distributed transactions, saga pattern, compensation",
        "hints": "What happens if step two fails after step one succeeds?",
        "learning_objectives": "Model cross-service workflows with compensating sagas",
        "time_estimate_minutes": 30,
    },
    {
        "question": "Fix observability blind spot during incident — logs missing correlation ids across services.",
        "buggy_code": '''def handle_event(event):
    logger.info("processing event")
    downstream.process(event)  # no trace/log correlation''',
        "solution_code": '''def handle_event(event):
    ctx = {"trace_id": event.trace_id or uuid4().hex, "order_id": event.order_id}
    with log_context(**ctx):
        logger.info("processing event")
        downstream.process(event, headers=propagate_headers(ctx))''',
        "solution_explanation": "Without propagated correlation ids, cross-service incidents cannot be reconstructed quickly.",
        "ideal_topics": "correlation id, structured logging, incident debugging",
        "hints": "Can you follow one order id across all log lines?",
        "learning_objectives": "Instrument cross-service flows with correlation identifiers",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Fix autoscaling lag causing OOM during traffic spike before new pods register.",
        "buggy_code": '''# HPA scales on CPU average, 60s stabilization window
# Traffic 10x in 30s — existing pods accept all load until new pods ready''',
        "solution_code": '''# Add RPS-based scaling + predictive scaling + maxSurge
# Queue overload at edge (429) + client backoff
# Pre-warm minimum replicas during known events
hpa.metrics = [cpu, requests_per_second]
hpa.minReplicas = baseline_for_peak * 0.5''',
        "solution_explanation": "CPU lagging indicators react too slowly; combine request-rate signals, minimums, and edge backpressure.",
        "ideal_topics": "autoscaling lag, HPA, backpressure, capacity planning",
        "hints": "How long from metric breach to ready pod?",
        "learning_objectives": "Mitigate autoscaling lag during sharp traffic spikes",
        "time_estimate_minutes": 28,
    },
    {
        "question": "Fix schema drift breaking downstream consumers after producer deploy.",
        "buggy_code": '''# Producer v2 deploy — renames field total_cents -> amount_cents without compatibility window
event = {"order_id": 1, "amount_cents": 999}''',
        "solution_code": '''# Expand: emit both fields during transition
event = {
    "order_id": 1,
    "total_cents": 999,      # deprecated but present
    "amount_cents": 999,     # new canonical field
    "schema_version": 2,
}''',
        "solution_explanation": "Breaking schema changes require dual-write/dual-read compatibility periods and versioned contracts.",
        "ideal_topics": "schema evolution, compatibility, event contracts",
        "hints": "Can old consumers ignore unknown fields and read old names?",
        "learning_objectives": "Roll out schema changes without breaking consumers",
        "time_estimate_minutes": 27,
    },
    {
        "question": "Fix poison message loop crashing consumer group indefinitely.",
        "buggy_code": '''for msg in consumer:
    try:
        handle(msg)
    except Exception:
        raise  # broker redelivers forever — poison pill''',
        "solution_code": '''for msg in consumer:
    try:
        handle(msg)
    except ValidationError as exc:
        dead_letter.publish(msg, reason=str(exc))  # quarantine bad messages
        consumer.commit()
    except Exception:
        retry_with_backoff(msg)''',
        "solution_explanation": "Non-transient bad payloads must route to DLQ after bounded retries, not infinite redelivery.",
        "ideal_topics": "poison messages, dead letter queue, consumer reliability",
        "hints": "Will retrying fix a permanently invalid payload?",
        "learning_objectives": "Quarantine poison messages without stalling consumers",
        "time_estimate_minutes": 26,
    },
    {
        "question": "Fix incomplete GDPR delete that left PII in analytics warehouse.",
        "buggy_code": '''def delete_user(user_id):
    User.objects.filter(pk=user_id).delete()  # OLTP only''',
        "solution_code": '''def delete_user(user_id):
    User.objects.filter(pk=user_id).delete()
    enqueue_anonymize(user_id)  # propagate to warehouse, search, backups
    tombstone_registry.record(user_id, deleted_at=now())''',
        "solution_explanation": "User deletion must cascade to async pipelines, derived stores, and retention policies.",
        "ideal_topics": "GDPR, data deletion propagation, compliance",
        "hints": "Where else is user PII copied asynchronously?",
        "learning_objectives": "Design deletion flows that reach derived data stores",
        "time_estimate_minutes": 29,
    },
    {
        "question": "Fix multi-tenant data isolation breach via missing org filter in shared query.",
        "buggy_code": '''def list_invoices(request):
    return Invoice.objects.filter(status="open")  # no tenant scoping''',
        "solution_code": '''def list_invoices(request):
    return Invoice.objects.filter(
        organization_id=request.user.organization_id,
        status="open",
    )''',
        "solution_explanation": "Shared tables require mandatory tenant predicates on every query path.",
        "ideal_topics": "multi-tenancy, authorization, data isolation",
        "hints": "Can tenant A infer tenant B rows from sequential ids?",
        "learning_objectives": "Enforce tenant scoping in all data access layers",
        "time_estimate_minutes": 26,
    },
    {
        "question": "Fix canary analysis using wrong success metric that hid elevated 500 rate.",
        "buggy_code": '''# Canary pass criteria: average latency only
if canary.p99_latency < baseline.p99_latency:
    promote()  # 500 rate doubled but latency improved slightly''',
        "solution_code": '''if (
    canary.error_rate <= baseline.error_rate * 1.05
    and canary.p99_latency <= baseline.p99_latency * 1.10
    and canary.business_kpi("checkout_success") >= baseline.kpi * 0.99
):
    promote()
else:
    rollback()''',
        "solution_explanation": "Single-metric canary gates miss regressions; combine error rate, latency, and business KPIs.",
        "ideal_topics": "canary deployments, SLOs, release safety",
        "hints": "Would you ship if errors spike but latency drops?",
        "learning_objectives": "Define multi-signal canary promotion criteria",
        "time_estimate_minutes": 27,
    },
    {
        "question": "Fix rollback that left mixed schema versions across sharded databases.",
        "buggy_code": '''# Roll back app only — migration 202602 already applied on 3/8 shards
deploy.previous_version()''',
        "solution_code": '''# Forward-fix preferred; if rollback required:
# 1. freeze writes
# 2. verify migration status per shard
# 3. apply compensating migration or complete rollout on all shards
# 4. deploy compatible app version''',
        "solution_explanation": "App rollback without schema compatibility across shards causes runtime crashes; forward-fix or uniform schema state required.",
        "ideal_topics": "rollback strategy, sharded migrations, forward-fix",
        "hints": "Is the database schema backward compatible with the rolled-back app?",
        "learning_objectives": "Plan rollbacks with schema compatibility across shards",
        "time_estimate_minutes": 30,
    },
    {
        "question": "Fix clock skew breaking JWT and replay protection across nodes.",
        "buggy_code": '''def validate_token(token):
    payload = jwt.decode(token, key, algorithms=["HS256"])
    if payload["iat"] > time.time():  # nodes drift ±5 minutes
        raise InvalidToken()''',
        "solution_code": '''def validate_token(token):
    payload = jwt.decode(
        token,
        key,
        algorithms=["HS256"],
        leeway=300,  # tolerate bounded skew
    )
    # enforce NTP on all nodes; monitor clock drift metrics''',
        "solution_explanation": "Strict time checks without NTP discipline reject valid tokens; allow leeway and monitor drift.",
        "ideal_topics": "clock skew, JWT iat/exp, NTP",
        "hints": "Are all servers synchronized within seconds?",
        "learning_objectives": "Handle clock skew in distributed authentication",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Fix hot partition in sharded orders table overwhelming single database node.",
        "buggy_code": '''def shard_for(tenant_id):
    return tenant_id % 4  # mega-tenant id=0 maps to shard 0 always''',
        "solution_code": '''def shard_for(tenant_id):
    return hash_shard(f"{tenant_id}", num_shards=64)  # spread large tenants

# plus separate logical shard for flagged hot tenants''',
        "solution_explanation": "Modulo on low-cardinality ids concentrates hot tenants; use consistent hashing and hot-tenant isolation.",
        "ideal_topics": "sharding, hot partitions, consistent hashing",
        "hints": "Does one tenant dominate write volume on a shard?",
        "learning_objectives": "Reshard workloads to eliminate hot partitions",
        "time_estimate_minutes": 29,
    },
    {
        "question": "Fix missing backpressure causing OOM when downstream indexing lagged.",
        "buggy_code": '''def on_message(msg):
    batch.append(msg)
    if len(batch) >= 1000:
        indexer.bulk_send(batch)  # unbounded batch if indexer slow
        batch.clear()''',
        "solution_code": '''queue = BoundedQueue(maxsize=5000)

def on_message(msg):
    queue.put(msg, timeout=1)  # block or drop with metric

def indexer_worker():
    while True:
        batch = queue.drain(max_items=1000, timeout=0.5)
        if batch:
            indexer.bulk_send(batch)''',
        "solution_explanation": "Unbounded in-memory buffering grows without limit when consumers lag; bound queues and apply backpressure.",
        "ideal_topics": "backpressure, bounded queues, OOM prevention",
        "hints": "What happens if indexer throughput < producer rate for minutes?",
        "learning_objectives": "Apply backpressure to protect services under sustained overload",
        "time_estimate_minutes": 28,
    },
    {
        "question": "Fix saga compensation failure leaving orphaned reservation after refund error.",
        "buggy_code": '''try:
    inventory.reserve(order)
    payment.charge(order)
except PaymentError:
    inventory.release(order)  # release fails silently — inventory stuck''',
        "solution_code": '''try:
    inventory.reserve(order)
    payment.charge(order)
except PaymentError:
    compensations.enqueue("release_inventory", order.id, retry_policy=exponential)
    raise
# reconciliation job scans stale reservations''',
        "solution_explanation": "Compensations must be durable retried workflows, not one-shot calls that can fail silently.",
        "ideal_topics": "saga compensation, reconciliation, durable retries",
        "hints": "Is there a ledger of pending compensations?",
        "learning_objectives": "Make saga compensations reliable and auditable",
        "time_estimate_minutes": 29,
    },
    {
        "question": "Fix config drift between staging and production causing surprise outage on promote.",
        "buggy_code": '''# staging.env
CACHE_URL=redis://localhost:6379/0
# production.env (undocumented)
CACHE_URL=redis://prod-cluster:6379/0
FEATURE_X=true  # only in prod''',
        "solution_code": '''# Single source templated config with required keys validated at boot
settings = load_config(env=os.environ["APP_ENV"], schema=ConfigSchema)
settings.validate_required(["CACHE_URL", "FEATURE_X"])
# diff staging vs prod in CI promotion gate''',
        "solution_explanation": "Undocumented env divergence breaks parity; schema-validate config and gate promotes on diffs.",
        "ideal_topics": "configuration management, environment parity, CI gates",
        "hints": "Would staging have caught the prod-only flag interaction?",
        "learning_objectives": "Prevent environment config drift from causing production incidents",
        "time_estimate_minutes": 26,
    },
    {
        "question": "Fix dependency upgrade that broke ABI compatibility in native extension wheel.",
        "buggy_code": '''# requirements.txt pin bump without rebuild
cryptography==42.0.0  # upgraded
# deployed prebuilt wheel compiled against cryptography 41.x — segfault at import''',
        "solution_code": '''# Pin transitive deps + rebuild wheels in CI for target manylinux
cryptography==42.0.0
# CI: pip install --no-binary :all: where needed; run smoke import test
# lockfile: pip-tools / poetry lock + test matrix''',
        "solution_explanation": "Native wheels bind to specific ABI; upgrade requires rebuild and import smoke tests in CI.",
        "ideal_topics": "dependency upgrades, ABI compatibility, CI smoke tests",
        "hints": "Was the extension rebuilt after the cryptography major bump?",
        "learning_objectives": "Safely upgrade native Python dependencies in production",
        "time_estimate_minutes": 27,
    },
    {
        "question": "Fix post-incident runbook gap — on-call repeated manual steps not captured after Sev-1.",
        "buggy_code": '''# Incident resolved in Slack threads; no runbook update
# Next occurrence: new engineer repeats 45-minute manual cache flush procedure''',
        "solution_code": '''# Post-incident actions:
# 1. blameless review with timeline
# 2. document detection + mitigation in runbook repo
# 3. automate cache flush via guarded admin command
# 4. add monitor alert 15 minutes earlier in failure chain''',
        "solution_explanation": "Incidents without runbook and automation updates guarantee repeat toil and longer MTTR.",
        "ideal_topics": "incident response, runbooks, postmortems, toil reduction",
        "hints": "What manual steps did the resolver perform that are not documented?",
        "learning_objectives": "Convert incident learnings into runbooks and automation",
        "time_estimate_minutes": 25,
    },
]
