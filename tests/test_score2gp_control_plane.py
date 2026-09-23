from pathlib import Path

import pytest

from scripts.score2gp_control_plane import (
    REQUIRED_SKILLS,
    GateError,
    activate_skills_checkout,
    default_skills_repo,
    materialize_review_head,
    materialize_skills_checkout,
    read_required_skills,
    read_skills_pin,
    resolve_venv_python,
    validate_skills_checkout,
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
    skills_repo = tmp_path / "agentops-claude-skills"
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
    assert REQUIRED_SKILLS["code-review"] == "skills/code-review"
    assert REQUIRED_SKILLS["hard-review"] == "skills/hard-review"
    assert REQUIRED_SKILLS["devils-advocate-review"] == "skills/devils-advocate-review"


@pytest.mark.parametrize("slot", ["auto", "gov", "codex"])
def test_default_skills_repo_is_the_sibling_checkout(tmp_path, monkeypatch, slot) -> None:
    agentops = tmp_path / "worktrees" / slot / "score2gp-agentops"
    agentops.mkdir(parents=True)
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    expected = tmp_path / "worktrees" / slot / "agentops-claude-skills"
    assert default_skills_repo(agentops) == expected.resolve()
    relative = Path("..") / "worktrees" / slot / "score2gp-agentops"
    assert default_skills_repo(relative) == expected.resolve()


@pytest.mark.parametrize(
    "layout", [Path(".venv/Scripts/python.exe"), Path(".venv/bin/python")]
)
def test_venv_python_resolves_windows_and_posix_layouts(tmp_path, layout) -> None:
    interpreter = tmp_path / layout
    interpreter.parent.mkdir(parents=True)
    interpreter.write_text("", encoding="utf-8")
    assert resolve_venv_python(tmp_path) == interpreter


def test_missing_venv_python_fails_closed(tmp_path) -> None:
    (tmp_path / ".venv").mkdir()
    with pytest.raises(GateError, match="VENV_PYTHON_MISSING"):
        resolve_venv_python(tmp_path)


def fake_pin_git(pin: str, merged: bool, head: str | None = None):
    def fake_git(repo: Path, *args: str, check: bool = True) -> str:
        if args == ("rev-parse", "--verify", f"{pin}^{{commit}}"):
            return pin
        if args[:2] == ("worktree", "add"):
            Path(args[-2]).mkdir(parents=True)
            return ""
        if args == ("rev-parse", "HEAD"):
            return head or pin
        return ""

    return fake_git, (lambda *args: merged)


def test_pin_not_on_main_is_refused(tmp_path, monkeypatch) -> None:
    pin = "b" * 40
    fake_git, succeeds = fake_pin_git(pin, merged=False)
    monkeypatch.setattr("scripts.score2gp_control_plane.git", fake_git)
    monkeypatch.setattr("scripts.score2gp_control_plane.git_succeeds", succeeds)
    with pytest.raises(GateError, match="SKILLS_PIN_NOT_MERGED"):
        materialize_skills_checkout(tmp_path / "agentops-claude-skills", pin)


def test_dirty_pin_checkout_is_refused(tmp_path, monkeypatch) -> None:
    pin = "c" * 40
    fake_git, succeeds = fake_pin_git(pin, merged=True)

    def dirty(repo: Path, *args: str, check: bool = True) -> str:
        if args == ("status", "--porcelain"):
            return " M SKILL.md"
        return fake_git(repo, *args, check=check)

    monkeypatch.setattr("scripts.score2gp_control_plane.git", dirty)
    monkeypatch.setattr("scripts.score2gp_control_plane.git_succeeds", succeeds)
    with pytest.raises(GateError, match="DIRTY_SKILLS_CHECKOUT"):
        materialize_skills_checkout(tmp_path / "agentops-claude-skills", pin)


def test_pins_are_materialized_beside_the_skills_repo(tmp_path, monkeypatch) -> None:
    pin = "d" * 40
    fake_git, succeeds = fake_pin_git(pin, merged=True)
    monkeypatch.setattr("scripts.score2gp_control_plane.git", fake_git)
    monkeypatch.setattr("scripts.score2gp_control_plane.git_succeeds", succeeds)
    checkout = materialize_skills_checkout(tmp_path / "agentops-claude-skills", pin)
    assert checkout == tmp_path / "agentops-claude-skills-pins" / pin


def pinned_skills(tmp_path: Path, names) -> Path:
    checkout = tmp_path / "pin"
    for name in names:
        skill = checkout / "skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(f"# {name}\n", encoding="utf-8")
    return checkout


def test_missing_required_skill_fails_closed(tmp_path) -> None:
    checkout = pinned_skills(tmp_path, [n for n in REQUIRED_SKILLS if n != "hard-review"])
    with pytest.raises(GateError, match="REQUIRED_SKILL_MISSING hard-review"):
        validate_skills_checkout(checkout, REQUIRED_SKILLS)


def symlinks_supported(tmp_path: Path) -> bool:
    target = tmp_path / "probe-target"
    target.mkdir()
    try:
        (tmp_path / "probe-link").symlink_to(target, target_is_directory=True)
    except OSError:
        return False
    return True


def test_valid_pin_activates_the_required_skills(tmp_path, monkeypatch) -> None:
    if not symlinks_supported(tmp_path):
        pytest.skip("directory symlinks need Developer Mode or privilege on this host")
    checkout = pinned_skills(tmp_path, REQUIRED_SKILLS)
    home = tmp_path / "home"
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    validate_skills_checkout(checkout, REQUIRED_SKILLS)
    activate_skills_checkout(checkout, REQUIRED_SKILLS)
    for name, relative in REQUIRED_SKILLS.items():
        link = home / ".agents" / "skills" / name
        assert link.is_symlink()
        assert link.resolve() == (checkout / relative).resolve()


def test_activation_without_symlink_support_fails_closed(tmp_path, monkeypatch) -> None:
    checkout = pinned_skills(tmp_path, REQUIRED_SKILLS)
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path / "home"))

    def refuse(self, *args, **kwargs):
        raise OSError(1314, "A required privilege is not held by the client")

    monkeypatch.setattr(Path, "symlink_to", refuse)
    with pytest.raises(GateError, match="SKILL_LINK_UNSUPPORTED"):
        activate_skills_checkout(checkout, REQUIRED_SKILLS)
