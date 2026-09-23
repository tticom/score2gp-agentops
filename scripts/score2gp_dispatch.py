#!/usr/bin/env python3
"""Score2GP continuation dispatcher with Orca and legacy compatibility modes.

Orca mode consumes a deterministic live snapshot and emits a bounded assignment.
Legacy mode routes by the authenticated GitHub login, cross-checked against the
workspace that owns the AgentOps checkout and the roles in the authority file.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from scripts.score2gp_control_plane import default_skills_repo
    from scripts.verify_identity import (
        IdentityError,
        verify_git_identity,
        verify_workspace_login,
    )
except ModuleNotFoundError:
    from score2gp_control_plane import default_skills_repo
    from verify_identity import IdentityError, verify_git_identity, verify_workspace_login


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


def _authenticated_login() -> str:
    try:
        from scripts.score2gp_orca_control import (
            ControlError,
            authenticated_github_login,
        )
    except ModuleNotFoundError:
        from score2gp_orca_control import ControlError, authenticated_github_login
    try:
        return authenticated_github_login()
    except OSError as error:
        raise DispatchError("GitHub identity check could not run") from error
    except ControlError as error:
        raise DispatchError(f"GitHub identity check failed: {error}") from error


def _role_logins(roles: dict[str, Any], role: str) -> set[str]:
    policy = roles.get(role)
    if not isinstance(policy, dict):
        return set()
    return set(policy.get("github_logins") or [])


def select_bootstrap(
    login: str,
    agentops: Path,
    roles: dict[str, Any],
    review_pr: int | None = None,
) -> str:
    """Select the bootstrap for an authenticated login in its own workspace.

    The login must own the workspace containing ``agentops``. An explicit
    review needs the reviewer role; otherwise the ``auto`` workspace runs the
    author bootstrap under the implementation role, and the ``gov`` and
    ``codex`` workspaces run the review/governance bootstrap.
    """
    try:
        slot = verify_workspace_login(login, agentops)
    except IdentityError as error:
        raise DispatchError(f"unsupported Score2GP worker identity: {error}") from error
    if review_pr is not None:
        if login not in _role_logins(roles, "reviewer"):
            raise DispatchError(f"unsupported Score2GP worker identity: {login} lacks the reviewer role")
        return "score2gp_got_bootstrap.py"
    if slot == "auto":
        if login not in _role_logins(roles, "implementation"):
            raise DispatchError(
                f"unsupported Score2GP worker identity: {login} lacks the implementation role"
            )
        return "score2gp_go_bootstrap.py"
    if login not in _role_logins(roles, "reviewer") | _role_logins(roles, "governance"):
        raise DispatchError(
            f"unsupported Score2GP worker identity: {login} lacks the reviewer and governance roles"
        )
    return "score2gp_got_bootstrap.py"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Route Score2GP continuation to the worker's authorised role."
    )
    parser.add_argument("--agentops", default=".")
    parser.add_argument("--product", default="../score2gp")
    parser.add_argument(
        "--skills-repo",
        type=Path,
        help="defaults to the agentops-claude-skills checkout beside --agentops",
    )
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--review-repo")
    parser.add_argument("--review-pr", type=int)
    parser.add_argument("--review-head")
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

    if (args.review_repo is None) != (args.review_pr is None):
        raise DispatchError("--review-repo and --review-pr must be supplied together")
    agentops = Path(args.agentops).resolve()
    product = Path(args.product).resolve()
    skills_repo = (args.skills_repo or default_skills_repo(agentops)).resolve()
    # Prove the identity before any write, then read roles from synced main.
    login = _authenticated_login()
    try:
        verify_workspace_login(login, agentops)
        verify_git_identity(login, agentops)
    except IdentityError as error:
        raise DispatchError(f"identity gate failed: {error}") from error
    synchronize_agentops_main(agentops)
    authority = json.loads(
        (agentops / "projects/score2gp/ORCHESTRATION_STATE.json").read_text(encoding="utf-8")
    )
    bootstrap = select_bootstrap(
        login, agentops, authority.get("roles", {}), review_pr=args.review_pr
    )
    helper = agentops / "scripts" / bootstrap
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
    if args.review_head:
        command.extend(["--review-head", args.review_head])
    if args.review_level:
        command.extend(["--review-level", args.review_level])
    if args.json:
        command.append("--json")
    completed = subprocess.run(command, cwd=agentops)
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    try:
        main()
    except DispatchError as error:
        raise SystemExit(f"CONTINUATION_DISPATCH_FAILED: {error}") from error
