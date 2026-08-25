#!/usr/bin/env python3
"""Tests for score2gp_publish_handback module."""
from __future__ import annotations

import json
import subprocess
from typing import Any

import pytest
from scripts.score2gp_publish_handback import HandbackPublishError, publish_author_handback


def make_mock_runner(responses: list[dict[str, Any]]) -> Any:
    call_index = 0

    def mock_runner(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        nonlocal call_index
        if call_index >= len(responses):
            raise RuntimeError(f"Unexpected runner call {call_index}: {' '.join(cmd)}")
        resp = responses[call_index]
        call_index += 1
        return subprocess.CompletedProcess(
            args=cmd,
            returncode=resp.get("returncode", 0),
            stdout=json.dumps(resp["data"]) if "data" in resp else resp.get("stdout", ""),
            stderr=resp.get("stderr", ""),
        )

    return mock_runner


def test_publish_new_handback_posts_and_reads_back() -> None:
    expected_head = "a" * 40
    repo = "tticom/score2gp"
    pr_number = 431

    pr_view = {"state": "OPEN", "headRefOid": expected_head, "author": {"login": "tticom-automation"}}
    comments_before: list[dict[str, Any]] = []
    post_resp = {"id": 101, "body": f"Exact Head SHA: `{expected_head}`\n\nAWAITING_GOVERNANCE_REVIEW"}
    comments_after = [
        {
            "id": 101,
            "body": f"Exact Head SHA: `{expected_head}`\n\nAWAITING_GOVERNANCE_REVIEW",
            "user": {"login": "tticom-automation"},
        }
    ]

    mock_runner = make_mock_runner([
        {"data": pr_view},
        {"data": comments_before},
        {"data": post_resp},
        {"data": comments_after},
    ])

    receipt = publish_author_handback(
        repo=repo,
        pr_number=pr_number,
        expected_head=expected_head,
        author="tticom-automation",
        runner=mock_runner,
    )

    assert receipt["id"] == 101
    assert expected_head in receipt["body"]


def test_publish_existing_stale_handback_patches_and_reads_back() -> None:
    expected_head = "b" * 40
    old_head = "a" * 40
    repo = "tticom/score2gp"
    pr_number = 431

    pr_view = {"state": "OPEN", "headRefOid": expected_head, "author": {"login": "tticom-automation"}}
    stale_comment = {
        "id": 50,
        "body": f"Exact Head SHA: `{old_head}`\nAWAITING_GOVERNANCE_REVIEW",
        "user": {"login": "tticom-automation"},
    }
    comments_before = [stale_comment]
    patch_resp = {"id": 50, "body": f"Exact Head SHA: `{expected_head}`\n\nAWAITING_GOVERNANCE_REVIEW"}
    comments_after = [
        {
            "id": 50,
            "body": f"Exact Head SHA: `{expected_head}`\n\nAWAITING_GOVERNANCE_REVIEW",
            "user": {"login": "tticom-automation"},
        }
    ]

    mock_runner = make_mock_runner([
        {"data": pr_view},
        {"data": comments_before},
        {"data": patch_resp},
        {"data": comments_after},
    ])

    receipt = publish_author_handback(
        repo=repo,
        pr_number=pr_number,
        expected_head=expected_head,
        author="tticom-automation",
        runner=mock_runner,
    )

    assert receipt["id"] == 50
    assert expected_head in receipt["body"]


def test_publish_raises_if_head_mismatch() -> None:
    expected_head = "a" * 40
    actual_head = "b" * 40

    mock_runner = make_mock_runner([
        {"data": {"state": "OPEN", "headRefOid": actual_head}},
    ])

    with pytest.raises(HandbackPublishError, match="head changed before handback publication"):
        publish_author_handback(
            repo="tticom/score2gp",
            pr_number=431,
            expected_head=expected_head,
            runner=mock_runner,
        )

def test_cli_subprocess_missing_args_fails() -> None:
    result = subprocess.run(
        ["python3", "scripts/score2gp_publish_handback.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "the following arguments are required" in result.stderr

def test_cli_subprocess_invalid_json_returns_gracefully() -> None:
    # Test that the CLI itself can be imported and executed without NameError
    result = subprocess.run(
        ["python3", "scripts/score2gp_publish_handback.py", "--repo", "nonexistent/repo", "--pr", "1", "--head", "a" * 40],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    # The actual gh command will fail, but it shouldn't be a NameError
    assert "NameError" not in result.stderr
