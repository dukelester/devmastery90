"""Bi-weekly mock interview rounds — structured easy → hardest progression."""

QUESTION_BLUEPRINT = [
    (1, "behavioral", "easy", 5, "Behavioral warm-up"),
    (2, "technical", "easy", 8, "Technical fundamentals"),
    (3, "coding", "easy", 10, "Coding warm-up"),
    (4, "technical", "medium", 12, "Applied technical"),
    (5, "coding", "medium", 15, "Coding problem"),
    (6, "technical", "hard", 18, "Deep technical"),
    (7, "system_design", "expert", 20, "Hardest: system design"),
]

MOCK_ROUNDS = [
    {
        "round_number": 1,
        "title": "Mock 1: Python Foundations",
        "description": "Days 1–14 checkpoint — object model, core syntax, and how you learn.",
        "unlock_day": 1,
        "period_end_day": 14,
        "duration_minutes": 88,
        "focus_areas": "Python basics, mutability, functions, study habits",
        "theme": "python_foundations",
    },
    {
        "round_number": 2,
        "title": "Mock 2: Python Deep Dive",
        "description": "Days 15–28 checkpoint — decorators, typing, packaging, and DSA intro.",
        "unlock_day": 15,
        "period_end_day": 28,
        "duration_minutes": 88,
        "focus_areas": "Decorators, type hints, algorithms introduction",
        "theme": "python_advanced",
    },
    {
        "round_number": 3,
        "title": "Mock 3: Algorithms & DSA",
        "description": "Days 29–42 checkpoint — arrays, trees, graphs, complexity analysis.",
        "unlock_day": 29,
        "period_end_day": 42,
        "duration_minutes": 88,
        "focus_areas": "DSA patterns, Big-O, problem decomposition",
        "theme": "dsa",
    },
    {
        "round_number": 4,
        "title": "Mock 4: Backend & Django",
        "description": "Days 43–56 checkpoint — HTTP, REST, Django ORM, API design.",
        "unlock_day": 43,
        "period_end_day": 56,
        "duration_minutes": 88,
        "focus_areas": "Django, REST, auth, ORM optimization",
        "theme": "backend",
    },
    {
        "round_number": 5,
        "title": "Mock 5: Databases & Distributed",
        "description": "Days 57–70 checkpoint — PostgreSQL, Redis, caching, transactions.",
        "unlock_day": 57,
        "period_end_day": 70,
        "duration_minutes": 88,
        "focus_areas": "SQL tuning, Redis, distributed basics",
        "theme": "data_distributed",
    },
    {
        "round_number": 6,
        "title": "Mock 6: Production Engineering",
        "description": "Days 71–84 checkpoint — testing, DevOps, performance, reliability.",
        "unlock_day": 71,
        "period_end_day": 84,
        "duration_minutes": 88,
        "focus_areas": "Testing, CI/CD, observability, performance",
        "theme": "production",
    },
    {
        "round_number": 7,
        "title": "Mock 7: Final Readiness",
        "description": "Days 85–90 final mock — full-stack senior interview simulation.",
        "unlock_day": 85,
        "period_end_day": 90,
        "duration_minutes": 88,
        "focus_areas": "Full interview loop: coding, system design, behavioral",
        "theme": "final",
    },
]

# Per-theme question templates keyed by blueprint order (1-7)
THEME_QUESTIONS: dict[str, dict[int, dict]] = {
    "python_foundations": {
        1: {
            "question": "Tell me about yourself and why you started this 90-day engineering program.",
            "sample_answer": "Brief career arc, motivation, specific skills targeted, and how you structure daily practice.",
            "rubric": "Clarity, structure, relevance to engineering growth (0–10).",
            "hints": "Use present → past → future structure. Mention concrete goals.",
        },
        2: {
            "question": "Explain the difference between `is` and `==` in Python with an example.",
            "sample_answer": "`==` compares values via __eq__; `is` compares object identity (same id). Lists with equal contents can be `==` but not `is`.",
            "rubric": "Correct definitions, example, mention of id()/interning (0–10).",
            "hints": "Give a list example where == is True but is is False.",
        },
        3: {
            "question": "Write a function `sum_positive(nums)` that returns the sum of positive integers in a list.",
            "sample_answer": "def sum_positive(nums):\n    return sum(x for x in nums if x > 0)",
            "rubric": "Correct logic, handles empty list, clean code (0–10).",
            "hints": "Filter before sum; watch edge cases with zero.",
            "function_name": "sum_positive",
            "starter_code": "def sum_positive(nums):\n    \"\"\"Return the sum of all positive integers in nums.\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {"name": "mixed", "args": [[1, -2, 3, 0, 4]], "expected": 8},
                {"name": "empty", "args": [[]], "expected": 0},
                {"name": "all_negative", "args": [[-1, -5]], "expected": 0, "hidden": True},
                {"name": "zeros", "args": [[0, 0, 5]], "expected": 5, "hidden": True},
            ],
        },
        4: {
            "question": "What are mutable vs immutable types in Python? How does mutability affect function arguments?",
            "sample_answer": "Lists/dicts are mutable; tuples/strings/ints immutable. Passing a list lets the callee mutate caller data unless copied.",
            "rubric": "Examples of each, side-effect story, defensive copy mention (0–10).",
            "hints": "Use a function that appends to a list passed in.",
        },
        5: {
            "question": "Implement `unique_sorted(words)` returning deduplicated words in alphabetical order.",
            "sample_answer": "return sorted(set(words))",
            "rubric": "Correct dedup + sort, discuss set vs sorted uniqueness (0–10).",
            "hints": "set() then sorted(); mention case sensitivity if asked.",
            "function_name": "unique_sorted",
            "starter_code": "def unique_sorted(words):\n    \"\"\"Return unique words sorted alphabetically.\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {"name": "basic", "args": [["banana", "apple", "banana"]], "expected": ["apple", "banana"]},
                {"name": "empty", "args": [[]], "expected": []},
                {"name": "already_unique", "args": [["c", "a", "b"]], "expected": ["a", "b", "c"], "hidden": True},
            ],
        },
        6: {
            "question": "Explain how Python's GIL affects multithreading for CPU-bound vs I/O-bound work.",
            "sample_answer": "GIL allows one thread to execute Python bytecode at a time — limits CPU parallelism; I/O releases GIL so threads help for I/O-bound tasks.",
            "rubric": "GIL definition, CPU vs I/O distinction, multiprocessing alternative (0–10).",
            "hints": "Contrast threads with multiprocessing for CPU work.",
        },
        7: {
            "question": "Design a CLI tool that ingests a CSV of study tasks and prints a daily schedule under a time budget.",
            "sample_answer": "Parse CSV → validate → priority queue by priority/estimate → greedy pack into budget → output schedule + overflow.",
            "rubric": "Components, data model, algorithm, edge cases, extensibility (0–10).",
            "hints": "Start with inputs/outputs, then scheduling heuristic.",
        },
    },
    "python_advanced": {
        1: {
            "question": "Describe a time you struggled with a hard Python concept and how you overcame it.",
            "sample_answer": "STAR format: specific concept (e.g. decorators), actions (docs, small repro, mentor), measurable outcome.",
            "rubric": "STAR structure, specificity, reflection (0–10).",
            "hints": "Name the concept and what evidence showed improvement.",
        },
        2: {
            "question": "How do decorators work in Python? Write a simple `@timing` decorator.",
            "sample_answer": "Decorator replaces function with wrapper; use functools.wraps; wrapper calls fn and records duration.",
            "rubric": "Closure/wrapper explanation, working code, wraps preservation (0–10).",
            "hints": "def timing(fn): def wrapper(*a,**k): ... return wrapper",
        },
        3: {
            "question": "Implement a generator `fibonacci()` that yields Fibonacci numbers indefinitely.",
            "sample_answer": "a,b=0,1; while True: yield a; a,b=b,a+b",
            "rubric": "Generator syntax, infinite sequence, memory efficiency note (0–10).",
            "hints": "Use yield in a loop, not recursion.",
            "function_name": "fibonacci",
            "starter_code": "def fibonacci():\n    \"\"\"Yield Fibonacci numbers forever: 0, 1, 1, 2, 3, …\"\"\"\n    # TODO: implement with yield\n    pass\n",
            "test_cases": [
                {"name": "first_7", "args": [], "take": 7, "expected": [0, 1, 1, 2, 3, 5, 8]},
                {"name": "first_1", "args": [], "take": 1, "expected": [0]},
                {"name": "first_10", "args": [], "take": 10, "expected": [0, 1, 1, 2, 3, 5, 8, 13, 21, 34], "hidden": True},
            ],
        },
        4: {
            "question": "Explain type hints, `Optional`, and when static analysis helps in a Django project.",
            "sample_answer": "Hints annotate intent; mypy/pyright catch bugs before runtime; optional for gradual typing in views/services.",
            "rubric": "Optional/Union, tooling, tradeoffs, Django example (0–10).",
            "hints": "Mention mypy and service layer typing.",
        },
        5: {
            "question": "Write `group_by(items, key)` returning a dict of lists grouped by a string field name on each dict item.",
            "sample_answer": "d={}; for item in items: d.setdefault(item[key], []).append(item); return d",
            "rubric": "Correct grouping, setdefault/defaultdict, key field (0–10).",
            "hints": "Use setdefault or defaultdict(list).",
            "function_name": "group_by",
            "starter_code": "def group_by(items, key):\n    \"\"\"Group dict items by items[i][key]. Return {key_value: [items…]}.\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {
                    "name": "by_type",
                    "args": [
                        [{"type": "a", "n": 1}, {"type": "b", "n": 2}, {"type": "a", "n": 3}],
                        "type",
                    ],
                    "expected": {
                        "a": [{"type": "a", "n": 1}, {"type": "a", "n": 3}],
                        "b": [{"type": "b", "n": 2}],
                    },
                },
                {"name": "empty", "args": [[], "type"], "expected": {}},
                {
                    "name": "single",
                    "args": [[{"k": "x"}], "k"],
                    "expected": {"x": [{"k": "x"}]},
                    "hidden": True,
                },
            ],
        },
        6: {
            "question": "Explain context managers and write a context manager that temporarily changes a config dict.",
            "sample_answer": "class Ctx: __enter__/__exit__ restore previous value; or contextlib.contextmanager yield pattern.",
            "rubric": "Protocol, cleanup on exit, exception safety (0–10).",
            "hints": "__enter__ saves state, __exit__ restores even on error.",
        },
        7: {
            "question": "Design a plugin system where third-party modules register hooks without editing core code.",
            "sample_answer": "Entry points / registry dict / importlib metadata; hook spec; versioned API; discovery at startup.",
            "rubric": "Registration, discovery, isolation, versioning, failure handling (0–10).",
            "hints": "Think setuptools entry points or explicit registry.",
        },
    },
    "dsa": {
        1: {
            "question": "Tell me about your approach when you see a new algorithm problem in an interview.",
            "sample_answer": "Clarify inputs/outputs, examples, edge cases, brute force, optimize, code, test.",
            "rubric": "Structured process, communication, edge cases (0–10).",
            "hints": "Mention clarifying questions before coding.",
        },
        2: {
            "question": "Explain Big-O notation and compare O(n), O(n log n), and O(n²) with real examples.",
            "sample_answer": "n: single pass; n log n: efficient sort; n²: nested loops over same collection.",
            "rubric": "Correct definitions, examples, growth intuition (0–10).",
            "hints": "Give algorithm names for each complexity.",
        },
        3: {
            "question": "Given an integer array, return indices of two numbers that add to target (one solution). Function: `two_sum(nums, target)`.",
            "sample_answer": "Hash map of value→index; for each x check target-x in map; O(n) time.",
            "rubric": "Correct algorithm, hash map, complexity (0–10).",
            "hints": "One-pass hash map beats O(n²) pairs.",
            "function_name": "two_sum",
            "starter_code": "def two_sum(nums, target):\n    \"\"\"Return [i, j] such that nums[i] + nums[j] == target (i != j).\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {"name": "basic", "args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                {"name": "later", "args": [[3, 2, 4], 6], "expected": [1, 2]},
                {"name": "duplicates", "args": [[3, 3], 6], "expected": [0, 1], "hidden": True},
            ],
        },
        4: {
            "question": "When would you use a stack vs a queue vs a heap for a problem?",
            "sample_answer": "Stack: DFS, parsing; Queue: BFS, scheduling FIFO; Heap: top-k, merge k lists, Dijkstra.",
            "rubric": "Correct use cases, complexity notes (0–10).",
            "hints": "Link structure to classic algorithms.",
        },
        5: {
            "question": "Implement `shortest_path(graph, start, end)` — BFS distance in an unweighted adjacency-list graph. Return -1 if unreachable.",
            "sample_answer": "deque queue, visited set; pop, enqueue neighbors distance+1.",
            "rubric": "BFS structure, visited handling, correct distance (0–10).",
            "hints": "Use a queue; track distance as you enqueue.",
            "function_name": "shortest_path",
            "starter_code": "def shortest_path(graph, start, end):\n    \"\"\"graph: dict[node] -> list[neighbors]. Return hop count start→end, or -1.\"\"\"\n    # TODO: implement BFS\n    pass\n",
            "test_cases": [
                {
                    "name": "direct",
                    "args": [{"A": ["B"], "B": ["C"], "C": []}, "A", "C"],
                    "expected": 2,
                },
                {
                    "name": "same_node",
                    "args": [{"A": ["B"], "B": []}, "A", "A"],
                    "expected": 0,
                },
                {
                    "name": "unreachable",
                    "args": [{"A": ["B"], "B": [], "C": []}, "A", "C"],
                    "expected": -1,
                    "hidden": True,
                },
            ],
        },
        6: {
            "question": "Explain dynamic programming with the classic coin change problem (min coins).",
            "sample_answer": "dp[amount]=min(dp[amount-c]+1); iterate coins and amounts; base dp[0]=0.",
            "rubric": "Recurrence, bottom-up, complexity, example walkthrough (0–10).",
            "hints": "Define dp array meaning clearly first.",
        },
        7: {
            "question": "Design a rate-limited leaderboard for 10M users with real-time score updates.",
            "sample_answer": "Redis sorted set for top-N; write path updates score; periodic sync to DB; sharding by game id.",
            "rubric": "Hot path, storage, consistency, scale numbers (0–10).",
            "hints": "Redis ZSET is a common pattern for leaderboards.",
        },
    },
    "backend": {
        1: {
            "question": "Describe a project where you built or consumed a REST API. What went well and what was hard?",
            "sample_answer": "STAR with endpoints, auth, error handling, and a concrete challenge (versioning, pagination).",
            "rubric": "Technical depth, honesty, lessons learned (0–10).",
            "hints": "Mention status codes and error contracts.",
        },
        2: {
            "question": "Explain HTTP methods, idempotency, and safe vs idempotent classification.",
            "sample_answer": "GET safe+idempotent; POST not idempotent; PUT idempotent; DELETE idempotent; PATCH varies.",
            "rubric": "Correct mapping, idempotency definition, examples (0–10).",
            "hints": "Give a duplicate POST vs PUT example.",
        },
        3: {
            "question": "Write `user_orders(orders, user_id, page, page_size)` returning a paginated list of that user's orders (dicts with user_id), newest first by `created` descending.",
            "sample_answer": "Filter by user_id, sort by created desc, slice for page.",
            "rubric": "Auth scoping analog, sort, pagination math (0–10).",
            "hints": "offset = (page-1)*page_size; sort before slice.",
            "function_name": "user_orders",
            "starter_code": "def user_orders(orders, user_id, page, page_size):\n    \"\"\"Return page of orders for user_id, sorted by created descending.\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {
                    "name": "page1",
                    "args": [
                        [
                            {"user_id": 1, "id": 1, "created": 10},
                            {"user_id": 1, "id": 2, "created": 30},
                            {"user_id": 2, "id": 3, "created": 40},
                            {"user_id": 1, "id": 4, "created": 20},
                        ],
                        1,
                        1,
                        2,
                    ],
                    "expected": [
                        {"user_id": 1, "id": 2, "created": 30},
                        {"user_id": 1, "id": 4, "created": 20},
                    ],
                },
                {
                    "name": "empty_user",
                    "args": [[{"user_id": 2, "id": 1, "created": 1}], 1, 1, 10],
                    "expected": [],
                },
                {
                    "name": "page2",
                    "args": [
                        [
                            {"user_id": 1, "id": 1, "created": 10},
                            {"user_id": 1, "id": 2, "created": 30},
                            {"user_id": 1, "id": 4, "created": 20},
                        ],
                        1,
                        2,
                        2,
                    ],
                    "expected": [{"user_id": 1, "id": 1, "created": 10}],
                    "hidden": True,
                },
            ],
        },
        4: {
            "question": "How does Django ORM lazy evaluation work? When does a queryset hit the database?",
            "sample_answer": "Queryset is lazy until evaluated: list(), len(), bool(), iteration, repr in debug.",
            "rubric": "Evaluation triggers, queryset caching, performance implication (0–10).",
            "hints": "Mention that slicing can add LIMIT but still lazy until consumed.",
        },
        5: {
            "question": "Implement `process_payment(store, key, amount)` — idempotent payment: first call with a key processes and stores result; duplicate key returns the stored result without double-charging.",
            "sample_answer": "If key in store return store[key]; else compute, store, return.",
            "rubric": "Idempotency store, no double process, return cached (0–10).",
            "hints": "Check key before side effects; store result before return.",
            "function_name": "process_payment",
            "starter_code": "def process_payment(store, key, amount):\n    \"\"\"store is a dict. Return {'key': key, 'amount': amount, 'status': 'ok'}.\n    Duplicate keys must return the original result unchanged.\n    \"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {
                    "name": "first",
                    "args": [{}, "k1", 50],
                    "expected": {"key": "k1", "amount": 50, "status": "ok"},
                },
                {
                    "name": "idempotent",
                    "args": [{"k1": {"key": "k1", "amount": 50, "status": "ok"}}, "k1", 999],
                    "expected": {"key": "k1", "amount": 50, "status": "ok"},
                },
                {
                    "name": "new_key",
                    "args": [{"k1": {"key": "k1", "amount": 1, "status": "ok"}}, "k2", 7],
                    "expected": {"key": "k2", "amount": 7, "status": "ok"},
                    "hidden": True,
                },
            ],
        },
        6: {
            "question": "Explain JWT vs session auth tradeoffs for a multi-service SaaS API.",
            "sample_answer": "JWT: stateless, harder revoke, size; sessions: server state, easier revoke, sticky sessions or shared store.",
            "rubric": "Tradeoffs, security (revocation, XSS), ops complexity (0–10).",
            "hints": "Mention refresh tokens and short-lived access tokens.",
        },
        7: {
            "question": "Design a multi-tenant SaaS API where each tenant's data must be strictly isolated.",
            "sample_answer": "Tenant ID on every row + middleware sets tenant context; row-level security or schema-per-tenant; audit logs.",
            "rubric": "Isolation strategy, request context, migration, testing (0–10).",
            "hints": "Compare shared schema vs schema-per-tenant.",
        },
    },
    "data_distributed": {
        1: {
            "question": "Tell me about a time you debugged a slow database query or production incident.",
            "sample_answer": "STAR: symptom, measurement (EXPLAIN), fix (index/query rewrite), prevention.",
            "rubric": "Metrics, root cause, fix validation (0–10).",
            "hints": "Include before/after latency if possible.",
        },
        2: {
            "question": "Explain database indexes: B-tree basics and when an index helps or hurts.",
            "sample_answer": "B-tree for range/equality; helps selective queries; hurts write-heavy tables; composite index column order matters.",
            "rubric": "B-tree intuition, selectivity, write cost (0–10).",
            "hints": "Mention covering indexes and left-prefix rule.",
        },
        3: {
            "question": "Write `heavy_users(orders, days, min_count)` — given orders as dicts with user_id and day (int days ago, 0=today), return sorted user_ids with more than min_count orders in the last `days` days.",
            "sample_answer": "Filter day < days, count per user, keep counts > min_count, sort.",
            "rubric": "Correct filter window, group counts, threshold (0–10).",
            "hints": "Analog of GROUP BY / HAVING in Python.",
            "function_name": "heavy_users",
            "starter_code": "def heavy_users(orders, days, min_count):\n    \"\"\"Return sorted list of user_ids with > min_count orders where day < days.\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {
                    "name": "basic",
                    "args": [
                        [
                            {"user_id": 1, "day": 1},
                            {"user_id": 1, "day": 2},
                            {"user_id": 1, "day": 3},
                            {"user_id": 2, "day": 1},
                            {"user_id": 1, "day": 40},
                        ],
                        30,
                        2,
                    ],
                    "expected": [1],
                },
                {"name": "none", "args": [[{"user_id": 1, "day": 1}], 30, 5], "expected": []},
                {
                    "name": "tie",
                    "args": [
                        [
                            {"user_id": 2, "day": 0},
                            {"user_id": 2, "day": 1},
                            {"user_id": 2, "day": 2},
                            {"user_id": 1, "day": 0},
                            {"user_id": 1, "day": 1},
                            {"user_id": 1, "day": 2},
                        ],
                        7,
                        2,
                    ],
                    "expected": [1, 2],
                    "hidden": True,
                },
            ],
        },
        4: {
            "question": "Compare Redis use cases: cache, session store, rate limiter, pub/sub.",
            "sample_answer": "Cache: TTL keys; sessions: hash with expiry; rate limit: INCR+EXPIRE; pub/sub: fan-out not durable queue.",
            "rubric": "Four use cases, data structures, pitfalls (0–10).",
            "hints": "Note pub/sub is fire-and-forget.",
        },
        5: {
            "question": "Implement `allow_request(timestamps, now, limit, window)` — sliding-window rate limit. `timestamps` is a list of prior request times; return (allowed: bool, new_timestamps: list).",
            "sample_answer": "Drop timestamps older than now-window; if len < limit append now and allow.",
            "rubric": "Window trim, limit check, append on allow (0–10).",
            "hints": "Keep only timestamps within [now-window, now].",
            "function_name": "allow_request",
            "starter_code": "def allow_request(timestamps, now, limit, window):\n    \"\"\"Return (allowed, updated_timestamps) for a sliding window limiter.\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {"name": "first", "args": [[], 100, 3, 60], "expected": [True, [100]]},
                {"name": "at_limit", "args": [[90, 95, 99], 100, 3, 60], "expected": [False, [90, 95, 99]]},
                {
                    "name": "expire_old",
                    "args": [[10, 95], 100, 3, 60],
                    "expected": [True, [95, 100]],
                    "hidden": True,
                },
            ],
        },
        6: {
            "question": "Explain ACID vs BASE and when you'd accept eventual consistency.",
            "sample_answer": "ACID for financial core; BASE for high-scale reads, caches, analytics; sagas for cross-service consistency.",
            "rubric": "Definitions, examples, business tradeoff (0–10).",
            "hints": "Name a product feature that can be eventually consistent.",
        },
        7: {
            "question": "Design a globally distributed counter (likes) with high write throughput.",
            "sample_answer": "Sharded counters per region, async aggregation, approximate counts acceptable or CRDT/sync strategy.",
            "rubric": "Write path, aggregation, consistency choice, hot key mitigation (0–10).",
            "hints": "Discuss write sharding and periodic rollups.",
        },
    },
    "production": {
        1: {
            "question": "How do you balance shipping fast with writing tests in a solo learning project?",
            "sample_answer": "Risk-based testing: critical paths integration tests; pytest fixtures; CI on PR; don't skip error paths.",
            "rubric": "Pragmatism, test pyramid, automation (0–10).",
            "hints": "Mention regression tests for bugs you fixed.",
        },
        2: {
            "question": "Explain the test pyramid and what you integration-test vs unit-test in Django.",
            "sample_answer": "Many unit tests for pure logic; integration for ORM/views with test DB; few E2E; factories for data.",
            "rubric": "Pyramid layers, Django test client, fixtures (0–10).",
            "hints": "pytest-django and factory_boy examples.",
        },
        3: {
            "question": "Write `assert_forbidden(status_code)` that returns True only when status_code is 403 (simulating an authz test helper).",
            "sample_answer": "return status_code == 403",
            "rubric": "Correct assertion helper, clarity (0–10).",
            "hints": "Keep it a pure predicate used by tests.",
            "function_name": "assert_forbidden",
            "starter_code": "def assert_forbidden(status_code):\n    \"\"\"Return True iff status_code means forbidden (403).\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {"name": "forbidden", "args": [403], "expected": True},
                {"name": "ok", "args": [200], "expected": False},
                {"name": "unauthorized", "args": [401], "expected": False, "hidden": True},
            ],
        },
        4: {
            "question": "What metrics and logs would you add before launching a new API endpoint?",
            "sample_answer": "RED: rate, errors, duration; structured logs with request_id; tracing; saturation (CPU, DB connections).",
            "rubric": "RED/USE, correlation IDs, alerting thresholds (0–10).",
            "hints": "Mention p95 latency not just average.",
        },
        5: {
            "question": "Implement `pipeline_ok(stages)` — given a list of stage dicts `{name, ok: bool}`, return True only if every stage passed (CI gate).",
            "sample_answer": "return all(s['ok'] for s in stages)",
            "rubric": "Fail-fast semantics, empty pipeline (0–10).",
            "hints": "Empty list of stages should return True (nothing failed).",
            "function_name": "pipeline_ok",
            "starter_code": "def pipeline_ok(stages):\n    \"\"\"Return True if every stage has ok=True.\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {
                    "name": "all_pass",
                    "args": [[{"name": "lint", "ok": True}, {"name": "test", "ok": True}]],
                    "expected": True,
                },
                {
                    "name": "fail",
                    "args": [[{"name": "lint", "ok": True}, {"name": "test", "ok": False}]],
                    "expected": False,
                },
                {"name": "empty", "args": [[]], "expected": True, "hidden": True},
            ],
        },
        6: {
            "question": "Explain how you'd debug memory growth in a long-running Celery worker.",
            "sample_answer": "tracemalloc snapshots, objgraph, worker max tasks per child, inspect task args holding references.",
            "rubric": "Tools, reproduction, mitigation, prevention (0–10).",
            "hints": "CELERYD_MAX_TASKS_PER_CHILD as mitigation.",
        },
        7: {
            "question": "Design zero-downtime deployment for a stateful web app with background workers.",
            "sample_answer": "Blue/green or rolling; backward-compatible migrations; drain queues; feature flags; health checks; rollback plan.",
            "rubric": "Deploy strategy, migrations, workers, rollback (0–10).",
            "hints": "Expand-contract migrations for schema changes.",
        },
    },
    "final": {
        1: {
            "question": "Why should we hire you as a mid-level backend engineer after this 90-day program?",
            "sample_answer": "Evidence: projects, systematic practice metrics, debugging stories, growth mindset with specifics.",
            "rubric": "Evidence-based, humility, alignment with role (0–10).",
            "hints": "Use metrics from your dashboard (streak, assessments).",
        },
        2: {
            "question": "Walk through how you would design and implement user authentication for a new product.",
            "sample_answer": "Requirements, session vs JWT, password hashing, MFA option, threat model, audit.",
            "rubric": "End-to-end flow, security basics, tradeoffs (0–10).",
            "hints": "Cover signup, login, logout, password reset.",
        },
        3: {
            "question": "Code: merge two sorted lists into one sorted list. Function: `merge_sorted(a, b)`.",
            "sample_answer": "Two pointers, append smaller, O(n+m) time.",
            "rubric": "Correct merge, edge cases, complexity (0–10).",
            "hints": "Handle when one list empties first.",
            "function_name": "merge_sorted",
            "starter_code": "def merge_sorted(a, b):\n    \"\"\"Merge two sorted lists into one sorted list.\"\"\"\n    # TODO: implement\n    pass\n",
            "test_cases": [
                {"name": "basic", "args": [[1, 3, 5], [2, 4, 6]], "expected": [1, 2, 3, 4, 5, 6]},
                {"name": "empty_a", "args": [[], [1, 2]], "expected": [1, 2]},
                {"name": "dupes", "args": [[1, 1], [1, 2]], "expected": [1, 1, 1, 2], "hidden": True},
            ],
        },
        4: {
            "question": "Deep dive: explain Django request lifecycle from URL to response.",
            "sample_answer": "URL resolver → middleware chain → view → template/response → middleware unwind.",
            "rubric": "Middleware order, ORM in views, response types (0–10).",
            "hints": "Mention WSGI/ASGI entry separately if asked.",
        },
        5: {
            "question": "Implement LRU cache with O(1) get and put. Class `LRUCache` with `__init__(capacity)`, `get(key)`, `put(key, value)`. For tests, use helper `run_lru(ops)` that applies a list of ops and returns results.",
            "sample_answer": "OrderedDict; move to end on get; pop oldest on overflow.",
            "rubric": "O(1) operations, correct eviction, tests (0–10).",
            "hints": "Use a dict + track order, or OrderedDict.",
            "function_name": "run_lru",
            "starter_code": (
                "class LRUCache:\n"
                "    def __init__(self, capacity):\n"
                "        self.capacity = capacity\n"
                "        # TODO: implement storage\n"
                "\n"
                "    def get(self, key):\n"
                "        # Return value or -1 if missing\n"
                "        pass\n"
                "\n"
                "    def put(self, key, value):\n"
                "        # Insert/update; evict LRU if over capacity\n"
                "        pass\n"
                "\n"
                "def run_lru(capacity, ops):\n"
                "    \"\"\"ops: list of ['get', key] or ['put', key, value]. Return list of get results (-1 if miss).\"\"\"\n"
                "    cache = LRUCache(capacity)\n"
                "    out = []\n"
                "    for op in ops:\n"
                "        if op[0] == 'get':\n"
                "            out.append(cache.get(op[1]))\n"
                "        else:\n"
                "            cache.put(op[1], op[2])\n"
                "    return out\n"
            ),
            "test_cases": [
                {
                    "name": "basic",
                    "args": [
                        2,
                        [["put", 1, 1], ["put", 2, 2], ["get", 1], ["put", 3, 3], ["get", 2], ["get", 3]],
                    ],
                    "expected": [1, -1, 3],
                },
                {
                    "name": "update",
                    "args": [1, [["put", 1, 1], ["put", 1, 2], ["get", 1]]],
                    "expected": [2],
                },
                {
                    "name": "evict",
                    "args": [
                        2,
                        [["put", 1, 10], ["put", 2, 20], ["get", 1], ["put", 3, 30], ["get", 1], ["get", 2]],
                    ],
                    "expected": [10, 10, -1],
                    "hidden": True,
                },
            ],
        },
        6: {
            "question": "Hard: explain distributed transaction options across payment + inventory services.",
            "sample_answer": "2PC limitations; saga orchestration/choreography; outbox; idempotency; compensating transactions.",
            "rubric": "Saga pattern, failure modes, idempotency (0–10).",
            "hints": "Compare orchestration vs choreography.",
        },
        7: {
            "question": "Hardest: design Twitter/X timeline at scale (home feed for 100M users).",
            "sample_answer": "Fan-out on write vs read; hybrid for celebrities; cache hot feeds; ranking layer; regional shards.",
            "rubric": "Fan-out tradeoffs, hot users, storage estimates, failure modes (0–10).",
            "hints": "Start with read vs write ratio assumptions.",
        },
    },
}


def build_mock_rounds() -> list[dict]:
    """Return round metadata dicts for seeding."""
    return [dict(r) for r in MOCK_ROUNDS]


def build_mock_questions_for_round(round_meta: dict) -> list[dict]:
    theme = round_meta["theme"]
    bank = THEME_QUESTIONS[theme]
    questions = []
    for order, qtype, difficulty, minutes, _label in QUESTION_BLUEPRINT:
        tpl = bank[order]
        questions.append(
            {
                "order": order,
                "interview_type": qtype,
                "difficulty": difficulty,
                "time_limit_minutes": minutes,
                "question": tpl["question"],
                "sample_answer": tpl["sample_answer"],
                "rubric": tpl["rubric"],
                "hints": tpl.get("hints", ""),
                "starter_code": tpl.get("starter_code", ""),
                "function_name": tpl.get("function_name", ""),
                "test_cases": tpl.get("test_cases", []),
            }
        )
    return questions
