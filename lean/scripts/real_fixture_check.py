#!/usr/bin/env python3
"""Local real-fixture check for the product repository (maintainer machine only).

Runs the public suite and the private-fixture checks against a product checkout and
prints a SANITISED summary: step names, statuses, exit codes and counts. Raw output
is written to a log directory OUTSIDE the product repository and never printed, so
the summary is safe to paste into a PR.

Result and exit code:
    PASS           0  every required step ran and passed
    FAIL           1  a required step failed, or the product tree is dirty with --require-clean
    NOT_EVALUATED  2  fixtures missing or a required step could not run; NEVER a pass

A skipped test is reported as a count. With --fail-on-skips any skip in a pytest step
makes the result FAIL (use it on the maintainer machine, where nothing should skip).

Steps default to the commands in the product TESTING.md. Override with --config, a
JSON file: {"fixture_dir": "fixtures/private", "min_fixtures": 1,
"fixture_glob": "*.pdf", "steps": [{"name": "...", "argv": ["{python}", "..."],
"kind": "pytest|command|tracked-files", "required": true}]}.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

PASS, FAIL, NOT_EVALUATED = "PASS", "FAIL", "NOT_EVALUATED"
EXIT = {PASS: 0, FAIL: 1, NOT_EVALUATED: 2}

DEFAULT_CONFIG = {
    "fixture_dir": "fixtures/private",
    "fixture_glob": "*.pdf",
    "min_fixtures": 1,
    "steps": [
        {"name": "public-tests", "kind": "pytest", "argv": ["{python}", "-m", "pytest", "-q", "-p", "no:cacheprovider"], "required": True},
        {"name": "private-e2e-smoke", "kind": "command", "argv": ["{python}", "scripts/private_e2e_smoke.py"], "required": True},
        {"name": "private-gp-quality-audit", "kind": "command", "argv": ["{python}", "scripts/private_gp_quality_audit.py"], "required": True},
        {
            "name": "private-safety-invariant",
            "kind": "tracked-files",
            "paths": ["fixtures/private", "work"],
            "allowed": ["fixtures/private/.gitkeep"],
            "required": True,
        },
        {"name": "git-diff-check", "kind": "command", "argv": ["git", "diff", "--check"], "required": True},
    ],
}

COUNT_RE = re.compile(r"(\d+) (passed|failed|skipped|errors?|xfailed|xpassed|deselected)")


def parse_pytest_counts(text: str) -> dict[str, int]:
    """Parse the final pytest summary line into counts; empty when none is found."""
    counts: dict[str, int] = {}
    for line in reversed(text.strip().splitlines()):
        found = COUNT_RE.findall(line)
        if found and ("passed" in line or "failed" in line or "error" in line or "skipped" in line):
            for number, word in found:
                key = "errors" if word.startswith("error") else word
                counts[key] = counts.get(key, 0) + int(number)
            return counts
    return counts


def detect_python(product: Path, explicit: str | None) -> str:
    if explicit:
        return explicit
    for candidate in (".venv/Scripts/python.exe", ".venv/bin/python"):
        path = product / candidate
        if path.is_file():
            return str(path)
    return sys.executable


def git_out(product: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(product), *args], check=False, capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def fixture_status(product: Path, config: dict) -> tuple[bool, int]:
    directory = product / config["fixture_dir"]
    count = len(list(directory.glob(config["fixture_glob"]))) if directory.is_dir() else 0
    return count >= int(config.get("min_fixtures", 1)), count


def run_step(step: dict, product: Path, python: str, log_dir: Path, fail_on_skips: bool) -> dict:
    name = step["name"]
    required = bool(step.get("required", True))
    result: dict = {"name": name, "required": required, "status": NOT_EVALUATED}
    kind = step.get("kind", "command")

    if kind == "tracked-files":
        listed = git_out(product, "ls-files", *step["paths"]).splitlines()
        extra = sorted(set(listed) - set(step.get("allowed", [])))
        result.update(status=PASS if not extra else FAIL, tracked_unexpected=len(extra))
        return result

    argv = [a.replace("{python}", python) for a in step["argv"]]
    result["command"] = " ".join(Path(a).name if os.path.isabs(a) and i == 0 else a for i, a in enumerate(argv))
    env = dict(os.environ, PYTHONPATH=str(product), PYTHONIOENCODING="utf-8")
    start = time.time()
    try:
        proc = subprocess.run(argv, cwd=product, env=env, check=False, capture_output=True, text=True, encoding="utf-8", errors="replace")
    except OSError:
        result["detail"] = "could not start"
        return result
    result["seconds"] = round(time.time() - start, 1)
    result["exit_code"] = proc.returncode
    (log_dir / f"{name}.log").write_text(proc.stdout + "\n--- stderr ---\n" + proc.stderr, encoding="utf-8")

    status = PASS if proc.returncode == 0 else FAIL
    if kind == "pytest":
        counts = parse_pytest_counts(proc.stdout)
        result["counts"] = counts
        if not counts:
            status = NOT_EVALUATED if status == PASS else FAIL
            result["detail"] = "no pytest summary found"
        elif counts.get("passed", 0) == 0 and status == PASS:
            status = NOT_EVALUATED
            result["detail"] = "zero tests passed"
        if status == PASS and fail_on_skips and counts.get("skipped", 0) > 0:
            status = FAIL
            result["detail"] = "skips present with --fail-on-skips"
    result["status"] = status
    return result


def overall(results: list[dict], fixtures_ok: bool, dirty: bool, require_clean: bool) -> str:
    if require_clean and dirty:
        return FAIL
    required = [r for r in results if r["required"]]
    if any(r["status"] == FAIL for r in required):
        return FAIL
    if not fixtures_ok or any(r["status"] == NOT_EVALUATED for r in required):
        return NOT_EVALUATED
    return PASS


def run(product: Path, config: dict, python: str, log_dir: Path, fail_on_skips: bool, require_clean: bool) -> dict:
    fixtures_ok, fixture_count = fixture_status(product, config)
    dirty = bool(git_out(product, "status", "--porcelain=v1", "--untracked-files=no"))
    results = [run_step(s, product, python, log_dir, fail_on_skips) for s in config["steps"]]
    return {
        "result": overall(results, fixtures_ok, dirty, require_clean),
        "product_head": git_out(product, "rev-parse", "HEAD"),
        "tracked_tree_dirty": dirty,
        "fixtures_present": fixtures_ok,
        "fixture_count": fixture_count,
        "steps": results,
    }


def render_markdown(summary: dict) -> str:
    lines = [
        f"Real-fixture check: {summary['result']}",
        f"Product head: {summary['product_head']}",
        f"Fixtures present: {summary['fixtures_present']} ({summary['fixture_count']} files)",
        f"Tracked tree dirty: {summary['tracked_tree_dirty']}",
        "",
        "| step | status | exit | counts |",
        "|---|---|---|---|",
    ]
    for r in summary["steps"]:
        counts = ", ".join(f"{k}={v}" for k, v in r.get("counts", {}).items()) or r.get("detail", "")
        lines.append(f"| {r['name']} | {r['status']} | {r.get('exit_code', '-')} | {counts} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--product", type=Path, required=True, help="product repository checkout")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--python", help="interpreter for {python}; default: product .venv, else this one")
    parser.add_argument("--log-dir", type=Path, help="raw logs (default: a new temp dir outside the product)")
    parser.add_argument("--fail-on-skips", action="store_true")
    parser.add_argument("--require-clean", action="store_true", help="FAIL if tracked files are modified")
    parser.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    args = parser.parse_args(argv)

    product = args.product.resolve()
    if not (product / ".git").exists():
        print("NOT_A_PRODUCT_CHECKOUT", file=sys.stderr)
        return 64
    config = json.loads(args.config.read_text(encoding="utf-8")) if args.config else DEFAULT_CONFIG
    log_dir = (args.log_dir or Path(tempfile.mkdtemp(prefix="real-fixture-check-"))).resolve()
    if product in (log_dir, *log_dir.parents):
        print("LOG_DIR_INSIDE_PRODUCT refused: raw logs must stay outside the repository", file=sys.stderr)
        return 64
    log_dir.mkdir(parents=True, exist_ok=True)

    summary = run(product, config, detect_python(product, args.python), log_dir, args.fail_on_skips, args.require_clean)
    print(json.dumps(summary, indent=2) if args.json else render_markdown(summary))
    print(f"raw logs (local only): {log_dir}", file=sys.stderr)
    return EXIT[summary["result"]]


if __name__ == "__main__":
    sys.exit(main())
