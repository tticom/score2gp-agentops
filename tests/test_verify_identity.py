from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts.verify_identity import (
    WORKSPACE_LOGINS,
    IdentityError,
    github_login,
    main,
    verify_git_identity,
    verify_identity,
    verify_workspace_login,
    workspace_slot,
)


def checkout(tmp_path: Path, slot: str, name: str = "score2gp-agentops") -> Path:
    path = tmp_path / "worktrees" / slot / name
    path.mkdir(parents=True)
    return path


def fake_runner(login="tticom-automation", author=None, committer=None, gh_code=0):
    author = author or f"{login} <{login}@example.com> 1790000000 +0100"
    committer = committer or author

    def run(command, **kwargs):
        if command[:2] == ["gh", "api"]:
            return SimpleNamespace(returncode=gh_code, stdout=login + "\n", stderr="")
        if command[-1] == "GIT_AUTHOR_IDENT":
            return SimpleNamespace(returncode=0, stdout=author + "\n", stderr="")
        if command[-1] == "GIT_COMMITTER_IDENT":
            return SimpleNamespace(returncode=0, stdout=committer + "\n", stderr="")
        raise AssertionError(f"unexpected command {command}")

    return run


@pytest.mark.parametrize("slot", sorted(WORKSPACE_LOGINS))
def test_workspace_slot_is_read_from_the_checkout_path(tmp_path, slot) -> None:
    assert workspace_slot(checkout(tmp_path, slot)) == slot


def test_task_worktree_beside_the_canonical_checkout_keeps_its_slot(tmp_path) -> None:
    assert workspace_slot(checkout(tmp_path, "gov", "score2gp-agentops-review")) == "gov"


@pytest.mark.parametrize(
    "relative",
    ["score2gp-agentops", "worktrees/score2gp-agentops", "worktrees/other/score2gp-agentops",
     "work/auto/score2gp-agentops", "worktrees/auto/nested/score2gp-agentops"],
)
def test_checkout_outside_the_workspace_layout_is_refused(tmp_path, relative) -> None:
    path = tmp_path / relative
    path.mkdir(parents=True)
    with pytest.raises(IdentityError, match="not under worktrees"):
        workspace_slot(path)


@pytest.mark.parametrize(("slot", "login"), sorted(WORKSPACE_LOGINS.items()))
def test_login_is_accepted_only_in_its_own_workspace(tmp_path, slot, login) -> None:
    assert verify_workspace_login(login, checkout(tmp_path, slot)) == slot
    for other in WORKSPACE_LOGINS.values():
        if other != login:
            with pytest.raises(IdentityError, match="may not operate"):
                verify_workspace_login(other, tmp_path / "worktrees" / slot / "score2gp-agentops")


def test_github_login_reads_gh() -> None:
    assert github_login(fake_runner("tticom-codex")) == "tticom-codex"


@pytest.mark.parametrize("runner", [
    fake_runner(gh_code=1),
    fake_runner(login=""),
])
def test_github_login_failure_is_closed(runner) -> None:
    with pytest.raises(IdentityError, match="GitHub identity check failed"):
        github_login(runner)


def test_missing_gh_is_closed() -> None:
    def missing(*args, **kwargs):
        raise FileNotFoundError("gh")

    with pytest.raises(IdentityError, match="could not run"):
        github_login(missing)


def test_git_identity_must_match_login(tmp_path) -> None:
    repo = checkout(tmp_path, "auto")
    assert verify_git_identity("tticom-automation", repo, fake_runner()) == "tticom-automation@example.com"
    wrong_author = fake_runner(author="tticom <t@example.com> 1790000000 +0100")
    with pytest.raises(IdentityError, match="Git author 'tticom' does not match"):
        verify_git_identity("tticom-automation", repo, wrong_author)
    wrong_committer = fake_runner(committer="tticom <t@example.com> 1790000000 +0100")
    with pytest.raises(IdentityError, match="Git committer 'tticom' does not match"):
        verify_git_identity("tticom-automation", repo, wrong_committer)


def test_git_identity_rejects_empty_or_split_email(tmp_path) -> None:
    repo = checkout(tmp_path, "auto")
    with pytest.raises(IdentityError, match="email is empty"):
        verify_git_identity("tticom-automation", repo,
                            fake_runner(author="tticom-automation <> 1790000000 +0100"))
    split = fake_runner(
        author="tticom-automation <a@example.com> 1790000000 +0100",
        committer="tticom-automation <b@example.com> 1790000000 +0100",
    )
    with pytest.raises(IdentityError, match="emails differ"):
        verify_git_identity("tticom-automation", repo, split)


def test_unconfigured_git_identity_is_closed(tmp_path) -> None:
    def unconfigured(command, **kwargs):
        return SimpleNamespace(returncode=128, stdout="", stderr="empty ident")

    with pytest.raises(IdentityError, match="not configured"):
        verify_git_identity("tticom-automation", checkout(tmp_path, "auto"), unconfigured)


def test_full_gate_reports_the_verified_identity(tmp_path) -> None:
    repo = checkout(tmp_path, "codex")
    result = verify_identity(repo, fake_runner("tticom-codex"))
    assert result == {
        "github_login": "tticom-codex",
        "workspace": "codex",
        "git_email": "tticom-codex@example.com",
        "checkout": str(repo.resolve()),
    }


def test_full_gate_refuses_login_in_wrong_workspace(tmp_path) -> None:
    with pytest.raises(IdentityError, match="belongs to tticom-automation"):
        verify_identity(checkout(tmp_path, "auto"), fake_runner("tticom-codex"))


def test_environment_role_does_not_change_the_gate(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("SCORE2GP_AGENT_ROLE", "gov")
    with pytest.raises(IdentityError, match="may not operate"):
        verify_identity(checkout(tmp_path, "gov"), fake_runner("tticom-automation"))


def test_cli_fails_closed_with_a_stable_prefix(tmp_path, monkeypatch, capsys) -> None:
    monkeypatch.setattr("scripts.verify_identity.subprocess.run", fake_runner(gh_code=1))
    assert main(["--checkout", str(checkout(tmp_path, "auto"))]) == 1
    assert capsys.readouterr().err.startswith("IDENTITY_GATE_FAILED: ")
