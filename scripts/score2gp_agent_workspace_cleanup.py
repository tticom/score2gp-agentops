#!/usr/bin/env python3
"""Agent Workspace Cleanup Skill
Safely identifies and removes stale Git worktrees, prunable metadata, generated
artifacts, and untracked files across agent identities without deleting active
or uncommitted work.
"""
import json
import subprocess
# CLI output is UTF-8; strict errors reject corrupt bytes instead of hiding evidence.
import sys
import os
import getpass
from pathlib import Path
import datetime

ALLOWED_IDENTITIES = {"tticom", "tticom-gov", "tticom-automation", "tticom-codex", "niall", "tticom-orca"}

def run_cmd(cmd, cwd=None, check=True):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="strict")
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{res.stderr}")
    return res

def is_dirty(path):
    res = run_cmd(["git", "status", "--porcelain"], cwd=path)
    return bool(res.stdout.strip())

def get_worktrees(repo_path):
    res = run_cmd(["git", "worktree", "list", "--porcelain"], cwd=repo_path)
    worktrees = []
    current_wt = {}
    for line in res.stdout.splitlines():
        if line.startswith("worktree "):
            if current_wt:
                worktrees.append(current_wt)
            current_wt = {"path": line.split(" ", 1)[1]}
        elif line.startswith("branch "):
            current_wt["branch"] = line.split(" ", 1)[1]
        elif line.startswith("locked"):
            current_wt["locked"] = line.split(" ", 1)[1] if " " in line else "locked"
        elif line.startswith("prunable"):
            current_wt["prunable"] = line.split(" ", 1)[1] if " " in line else "prunable"
        elif line == "detached":
            current_wt["detached"] = True
    if current_wt:
        worktrees.append(current_wt)
    return worktrees

def discover_repos(workspace):
    repos = []
    for d in workspace.iterdir():
        if d.is_dir() and (d / ".git").exists():
            repos.append(d)
    return repos

def resolve_workspace():
    if "SCORE2GP_WORKSPACE" in os.environ:
        return Path(os.environ["SCORE2GP_WORKSPACE"]).resolve()
    if "WORKSPACE_ROOT" in os.environ:
        return Path(os.environ["WORKSPACE_ROOT"]).resolve()
    
    script_dir = Path(__file__).resolve().parent
    workspace = script_dir.parent.parent
    return workspace

def main():
    # Retain the skill entrypoint, but require explicit lifecycle evidence and
    # bounds instead of deleting checkouts based on their names alone.
    try:
        from scripts.score2gp_lifecycle_cleanup import main as lifecycle_main
    except ModuleNotFoundError:
        from score2gp_lifecycle_cleanup import main as lifecycle_main
    return lifecycle_main()


if __name__ == "__main__":
    raise SystemExit(main())
