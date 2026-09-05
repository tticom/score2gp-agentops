#!/usr/bin/env python3
"""Isolated task clones and verified remote checkpoints; never stages or resets."""
from __future__ import annotations
import argparse
import json
import re
import subprocess
from pathlib import Path


class CheckpointError(RuntimeError):
    pass


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if check and result.returncode:
        # Remote/hook stderr can contain credentials; do not relay it.
        raise CheckpointError(f"git {args[0]} failed (exit {result.returncode}); preserve the task clone")
    return result.stdout.strip() if not result.returncode else ""


def validate_branch(branch: str) -> None:
    if branch in {"main", "master", "HEAD"} or not branch or "/" not in branch:
        raise CheckpointError("an explicit non-protected namespaced task branch is required")
    if subprocess.run(["git", "check-ref-format", "refs/heads/" + branch], capture_output=True).returncode:
        raise CheckpointError("invalid task branch")


def github_remote(url: str) -> str:
    if not re.fullmatch(r"https://github\.com/tticom/[A-Za-z0-9_.-]+\.git", url):
        raise CheckpointError("expected a credential-free HTTPS tticom GitHub origin")
    return url


def assert_clone(repo: Path, branch: str, remote: str) -> None:
    validate_branch(branch)
    if not (repo / ".git").is_dir() or (repo / ".git/objects/info/alternates").exists():
        raise CheckpointError("isolated clone with its own .git and objects is required")
    if Path(git(repo, "rev-parse", "--show-toplevel")).resolve() != repo.resolve():
        raise CheckpointError("task directory must be the clone root")
    if git(repo, "branch", "--show-current") != branch:
        raise CheckpointError("task branch mismatch or detached HEAD")
    if git(repo, "remote", "get-url", "origin") != remote or git(repo, "remote", "get-url", "--push", "origin") != remote:
        raise CheckpointError("task origin/push URL mismatch")
    if git(repo, "config", "--get", "remote.origin.mirror", check=False) == "true":
        raise CheckpointError("mirror remotes are forbidden")


def clean(repo: Path) -> None:
    if git(repo, "status", "--porcelain=v1", "--untracked-files=all"):
        raise CheckpointError("uncommitted work: inspect and commit explicit safe paths, then checkpoint")


def remote_head(repo: Path, remote: str, branch: str) -> str:
    rows = git(repo, "ls-remote", "--heads", remote, "refs/heads/" + branch).splitlines()
    if not rows:
        return ""
    if len(rows) != 1 or rows[0].split()[1] != "refs/heads/" + branch:
        raise CheckpointError("ambiguous remote branch receipt")
    return rows[0].split()[0]


def checkpoint(repo: Path, branch: str, remote: str, *, publish: bool = True) -> dict[str, str]:
    assert_clone(repo, branch, remote)
    clean(repo)
    local = git(repo, "rev-parse", "HEAD")
    if publish:
        git(repo, "push", "--porcelain", remote, f"HEAD:refs/heads/{branch}")
    if remote_head(repo, remote, branch) != local:
        raise CheckpointError("remote HEAD differs; checkpoint is not durable")
    if git(repo, "rev-parse", "HEAD") != local:
        raise CheckpointError("local HEAD moved during checkpoint")
    clean(repo)
    return {"status": "REMOTE_VERIFIED", "branch": branch, "head": local, "repository": remote}


def prepare(source: Path, target: Path, branch: str, base: str, *, review: bool = False) -> dict[str, str]:
    validate_branch(branch)
    remote = github_remote(git(source, "remote", "get-url", "origin"))
    if target.resolve() == source.resolve() or source.resolve() in target.resolve().parents:
        raise CheckpointError("task clone must be separate from source")
    if not re.fullmatch(r"[A-Za-z0-9_./-]+", base) or base.startswith("-"):
        raise CheckpointError("invalid base branch")
    if not target.exists():
        target.parent.mkdir(parents=True, exist_ok=True)
        git(source, "clone", "--no-checkout", "--no-local", remote, str(target))
        if remote_head(target, remote, branch):
            git(target, "switch", "--track", "-c", branch, "origin/" + branch)
        elif review:
            raise CheckpointError("review branch must already exist remotely")
        else:
            git(target, "switch", "-c", branch, "refs/remotes/origin/" + base)
    assert_clone(target, branch, remote)
    clean(target)
    git(target, "fetch", "origin", "+refs/heads/*:refs/remotes/origin/*")
    remote_sha = remote_head(target, remote, branch)
    if remote_sha:
        local = git(target, "rev-parse", "HEAD")
        ahead = git(target, "rev-list", "--count", f"{remote_sha}..{local}")
        behind = git(target, "rev-list", "--count", f"{local}..{remote_sha}")
        if ahead != "0" and behind != "0":
            raise CheckpointError("task branch diverged; preserve both histories")
        if behind != "0":
            git(target, "merge", "--ff-only", "refs/remotes/origin/" + branch)
    receipt = checkpoint(target, branch, remote, publish=not review)
    git(target, "config", "branch." + branch + ".remote", "origin")
    git(target, "config", "branch." + branch + ".merge", "refs/heads/" + branch)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("prepare", "checkpoint", "verify"))
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--branch", required=True)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--base", default="main")
    parser.add_argument("--remote")
    parser.add_argument("--review", action="store_true")
    args = parser.parse_args()
    try:
        if args.operation == "prepare":
            if not args.source:
                raise CheckpointError("prepare requires --source")
            receipt = prepare(args.source, args.repo, args.branch, args.base, review=args.review)
        else:
            remote = github_remote(args.remote or git(args.repo, "remote", "get-url", "origin"))
            receipt = checkpoint(args.repo, args.branch, remote, publish=args.operation == "checkpoint" and not args.review)
        print(json.dumps(receipt, sort_keys=True))
    except CheckpointError as error:
        print(f"CHECKPOINT_BLOCKED: {error}")
        raise SystemExit(75)


if __name__ == "__main__":
    main()
