"""Curriculum data for the 90-day DevMastery program."""
from typing import Any

SKILLS = [
    ("Python", "language"),
    ("Algorithms & Data Structures", "algorithms"),
    ("Backend Engineering", "backend"),
    ("Django", "backend"),
    ("FastAPI", "backend"),
    ("PostgreSQL", "database"),
    ("Redis", "infrastructure"),
    ("System Design", "architecture"),
    ("Distributed Systems", "architecture"),
    ("Testing", "testing"),
    ("Docker", "infrastructure"),
    ("Kubernetes", "infrastructure"),
    ("AWS", "cloud"),
    ("Performance Engineering", "architecture"),
    ("AI Engineering", "ai"),
    ("Software Architecture", "architecture"),
    ("Debugging", "testing"),
    ("Communication", "soft_skills"),
    ("Interview Skills", "soft_skills"),
]

PHASES = [
    {
        "order": 1,
        "name": "Phase 1 — Python + Problem Solving",
        "description": "Advanced Python foundations, deep dive, algorithms, and advanced DSA (Days 1–30).",
    },
    {
        "order": 2,
        "name": "Phase 2 — Production Backend Engineering",
        "description": "HTTP/REST/Django, PostgreSQL, Redis, distributed systems, and system design (Days 31–60).",
    },
    {
        "order": 3,
        "name": "Phase 3 — Elite Engineering + Interview Preparation",
        "description": "Production project, hardening, testing, cloud, performance, and interview war room (Days 61–90).",
    },
]

WEEKS = [
  # Phase 1
  {"week_number": 1, "phase_order": 1, "title": "Advanced Python Foundations", "objectives": "Master Python object model, collections, iterators, generators, decorators, and context managers."},
  {"week_number": 2, "phase_order": 1, "title": "Python Deep Dive", "objectives": "Classes, type hints, exceptions, packaging, logging, and production Python patterns."},
  {"week_number": 3, "phase_order": 1, "title": "Algorithms", "objectives": "Core algorithmic patterns: two pointers, sliding window, binary search, stacks, linked lists, recursion."},
  {"week_number": 4, "phase_order": 1, "title": "Advanced DSA", "objectives": "Trees, heaps, graphs, dynamic programming, greedy algorithms, and month 1 assessment."},
  # Phase 2
  {"week_number": 5, "phase_order": 2, "title": "HTTP + REST + Django", "objectives": "HTTP fundamentals, REST API design, Django architecture, DRF, auth, and production APIs."},
  {"week_number": 6, "phase_order": 2, "title": "PostgreSQL", "objectives": "Schema design, advanced SQL, indexes, query optimization, transactions, and concurrency."},
  {"week_number": 7, "phase_order": 2, "title": "Redis + Distributed Systems", "objectives": "Caching, Celery, message queues, idempotency, and distributed systems fundamentals."},
  {"week_number": 8, "phase_order": 2, "title": "System Design", "objectives": "Scalability, database scaling, CDN, and classic system design problems."},
  # Phase 3
  {"week_number": 9, "phase_order": 3, "title": "Production Project", "objectives": "Build AI Document Processing Platform with multi-tenancy, uploads, Celery, and AI integration."},
  {"week_number": 10, "phase_order": 3, "title": "Production Hardening", "objectives": "Optimization, caching, rate limiting, logging, Docker, and CI/CD."},
  {"week_number": 11, "phase_order": 3, "title": "Testing + Cloud + Performance", "objectives": "pytest mastery, integration testing, AWS, cloud architecture, and performance testing."},
  {"week_number": 12, "phase_order": 3, "title": "Interview / Assessment War Room", "objectives": "Full mock interviews, assessments, debugging challenges, and final review."},
]

# Day definitions: day_number, week_number, title, focus, target_minutes, tasks
# Each task: (title, description, task_type, skill_slug, estimated_minutes, difficulty, priority, order)
DAYS: list[dict[str, Any]] = [
    # Week 1
    {
        "day_number": 1, "week_number": 1,
        "title": "Python Object Model", "focus": "Advanced Python Foundations",
        "target_minutes": 210,
        "tasks": [
            ("Study: Python object model", "Deep dive into Python's object model: types, instances, and identity.", "study", "python", 45, "medium", "high", 1),
            ("Study: is vs == and mutability", "Understand object identity, equality, mutable vs immutable objects, and memory behavior.", "study", "python", 30, "medium", "high", 2),
            ("Coding: 3 Python problems", "Solve 3 problems on object identity, mutability, and reference behavior.", "coding", "python", 60, "medium", "high", 3),
            ("Reading: Memory behavior notes", "Document how Python handles object allocation, interning, and copy vs reference.", "reading", "python", 30, "easy", "medium", 4),
            ("Review: Day 1 concepts", "Summarize key takeaways and note areas needing reinforcement.", "review", "python", 15, "easy", "medium", 5),
        ],
    },
    {
        "day_number": 2, "week_number": 1,
        "title": "Collections & Hashing", "focus": "Advanced Python Foundations",
        "target_minutes": 240,
        "tasks": [
            ("Study: Lists, tuples, sets, dicts", "Compare Python collection types, their internals, and use cases.", "study", "python", 45, "medium", "high", 1),
            ("Study: Hashing and Big-O", "Understand hash tables, collision handling, and complexity of collection operations.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
            ("Coding: 4 hash-map problems", "Solve 4 problems using hash maps for frequency counting and lookups.", "coding", "algorithms-data-structures", 75, "medium", "high", 3),
            ("Coding: Benchmark lookup operations", "Benchmark list vs set vs dict lookup performance with timing benchmarks.", "coding", "python", 45, "medium", "medium", 4),
            ("Review: Collection patterns", "Document patterns where each collection type is the optimal choice.", "review", "python", 15, "easy", "medium", 5),
        ],
    },
    {
        "day_number": 3, "week_number": 1,
        "title": "Iterators & Iterables", "focus": "Advanced Python Foundations",
        "target_minutes": 210,
        "tasks": [
            ("Study: Iterables and iterators", "Understand the iterator protocol: __iter__, __next__, and StopIteration.", "study", "python", 45, "medium", "high", 1),
            ("Study: iter() and next()", "Practice using built-in iterator functions and custom iteration patterns.", "study", "python", 30, "medium", "high", 2),
            ("Project: Build custom iterator", "Implement a custom iterator class with state management.", "project", "python", 60, "hard", "high", 3),
            ("Coding: 3 iterator problems", "Solve 3 problems requiring custom iteration logic.", "coding", "python", 60, "medium", "high", 4),
            ("Review: Iterator patterns", "Summarize when to use iterators vs generators vs loops.", "review", "python", 15, "easy", "medium", 5),
        ],
    },
    {
        "day_number": 4, "week_number": 1,
        "title": "Generators & Streaming", "focus": "Advanced Python Foundations",
        "target_minutes": 210,
        "tasks": [
            ("Study: Generators and yield", "Master generator functions, yield expressions, and lazy evaluation.", "study", "python", 45, "medium", "high", 1),
            ("Study: Generator expressions", "Compare generator expressions with list comprehensions and memory implications.", "study", "python", 30, "medium", "high", 2),
            ("Project: Large-file streaming processor", "Build a streaming processor that handles multi-GB files without loading into memory.", "project", "python", 75, "hard", "critical", 3),
            ("Coding: Generator pipeline problems", "Solve 2 problems using generator pipelines for data transformation.", "coding", "python", 45, "medium", "high", 4),
            ("Review: Streaming patterns", "Document streaming patterns for production data processing.", "review", "python", 15, "easy", "medium", 5),
        ],
    },
    {
        "day_number": 5, "week_number": 1,
        "title": "Decorators & Closures", "focus": "Advanced Python Foundations",
        "target_minutes": 240,
        "tasks": [
            ("Study: Decorators and closures", "Understand closures, decorator syntax, and functools utilities.", "study", "python", 45, "medium", "high", 1),
            ("Project: Build logging decorator", "Create a reusable logging decorator with configurable log levels.", "project", "python", 45, "medium", "high", 2),
            ("Project: Build retry decorator", "Implement a retry decorator with exponential backoff and max attempts.", "project", "python", 45, "hard", "high", 3),
            ("Coding: 3 decorator problems", "Solve 3 problems requiring custom decorator implementations.", "coding", "python", 60, "hard", "high", 4),
            ("Review: Decorator patterns", "Document common decorator patterns used in production Python.", "review", "python", 15, "easy", "medium", 5),
        ],
    },
    {
        "day_number": 6, "week_number": 1,
        "title": "Context Managers", "focus": "Advanced Python Foundations",
        "target_minutes": 180,
        "tasks": [
            ("Study: Context managers", "Master the with statement, __enter__, __exit__, and contextlib utilities.", "study", "python", 45, "medium", "high", 1),
            ("Project: Custom context manager", "Build a context manager for resource management (DB connection, file lock).", "project", "python", 60, "hard", "high", 2),
            ("Coding: Context manager exercises", "Implement 2 context managers for common production scenarios.", "coding", "python", 45, "medium", "high", 3),
            ("Review: Week 1 concepts", "Comprehensive review of all Week 1 Python foundations topics.", "review", "python", 30, "medium", "high", 4),
        ],
    },
    {
        "day_number": 7, "week_number": 1,
        "title": "Week 1 Assessment", "focus": "Advanced Python Foundations",
        "target_minutes": 180,
        "tasks": [
            ("Assessment: 10 Python problems", "60-minute timed test with 10 Python problems covering Week 1 topics.", "assessment", "python", 60, "hard", "critical", 1),
            ("Review: Mistake analysis", "Analyze every mistake from the assessment and categorize by root cause.", "review", "python", 45, "medium", "high", 2),
            ("Interview: Python fundamentals", "Practice explaining object model, decorators, and generators verbally.", "interview", "interview-skills", 30, "medium", "high", 3),
            ("Review: Weekly review", "Complete weekly review form: wins, challenges, lessons, next week focus.", "review", "python", 15, "easy", "medium", 4),
        ],
    },
    # Week 2
    {
        "day_number": 8, "week_number": 2,
        "title": "Classes & Inheritance", "focus": "Python Deep Dive",
        "target_minutes": 210,
        "tasks": [
            ("Study: Classes and inheritance", "Deep dive into class creation, inheritance chains, and polymorphism.", "study", "python", 45, "medium", "high", 1),
            ("Study: MRO and super()", "Understand Method Resolution Order, super() behavior, and diamond problem.", "study", "python", 30, "hard", "high", 2),
            ("Study: Multiple inheritance", "Learn mixin patterns, composition vs inheritance, and ABC usage.", "study", "python", 30, "medium", "high", 3),
            ("Coding: Class design problems", "Solve 3 problems requiring careful class hierarchy design.", "coding", "python", 60, "hard", "high", 4),
            ("Review: OOP patterns", "Document OOP patterns: strategy, factory, mixin, and composition.", "review", "python", 15, "easy", "medium", 5),
        ],
    },
    {
        "day_number": 9, "week_number": 2,
        "title": "Dataclasses & Descriptors", "focus": "Python Deep Dive",
        "target_minutes": 210,
        "tasks": [
            ("Study: Dataclasses and properties", "Master dataclasses, @property, and computed attributes.", "study", "python", 45, "medium", "high", 1),
            ("Study: Descriptors and ABCs", "Understand descriptor protocol, abstract base classes, and Protocol typing.", "study", "python", 45, "hard", "high", 2),
            ("Coding: Descriptor implementation", "Build custom descriptors for validated attributes and lazy loading.", "coding", "python", 60, "hard", "high", 3),
            ("Review: Advanced class patterns", "Summarize dataclass vs namedtuple vs attrs trade-offs.", "review", "python", 15, "easy", "medium", 4),
        ],
    },
    {
        "day_number": 10, "week_number": 2,
        "title": "Type Hints & Static Analysis", "focus": "Python Deep Dive",
        "target_minutes": 210,
        "tasks": [
            ("Study: Type hints and generics", "Master typing module: Optional, Union, Generic, TypeVar, and overloads.", "study", "python", 45, "medium", "high", 1),
            ("Study: TypedDict and Protocol", "Use TypedDict for structured dicts and Protocol for structural subtyping.", "study", "python", 30, "medium", "high", 2),
            ("Project: Add type hints to codebase", "Add comprehensive type hints to a sample project and run mypy.", "project", "python", 60, "medium", "high", 3),
            ("Coding: Type-safe API design", "Design a type-safe API layer with proper generic types.", "coding", "python", 45, "hard", "high", 4),
            ("Review: Type hint patterns", "Document type hint patterns for production Python projects.", "review", "python", 15, "easy", "medium", 5),
        ],
    },
    {
        "day_number": 11, "week_number": 2,
        "title": "Exception Handling", "focus": "Python Deep Dive",
        "target_minutes": 210,
        "tasks": [
            ("Study: Exception hierarchy", "Map Python's exception hierarchy and when to catch specific vs base exceptions.", "study", "python", 30, "medium", "high", 1),
            ("Study: Custom exceptions", "Design custom exception hierarchies for domain-specific errors.", "study", "python", 30, "medium", "high", 2),
            ("Study: Error-handling strategies", "Learn fail-fast, retry, circuit breaker, and graceful degradation patterns.", "study", "backend-engineering", 30, "medium", "high", 3),
            ("Project: Robust API errors", "Build an API error handling layer with structured error responses.", "project", "backend-engineering", 60, "hard", "critical", 4),
            ("Review: Error handling patterns", "Document error handling patterns for production APIs.", "review", "backend-engineering", 15, "easy", "medium", 5),
        ],
    },
    {
        "day_number": 12, "week_number": 2,
        "title": "Python Packaging", "focus": "Python Deep Dive",
        "target_minutes": 210,
        "tasks": [
            ("Study: Python packaging", "Master pyproject.toml, setuptools, and modern Python packaging.", "study", "python", 45, "medium", "high", 1),
            ("Study: Virtual environments", "Understand venv, pip, dependency resolution, and lock files.", "study", "python", 30, "medium", "high", 2),
            ("Project: Build reusable package", "Create a publishable Python package with tests, docs, and CI.", "project", "python", 90, "hard", "critical", 3),
            ("Review: Packaging checklist", "Create a packaging checklist for production Python libraries.", "review", "python", 15, "easy", "medium", 4),
        ],
    },
    {
        "day_number": 13, "week_number": 2,
        "title": "Logging & Configuration", "focus": "Python Deep Dive",
        "target_minutes": 210,
        "tasks": [
            ("Study: Logging fundamentals", "Master Python logging: handlers, formatters, filters, and log levels.", "study", "python", 45, "medium", "high", 1),
            ("Study: Structured logging", "Implement structured logging with JSON output for production observability.", "study", "python", 30, "medium", "high", 2),
            ("Study: Configuration management", "Environment variables, settings modules, and secrets management.", "study", "backend-engineering", 30, "medium", "high", 3),
            ("Project: Production logging setup", "Configure logging for a Django app with rotation, structured output, and correlation IDs.", "project", "python", 60, "hard", "high", 4),
            ("Review: Week 2 concepts", "Comprehensive review of Python deep dive topics.", "review", "python", 15, "easy", "medium", 5),
        ],
    },
    {
        "day_number": 14, "week_number": 2,
        "title": "Week 2 Assessment", "focus": "Python Deep Dive",
        "target_minutes": 240,
        "tasks": [
            ("Assessment: 90-minute Python test", "Comprehensive Python assessment covering all Week 2 topics.", "assessment", "python", 90, "hard", "critical", 1),
            ("Review: Mistake analysis", "Categorize and analyze all assessment mistakes.", "review", "python", 45, "medium", "high", 2),
            ("Interview: Python deep dive", "Practice explaining type hints, packaging, and error handling in interviews.", "interview", "interview-skills", 30, "medium", "high", 3),
            ("Review: Weekly review", "Complete weekly review with focus areas for algorithms week.", "review", "python", 15, "easy", "medium", 4),
        ],
    },
]

from training.curriculum_remaining import REMAINING_DAYS, build_week_5_12_days

DAYS.extend(REMAINING_DAYS)
DAYS.extend(build_week_5_12_days())
