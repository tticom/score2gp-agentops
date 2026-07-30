#!/usr/bin/env python3
"""Publish and verify a formal Codex review for one exact PR head."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any, Callable, Sequence

try:
    from scripts.score2gp_pr_review_state import resolve_current_head_review
except ModuleNotFoundError:  # Direct execution
    from score2gp_pr_review_state import resolve_current_head_review


class ReviewPublishError(RuntimeError):
    pass


Runner = Callable[..., subprocess.CompletedProcess[str]]


def normalize_verdict(verdict: str) -> tuple[str, str, str]:
    normalized = verdict.strip().upper().replace("-", "_").replace(" ", "_")
    if normalized in {"NEEDS_CHANGES", "REQUEST_CHANGES", "CHANGES_REQUESTED"}:
        return "CHANGES_REQUESTED", "REQUEST_CHANGES", "AWAITING_AGY_FIXES"
    if normalized in {"APPROVE", "APPROVED"}:
        return "APPROVED", "APPROVE", "READY_FOR_HUMAN_MERGE"
    raise ReviewPublishError(
        "unsupported verdict; use needs changes, CHANGES_REQUESTED, or APPROVED"
    )


def _run_json(
    command: Sequence[str], runner: Runner = subprocess.run
) -> Any:
    result = runner(command, capture_output=True, text=True)
    if result.returncode:
        raise ReviewPublishError(
            result.stderr.strip() or f"command failed: {' '.join(command)}"
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise ReviewPublishError(
            f"invalid JSON from command: {' '.join(command)}"
        ) from error


def publish_review(
    *,
    repo: str,
    pr_number: int,
    expected_head: str,
    verdict: str,
    body: str,
    reviewer: str = "tticomgov-code",
    runner: Runner = subprocess.run,
) -> dict[str, Any]:
    expected_state, event, dispatch_state = normalize_verdict(verdict)
    pr = _run_json(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--repo",
            repo,
            "--json",
            "state,headRefOid",
        ],
        runner,
    )
    live_head = str(pr.get("headRefOid", ""))
    if str(pr.get("state", "")).upper() != "OPEN":
        raise ReviewPublishError("pull request is not open")
    if live_head != expected_head:
        raise ReviewPublishError(
            f"head changed before publication: expected {expected_head}, got {live_head}"
        )

    published = _run_json(
        [
            "gh",
            "api",
            "--method",
            "POST",
            f"repos/{repo}/pulls/{pr_number}/reviews",
            "-f",
            f"commit_id={expected_head}",
            "-f",
            f"body={body}",
            "-f",
            f"event={event}",
        ],
        runner,
    )
    review_id = int(published.get("id") or 0)
    if not review_id:
        raise ReviewPublishError("review publication returned no review ID")

    final_pr = _run_json(
        [
            "gh",
            "pr",
            "view",
            str(pr_number),
            "--repo",
            repo,
            "--json",
            "state,headRefOid",
        ],
        runner,
    )
    final_head = str(final_pr.get("headRefOid", ""))
    if (
        str(final_pr.get("state", "")).upper() != "OPEN"
        or final_head != expected_head
    ):
        raise ReviewPublishError(
            f"head changed during publication: expected {expected_head}, got {final_head}"
        )

    reviews = _run_json(
        [
            "gh",
            "api",
            f"repos/{repo}/pulls/{pr_number}/reviews?per_page=100",
        ],
        runner,
    )
    if not isinstance(reviews, list):
        raise ReviewPublishError("review verification did not return a list")
    current = resolve_current_head_review(reviews, expected_head, reviewer)
    if not current:
        raise ReviewPublishError("published review is not authoritative for the exact head")
    if int(current.get("id") or 0) != review_id:
        raise ReviewPublishError(
            f"published review {review_id} was superseded by {current.get('id')}"
        )
    if str(current.get("state", "")).upper() != expected_state:
        raise ReviewPublishError(
            f"review state mismatch: expected {expected_state}, got {current.get('state')}"
        )
    return {
        "ok": True,
        "state": dispatch_state,
        "review": current,
        "head": expected_head,
        "pr_number": pr_number,
        "repository": repo,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--head", required=True)
    parser.add_argument("--verdict", required=True)
    parser.add_argument("--body-file", required=True, type=Path)
    args = parser.parse_args()
    body = args.body_file.read_text(encoding="utf-8").strip()
    if not body:
        raise ReviewPublishError("review body is empty")
    print(
        json.dumps(
            publish_review(
                repo=args.repo,
                pr_number=args.pr,
                expected_head=args.head,
                verdict=args.verdict,
                body=body,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except ReviewPublishError as error:
        raise SystemExit(f"REVIEW_PUBLICATION_FAILED: {error}") from error
