"""Debugging practice — Easy level (common Python pitfalls)."""

TOPICS = [
    {
        "question": "Fix the mutable default argument bug that causes shared state across calls.",
        "buggy_code": '''def add_item(item, bucket=[]):
    bucket.append(item)
    return bucket

print(add_item("a"))
print(add_item("b"))  # expected ['b'], got ['a', 'b']''',
        "solution_code": '''def add_item(item, bucket=None):
    if bucket is None:
        bucket = []  # new list per call
    bucket.append(item)
    return bucket

print(add_item("a"))   # ['a']
print(add_item("b"))   # ['b']''',
        "solution_explanation": "Default arguments are evaluated once at definition time; mutable defaults are shared across calls.",
        "ideal_topics": "mutable default arguments, function defaults, shared state",
        "hints": "Use `None` as the default and create a fresh list inside the function.",
        "learning_objectives": "Identify and fix the mutable default argument antipattern",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Fix the closure so each button callback prints its own index.",
        "buggy_code": '''def make_handlers():
    handlers = []
    for i in range(3):
        handlers.append(lambda: print(i))
    return handlers

for fn in make_handlers():
    fn()  # prints 2, 2, 2 — expected 0, 1, 2''',
        "solution_code": '''def make_handlers():
    handlers = []
    for i in range(3):
        handlers.append(lambda i=i: print(i))  # bind i at definition time
    return handlers

for fn in make_handlers():
    fn()  # 0, 1, 2''',
        "solution_explanation": "Closures capture variables by reference; late binding makes all lambdas see the final loop value.",
        "ideal_topics": "closures, late binding, default argument binding",
        "hints": "Capture the loop variable in a default parameter: `lambda i=i: ...`.",
        "learning_objectives": "Fix late-binding closure bugs in loop-created callbacks",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix the None check so missing optional values are detected correctly.",
        "buggy_code": '''def find_user(user_id):
    user = None
    if user_id == 1:
        user = {"name": "Ada"}
    return user

result = find_user(99)
if result == False:
    print("Not found")
else:
    print("Found")''',
        "solution_code": '''def find_user(user_id):
    user = None
    if user_id == 1:
        user = {"name": "Ada"}
    return user

result = find_user(99)
if result is None:  # use `is None` for singleton None
    print("Not found")
else:
    print("Found")''',
        "solution_explanation": "`None` is a singleton; compare with `is None`. `== False` does not detect a missing user.",
        "ideal_topics": "None checks, identity, boolean pitfalls",
        "hints": "What value does the function return when no user matches?",
        "learning_objectives": "Use idiomatic None checks instead of falsey comparisons",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Fix the file handling so the handle is always closed.",
        "buggy_code": '''def read_config(path):
    f = open(path, encoding="utf-8")
    data = f.read()
    if "debug" not in data:
        raise ValueError("missing debug flag")
    return data

read_config("app.cfg")''',
        "solution_code": '''def read_config(path):
    with open(path, encoding="utf-8") as f:  # context manager closes file
        data = f.read()
    if "debug" not in data:
        raise ValueError("missing debug flag")
    return data''',
        "solution_explanation": "If an exception occurs before `close()`, the file handle leaks; `with` guarantees cleanup.",
        "ideal_topics": "file I/O, context managers, resource leaks",
        "hints": "Use a `with` statement around `open()`.",
        "learning_objectives": "Prevent file descriptor leaks with context managers",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Fix the exception handler so real errors are not silently swallowed.",
        "buggy_code": '''def parse_age(raw):
    try:
        return int(raw)
    except:
        return 0

print(parse_age("twenty"))  # returns 0 — hides ValueError details''',
        "solution_code": '''def parse_age(raw):
    try:
        return int(raw)
    except ValueError:  # catch only expected conversion failures
        return 0

print(parse_age("twenty"))  # 0''',
        "solution_explanation": "Bare `except` catches all exceptions including KeyboardInterrupt and masks unexpected bugs.",
        "ideal_topics": "exception handling, bare except, ValueError",
        "hints": "Catch the specific exception raised by `int()` on invalid input.",
        "learning_objectives": "Replace bare except with targeted exception types",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Fix enumerate usage so both index and value are printed correctly.",
        "buggy_code": '''items = ["alpha", "beta", "gamma"]
for i, item in enumerate(items, start=0):
    print(i, items[i + 1])  # IndexError on last item''',
        "solution_code": '''items = ["alpha", "beta", "gamma"]
for i, item in enumerate(items):
    print(i, item)  # use the value from enumerate directly''',
        "solution_explanation": "You already have the element from enumerate; indexing `i + 1` walks past the end.",
        "ideal_topics": "enumerate, IndexError, iteration",
        "hints": "Why index into the list again when enumerate yields the value?",
        "learning_objectives": "Use enumerate return values instead of manual indexing",
        "time_estimate_minutes": 9,
    },
    {
        "question": "Fix the sorting call so the original list is sorted in place.",
        "buggy_code": '''scores = [30, 10, 20]
sorted(scores)
print(scores)  # expected [10, 20, 30]''',
        "solution_code": '''scores = [30, 10, 20]
scores.sort()  # sort in place; sorted() returns a new list
print(scores)  # [10, 20, 30]''',
        "solution_explanation": "`sorted()` returns a new list and leaves the original unchanged; `.sort()` mutates in place.",
        "ideal_topics": "sorted vs sort, mutability, list methods",
        "hints": "Did you capture the return value of `sorted()`?",
        "learning_objectives": "Choose between sorted() and list.sort() correctly",
        "time_estimate_minutes": 8,
    },
    {
        "question": "Fix the shallow copy bug that lets nested list mutations leak between objects.",
        "buggy_code": '''import copy

original = [[1], [2]]
clone = copy.copy(original)
clone[0].append(99)
print(original)  # expected [[1], [2]]''',
        "solution_code": '''import copy

original = [[1], [2]]
clone = copy.deepcopy(original)  # deep copy nested lists
clone[0].append(99)
print(original)  # [[1], [2]]''',
        "solution_explanation": "Shallow copy duplicates outer list references; inner lists remain shared.",
        "ideal_topics": "copy vs deepcopy, nested mutability, aliasing",
        "hints": "Are inner lists copied, or only the outer container?",
        "learning_objectives": "Select deepcopy when nested mutable structures must be independent",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix the f-string so the literal braces render correctly.",
        "buggy_code": '''name = "Ada"
message = f"Hello {name} from {team}"
print(message)''',
        "solution_code": '''name = "Ada"
team = "platform"
message = f"Hello {name} from {team}"  # define missing variable
print(message)''',
        "solution_explanation": "Every `{expression}` in an f-string must refer to a defined name or expression.",
        "ideal_topics": "f-strings, NameError, string formatting",
        "hints": "Which name inside braces is undefined?",
        "learning_objectives": "Resolve NameError in f-string expressions",
        "time_estimate_minutes": 8,
    },
    {
        "question": "Fix the loop that skips elements while removing duplicates in place.",
        "buggy_code": '''values = [1, 2, 2, 3, 3, 3]
for i, v in enumerate(values):
    if i > 0 and v == values[i - 1]:
        values.pop(i)
print(values)  # unpredictable due to mutation during iteration''',
        "solution_code": '''values = [1, 2, 2, 3, 3, 3]
values = [v for i, v in enumerate(values) if i == 0 or v != values[i - 1]]
print(values)  # [1, 2, 3]''',
        "solution_explanation": "Mutating a list while iterating shifts indices and skips elements.",
        "ideal_topics": "mutation during iteration, list comprehension, deduplication",
        "hints": "Build a new list or iterate over a copy instead of popping during traversal.",
        "learning_objectives": "Avoid modifying a collection while iterating over it",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix the global counter so increments persist across function calls.",
        "buggy_code": '''counter = 0

def increment():
    counter += 1

increment()
print(counter)  # expected 1''',
        "solution_code": '''counter = 0

def increment():
    global counter
    counter += 1  # declare global before rebinding

increment()
print(counter)  # 1''',
        "solution_explanation": "Assignment inside a function creates a local variable unless `global` is declared.",
        "ideal_topics": "global keyword, UnboundLocalError, scope",
        "hints": "Does Python treat `counter += 1` as local assignment?",
        "learning_objectives": "Fix UnboundLocalError when mutating module-level state",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Fix dict.get usage so the default is not a shared mutable object.",
        "buggy_code": '''def add_tag(record, tag):
    tags = record.get("tags", [])
    tags.append(tag)
    return record

r1 = add_tag({}, "urgent")
r2 = add_tag({}, "review")
print(r2)  # expected {'tags': ['review']}''',
        "solution_code": '''def add_tag(record, tag):
    tags = record.get("tags")
    if tags is None:
        tags = []
    tags = list(tags)  # copy if present; fresh list if missing
    tags.append(tag)
    record["tags"] = tags
    return record''',
        "solution_explanation": "The default `[]` in `get()` is reused across calls, leaking tags between records.",
        "ideal_topics": "dict.get defaults, mutable defaults, side effects",
        "hints": "Is the default list created once or per call?",
        "learning_objectives": "Avoid shared mutable defaults in dict.get",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix datetime usage so elapsed time is computed in the same timezone.",
        "buggy_code": '''from datetime import datetime, timezone

start = datetime.now()
end = datetime.now(timezone.utc)
elapsed = end - start  # TypeError or wrong result''',
        "solution_code": '''from datetime import datetime, timezone

start = datetime.now(timezone.utc)
end = datetime.now(timezone.utc)  # both aware UTC datetimes
elapsed = end - start''',
        "solution_explanation": "Mixing naive and aware datetimes causes TypeError or incorrect deltas.",
        "ideal_topics": "datetime, timezone-aware, naive vs aware",
        "hints": "Are both datetimes timezone-aware?",
        "learning_objectives": "Keep datetime arithmetic within consistent timezone semantics",
        "time_estimate_minutes": 11,
    },
    {
        "question": "Fix the regex so it matches the full email domain, not a partial prefix.",
        "buggy_code": '''import re

email = "user@mail.example.com"
match = re.search(r"user@mail", email)
domain = match.group(0)
print(domain)  # expected full domain extraction''',
        "solution_code": '''import re

email = "user@mail.example.com"
match = re.search(r"@([\\w.-]+)", email)
domain = match.group(1) if match else ""
print(domain)  # mail.example.com''',
        "solution_explanation": "Greedy/literal patterns may match too little; capture groups extract the intended segment.",
        "ideal_topics": "regular expressions, capture groups, re.search",
        "hints": "Use a group to capture everything after `@`.",
        "learning_objectives": "Extract structured substrings with regex capture groups",
        "time_estimate_minutes": 12,
    },
    {
        "question": "Fix path joining so files resolve correctly on all platforms.",
        "buggy_code": '''base = "/var/app"
filename = "logs/access.log"
path = base + "/" + filename
backup = base + "backup/" + filename  # missing separator
print(backup)''',
        "solution_code": '''from pathlib import Path

base = Path("/var/app")
filename = "logs/access.log"
path = base / filename
backup = base / "backup" / filename  # pathlib inserts separators safely
print(backup)''',
        "solution_explanation": "String concatenation is error-prone for paths; `Path` handles separators portably.",
        "ideal_topics": "pathlib, path joining, portability",
        "hints": "Use `/` operator on `Path` objects instead of manual slashes.",
        "learning_objectives": "Build filesystem paths with pathlib instead of string concat",
        "time_estimate_minutes": 10,
    },
    {
        "question": "Fix JSON loading from a file handle.",
        "buggy_code": '''import json

with open("config.json", encoding="utf-8") as fh:
    data = json.loads(fh)  # TypeError: expected str, bytes, or bytearray''',
        "solution_code": '''import json

with open("config.json", encoding="utf-8") as fh:
    data = json.load(fh)  # load reads from file object; loads parses string''',
        "solution_explanation": "`json.loads()` parses a string; `json.load()` reads from a file-like object.",
        "ideal_topics": "json.load vs loads, file objects, TypeError",
        "hints": "Are you passing a file handle or string to the JSON parser?",
        "learning_objectives": "Choose json.load vs json.loads based on input type",
        "time_estimate_minutes": 9,
    },
    {
        "question": "Fix the script entry point so utility code does not run on import.",
        "buggy_code": '''def main():
    print("Running batch job")

main()  # runs even when this file is imported elsewhere''',
        "solution_code": '''def main():
    print("Running batch job")

if __name__ == "__main__":
    main()  # execute only when run as a script''',
        "solution_explanation": "Top-level calls execute on import; guard script logic with the main guard.",
        "ideal_topics": "__name__, __main__, import side effects",
        "hints": "What is `__name__` when the file is imported vs executed directly?",
        "learning_objectives": "Prevent import-time side effects with if __name__ == '__main__'",
        "time_estimate_minutes": 9,
    },
    {
        "question": "Fix integer division so average rating keeps fractional precision.",
        "buggy_code": '''total = 7
count = 2
average = total // count
print(average)  # expected 3.5, got 3''',
        "solution_code": '''total = 7
count = 2
average = total / count  # true division returns float
print(average)  # 3.5''',
        "solution_explanation": "`//` is floor division for integers; `/` performs true division and returns a float.",
        "ideal_topics": "floor division, true division, numeric types",
        "hints": "Which operator preserves fractional results?",
        "learning_objectives": "Select correct division operator for intended numeric result",
        "time_estimate_minutes": 8,
    },
    {
        "question": "Fix set deduplication that fails because lists are unhashable.",
        "buggy_code": '''pairs = [(1, "a"), (2, "b"), (1, "a")]
unique = set(pairs)
print(len(unique))''',
        "solution_code": '''pairs = [(1, "a"), (2, "b"), (1, "a")]
unique = set(pairs)  # tuples are hashable — bug is elsewhere if using lists

# If pairs contained lists:
pairs = [[1, "a"], [2, "b"], [1, "a"]]
unique = {tuple(p) for p in pairs}  # convert to hashable tuples
print(len(unique))  # 2''',
        "solution_explanation": "Set elements must be hashable; lists are mutable and unhashable, while tuples work.",
        "ideal_topics": "hashability, set, TypeError, tuples",
        "hints": "Can mutable lists be inserted into a set?",
        "learning_objectives": "Diagnose unhashable type errors when building sets",
        "time_estimate_minutes": 11,
    },
    {
        "question": "Fix chained comparison that accidentally checks the wrong middle value.",
        "buggy_code": '''score = 75
passed = 60 < score < 50  # impossible condition
print(passed)  # expected True for score between 60 and 100''',
        "solution_code": '''score = 75
passed = 60 < score <= 100  # chained comparisons must be simultaneously true
print(passed)  # True''',
        "solution_explanation": "`a < b < c` means `(a < b) and (b < c)`; the upper bound must exceed the lower bound.",
        "ideal_topics": "chained comparisons, boolean logic, range checks",
        "hints": "Can any number be both greater than 60 and less than 50?",
        "learning_objectives": "Write valid chained comparisons for numeric ranges",
        "time_estimate_minutes": 9,
    },
]
