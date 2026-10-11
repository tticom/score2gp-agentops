#!/usr/bin/env python3
"""Install, check or remove the lean pre-push guard in a git repository.

The hook is COPIED into the repository's shared hooks directory (the git common
dir, so one install covers every worktree of that clone). It refuses to overwrite
a different existing hook unless --force is given, in which case the old one is
kept as pre-push.bak.

Usage:
    python install_hooks.py [--repo PATH] [--check | --uninstall | --force]

Exit codes: 0 ok, 1 not installed / differs (with --check) or refused, 64 usage.
This is a convention aid, not server enforcement: `git push --no-verify` skips it.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HOOK_SOURCE = Path(__file__).resolve().parent.parent / "hooks" / "pre-push"


def hooks_dir(repo: Path) -> Path:
    result = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--git-path", "hooks"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode:
        raise SystemExit("NOT_A_GIT_REPOSITORY")
    path = Path(result.stdout.strip())
    return path if path.is_absolute() else (repo / path).resolve()


def hooks_path_override(repo: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "config", "--get", "core.hooksPath"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def read_bytes(path: Path) -> bytes:
    # Compare line-ending-insensitively: a Windows checkout may rewrite LF.
    return path.read_bytes().replace(b"\r\n", b"\n")


def install(repo: Path, force: bool = False) -> int:
    if hooks_path_override(repo):
        print("REFUSED core.hooksPath is set; git would ignore this hook. Unset it or install manually.")
        return 1
    target = hooks_dir(repo) / "pre-push"
    target.parent.mkdir(parents=True, exist_ok=True)
    wanted = read_bytes(HOOK_SOURCE)
    if target.exists():
        if read_bytes(target) == wanted:
            target.chmod(0o755)
            print(f"ALREADY_INSTALLED {target}")
            return 0
        if not force:
            print(f"REFUSED a different pre-push hook exists at {target}; use --force to replace (backed up).")
            return 1
        shutil.copy2(target, target.with_name("pre-push.bak"))
    target.write_bytes(wanted)  # always LF
    target.chmod(0o755)
    print(f"INSTALLED {target}")
    return 0


def check(repo: Path) -> int:
    if hooks_path_override(repo):
        print("NOT_ACTIVE core.hooksPath is set; this hook would be ignored.")
        return 1
    target = hooks_dir(repo) / "pre-push"
    if not target.exists():
        print(f"NOT_INSTALLED {target}")
        return 1
    if read_bytes(target) != read_bytes(HOOK_SOURCE):
        print(f"DIFFERS {target}")
        return 1
    if os.name != "nt" and not os.access(target, os.X_OK):
        print(f"NOT_EXECUTABLE {target} (git would skip it); run install again")
        return 1
    print(f"OK {target}")
    return 0


def uninstall(repo: Path) -> int:
    target = hooks_dir(repo) / "pre-push"
    if not target.exists():
        print("NOT_INSTALLED")
        return 0
    if read_bytes(target) != read_bytes(HOOK_SOURCE):
        print(f"REFUSED {target} is not the lean hook; not removing it.")
        return 1
    target.unlink()
    backup = target.with_name("pre-push.bak")
    if backup.exists():
        backup.replace(target)
        print("REMOVED (previous hook restored)")
    else:
        print("REMOVED")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo", type=Path, default=Path("."))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true")
    group.add_argument("--uninstall", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    if not HOOK_SOURCE.is_file():
        print(f"MISSING_HOOK_SOURCE {HOOK_SOURCE}")
        return 1
    if args.check:
        return check(args.repo)
    if args.uninstall:
        return uninstall(args.repo)
    return install(args.repo, args.force)


if __name__ == "__main__":
    sys.exit(main())
