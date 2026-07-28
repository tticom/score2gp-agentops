#!/usr/bin/env python3
"""Resolve the authoritative formal review verdict for one exact PR head."""
from __future__ import annotations

import argparse
import json
import subprocess
from typing import Any, Iterable


class ReviewStateError(RuntimeError):
    pass


def resolve_current_head_review(
    reviews: Iterable[dict[str, Any]], live_head: str, reviewer: str
) -> dict[str, Any] | None:
    eligible = []
    for review in reviews:
        author = (review.get("user") or review.get("author") or {}).get("login")
        state = str(review.get("state", "")).upper()
        if (
            author == reviewer
            and review.get("commit_id") == live_head
            and state in {"APPROVED", "CHANGES_REQUESTED"}
        ):
            eligible.append(review)
    if not eligible:
        return None
    return max(
        eligible,
        key=lambda item: (str(item.get("submitted_at") or ""), int(item.get("id") or 0)),
    )


def query_reviews(repo: str, pr_number: int) -> list[dict[str, Any]]:
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/pulls/{pr_number}/reviews?per_page=100"],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise ReviewStateError(result.stderr.strip() or "review query failed")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise ReviewStateError("invalid review JSON") from error
    if not isinstance(payload, list):
        raise ReviewStateError("review query did not return a list")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True, type=int)
    parser.add_argument("--head", required=True)
    parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()
    review = resolve_current_head_review(
        query_reviews(args.repo, args.pr), args.head, args.reviewer
    )
    print(json.dumps(review, indent=2) if review else "null")


if __name__ == "__main__":
    try:
        main()
    except ReviewStateError as error:
        raise SystemExit(f"REVIEW_STATE_UNAVAILABLE: {error}") from error
