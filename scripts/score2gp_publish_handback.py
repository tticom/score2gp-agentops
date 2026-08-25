#!/usr/bin/env python3
"""Reconstruct, publish, and read back author PR handback comments for Score2GP."""
from __future__ import annotations

import argparse
import json
import subprocess
from typing import Any, Callable, Sequence



class HandbackPublishError(RuntimeError):
    pass


Runner = Callable[..., subprocess.CompletedProcess[str]]


def _run_json(
    command: Sequence[str], runner: Runner = subprocess.run
) -> Any:
    result = runner(command, capture_output=True, text=True)
    if result.returncode:
        raise HandbackPublishError(
            result.stderr.strip() or f"command failed: {' '.join(command)}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise HandbackPublishError(
            f"invalid JSON from command: {' '.join(command)}"
        ) from error


def query_comments_with_runner(
    repo: str, pr_number: int, runner: Runner = subprocess.run
) -> list[dict[str, Any]]:
    payload = _run_json(
        ["gh", "api", f"repos/{repo}/issues/{pr_number}/comments?per_page=100"],
        runner=runner,
    )
    if not isinstance(payload, list):
        raise HandbackPublishError("PR comment query must return a list")
    return [comment for comment in payload if isinstance(comment, dict)]



HANDOFF_MARKERS = {
    "AWAITING_CODE_REVIEW",
    "AWAITING_CODEX_REVIEW",
    "AWAITING_GOVERNANCE_REVIEW",
    "AWAITING_AGY_HANDBACK",
}

def query_pr_comments(repo: str, pr_number: int) -> list[dict]:
    import subprocess
    import json
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/issues/{pr_number}/comments?per_page=100"],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise HandbackPublishError(result.stderr.strip() or "PR handback-comment query failed")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise HandbackPublishError("invalid PR handback-comment JSON") from error
    if not isinstance(payload, list):
        raise HandbackPublishError("PR handback-comment query must return a list")
    return [comment for comment in payload if isinstance(comment, dict)]


def find_current_head_handback(
    comments: list[dict], *, head: str, author: str
) -> dict | None:
    if len(head) != 40 or not author:
        return None
    eligible = []
    for comment in comments:
        body = str(comment.get("body", ""))
        login = str((comment.get("user") or {}).get("login", ""))
        if (
            (login == author or (author == "tticom-automation" and login == "tticom"))
            and head in body
            and any(marker in body for marker in HANDOFF_MARKERS)
        ):
            eligible.append(comment)
    if not eligible:
        return None
    return max(eligible, key=lambda comment: int(comment.get("id") or 0))


def find_latest_marked_author_handback(
    comments: list[dict], *, author: str
) -> dict | None:
    if not author:
        return None
    eligible = []
    for comment in comments:
        body = str(comment.get("body", ""))
        login = str((comment.get("user") or {}).get("login", ""))
        if (
            (login == author or (author == "tticom-automation" and login == "tticom"))
            and any(marker in body for marker in HANDOFF_MARKERS)
        ):
            eligible.append(comment)
    if not eligible:
        return None
    return max(eligible, key=lambda comment: int(comment.get("id") or 0))
def publish_author_handback(
    *,
    repo: str,
    pr_number: int,
    expected_head: str,
    author: str = "tticom-automation",
    body: str | None = None,
    runner: Runner = subprocess.run,
) -> dict[str, Any]:
    """Reconstruct, publish (POST/PATCH), and read back the author handback receipt."""
    pr = _run_json(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--repo",
            repo,
            "--json",
            "state,headRefOid,author",
        ],
        runner=runner,
    )
    if str(pr.get("state", "")).upper() != "OPEN":
        raise HandbackPublishError("pull request is not open")
    live_head = str(pr.get("headRefOid", ""))
    if live_head != expected_head:
        raise HandbackPublishError(
            f"head changed before handback publication: expected {expected_head}, got {live_head}"
        )

    pr_author = str((pr.get("author") or {}).get("login", "")) or author

    comments = query_comments_with_runner(repo, pr_number, runner=runner)
    existing_head_handback = find_current_head_handback(
        comments, head=expected_head, author=pr_author
    )

    if not body:
        body = f"Exact Head SHA: `{expected_head}`\n\nAWAITING_GOVERNANCE_REVIEW"

    # If exact-head handback already exists and matches body, return read-back receipt
    if existing_head_handback and str(existing_head_handback.get("body", "")) == body:
        return existing_head_handback

    latest_marked = find_latest_marked_author_handback(comments, author=pr_author)

    if latest_marked and latest_marked.get("id"):
        comment_id = int(latest_marked["id"])
        _run_json(
            [
                "gh",
                "api",
                "--method",
                "PATCH",
                f"repos/{repo}/issues/comments/{comment_id}",
                "-f",
                f"body={body}",
            ],
            runner=runner,
        )
    else:
        _run_json(
            [
                "gh",
                "api",
                "--method",
                "POST",
                f"repos/{repo}/issues/{pr_number}/comments",
                "-f",
                f"body={body}",
            ],
            runner=runner,
        )

    # Read back receipt from GitHub API and verify
    comments_after = query_comments_with_runner(repo, pr_number, runner=runner)
    verified = find_current_head_handback(
        comments_after, head=expected_head, author=pr_author
    )
    if not verified:
        raise HandbackPublishError(
            "handback publication read-back verification failed: published comment not found"
        )
    return verified


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reconstruct, publish, and read back author PR handback comments."
    )
    parser.add_argument("--repo", required=True, help="GitHub repository slug (owner/repo)")
    parser.add_argument("--pr", required=True, type=int, help="Pull request number")
    parser.add_argument("--head", required=True, help="Expected commit SHA")
    parser.add_argument("--author", default="tticom-automation", help="Author GitHub login")
    parser.add_argument("--body", help="Optional custom handback comment body")
    args = parser.parse_args()

    receipt = publish_author_handback(
        repo=args.repo,
        pr_number=args.pr,
        expected_head=args.head,
        author=args.author,
        body=args.body,
    )
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    try:
        main()
    except HandbackPublishError as error:
        raise SystemExit(f"HANDBACK_PUBLISH_FAILED: {error}") from error
