import pytest
from pathlib import Path
from types import SimpleNamespace

from scripts.score2gp_dispatch import (
    DispatchError,
    select_bootstrap,
    synchronize_agentops_main,
)


def test_automation_worker_routes_to_author_bootstrap() -> None:
    assert select_bootstrap("tticom-automation") == "score2gp_go_bootstrap.py"


def test_governance_worker_routes_to_governance_bootstrap() -> None:
    assert select_bootstrap("tticom-gov") == "score2gp_got_bootstrap.py"


def test_unknown_worker_fails_closed() -> None:
    with pytest.raises(DispatchError, match="unsupported Score2GP worker identity"):
        select_bootstrap("tticom")


def test_publishing_identity_is_not_a_linux_worker() -> None:
    with pytest.raises(DispatchError):
        select_bootstrap("tticomgov-code")


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
