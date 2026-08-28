#!/usr/bin/env python3
"""Score2GP continuation dispatcher with Orca and legacy compatibility modes.

Orca mode consumes a deterministic live snapshot and emits a bounded assignment.
Legacy mode retains Linux-user routing during migration only.
"""
from __future__ import annotations

import argparse
import getpass
import json
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
    if linux_user in {"tticom-gov", "tticom-codex", "tticom"}:
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
    parser.add_argument("--review-repo")
    parser.add_argument("--review-pr", type=int)
    parser.add_argument("--review-level")
    parser.add_argument("--orca-role", choices=("implementation", "reviewer", "governance", "architect"))
    parser.add_argument("--live", type=Path)
    parser.add_argument("--github-login")
    parser.add_argument("--legacy", action="store_true")
    args = parser.parse_args()

    if args.orca_role:
        if args.legacy:
            raise DispatchError("--orca-role and --legacy are mutually exclusive")
        if args.live is None or not args.github_login:
            raise DispatchError("Orca dispatch requires --live and --github-login")
        try:
            from scripts.score2gp_orca_control import (
                RuntimeIdentity,
                ControlError,
                authenticated_github_login,
                build_assignment,
                git_head,
                load_json,
                resolve_state,
                validate_legacy_alignment,
            )
        except ModuleNotFoundError:
            from score2gp_orca_control import (
                RuntimeIdentity,
                ControlError,
                authenticated_github_login,
                build_assignment,
                git_head,
                load_json,
                resolve_state,
                validate_legacy_alignment,
            )
        agentops = Path(args.agentops).resolve()
        authority = load_json(agentops / "projects/score2gp/ORCHESTRATION_STATE.json")
        validate_legacy_alignment(
            authority,
            (agentops / "projects/score2gp/ACTIVE_TASK.md").read_text(encoding="utf-8"),
        )
        live = load_json(args.live)
        resolved = resolve_state(authority, live)
        if resolved.get("dispatch_role") != args.orca_role:
            raise DispatchError(
                f"resolver requires role {resolved.get('dispatch_role') or '<none>'}, "
                f"not {args.orca_role}; state={resolved['state']}"
            )
        login = authenticated_github_login()
        if args.github_login != login:
            raise DispatchError(
                f"expected GitHub login {args.github_login}, authenticated as {login}"
            )
        try:
            assignment = build_assignment(
                authority,
                live,
                resolved,
                RuntimeIdentity(getpass.getuser(), login),
                git_head(agentops),
            )
        except ControlError as error:
            raise DispatchError(str(error)) from error
        print(json.dumps(assignment, indent=2, sort_keys=True))
        return

    linux_user = getpass.getuser()
    if (args.review_repo is None) != (args.review_pr is None):
        raise DispatchError("--review-repo and --review-pr must be supplied together")
    if linux_user == "tticom-automation" and args.review_pr is not None:
        raise DispatchError(
            "tticom-automation cannot use explicit reviewer dispatch"
        )
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
    if args.review_pr is not None:
        command.extend([
            "--review-repo", str(args.review_repo),
            "--review-pr", str(args.review_pr),
        ])
    if args.review_level:
        command.extend(["--review-level", args.review_level])
    if helper.name == "score2gp_go_bootstrap.py" and args.json:
        command.append("--json")
    completed = subprocess.run(command, cwd=agentops)
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    try:
        main()
    except DispatchError as error:
        raise SystemExit(f"CONTINUATION_DISPATCH_FAILED: {error}") from error
