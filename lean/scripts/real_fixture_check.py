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

Rules that keep it from reporting a false PASS:
  * A skipped test is NOT_EVALUATED, never a pass: any skip in a pytest step makes that
    step NOT_EVALUATED unless --allow-skips is given (then skips are reported as counts).
  * A pytest summary with failures or errors is FAIL even if the exit code was 0.
  * A step with a "summary" entry must also have produced a FRESH JSON result file with
    at least min_entries entries; a tool that exits 0 after processing nothing is
    NOT_EVALUATED.
  * A failed git query is NOT_EVALUATED, never an empty (clean) result.
  Scores that legitimately "fail cleanly" are counted and shown in the distribution but do
  not by themselves fail the check: compare the counts with the previous run.

Steps default to the commands in the product TESTING.md. Override with --config, a JSON
file: {"fixture_dir": "fixtures/private", "min_fixtures": 1, "fixture_glob": "*.pdf",
"steps": [{"name": "...", "argv": ["{python}", "..."], "kind": "pytest|command|tracked-files",
"required": true, "summary": {"file": "work/x.json", "min_entries": 1, "status_key": "k"}}]}.
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
        {
            "name": "private-e2e-smoke",
            "kind": "command",
            "argv": ["{python}", "scripts/private_e2e_smoke.py"],
            "required": True,
            "summary": {"file": "work/private_e2e_smoke_v0_1/private_e2e_summary.json", "status_key": "alignment_status"},
        },
        {
            "name": "private-gp-quality-audit",
            "kind": "command",
            "argv": ["{python}", "scripts/private_gp_quality_audit.py"],
            "required": True,
            "summary": {"file": "work/private_gp_quality_audit_v0_1/summary.json", "status_key": "pass_fail_status"},
        },
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


def git_out(product: Path, *args: str) -> str | None:
    """Stdout of a git command, or None when git failed (never confuse failure with empty output)."""
    result = subprocess.run(
        ["git", "-C", str(product), *args], check=False, capture_output=True, text=True, encoding="utf-8"
    )
    return result.stdout.strip() if result.returncode == 0 else None


def fixture_status(product: Path, config: dict) -> tuple[bool, int]:
    directory = product / config["fixture_dir"]
    count = len(list(directory.glob(config["fixture_glob"]))) if directory.is_dir() else 0
    return count >= int(config.get("min_fixtures", 1)), count


def check_summary(spec: dict, product: Path, started: float, default_min: int) -> tuple[bool, dict]:
    """Verify a step's JSON result file is fresh and non-trivial. Returns (ok, sanitised counts)."""
    path = product / spec["file"]
    if not path.is_file() or path.stat().st_mtime < started - 2:
        return False, {"summary": "missing or stale"}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False, {"summary": "unreadable"}
    if not isinstance(data, list):
        return False, {"summary": "unexpected shape"}
    info: dict = {"entries": len(data)}
    key = spec.get("status_key")
    if key:
        dist: dict[str, int] = {}
        for entry in data:
            value = str(entry.get(key, "missing")) if isinstance(entry, dict) else "missing"
            dist[value] = dist.get(value, 0) + 1
        info["by_" + key] = dist
    return len(data) >= int(spec.get("min_entries", default_min)), info


def run_step(step: dict, product: Path, python: str, log_dir: Path, allow_skips: bool, default_min: int = 1) -> dict:
    name = step["name"]
    required = bool(step.get("required", True))
    result: dict = {"name": name, "required": required, "status": NOT_EVALUATED}
    kind = step.get("kind", "command")

    if kind == "tracked-files":
        output = git_out(product, "ls-files", *step["paths"])
        if output is None:
            result["detail"] = "git ls-files failed"
            return result
        extra = sorted(set(output.splitlines()) - set(step.get("allowed", [])))
        result.update(status=PASS if not extra else FAIL, counts={"tracked_unexpected": len(extra)})
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
        elif counts.get("failed", 0) or counts.get("errors", 0):
            status = FAIL
            result["detail"] = "failures or errors in summary"
        elif counts.get("passed", 0) == 0 and status == PASS:
            status = NOT_EVALUATED
            result["detail"] = "zero tests passed"
        if status == PASS and counts.get("skipped", 0) > 0 and not allow_skips:
            status = NOT_EVALUATED
            result["detail"] = "skips present (a skip is not a pass; --allow-skips to accept)"
    if status == PASS and step.get("summary"):
        ok, info = check_summary(step["summary"], product, start, default_min)
        if "entries" in info:
            result["counts"] = {**result.get("counts", {}), "entries": info["entries"]}
        result["distribution"] = {k: v for k, v in info.items() if k.startswith("by_")}
        if not ok:
            status = NOT_EVALUATED
            result["detail"] = "no fresh result entries (" + str(info.get("summary", "too few")) + ")"
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


def run(product: Path, config: dict, python: str, log_dir: Path, allow_skips: bool, require_clean: bool) -> dict:
    fixtures_ok, fixture_count = fixture_status(product, config)
    status_out = git_out(product, "status", "--porcelain=v1", "--untracked-files=no")
    dirty = bool(status_out) if status_out is not None else True  # unknown counts as dirty
    min_entries = int(config.get("min_fixtures", 1))
    results = [run_step(s, product, python, log_dir, allow_skips, min_entries) for s in config["steps"]]
    return {
        "result": overall(results, fixtures_ok, dirty, require_clean),
        "product_head": git_out(product, "rev-parse", "HEAD") or "unknown",
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
        parts = [f"{k}={v}" for k, v in r.get("counts", {}).items()]
        for key, dist in r.get("distribution", {}).items():
            parts.append(key + ": " + ", ".join(f"{k}={v}" for k, v in sorted(dist.items())))
        if r.get("detail"):
            parts.append(r["detail"])
        lines.append(f"| {r['name']} | {r['status']} | {r.get('exit_code', '-')} | {'; '.join(parts)} |")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--product", type=Path, required=True, help="product repository checkout")
    parser.add_argument("--config", type=Path)
    parser.add_argument("--python", help="interpreter for {python}; default: product .venv, else this one")
    parser.add_argument("--log-dir", type=Path, help="raw logs (default: a new temp dir outside the product)")
    parser.add_argument("--allow-skips", action="store_true", help="report skips as counts instead of NOT_EVALUATED")
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

    summary = run(product, config, detect_python(product, args.python), log_dir, args.allow_skips, args.require_clean)
    print(json.dumps(summary, indent=2) if args.json else render_markdown(summary))
    print(f"raw logs (local only): {log_dir}", file=sys.stderr)
    return EXIT[summary["result"]]


if __name__ == "__main__":
    sys.exit(main())
