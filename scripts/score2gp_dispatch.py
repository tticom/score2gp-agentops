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


def select_bootstrap(linux_user: str) -> str:
    if linux_user == "tticom-automation":
        return "score2gp_go_bootstrap.py"
    if linux_user in {"tticom-gov", "tticom-codex"}:
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
    helper = Path(__file__).with_name(select_bootstrap(linux_user))
    command = [
        sys.executable,
        os.fspath(helper),
        "--product", args.product,
        "--agentops", args.agentops,
        "--skills-repo", args.skills_repo,
    ]
    if helper.name == "score2gp_go_bootstrap.py" and args.json:
        command.append("--json")
    completed = subprocess.run(command)
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    try:
        main()
    except DispatchError as error:
        raise SystemExit(f"CONTINUATION_DISPATCH_FAILED: {error}") from error
