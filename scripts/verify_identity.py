#!/usr/bin/env python3
"""Portable Score2GP identity gate.

The worker identity is the authenticated GitHub login. It must match the
workspace the checkout lives in (``worktrees/<auto|gov|codex>/...``) and the
effective Git author and committer of that checkout. OS usernames and
environment-supplied roles never select or relax an identity.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

WORKSPACE_LOGINS = {
    "auto": "tticom-automation",
    "gov": "tticomgov-code",
    "codex": "tticom-codex",
}
IDENT_PATTERN = re.compile(r"^(?P<name>.*?) <(?P<email>[^<>]*)> \d+ [+-]\d{4}$")

Runner = Callable[..., Any]


class IdentityError(RuntimeError):
    pass


def workspace_slot(checkout: Path) -> str:
    """Return the workspace slot owning ``checkout``: auto, gov or codex."""
    resolved = checkout.resolve()
    slot = resolved.parent.name
    if resolved.parent.parent.name != "worktrees" or slot not in WORKSPACE_LOGINS:
        raise IdentityError(
            f"checkout is not under worktrees/<auto|gov|codex>: {resolved}"
        )
    return slot


def github_login(runner: Runner | None = None) -> str:
    runner = runner or subprocess.run
    try:
        result = runner(
            ["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True
        )
    except OSError as error:
        raise IdentityError("GitHub identity check could not run") from error
    login = (result.stdout or "").strip()
    if result.returncode or not login:
        raise IdentityError("GitHub identity check failed")
    return login


def verify_workspace_login(login: str, checkout: Path) -> str:
    slot = workspace_slot(checkout)
    expected = WORKSPACE_LOGINS[slot]
    if login != expected:
        raise IdentityError(
            f"GitHub login {login or '<none>'} may not operate in worktrees/{slot}, "
            f"which belongs to {expected}"
        )
    return slot


def _git_ident(checkout: Path, variable: str, runner: Runner) -> tuple[str, str]:
    try:
        result = runner(
            ["git", "-C", str(checkout), "var", variable],
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise IdentityError("Git identity check could not run") from error
    match = IDENT_PATTERN.match((result.stdout or "").strip())
    if result.returncode or not match:
        raise IdentityError(f"Git identity {variable} is not configured")
    return match["name"], match["email"]


def verify_git_identity(login: str, checkout: Path, runner: Runner | None = None) -> str:
    """Require the effective author and committer to be ``login``.

    The effective identity includes repository-local config and GIT_AUTHOR_*/
    GIT_COMMITTER_* variables, because that is what commits carry. A shared
    global config (one OS account hosting several workers) is not checked.
    """
    runner = runner or subprocess.run
    author = _git_ident(checkout, "GIT_AUTHOR_IDENT", runner)
    committer = _git_ident(checkout, "GIT_COMMITTER_IDENT", runner)
    for role, (name, email) in (("author", author), ("committer", committer)):
        if name != login:
            raise IdentityError(f"Git {role} {name!r} does not match GitHub login {login}")
        if not email:
            raise IdentityError(f"Git {role} email is empty")
    if author[1] != committer[1]:
        raise IdentityError("Git author and committer emails differ")
    return author[1]


def verify_identity(checkout: Path, runner: Runner | None = None) -> dict[str, str]:
    login = github_login(runner)
    slot = verify_workspace_login(login, checkout)
    email = verify_git_identity(login, checkout, runner)
    return {
        "github_login": login,
        "workspace": slot,
        "git_email": email,
        "checkout": str(checkout.resolve()),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--checkout", type=Path, default=Path("."))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = verify_identity(args.checkout)
    except IdentityError as error:
        print(f"IDENTITY_GATE_FAILED: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for key, value in result.items():
            print(f"{key.upper()}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
