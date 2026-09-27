"""CP-13: a task may name its author login, and review stays crossed.

The fixtures are fixed and self-contained. They never read the repository's
live ORCHESTRATION_STATE.json, so a later promotion cannot change these
assertions.
"""
from copy import deepcopy
import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from scripts.score2gp_dispatch import (
    SLOT_ROLES,
    DispatchError,
    check_workspace_role,
    main,
    select_bootstrap,
)
from scripts.score2gp_orca_control import (
    ControlError,
    RuntimeIdentity,
    build_assignment,
    derive_governance_go,
    resolve_state,
    validate_authority,
    verify_merge_gate,
)
from scripts.score2gp_orchestrator import render_active_task

AUTO, GOV, CODEX = "tticom-automation", "tticomgov-code", "tticom-codex"
OWNERS = {"auto": AUTO, "gov": GOV, "codex": CODEX}
GO = "score2gp_go_bootstrap.py"
GOT = "score2gp_got_bootstrap.py"
SHA = "e" * 40
HEAD = "a" * 40

# The roles as recorded when CP-13 was promoted (authority revision 60).
ROLES = {
    "implementation": {
        "github_logins": [AUTO, CODEX],
        "allowed_actions": ["edit", "test", "commit", "push_task_branch", "publish_handback"],
        "forbidden_actions": ["review", "approve", "merge", "governance_edit"],
    },
    "architect": {
        "github_logins": [CODEX, AUTO],
        "allowed_actions": ["governance_edit", "test", "commit", "push_task_branch", "publish_handback"],
        "forbidden_actions": ["review_own_work", "approve_own_work", "merge", "product_edit"],
    },
    "reviewer": {
        "github_logins": [CODEX, GOV, AUTO],
        "allowed_actions": ["inspect", "test", "publish_review"],
        "forbidden_actions": ["edit", "commit", "push", "merge"],
    },
    "governance": {
        "github_logins": [GOV, "tticom"],
        "allowed_actions": ["governance_edit", "publish_governance_review", "promote_task"],
        "forbidden_actions": ["product_edit", "merge"],
    },
    "supervisor": {"github_logins": ["tticom"], "allowed_actions": ["dispatch"], "forbidden_actions": ["merge"]},
    "merge_controller": {
        "github_logins": [CODEX, GOV],
        "allowed_actions": ["verify_merge_gate", "merge_exact_head"],
        "forbidden_actions": ["edit", "review", "approve", "bypass"],
    },
}

TASK = {
    "id": "CP-13-FIXTURE",
    "title": "Author lane fixture task",
    "objective": "Exercise author assignment.",
    "status": "PROMOTED",
    "repository": "tticom/score2gp-agentops",
    "base_branch": "main",
    "branch": "feat/cp-13-fixture",
    "pull_request": None,
    "owner_role": "implementation",
    "reviewer_role": "reviewer",
    "delivery_action": "pull_request",
    "prompt": "projects/score2gp/prompts/next/cp-13-fixture.md",
    "allowed_paths": ["scripts/fixture.py"],
    "acceptance": ["Author assignment is exercised."],
    "validation_commands": ["python -m pytest"],
    "dependencies": [],
    "stop_conditions": [],
}


def authority(author_login: str | None = None, **task_overrides) -> dict:
    task = {**deepcopy(TASK), **task_overrides}
    if author_login is not None:
        task["author_login"] = author_login
    return {
        "schema_version": 2,
        "project": "score2gp",
        "authority_revision": 60,
        "task": task,
        "next_task_proposal": None,
        "queued_task_proposals": [],
        "incidents": [],
        "roles": deepcopy(ROLES),
        "merge_policy": {
            "required_checks": ["deterministic-control-plane"],
            "minimum_approvals": 1,
            "require_governance_go": True,
            "require_reviewed_head": True,
            "require_resolved_threads": True,
            "allow_admin_bypass": False,
        },
        "completed_tasks": [],
    }


def identity(login: str) -> RuntimeIdentity:
    return RuntimeIdentity("worker", login)


def open_pr(author: str, reviews: list[dict] | None = None) -> dict:
    return {
        "snapshot": {"repository": TASK["repository"]},
        "pull_request": {
            "number": 713,
            "state": "OPEN",
            "head_branch": TASK["branch"],
            "base_branch": "main",
            "head_sha": HEAD,
            "author": author,
            "reviews": reviews or [],
            "checks": [{"name": "deterministic-control-plane", "conclusion": "SUCCESS"}],
            "unresolved_threads": 0,
        },
        "protection": {"active_rulesets": 1, "current_user_can_bypass": False},
        "admin_bypass": False,
    }


def checkout(tmp_path: Path, slot: str) -> Path:
    path = tmp_path / "worktrees" / slot / "score2gp-agentops"
    path.mkdir(parents=True)
    return path


# --- 1. Slot roles -----------------------------------------------------------


def test_codex_slot_allows_author_roles_and_other_slots_are_unchanged() -> None:
    assert SLOT_ROLES["codex"] == {"governance", "reviewer", "architect", "implementation"}
    assert SLOT_ROLES["auto"] == {"implementation", "architect"}
    assert SLOT_ROLES["gov"] == {"governance", "reviewer"}


@pytest.mark.parametrize("role", ["implementation", "architect"])
def test_codex_slot_runs_an_author_role_only_for_a_task_assigned_to_codex(tmp_path, role) -> None:
    agentops = checkout(tmp_path, "codex")
    assert check_workspace_role(CODEX, agentops, role, author_login=CODEX) == "codex"
    for assigned in (None, AUTO):
        with pytest.raises(DispatchError, match=f"worktrees/codex may not run the {role} role"):
            check_workspace_role(CODEX, agentops, role, author_login=assigned)


def test_author_assignment_never_admits_a_login_outside_its_workspace(tmp_path) -> None:
    with pytest.raises(DispatchError, match="may not operate in worktrees/auto"):
        check_workspace_role(CODEX, checkout(tmp_path, "auto"), "implementation", author_login=CODEX)
    with pytest.raises(DispatchError, match="worktrees/gov may not run the implementation role"):
        check_workspace_role(GOV, checkout(tmp_path, "gov"), "implementation", author_login=GOV)


# --- 2. Author assignment ----------------------------------------------------


@pytest.mark.parametrize("login", [AUTO, CODEX])
def test_authority_accepts_an_author_login_holding_the_owner_role(login) -> None:
    validate_authority(authority(login))


@pytest.mark.parametrize("login", [GOV, "tticom", "stranger", "", 7])
def test_authority_rejects_an_author_login_outside_the_owner_role(login) -> None:
    with pytest.raises(ControlError, match="author_login"):
        validate_authority(authority(login))


def test_author_login_is_checked_against_the_tasks_own_owner_role() -> None:
    config = authority(CODEX, owner_role="architect")
    validate_authority(config)
    config["roles"]["architect"]["github_logins"] = [AUTO]
    with pytest.raises(ControlError, match="author_login tticom-codex .* architect"):
        validate_authority(config)


@pytest.mark.parametrize("where", ["next_task_proposal", "queued_task_proposals"])
def test_proposals_are_validated_like_the_task(where) -> None:
    config = authority()
    proposal = {**deepcopy(TASK), "id": "NEXT-1", "branch": "feat/next-1", "status": "PROPOSED",
                "author_login": GOV}
    config[where] = [proposal] if where == "queued_task_proposals" else proposal
    with pytest.raises(ControlError, match="NEXT-1 author_login tticomgov-code"):
        validate_authority(config)
    proposal["author_login"] = CODEX
    validate_authority(config)


def test_resolution_names_the_assigned_author_only_when_one_is_set() -> None:
    assigned = resolve_state(authority(CODEX), {})
    assert assigned["dispatch_role"] == "implementation"
    assert assigned["author_login"] == CODEX
    assert "author_login" not in resolve_state(authority(), {})


def test_assignment_goes_only_to_the_assigned_author() -> None:
    config = authority(CODEX)
    resolved = resolve_state(config, {})
    assignment = build_assignment(config, {}, resolved, identity(CODEX), SHA)
    assert assignment["worker"] == {"role": "implementation", "os_user": "worker", "github_login": CODEX}
    assert assignment["work"]["author_login"] == CODEX
    with pytest.raises(ControlError, match="assigned to tticom-codex"):
        build_assignment(config, {}, resolved, identity(AUTO), SHA)


def test_assigned_author_is_enforced_even_when_resolution_omits_it() -> None:
    config = authority(CODEX)
    resolved = {k: v for k, v in resolve_state(config, {}).items() if k != "author_login"}
    with pytest.raises(ControlError, match="assigned to tticom-codex"):
        build_assignment(config, {}, resolved, identity(AUTO), SHA)


def test_changes_requested_on_an_assigned_task_return_to_its_author() -> None:
    config = authority(CODEX, pull_request=713, status="RUNNING")
    review = {"author": AUTO, "state": "CHANGES_REQUESTED", "head_sha": HEAD}
    live = open_pr(CODEX, [review])
    resolved = resolve_state(config, live)
    assert (resolved["state"], resolved["dispatch_role"], resolved["author_login"]) == (
        "RUNNING", "implementation", CODEX)
    assert build_assignment(config, live, resolved, identity(CODEX), SHA)["work"]["expected_head_sha"] == HEAD
    with pytest.raises(ControlError, match="assigned to tticom-codex"):
        build_assignment(config, live, resolved, identity(AUTO), SHA)


def test_a_discovered_pr_on_an_assigned_task_must_be_by_the_assigned_author() -> None:
    config = authority(CODEX)
    for author, reason in ((AUTO, "active_task_pr_author_not_assigned_author"), (CODEX, None)):
        live = open_pr(author)
        live["pr_binding"] = "discovered"
        live["discovery"] = {
            "repository": TASK["repository"], "branch": TASK["branch"], "base_branch": "main",
            "candidates": [{"number": 713, "state": "OPEN", "head_branch": TASK["branch"],
                            "base_branch": "main", "author": author, "cross_repository": False}],
        }
        resolved = resolve_state(config, live)
        if reason:
            assert (resolved["state"], resolved["reason"]) == ("BLOCKED", reason)
        else:
            assert resolved["state"] == "REVIEW_REQUIRED"


# --- 3. Self-review and self-merge stay refused --------------------------------


def test_codex_may_not_review_the_pr_it_authored() -> None:
    config = authority(CODEX, pull_request=713, status="RUNNING")
    live = open_pr(CODEX)
    resolved = resolve_state(config, live)
    assert resolved["dispatch_role"] == "reviewer"
    with pytest.raises(ControlError, match="self-review is forbidden"):
        build_assignment(config, live, resolved, identity(CODEX), SHA)
    for reviewer in (AUTO, GOV):
        assert build_assignment(config, live, resolved, identity(reviewer), SHA)["worker"]["role"] == "reviewer"


def test_codex_may_not_merge_the_pr_it_authored() -> None:
    config = authority(CODEX, pull_request=713, status="RUNNING")
    facts = open_pr(CODEX, [{"author": AUTO, "state": "APPROVED", "head_sha": HEAD}])
    facts["governance"] = derive_governance_go(config, facts)

    by_author = {**facts, "merge_controller_login": CODEX}
    decision = verify_merge_gate(config, by_author)
    assert decision["decision"] == "DENY"
    assert "merge_controller_is_pr_author" in decision["failures"]

    by_other = {**facts, "merge_controller_login": GOV}
    assert verify_merge_gate(config, by_other)["decision"] == "ALLOW"


def test_codex_self_approval_does_not_count_toward_its_merge() -> None:
    config = authority(CODEX, pull_request=713, status="RUNNING")
    facts = open_pr(CODEX, [{"author": CODEX, "state": "APPROVED", "head_sha": HEAD}])
    facts["governance"] = derive_governance_go(config, facts)
    facts["merge_controller_login"] = GOV
    failures = verify_merge_gate(config, facts)["failures"]
    assert "insufficient_independent_approvals" in failures
    assert "governance_go_missing" in failures


# --- 4. Routing --------------------------------------------------------------


def orca_checkout(tmp_path: Path, slot: str, config: dict) -> Path:
    agentops = checkout(tmp_path, slot)
    project = agentops / "projects/score2gp"
    project.mkdir(parents=True)
    (project / "ORCHESTRATION_STATE.json").write_text(json.dumps(config, indent=2), encoding="utf-8")
    (project / "ACTIVE_TASK.md").write_text(render_active_task(config), encoding="utf-8")
    (tmp_path / "live.json").write_text("{}", encoding="utf-8")
    return agentops


def run_orca_main(monkeypatch, agentops: Path, login: str, role: str = "implementation") -> None:
    monkeypatch.setattr("scripts.score2gp_orca_control.authenticated_github_login", lambda: login)
    monkeypatch.setattr("scripts.score2gp_orca_control.git_head", lambda root: SHA)
    monkeypatch.setattr(sys, "argv", [
        "score2gp_dispatch.py", "--agentops", str(agentops), "--orca-role", role,
        "--live", str(agentops.parents[2] / "live.json"), "--github-login", login,
    ])
    main()


def test_task_assigned_to_codex_is_authorised_in_the_codex_workspace(tmp_path, monkeypatch, capsys) -> None:
    run_orca_main(monkeypatch, orca_checkout(tmp_path, "codex", authority(CODEX)), CODEX)
    assignment = json.loads(capsys.readouterr().out)
    assert assignment["worker"]["github_login"] == CODEX
    assert assignment["worker"]["role"] == "implementation"
    assert assignment["work"]["author_login"] == CODEX


def test_task_assigned_to_codex_is_refused_in_the_auto_workspace(tmp_path, monkeypatch, capsys) -> None:
    with pytest.raises(SystemExit) as stopped:
        run_orca_main(monkeypatch, orca_checkout(tmp_path, "auto", authority(CODEX)), AUTO)
    assert stopped.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is False
    assert out["state"] == "ASSIGNED_TO_ANOTHER_AUTHOR"
    assert out["assigned_author"] == CODEX
    assert out["github_login"] == AUTO
    assert out["task_id"] == TASK["id"]
    assert "worktrees/codex" in out["next_action"]
    assert "assignment_type" not in out


def test_task_assigned_to_automation_is_refused_in_the_codex_workspace(tmp_path, monkeypatch, capsys) -> None:
    with pytest.raises(SystemExit) as stopped:
        run_orca_main(monkeypatch, orca_checkout(tmp_path, "codex", authority(AUTO)), CODEX)
    assert stopped.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert (out["state"], out["assigned_author"]) == ("ASSIGNED_TO_ANOTHER_AUTHOR", AUTO)


def test_assignment_does_not_bypass_the_workspace_identity_gate(tmp_path, monkeypatch, capsys) -> None:
    with pytest.raises(DispatchError, match="may not operate in worktrees/auto"):
        run_orca_main(monkeypatch, orca_checkout(tmp_path, "auto", authority(CODEX)), CODEX)
    assert capsys.readouterr().out == ""


def test_unassigned_task_keeps_todays_routing(tmp_path, monkeypatch, capsys) -> None:
    run_orca_main(monkeypatch, orca_checkout(tmp_path / "a", "auto", authority()), AUTO)
    assert json.loads(capsys.readouterr().out)["worker"]["github_login"] == AUTO
    with pytest.raises(DispatchError, match="worktrees/codex may not run the implementation role"):
        run_orca_main(monkeypatch, orca_checkout(tmp_path / "c", "codex", authority()), CODEX)
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    ("slot", "author_login", "expected"),
    [("auto", None, GO), ("gov", None, GOT), ("codex", None, GOT),
     ("auto", CODEX, GO), ("codex", CODEX, GO), ("codex", AUTO, GOT), ("gov", CODEX, GOT)],
)
def test_legacy_router_sends_the_assigned_author_to_the_author_bootstrap(
    tmp_path, slot, author_login, expected
) -> None:
    assert select_bootstrap(OWNERS[slot], checkout(tmp_path, slot), ROLES, author_login=author_login) == expected


def test_explicit_review_still_routes_the_assigned_author_to_review(tmp_path) -> None:
    assert select_bootstrap(CODEX, checkout(tmp_path, "codex"), ROLES, review_pr=713, author_login=CODEX) == GOT


def test_characterisation_unassigned_resolution_and_assignment_are_unchanged() -> None:
    # Pinned before CP-13: an unassigned task's resolution and assignment.
    config = authority()
    resolved = resolve_state(config, {})
    assert resolved == {
        "schema_version": 1,
        "state": "READY",
        "reason": "authorised_task_without_pr",
        "task_id": TASK["id"],
        "dispatch_role": "implementation",
    }
    assignment = build_assignment(config, {}, resolved, identity(AUTO), SHA)
    assert assignment["work"] == {
        "goal": TASK["title"],
        "repository": TASK["repository"],
        "branch": TASK["branch"],
        "pull_request": None,
        "expected_head_sha": None,
        "prompt": TASK["prompt"],
        "allowed_paths": TASK["allowed_paths"],
        "acceptance": TASK["acceptance"],
        "required_evidence": [],
    }
    # Both implementation logins may still be assigned an unassigned task by the resolver;
    # the workspace gate is what keeps it in worktrees/auto.
    assert build_assignment(config, {}, resolved, identity(CODEX), SHA)["worker"]["github_login"] == CODEX


def test_characterisation_current_cp_13_task_resolution_is_unchanged() -> None:
    # The CP-13 task as promoted at authority revision 60 declares no author_login.
    config = authority(
        id="CP-13", title="Let Codex author assigned tasks, with crossed review",
        branch="feat/cp-13-codex-author-lane",
        prompt="projects/score2gp/prompts/next/cp-13-codex-author-lane.md",
    )
    assert resolve_state(config, {}) == {
        "schema_version": 1,
        "state": "READY",
        "reason": "authorised_task_without_pr",
        "task_id": "CP-13",
        "dispatch_role": "implementation",
    }


# --- 5. Review of 26c8825: recorded PRs and the architect author lane -----------


@pytest.mark.parametrize("review", [None, "APPROVED", "CHANGES_REQUESTED"])
def test_a_recorded_pr_on_an_assigned_task_must_be_by_the_assigned_author(review) -> None:
    config = authority(CODEX, pull_request=713, status="RUNNING")
    reviews = [{"author": GOV, "state": review, "head_sha": HEAD}] if review else []
    blocked = resolve_state(config, open_pr(AUTO, reviews))
    assert (blocked["state"], blocked["reason"]) == ("BLOCKED", "active_task_pr_author_not_assigned_author")
    assert "dispatch_role" not in blocked
    # Negative control: the same PR by the assigned author routes normally.
    assert resolve_state(config, open_pr(CODEX, reviews))["state"] != "BLOCKED"


def test_a_merged_recorded_pr_not_by_the_assigned_author_is_blocked() -> None:
    config = authority(CODEX, pull_request=713, status="RUNNING")
    live = open_pr(AUTO)
    live["pull_request"]["state"] = "MERGED"
    resolved = resolve_state(config, live)
    assert (resolved["state"], resolved["reason"]) == ("BLOCKED", "active_task_pr_author_not_assigned_author")


def merge_facts(config: dict, author: str, approver: str, merger: str) -> dict:
    facts = open_pr(author, [{"author": approver, "state": "APPROVED", "head_sha": HEAD}])
    facts["governance"] = derive_governance_go(config, facts)
    facts["merge_controller_login"] = merger
    return facts


def test_merge_gate_denies_a_recorded_pr_not_by_the_assigned_author() -> None:
    config = authority(CODEX, pull_request=713, status="RUNNING")
    decision = verify_merge_gate(config, merge_facts(config, AUTO, CODEX, GOV))
    assert decision["decision"] == "DENY"
    assert decision["failures"] == ["pr_author_not_assigned_author"]
    # Negative control: the assigned author's PR, independently approved, is allowed.
    assert verify_merge_gate(config, merge_facts(config, CODEX, AUTO, GOV))["decision"] == "ALLOW"


@pytest.mark.parametrize("author", [AUTO, CODEX])
def test_an_unassigned_task_accepts_either_implementation_author(author) -> None:
    config = authority(pull_request=713, status="RUNNING")
    assert resolve_state(config, open_pr(author))["state"] == "REVIEW_REQUIRED"
    approver = CODEX if author == AUTO else AUTO
    assert verify_merge_gate(config, merge_facts(config, author, approver, GOV))["decision"] == "ALLOW"


class GoRunner:
    """Scripted subprocess.run for the go bootstrap; resolves with the real resolver."""

    def __init__(self, login: str):
        self.login = login
        self.dispatched: list[tuple[list[str], dict]] = []

    def __call__(self, command, **kwargs):
        command = [str(part) for part in command]

        def done(stdout=""):
            return SimpleNamespace(returncode=0, stdout=stdout, stderr="")

        if command[0] == "git":
            return done()
        if command[:3] == ["gh", "api", "user"]:
            return done(self.login + "\n")
        if "task-live" in command:
            return done(json.dumps({"discovery": {
                "repository": TASK["repository"], "branch": TASK["branch"], "base_branch": "main",
                "candidates": [], "branch_ahead_by": 0}}))
        if "resolve" in command:
            config = json.loads(Path(command[command.index("--authority") + 1]).read_text(encoding="utf-8"))
            live = json.loads(Path(command[command.index("--live") + 1]).read_text(encoding="utf-8"))
            return done(json.dumps(resolve_state(config, live)))
        if command[1].endswith("score2gp_dispatch.py"):
            live = json.loads(Path(command[command.index("--live") + 1]).read_text(encoding="utf-8"))
            self.dispatched.append((command, live))
            return done()
        raise AssertionError(f"unexpected command {command}")


def run_legacy_router(monkeypatch, agentops: Path, login: str) -> list[str]:
    """Run ``score2gp_dispatch.py`` without --orca-role and return the bootstrap command it launches."""
    import scripts.score2gp_dispatch as dispatch

    launched: list[list[str]] = []

    def launch(command, **kwargs):
        launched.append([str(part) for part in command])
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(dispatch, "_authenticated_login", lambda: login)
    monkeypatch.setattr(dispatch, "verify_git_identity", lambda login, path: None)
    monkeypatch.setattr(dispatch, "synchronize_agentops_main", lambda path: None)
    with monkeypatch.context() as patch:
        patch.setattr(dispatch.subprocess, "run", launch)
        patch.setattr(sys, "argv", ["score2gp_dispatch.py", "--agentops", str(agentops),
                                    "--product", str(agentops.parent / "score2gp"), "--json"])
        with pytest.raises(SystemExit) as stopped:
            main()
    assert stopped.value.code == 0
    [command] = launched
    return command


def run_go_bootstrap(monkeypatch, agentops: Path, login: str) -> tuple[int, GoRunner]:
    from scripts import score2gp_go_bootstrap

    runner = GoRunner(login)
    with monkeypatch.context() as patch:
        patch.setattr("subprocess.run", runner)
        patch.setattr(sys, "argv", ["score2gp_go_bootstrap.py", "--agentops", str(agentops),
                                    "--product", str(agentops.parent / "score2gp"), "--json"])
        with pytest.raises(SystemExit) as stopped:
            score2gp_go_bootstrap.main()
    return stopped.value.code, runner


def run_dispatched_orca_path(monkeypatch, tmp_path: Path, dispatched: list[str], live: dict, login: str) -> None:
    """Run the Orca command the go bootstrap launched, exactly as it was built."""
    live_file = tmp_path / "dispatched-live.json"
    live_file.write_text(json.dumps(live), encoding="utf-8")
    dispatched = list(dispatched)
    dispatched[dispatched.index("--live") + 1] = str(live_file)
    monkeypatch.setattr("scripts.score2gp_orca_control.authenticated_github_login", lambda: login)
    monkeypatch.setattr("scripts.score2gp_orca_control.git_head", lambda root: SHA)
    monkeypatch.setattr(sys, "argv", dispatched[1:])
    main()


def test_go_delivers_an_architect_task_assigned_to_codex_end_to_end(tmp_path, monkeypatch, capsys) -> None:
    agentops = orca_checkout(tmp_path, "codex", authority(CODEX, owner_role="architect"))

    # 1. The legacy router selects the author bootstrap for the assigned author.
    command = run_legacy_router(monkeypatch, agentops, CODEX)
    assert Path(command[1]).name == GO

    # 2. The go bootstrap hands the resolved architect role to the Orca path.
    code, runner = run_go_bootstrap(monkeypatch, agentops, CODEX)
    assert code == 0, capsys.readouterr().out
    [(dispatched, live)] = runner.dispatched
    assert dispatched[dispatched.index("--orca-role") + 1] == "architect"
    assert dispatched[dispatched.index("--github-login") + 1] == CODEX

    # 3. The Orca path assigns the architect role to the assigned author.
    capsys.readouterr()
    run_dispatched_orca_path(monkeypatch, tmp_path, dispatched, live, CODEX)
    assignment = json.loads(capsys.readouterr().out)
    assert assignment["worker"]["role"] == "architect"
    assert assignment["worker"]["github_login"] == CODEX
    assert assignment["work"]["author_login"] == CODEX


def test_go_still_refuses_an_unassigned_architect_task(tmp_path, monkeypatch, capsys) -> None:
    agentops = orca_checkout(tmp_path, "auto", authority(owner_role="architect"))
    code, runner = run_go_bootstrap(monkeypatch, agentops, AUTO)
    assert code == 1
    out = json.loads(capsys.readouterr().out)
    assert (out["ok"], out["dispatch_role"]) == (False, "architect")
    assert runner.dispatched == []


def test_go_stops_another_login_at_an_architect_task_assigned_to_codex(tmp_path, monkeypatch, capsys) -> None:
    agentops = orca_checkout(tmp_path, "auto", authority(CODEX, owner_role="architect"))
    code, runner = run_go_bootstrap(monkeypatch, agentops, AUTO)
    assert code == 0
    [(dispatched, live)] = runner.dispatched
    capsys.readouterr()
    with pytest.raises(SystemExit) as stopped:
        run_dispatched_orca_path(monkeypatch, tmp_path, dispatched, live, AUTO)
    assert stopped.value.code == 1
    out = json.loads(capsys.readouterr().out)
    assert (out["state"], out["dispatch_role"], out["assigned_author"]) == (
        "ASSIGNED_TO_ANOTHER_AUTHOR", "architect", CODEX)
    assert "assignment_type" not in out


def test_legacy_router_requires_the_assigned_author_to_hold_the_owner_role(tmp_path) -> None:
    roles = deepcopy(ROLES)
    roles["architect"]["github_logins"] = [AUTO]
    with pytest.raises(DispatchError, match="lacks the architect role"):
        select_bootstrap(CODEX, checkout(tmp_path, "codex"), roles, author_login=CODEX, owner_role="architect")
    assert select_bootstrap(CODEX, checkout(tmp_path / "x", "codex"), ROLES,
                            author_login=CODEX, owner_role="architect") == GO
