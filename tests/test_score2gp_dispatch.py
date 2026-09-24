import copy
import json
import sys
import pytest
from pathlib import Path
from types import SimpleNamespace


from scripts.score2gp_orchestrator import render_active_task
from scripts.score2gp_dispatch import (
    DispatchError,
    _authenticated_login,
    check_workspace_role,
    main,
    select_bootstrap,
    synchronize_agentops_main,
)

REPO = Path(__file__).resolve().parents[1]
ROLES = json.loads(
    (REPO / "projects/score2gp/ORCHESTRATION_STATE.json").read_text(encoding="utf-8")
)["roles"]
OWNERS = {"auto": "tticom-automation", "gov": "tticomgov-code", "codex": "tticom-codex"}
GO = "score2gp_go_bootstrap.py"
GOT = "score2gp_got_bootstrap.py"


@pytest.fixture(autouse=True)
def forbid_unexpected_github_lookup(monkeypatch):
    def unexpected(*args, **kwargs):
        pytest.fail("unexpected GitHub lookup")

    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", unexpected)


def checkout(tmp_path: Path, slot: str) -> Path:
    path = tmp_path / "worktrees" / slot / "score2gp-agentops"
    path.mkdir(parents=True)
    return path


def without_login(role: str, login: str) -> dict:
    roles = json.loads(json.dumps(ROLES))
    roles[role]["github_logins"].remove(login)
    return roles


@pytest.mark.parametrize(
    ("slot", "expected"), [("auto", GO), ("gov", GOT), ("codex", GOT)]
)
def test_each_login_routes_in_its_own_workspace(tmp_path, slot, expected) -> None:
    assert select_bootstrap(OWNERS[slot], checkout(tmp_path, slot), ROLES) == expected


def test_governance_login_has_a_route(tmp_path) -> None:
    # tticomgov-code was previously refused by the host-user router.
    assert select_bootstrap("tticomgov-code", checkout(tmp_path, "gov"), ROLES) == GOT


@pytest.mark.parametrize(
    ("slot", "login"),
    [(slot, login) for slot in OWNERS for login in OWNERS.values() if OWNERS[slot] != login],
)
def test_login_in_another_identitys_workspace_is_refused(tmp_path, slot, login) -> None:
    with pytest.raises(DispatchError, match="may not operate in worktrees"):
        select_bootstrap(login, checkout(tmp_path, slot), ROLES)


@pytest.mark.parametrize("slot", ["auto", "gov", "codex"])
@pytest.mark.parametrize("login", ["", "niall", "tticom", "tticom-orca", "tticom-gov", "agent"])
def test_unknown_login_is_refused(tmp_path, slot, login) -> None:
    with pytest.raises(DispatchError, match="unsupported Score2GP worker identity"):
        select_bootstrap(login, checkout(tmp_path, slot), ROLES)


@pytest.mark.parametrize("review_pr", [None, 667])
def test_checkout_outside_workspace_layout_is_refused(tmp_path, review_pr) -> None:
    outside = tmp_path / "score2gp-agentops"
    outside.mkdir()
    with pytest.raises(DispatchError, match="not under worktrees"):
        select_bootstrap("tticom-automation", outside, ROLES, review_pr=review_pr)


@pytest.mark.parametrize("slot", ["auto", "gov", "codex"])
def test_explicit_review_routes_reviewer_to_review_bootstrap(tmp_path, slot) -> None:
    assert select_bootstrap(OWNERS[slot], checkout(tmp_path, slot), ROLES, review_pr=667) == GOT


def test_explicit_review_requires_reviewer_role(tmp_path) -> None:
    roles = without_login("reviewer", "tticom-automation")
    with pytest.raises(DispatchError, match="lacks the reviewer role"):
        select_bootstrap("tticom-automation", checkout(tmp_path, "auto"), roles, review_pr=667)


def test_author_route_requires_implementation_role(tmp_path) -> None:
    roles = without_login("implementation", "tticom-automation")
    with pytest.raises(DispatchError, match="lacks the implementation role"):
        select_bootstrap("tticom-automation", checkout(tmp_path, "auto"), roles)


def test_review_route_requires_reviewer_or_governance_role(tmp_path) -> None:
    roles = without_login("reviewer", "tticomgov-code")
    roles["governance"]["github_logins"].remove("tticomgov-code")
    with pytest.raises(DispatchError, match="lacks the reviewer and governance roles"):
        select_bootstrap("tticomgov-code", checkout(tmp_path, "gov"), roles)


@pytest.mark.parametrize("value", ["automation", "gov", "reviewer", "governance"])
@pytest.mark.parametrize(("slot", "expected"), [("auto", GO), ("gov", GOT), ("codex", GOT)])
def test_environment_role_is_never_obeyed(tmp_path, monkeypatch, value, slot, expected) -> None:
    monkeypatch.setenv("SCORE2GP_AGENT_ROLE", value)
    assert select_bootstrap(OWNERS[slot], checkout(tmp_path, slot), ROLES) == expected


def test_environment_role_does_not_admit_unknown_login(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("SCORE2GP_AGENT_ROLE", "automation")
    with pytest.raises(DispatchError, match="unsupported Score2GP worker identity"):
        select_bootstrap("agent", checkout(tmp_path, "auto"), ROLES)


def test_authenticated_login_is_read_from_github(monkeypatch) -> None:
    calls = []

    def lookup(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0, stdout="tticom-automation\n")

    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", lookup)
    assert _authenticated_login() == "tticom-automation"
    assert calls == [(["gh", "api", "user", "--jq", ".login"],
                      {"capture_output": True, "text": True})]


def test_empty_login_is_closed(monkeypatch) -> None:
    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", lambda *a, **k:
                        SimpleNamespace(returncode=0, stdout="\n"))
    with pytest.raises(DispatchError, match="GitHub identity check failed"):
        _authenticated_login()


def test_authentication_failure_is_closed(monkeypatch) -> None:
    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", lambda *a, **k:
                        SimpleNamespace(returncode=1, stdout="tticom-automation", stderr=""))
    with pytest.raises(DispatchError, match="GitHub identity check failed"):
        _authenticated_login()


def test_missing_gh_is_closed(monkeypatch) -> None:
    def missing(*args, **kwargs):
        raise FileNotFoundError("gh")

    monkeypatch.setattr("scripts.score2gp_dispatch.subprocess.run", missing)
    with pytest.raises(DispatchError, match="GitHub identity check failed"):
        _authenticated_login()


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


@pytest.mark.parametrize(
    ("slot", "role"),
    [("auto", "implementation"), ("auto", "architect"),
     ("gov", "governance"), ("gov", "reviewer"),
     ("codex", "governance"), ("codex", "reviewer")],
)
def test_slot_allows_its_roles(tmp_path, slot, role) -> None:
    assert check_workspace_role(OWNERS[slot], checkout(tmp_path, slot), role) == slot


@pytest.mark.parametrize(
    ("slot", "role"),
    [("auto", "reviewer"), ("auto", "governance"),
     ("gov", "implementation"), ("gov", "architect"),
     ("codex", "implementation"), ("codex", "architect")],
)
def test_slot_refuses_other_roles(tmp_path, slot, role) -> None:
    with pytest.raises(DispatchError, match=f"worktrees/{slot} may not run the {role} role"):
        check_workspace_role(OWNERS[slot], checkout(tmp_path, slot), role)


@pytest.mark.parametrize("slot", ["auto", "gov", "codex"])
def test_explicit_review_may_run_reviewer_from_any_slot(tmp_path, slot) -> None:
    assert check_workspace_role(
        OWNERS[slot], checkout(tmp_path, slot), "reviewer", explicit_review=True
    ) == slot


def test_explicit_review_does_not_widen_to_implementation(tmp_path) -> None:
    with pytest.raises(DispatchError, match="may not run the implementation role"):
        check_workspace_role(
            "tticom-codex", checkout(tmp_path, "codex"), "implementation", explicit_review=True
        )


def live_authority() -> dict:
    return json.loads(
        (REPO / "projects/score2gp/ORCHESTRATION_STATE.json").read_text(encoding="utf-8")
    )


def orca_checkout(tmp_path: Path, slot: str, authority: dict | None = None) -> Path:
    # A self-contained authority whose active task is a promoted implementation
    # task, so these tests do not depend on the live task's current status.
    fixture = copy.deepcopy(authority if authority is not None else live_authority())
    fixture["task"] = {
        **fixture["task"],
        "id": "ORCA-FIXTURE",
        "status": "PROMOTED",
        "owner_role": "implementation",
        "branch": "feat/orca-fixture",
        "pull_request": None,
    }
    agentops = checkout(tmp_path, slot)
    project = agentops / "projects/score2gp"
    project.mkdir(parents=True)
    (project / "ORCHESTRATION_STATE.json").write_text(json.dumps(fixture, indent=2), encoding="utf-8")
    (project / "ACTIVE_TASK.md").write_text(render_active_task(fixture), encoding="utf-8")
    (tmp_path / "live.json").write_text("{}", encoding="utf-8")
    return agentops


def run_orca_main(monkeypatch, agentops: Path, login: str, role: str) -> None:
    monkeypatch.setattr("scripts.score2gp_orca_control.authenticated_github_login", lambda: login)
    monkeypatch.setattr("scripts.score2gp_orca_control.git_head", lambda root: "e" * 40)
    monkeypatch.setattr(sys, "argv", [
        "score2gp_dispatch.py", "--agentops", str(agentops), "--orca-role", role,
        "--live", str(agentops.parents[2] / "live.json"), "--github-login", login,
    ])
    main()


def test_orca_path_assigns_implementation_in_the_author_workspace(tmp_path, monkeypatch, capsys) -> None:
    agentops = orca_checkout(tmp_path, "auto")
    run_orca_main(monkeypatch, agentops, "tticom-automation", "implementation")
    assignment = json.loads(capsys.readouterr().out)
    assert assignment["worker"]["github_login"] == "tticom-automation"
    assert assignment["worker"]["role"] == "implementation"


def test_orca_path_does_not_depend_on_the_live_task_status(tmp_path, monkeypatch, capsys) -> None:
    completed = live_authority()
    completed["task"]["status"] = "COMPLETED"
    agentops = orca_checkout(tmp_path, "auto", completed)
    run_orca_main(monkeypatch, agentops, "tticom-automation", "implementation")
    assignment = json.loads(capsys.readouterr().out)
    assert assignment["worker"]["role"] == "implementation"


def test_orca_path_refuses_implementation_in_the_codex_workspace(tmp_path, monkeypatch, capsys) -> None:
    # tticom-codex holds the implementation role, but its workspace may not run it.
    agentops = orca_checkout(tmp_path, "codex")
    with pytest.raises(DispatchError, match="worktrees/codex may not run the implementation role"):
        run_orca_main(monkeypatch, agentops, "tticom-codex", "implementation")
    assert capsys.readouterr().out == ""


def test_orca_path_refuses_login_in_another_identitys_workspace(tmp_path, monkeypatch, capsys) -> None:
    agentops = orca_checkout(tmp_path, "gov")
    with pytest.raises(DispatchError, match="may not operate in worktrees/gov"):
        run_orca_main(monkeypatch, agentops, "tticom-automation", "implementation")
    assert capsys.readouterr().out == ""
