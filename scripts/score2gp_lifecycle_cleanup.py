"""Bounded lifecycle cleanup; run from a canonical checkout, outside the target.

Workstation integration points (listed here, not edited in AgentOps):
launchers/{codex_author,codex_reviews2,claude_reviews,gov_codex_review,
gov_claude_review,vp_author}.sh and launchers/unattended_loop.sh.
Review launchers call ``clean`` after publication; author launchers call it on
later merged/closed reconciliation, never immediately after author handback.
Wrap the worker command with ``run`` for per-process pytest temp ownership.
Example (all paths absolute):
  python scripts/score2gp_lifecycle_cleanup.py clean --root SLOT --repo REPO \
    --path CHECKOUT --kind review --github-repo tticom/score2gp --pr 123 \
    --receipt OUT/cleanup.json
  python scripts/score2gp_lifecycle_cleanup.py run --temp-root SLOT/.tmp \
    --receipt OUT/temp.json -- python -m pytest --basetemp {temp}/pytest
``--keep`` preserves the entire target when deliverables were requested.
No force, prune, branch deletion, review publication or gate changes occur here.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile
from urllib.parse import quote
from datetime import datetime, timezone

TRUSTED = {"tticom", "tticom-codex", "tticomgov-code", "tticom-automation"}


def command(args, cwd=None):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True,
                            encoding="utf-8", errors="strict", check=True, timeout=30)
    if args[0] == "git" and "status" in args and result.stderr.strip():
        raise ValueError("status_incomplete")
    return result.stdout.strip()


def git(repo, *args):
    return command(["git", "-C", str(repo), *args])


def linked(path):
    return path.is_symlink() or getattr(path, "is_junction", lambda: False)()


def safe_target(root, path):
    # Check lexical components before resolve: resolving first hides junctions.
    root, path = Path(root).absolute(), Path(path).absolute()
    if path.parent != root or linked(root) or linked(path):
        return False
    return not any(linked(p) for p in root.parents)


def worktree(repo, path):
    raw = command(["git", "-C", str(repo), "worktree", "list", "--porcelain", "-z"])
    for block in raw.split("\0\0"):
        fields = {}
        for line in block.split("\0"):
            key, _, value = line.partition(" ")
            fields[key] = value
        if fields.get("worktree") and Path(fields["worktree"]).resolve() == path.resolve():
            return fields
    return None


def api(endpoint):
    return json.loads(command(["gh", "api", endpoint]))


def pages(endpoint):
    separator = "&" if "?" in endpoint else "?"
    return [item for page in json.loads(command(
        ["gh", "api", "--paginate", "--slurp", endpoint + separator + "per_page=100"])) for item in page]


def published(repository, pr, head, author):
    reviews = pages(f"repos/{repository}/pulls/{pr}/reviews")
    comments = pages(f"repos/{repository}/issues/{pr}/comments")
    for review in reviews:
        actor = (review.get("user") or {}).get("login")
        verdict = {"APPROVED": "APPROVE", "CHANGES_REQUESTED": "REQUEST_CHANGES"}.get(review.get("state"))
        if actor not in TRUSTED or actor == author or not verdict or review.get("commit_id") != head:
            continue
        for comment in comments:
            body = comment.get("body", "")
            if (comment.get("user") or {}).get("login") != actor:
                continue
            if any(f"<!-- reviewer-summary:{level}:{head} -->" in body
                   for level in ("basic", "hard", "devils-advocate")) and f"Verdict: {verdict}" in body:
                return True
    return False


def decision(root, repo, path, kind, repository, pr, keep=()):
    """Re-read filesystem and remote lifecycle evidence immediately before removal."""
    if not safe_target(root, path):
        return "unsafe_path"
    if keep:
        return "requested_deliverables"
    wt = worktree(repo, path)
    if wt is None:
        return "unclassified"
    if "locked" in wt:
        return "locked"
    # Include every untracked file. Ignored build/venv output is disposable,
    # but deliverables requested by the launcher always preserve the worktree.
    if git(path, "status", "--porcelain", "--untracked-files=all"):
        return "dirty"
    common_path = Path(git(path, "rev-parse", "--git-common-dir"))
    if common_path.is_absolute():
        common = common_path.resolve()
    else:
        common = (path / common_path).resolve()
    if common == (path / ".git").resolve():
        return "canonical_checkout"
    if path.resolve() == Path.cwd() or path.resolve() in Path.cwd().parents:
        return "active_checkout"
    if kind == "review":
        if "detached" not in wt or not re.fullmatch(r"review-.+", path.name):
            return "unclassified"
    elif kind == "author":
        if not path.name.startswith("author-") or not wt.get("branch"):
            return "unclassified"
    else:
        return "unclassified"
    remote = git(repo, "remote", "get-url", "origin").removesuffix(".git")
    if remote not in {f"https://github.com/{repository}", f"git@github.com:{repository}"}:
        return "repository_mismatch"
    facts = api(f"repos/{repository}/pulls/{pr}")
    if facts.get("number") != pr or facts.get("base", {}).get("repo", {}).get("full_name") != repository:
        return "pr_mismatch"
    if kind == "author":
        if (facts.get("head", {}).get("ref") != wt["branch"].removeprefix("refs/heads/")
                or facts.get("head", {}).get("sha") != wt.get("HEAD")
                or facts.get("head", {}).get("repo", {}).get("full_name") != repository):
            return "pr_mismatch"
        if facts.get("state") != "closed":
            return "open_pr_author"
        branch = quote(f"{repository.split('/')[0]}:{facts['head']['ref']}", safe="")
        if pages(f"repos/{repository}/pulls?state=open&head={branch}"):
            return "open_pr_author"
        return "remove_closed_author"
    if published(repository, pr, wt.get("HEAD"), (facts.get("user") or {}).get("login")):
        return "remove_published_review"
    return "review_unpublished"


def receipt(file, rows):
    file = Path(file)
    file.parent.mkdir(parents=True, exist_ok=True)
    payload = {"schema_version": "workspace-cleanup.v1",
               "timestamp": datetime.now(timezone.utc).isoformat(), "entries": rows}
    # Atomic replacement; the intent is durable before any destructive action.
    staging = file.with_suffix(file.suffix + ".tmp")
    staging.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    staging.replace(file)


def clean(root, repo, path, kind, repository, pr, output, keep=(), dry_run=False):
    path, repo, root, output = map(Path, (path, repo, root, output))
    # Receipt must survive removal and must not itself make a target dirty.
    if output.resolve().is_relative_to(path.resolve()):
        raise ValueError("receipt_inside_target")
    row = {"path": str(path.absolute()), "action": "preserved", "reason": "evidence_unavailable"}
    try:
        reason = decision(root, repo, path, kind, repository, pr, keep)
        row["reason"] = reason
        if reason.startswith("remove_"):
            row["action"] = "would_remove" if dry_run else "pending"
            receipt(output, [row])
            if not dry_run:
                # Git rechecks dirt and locks and refuses busy/changed targets.
                # No --force: a concurrent lock/dirty change must win.
                git(repo, "worktree", "remove", str(path.absolute()))
                row["action"] = "removed"
    except (OSError, ValueError, KeyError, TypeError, AttributeError, subprocess.SubprocessError):
        row.update(action="preserved", reason="evidence_or_removal_failed")
    receipt(output, [row])
    return row


def run_owned(temp_root, output, args, keep=()):
    """Own one fresh temp directory; never sweep another process's pytest data."""
    temp_root = Path(temp_root).resolve()
    temp_root.mkdir(parents=True, exist_ok=True)
    path = Path(tempfile.mkdtemp(prefix="pytest-owned-", dir=temp_root))
    row = {"path": str(path), "action": "pending", "reason": "owned_temp"}
    try:
        receipt(output, [row])
        env = dict(os.environ, TMP=str(path), TEMP=str(path), TMPDIR=str(path))
        return subprocess.run([arg.replace("{temp}", str(path)) for arg in args], env=env).returncode
    finally:
        if keep:
            row.update(action="preserved", reason="requested_deliverables")
        else:
            try:
                # Never follow a link or junction substituted by a child.
                if not safe_target(temp_root, path) or any(
                    linked(Path(here, name)) for here, dirs, files in os.walk(path)
                    for name in dirs + files
                ):
                    row.update(action="preserved", reason="unsafe_path")
                else:
                    def retry_readonly(function, item, error):
                        item = Path(item)
                        if (not item.resolve().is_relative_to(path.resolve()) or linked(item)
                                or item.stat().st_mode & stat.S_IWUSR):
                            raise error[1]
                        # Windows Git object files can be read-only. Do not
                        # change ACLs or retry a busy/locked writable file.
                        item.chmod(stat.S_IREAD | stat.S_IWRITE)
                        function(str(item))

                    shutil.rmtree(path, onerror=retry_readonly)
                    row["action"] = "removed"
            except OSError:
                row.update(action="preserved", reason="temp_removal_failed")
        receipt(output, [row])


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)
    cleanup = sub.add_parser("clean")
    for name in ("root", "repo", "path"):
        cleanup.add_argument("--" + name, type=Path, required=True)
    cleanup.add_argument("--kind", choices=("author", "review"), required=True)
    cleanup.add_argument("--github-repo", required=True)
    cleanup.add_argument("--pr", type=int, required=True)
    cleanup.add_argument("--dry-run", action="store_true")
    run = sub.add_parser("run")
    run.add_argument("--temp-root", type=Path, required=True)
    run.add_argument("command", nargs=argparse.REMAINDER)
    for child in (cleanup, run):
        child.add_argument("--receipt", type=Path, required=True)
        child.add_argument("--keep", action="append", default=[])
    args = parser.parse_args(argv)
    if args.mode == "run":
        command_args = args.command[1:] if args.command[:1] == ["--"] else args.command
        if not command_args:
            parser.error("run requires a command")
        return run_owned(args.temp_root, args.receipt, command_args, args.keep)
    row = clean(args.root, args.repo, args.path, args.kind, args.github_repo, args.pr,
                args.receipt, args.keep, args.dry_run)
    print(json.dumps(row))
    return int(row["reason"] == "evidence_or_removal_failed")


if __name__ == "__main__":
    raise SystemExit(main())
