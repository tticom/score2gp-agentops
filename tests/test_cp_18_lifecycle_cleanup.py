"""Real Git deletion oracles; GitHub protocol facts are supplied offline.

Each test's rejecting mutation is executable in score2gp_cleanup_mutants.py.
No private inputs or production worktree is modified by this suite.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

SOURCE = Path(os.environ.get("CP18_CLEANUP_MODULE", Path(__file__).parents[1] /
                             "scripts/score2gp_lifecycle_cleanup.py"))
spec = importlib.util.spec_from_file_location("cleanup_under_test", SOURCE)
cleanup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cleanup)


@pytest.fixture
def checkout(tmp_path, monkeypatch):
    repo = tmp_path / "canonical"
    repo.mkdir()
    cleanup.git(repo, "init", "-q")
    cleanup.git(repo, "config", "user.name", "cleanup-test")
    cleanup.git(repo, "config", "user.email", "cleanup-test@example.invalid")
    (repo / "tracked").write_text("public test sentinel\n")
    (repo / ".gitignore").write_text("build/\n")
    cleanup.git(repo, "add", ".")
    cleanup.git(repo, "commit", "-qm", "test root")
    cleanup.git(repo, "remote", "add", "origin", "https://github.com/tticom/score2gp-agentops.git")
    root = tmp_path / "slot"
    root.mkdir()
    path = root / "author-test"
    cleanup.git(repo, "worktree", "add", "-qb", "task", str(path))
    head = cleanup.git(path, "rev-parse", "HEAD")
    facts = {"number": 18, "state": "closed", "merged": True,
             "base": {"repo": {"full_name": "tticom/score2gp-agentops"}},
             "head": {"ref": "task", "sha": head,
                      "repo": {"full_name": "tticom/score2gp-agentops"}},
             "user": {"login": "tticom-codex"}}
    monkeypatch.setattr(cleanup, "api", lambda endpoint: facts)
    reviews = [{"id": 123, "state": "APPROVED", "commit_id": head,
                "user": {"login": "tticomgov-code"}}]
    comments = [{"user": {"login": "tticomgov-code"},
                 "body": f"<!-- reviewer-summary:hard:{head} -->\nVerdict: APPROVE"}]
    monkeypatch.setattr(cleanup, "pages", lambda endpoint: [] if "state=open" in endpoint
                        else reviews if "/reviews" in endpoint else comments)
    output = tmp_path / "receipt.json"
    return repo, root, path, facts, reviews, comments, output


@pytest.mark.parametrize("case,expected", [
    ("merged", "remove_closed_author"), ("closed", "remove_closed_author"),
    ("dirty", "dirty"), ("untracked", "dirty"), ("locked", "locked"),
    ("open", "open_pr_author"), ("published_review", "remove_published_review"),
    ("unclassified", "unclassified"), ("attached_review", "unclassified"),
    ("unpublished", "review_unpublished"), ("keep", "requested_deliverables"),
    ("wrong_pr", "pr_mismatch"), ("wrong_head", "pr_mismatch"),
    ("wrong_remote", "repository_mismatch"),
    ("reused_branch", "open_pr_author"),
])
def test_lifecycle(checkout, monkeypatch, case, expected):
    """Reject unsafe eligibility or a no-op remover using files and Git registry."""
    repo, root, path, facts, reviews, comments, output = checkout
    kind = "author"
    keep = []
    if case in {"published_review", "unpublished", "attached_review"}:
        kind = "review"
        new = root / "review-agentops-18"
        cleanup.git(repo, "worktree", "move", str(path), str(new))
        path = new
        facts["state"] = "open"
        if case != "attached_review":
            cleanup.git(path, "checkout", "--detach", "-q")
        if case == "unpublished":
            comments.clear()
    if case == "closed":
        facts["merged"] = False
    if case == "dirty":
        (path / "tracked").write_text("uncommitted change")
    if case == "untracked":
        (path / "untracked").write_text("must survive")
    if case == "locked":
        cleanup.git(repo, "worktree", "lock", str(path))
    if case == "open":
        facts["state"] = "open"
    if case == "unclassified":
        kind = "other"
    if case == "keep":
        keep = ["build/requested-output"]
        (path / "build").mkdir()
        (path / keep[0]).write_text("requested deliverable")
    if case == "wrong_pr":
        facts["head"]["ref"] = "other-task"
    if case == "wrong_head":
        facts["head"]["sha"] = "0" * 40
    if case == "wrong_remote":
        cleanup.git(repo, "remote", "set-url", "origin", "https://github.com/other/repo.git")
    if case == "reused_branch":
        monkeypatch.setattr(cleanup, "pages", lambda endpoint: [{"number": 19}])
    row = cleanup.clean(root, repo, path, kind, "tticom/score2gp-agentops", 18, output, keep)
    assert row["reason"] == expected
    removed = expected.startswith("remove_")
    assert row["action"] == ("removed" if removed else "preserved")
    assert path.exists() is not removed
    assert (cleanup.worktree(repo, path) is None) is removed
    assert json.loads(output.read_text())["entries"] == [row]
    if keep:
        assert (path / keep[0]).read_text() == "requested deliverable"


@pytest.mark.parametrize("case,expected", [
    ("good", True), ("changes", True), ("no_summary", False),
    ("wrong_actor", False), ("wrong_head", False), ("self_review", False),
    ("pending", False), ("wrong_verdict", False),
])
def test_publication(checkout, case, expected):
    """Reject treating a formal review alone or mismatched summary as publication."""
    _, _, _, facts, reviews, comments, _ = checkout
    if case == "changes":
        reviews[0]["state"] = "CHANGES_REQUESTED"
        comments[0]["body"] = comments[0]["body"].replace("APPROVE", "REQUEST_CHANGES")
    if case == "no_summary":
        comments.clear()
    if case == "wrong_actor":
        comments[0]["user"]["login"] = "someone-else"
    if case == "wrong_head":
        reviews[0]["commit_id"] = "0" * 40
    if case == "self_review":
        reviews[0]["user"]["login"] = "tticom-codex"
        comments[0]["user"]["login"] = "tticom-codex"
    if case == "pending":
        reviews[0]["state"] = "PENDING"
    if case == "wrong_verdict":
        comments[0]["body"] = comments[0]["body"].replace("APPROVE", "REQUEST_CHANGES")
    assert cleanup.published("tticom/score2gp-agentops", 18, facts["head"]["sha"], "tticom-codex") is expected


def test_dry_run_and_removal_failure(checkout, monkeypatch):
    """Reject deletion in dry-run and recording success before Git succeeds."""
    repo, root, path, _, _, _, output = checkout
    args = (root, repo, path, "author", "tticom/score2gp-agentops", 18, output)
    row = cleanup.clean(*args, dry_run=True)
    assert row["action"] == "would_remove" and path.exists()
    original = cleanup.git

    def fail_remove(repo, *args):
        if args[:2] == ("worktree", "remove"):
            assert json.loads(output.read_text())["entries"][0]["action"] == "pending"
            raise subprocess.CalledProcessError(1, "git")
        return original(repo, *args)

    monkeypatch.setattr(cleanup, "git", fail_remove)
    row = cleanup.clean(*args)
    assert row["action"] == "preserved" and path.exists()
    assert row["reason"] == "evidence_or_removal_failed"


def test_bounds_and_api_failure(checkout, monkeypatch):
    """Reject a target outside the slot, missing registration, or unknown PR state."""
    repo, root, path, _, _, _, output = checkout
    assert cleanup.decision(root, repo, repo, "author", "x", 1) == "unsafe_path"
    assert cleanup.decision(root, repo, root / "missing", "author", "x", 1) == "unclassified"
    with pytest.raises(ValueError, match="receipt_inside_target"):
        cleanup.clean(root, repo, path, "author", "x", 1, path / "receipt.json")

    def unavailable(endpoint):
        raise subprocess.CalledProcessError(1, "gh")

    monkeypatch.setattr(cleanup, "api", unavailable)
    # Use the correct remote so this test actually reaches the failing API.
    row = cleanup.clean(root, repo, path, "author", "tticom/score2gp-agentops", 18, output)
    assert row["reason"] == "evidence_or_removal_failed" and path.exists()


@pytest.mark.parametrize("exit_code,keep", [(0, False), (7, False), (0, True)])
def test_owned_temp(tmp_path, exit_code, keep):
    """Reject leaking temp on child failure, sweeping peers or losing deliverables."""
    root = tmp_path / "temp"
    root.mkdir()
    peer = root / "pytest-peer"
    peer.mkdir()
    sentinel = peer / "active"
    sentinel.write_text("other process")
    output = tmp_path / "temp-receipt.json"
    child = [sys.executable, "-c", "import os,pathlib,stat,sys; "
             "p=pathlib.Path(sys.argv[1]); assert os.environ['TEMP']==str(p); "
             "(p/'result').write_text('deliverable'); (p/'result').chmod(stat.S_IREAD); "
             "sys.exit(int(sys.argv[2]))",
             "{temp}", str(exit_code)]
    result = cleanup.run_owned(root, output, child, ["result"] if keep else [])
    assert result == exit_code
    row = json.loads(output.read_text())["entries"][0]
    assert row["action"] == ("preserved" if keep else "removed")
    assert Path(row["path"]).exists() is keep
    assert sentinel.exists(), "cleanup swept another process temp directory"
    assert sentinel.read_text() == "other process"


def test_legacy_entrypoint_is_bounded():
    """Reject retaining the old name-only, publication-blind deletion CLI."""
    script = Path(os.environ.get("CP18_LEGACY_MODULE", Path(__file__).parents[1] /
                                 "scripts/score2gp_agent_workspace_cleanup.py"))
    result = subprocess.run([sys.executable, str(script), "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "{clean,run}" in result.stdout


def test_status_warning_is_not_clean(monkeypatch):
    """Reject empty stdout as clean when Git warns it cannot read a directory."""
    monkeypatch.setattr(cleanup.subprocess, "run", lambda *a, **kw:
                        SimpleNamespace(stdout="", stderr="warning: unreadable directory"))
    rejected = False
    try:
        cleanup.git(Path("unused"), "status", "--porcelain", "--untracked-files=all")
    except ValueError as error:
        rejected = str(error) == "status_incomplete"
    assert rejected, "Git warning was incorrectly treated as clean status"
