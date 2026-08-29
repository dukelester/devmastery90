"""Debugging practice — Medium level (stdlib and patterns)."""

TOPICS = [
    {
        "question": "Fix itertools.chain usage so nested lists flatten correctly.",
        "buggy_code": '''from itertools import chain

groups = [[1, 2], [3], [4, 5]]
flat = list(chain(groups))
print(flat)  # expected [1, 2, 3, 4, 5]''',
        "solution_code": '''from itertools import chain

groups = [[1, 2], [3], [4, 5]]
flat = list(chain.from_iterable(groups))  # unpack iterables of iterables
print(flat)  # [1, 2, 3, 4, 5]''',
        "solution_explanation": "`chain(iterable)` iterates the outer iterable; nested lists require `from_iterable`.",
        "ideal_topics": "itertools.chain, flattening, iterables",
        "hints": "Does `chain(groups)` iterate inner lists or the list objects themselves?",
        "learning_objectives": "Flatten nested iterables with chain.from_iterable",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix the dataclass so each instance gets its own tags list.",
        "buggy_code": '''from dataclasses import dataclass

@dataclass
class Task:
    title: str
    tags: list = []

t1 = Task("deploy")
t2 = Task("review")
t1.tags.append("prod")
print(t2.tags)  # unexpectedly ['prod']''',
        "solution_code": '''from dataclasses import dataclass, field

@dataclass
class Task:
    title: str
    tags: list = field(default_factory=list)  # new list per instance

t1 = Task("deploy")
t2 = Task("review")
t1.tags.append("prod")
print(t2.tags)  # []''',
        "solution_explanation": "Mutable class attributes are shared; use `field(default_factory=...)` for per-instance defaults.",
        "ideal_topics": "dataclasses, default_factory, mutable defaults",
        "hints": "Same pitfall as mutable function defaults — defaults are shared at class level.",
        "learning_objectives": "Configure dataclass fields with default_factory for mutable values",
        "time_estimate_minutes": 13,
    },
    {
        "question": "Fix database connection handling using a context manager pattern.",
        "buggy_code": '''class Connection:
    def connect(self):
        print("open")
    def close(self):
        print("close")

def query():
    conn = Connection()
    conn.connect()
    # ... run query ...
    return rows  # close never called on success path''',
        "solution_code": '''class Connection:
    def connect(self):
        print("open")
    def close(self):
        print("close")
    def __enter__(self):
        self.connect()
        return self
    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False

def query():
    with Connection() as conn:
        # ... run query ...
        return rows  # close always runs''',
        "solution_explanation": "Context managers guarantee cleanup in `__exit__`, even when exceptions occur.",
        "ideal_topics": "context managers, __enter__, __exit__, resource cleanup",
        "hints": "Implement the context manager protocol or use contextlib.contextmanager.",
        "learning_objectives": "Ensure resources close reliably with context managers",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Fix lru_cache usage that crashes on unhashable list arguments.",
        "buggy_code": '''from functools import lru_cache

@lru_cache(maxsize=128)
def score_pair(values):
    return sum(values)

print(score_pair([1, 2, 3]))  # TypeError: unhashable type: 'list' ''',
        "solution_code": '''from functools import lru_cache

@lru_cache(maxsize=128)
def score_pair(values):
    return sum(values)

print(score_pair((1, 2, 3)))  # pass hashable tuple instead of list''',
        "solution_explanation": "LRU cache keys must be hashable; convert mutable arguments to tuples before caching.",
        "ideal_topics": "functools.lru_cache, hashability, memoization",
        "hints": "Cache keys are built from function arguments — can lists be hashed?",
        "learning_objectives": "Make cached function arguments hashable for lru_cache",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix logging configuration so ERROR messages appear in output.",
        "buggy_code": '''import logging

logging.basicConfig(level=logging.WARNING)
log = logging.getLogger(__name__)

log.info("starting worker")
log.error("worker crashed")  # should appear but INFO won't''',
        "solution_code": '''import logging

logging.basicConfig(level=logging.INFO)  # INFO and above visible
log = logging.getLogger(__name__)

log.info("starting worker")
log.error("worker crashed")''',
        "solution_explanation": "Loggers filter by level; ERROR passes at WARNING but INFO does not.",
        "ideal_topics": "logging levels, basicConfig, observability",
        "hints": "Which level is lower: INFO or WARNING?",
        "learning_objectives": "Configure logging levels to capture intended messages",
        "time_estimate_minutes": 11,
    },
    {
        "question": "Fix defaultdict usage that never creates missing nested keys.",
        "buggy_code": '''from collections import defaultdict

tree = defaultdict(list)
tree["users"]["ada"] = 1  # KeyError: 'users' value is list, not dict''',
        "solution_code": '''from collections import defaultdict

def nested_dict():
    return defaultdict(nested_dict)

tree = nested_dict()
tree["users"]["ada"] = 1  # auto-creates nested defaultdict nodes''',
        "solution_explanation": "A `defaultdict(list)` creates lists for missing keys, not nested dicts.",
        "ideal_topics": "collections.defaultdict, nested structures, KeyError",
        "hints": "The factory must return the same type of container you intend to nest.",
        "learning_objectives": "Model nested mappings with recursive defaultdict factories",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Fix pathlib path concatenation that drops a directory segment.",
        "buggy_code": '''from pathlib import Path

root = Path("/data")
subdir = Path("exports")
path = root / subdir.name  # uses only last segment "exports"
print(path)  # expected /data/exports''',
        "solution_code": '''from pathlib import Path

root = Path("/data")
subdir = Path("exports")
path = root / subdir  # join full relative path object
print(path)  # /data/exports''',
        "solution_explanation": "`.name` returns the final component only; join whole Path objects to preserve segments.",
        "ideal_topics": "pathlib, Path joining, .name vs full path",
        "hints": "Does `subdir.name` include parent directories?",
        "learning_objectives": "Join paths with pathlib without losing segments",
        "time_estimate_minutes": 11,
    },
    {
        "question": "Fix asyncio task scheduling so coroutines actually run.",
        "buggy_code": '''import asyncio

async def fetch(url):
    await asyncio.sleep(0.1)
    return url

async def main():
    asyncio.create_task(fetch("https://api.example.com"))  # task discarded
    print("done")

asyncio.run(main())  # fetch never completes before exit''',
        "solution_code": '''import asyncio

async def fetch(url):
    await asyncio.sleep(0.1)
    return url

async def main():
    task = asyncio.create_task(fetch("https://api.example.com"))
    result = await task  # await task completion
    print(result)

asyncio.run(main())''',
        "solution_explanation": "Created tasks must be awaited or gathered; otherwise the loop may exit before they finish.",
        "ideal_topics": "asyncio, create_task, await, event loop",
        "hints": "What happens to a task that is never awaited?",
        "learning_objectives": "Ensure asyncio tasks are awaited before loop shutdown",
        "time_estimate_minutes": 14,
    },
    {
        "question": "Fix a simple threading race that loses counter increments.",
        "buggy_code": '''import threading

counter = 0

def worker():
    global counter
    for _ in range(100000):
        counter += 1  # not atomic

threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)  # expected 400000, often lower''',
        "solution_code": '''import threading

counter = 0
lock = threading.Lock()

def worker():
    global counter
    for _ in range(100000):
        with lock:
            counter += 1  # protect read-modify-write

threads = [threading.Thread(target=worker) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(counter)  # 400000''',
        "solution_explanation": "Read-modify-write on shared state without synchronization causes lost updates.",
        "ideal_topics": "threading, race conditions, Lock",
        "hints": "Is `counter += 1` atomic in Python?",
        "learning_objectives": "Protect shared mutable state with threading locks",
        "time_estimate_minutes": 15,
    },
    {
        "question": "Fix Enum comparison that fails because raw strings are compared to members.",
        "buggy_code": '''from enum import Enum

class Status(Enum):
    OPEN = "open"
    CLOSED = "closed"

def is_open(value):
    return value == Status.OPEN  # False when value is "open"

print(is_open("open"))''',
        "solution_code": '''from enum import Enum

class Status(Enum):
    OPEN = "open"
    CLOSED = "closed"

def is_open(value):
    if isinstance(value, Status):
        return value == Status.OPEN
    return value == Status.OPEN.value  # compare string to member value

print(is_open("open"))  # True''',
        "solution_explanation": "Enum members are not equal to their `.value` strings unless you compare explicitly.",
        "ideal_topics": "enum.Enum, value vs member, type checks",
        "hints": "Compare against `.value` or coerce input to the Enum type.",
        "learning_objectives": "Compare Enum members correctly against external string input",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix Optional handling so None inputs do not crash uppercasing.",
        "buggy_code": '''from typing import Optional

def normalize_name(name: Optional[str]) -> str:
    return name.strip().upper()  # AttributeError if name is None

print(normalize_name(None))''',
        "solution_code": '''from typing import Optional

def normalize_name(name: Optional[str]) -> str:
    if name is None:
        return ""
    return name.strip().upper()

print(normalize_name(None))  # ""''',
        "solution_explanation": "Type hints do not enforce runtime checks; guard Optional values before method calls.",
        "ideal_topics": "Optional, None guards, typing vs runtime",
        "hints": "What happens when you call `.strip()` on None?",
        "learning_objectives": "Handle Optional parameters defensively at runtime",
        "time_estimate_minutes": 11,
    },
    {
        "question": "Fix JSON serialization of datetime objects in an API payload.",
        "buggy_code": '''import json
from datetime import datetime

payload = {"created_at": datetime(2026, 1, 15, 12, 0)}
body = json.dumps(payload)  # TypeError: datetime not JSON serializable''',
        "solution_code": '''import json
from datetime import datetime

payload = {"created_at": datetime(2026, 1, 15, 12, 0)}
body = json.dumps(payload, default=str)  # coerce non-serializable types
# better: payload["created_at"] = payload["created_at"].isoformat()''',
        "solution_explanation": "Standard JSON encoders do not know datetime; convert to ISO strings or provide a default handler.",
        "ideal_topics": "json.dumps, datetime serialization, TypeError",
        "hints": "Use `.isoformat()` or a custom `default` callback.",
        "learning_objectives": "Serialize datetime values for JSON APIs",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix subprocess invocation that breaks on filenames with spaces.",
        "buggy_code": '''import subprocess

subprocess.run("convert input file.pdf output file.pdf", shell=True, check=True)''',
        "solution_code": '''import subprocess

subprocess.run(
    ["convert", "input file.pdf", "output file.pdf"],  # argv list, no shell
    check=True,
)''',
        "solution_explanation": "Shell=True parses a single string and splits poorly on spaces; pass argv list without shell when possible.",
        "ideal_topics": "subprocess, shell=True, command injection, argv",
        "hints": "Pass arguments as a list and disable the shell unless you need shell features.",
        "learning_objectives": "Invoke subprocess safely with argument lists",
        "time_estimate_minutes": 13,
    },
    {
        "question": "Fix tempfile usage that leaves orphaned files on disk.",
        "buggy_code": '''import tempfile

def write_report(data: bytes) -> str:
    path = tempfile.mktemp(suffix=".bin")  # deprecated, race-prone
    with open(path, "wb") as fh:
        fh.write(data)
    return path  # caller may forget cleanup''',
        "solution_code": '''import tempfile

def write_report(data: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix=".bin", delete=False) as fh:
        fh.write(data)
        return fh.name  # document that caller must unlink when done''',
        "solution_explanation": "`mktemp()` is unsafe and deprecated; use NamedTemporaryFile or TemporaryDirectory.",
        "ideal_topics": "tempfile, resource cleanup, mktemp deprecation",
        "hints": "Prefer context-managed temporary files over predictable paths.",
        "learning_objectives": "Create temporary files safely with tempfile APIs",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix csv.DictReader field access when headers include stray spaces.",
        "buggy_code": '''import csv
from io import StringIO

raw = "name, email\\nAda,ada@example.com\\n"
reader = csv.DictReader(StringIO(raw))
row = next(reader)
print(row["email"])  # KeyError''',
        "solution_code": '''import csv
from io import StringIO

raw = "name, email\\nAda,ada@example.com\\n"
reader = csv.DictReader(StringIO(raw))
row = next(reader)
email = row.get("email") or row.get(" email")  # handle spaced header
# better: strip fieldnames after read
reader.fieldnames = [h.strip() for h in reader.fieldnames]
row = next(csv.DictReader(StringIO(raw)))
print(row["email"])''',
        "solution_explanation": "DictReader keys match header text exactly, including whitespace.",
        "ideal_topics": "csv module, DictReader, data cleaning",
        "hints": "Print `reader.fieldnames` to inspect actual keys.",
        "learning_objectives": "Normalize CSV headers before keyed access",
        "time_estimate_minutes": 13,
    },
    {
        "question": "Fix hashlib usage that produces wrong digests for Unicode text.",
        "buggy_code": '''import hashlib

def digest(text: str) -> str:
    return hashlib.sha256(text).hexdigest()  # TypeError''',
        "solution_code": '''import hashlib

def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()  # hash bytes''',
        "solution_explanation": "Hash functions operate on bytes; encode text explicitly with a documented encoding.",
        "ideal_topics": "hashlib, encoding, bytes vs str",
        "hints": "Does sha256 accept str or bytes?",
        "learning_objectives": "Encode strings before passing to hashlib",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Fix URL encoding that breaks query parameters containing spaces.",
        "buggy_code": '''from urllib.parse import urlencode

params = {"q": "hello world", "page": 1}
url = "https://example.com/search?" + urlencode(params)
# manually replaced space with + earlier causing double-encoding bugs
url = url.replace(" ", "+")''',
        "solution_code": '''from urllib.parse import urlencode

params = {"q": "hello world", "page": 1}
url = "https://example.com/search?" + urlencode(params)  # urlencode handles encoding
print(url)''',
        "solution_explanation": "`urlencode` percent-encodes values correctly; manual string tweaks corrupt the query string.",
        "ideal_topics": "urllib.parse, urlencode, query strings",
        "hints": "Let the standard library encode parameters instead of manual replace.",
        "learning_objectives": "Build query strings with urllib.parse.urlencode",
        "time_estimate_minutes": 11,
    },
    {
        "question": "Fix property setter that allows invalid negative prices.",
        "buggy_code": '''class Product:
    def __init__(self, price):
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value  # no validation

p = Product(-5)
print(p.price)''',
        "solution_code": '''class Product:
    def __init__(self, price):
        self.price = price

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("price must be non-negative")
        self._price = value''',
        "solution_explanation": "Setters should enforce invariants; assigning directly to `_price` bypasses validation.",
        "ideal_topics": "property decorator, validation, descriptors",
        "hints": "Where should business rules live when using @property?",
        "learning_objectives": "Validate state in property setters",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix functools.reduce initial value omission that fails on empty iterables.",
        "buggy_code": '''from functools import reduce

def multiply(a, b):
    return a * b

values = []
total = reduce(multiply, values)  # TypeError on empty sequence''',
        "solution_code": '''from functools import reduce

def multiply(a, b):
    return a * b

values = []
total = reduce(multiply, values, 1)  # identity element for multiplication
print(total)  # 1''',
        "solution_explanation": "Without an initializer, reduce on an empty iterable raises TypeError.",
        "ideal_topics": "functools.reduce, identity element, empty iterables",
        "hints": "Supply the neutral element for your operation (0 for +, 1 for *).",
        "learning_objectives": "Provide initial values to reduce for empty-input safety",
        "time_estimate_minutes": 11,
    },
    {
        "question": "Fix weakref callback that keeps objects alive unintentionally.",
        "buggy_code": '''import weakref

class Cache:
    def __init__(self):
        self._items = []

    def remember(self, obj):
        self._items.append(obj)  # strong reference prevents GC
        weakref.finalize(obj, lambda: print("collected", obj.id))

c = Cache()
o = type("Obj", (), {"id": 1})()
c.remember(o)
del o  # never collected''',
        "solution_code": '''import weakref

class Cache:
    def __init__(self):
        self._items = []

    def remember(self, obj):
        self._items.append(weakref.ref(obj))  # store weak reference
        weakref.finalize(obj, lambda oid=obj.id: print("collected", oid))

c = Cache()
o = type("Obj", (), {"id": 1})()
c.remember(o)
del o  # eligible for collection''',
        "solution_explanation": "Strong references in caches prevent garbage collection; use weakref.ref or WeakValueDictionary.",
        "ideal_topics": "weakref, garbage collection, memory leaks",
        "hints": "Does the cache need to own the object strongly?",
        "learning_objectives": "Avoid strong-reference caches when weak references suffice",
        "time_estimate_minutes": 15,
    },
]
