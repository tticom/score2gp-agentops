#!/usr/bin/env python3
"""Fail-closed control-plane synchronization shared by `go` and `got`."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")
LOCK_PATTERN = re.compile(r"Required source commit:\s*\n\s*`([0-9a-f]{40})`")
REQUIRED_SKILLS = {
    "governed-development-loop": "skills/engineering/governed-development-loop",
    "identity-safe-git": "skills/engineering/identity-safe-git",
    "durable-handoff": "skills/productivity/durable-handoff",
    "code-review": "skills/engineering/code-review",
    "hard-review": "skills/engineering/hard-review",
    "devils-advocate-review": "skills/engineering/devils-advocate-review",
}


class GateError(RuntimeError):
    pass


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    )
    if check and result.returncode:
        raise GateError(result.stderr.strip() or "git command failed")
    return result.stdout.strip() if result.returncode == 0 else ""


def git_succeeds(repo: Path, *args: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
    ).returncode == 0


def require_clean(repo: Path, name: str) -> None:
    if git(repo, "status", "--porcelain"):
        raise GateError(f"DIRTY_{name.upper()}")


def sync_main(repo: Path, name: str) -> str:
    require_clean(repo, name)
    git(repo, "fetch", "origin", "main")
    git(repo, "switch", "main")
    git(repo, "merge", "--ff-only", "origin/main")
    local = git(repo, "rev-parse", "HEAD")
    remote = git(repo, "rev-parse", "origin/main")
    if local != remote:
        raise GateError(f"{name.upper()}_MAIN_MISMATCH")
    return local


def read_skills_pin(agentops: Path) -> str:
    text = (agentops / "projects/score2gp/SKILLS_LOCK.md").read_text(encoding="utf-8")
    match = LOCK_PATTERN.search(text)
    if not match:
        raise GateError("SKILLS_LOCK_INVALID")
    return match.group(1)


def read_required_skills(agentops: Path) -> dict[str, str]:
    text = (agentops / "projects/score2gp/SKILLS_LOCK.md").read_text(
        encoding="utf-8"
    )
    try:
        block = text.split("Required skills:", 1)[1].split("## Activation gate", 1)[0]
    except IndexError as error:
        raise GateError("SKILLS_LOCK_REQUIRED_SKILLS_INVALID") from error
    names = re.findall(r"^- `([a-z0-9-]+)`\s*$", block, flags=re.MULTILINE)
    if not names or len(names) != len(set(names)):
        raise GateError("SKILLS_LOCK_REQUIRED_SKILLS_INVALID")
    unknown = [name for name in names if name not in REQUIRED_SKILLS]
    if unknown:
        raise GateError(f"SKILLS_LOCK_UNKNOWN_SKILL {unknown[0]}")
    return {name: REQUIRED_SKILLS[name] for name in names}


def materialize_skills_checkout(skills_repo: Path, pin: str) -> Path:
    """Materialize a merged immutable skills pin without activating it."""
    if not FULL_SHA.fullmatch(pin):
        raise GateError("SKILLS_PIN_INVALID")
    git(skills_repo, "fetch", "origin", "main")
    resolved = git(skills_repo, "rev-parse", "--verify", f"{pin}^{{commit}}", check=False)
    if resolved != pin:
        raise GateError("SKILLS_PIN_UNAVAILABLE")
    if not git_succeeds(skills_repo, "merge-base", "--is-ancestor", pin, "origin/main"):
        raise GateError("SKILLS_PIN_NOT_MERGED")

    pins_root = skills_repo.parent / "agy-skills-pins"
    checkout = pins_root / pin
    if not checkout.exists():
        pins_root.mkdir(parents=True, exist_ok=True)
        git(skills_repo, "worktree", "add", "--detach", str(checkout), pin)
    require_clean(checkout, "skills_checkout")
    head = git(checkout, "rev-parse", "HEAD")
    if head != pin:
        raise GateError(f"SKILLS_PIN_MISMATCH expected={pin} actual={head}")

    return checkout


def validate_skills_checkout(checkout: Path, required_skills: dict[str, str]) -> None:
    for name, relative in required_skills.items():
        if not (checkout / relative / "SKILL.md").is_file():
            raise GateError(f"REQUIRED_SKILL_MISSING {name}")


def activate_skills_checkout(
    checkout: Path, required_skills: dict[str, str]
) -> None:
    installed_root = Path.home() / ".agents/skills"
    installed_root.mkdir(parents=True, exist_ok=True)
    for name, relative in required_skills.items():
        source = checkout / relative
        if not (source / "SKILL.md").is_file():
            raise GateError(f"REQUIRED_SKILL_MISSING {name}")
        destination = installed_root / name
        if destination.exists() and not destination.is_symlink():
            raise GateError(f"SKILL_DESTINATION_NOT_SYMLINK {destination}")
        if destination.is_symlink() and destination.resolve() == source.resolve():
            continue
        replacement = installed_root / f".{name}.next"
        if replacement.exists() or replacement.is_symlink():
            replacement.unlink()
        replacement.symlink_to(source, target_is_directory=True)
        os.replace(replacement, destination)


def materialize_and_activate_skills(
    skills_repo: Path,
    pin: str,
    required_skills: dict[str, str] | None = None,
) -> str:
    required = required_skills or REQUIRED_SKILLS
    checkout = materialize_skills_checkout(skills_repo, pin)
    validate_skills_checkout(checkout, required)
    activate_skills_checkout(checkout, required)
    head = git(checkout, "rev-parse", "HEAD")
    return head


def materialize_review_head(product: Path, review_worktree: Path, live_head: str) -> str:
    if not FULL_SHA.fullmatch(live_head):
        raise GateError("LIVE_HEAD_INVALID")
    require_clean(product, "product")
    git(product, "fetch", "origin", live_head)
    if review_worktree.exists():
        require_clean(review_worktree, "review_worktree")
    else:
        git(product, "worktree", "add", "--detach", str(review_worktree), live_head)
    local = git(review_worktree, "rev-parse", "HEAD")
    if local != live_head:
        raise GateError(f"REVIEW_HEAD_MISMATCH expected={live_head} actual={local}")
    return local


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agentops", type=Path, required=True)
    parser.add_argument("--product", type=Path, required=True)
    parser.add_argument("--skills-repo", type=Path, required=True)
    parser.add_argument("--live-pr-head")
    parser.add_argument("--review-worktree", type=Path)
    args = parser.parse_args()

    agentops_sha = sync_main(args.agentops.resolve(), "agentops")
    product_sha = sync_main(args.product.resolve(), "product")
    pin = read_skills_pin(args.agentops.resolve())
    skills_sha = materialize_and_activate_skills(args.skills_repo.resolve(), pin)

    review_sha = None
    if args.live_pr_head:
        if not args.review_worktree:
            raise GateError("REVIEW_WORKTREE_REQUIRED")
        review_sha = materialize_review_head(
            args.product.resolve(), args.review_worktree.resolve(), args.live_pr_head
        )

    print(f"AGENTOPS_SHA={agentops_sha}")
    print(f"PRODUCT_MAIN_SHA={product_sha}")
    print(f"SKILLS_SHA={skills_sha}")
    if review_sha:
        print(f"REVIEW_LOCAL_HEAD={review_sha}")
        print(f"REVIEW_LIVE_HEAD={args.live_pr_head}")


if __name__ == "__main__":
    try:
        main()
    except GateError as error:
        raise SystemExit(f"CONTROL_PLANE_GATE_FAILED: {error}") from error
