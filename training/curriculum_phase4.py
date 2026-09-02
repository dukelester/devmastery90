"""Phase 4 — Elite mastery track (Days 91–120).

Remediation, failure drills, proof artifacts, and interview density —
not a longer version of the same checklist.
"""
from typing import Any


PHASE4 = {
    "order": 4,
    "name": "Phase 4 — Elite Mastery Track",
    "description": (
        "Days 91–120: weakness remediation, production failure drills, "
        "proof-of-work artifacts, and interview calibration for elite bar."
    ),
}

WEEKS_13_16 = [
    {
        "week_number": 13,
        "phase_order": 4,
        "title": "Weakness Remediation Lab",
        "objectives": (
            "Close skill gaps from Phases 1–3 with timed drills, "
            "mistake autopsy, and fluency targets."
        ),
    },
    {
        "week_number": 14,
        "phase_order": 4,
        "title": "Production Failure Drills",
        "objectives": (
            "Incident response, chaos thinking, capacity/cost tradeoffs, "
            "and observability under pressure."
        ),
    },
    {
        "week_number": 15,
        "phase_order": 4,
        "title": "Proof-of-Work & Hard Systems",
        "objectives": (
            "Ship elite project NFRs, ADRs, load-test writeups, "
            "and defend architecture decisions."
        ),
    },
    {
        "week_number": 16,
        "phase_order": 4,
        "title": "Interview Calibration War Room",
        "objectives": (
            "Dense mocks, peer/self calibration, portfolio story, "
            "and next 90-day elite plan."
        ),
    },
]


def _day(
    day: int,
    week: int,
    title: str,
    focus: str,
    minutes: int,
    tasks: list[tuple],
) -> dict[str, Any]:
    return {
        "day_number": day,
        "week_number": week,
        "title": title,
        "focus": focus,
        "target_minutes": minutes,
        "tasks": tasks,
    }


PHASE4_DAYS: list[dict[str, Any]] = [
    # ——— Week 13: Weakness remediation ———
    _day(
        91, 13, "Skill autopsy & remediation plan", "Weakness Remediation", 210,
        [
            ("Review: Export top weaknesses", "Pull reports for HIGH/MEDIUM skills; write a 7-day remediation plan.", "review", "interview-skills", 45, "medium", "critical", 1),
            ("Study: Mistake taxonomy", "Re-categorize last 20 mistakes; mark unresolved knowledge gaps.", "study", "debugging", 45, "medium", "high", 2),
            ("Coding: Weak-pattern set (5)", "Timed set on your two weakest DSA patterns.", "coding", "algorithms-data-structures", 90, "hard", "critical", 3),
            ("Reading: Skill resource pack", "Complete primary curated resources for your weakest skill.", "reading", "interview-skills", 30, "easy", "high", 4),
        ],
    ),
    _day(
        92, 13, "Python fluency under time", "Weakness Remediation", 240,
        [
            ("Assessment: 60m advanced Python", "Timed Python covering descriptors, concurrency, packaging.", "assessment", "python", 60, "hard", "critical", 1),
            ("Coding: Re-solve failures", "Re-solve every missed problem until you can teach it.", "coding", "python", 90, "hard", "critical", 2),
            ("Interview: Explain GIL & async", "Record a 8-minute explanation; score clarity.", "interview", "interview-skills", 45, "medium", "high", 3),
            ("Review: Python remediation notes", "Write flashcards for remaining gaps.", "review", "python", 30, "easy", "medium", 4),
        ],
    ),
    _day(
        93, 13, "DSA pressure block A", "Weakness Remediation", 240,
        [
            ("Coding: Graphs timed (6)", "Six graph problems in 90 minutes; track pattern misses.", "coding", "algorithms-data-structures", 90, "hard", "critical", 1),
            ("Coding: DP timed (4)", "Four DP problems with complexity writeups.", "coding", "algorithms-data-structures", 90, "hard", "critical", 2),
            ("Review: Pattern cheat-sheet", "Update personal pattern sheet from today's misses.", "review", "algorithms-data-structures", 30, "medium", "high", 3),
            ("Reading: Algorithm resource", "Read primary DSA curated article/course chapter.", "reading", "algorithms-data-structures", 30, "easy", "medium", 4),
        ],
    ),
    _day(
        94, 13, "DSA pressure block B", "Weakness Remediation", 240,
        [
            ("Coding: Heaps & scheduling (5)", "Five heap/interval problems under timer.", "coding", "algorithms-data-structures", 90, "hard", "critical", 1),
            ("Coding: Mixed hard set (4)", "Four mixed hard problems; no pattern hints.", "coding", "algorithms-data-structures", 90, "hard", "critical", 2),
            ("Assessment: 45m DSA mini-mock", "Self-proctored mock; log confidence per problem.", "assessment", "algorithms-data-structures", 45, "hard", "high", 3),
            ("Review: Mistake cards", "Create spaced-review cards for every wrong answer.", "review", "algorithms-data-structures", 15, "easy", "medium", 4),
        ],
    ),
    _day(
        95, 13, "SQL & Postgres deep remediation", "Weakness Remediation", 240,
        [
            ("Study: Isolation & locking deep dive", "Work through isolation anomalies with examples.", "study", "postgresql", 45, "hard", "critical", 1),
            ("Project: Optimize 5 slow queries", "EXPLAIN ANALYZE five queries; before/after plans.", "project", "postgresql", 90, "hard", "critical", 2),
            ("Coding: Window + CTE drills", "Four SQL drills with correctness checks.", "coding", "postgresql", 60, "hard", "high", 3),
            ("Reading: Postgres docs pack", "Primary Postgres curated resources.", "reading", "postgresql", 30, "easy", "high", 4),
        ],
    ),
    _day(
        96, 13, "Backend API remediation", "Weakness Remediation", 210,
        [
            ("Project: Harden authz matrix", "Document and test RBAC edge cases for a sample API.", "project", "backend-engineering", 75, "hard", "critical", 1),
            ("Coding: Idempotent endpoints", "Implement idempotency keys + replay tests.", "coding", "django", 60, "hard", "high", 2),
            ("Debugging: Reproduce race", "Induce and fix a TOCTOU/race in a checkout-like flow.", "debugging", "debugging", 45, "hard", "high", 3),
            ("Review: API remediation notes", "Capture patterns for interviews.", "review", "backend-engineering", 30, "easy", "medium", 4),
        ],
    ),
    _day(
        97, 13, "Week 13 remediation assessment", "Weakness Remediation", 240,
        [
            ("Assessment: Combined remediation exam", "Python + DSA + SQL timed block.", "assessment", "interview-skills", 120, "hard", "critical", 1),
            ("Review: Score vs day-90 baseline", "Compare to Phase 3 scores; update skill targets.", "review", "interview-skills", 45, "medium", "critical", 2),
            ("Interview: Teach your weakest topic", "15-minute teach-back recording.", "interview", "communication", 45, "medium", "high", 3),
            ("Review: Weekly review", "Wins, gaps, next week focus.", "review", "interview-skills", 30, "easy", "medium", 4),
        ],
    ),
    # ——— Week 14: Production failure drills ———
    _day(
        98, 14, "Incident command basics", "Production Failure Drills", 210,
        [
            ("Study: Incident response playbook", "Roles, severity, comms, blameless postmortem structure.", "study", "software-architecture", 45, "medium", "critical", 1),
            ("Project: Write on-call runbook", "Runbook for your Phase 3 project (alerts, dashboards, steps).", "project", "performance-engineering", 75, "hard", "critical", 2),
            ("Debugging: Synthetic SEV-2", "Inject latency; practice diagnose→mitigate→verify.", "debugging", "debugging", 60, "hard", "high", 3),
            ("Reading: SRE incident articles", "Primary curated SRE/incident resources.", "reading", "software-architecture", 30, "easy", "high", 4),
        ],
    ),
    _day(
        99, 14, "Chaos & failure modes", "Production Failure Drills", 240,
        [
            ("Study: Failure mode catalog", "Timeouts, partial outages, poison messages, thundering herd.", "study", "distributed-systems", 45, "hard", "critical", 1),
            ("Project: Chaos experiment plan", "Design 3 chaos experiments with abort criteria.", "project", "distributed-systems", 75, "hard", "critical", 2),
            ("Coding: Circuit breaker + retry", "Implement breaker/retry with tests for failure paths.", "coding", "backend-engineering", 75, "hard", "high", 3),
            ("Review: Failure notes", "Map each failure to detection signal.", "review", "distributed-systems", 30, "medium", "medium", 4),
        ],
    ),
    _day(
        100, 14, "Capacity, cost, latency budgets", "Production Failure Drills", 210,
        [
            ("Study: SLO / error budget math", "Define SLIs/SLOs for a sample API; error budget policy.", "study", "performance-engineering", 45, "hard", "critical", 1),
            ("Project: Capacity estimate sheet", "Back-of-envelope for QPS, storage, cost at 10× growth.", "project", "system-design", 75, "hard", "critical", 2),
            ("Project: Load-test writeup", "Run Locust/k6; publish p50/p95/p99 and bottleneck notes.", "project", "performance-engineering", 60, "hard", "high", 3),
            ("Reading: Performance resources", "Curated perf/SRE readings.", "reading", "performance-engineering", 30, "easy", "medium", 4),
        ],
    ),
    _day(
        101, 14, "Observability deep dive", "Production Failure Drills", 210,
        [
            ("Project: Trace a request end-to-end", "Add correlation IDs; document span map.", "project", "performance-engineering", 75, "hard", "critical", 1),
            ("Coding: Metrics & alert stubs", "RED/USE metrics + one actionable alert definition.", "coding", "backend-engineering", 60, "medium", "high", 2),
            ("Debugging: Blind log hunt", "Diagnose a planted bug using logs only.", "debugging", "debugging", 45, "hard", "high", 3),
            ("Review: Observability ADR", "One-page ADR on logging/metrics/tracing choices.", "review", "software-architecture", 30, "medium", "medium", 4),
        ],
    ),
    _day(
        102, 14, "Data & consistency under failure", "Production Failure Drills", 210,
        [
            ("Study: Exactly-once illusions", "At-least-once + idempotency; outbox pattern.", "study", "distributed-systems", 45, "hard", "critical", 1),
            ("Project: Outbox / webhook reliability", "Implement or design durable outbound delivery.", "project", "backend-engineering", 75, "hard", "critical", 2),
            ("Coding: Poison message handling", "DLQ path with replay tooling notes.", "coding", "redis", 60, "hard", "high", 3),
            ("Interview: Consistency tradeoffs", "Record 10-minute CAP/consistency interview answer.", "interview", "system-design", 30, "medium", "high", 4),
        ],
    ),
    _day(
        103, 14, "Security & abuse under load", "Production Failure Drills", 210,
        [
            ("Study: Authn/z failure modes", "Token expiry, confused deputy, IDOR drills.", "study", "backend-engineering", 45, "hard", "critical", 1),
            ("Project: Threat model (STRIDE lite)", "Threat model your flagship project; top 5 mitigations.", "project", "software-architecture", 75, "hard", "critical", 2),
            ("Coding: Rate limit + abuse controls", "Implement and test rate limits with burst behavior.", "coding", "django", 60, "hard", "high", 3),
            ("Review: Security checklist", "Checklist for interview + production.", "review", "backend-engineering", 30, "easy", "medium", 4),
        ],
    ),
    _day(
        104, 14, "Week 14 failure-drill assessment", "Production Failure Drills", 240,
        [
            ("Assessment: Incident tabletop", "90-minute tabletop SEV-1; write timeline + actions.", "assessment", "software-architecture", 90, "hard", "critical", 1),
            ("Project: Blameless postmortem", "Publish postmortem with action items and owners.", "project", "communication", 60, "hard", "critical", 2),
            ("Interview: Production story", "Behavioral: tell a production incident story (STAR).", "interview", "communication", 45, "medium", "high", 3),
            ("Review: Weekly review", "What would break next under 10× traffic?", "review", "performance-engineering", 30, "easy", "medium", 4),
        ],
    ),
    # ——— Week 15: Proof-of-work ———
    _day(
        105, 15, "Elite NFR pass — planning", "Proof-of-Work", 210,
        [
            ("Project: Gap analysis vs elite NFRs", "Map project against elite NFR/AC list; prioritize gaps.", "project", "software-architecture", 60, "hard", "critical", 1),
            ("Study: ADR writing", "Write 2 ADRs for contested decisions.", "study", "software-architecture", 45, "medium", "high", 2),
            ("Project: Architecture diagram v2", "Update C4/sequence diagrams for failure paths.", "project", "system-design", 60, "hard", "high", 3),
            ("Reading: Architecture resources", "Curated architecture readings.", "reading", "software-architecture", 30, "easy", "medium", 4),
        ],
    ),
    _day(
        106, 15, "Elite NFR pass — reliability", "Proof-of-Work", 240,
        [
            ("Project: Implement critical NFRs", "Ship retries, timeouts, idempotency, health checks.", "project", "backend-engineering", 120, "hard", "critical", 1),
            ("Coding: Contract tests", "Add contract/integration tests for failure paths.", "coding", "testing", 75, "hard", "high", 2),
            ("Review: Reliability notes", "Document what is still soft.", "review", "testing", 30, "easy", "medium", 3),
        ],
    ),
    _day(
        107, 15, "Elite NFR pass — performance", "Proof-of-Work", 240,
        [
            ("Project: Benchmark + optimize", "Hit documented p95 targets or explain gaps with data.", "project", "performance-engineering", 120, "hard", "critical", 1),
            ("Project: Cost/latency tradeoff memo", "One-page memo: what you sacrificed and why.", "project", "system-design", 60, "hard", "high", 2),
            ("Review: Perf evidence pack", "Charts + methodology for interviews.", "review", "performance-engineering", 45, "medium", "high", 3),
        ],
    ),
    _day(
        108, 15, "System design elite set", "Proof-of-Work", 240,
        [
            ("System design: Multi-region API", "Design multi-region with failover; 45m timed.", "system_design", "system-design", 60, "hard", "critical", 1),
            ("System design: Job platform", "Design async job platform with fairness & poison handling.", "system_design", "system-design", 60, "hard", "critical", 2),
            ("System design: Search/index", "Design search indexing pipeline.", "system_design", "system-design", 60, "hard", "high", 3),
            ("Review: Design scorecards", "Self-score against clarity, bottlenecks, tradeoffs.", "review", "system-design", 45, "medium", "high", 4),
        ],
    ),
    _day(
        109, 15, "Cloud & ops proof", "Proof-of-Work", 210,
        [
            ("Project: Deploy story", "Document real deploy path (compose/k8s/cloud) with rollback.", "project", "aws", 75, "hard", "critical", 1),
            ("Study: K8s mental model", "Pods, services, probes, HPA — map to your app.", "study", "kubernetes", 45, "medium", "high", 2),
            ("Project: CI quality gates", "Require tests + lint + migration check in CI.", "project", "docker", 60, "medium", "high", 3),
            ("Reading: Cloud curated pack", "Primary AWS/K8s resources.", "reading", "aws", 30, "easy", "medium", 4),
        ],
    ),
    _day(
        110, 15, "Portfolio & GitHub proof pack", "Proof-of-Work", 210,
        [
            ("Project: README + demo script", "5-minute demo script; architecture section; env docs.", "project", "communication", 75, "medium", "critical", 1),
            ("Project: Case study writeup", "Problem → constraints → design → results → lessons.", "project", "communication", 75, "hard", "critical", 2),
            ("Review: CV bullet draft", "3 quantified bullets from this project.", "review", "interview-skills", 30, "easy", "high", 3),
            ("Interview: Walk the repo", "Record 10-minute repo walkthrough.", "interview", "interview-skills", 30, "medium", "high", 4),
        ],
    ),
    _day(
        111, 15, "Week 15 proof assessment", "Proof-of-Work", 240,
        [
            ("Assessment: Defend the system", "90m: defend architecture to an imagined senior panel.", "assessment", "system-design", 90, "hard", "critical", 1),
            ("Project: Checklist elite AC", "Mark project hub criteria; close remaining required AC.", "project", "software-architecture", 75, "hard", "critical", 2),
            ("Review: Weekly review", "Evidence pack completeness score.", "review", "interview-skills", 45, "medium", "high", 3),
            ("Reading: Communication resources", "Curated writing/speaking resources.", "reading", "communication", 30, "easy", "medium", 4),
        ],
    ),
    # ——— Week 16: Interview calibration ———
    _day(
        112, 16, "Mock gauntlet — coding", "Interview Calibration", 240,
        [
            ("Interview: Full coding mock", "90m mock coding with narration.", "interview", "algorithms-data-structures", 90, "hard", "critical", 1),
            ("Review: Score & rework", "Rubric score; rework weak solutions.", "review", "algorithms-data-structures", 75, "hard", "critical", 2),
            ("Coding: Follow-up hard set", "Three hard follow-ups from mock misses.", "coding", "algorithms-data-structures", 60, "hard", "high", 3),
            ("Reading: Interview craft", "Curated interview resources.", "reading", "interview-skills", 15, "easy", "medium", 4),
        ],
    ),
    _day(
        113, 16, "Mock gauntlet — backend", "Interview Calibration", 240,
        [
            ("Interview: Backend design + code", "API + schema + tests in timed session.", "interview", "backend-engineering", 90, "hard", "critical", 1),
            ("Assessment: SQL interview set", "Timed SQL + indexing reasoning.", "assessment", "postgresql", 60, "hard", "critical", 2),
            ("Debugging: Live debug interview", "Debug a broken service with limited time.", "debugging", "debugging", 60, "hard", "high", 3),
            ("Review: Backend rubric", "Self-score against senior rubric.", "review", "backend-engineering", 30, "medium", "high", 4),
        ],
    ),
    _day(
        114, 16, "Mock gauntlet — system design", "Interview Calibration", 240,
        [
            ("Interview: System design mock A", "45m design + 15m critique.", "interview", "system-design", 60, "hard", "critical", 1),
            ("Interview: System design mock B", "Different domain; focus on bottlenecks.", "interview", "system-design", 60, "hard", "critical", 2),
            ("System design: Rapid drills (3)", "Three 20-minute outline-only designs.", "system_design", "system-design", 75, "hard", "high", 3),
            ("Review: Design improvements", "Rewrite weakest answer.", "review", "system-design", 30, "medium", "high", 4),
        ],
    ),
    _day(
        115, 16, "Behavioral & leadership stories", "Interview Calibration", 180,
        [
            ("Interview: Leadership STAR set", "Conflict, failure, mentorship, ambiguity — 4 stories.", "interview", "communication", 75, "medium", "critical", 1),
            ("Interview: AI usage ethics", "How you use AI responsibly in engineering work.", "interview", "ai-engineering", 30, "medium", "high", 2),
            ("Project: Story bank doc", "Written bank of 8 stories with metrics.", "project", "communication", 45, "medium", "high", 3),
            ("Review: Delivery practice", "Rehearse top 3 stories aloud.", "review", "interview-skills", 30, "easy", "medium", 4),
        ],
    ),
    _day(
        116, 16, "Full loop simulation", "Interview Calibration", 300,
        [
            ("Interview: Full loop day", "Coding + backend + design + behavioral in one day.", "interview", "interview-skills", 210, "hard", "critical", 1),
            ("Review: Loop debrief", "Scorecard vs elite bar; recovery plan.", "review", "interview-skills", 60, "hard", "critical", 2),
            ("Review: Energy & pacing notes", "What drained time; fix for next loop.", "review", "interview-skills", 30, "easy", "medium", 3),
        ],
    ),
    _day(
        117, 16, "External calibration", "Interview Calibration", 210,
        [
            ("Project: Peer or mentor review ask", "Send repo + design doc for feedback (or self-rubric if solo).", "project", "communication", 60, "medium", "critical", 1),
            ("Interview: Cold problem set", "Problems you have not seen; no notes.", "interview", "algorithms-data-structures", 90, "hard", "critical", 2),
            ("Review: Incorporate feedback", "Action list from calibration.", "review", "interview-skills", 45, "medium", "high", 3),
            ("Reading: Role leveling guides", "Curated senior/staff leveling articles.", "reading", "interview-skills", 15, "easy", "medium", 4),
        ],
    ),
    _day(
        118, 16, "Offer readiness pack", "Interview Calibration", 180,
        [
            ("Project: Negotiate & level research", "Comp bands, level expectations, questions to ask.", "project", "interview-skills", 60, "medium", "high", 1),
            ("Review: GitHub + LinkedIn polish", "Pin projects; align headlines with proof pack.", "review", "interview-skills", 45, "easy", "critical", 2),
            ("Interview: Closing pitch", "2-minute 'why me' with production proof.", "interview", "interview-skills", 45, "medium", "high", 3),
            ("Reading: Career resources", "Curated career/offer resources.", "reading", "interview-skills", 30, "easy", "medium", 4),
        ],
    ),
    _day(
        119, 16, "Final elite assessment", "Interview Calibration", 300,
        [
            ("Assessment: Elite composite exam", "Python, DSA, SQL, design — no notes.", "assessment", "interview-skills", 150, "hard", "critical", 1),
            ("Assessment: Debug + harden", "Debug challenge + regression tests.", "assessment", "debugging", 75, "hard", "critical", 2),
            ("Review: Final skill scores", "Update skill scores honestly against evidence.", "review", "interview-skills", 45, "medium", "critical", 3),
            ("Review: Gap list for next cycle", "Anything still below elite bar.", "review", "interview-skills", 30, "easy", "high", 4),
        ],
    ),
    _day(
        120, 16, "Day 120 — Elite closeout", "Interview Calibration", 210,
        [
            ("Review: Portfolio & proof archive", "Archive ADRs, postmortems, load reports, demos.", "review", "communication", 60, "medium", "critical", 1),
            ("Project: Next 90-day elite plan", "New plan targeting remaining gaps + role trajectory.", "project", "interview-skills", 60, "medium", "critical", 2),
            ("Interview: Final mock (short)", "45m mixed mock as smoke test.", "interview", "interview-skills", 45, "hard", "high", 3),
            ("Review: Celebrate & reset", "Mark Phase 4 complete; set start for next cycle.", "review", "interview-skills", 30, "easy", "medium", 4),
        ],
    ),
]
