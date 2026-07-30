#!/usr/bin/env python3
"""Identity-aware Score2GP continuation dispatcher.

The human command word is deliberately not authoritative. The isolated Linux
worker identity selects the only role-specific bootstrap it may execute.
"""
from __future__ import annotations

import argparse
import getpass
import os
import subprocess
import sys
from pathlib import Path


class DispatchError(RuntimeError):
    pass


def synchronize_agentops_main(
    agentops: Path,
    runner: object = subprocess.run,
) -> None:
    def run_git(*args: str) -> str:
        result = runner(
            ["git", *args],
            cwd=agentops,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            detail = result.stderr.strip() or result.stdout.strip()
            raise DispatchError(f"git {' '.join(args)} failed: {detail}")
        return result.stdout.strip()

    if run_git("status", "--porcelain"):
        raise DispatchError(f"AgentOps checkout is dirty: {agentops}")
    run_git("fetch", "origin")
    run_git("switch", "main")
    run_git("merge", "--ff-only", "origin/main")


def select_bootstrap(linux_user: str) -> str:
    if linux_user == "tticom-automation":
        return "score2gp_go_bootstrap.py"
    if linux_user == "tticom-gov":
        return "score2gp_got_bootstrap.py"
    raise DispatchError(f"unsupported Score2GP worker identity: {linux_user}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Route Score2GP continuation to the worker's authorised role."
    )
    parser.add_argument("--agentops", default=".")
    parser.add_argument("--product", default="../score2gp")
    parser.add_argument("--skills-repo", default="../../agy-skills")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    linux_user = getpass.getuser()
    agentops = Path(args.agentops).resolve()
    product = Path(args.product).resolve()
    skills_repo = Path(args.skills_repo).resolve()
    synchronize_agentops_main(agentops)
    helper = agentops / "scripts" / select_bootstrap(linux_user)
    command = [
        sys.executable,
        os.fspath(helper),
        "--product", os.fspath(product),
        "--agentops", os.fspath(agentops),
        "--skills-repo", os.fspath(skills_repo),
    ]
    if helper.name == "score2gp_go_bootstrap.py" and args.json:
        command.append("--json")
    completed = subprocess.run(command, cwd=agentops)
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    try:
        main()
    except DispatchError as error:
        raise SystemExit(f"CONTINUATION_DISPATCH_FAILED: {error}") from error
