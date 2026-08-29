"""Generate aptitude test questions programmatically."""
from __future__ import annotations

from typing import Any


def _entry(
    question: str,
    answer: str,
    explanation: str,
    category: str,
    difficulty: str = "medium",
) -> dict[str, Any]:
    return {
        "question": question,
        "answer": answer,
        "explanation": explanation,
        "category": category,
        "difficulty": difficulty,
    }


def _number_series_questions() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    patterns = [
        ("2, 4, 8, 16, ?", "32", "Multiply by 2 each step (geometric sequence).", "easy"),
        ("1, 1, 2, 3, 5, 8, ?", "13", "Fibonacci: sum of previous two terms.", "easy"),
        ("3, 6, 11, 18, ?", "27", "Differences increase by 2: +3, +5, +7, +9.", "medium"),
        ("2, 6, 12, 20, 30, ?", "42", "Differences: +4, +6, +8, +10, +12.", "medium"),
        ("1, 4, 9, 16, 25, ?", "36", "Perfect squares n².", "easy"),
        ("2, 3, 5, 8, 13, ?", "21", "Fibonacci-style addition.", "easy"),
        ("64, 32, 16, 8, ?", "4", "Halve each term.", "easy"),
        ("1, 3, 6, 10, 15, ?", "21", "Triangular numbers: +2, +3, +4, +5, +6.", "medium"),
        ("5, 10, 20, 40, ?", "80", "Multiply by 2.", "easy"),
        ("100, 95, 90, 85, ?", "80", "Subtract 5 each step.", "easy"),
    ]
    for q, a, e, d in patterns:
        items.append(_entry(q, a, e, "number_series", d))

    for n in range(2, 42):
        seq = [n, n + 2, n + 4, n + 6, n + 8]
        items.append(
            _entry(
                f"{seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ?",
                str(seq[4]),
                "Arithmetic sequence with common difference 2.",
                "number_series",
                "easy",
            )
        )

    for start in range(1, 31):
        term = start ** 2
        items.append(
            _entry(
                f"{start**2}, {(start+1)**2}, {(start+2)**2}, {(start+3)**2}, ?",
                str((start + 4) ** 2),
                "Consecutive perfect squares.",
                "number_series",
                "medium",
            )
        )
    return items


def _percentage_questions() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for pct in range(5, 96, 5):
        for base in [80, 120, 200, 240, 500, 1000]:
            part = round(base * pct / 100)
            items.append(
                _entry(
                    f"What is {pct}% of {base}?",
                    str(part),
                    f"{pct}% of {base} = ({pct}/100) × {base} = {part}.",
                    "percentages",
                    "easy" if pct <= 30 else "medium",
                )
            )
    for pct in [10, 15, 20, 25, 30, 40, 50]:
        for val in [60, 80, 120, 150, 200, 400]:
            result = round(val * (100 + pct) / 100)
            items.append(
                _entry(
                    f"A price of ${val} increases by {pct}%. What is the new price?",
                    f"${result}",
                    f"Increase: {val} × {1 + pct/100} = {result}.",
                    "percentages",
                    "medium",
                )
            )
            result_dec = round(val * (100 - pct) / 100)
            items.append(
                _entry(
                    f"A price of ${val} decreases by {pct}%. What is the new price?",
                    f"${result_dec}",
                    f"Decrease: {val} × {1 - pct/100} = {result_dec}.",
                    "percentages",
                    "medium",
                )
            )
    return items


def _ratio_questions() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    pairs = [(2, 3), (3, 4), (4, 5), (5, 8), (2, 5), (3, 7), (4, 9), (5, 12)]
    for a, b in pairs:
        for mult in range(2, 18):
            items.append(
                _entry(
                    f"Divide {a * mult + b * mult} in the ratio {a}:{b}. What is the larger share?",
                    str(max(a, b) * mult),
                    f"Total parts = {a + b}. Larger share = {max(a,b)}/{a+b} × {a*mult + b*mult}.",
                    "ratios",
                    "medium",
                )
            )
    for x in range(2, 25):
        items.append(
            _entry(
                f"If {x} workers finish a job in 12 days, how many days for {x * 2} workers at the same rate?",
                "6",
                "Inverse proportion: double workers → half the time.",
                "ratios",
                "medium",
            )
        )
    return items


def _time_speed_distance() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    speeds = [30, 40, 50, 60, 72, 80, 90, 100]
    times = [2, 3, 4, 5, 6]
    for s in speeds:
        for t in times:
            dist = s * t
            items.append(
                _entry(
                    f"A train travels at {s} km/h for {t} hours. Distance covered?",
                    f"{dist} km",
                    f"Distance = speed × time = {s} × {t} = {dist} km.",
                    "time_speed_distance",
                    "easy",
                )
            )
            items.append(
                _entry(
                    f"Distance {dist} km at {s} km/h. How many hours?",
                    str(t),
                    f"Time = distance / speed = {dist}/{s} = {t} h.",
                    "time_speed_distance",
                    "easy",
                )
            )
    return items


def _averages_questions() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for _ in range(40):
        nums = [10 + _ * 2, 20 + _ * 3, 30 + _, 40 + _ * 2]
        avg = round(sum(nums) / len(nums), 2)
        q = ", ".join(str(n) for n in nums)
        items.append(
            _entry(
                f"What is the average of {q}?",
                str(avg),
                f"Sum = {sum(nums)}. Average = {sum(nums)}/4 = {avg}.",
                "averages",
                "easy",
            )
        )
    return items


def _algebra_word_problems() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for a in range(3, 25):
        b = 5 + (a % 12)
        total = a + b
        items.append(
            _entry(
                f"The sum of two numbers is {total}. One is {a} more than the other. Find the larger number.",
                str((total + a) // 2),
                f"Let smaller = x, larger = x+{a}. 2x+{a}={total} → x={(total-a)//2}, larger={(total+a)//2}.",
                "algebra",
                "medium",
            )
        )
    for n in range(2, 30):
        items.append(
            _entry(
                f"Three consecutive integers sum to {3 * n + 3}. What is the middle integer?",
                str(n + 1),
                f"Let integers be n, n+1, n+2. Sum = 3n+3 → middle = n+1.",
                "algebra",
                "easy",
            )
        )
    return items


def _probability_questions() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    items.append(
        _entry(
            "A fair coin is flipped twice. Probability of exactly one head?",
            "1/2",
            "Outcomes: HH, HT, TH, TT — two with exactly one head → 2/4 = 1/2.",
            "probability",
            "medium",
        )
    )
    items.append(
        _entry(
            "A bag has 3 red and 5 blue balls. Probability of drawing red?",
            "3/8",
            "3 red out of 8 total → 3/8.",
            "probability",
            "easy",
        )
    )
    for red in range(2, 9):
        blue = red + (red % 5) + 1
        total = red + blue
        items.append(
            _entry(
                f"A bag has {red} red and {blue} blue balls. Probability of blue?",
                f"{blue}/{total}",
                f"{blue} blue out of {total} total.",
                "probability",
                "easy",
            )
        )
    return items


def _logical_reasoning() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = [
        _entry(
            "All mammals breathe air. Whales are mammals. What follows?",
            "Whales breathe air.",
            "Valid syllogism: whales inherit mammal properties.",
            "logical_reasoning",
            "easy",
        ),
        _entry(
            "If it rains, the ground gets wet. The ground is wet. Must it have rained?",
            "No",
            "Affirming the consequent fallacy — other causes could wet the ground.",
            "logical_reasoning",
            "medium",
        ),
        _entry(
            "Some A are B. All B are C. What can we conclude about A and C?",
            "Some A may be C (some A are C is possible).",
            "Some A in B, all B in C → those A are also in C.",
            "logical_reasoning",
            "hard",
        ),
        _entry(
            "Five people in a line: Alice is left of Bob, Bob left of Carol. Carol not at right end. Who is at the right end?",
            "Cannot be Carol; could be Alice, Bob, or others depending on full order — with only these facts, often Bob or another if only three named.",
            "Partial order constraints — list valid permutations.",
            "logical_reasoning",
            "hard",
        ),
    ]
    for i in range(1, 35):
        items.append(
            _entry(
                f"If ▲ + ▲ = {2 * i}, what is ▲?",
                str(i),
                f"2▲ = {2*i} → ▲ = {i}.",
                "logical_reasoning",
                "easy",
            )
        )
    return items


def _profit_loss() -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for cost in [40, 50, 80, 120, 200, 250, 400]:
        for margin in [10, 15, 20, 25, 30]:
            sp = round(cost * (100 + margin) / 100)
            items.append(
                _entry(
                    f"Cost price ${cost}, profit {margin}%. Selling price?",
                    f"${sp}",
                    f"SP = CP × (1 + {margin}/100) = {sp}.",
                    "profit_loss",
                    "medium",
                )
            )
    return items


def build_aptitude_questions() -> list[dict[str, Any]]:
    all_q: list[dict[str, Any]] = []
    all_q.extend(_number_series_questions())
    all_q.extend(_percentage_questions())
    all_q.extend(_ratio_questions())
    all_q.extend(_time_speed_distance())
    all_q.extend(_averages_questions())
    all_q.extend(_algebra_word_problems())
    all_q.extend(_probability_questions())
    all_q.extend(_logical_reasoning())
    all_q.extend(_profit_loss())
    return all_q
