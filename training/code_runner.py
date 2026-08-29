"""Sandboxed Python runner for mock interview coding questions."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


HARVEST_TIMEOUT_SECONDS = 2.5
MAX_CODE_CHARS = 20_000

# Minimal builtins for user solutions (no file/network/process access).
SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "float": float,
    "frozenset": frozenset,
    "int": int,
    "isinstance": isinstance,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "pow": pow,
    "print": print,
    "range": range,
    "reversed": reversed,
    "round": round,
    "set": set,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
    "True": True,
    "False": False,
    "None": None,
    "Exception": Exception,
    "ValueError": ValueError,
    "TypeError": TypeError,
    "KeyError": KeyError,
    "IndexError": IndexError,
    "StopIteration": StopIteration,
}


def _harness_source() -> str:
    """Python source executed in a child process."""
    return r'''
import json
import sys
from itertools import islice

SAFE_BUILTINS = {
    "abs": abs, "all": all, "any": any, "bool": bool, "dict": dict,
    "enumerate": enumerate, "float": float, "frozenset": frozenset,
    "int": int, "isinstance": isinstance, "len": len, "list": list,
    "max": max, "min": min, "pow": pow, "print": print, "range": range,
    "reversed": reversed, "round": round, "set": set, "sorted": sorted,
    "str": str, "sum": sum, "tuple": tuple, "zip": zip,
    "True": True, "False": False, "None": None,
    "Exception": Exception, "ValueError": ValueError, "TypeError": TypeError,
    "KeyError": KeyError, "IndexError": IndexError, "StopIteration": StopIteration,
    "map": map, "filter": filter,
    "__build_class__": __build_class__,
    "__name__": "__main__",
}

def main():
    payload = json.load(sys.stdin)
    code = payload["code"]
    fn_name = payload["function_name"]
    cases = payload["cases"]
    results = []

    globals_dict = {"__builtins__": SAFE_BUILTINS}
    try:
        compiled = compile(code, "<user>", "exec")
        exec(compiled, globals_dict, globals_dict)
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "error": f"Compile/runtime error: {type(exc).__name__}: {exc}",
            "results": [],
        }))
        return

    if fn_name not in globals_dict or not callable(globals_dict[fn_name]):
        print(json.dumps({
            "ok": False,
            "error": f"Function `{fn_name}` not found. Define it in your code.",
            "results": [],
        }))
        return

    fn = globals_dict[fn_name]

    for case in cases:
        name = case.get("name", "case")
        args = case.get("args", [])
        kwargs = case.get("kwargs", {})
        expected = case.get("expected")
        take = case.get("take")
        hidden = bool(case.get("hidden", False))
        try:
            got = fn(*args, **kwargs)
            if take is not None:
                got = list(islice(got, int(take)))
            got_cmp = _normalize(got)
            exp_cmp = _normalize(expected)
            passed = got_cmp == exp_cmp
            entry = {
                "name": name,
                "passed": passed,
                "hidden": hidden,
            }
            if not hidden:
                entry["expected"] = expected
                entry["got"] = got_cmp if _jsonable(got_cmp) else repr(got)
                entry["args"] = args
                entry["kwargs"] = kwargs
            if not passed and not hidden:
                entry["message"] = f"Expected {expected!r}, got {got!r}"
            elif not passed and hidden:
                entry["message"] = "Hidden test failed"
            results.append(entry)
        except Exception as exc:
            entry = {
                "name": name,
                "passed": False,
                "hidden": hidden,
                "message": f"{type(exc).__name__}: {exc}",
            }
            if not hidden:
                entry["expected"] = expected
                entry["args"] = args
                entry["kwargs"] = kwargs
            results.append(entry)

    print(json.dumps({"ok": True, "error": "", "results": results}))

def _jsonable(value):
    try:
        json.dumps(value)
        return True
    except Exception:
        return False

def _normalize(value):
    if isinstance(value, tuple):
        return [_normalize(v) for v in value]
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    return value

if __name__ == "__main__":
    main()
'''


def public_test_cases(test_cases: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    if not test_cases:
        return []
    return [c for c in test_cases if not c.get("hidden")]


def run_coding_tests(
    code: str,
    function_name: str,
    test_cases: list[dict[str, Any]],
    *,
    include_hidden: bool = False,
) -> dict[str, Any]:
    """
    Execute user code against test cases in a subprocess.

    Returns:
      {
        ok: bool,
        error: str,
        results: [...],
        passed: int,
        total: int,
        score: float  # 0–10
      }
    """
    code = (code or "").strip()
    if not code:
        return {
            "ok": False,
            "error": "Write some code before running tests.",
            "results": [],
            "passed": 0,
            "total": 0,
            "score": 0.0,
        }
    if len(code) > MAX_CODE_CHARS:
        return {
            "ok": False,
            "error": f"Code exceeds {MAX_CODE_CHARS} characters.",
            "results": [],
            "passed": 0,
            "total": 0,
            "score": 0.0,
        }
    if not function_name:
        return {
            "ok": False,
            "error": "This question has no runnable function configured.",
            "results": [],
            "passed": 0,
            "total": 0,
            "score": 0.0,
        }
    if not test_cases:
        return {
            "ok": False,
            "error": "No test cases configured for this question.",
            "results": [],
            "passed": 0,
            "total": 0,
            "score": 0.0,
        }

    cases = list(test_cases) if include_hidden else public_test_cases(test_cases)
    if not cases:
        cases = list(test_cases)

    payload = {
        "code": code,
        "function_name": function_name,
        "cases": cases,
    }

    with tempfile.TemporaryDirectory(prefix="dm_mock_") as tmp:
        harness_path = Path(tmp) / "harness.py"
        harness_path.write_text(_harness_source(), encoding="utf-8")
        try:
            proc = subprocess.run(
                [sys.executable, str(harness_path)],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=HARVEST_TIMEOUT_SECONDS,
                cwd=tmp,
            )
        except subprocess.TimeoutExpired:
            return {
                "ok": False,
                "error": "Execution timed out (2.5s). Check for infinite loops.",
                "results": [],
                "passed": 0,
                "total": len(cases),
                "score": 0.0,
            }

    if proc.returncode != 0 and not proc.stdout.strip():
        err = (proc.stderr or "Runner failed").strip()[:500]
        return {
            "ok": False,
            "error": err,
            "results": [],
            "passed": 0,
            "total": len(cases),
            "score": 0.0,
        }

    try:
        data = json.loads(proc.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {
            "ok": False,
            "error": "Could not parse runner output.",
            "results": [],
            "passed": 0,
            "total": len(cases),
            "score": 0.0,
        }

    results = data.get("results") or []
    passed = sum(1 for r in results if r.get("passed"))
    total = len(results)
    score = round((passed / total) * 10, 1) if total else 0.0
    return {
        "ok": bool(data.get("ok", True)) and not data.get("error"),
        "error": data.get("error") or "",
        "results": results,
        "passed": passed,
        "total": total,
        "score": score,
    }


def score_from_full_suite(code: str, function_name: str, test_cases: list[dict[str, Any]]) -> dict[str, Any]:
    """Run all tests including hidden ones for submit scoring."""
    return run_coding_tests(
        code, function_name, test_cases, include_hidden=True
    )
