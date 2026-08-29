"""Debugging practice — Hard level (concurrency, ORM, APIs)."""

TOPICS = [
    {
        "question": "Fix the Django view that triggers an N+1 query when listing posts with authors.",
        "buggy_code": '''# Django ORM snippet
def post_list(request):
    posts = Post.objects.all()
    data = []
    for post in posts:
        data.append({
            "title": post.title,
            "author": post.author.name,  # query per post
        })
    return JsonResponse({"posts": data})''',
        "solution_code": '''# Django ORM snippet
def post_list(request):
    posts = Post.objects.select_related("author").all()  # join author in one query
    data = [
        {"title": post.title, "author": post.author.name}
        for post in posts
    ]
    return JsonResponse({"posts": data})''',
        "solution_explanation": "Accessing `post.author` without prefetch/select_related causes one query per row.",
        "ideal_topics": "Django ORM, N+1 queries, select_related",
        "hints": "Use Django Debug Toolbar or `print(len(connection.queries))` to count queries.",
        "learning_objectives": "Eliminate N+1 ORM access with select_related",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Fix ManyToMany access that omits prefetch and explodes query count.",
        "buggy_code": '''def course_detail(course_id):
    course = Course.objects.get(pk=course_id)
    return [
        {"student": e.student.name, "grade": e.grade}
        for e in course.enrollments.all()  # plus query per enrollment.student
    ]''',
        "solution_code": '''def course_detail(course_id):
    course = (
        Course.objects.prefetch_related("enrollments__student")
        .get(pk=course_id)
    )
    return [
        {"student": e.student.name, "grade": e.grade}
        for e in course.enrollments.all()
    ]''',
        "solution_explanation": "Reverse FK and M2M chains need `prefetch_related` for related object hydration.",
        "ideal_topics": "Django ORM, prefetch_related, ManyToMany",
        "hints": "select_related is for FK joins; prefetch_related batches reverse relations.",
        "learning_objectives": "Use prefetch_related for reverse and many-to-many relations",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Fix cache get-or-set race that stores stale None forever.",
        "buggy_code": '''import threading
cache = {}
lock = threading.Lock()

def get_user(user_id):
    if user_id in cache:
        return cache[user_id]
    with lock:
        user = fetch_from_db(user_id)  # slow
        if not user:
            return None  # never cached — thundering herd on misses
        cache[user_id] = user
    return user''',
        "solution_code": '''import threading
cache = {}
lock = threading.Lock()

def get_user(user_id):
    if user_id in cache:
        return cache[user_id]
    with lock:
        if user_id in cache:  # double-checked locking
            return cache[user_id]
        user = fetch_from_db(user_id)
        cache[user_id] = user  # cache None too to prevent stampedes
    return cache[user_id]''',
        "solution_explanation": "Check-then-act outside the lock races; cache negative results to avoid repeated DB hits.",
        "ideal_topics": "caching, race conditions, double-checked locking",
        "hints": "Re-check inside the lock and consider caching misses briefly.",
        "learning_objectives": "Make cache population thread-safe under concurrency",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Fix lock ordering that causes deadlock between transfer operations.",
        "buggy_code": '''import threading

lock_a = threading.Lock()
lock_b = threading.Lock()

def transfer(from_acc, to_acc, amount):
    with lock_a if from_acc.id < to_acc.id else lock_b:
        with lock_b if from_acc.id < to_acc.id else lock_a:
            from_acc.balance -= amount
            to_acc.balance += amount''',
        "solution_code": '''import threading

locks = {}

def account_lock(account_id):
    if account_id not in locks:
        locks[account_id] = threading.Lock()
    return locks[account_id]

def transfer(from_acc, to_acc, amount):
    first, second = sorted([from_acc.id, to_acc.id])
    with account_lock(first):
        with account_lock(second):
            from_acc.balance -= amount
            to_acc.balance += amount''',
        "solution_explanation": "Deadlock happens when threads acquire the same locks in opposite order; always lock in global order.",
        "ideal_topics": "deadlock, lock ordering, threading",
        "hints": "Sort resource IDs before acquiring multiple locks.",
        "learning_objectives": "Prevent deadlock with consistent lock acquisition order",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Fix Celery task that is not idempotent and double-charges customers on retry.",
        "buggy_code": '''@shared_task(bind=True, max_retries=3)
def charge_invoice(self, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    gateway.charge(invoice.amount, invoice.customer_id)
    invoice.status = "paid"
    invoice.save()''',
        "solution_code": '''@shared_task(bind=True, max_retries=3)
def charge_invoice(self, invoice_id):
    invoice = Invoice.objects.select_for_update().get(pk=invoice_id)
    if invoice.status == "paid":
        return "already paid"  # idempotent on retry
    charge_id = gateway.charge(invoice.amount, invoice.customer_id)
    invoice.status = "paid"
    invoice.charge_id = charge_id
    invoice.save()''',
        "solution_explanation": "Retries re-run side effects; guard with status checks and store external ids for deduplication.",
        "ideal_topics": "Celery, idempotency, retries, payments",
        "hints": "What happens if the worker crashes after charging but before saving?",
        "learning_objectives": "Design idempotent background tasks with safe retries",
        "time_estimate_minutes": 22,
    },
    {
        "question": "Fix REST list endpoint that returns unbounded results and times out.",
        "buggy_code": '''@api_view(["GET"])
def list_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)''',
        "solution_code": '''@api_view(["GET"])
def list_orders(request):
    qs = Order.objects.filter(user=request.user).order_by("-created_at")
    page = paginate_queryset(qs, request, page_size=50)  # cursor/page pagination
    serializer = OrderSerializer(page, many=True)
    return Response({"results": serializer.data, "next": page.next})''',
        "solution_explanation": "Unpaginated list endpoints load entire tables into memory and serialize slowly.",
        "ideal_topics": "REST APIs, pagination, performance",
        "hints": "Cap page size and return continuation tokens or next links.",
        "learning_objectives": "Add pagination to prevent unbounded API responses",
        "time_estimate_minutes": 17,
    },
    {
        "question": "Fix SQL injection in a raw query built with string formatting.",
        "buggy_code": '''# SQL snippet — vulnerable
def find_user(username):
    sql = f"SELECT id, email FROM users WHERE username = '{username}'"
    return connection.cursor().execute(sql)''',
        "solution_code": '''# SQL snippet — parameterized
def find_user(username):
    sql = "SELECT id, email FROM users WHERE username = %s"
    with connection.cursor() as cursor:
        cursor.execute(sql, [username])  # bind parameters safely
        return cursor.fetchall()''',
        "solution_explanation": "Interpolating user input into SQL lets attackers alter query structure; always bind parameters.",
        "ideal_topics": "SQL injection, parameterized queries, security",
        "hints": "Never embed user strings directly into SQL text.",
        "learning_objectives": "Replace string-built SQL with parameterized queries",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Fix connection pool exhaustion from cursors not closed in a loop.",
        "buggy_code": '''def export_rows(ids):
    results = []
    for row_id in ids:
        cursor = connection.cursor()
        cursor.execute("SELECT payload FROM events WHERE id = %s", [row_id])
        results.append(cursor.fetchone())
    return results  # cursors never closed''',
        "solution_code": '''def export_rows(ids):
    results = []
    with connection.cursor() as cursor:
        for row_id in ids:
            cursor.execute("SELECT payload FROM events WHERE id = %s", [row_id])
            results.append(cursor.fetchone())
    return results  # cursor context closes once''',
        "solution_explanation": "Leaked cursors hold connections from the pool until garbage-collected.",
        "ideal_topics": "database connections, connection pool, cursor lifecycle",
        "hints": "Use one cursor in a context manager or ensure explicit close.",
        "learning_objectives": "Release DB cursors to avoid pool exhaustion",
        "time_estimate_minutes": 17,
    },
    {
        "question": "Fix asyncio.gather that hides failures and returns partial success silently.",
        "buggy_code": '''import asyncio

async def fetch_one(url):
    ...

async def fetch_all(urls):
    return await asyncio.gather(*(fetch_one(u) for u in urls))  # first exception cancels others''',
        "solution_code": '''import asyncio

async def fetch_one(url):
    ...

async def fetch_all(urls):
    results = await asyncio.gather(
        *(fetch_one(u) for u in urls),
        return_exceptions=True,  # capture failures per task
    )
    errors = [r for r in results if isinstance(r, Exception)]
    if errors:
        raise errors[0]
    return results''',
        "solution_explanation": "Default gather fails fast; `return_exceptions=True` surfaces per-task errors for inspection.",
        "ideal_topics": "asyncio.gather, error handling, concurrent I/O",
        "hints": "Decide whether one failure should cancel siblings or be collected.",
        "learning_objectives": "Handle per-task exceptions in asyncio.gather",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Fix Django transaction.atomic block that commits partial work on exception.",
        "buggy_code": '''from django.db import transaction

def reassign_owner(project_id, new_owner_id):
    project = Project.objects.get(pk=project_id)
    with transaction.atomic():
        project.owner_id = new_owner_id
        project.save()
    AuditLog.objects.create(action="reassign", project_id=project_id)  # outside atomic''',
        "solution_code": '''from django.db import transaction

def reassign_owner(project_id, new_owner_id):
    with transaction.atomic():
        project = Project.objects.select_for_update().get(pk=project_id)
        project.owner_id = new_owner_id
        project.save()
        AuditLog.objects.create(action="reassign", project_id=project_id)  # same transaction''',
        "solution_explanation": "Operations outside `atomic()` are not rolled back with the main unit of work.",
        "ideal_topics": "Django transactions, atomic, consistency",
        "hints": "Include all related writes that must succeed or fail together inside one atomic block.",
        "learning_objectives": "Scope related DB writes within a single transaction.atomic",
        "time_estimate_minutes": 19,
    },
    {
        "question": "Fix cache stampede where many workers recompute the same expensive key.",
        "buggy_code": '''def get_report(report_id):
    key = f"report:{report_id}"
    data = cache.get(key)
    if data is None:
        data = build_report(report_id)  # 10s CPU — all workers enter here
        cache.set(key, data, timeout=300)
    return data''',
        "solution_code": '''def get_report(report_id):
    key = f"report:{report_id}"
    data = cache.get(key)
    if data is None:
        with cache.lock(f"lock:{key}", timeout=30):
            data = cache.get(key)
            if data is None:
                data = build_report(report_id)
                cache.set(key, data, timeout=300)
    return data''',
        "solution_explanation": "Use a short-lived lock or single-flight pattern so only one worker rebuilds a hot key.",
        "ideal_topics": "cache stampede, Redis lock, single-flight",
        "hints": "Double-check the cache after acquiring a rebuild lock.",
        "learning_objectives": "Prevent thundering herd on cache expiration",
        "time_estimate_minutes": 21,
    },
    {
        "question": "Fix thread-local storage leak in a WSGI middleware that never clears request state.",
        "buggy_code": '''import threading
_request_local = threading.local()

class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_local.user = request.user
        response = self.get_response(request)
        return response  # user bleeds into next request on same thread''',
        "solution_code": '''import threading
_request_local = threading.local()

class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _request_local.user = request.user
        try:
            return self.get_response(request)
        finally:
            _request_local.user = None  # clear per-thread state''',
        "solution_explanation": "Thread pool workers reuse threads; locals must be reset after each request.",
        "ideal_topics": "threading.local, WSGI middleware, request isolation",
        "hints": "Use try/finally to clear locals even when downstream code raises.",
        "learning_objectives": "Clear thread-local state in middleware finally blocks",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Fix Gunicorn worker timeout misconfiguration killing long but valid exports.",
        "buggy_code": '''# gunicorn config snippet
timeout = 30

def export_large_dataset(request):
    rows = list(HugeTable.objects.all())  # 2 minutes
    return build_csv_response(rows)''',
        "solution_code": '''# gunicorn config snippet — move long work off request thread
timeout = 30

def export_large_dataset(request):
    job_id = enqueue_export.delay(request.user.id)  # Celery/async job
    return JsonResponse({"job_id": job_id, "status": "queued"}, status=202)''',
        "solution_explanation": "Sync request workers should finish within timeout; offload long jobs to background workers.",
        "ideal_topics": "Gunicorn timeout, background jobs, HTTP 202",
        "hints": "Return a job id and poll or webhook when work exceeds worker timeout.",
        "learning_objectives": "Move long-running work off synchronous web workers",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Fix Django middleware order so authentication runs before permission checks.",
        "buggy_code": '''MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "myapp.middleware.RequireRoleMiddleware",  # expects request.user
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]''',
        "solution_code": '''MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # before custom authz
    "myapp.middleware.RequireRoleMiddleware",
]''',
        "solution_explanation": "Middleware runs top-down on request; auth middleware must populate `request.user` first.",
        "ideal_topics": "Django middleware order, authentication, authorization",
        "hints": "Session and AuthenticationMiddleware must precede custom permission middleware.",
        "learning_objectives": "Order Django middleware so dependencies run first",
        "time_estimate_minutes": 17,
    },
    {
        "question": "Fix API rate limiter bypass via uncounted HEAD requests.",
        "buggy_code": '''def rate_limit_middleware(get_response):
    def middleware(request):
        if request.method == "GET":
            if is_over_limit(request.user.id):
                return HttpResponse(status=429)
        return get_response(request)
    return middleware''',
        "solution_code": '''def rate_limit_middleware(get_response):
    def middleware(request):
        if request.method in {"GET", "HEAD", "POST"}:  # count all expensive/read methods
            if is_over_limit(request.user.id):
                return HttpResponse(status=429)
        return get_response(request)
    return middleware''',
        "solution_explanation": "Clients can bypass limits by switching HTTP methods unless all relevant verbs are counted.",
        "ideal_topics": "rate limiting, HTTP methods, API security",
        "hints": "Should HEAD or POST bypass the same quota as GET?",
        "learning_objectives": "Close rate-limit bypass holes across HTTP methods",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Fix Django Q object filter that excludes rows due to incorrect OR grouping.",
        "buggy_code": '''from django.db.models import Q

active_admins = User.objects.filter(
    Q(is_active=True) | Q(is_staff=True),
    is_deleted=False,
)  # AND binds tighter — wrong precedence in complex filters''',
        "solution_code": '''from django.db.models import Q

active_admins = User.objects.filter(
    Q(is_active=True) | Q(is_staff=True),
).filter(is_deleted=False)

# or explicitly group:
active_admins = User.objects.filter(
    (Q(is_active=True) | Q(is_staff=True)) & Q(is_deleted=False)
)''',
        "solution_explanation": "Multiple positional args to filter() are ANDed; OR conditions may need explicit grouping.",
        "ideal_topics": "Django Q objects, query precedence, ORM filters",
        "hints": "Draw the boolean logic before writing Q expressions.",
        "learning_objectives": "Compose Django Q filters with correct boolean grouping",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Fix concurrent dict update in a metrics aggregator losing counts.",
        "buggy_code": '''from concurrent.futures import ThreadPoolExecutor

counts = {}

def record(event):
    counts[event] = counts.get(event, 0) + 1

with ThreadPoolExecutor(max_workers=8) as pool:
    pool.map(record, events)  # lost updates under contention''',
        "solution_code": '''from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import threading

counts = Counter()
lock = threading.Lock()

def record(event):
    with lock:
        counts[event] += 1

with ThreadPoolExecutor(max_workers=8) as pool:
    pool.map(record, events)''',
        "solution_explanation": "In-place dict updates are not atomic across threads; use locks or thread-safe counters.",
        "ideal_topics": "concurrent updates, Counter, ThreadPoolExecutor",
        "hints": "Protect read-modify-write or aggregate per-thread then merge.",
        "learning_objectives": "Aggregate metrics safely under thread concurrency",
        "time_estimate_minutes": 19,
    },
    {
        "question": "Fix WebSocket consumer that processes messages out of order under load.",
        "buggy_code": '''class OrderConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content):
        asyncio.create_task(self.handle_message(content))  # unordered completion''',
        "solution_code": '''class OrderConsumer(AsyncJsonWebsocketConsumer):
    async def receive_json(self, content):
        await self.handle_message(content)  # sequential per connection
        # or use asyncio.Queue + single worker task for ordered processing''',
        "solution_explanation": "Fire-and-forget tasks complete unpredictably; await or queue preserves per-connection order.",
        "ideal_topics": "WebSockets, asyncio, message ordering",
        "hints": "Does each message depend on prior state on the same socket?",
        "learning_objectives": "Preserve message ordering in async WebSocket handlers",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Fix database connection not returned after exception in manual ORM usage.",
        "buggy_code": '''from django.db import connection

def run_raw(sql, params):
    cursor = connection.cursor()
    cursor.execute(sql, params)
    if cursor.rowcount == 0:
        raise LookupError("not found")
    return cursor.fetchone()  # cursor left open on exception paths''',
        "solution_code": '''from django.db import connection

def run_raw(sql, params):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        if cursor.rowcount == 0:
            raise LookupError("not found")
        return cursor.fetchone()''',
        "solution_explanation": "Context-managed cursors close on exceptions, returning connections to the pool.",
        "ideal_topics": "Django database API, cursor context manager, connection pool",
        "hints": "Wrap cursor usage in `with connection.cursor() as cursor`.",
        "learning_objectives": "Ensure DB connections return to pool on errors",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Fix JWT authentication that ignores token expiration.",
        "buggy_code": '''import jwt

def authenticate(header_token):
    payload = jwt.decode(
        header_token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_exp": False},  # exp ignored
    )
    return User.objects.get(pk=payload["sub"])''',
        "solution_code": '''import jwt

def authenticate(header_token):
    payload = jwt.decode(
        header_token,
        settings.SECRET_KEY,
        algorithms=["HS256"],
        options={"verify_exp": True},  # enforce expiration
    )
    return User.objects.get(pk=payload["sub"])''',
        "solution_explanation": "Disabling exp verification allows replay of stolen tokens indefinitely.",
        "ideal_topics": "JWT, expiration, API authentication, security",
        "hints": "Should expired tokens be rejected by default?",
        "learning_objectives": "Enforce JWT exp validation in authentication",
        "time_estimate_minutes": 17,
    },
]
