"""Days 15-90 of the DevMastery curriculum."""
from typing import Any

REMAINING_DAYS: list[dict[str, Any]] = [
    # Week 3
    {"day_number": 15, "week_number": 3, "title": "Arrays & Two Pointers", "focus": "Algorithms", "target_minutes": 240,
     "tasks": [
         ("Study: Big-O and arrays", "Review complexity analysis and array operations.", "study", "algorithms-data-structures", 30, "medium", "high", 1),
         ("Study: Two pointers technique", "Master two-pointer patterns.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
         ("Coding: 5 two-pointer problems", "Solve 5 two-pointer problems.", "coding", "algorithms-data-structures", 90, "medium", "high", 3),
         ("Review: Pattern notes", "Document two-pointer patterns.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 16, "week_number": 3, "title": "Sliding Window", "focus": "Algorithms", "target_minutes": 240,
     "tasks": [
         ("Study: Sliding window", "Fixed and variable sliding window patterns.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: Frequency counting", "Frequency maps in sliding windows.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
         ("Coding: 5 sliding window problems", "Solve 5 sliding window problems.", "coding", "algorithms-data-structures", 90, "hard", "high", 3),
         ("Review: Window patterns", "Document sliding window framework.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 17, "week_number": 3, "title": "Binary Search", "focus": "Algorithms", "target_minutes": 240,
     "tasks": [
         ("Study: Binary search fundamentals", "Binary search and search space reduction.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: Search variations", "Rotated arrays and answer-space search.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
         ("Coding: 5 binary search problems", "Solve 5 binary search problems.", "coding", "algorithms-data-structures", 90, "hard", "high", 3),
         ("Review: Binary search patterns", "When binary search applies beyond sorted arrays.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 18, "week_number": 3, "title": "Stacks & Queues", "focus": "Algorithms", "target_minutes": 240,
     "tasks": [
         ("Study: Stack, queue, deque", "Stack, queue, and deque implementations.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: Monotonic stack", "Monotonic stack for range problems.", "study", "algorithms-data-structures", 30, "hard", "high", 2),
         ("Coding: 5 stack/queue problems", "Solve 5 stack and queue problems.", "coding", "algorithms-data-structures", 90, "hard", "high", 3),
         ("Review: Stack patterns", "Monotonic stack patterns.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 19, "week_number": 3, "title": "Linked Lists", "focus": "Algorithms", "target_minutes": 240,
     "tasks": [
         ("Study: Linked list operations", "Insertion, deletion, reversal, cycle detection.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: Fast/slow pointers", "Fast/slow pointer technique.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
         ("Coding: 5 linked list problems", "Solve 5 linked list problems.", "coding", "algorithms-data-structures", 90, "hard", "high", 3),
         ("Review: Linked list patterns", "Linked list problem patterns.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 20, "week_number": 3, "title": "Recursion & Backtracking", "focus": "Algorithms", "target_minutes": 240,
     "tasks": [
         ("Study: Recursion fundamentals", "Base cases and recursive structure.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: Backtracking", "Permutations, combinations, constraint search.", "study", "algorithms-data-structures", 30, "hard", "high", 2),
         ("Coding: 5 recursion problems", "Solve 5 backtracking problems.", "coding", "algorithms-data-structures", 90, "hard", "high", 3),
         ("Review: Recursion patterns", "Backtracking template.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 21, "week_number": 3, "title": "Week 3 DSA Assessment", "focus": "Algorithms", "target_minutes": 240,
     "tasks": [
         ("Assessment: 10 timed DSA problems", "90-minute DSA assessment.", "assessment", "algorithms-data-structures", 90, "hard", "critical", 1),
         ("Review: Mistake analysis", "Analyze mistakes and weak patterns.", "review", "algorithms-data-structures", 45, "medium", "high", 2),
         ("Review: Pattern review", "Review Week 3 patterns.", "review", "algorithms-data-structures", 30, "medium", "high", 3),
         ("Review: Weekly review", "Complete weekly review.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    # Week 4
    {"day_number": 22, "week_number": 4, "title": "Trees DFS/BFS", "focus": "Advanced DSA", "target_minutes": 240,
     "tasks": [
         ("Study: Tree fundamentals", "Binary trees and traversals.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: DFS and BFS on trees", "Tree traversal strategies.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
         ("Coding: 5 tree problems", "Solve 5 tree problems.", "coding", "algorithms-data-structures", 90, "hard", "high", 3),
         ("Review: Tree patterns", "Tree problem classification.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 23, "week_number": 4, "title": "Binary Search Trees", "focus": "Advanced DSA", "target_minutes": 210,
     "tasks": [
         ("Study: BST operations", "Insert, delete, search, validate BST.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: Tree traversal variants", "Inorder, preorder, postorder in BST.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
         ("Coding: BST problems including LCA", "Solve BST problems.", "coding", "algorithms-data-structures", 75, "hard", "high", 3),
         ("Review: BST patterns", "BST problem patterns.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 24, "week_number": 4, "title": "Heaps & Priority Queues", "focus": "Advanced DSA", "target_minutes": 210,
     "tasks": [
         ("Study: Heaps and priority queues", "Min/max heap operations.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: Top-K problems", "Top-K using heaps.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
         ("Coding: 5 heap problems", "Solve 5 heap problems.", "coding", "algorithms-data-structures", 75, "hard", "high", 3),
         ("Review: Heap patterns", "When heaps beat sorting.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 25, "week_number": 4, "title": "Graph Fundamentals", "focus": "Advanced DSA", "target_minutes": 210,
     "tasks": [
         ("Study: Graph representation", "Adjacency list, matrix, edge list.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: Graph BFS and DFS", "Graph traversal algorithms.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
         ("Coding: 5 graph traversal problems", "Solve graph BFS/DFS problems.", "coding", "algorithms-data-structures", 75, "hard", "high", 3),
         ("Review: Graph patterns", "Graph problem identification.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 26, "week_number": 4, "title": "Advanced Graph Algorithms", "focus": "Advanced DSA", "target_minutes": 210,
     "tasks": [
         ("Study: Topological sorting", "Kahn's and DFS topo sort.", "study", "algorithms-data-structures", 45, "hard", "high", 1),
         ("Study: Union Find", "DSU with path compression.", "study", "algorithms-data-structures", 30, "hard", "high", 2),
         ("Coding: Graph connectivity problems", "Topo sort and union find problems.", "coding", "algorithms-data-structures", 75, "hard", "high", 3),
         ("Review: Advanced graph patterns", "Union find applications.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 27, "week_number": 4, "title": "Dynamic Programming", "focus": "Advanced DSA", "target_minutes": 240,
     "tasks": [
         ("Study: DP fundamentals", "Memoization vs tabulation.", "study", "algorithms-data-structures", 45, "hard", "high", 1),
         ("Study: DP patterns", "1D, 2D, knapsack, interval DP.", "study", "algorithms-data-structures", 45, "hard", "high", 2),
         ("Coding: 5 DP problems", "Solve 5 DP problems.", "coding", "algorithms-data-structures", 90, "hard", "critical", 3),
         ("Review: DP framework", "DP identification framework.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 28, "week_number": 4, "title": "Greedy Algorithms", "focus": "Advanced DSA", "target_minutes": 210,
     "tasks": [
         ("Study: Greedy algorithms", "Greedy choice property.", "study", "algorithms-data-structures", 45, "medium", "high", 1),
         ("Study: Intervals and scheduling", "Interval scheduling problems.", "study", "algorithms-data-structures", 30, "medium", "high", 2),
         ("Coding: 5 greedy problems", "Solve 5 greedy problems.", "coding", "algorithms-data-structures", 75, "hard", "high", 3),
         ("Review: Greedy vs DP", "When greedy works.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
     ]},
    {"day_number": 29, "week_number": 4, "title": "DSA Mock Assessment", "focus": "Advanced DSA", "target_minutes": 300,
     "tasks": [
         ("Assessment: 2-hour DSA mock", "Full DSA mock assessment.", "assessment", "algorithms-data-structures", 120, "hard", "critical", 1),
         ("Review: Mistake analysis", "Deep mistake analysis.", "review", "algorithms-data-structures", 60, "medium", "high", 2),
         ("Review: Weak pattern focus", "Targeted practice plan.", "review", "algorithms-data-structures", 30, "medium", "high", 3),
     ]},
    {"day_number": 30, "week_number": 4, "title": "Month 1 Assessment", "focus": "Advanced DSA", "target_minutes": 300,
     "tasks": [
         ("Assessment: Python assessment", "Phase 1 Python assessment.", "assessment", "python", 90, "hard", "critical", 1),
         ("Assessment: DSA assessment", "Phase 1 DSA assessment.", "assessment", "algorithms-data-structures", 90, "hard", "critical", 2),
         ("Review: Update skill scores", "Update skill scores from month 1.", "review", "python", 30, "medium", "high", 3),
         ("Review: Monthly review", "Month 1 comprehensive review.", "review", "interview-skills", 30, "medium", "high", 4),
     ]},
]

WEEKS_5_12_TEMPLATE: list[dict[str, Any]] = [
    {"day": 31, "week": 5, "title": "HTTP Fundamentals", "focus": "HTTP + REST + Django", "minutes": 210, "skill": "backend-engineering",
     "items": ["HTTP methods and semantics", "Status codes and headers", "Cookies and sessions", "Build raw HTTP API"]},
    {"day": 32, "week": 5, "title": "REST API Design", "focus": "HTTP + REST + Django", "minutes": 210, "skill": "backend-engineering",
     "items": ["REST principles", "Resource design", "Pagination filtering sorting", "API design exercise"]},
    {"day": 33, "week": 5, "title": "Django Architecture", "focus": "HTTP + REST + Django", "minutes": 240, "skill": "django",
     "items": ["Django project structure", "Models and migrations", "Views and URLs", "CRUD API implementation"]},
    {"day": 34, "week": 5, "title": "Django REST Framework", "focus": "HTTP + REST + Django", "minutes": 240, "skill": "django",
     "items": ["Serializers and validation", "ViewSets and routers", "Permissions", "DRF API project"]},
    {"day": 35, "week": 5, "title": "Auth & Authorization", "focus": "HTTP + REST + Django", "minutes": 210, "skill": "backend-engineering",
     "items": ["JWT and sessions", "Authorization patterns", "RBAC implementation", "Secure API endpoints"]},
    {"day": 36, "week": 5, "title": "API Production Patterns", "focus": "HTTP + REST + Django", "minutes": 210, "skill": "backend-engineering",
     "items": ["Validation strategies", "Error handling", "API versioning", "Rate limiting"]},
    {"day": 37, "week": 5, "title": "Production REST API", "focus": "HTTP + REST + Django", "minutes": 240, "skill": "django",
     "items": ["Production REST API build", "API documentation", "API testing suite", "Weekly review"]},
    {"day": 38, "week": 6, "title": "Schema Design", "focus": "PostgreSQL", "minutes": 210, "skill": "postgresql",
     "items": ["Schema design principles", "Normalization", "Constraints and integrity", "SaaS schema exercise"]},
    {"day": 39, "week": 6, "title": "Advanced SQL", "focus": "PostgreSQL", "minutes": 240, "skill": "postgresql",
     "items": ["JOINs and subqueries", "CTEs and window functions", "Complex query exercises", "SQL problem set"]},
    {"day": 40, "week": 6, "title": "Indexes", "focus": "PostgreSQL", "minutes": 210, "skill": "postgresql",
     "items": ["B-tree indexes", "Composite indexes", "Index selection strategy", "Indexing exercises"]},
    {"day": 41, "week": 6, "title": "Query Optimization", "focus": "PostgreSQL", "minutes": 210, "skill": "postgresql",
     "items": ["EXPLAIN and EXPLAIN ANALYZE", "Query plan analysis", "Optimize 3 slow queries", "Optimization report"]},
    {"day": 42, "week": 6, "title": "Transactions & ACID", "focus": "PostgreSQL", "minutes": 210, "skill": "postgresql",
     "items": ["ACID properties", "Isolation levels", "Locking mechanisms", "Transaction exercises"]},
    {"day": 43, "week": 6, "title": "Concurrency", "focus": "PostgreSQL", "minutes": 210, "skill": "postgresql",
     "items": ["Race conditions", "Optimistic locking", "Pessimistic locking", "Concurrency exercises"]},
    {"day": 44, "week": 6, "title": "PostgreSQL Assessment", "focus": "PostgreSQL", "minutes": 240, "skill": "postgresql",
     "items": ["PostgreSQL assessment", "SaaS database design", "Query optimization challenge", "Weekly review"]},
    {"day": 45, "week": 7, "title": "Redis Fundamentals", "focus": "Redis + Distributed Systems", "minutes": 210, "skill": "redis",
     "items": ["Redis data structures", "Redis commands", "Persistence options", "Redis exercises"]},
    {"day": 46, "week": 7, "title": "Caching Strategies", "focus": "Redis + Distributed Systems", "minutes": 210, "skill": "redis",
     "items": ["Cache-aside pattern", "TTL strategies", "Cache invalidation", "Caching implementation"]},
    {"day": 47, "week": 7, "title": "Celery & Background Jobs", "focus": "Redis + Distributed Systems", "minutes": 240, "skill": "distributed-systems",
     "items": ["Celery architecture", "Task queues", "Retry strategies", "Background job implementation"]},
    {"day": 48, "week": 7, "title": "Message Queues", "focus": "Redis + Distributed Systems", "minutes": 210, "skill": "distributed-systems",
     "items": ["RabbitMQ concepts", "Kafka fundamentals", "Event-driven architecture", "Queue design exercise"]},
    {"day": 49, "week": 7, "title": "Reliability Patterns", "focus": "Redis + Distributed Systems", "minutes": 210, "skill": "distributed-systems",
     "items": ["Idempotency", "Retry policies", "Timeouts", "Circuit breakers"]},
    {"day": 50, "week": 7, "title": "CAP Theorem", "focus": "Redis + Distributed Systems", "minutes": 210, "skill": "distributed-systems",
     "items": ["CAP theorem", "Consistency models", "Availability trade-offs", "Partition tolerance"]},
    {"day": 51, "week": 7, "title": "Distributed Systems Assessment", "focus": "Redis + Distributed Systems", "minutes": 240, "skill": "distributed-systems",
     "items": ["Distributed systems assessment", "Design notification system", "Review mistakes", "Weekly review"]},
    {"day": 52, "week": 8, "title": "Scalability", "focus": "System Design", "minutes": 210, "skill": "system-design",
     "items": ["Horizontal vs vertical scaling", "Load balancing", "Auto-scaling concepts", "Scalability exercise"]},
    {"day": 53, "week": 8, "title": "Database Scaling", "focus": "System Design", "minutes": 210, "skill": "system-design",
     "items": ["Replication strategies", "Read replicas", "Sharding concepts", "Scaling design exercise"]},
    {"day": 54, "week": 8, "title": "CDN & Object Storage", "focus": "System Design", "minutes": 210, "skill": "system-design",
     "items": ["CDN architecture", "Object storage S3", "Large file systems", "Storage design exercise"]},
    {"day": 55, "week": 8, "title": "Design URL Shortener", "focus": "System Design", "minutes": 240, "skill": "system-design",
     "items": ["URL shortener requirements", "Architecture design", "Record and review answer", "Iterate on design"]},
    {"day": 56, "week": 8, "title": "Design Chat System", "focus": "System Design", "minutes": 240, "skill": "system-design",
     "items": ["Chat system requirements", "Real-time architecture", "Record and review answer", "Iterate on design"]},
    {"day": 57, "week": 8, "title": "Design Payment System", "focus": "System Design", "minutes": 240, "skill": "system-design",
     "items": ["Payment system requirements", "Consistency and idempotency", "Record and review answer", "Iterate on design"]},
    {"day": 58, "week": 8, "title": "Design Video Processing", "focus": "System Design", "minutes": 240, "skill": "system-design",
     "items": ["Video processing requirements", "Pipeline architecture", "Record and review answer", "Iterate on design"]},
    {"day": 59, "week": 8, "title": "System Design Interview", "focus": "System Design", "minutes": 240, "skill": "system-design",
     "items": ["90-minute system design interview", "Record answer", "Self-review and scoring", "Improvement plan"]},
    {"day": 60, "week": 8, "title": "Month 2 Assessment", "focus": "System Design", "minutes": 300, "skill": "backend-engineering",
     "items": ["Backend coding assessment", "SQL assessment", "System design assessment", "Update skill scores"]},
    {"day": 61, "week": 9, "title": "Project Architecture", "focus": "AI Document Processing Platform", "minutes": 240, "skill": "software-architecture",
     "items": ["Requirements gathering", "Architecture design", "Database design", "API specification"]},
    {"day": 62, "week": 9, "title": "Django Project Setup", "focus": "AI Document Processing Platform", "minutes": 240, "skill": "django",
     "items": ["Django project scaffold", "Authentication system", "User management", "Project configuration"]},
    {"day": 63, "week": 9, "title": "Multi-tenancy", "focus": "AI Document Processing Platform", "minutes": 240, "skill": "django",
     "items": ["Multi-tenancy patterns", "Organization permissions", "Tenant isolation", "Organization management"]},
    {"day": 64, "week": 9, "title": "Document Uploads", "focus": "AI Document Processing Platform", "minutes": 240, "skill": "backend-engineering",
     "items": ["File upload handling", "Object storage integration", "Upload validation", "Storage security"]},
    {"day": 65, "week": 9, "title": "Background Processing", "focus": "AI Document Processing Platform", "minutes": 240, "skill": "distributed-systems",
     "items": ["Celery task design", "Redis queue setup", "Job monitoring", "Retry and error handling"]},
    {"day": 66, "week": 9, "title": "AI API Integration", "focus": "AI Document Processing Platform", "minutes": 240, "skill": "ai-engineering",
     "items": ["AI API integration", "Error handling and retries", "Response parsing", "Cost optimization"]},
    {"day": 67, "week": 9, "title": "Integration Testing", "focus": "AI Document Processing Platform", "minutes": 240, "skill": "testing",
     "items": ["Integration test suite", "End-to-end testing", "Project review", "Documentation"]},
    {"day": 68, "week": 10, "title": "PostgreSQL Optimization", "focus": "Production Hardening", "minutes": 210, "skill": "postgresql",
     "items": ["Query profiling", "Index optimization", "Connection pooling", "Performance report"]},
    {"day": 69, "week": 10, "title": "Redis Caching Layer", "focus": "Production Hardening", "minutes": 210, "skill": "redis",
     "items": ["Cache layer design", "Cache warming", "Cache monitoring", "Performance benchmarks"]},
    {"day": 70, "week": 10, "title": "API Security", "focus": "Production Hardening", "minutes": 210, "skill": "backend-engineering",
     "items": ["Rate limiting implementation", "API security headers", "Input sanitization", "Security audit"]},
    {"day": 71, "week": 10, "title": "Idempotency & Webhooks", "focus": "Production Hardening", "minutes": 210, "skill": "backend-engineering",
     "items": ["Idempotency keys", "Webhook design", "Retry handling", "Delivery guarantees"]},
    {"day": 72, "week": 10, "title": "Observability", "focus": "Production Hardening", "minutes": 210, "skill": "performance-engineering",
     "items": ["Structured logging", "Metrics collection", "Monitoring dashboards", "Alerting setup"]},
    {"day": 73, "week": 10, "title": "Docker & Compose", "focus": "Production Hardening", "minutes": 240, "skill": "docker",
     "items": ["Dockerfile optimization", "Docker Compose setup", "Production configuration", "Multi-stage builds"]},
    {"day": 74, "week": 10, "title": "CI/CD Pipeline", "focus": "Production Hardening", "minutes": 240, "skill": "docker",
     "items": ["CI/CD pipeline setup", "Automated testing in CI", "Deployment automation", "Weekly review"]},
    {"day": 75, "week": 11, "title": "pytest Mastery", "focus": "Testing + Cloud + Performance", "minutes": 210, "skill": "testing",
     "items": ["pytest fundamentals", "Fixtures and parametrization", "Mocking strategies", "Test suite build"]},
    {"day": 76, "week": 11, "title": "Integration Testing", "focus": "Testing + Cloud + Performance", "minutes": 210, "skill": "testing",
     "items": ["API integration tests", "Database test strategies", "Test isolation", "Integration test suite"]},
    {"day": 77, "week": 11, "title": "Failure & Security Testing", "focus": "Testing + Cloud + Performance", "minutes": 210, "skill": "testing",
     "items": ["Edge case testing", "Failure injection", "Security testing", "Chaos testing basics"]},
    {"day": 78, "week": 11, "title": "AWS Fundamentals", "focus": "Testing + Cloud + Performance", "minutes": 210, "skill": "aws",
     "items": ["EC2 and compute", "S3 object storage", "RDS database service", "AWS hands-on exercises"]},
    {"day": 79, "week": 11, "title": "Cloud Architecture", "focus": "Testing + Cloud + Performance", "minutes": 210, "skill": "aws",
     "items": ["Cloud architecture patterns", "Load balancing", "Auto scaling", "Cloud monitoring"]},
    {"day": 80, "week": 11, "title": "Performance Testing", "focus": "Testing + Cloud + Performance", "minutes": 240, "skill": "performance-engineering",
     "items": ["Locust setup", "API benchmarking", "Load test scenarios", "Performance baseline"]},
    {"day": 81, "week": 11, "title": "Performance Optimization", "focus": "Testing + Cloud + Performance", "minutes": 240, "skill": "performance-engineering",
     "items": ["Bottleneck analysis", "Fix performance issues", "Document improvements", "Weekly review"]},
    {"day": 82, "week": 12, "title": "Python War Room", "focus": "Interview War Room", "minutes": 240, "skill": "python",
     "items": ["90-minute Python assessment", "Mistake review", "Re-solve failed problems", "Pattern reinforcement"]},
    {"day": 83, "week": 12, "title": "DSA War Room", "focus": "Interview War Room", "minutes": 240, "skill": "algorithms-data-structures",
     "items": ["90-minute DSA assessment", "Complexity analysis review", "Re-solve failed problems", "Pattern reinforcement"]},
    {"day": 84, "week": 12, "title": "Backend War Room", "focus": "Interview War Room", "minutes": 300, "skill": "backend-engineering",
     "items": ["Backend implementation assessment", "PostgreSQL challenge", "Test writing challenge", "Docker deployment"]},
    {"day": 85, "week": 12, "title": "Debugging Challenge", "focus": "Interview War Room", "minutes": 240, "skill": "debugging",
     "items": ["Reproduce production bugs", "Diagnose root causes", "Fix and verify", "Write regression tests"]},
    {"day": 86, "week": 12, "title": "System Design War Room", "focus": "Interview War Room", "minutes": 300, "skill": "system-design",
     "items": ["Design payment system", "Design chat system", "Design file-processing system", "Self-review all designs"]},
    {"day": 87, "week": 12, "title": "Behavioral Preparation", "focus": "Interview War Room", "minutes": 210, "skill": "communication",
     "items": ["Technical achievements stories", "Production incident stories", "Failure and learning stories", "Leadership and AI usage"]},
    {"day": 88, "week": 12, "title": "Full Mock Interview", "focus": "Interview War Room", "minutes": 300, "skill": "interview-skills",
     "items": ["Coding interview mock", "Backend interview mock", "System design mock", "Behavioral interview mock"]},
    {"day": 89, "week": 12, "title": "Simulated Assessment", "focus": "Interview War Room", "minutes": 300, "skill": "interview-skills",
     "items": ["Full simulated assessment", "No notes allowed", "Timed conditions", "Post-assessment review"]},
    {"day": 90, "week": 12, "title": "Final Review & Next Plan", "focus": "Interview War Room", "minutes": 240, "skill": "interview-skills",
     "items": ["Re-solve all failed problems", "Review AI Document Processing project", "Update CV and GitHub", "Final skill assessment and next 90-day plan"]},
]


def classify_task(item: str, focus: str) -> str:
    lower = item.lower()
    if "assessment" in lower or "mock" in lower or "simulated" in lower:
        return "assessment"
    if "design" in lower and ("system" in focus.lower() or "payment" in lower or "chat" in lower):
        return "system_design"
    if "interview" in lower or "behavioral" in lower:
        return "interview"
    if "review" in lower:
        return "review"
    if "debug" in lower or "bug" in lower:
        return "debugging"
    if "solve" in lower or "problems" in lower:
        return "coding"
    if any(w in lower for w in ("build", "implement", "setup", "scaffold", "deployment")):
        return "project"
    if "test" in lower:
        return "project"
    return "study"


def build_week_5_12_days() -> list[dict[str, Any]]:
    days = []
    for entry in WEEKS_5_12_TEMPLATE:
        tasks = []
        for i, item in enumerate(entry["items"], 1):
            task_type = classify_task(item, entry["focus"])
            est = 45 if task_type == "study" else 60
            if "90-minute" in item.lower() or "2-hour" in item.lower():
                est = 90
            diff = "hard" if task_type in ("assessment", "system_design", "coding") else "medium"
            prio = "critical" if task_type == "assessment" else "high"
            tasks.append((item, f"Complete: {item}", task_type, entry["skill"], est, diff, prio, i))
        days.append({
            "day_number": entry["day"],
            "week_number": entry["week"],
            "title": entry["title"],
            "focus": entry["focus"],
            "target_minutes": entry["minutes"],
            "tasks": tasks,
        })
    return days
