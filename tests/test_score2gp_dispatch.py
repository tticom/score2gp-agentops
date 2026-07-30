import pytest

from scripts.score2gp_dispatch import DispatchError, select_bootstrap


def test_automation_worker_routes_to_author_bootstrap() -> None:
    assert select_bootstrap("tticom-automation") == "score2gp_go_bootstrap.py"


@pytest.mark.parametrize("linux_user", ["tticom-gov", "tticom-codex"])
def test_governance_worker_routes_to_governance_bootstrap(linux_user: str) -> None:
    assert select_bootstrap(linux_user) == "score2gp_got_bootstrap.py"


def test_unknown_worker_fails_closed() -> None:
    with pytest.raises(DispatchError, match="unsupported Score2GP worker identity"):
        select_bootstrap("tticom")
