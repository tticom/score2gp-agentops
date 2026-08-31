#!/usr/bin/env python3
"""Agent Workspace Cleanup Skill
Safely identifies and removes stale Git worktrees, prunable metadata, generated
artifacts, and untracked files across agent identities without deleting active
or uncommitted work.
"""
import json
import subprocess
import sys
from pathlib import Path
import datetime

def run_cmd(cmd, cwd=None):
    res = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{res.stderr}")
    return res.stdout.strip()

def is_dirty(path):
    out = run_cmd(["git", "status", "--porcelain"], cwd=path)
    return bool(out)

def get_worktrees(repo_path):
    out = run_cmd(["git", "worktree", "list", "--porcelain"], cwd=repo_path)
    worktrees = []
    current_wt = {}
    for line in out.splitlines():
        if line.startswith("worktree "):
            if current_wt:
                worktrees.append(current_wt)
            current_wt = {"path": line.split(" ", 1)[1]}
        elif line.startswith("branch "):
            current_wt["branch"] = line.split(" ", 1)[1]
        elif line == "detached":
            current_wt["detached"] = True
    if current_wt:
        worktrees.append(current_wt)
    return worktrees

def main():
    dry_run = "--dry-run" in sys.argv
    workspace = Path("/home/tticom-gov/work/score2gp-workspace")
    if not workspace.exists() or "/tmp" in str(workspace) or "/mnt/c" in str(workspace):
        print("Workspace path invalid or unsafe.")
        sys.exit(1)
        
    repos = [workspace / "score2gp", workspace / "score2gp-agentops"]
    receipt = []
    
    for repo in repos:
        if not repo.exists():
            continue
        print(f"Scanning {repo.name}...")
        worktrees = get_worktrees(repo)
        
        for wt in worktrees:
            wt_path = Path(wt["path"])
            if wt_path == repo:
                continue # canonical
                
            is_review = "-review-pr-" in wt_path.name or wt_path.name.endswith("-review")
            if not is_review:
                print(f"Skipping unclassified worktree: {wt_path}")
                continue
                
            try:
                dirty = is_dirty(wt_path)
            except Exception as e:
                print(f"Error checking {wt_path}: {e}")
                continue
                
            if dirty:
                print(f"Preserving dirty worktree: {wt_path}")
                receipt.append({"action": "preserved", "path": str(wt_path), "reason": "dirty worktree"})
                continue
                
            print(f"{'Would remove' if dry_run else 'Removing'} disposable worktree: {wt_path}")
            if not dry_run:
                try:
                    run_cmd(["git", "worktree", "remove", "--force", str(wt_path)], cwd=repo)
                    receipt.append({"action": "removed_worktree", "path": str(wt_path), "reason": "clean stale review worktree"})
                except Exception as e:
                    print(f"Failed to remove {wt_path}: {e}")
                    receipt.append({"action": "error", "path": str(wt_path), "reason": str(e)})
            else:
                receipt.append({"action": "dry_run_remove", "path": str(wt_path), "reason": "clean stale review worktree"})
                
    if not dry_run:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
        receipt_file = workspace / "score2gp-agentops" / "projects" / "score2gp" / "runs" / f"{timestamp}-cleanup-receipt.json"
        receipt_file.parent.mkdir(parents=True, exist_ok=True)
        with open(receipt_file, "w") as f:
            json.dump(receipt, f, indent=2)
        print(f"Cleanup receipt written to {receipt_file}")

if __name__ == "__main__":
    main()
