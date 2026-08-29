"""Debugging practice — Beginner level (syntax and basic logic)."""

TOPICS = [
    {
        "question": "This greeting function never prints. Find and fix the syntax error.",
        "buggy_code": '''def greet(name)
    print(f"Hello, {name}!")

greet("Ada")''',
        "solution_code": '''def greet(name):  # colon required after function signature
    print(f"Hello, {name}!")

greet("Ada")''',
        "solution_explanation": "Python requires a colon after function definitions, class definitions, and control-flow headers.",
        "ideal_topics": "syntax, SyntaxError, function definition",
        "hints": "Read the traceback line number and look at the line above the caret.",
        "learning_objectives": "Recognize missing-colon SyntaxError in function headers",
        "time_estimate_minutes": 5,
    },
    {
        "question": "Fix the indentation so the message prints only when `active` is True.",
        "buggy_code": '''active = True

if active:
print("Service is running")''',
        "solution_code": '''active = True

if active:
    print("Service is running")  # body must be indented under the if block''',
        "solution_explanation": "Indented blocks define scope in Python; statements under `if` must be nested consistently.",
        "ideal_topics": "IndentationError, control flow, blocks",
        "hints": "The line after `if active:` must be indented with spaces or tabs.",
        "learning_objectives": "Fix IndentationError in conditional blocks",
        "time_estimate_minutes": 5,
    },
    {
        "question": "The login check always succeeds. Fix the comparison operator.",
        "buggy_code": '''password = input("Password: ")
if password = "secret123":
    print("Access granted")
else:
    print("Access denied")''',
        "solution_code": '''password = input("Password: ")
if password == "secret123":  # == compares; = assigns
    print("Access granted")
else:
    print("Access denied")''',
        "solution_explanation": "`=` assigns a value; `==` compares values. Using `=` in a condition causes a SyntaxError.",
        "ideal_topics": "comparison vs assignment, SyntaxError, conditionals",
        "hints": "Assignment inside `if` is invalid — you need a comparison operator.",
        "learning_objectives": "Distinguish assignment from equality comparison in conditions",
        "time_estimate_minutes": 5,
    },
    {
        "question": "Fix the NameError when computing the total price.",
        "buggy_code": '''unit_price = 9.99
quantity = 3
total = unit_price * qantity
print(total)''',
        "solution_code": '''unit_price = 9.99
quantity = 3
total = unit_price * quantity  # variable name must match exactly
print(total)''',
        "solution_explanation": "Python resolves names at runtime; a typo in a variable name raises NameError.",
        "ideal_topics": "NameError, variable scope, typos",
        "hints": "Compare every identifier on the right-hand side with earlier assignments.",
        "learning_objectives": "Trace NameError to misspelled variable names",
        "time_estimate_minutes": 5,
    },
    {
        "question": "Fix the TypeError when building a user label.",
        "buggy_code": '''user_id = 42
label = "User #" + user_id
print(label)''',
        "solution_code": '''user_id = 42
label = "User #" + str(user_id)  # convert int before concatenating strings
print(label)''',
        "solution_explanation": "The `+` operator on strings expects another string; convert non-string values explicitly.",
        "ideal_topics": "TypeError, str(), type coercion",
        "hints": "Can you concatenate a string and an integer directly in Python?",
        "learning_objectives": "Fix type mismatch errors when combining strings and numbers",
        "time_estimate_minutes": 6,
    },
    {
        "question": "The loop should print 1 through 5 but stops early. Fix the range bounds.",
        "buggy_code": '''for i in range(1, 5):
    print(i)''',
        "solution_code": '''for i in range(1, 6):  # range stop is exclusive
    print(i)''',
        "solution_explanation": "`range(start, stop)` excludes `stop`, so `range(1, 5)` yields 1–4.",
        "ideal_topics": "range(), off-by-one, loops",
        "hints": "Remember that the upper bound in `range` is not included.",
        "learning_objectives": "Correct off-by-one errors with range stop values",
        "time_estimate_minutes": 6,
    },
    {
        "question": "Fix the function so callers receive the doubled value.",
        "buggy_code": '''def double(n):
    result = n * 2

print(double(10))''',
        "solution_code": '''def double(n):
    result = n * 2
    return result  # return value to caller

print(double(10))''',
        "solution_explanation": "Without `return`, a function implicitly returns `None`.",
        "ideal_topics": "return statement, None, functions",
        "hints": "What does a function return if there is no `return` statement?",
        "learning_objectives": "Ensure functions return computed results to callers",
        "time_estimate_minutes": 6,
    },
    {
        "question": "Fix the IndexError when accessing the last element.",
        "buggy_code": '''items = ["apple", "banana", "cherry"]
last = items[3]
print(last)''',
        "solution_code": '''items = ["apple", "banana", "cherry"]
last = items[-1]  # valid indices are 0..len-1; -1 is the last element
print(last)''',
        "solution_explanation": "Valid indices for a length-n list are `0` through `n-1`. Index `3` is out of range for three items.",
        "ideal_topics": "IndexError, list indexing, negative indices",
        "hints": "How many elements are in the list, and are indices zero-based?",
        "learning_objectives": "Fix out-of-range list index access",
        "time_estimate_minutes": 6,
    },
    {
        "question": "The sum helper returns 0 for every input. Fix the logic bug.",
        "buggy_code": '''def sum_positive(numbers):
    total = 0
    for n in numbers:
        if n > 0:
            total = n  # should accumulate, not replace
    return total

print(sum_positive([1, 2, 3]))''',
        "solution_code": '''def sum_positive(numbers):
    total = 0
    for n in numbers:
        if n > 0:
            total += n  # accumulate positive values
    return total

print(sum_positive([1, 2, 3]))  # 6''',
        "solution_explanation": "Assigning `total = n` overwrites the accumulator instead of adding to it.",
        "ideal_topics": "accumulation, loops, assignment vs update",
        "hints": "Use `+=` to add each positive number to a running total.",
        "learning_objectives": "Debug incorrect accumulator updates in loops",
        "time_estimate_minutes": 7,
    },
    {
        "question": "Fix the boolean condition so access is granted for admin OR owner roles.",
        "buggy_code": '''role = "owner"
if role == "admin" and role == "owner":
    print("Access granted")
else:
    print("Access denied")''',
        "solution_code": '''role = "owner"
if role == "admin" or role == "owner":  # either role should grant access
    print("Access granted")
else:
    print("Access denied")''',
        "solution_explanation": "A single value cannot equal two different strings at once; use `or` for alternative conditions.",
        "ideal_topics": "boolean logic, and vs or, conditionals",
        "hints": "Can one variable simultaneously equal both `'admin'` and `'owner'`?",
        "learning_objectives": "Choose correct boolean operators for multi-condition checks",
        "time_estimate_minutes": 7,
    },
    {
        "question": "Fix the SyntaxError in the function call.",
        "buggy_code": '''def area(width, height):
    return width * height

print(area(4, 5''',
        "solution_code": '''def area(width, height):
    return width * height

print(area(4, 5))  # close both the call and the print parentheses''',
        "solution_explanation": "Unclosed parentheses cause Python to reach EOF while still parsing an expression.",
        "ideal_topics": "SyntaxError, parentheses matching, function calls",
        "hints": "Count opening and closing parentheses on the last line.",
        "learning_objectives": "Resolve unclosed-parenthesis syntax errors",
        "time_estimate_minutes": 5,
    },
    {
        "question": "Fix operator precedence so the average of a and b is computed correctly.",
        "buggy_code": '''a = 10
b = 20
average = a + b / 2
print(average)  # expected 15.0''',
        "solution_code": '''a = 10
b = 20
average = (a + b) / 2  # division binds tighter than addition without parentheses
print(average)  # 15.0''',
        "solution_explanation": "Division has higher precedence than addition, so `a + b / 2` evaluates as `a + (b / 2)`.",
        "ideal_topics": "operator precedence, arithmetic, parentheses",
        "hints": "Which operation runs first: addition or division?",
        "learning_objectives": "Use parentheses to express intended arithmetic order",
        "time_estimate_minutes": 6,
    },
    {
        "question": "Fix the empty-list check so an empty cart is detected correctly.",
        "buggy_code": '''cart = []

if cart == None:
    print("Cart is empty")
else:
    print(f"{len(cart)} items")''',
        "solution_code": '''cart = []

if not cart:  # empty list is falsy; use truthiness, not None comparison
    print("Cart is empty")
else:
    print(f"{len(cart)} items")''',
        "solution_explanation": "An empty list is not `None`; it is falsy, so `not cart` is the idiomatic empty check.",
        "ideal_topics": "truthiness, None vs empty, conditionals",
        "hints": "Is `[]` the same object as `None`?",
        "learning_objectives": "Differentiate None checks from empty-collection checks",
        "time_estimate_minutes": 7,
    },
    {
        "question": "Fix the comparison so numeric strings sort correctly as numbers.",
        "buggy_code": '''scores = ["10", "2", "30"]
scores.sort()
print(scores[0])  # expected smallest numeric score: 2''',
        "solution_code": '''scores = ["10", "2", "30"]
scores.sort(key=int)  # sort by integer value, not lexicographic string order
print(scores[0])  # "2"''',
        "solution_explanation": "Default string sort is lexicographic, so `'10'` comes before `'2'`.",
        "ideal_topics": "sorting, key function, string vs int comparison",
        "hints": "How does Python compare `'10'` and `'2'` as strings?",
        "learning_objectives": "Fix incorrect default sorting of numeric strings",
        "time_estimate_minutes": 8,
    },
    {
        "question": "Fix the loop so searching stops as soon as the target is found.",
        "buggy_code": '''numbers = [3, 7, 2, 9, 5]
target = 9
found = False

for n in numbers:
    if n == target:
        found = True
    break  # breaks after first iteration regardless of match

print(found)''',
        "solution_code": '''numbers = [3, 7, 2, 9, 5]
target = 9
found = False

for n in numbers:
    if n == target:
        found = True
        break  # stop only after a match

print(found)  # True''',
        "solution_explanation": "`break` must live inside the matching branch; placing it outside exits after the first element.",
        "ideal_topics": "break, loop control, search",
        "hints": "Which statement should run only when a match is found?",
        "learning_objectives": "Place break statements in the correct control-flow branch",
        "time_estimate_minutes": 7,
    },
    {
        "question": "Fix the continue logic so negative numbers are skipped but positives are summed.",
        "buggy_code": '''values = [4, -1, 3, -2, 5]
total = 0

for v in values:
    if v < 0:
        continue
    total += v
    continue  # skips remaining logic every iteration

print(total)''',
        "solution_code": '''values = [4, -1, 3, -2, 5]
total = 0

for v in values:
    if v < 0:
        continue  # skip negatives only
    total += v

print(total)  # 12''',
        "solution_explanation": "An unconditional `continue` after accumulation prevents normal loop progression from doing useful work on positives.",
        "ideal_topics": "continue, loops, filtering",
        "hints": "Should every iteration hit `continue`, or only negative values?",
        "learning_objectives": "Use continue only when skipping unwanted iterations",
        "time_estimate_minutes": 7,
    },
    {
        "question": "Fix the grade classifier so B grades are reported correctly.",
        "buggy_code": '''score = 85

if score >= 90:
    grade = "A"
if score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(grade)  # expected B for score 85''',
        "solution_code": '''score = 85

if score >= 90:
    grade = "A"
elif score >= 80:  # elif chain prevents later branches from overwriting
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(grade)  # B''',
        "solution_explanation": "A standalone `if` after an earlier match can still run and overwrite the result; use `elif` for mutually exclusive branches.",
        "ideal_topics": "if/elif/else, control flow, chained conditions",
        "hints": "After assigning `'A'`, does another independent `if score >= 80` still execute?",
        "learning_objectives": "Build mutually exclusive conditional chains with elif",
        "time_estimate_minutes": 8,
    },
    {
        "question": "Fix the division so zero quantities are handled safely.",
        "buggy_code": '''total_cost = 100
quantity = 0
unit_cost = total_cost / quantity
print(unit_cost)''',
        "solution_code": '''total_cost = 100
quantity = 0

if quantity == 0:
    unit_cost = 0  # or raise a meaningful error for invalid input
else:
    unit_cost = total_cost / quantity

print(unit_cost)''',
        "solution_explanation": "Division by zero raises ZeroDivisionError; guard against invalid denominators first.",
        "ideal_topics": "ZeroDivisionError, input validation, defensive coding",
        "hints": "What happens when you divide by zero in Python?",
        "learning_objectives": "Prevent ZeroDivisionError with pre-checks",
        "time_estimate_minutes": 7,
    },
    {
        "question": "Fix the dictionary lookup so missing keys do not crash the program.",
        "buggy_code": '''settings = {"theme": "dark", "lang": "en"}
font = settings["font"]
print(font)''',
        "solution_code": '''settings = {"theme": "dark", "lang": "en"}
font = settings.get("font", "sans-serif")  # safe default when key is absent
print(font)''',
        "solution_explanation": "Subscript access raises KeyError for missing keys; `dict.get()` returns a default instead.",
        "ideal_topics": "KeyError, dict.get, defaults",
        "hints": "Is the 'font' key guaranteed to exist in the dictionary?",
        "learning_objectives": "Handle missing dictionary keys without KeyError",
        "time_estimate_minutes": 7,
    },
    {
        "question": "Fix the slice so the first three elements are returned.",
        "buggy_code": '''data = [10, 20, 30, 40, 50]
first_three = data[1:3]
print(first_three)  # expected [10, 20, 30]''',
        "solution_code": '''data = [10, 20, 30, 40, 50]
first_three = data[:3]  # slice end is exclusive; start at 0 for first three
print(first_three)  # [10, 20, 30]''',
        "solution_explanation": "Slice `[1:3]` returns indices 1 and 2 only; `[0:3]` or `[:3]` returns the first three elements.",
        "ideal_topics": "slicing, off-by-one, sequences",
        "hints": "Remember slice start is inclusive and stop is exclusive.",
        "learning_objectives": "Correct slice bounds for subsequence extraction",
        "time_estimate_minutes": 7,
    },
]
