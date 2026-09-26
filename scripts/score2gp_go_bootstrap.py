#!/usr/bin/env python3
"""Score2GP Agy `go` Dispatch Bootstrap Helper.

Thin compatibility wrapper around the Orca shared resolver.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

TERMINAL_TASK_STATUSES = {"COMPLETED", "COMPLETE", "MERGED", "RESOLVED"}


def should_snapshot_task_pr(status: str) -> bool:
    return status.strip().upper() not in TERMINAL_TASK_STATUSES


def fail_closed(reason: str) -> None:
    if "--json" in sys.argv:
        print(json.dumps({"ok": False, "state": "FAIL_CLOSED", "reason": reason}, indent=2))
    else:
        print(f"ERROR: {reason}", file=sys.stderr)
    sys.exit(1)


def sync_main(cwd: Path, name: str) -> None:
    try:
        res = subprocess.run(["git", "status", "--porcelain"], cwd=cwd, capture_output=True, text=True, check=True)
        if res.stdout.strip():
            fail_closed(f"{name} repository is dirty. Commit or stash changes before dispatching.")
        subprocess.run(["git", "fetch", "origin", "main"], cwd=cwd, capture_output=True, text=True, check=True)
        subprocess.run(["git", "switch", "main"], cwd=cwd, capture_output=True, text=True, check=True)
        subprocess.run(["git", "merge", "--ff-only", "origin/main"], cwd=cwd, capture_output=True, text=True, check=True)
    except Exception as e:
        detail = getattr(e, "stderr", None) or str(e)
        fail_closed(f"Failed to sync {name}: {detail.strip()}")


def capture_task_live(agentops: Path, authority_path: Path) -> dict:
    """Live state for the active task: its recorded PR, or GOV-03 discovery when none is recorded."""
    res = subprocess.run(
        [sys.executable, "scripts/score2gp_orca_control.py", "task-live", "--authority", str(authority_path)],
        cwd=agentops, capture_output=True, text=True,
    )
    if res.returncode != 0:
        fail_closed(f"Live-state capture failed: {res.stderr.strip()}")
    try:
        live = json.loads(res.stdout)
    except json.JSONDecodeError:
        fail_closed("Live-state capture returned invalid JSON")
    if not isinstance(live, dict):
        fail_closed("Live-state capture did not return a JSON object")
    return live


def resolve_live(agentops: Path, authority_path: Path, live_file: str) -> dict:
    res = subprocess.run(
        [sys.executable, "scripts/score2gp_orca_control.py", "resolve", "--authority", str(authority_path), "--live", live_file],
        cwd=agentops, capture_output=True, text=True,
    )
    if res.returncode != 0:
        fail_closed(f"Resolve failed: {res.stderr.strip()}")
    return json.loads(res.stdout)


def main() -> None:
    parser = argparse.ArgumentParser(description="Score2GP Agy `go` Dispatch Bootstrap Helper.")
    parser.add_argument("--product", type=str, default="../score2gp")
    parser.add_argument("--agentops", type=str, default=".")
    parser.add_argument(
        "--skills-repo",
        type=Path,
        help="defaults to the agentops-claude-skills checkout beside --agentops",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    agentops = Path(args.agentops).resolve()
    product = Path(args.product).resolve()

    sync_main(agentops, "agentops")
    sync_main(product, "product")

    # Capture live state
    authority_path = agentops / "projects/score2gp/ORCHESTRATION_STATE.json"
    if not authority_path.exists():
        fail_closed(f"Missing authority: {authority_path}")

    with open(authority_path, encoding="utf-8") as f:
        auth = json.load(f)

    task = auth.get("task", {})

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        live_file = f.name

    try:
        gh_user = subprocess.run(["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True)
        if gh_user.returncode != 0:
            fail_closed(f"GitHub identity check failed: {gh_user.stderr.strip()}")
        login = gh_user.stdout.strip()

        if not should_snapshot_task_pr(str(task.get("status", ""))):
            if args.json:
                print(json.dumps({"ok": True, "state": "COMPLETE", "reason": "task_declared_complete", "task_id": task.get("id")}, indent=2))
            else:
                print(f"score2gp: task {task.get('id')} is complete; no dispatch required")
            return

        # Never "no PR" while one exists: an unrecorded PR is discovered on the task branch.
        with open(live_file, "w", encoding="utf-8") as f:
            json.dump(capture_task_live(agentops, authority_path), f)

        resolved = resolve_live(agentops, authority_path, live_file)
        if resolved.get("dispatch_role") != "implementation":
            if args.json:
                print(json.dumps({"ok": False, **resolved}, indent=2))
            else:
                print(f"score2gp: {resolved.get('state')} ({resolved.get('reason')}); no implementation dispatch", file=sys.stderr)
            sys.exit(1)

        cmd = [
            sys.executable, "scripts/score2gp_dispatch.py",
            "--agentops", str(agentops),
            "--product", str(product),
            "--orca-role", "implementation",
            "--live", live_file,
            "--github-login", login
        ]
        if args.json:
            cmd.append("--json")

        res = subprocess.run(cmd, cwd=agentops)
        sys.exit(res.returncode)
    finally:
        os.unlink(live_file)


if __name__ == "__main__":
    main()
