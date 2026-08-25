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
    except Exception as e:
        fail_closed(f"Failed to sync {name}: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Score2GP Agy `go` Dispatch Bootstrap Helper.")
    parser.add_argument("--product", type=str, default="../score2gp")
    parser.add_argument("--agentops", type=str, default=".")
    parser.add_argument("--skills-repo", type=str, default="../../agy-skills")
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
    repo = task.get("repository")
    pr = task.get("pull_request")

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        live_file = f.name

    try:
        if repo and pr:
            res = subprocess.run(
                [sys.executable, "scripts/score2gp_orca_control.py", "snapshot", "--repository", str(repo), "--pull-request", str(pr)],
                cwd=agentops, capture_output=True, text=True
            )
            if res.returncode != 0:
                fail_closed(f"Snapshot failed: {res.stderr.strip()}")
            with open(live_file, "w") as f:
                f.write(res.stdout)
        else:
            with open(live_file, "w") as f:
                f.write("{}")

        gh_user = subprocess.run(["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True)
        if gh_user.returncode != 0:
            fail_closed(f"GitHub identity check failed: {gh_user.stderr.strip()}")
        login = gh_user.stdout.strip()

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
