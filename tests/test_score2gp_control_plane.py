from pathlib import Path

import pytest

from scripts.score2gp_control_plane import (
    GateError,
    materialize_review_head,
    read_skills_pin,
)


def test_reads_exact_full_skills_pin(tmp_path: Path) -> None:
    lock = tmp_path / "projects/score2gp"
    lock.mkdir(parents=True)
    sha = "a" * 40
    (lock / "SKILLS_LOCK.md").write_text(
        f"Required source commit:\n  `{sha}`\n", encoding="utf-8"
    )
    assert read_skills_pin(tmp_path) == sha


def test_rejects_abbreviated_skills_pin(tmp_path: Path) -> None:
    lock = tmp_path / "projects/score2gp"
    lock.mkdir(parents=True)
    (lock / "SKILLS_LOCK.md").write_text(
        "Required source commit:\n  `deadbee`\n", encoding="utf-8"
    )
    with pytest.raises(GateError, match="SKILLS_LOCK_INVALID"):
        read_skills_pin(tmp_path)


def test_rejects_abbreviated_live_pr_head(tmp_path: Path) -> None:
    with pytest.raises(GateError, match="LIVE_HEAD_INVALID"):
        materialize_review_head(tmp_path, tmp_path / "review", "deadbee")
