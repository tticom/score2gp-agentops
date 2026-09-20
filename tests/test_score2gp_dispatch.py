import pytest
from pathlib import Path
from types import SimpleNamespace

from scripts.score2gp_dispatch import (
    DispatchError,
    select_bootstrap,
    synchronize_agentops_main,
)


@pytest.fixture(autouse=True)
def forbid_unexpected_github_lookup(monkeypatch):
    def unexpected(*args, **kwargs):
        pytest.fail("unexpected GitHub lookup")

    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", unexpected)


def test_automation_worker_routes_to_author_bootstrap() -> None:
    assert select_bootstrap("tticom-automation") == "score2gp_go_bootstrap.py"


def test_orca_worker_routes_to_author_bootstrap() -> None:
    assert select_bootstrap("tticom-orca") == "score2gp_go_bootstrap.py"


def test_automation_explicit_review_routes_to_reviewer_bootstrap() -> None:
    assert select_bootstrap("tticom-automation", review_pr=667) == "score2gp_got_bootstrap.py"


def test_orca_explicit_review_routes_to_reviewer_bootstrap() -> None:
    assert select_bootstrap("tticom-orca", review_pr=667) == "score2gp_got_bootstrap.py"


def test_automation_container_routes_from_attested_role(monkeypatch) -> None:
    monkeypatch.setenv("SCORE2GP_AGENT_ROLE", "automation")
    assert select_bootstrap("agent") == "score2gp_go_bootstrap.py"


def test_governance_container_routes_from_attested_role(monkeypatch) -> None:
    monkeypatch.setenv("SCORE2GP_AGENT_ROLE", "gov")
    assert select_bootstrap("agent") == "score2gp_got_bootstrap.py"


def test_unknown_container_role_still_fails_closed(monkeypatch) -> None:
    monkeypatch.setenv("SCORE2GP_AGENT_ROLE", "")
    with pytest.raises(DispatchError, match="unsupported Score2GP worker identity"):
        select_bootstrap("agent")


def test_governance_worker_routes_to_governance_bootstrap() -> None:
    assert select_bootstrap("tticom-gov") == "score2gp_got_bootstrap.py"


def test_personal_worker_routes_to_governance_bootstrap() -> None:
    assert select_bootstrap("tticom") == "score2gp_got_bootstrap.py"


def test_codex_worker_routes_to_governance_bootstrap() -> None:
    assert select_bootstrap("tticom-codex") == "score2gp_got_bootstrap.py"


@pytest.mark.parametrize("host", ["niall", "unknown-user", "tticomgov-code"])
@pytest.mark.parametrize("login", ["tticom-automation", "tticom-gov", "tticom-codex"])
def test_native_worker_routes_from_authenticated_github(monkeypatch, host, login):
    calls = []

    def lookup(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0, stdout=login + "\n")

    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", lookup)
    expected = "go" if login == "tticom-automation" else "got"
    assert select_bootstrap(host) == f"score2gp_{expected}_bootstrap.py"
    assert calls == [(["gh", "api", "user", "--jq", ".login"],
                      {"capture_output": True, "text": True})]


@pytest.mark.parametrize("login", ["", "niall", "tticom", "tticom-orca", "tticomgov-code"])
@pytest.mark.parametrize("role", ["automation", "gov"])
def test_native_worker_rejects_unsupported_login_despite_role(monkeypatch, login, role):
    monkeypatch.setenv("SCORE2GP_AGENT_ROLE", role)
    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", lambda *a, **k:
                        SimpleNamespace(returncode=0, stdout=login))
    with pytest.raises(DispatchError, match="unsupported Score2GP worker identity"):
        select_bootstrap("niall")


def test_native_worker_authentication_failure_is_closed(monkeypatch):
    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", lambda *a, **k:
                        SimpleNamespace(returncode=1, stdout="tticom-automation"))
    with pytest.raises(DispatchError, match="GitHub identity check failed"):
        select_bootstrap("niall")


def test_native_worker_missing_gh_is_closed(monkeypatch):
    def missing(*args, **kwargs):
        raise FileNotFoundError("gh")

    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", missing)
    with pytest.raises(DispatchError, match="GitHub identity check could not run"):
        select_bootstrap("niall")


def test_native_explicit_review_routes_to_reviewer_without_fallback():
    assert select_bootstrap("niall", review_pr=667) == "score2gp_got_bootstrap.py"


def test_dispatcher_fast_forwards_clean_agentops_main() -> None:
    calls: list[list[str]] = []

    def runner(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    synchronize_agentops_main(Path("/canonical/agentops"), runner=runner)
    assert calls == [
        ["git", "status", "--porcelain"],
        ["git", "fetch", "origin"],
        ["git", "switch", "main"],
        ["git", "merge", "--ff-only", "origin/main"],
    ]


def test_dispatcher_refuses_dirty_checkout_before_fetch() -> None:
    calls: list[list[str]] = []

    def runner(command: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(command)
        return SimpleNamespace(returncode=0, stdout=" M AGENTS.md", stderr="")

    with pytest.raises(DispatchError, match="checkout is dirty"):
        synchronize_agentops_main(Path("/canonical/agentops"), runner=runner)
    assert calls == [["git", "status", "--porcelain"]]
