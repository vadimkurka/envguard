"""Structural checks for .env and .env.example; never execute or echo values."""

from difflib import get_close_matches
from pathlib import Path
import re
import sys

_KEY = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
_QUOTED = re.compile(r"^(['\"])(.*)\1(?:\s+#.*)?$", re.DOTALL)


def _read_env(path):
    """Return key -> value and safe diagnostics (no secret values or lines)."""
    values = {}
    errors = []
    try:
        lines = Path(path).read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        return values, [f"Cannot read {path}: {type(exc).__name__}"]

    for number, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        if "=" not in line:
            errors.append(f"{path}:{number}: expected KEY=VALUE")
            continue
        key, value = (part.strip() for part in line.split("=", 1))
        if not _KEY.fullmatch(key):
            errors.append(f"{path}:{number}: invalid variable name")
            continue
        if key in values:
            errors.append(f"{path}:{number}: duplicate key {key}")
            continue

        if value.startswith(("'", '"')):
            quoted = _QUOTED.fullmatch(value)
            if not quoted:
                errors.append(f"{path}:{number}: malformed quoted value for {key}")
                continue
            value = quoted.group(2)
        else:
            value = "" if value.startswith("#") else value.split(" #", 1)[0].rstrip()
        values[key] = value
    return values, errors


def run_check(env_path, example_path, out=None):
    """Compare structural keys; return True when no issues were found."""
    if out is None:
        out = sys.stdout
    env, errors = _read_env(env_path)
    example, other_errors = _read_env(example_path)
    errors.extend(other_errors)
    missing = sorted(set(example) - set(env))
    undocumented = sorted(set(env) - set(example))
    empty = sorted(key for key, val in env.items() if not val.strip())
    typos = []
    for key in undocumented:
        near = get_close_matches(key, missing, n=1, cutoff=0.76)
        if near:
            typos.append((key, near[0]))

    issue_count = len(errors) + len(missing) + len(undocumented) + len(empty) + len(typos)
    if errors:
        print("Input errors:", *[f"  - {msg}" for msg in errors], sep="\n", file=out)
    for label, entries in (("Missing variables", missing),
                           ("Undocumented variables", undocumented),
                           ("Empty values", empty)):
        if entries:
            print(label + ":", *[f"  - {key}" for key in entries], sep="\n", file=out)
    if typos:
        print("Possible typos:", *[f"  - {a} -> {b}" for a, b in typos], sep="\n", file=out)
    print(f"{'PASS' if not issue_count else 'FAIL'}: {issue_count} issue(s).", file=out)
    return issue_count == 0
