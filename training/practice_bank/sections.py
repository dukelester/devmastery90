"""Practice section definitions."""
from typing import TypedDict


class SectionDef(TypedDict):
    slug: str
    name: str
    description: str
    icon: str


PRACTICE_SECTIONS: list[SectionDef] = [
    {
        "slug": "python",
        "name": "Python",
        "description": "Object model, internals, async, production patterns",
        "icon": "code",
    },
    {
        "slug": "django",
        "name": "Django",
        "description": "ORM, views, middleware, production Django",
        "icon": "code",
    },
    {
        "slug": "rest",
        "name": "REST APIs",
        "description": "HTTP, resources, versioning, API design",
        "icon": "code",
    },
    {
        "slug": "postgresql",
        "name": "PostgreSQL",
        "description": "SQL, indexes, transactions, optimization",
        "icon": "code",
    },
    {
        "slug": "system-design",
        "name": "System Design",
        "description": "Scalability, distributed systems, architecture",
        "icon": "target",
    },
    {
        "slug": "dsa",
        "name": "DSA",
        "description": "Algorithms, data structures, complexity",
        "icon": "code",
    },
    {
        "slug": "testing",
        "name": "Testing",
        "description": "pytest, fixtures, mocking, integration tests",
        "icon": "check",
    },
    {
        "slug": "devops",
        "name": "DevOps",
        "description": "CI/CD, Docker, deployment, monitoring",
        "icon": "zap",
    },
    {
        "slug": "cloud",
        "name": "Cloud",
        "description": "AWS, scaling, storage, networking",
        "icon": "zap",
    },
    {
        "slug": "ai",
        "name": "AI Engineering",
        "description": "LLM APIs, RAG, embeddings, production AI",
        "icon": "zap",
    },
    {
        "slug": "behavioral",
        "name": "Behavioral",
        "description": "STAR stories, leadership, communication",
        "icon": "mic",
    },
    {
        "slug": "debugging",
        "name": "Debugging",
        "description": "Find and fix broken code — Beginner to Elite",
        "icon": "alert",
    },
]

QUESTIONS_PER_SECTION = 100
QUESTIONS_PER_LEVEL = 17  # 6 levels × 17 = 102 (trim to 100)
DEBUGGING_QUESTIONS_PER_LEVEL = 20
