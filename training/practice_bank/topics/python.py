"""Python practice topic bank."""
PYTHON_TOPICS = [
    {
        "question": "Explain the difference between `is` and `==` in Python.",
        "ideal_topics": "identity, equality, id(), __eq__",
        "solution_code": '''# == compares values; is compares object identity (same memory address)
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)   # True — equal contents
print(a is b)   # False — different list objects
print(a is c)   # True — same reference

# id() reveals memory identity
print(id(a), id(b), id(c))''',
        "solution_explanation": "`==` delegates to __eq__ for value comparison. `is` checks whether two references point to the same object.",
        "hints": "Use id() to inspect object identity. Small integers and strings may be interned.",
        "learning_objectives": "Understand Python object identity vs equality",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Demonstrate mutable vs immutable types and the impact on function arguments.",
        "ideal_topics": "mutability, side effects, defensive copying",
        "solution_code": '''def append_item(lst, item):
    # Mutates the caller's list — default arg pitfall is separate issue
    lst.append(item)
    return lst

numbers = [1, 2]
append_item(numbers, 3)
print(numbers)  # [1, 2, 3] — original mutated

# Immutable: strings cannot change in place
s = "hello"
# s[0] = "H"  # TypeError
s = "H" + s[1:]  # creates new string object''',
        "solution_explanation": "Lists are mutable; mutations through references affect all aliases. Immutable types force new object creation.",
        "hints": "Think about what happens when you pass a list vs a tuple to a function.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Build a custom iterator class for a numeric range with step.",
        "ideal_topics": "iter(), __iter__, __next__, StopIteration",
        "solution_code": '''class StepRange:
    def __init__(self, start, stop, step=1):
        self.current = start
        self.stop = stop
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += self.step
        return value

for n in StepRange(0, 10, 2):
    print(n)  # 0, 2, 4, 6, 8''',
        "solution_explanation": "Iterators implement __iter__ returning self and __next__ raising StopIteration when exhausted.",
        "hints": "Follow the iterator protocol from collections.abc.Iterator.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Write a generator that streams lines from a large file without loading it entirely.",
        "ideal_topics": "yield, lazy evaluation, memory efficiency",
        "solution_code": '''from pathlib import Path

def read_lines(path: str):
  """Yield lines lazily — O(1) memory per line."""
  with Path(path).open(encoding="utf-8") as fh:
      for line in fh:
          yield line.rstrip("\n")

# Consumer processes one line at a time
for line in read_lines("access.log"):
    if "ERROR" in line:
        print(line)''',
        "solution_explanation": "Generators suspend execution at yield, making them ideal for streaming and pipelines.",
        "hints": "Compare with loading readlines() into a list.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Implement a retry decorator with exponential backoff using functools.",
        "ideal_topics": "decorators, closures, functools.wraps, backoff",
        "solution_code": '''import functools
import time

def retry(max_attempts=3, base_delay=0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception:
                    attempt += 1
                    if attempt >= max_attempts:
                        raise
                    time.sleep(base_delay * (2 ** (attempt - 1)))
        return wrapper
    return decorator

@retry(max_attempts=4, base_delay=0.25)
def fetch():
    ...''',
        "solution_explanation": "Decorators wrap functions; functools.wraps preserves metadata. Backoff reduces load on failing dependencies.",
        "hints": "Structure: outer decorator factory → inner wrapper → call original func.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Create a context manager that times a block and logs duration.",
        "ideal_topics": "__enter__, __exit__, contextlib",
        "solution_code": '''import time
from contextlib import contextmanager

class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False  # do not suppress exceptions

@contextmanager
def timer(label="block"):
    start = time.perf_counter()
    try:
        yield
    finally:
        print(f"{label}: {time.perf_counter() - start:.4f}s")''',
        "solution_explanation": "Context managers guarantee setup/teardown. __exit__ receives exception info if an error occurred.",
        "hints": "contextlib.contextmanager is an alternative to a full class.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Demonstrate multiple inheritance and explain MRO with a diamond example.",
        "ideal_topics": "MRO, super(), C3 linearization",
        "solution_code": '''class A:
    def ping(self):
        return "A"

class B(A):
    def ping(self):
        return "B" + super().ping()

class C(A):
    def ping(self):
        return "C" + super().ping()

class D(B, C):
    pass

d = D()
print(d.ping())       # BCA — follows MRO: D → B → C → A
print(D.__mro__)''',
        "solution_explanation": "Python uses C3 linearization for MRO. super() follows MRO, not just the parent class.",
        "hints": "Print __mro__ on your classes to verify ordering.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Use dataclasses with frozen=True and custom __post_init__ validation.",
        "ideal_topics": "dataclasses, immutability, validation",
        "solution_code": '''from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str = "USD"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("amount must be non-negative")
        if len(self.currency) != 3:
            raise ValueError("currency must be ISO code")

usd = Money(10.5)
# usd.amount = 20  # FrozenInstanceError''',
        "solution_explanation": "frozen=True makes instances immutable. __post_init__ runs after field assignment for validation.",
        "hints": "Combine with field(default_factory=...) for mutable defaults.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Implement a descriptor that validates and caches an attribute.",
        "ideal_topics": "descriptors, __get__, __set__, data descriptor",
        "solution_code": '''class PositiveInt:
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name, 0)

    def __set__(self, obj, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("must be non-negative int")
        setattr(obj, self.name, value)

class Account:
    balance = PositiveInt()''',
        "solution_explanation": "Descriptors intercept attribute access. Data descriptors (with __set__) override instance __dict__.",
        "hints": "__set_name__ is called when the class body is executed.",
        "time_estimate_minutes": 20,
    },
    {
        "question": "Write typed functions using Protocol and TypeVar for a generic stack.",
        "ideal_topics": "type hints, Protocol, generics, mypy",
        "solution_code": '''from typing import Generic, List, TypeVar
from typing_extensions import Protocol

T = TypeVar("T")

class Stack(Protocol[T]):
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...

class ListStack(Generic[T]):
    def __init__(self) -> None:
        self._items: List[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()''',
        "solution_explanation": "Protocol defines structural subtyping. Generic[T] preserves element type through operations.",
        "hints": "Compare Protocol vs ABC inheritance for flexibility.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Design a custom exception hierarchy for a REST API client.",
        "ideal_topics": "exceptions, error handling, API errors",
        "solution_code": '''class APIError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        super().__init__(message)
        self.status_code = status_code
        self.payload = payload or {}

class NotFoundError(APIError):
    pass

class RateLimitError(APIError):
    pass

def handle_response(resp):
    if resp.status_code == 404:
        raise NotFoundError("Resource missing", status_code=404, payload=resp.json())
    if resp.status_code == 429:
        raise RateLimitError("Rate limited", status_code=429)''',
        "solution_explanation": "Domain-specific exceptions carry context (status, payload) for clean error boundaries.",
        "hints": "Catch specific exceptions before broad APIError.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Use asyncio to run multiple coroutines concurrently and gather results.",
        "ideal_topics": "asyncio, gather, coroutines, concurrency",
        "solution_code": '''import asyncio

async def fetch(url: str) -> str:
    await asyncio.sleep(0.1)  # simulate I/O
    return f"body:{url}"

async def main():
    urls = ["a", "b", "c"]
    results = await asyncio.gather(*(fetch(u) for u in urls))
    print(results)

asyncio.run(main())''',
        "solution_explanation": "asyncio.gather schedules coroutines concurrently on one thread via the event loop.",
        "hints": "Use return_exceptions=True to avoid one failure cancelling others.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Implement LRU cache using OrderedDict (or dict + ordering).",
        "ideal_topics": "OrderedDict, cache, O(1) operations",
        "solution_code": '''from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.store = OrderedDict()

    def get(self, key):
        if key not in self.store:
            return None
        self.store.move_to_end(key)
        return self.store[key]

    def put(self, key, value):
        if key in self.store:
            self.store.move_to_end(key)
        self.store[key] = value
        if len(self.store) > self.capacity:
            self.store.popitem(last=False)''',
        "solution_explanation": "OrderedDict maintains insertion order; move_to_end marks an entry as recently used.",
        "hints": "popitem(last=False) evicts the oldest (least recently used).",
        "time_estimate_minutes": 25,
    },
    {
        "question": "Parse and validate environment variables with defaults and type coercion.",
        "ideal_topics": "os.environ, configuration, twelve-factor",
        "solution_code": '''import os

def env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.lower() in {"1", "true", "yes", "on"}

def env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    return int(raw) if raw is not None else default

DEBUG = env_bool("DEBUG", False)
DB_PORT = env_int("DB_PORT", 5432)''',
        "solution_explanation": "Centralize env parsing to avoid scattered os.getenv calls and inconsistent coercion.",
        "hints": "Consider pydantic-settings for production apps.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Use structural pattern matching (match/case) for HTTP method routing.",
        "ideal_topics": "match case, Python 3.10+, pattern matching",
        "solution_code": '''def route(method: str, path: str):
    match (method.upper(), path):
        case ("GET", "/health"):
            return 200, "ok"
        case ("GET", "/users"):
            return 200, list_users()
        case ("POST", "/users"):
            return 201, create_user()
        case ("GET", path) if path.startswith("/users/"):
            return 200, get_user(path.split("/")[-1])
        case _:
            return 404, "not found"''',
        "solution_explanation": "match/case supports literals, sequences, guards, and wildcards for expressive branching.",
        "hints": "Guards (if ...) add conditions to patterns.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Implement a simple plugin registry using decorators.",
        "ideal_topics": "registry pattern, decorators, extensibility",
        "solution_code": '''REGISTRY = {}

def register(kind: str):
    def decorator(func):
        REGISTRY[kind] = func
        return func
    return decorator

@register("email")
def send_email(user, message):
    ...

@register("sms")
def send_sms(user, message):
    ...

def dispatch(kind, user, message):
    handler = REGISTRY.get(kind)
    if not handler:
        raise KeyError(f"unknown kind: {kind}")
    return handler(user, message)''',
        "solution_explanation": "Decorator registries enable plugin discovery without central switch statements.",
        "hints": "Import side effects populate REGISTRY at module load.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Profile a hot loop with timeit and identify optimization strategy.",
        "ideal_topics": "timeit, profiling, performance",
        "solution_code": '''import timeit

# Slow: repeated concatenation in loop
slow = "sum(len(str(i)) for i in range(1000))"

# Faster: join prebuilt strings
fast = "len(''.join(str(i) for i in range(1000)))"

print("slow", timeit.timeit(slow, number=1000))
print("fast", timeit.timeit(fast, number=1000))''',
        "solution_explanation": "Measure before optimizing. timeit isolates loop overhead for micro-benchmarks.",
        "hints": "For real apps use cProfile and line_profiler.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Use __slots__ to reduce memory for many small instances.",
        "ideal_topics": "__slots__, memory, instance dict",
        "solution_code": '''class Point:
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

# No per-instance __dict__ — lower memory footprint
p = Point(1, 2)
# p.z = 3  # AttributeError''',
        "solution_explanation": "__slots__ prevents dynamic attributes and avoids per-instance dict overhead.",
        "hints": "Trade flexibility for memory in high-volume object models.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Implement a thread-safe counter with threading.Lock.",
        "ideal_topics": "threading, locks, race conditions",
        "solution_code": '''import threading

class Counter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    @property
    def value(self):
        with self._lock:
            return self._value''',
        "solution_explanation": "Locks protect critical sections. Always use with lock for acquire/release safety.",
        "hints": "For high contention consider atomic operations or multiprocessing patterns.",
        "time_estimate_minutes": 16,
    },
    {
        "question": "Build a memoization decorator for pure functions.",
        "ideal_topics": "memoization, functools.lru_cache, caching",
        "solution_code": '''import functools

@functools.lru_cache(maxsize=128)
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(35))  # fast due to cache
print(fib.cache_info())''',
        "solution_explanation": "lru_cache stores results keyed by arguments. Only use with pure, hashable arguments.",
        "hints": "maxsize=None for unlimited cache; watch memory.",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Serialize datetimes safely for JSON APIs.",
        "ideal_topics": "datetime, JSON, isoformat, timezone",
        "solution_code": '''from datetime import datetime, timezone
import json

def default_serializer(obj):
    if isinstance(obj, datetime):
        if obj.tzinfo is None:
            obj = obj.replace(tzinfo=timezone.utc)
        return obj.isoformat()
    raise TypeError(f"unserializable: {type(obj)}")

payload = {"created": datetime.now(timezone.utc)}
print(json.dumps(payload, default=default_serializer))''',
        "solution_explanation": "JSON has no datetime type; ISO-8601 strings with explicit timezone are the standard.",
        "hints": "Always store UTC in backends; localize at display.",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Use pathlib for robust path operations across platforms.",
        "ideal_topics": "pathlib, file paths, portability",
        "solution_code": '''from pathlib import Path

root = Path("data")
config = root / "config" / "app.toml"
config.parent.mkdir(parents=True, exist_ok=True)

if not config.exists():
    config.write_text("# defaults", encoding="utf-8")

for path in root.rglob("*.log"):
    print(path.resolve())''',
        "solution_explanation": "pathlib abstracts OS path semantics and reads cleaner than os.path.",
        "hints": "Use / operator for joining; resolve() for absolute paths.",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Implement a simple event emitter (observer pattern).",
        "ideal_topics": "observer, callbacks, event-driven",
        "solution_code": '''class EventEmitter:
    def __init__(self):
        self._handlers = {}

    def on(self, event, handler):
        self._handlers.setdefault(event, []).append(handler)

    def emit(self, event, *args, **kwargs):
        for handler in self._handlers.get(event, []):
            handler(*args, **kwargs)

emitter = EventEmitter()
emitter.on("user_created", lambda user: print(f"welcome {user}"))
emitter.emit("user_created", "alice")''',
        "solution_explanation": "Observers decouple event producers from consumers — common in async systems.",
        "hints": "Consider weakref for handlers to avoid memory leaks.",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Write a context-aware logging setup for production services.",
        "ideal_topics": "logging, structured logs, context",
        "solution_code": '''import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if hasattr(record, "request_id"):
            payload["request_id"] = record.request_id
        return json.dumps(payload)

logger = logging.getLogger("app")
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)''',
        "solution_explanation": "Structured JSON logs integrate with ELK/Datadog. Attach request_id via LoggerAdapter or contextvars.",
        "hints": "Use logging.config.dictConfig in production.",
        "time_estimate_minutes": 18,
    },
    {
        "question": "Demonstrate weak references and when to use weakref.WeakValueDictionary.",
        "ideal_topics": "weakref, garbage collection, caches",
        "solution_code": '''import weakref

class User:
    def __init__(self, name):
        self.name = name

cache = weakref.WeakValueDictionary()
u = User("alice")
cache["alice"] = u
print("alice" in cache)  # True
del u
print("alice" in cache)  # False — entry removed when object collected''',
        "solution_explanation": "Weak references don't prevent garbage collection — useful for auxiliary caches.",
        "hints": "WeakKeyDictionary for dict keys that should not pin objects.",
        "time_estimate_minutes": 16,
    },
]
