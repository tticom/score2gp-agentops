import sys
import os
import json
import subprocess
from pathlib import Path
import pytest

# Add scripts to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

import score2gp_bootstrap

def test_parse_status_value():
    assert score2gp_bootstrap.parse_status_value("Status: APPROVED") == "APPROVED"
    assert score2gp_bootstrap.parse_status_value("Status: `APPROVED`") == "APPROVED"
    assert score2gp_bootstrap.parse_status_value("**Status**: APPROVED") == "APPROVED"
    assert score2gp_bootstrap.parse_status_value("Status: APPROVED only after Task 33 says ready") == "APPROVED only after Task 33 says ready"
    assert score2gp_bootstrap.parse_status_value("Status: BLOCKED") == "BLOCKED"
    assert score2gp_bootstrap.parse_status_value("No status line here") == ""

def test_get_next_approved_task(tmp_path):
    queue_dir = tmp_path / "projects/score2gp"
    os.makedirs(queue_dir)
    queue_file = queue_dir / "APPROVED_TASK_QUEUE.md"

    content = """
## Task 12 — Standard timing
Status: APPROVED
Description: Valid task

## Task 13 — Gated task
Status: APPROVED only after Task 10 completes
Description: Conditional task

## Task 14 — Blocked task
Status: BLOCKED
Description: Blocked task
"""
    queue_file.write_text(content, encoding="utf-8")

    next_approved, gated = score2gp_bootstrap.get_next_approved_task(tmp_path)
    assert next_approved == "Task 12 — Standard timing"
    assert gated == ["Task 13 — Gated task (Status: APPROVED only after Task 10 completes)"]

def test_invalid_product_path(tmp_path):
    # Test that invalid path fails closed with non-zero exit code
    invalid_path = str(tmp_path / "does-not-exist")

    with pytest.raises(SystemExit) as raised:
        sys.argv = ["score2gp_bootstrap.py", "--product", invalid_path, "--agentops", "."]
        score2gp_bootstrap.main()
    assert raised.value.code == 1
