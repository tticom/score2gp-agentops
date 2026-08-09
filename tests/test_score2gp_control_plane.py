from pathlib import Path

import pytest

from scripts.score2gp_control_plane import (
    REQUIRED_SKILLS,
    GateError,
    materialize_review_head,
    materialize_skills_checkout,
    read_required_skills,
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


def test_required_skills_are_read_from_the_lock_being_activated(tmp_path: Path) -> None:
    lock = tmp_path / "projects/score2gp"
    lock.mkdir(parents=True)
    (lock / "SKILLS_LOCK.md").write_text(
        """Required skills:

- `governed-development-loop`
- `identity-safe-git`
- `durable-handoff`
- `code-review`

## Activation gate
""",
        encoding="utf-8",
    )
    assert set(read_required_skills(tmp_path)) == {
        "governed-development-loop",
        "identity-safe-git",
        "durable-handoff",
        "code-review",
    }


def test_unknown_required_skill_fails_closed(tmp_path: Path) -> None:
    lock = tmp_path / "projects/score2gp"
    lock.mkdir(parents=True)
    (lock / "SKILLS_LOCK.md").write_text(
        "Required skills:\n\n- `invented-review`\n\n## Activation gate\n",
        encoding="utf-8",
    )
    with pytest.raises(GateError, match="SKILLS_LOCK_UNKNOWN_SKILL"):
        read_required_skills(tmp_path)


def test_materialized_skills_checkout_must_be_clean(
    tmp_path: Path, monkeypatch
) -> None:
    pin = "a" * 40
    skills_repo = tmp_path / "agy-skills"
    skills_repo.mkdir()
    clean_checks = []

    def fake_git(repo: Path, *args: str, check: bool = True) -> str:
        if args == ("rev-parse", "--verify", f"{pin}^{{commit}}"):
            return pin
        if args[:2] == ("worktree", "add"):
            Path(args[-2]).mkdir(parents=True)
            return ""
        if args == ("rev-parse", "HEAD"):
            return pin
        return ""

    monkeypatch.setattr("scripts.score2gp_control_plane.git", fake_git)
    monkeypatch.setattr(
        "scripts.score2gp_control_plane.git_succeeds",
        lambda *args: True,
    )
    monkeypatch.setattr(
        "scripts.score2gp_control_plane.require_clean",
        lambda repo, name: clean_checks.append((repo, name)),
    )

    checkout = materialize_skills_checkout(skills_repo, pin)
    assert clean_checks == [(checkout, "skills_checkout")]


def test_rejects_abbreviated_live_pr_head(tmp_path: Path) -> None:
    with pytest.raises(GateError, match="LIVE_HEAD_INVALID"):
        materialize_review_head(tmp_path, tmp_path / "review", "deadbee")


def test_tiered_review_skills_are_required_by_control_plane() -> None:
    assert REQUIRED_SKILLS["code-review"] == "skills/engineering/code-review"
    assert REQUIRED_SKILLS["hard-review"] == "skills/engineering/hard-review"
    assert (
        REQUIRED_SKILLS["devils-advocate-review"]
        == "skills/engineering/devils-advocate-review"
    )
