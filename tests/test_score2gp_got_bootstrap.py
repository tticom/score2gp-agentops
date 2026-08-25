import json
import subprocess
from pathlib import Path

import pytest

from scripts.score2gp_got_bootstrap import (
    GotError,
    find_current_head_handback,
    find_latest_marked_author_handback,
    find_current_head_review_summary,
    gate_review_on_handback,
    gate_review_on_publication,
    query_pr_number,
    resolve_got_state,
    select_review_skills_pin,
    required_skills_for_review,
    select_review_level,
    review_tool_paths,
    validate_governance_identity,
)


def test_merged_pr_overrides_historical_review_state() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 393},
        [{"state": "CHANGES_REQUESTED", "commit_id": "c" * 40}],
    )
    assert result["state"] == "PROMOTE_MERGED_TASK"
    assert result["current_review"] is None


def test_promoted_merged_task_is_terminal_for_got() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 398},
        [{"state": "CHANGES_REQUESTED", "commit_id": "c" * 40}],
        active_task_status="MERGED",
    )
    assert result == {"state": "NO_ACTIVE_TASK", "current_review": None}


def test_merged_pr_emits_promote_resolved_task_when_status_resolved() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 421},
        [],
        active_task_status="RESOLVED",
    )
    assert result["state"] == "PROMOTE_RESOLVED_TASK"
    assert result["current_review"] is None


def test_merged_pr_emits_promote_merged_task_when_status_not_resolved() -> None:
    result = resolve_got_state(
        {"state": "MERGED", "headRefOid": "e" * 40, "number": 396},
        [],
        active_task_status="APPROVED",
    )
    assert result["state"] == "PROMOTE_MERGED_TASK"
    assert result["current_review"] is None


def test_no_pr_waits_for_author_publication() -> None:
    result = resolve_got_state(None, [])
    assert result == {
        "state": "AWAITING_AGY_PUBLICATION",
        "current_review": None,
    }


def test_resolved_task_with_no_pr_emits_promote_resolved_task() -> None:
    result = resolve_got_state(None, [], active_task_status="RESOLVED")
    assert result == {
        "state": "PROMOTE_RESOLVED_TASK",
        "current_review": None,
    }


def test_open_pr_uses_latest_exact_head_review() -> None:
    head = "a" * 40
    reviews = [
        {"id": 1, "state": "APPROVED", "commit_id": head,
         "submitted_at": "2026-07-28T18:00:00Z", "user": {"login": "tticomgov-code"}},
        {"id": 2, "state": "CHANGES_REQUESTED", "commit_id": head,
         "submitted_at": "2026-07-28T19:00:00Z", "user": {"login": "tticomgov-code"}},
    ]
    result = resolve_got_state(
        {"state": "OPEN", "headRefOid": head, "number": 393}, reviews
    )
    assert result["state"] == "AWAITING_AGY_FIXES"
    assert result["current_review"]["id"] == 2


def test_open_pr_accepts_newer_codex_change_request() -> None:
    head = "a" * 40
    result = resolve_got_state(
        {"state": "OPEN", "headRefOid": head, "number": 396},
        [
            {"id": 1, "state": "APPROVED", "commit_id": head,
             "submitted_at": "2026-07-30T15:59:00Z", "user": {"login": "tticomgov-code"}},
            {"id": 2, "state": "CHANGES_REQUESTED", "commit_id": head,
             "submitted_at": "2026-07-30T16:48:00Z", "user": {"login": "tticom-codex"}},
        ],
    )
    assert result["state"] == "AWAITING_AGY_FIXES"
    assert result["current_review"]["id"] == 2


def test_open_pr_accepts_owner_verdict() -> None:
    head = "b" * 40
    result = resolve_got_state(
        {"state": "OPEN", "headRefOid": head, "number": 396},
        [{"id": 3, "state": "APPROVED", "commit_id": head,
          "submitted_at": "2026-07-30T17:00:00Z", "user": {"login": "tticom"}}],
    )
    assert result["state"] == "READY_FOR_HUMAN_MERGE"


def test_governance_worker_uses_codex_publishing_identity() -> None:
    validate_governance_identity(
        linux_user="tticom-gov",
        home="/home/tticom-gov",
        gh_user="tticomgov-code",
        git_user="tticomgov-code",
        agentops=Path("/home/tticom-gov/work/score2gp-workspace/score2gp-agentops"),
        product=Path("/home/tticom-gov/work/score2gp-workspace/score2gp"),
    )


def test_codex_reviewer_uses_isolated_codex_identity() -> None:
    validate_governance_identity(
        linux_user="tticom-codex",
        home="/home/tticom-codex",
        gh_user="tticom-codex",
        git_user="tticom-codex",
        agentops=Path("/home/tticom-codex/work/score2gp-workspace/score2gp-agentops"),
        product=Path("/home/tticom-codex/work/score2gp-workspace/score2gp"),
    )


def test_codex_reviewer_rejects_cross_profile_identity() -> None:
    with pytest.raises(GotError):
        validate_governance_identity(
            linux_user="tticom-codex",
            home="/home/tticom-codex",
            gh_user="tticomgov-code",
            git_user="tticom-codex",
            agentops=Path("/home/tticom-codex/work/score2gp-workspace/score2gp-agentops"),
            product=Path("/home/tticom-codex/work/score2gp-workspace/score2gp"),
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("linux_user", "tticom"),
        ("gh_user", "tticom"),
        ("git_user", "tticom"),
    ],
)
def test_governance_identity_rejects_personal_account(field: str, value: str) -> None:
    values = {
        "linux_user": "tticom-gov",
        "home": "/home/tticom-gov",
        "gh_user": "tticomgov-code",
        "git_user": "tticomgov-code",
        "agentops": Path("/home/tticom-gov/work/score2gp-workspace/score2gp-agentops"),
        "product": Path("/home/tticom-gov/work/score2gp-workspace/score2gp"),
    }
    values[field] = value
    with pytest.raises(GotError):
        validate_governance_identity(**values)


def test_personal_reviewer_uses_personal_identity() -> None:
    # Test with unauthenticated/empty gh_user
    validate_governance_identity(
        linux_user="tticom",
        home="/home/tticom",
        gh_user="",
        git_user="tticom",
        agentops=Path("/home/tticom/work/score2gp-workspace/score2gp-agentops"),
        product=Path("/home/tticom/work/score2gp-workspace/score2gp"),
    )
    # Test with authenticated gh_user
    validate_governance_identity(
        linux_user="tticom",
        home="/home/tticom",
        gh_user="tticom",
        git_user="tticom",
        agentops=Path("/home/tticom/work/score2gp-workspace/score2gp-agentops"),
        product=Path("/home/tticom/work/score2gp-workspace/score2gp"),
    )


def test_low_risk_documentation_pr_selects_basic_review() -> None:
    selected = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["docs/user-guide.md"],
        task="Clarify CLI spelling",
        title="docs: clarify CLI spelling",
        live_head="a" * 40,
    )
    assert selected == {
        "level": "basic",
        "skill": "code-review",
        "reasons": ["low-risk documentation-only change"],
    }


def test_code_or_test_change_selects_hard_review() -> None:
    selected = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["src/score2gp/config.py", "tests/test_config.py"],
        task="Configuration cleanup",
        title="refactor: simplify configuration loading",
        live_head="b" * 40,
    )
    assert selected["level"] == "hard"
    assert selected["skill"] == "hard-review"
    assert "code, test, fixture, or executable-script change" in selected["reasons"]


def test_governance_state_promotion_selects_basic_review() -> None:
    selected = select_review_level(
        repository="tticom/score2gp-agentops",
        changed_paths=[
            "projects/score2gp/ACTIVE_TASK.md",
            "projects/score2gp/ORCHESTRATION_STATE.json",
            "projects/score2gp/prompts/next/orc-02-agent-isolation.md",
        ],
        task="Promote ORC-02",
        authorised_role="Governor",
        title="chore: promote ORC-02 to active task",
        live_head="b" * 40,
    )
    assert selected == {
        "level": "basic",
        "skill": "code-review",
        "reasons": ["governance state/prompt promotion"],
    }


def test_agentops_executable_change_remains_devils_advocate() -> None:
    selected = select_review_level(
        repository="tticom/score2gp-agentops",
        changed_paths=["scripts/score2gp_got_bootstrap.py"],
        task="Change review routing",
        authorised_role="Governance",
        title="fix: route reviews by change risk",
        live_head="b" * 40,
    )
    assert selected["level"] == "devils-advocate"
    assert "governance/control-plane repository change" in selected["reasons"]


@pytest.mark.parametrize(
    ("repository", "paths", "task", "role", "reason"),
    [
        (
            "tticom/score2gp",
            ["docs/design/conversion-architecture.md"],
            "Conversion architecture",
            "Architect / Researcher",
            "architecture, research, or authority translation",
        ),
        (
            "tticom/score2gp",
            ["src/score2gp/timing.py"],
            "Repair MusicXML timing",
            "Developer",
            "high-risk conversion or evidence claim",
        ),
    ],
)
def test_high_risk_context_selects_devils_advocate_review(
    repository: str,
    paths: list[str],
    task: str,
    role: str,
    reason: str,
) -> None:
    selected = select_review_level(
        repository=repository,
        changed_paths=paths,
        task=task,
        authorised_role=role,
        live_head="c" * 40,
    )
    assert selected["level"] == "devils-advocate"
    assert selected["skill"] == "devils-advocate-review"
    assert reason in selected["reasons"]


def test_prior_trusted_review_on_earlier_head_forces_devils_advocate_rereview() -> None:
    selected = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["docs/user-guide.md"],
        task="Clarify CLI spelling",
        live_head="d" * 40,
        reviews=[
            {
                "commit_id": "e" * 40,
                "state": "APPROVED",
                "user": {"login": "tticomgov-code"},
            }
        ],
    )
    assert selected["level"] == "devils-advocate"
    assert "re-review after a trusted review on an earlier head" in selected["reasons"]


def test_declared_review_level_can_escalate_but_not_weaken() -> None:
    escalated = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["docs/user-guide.md"],
        declared_level="real review",
        live_head="f" * 40,
    )
    assert escalated["level"] == "devils-advocate"

    not_weakened = select_review_level(
        repository="tticom/score2gp",
        changed_paths=["src/score2gp/config.py"],
        declared_level="basic",
        live_head="f" * 40,
    )
    assert not_weakened["level"] == "hard"


def test_invalid_declared_review_level_fails_closed() -> None:
    with pytest.raises(GotError, match="unsupported Review Level"):
        select_review_level(
            repository="tticom/score2gp",
            changed_paths=["docs/user-guide.md"],
            declared_level="friendly glance",
        )


def test_exact_head_author_handback_is_required_for_review_dispatch() -> None:
    head = "a" * 40
    handback = {
        "id": 12,
        "body": f"Head: {head}\nAWAITING_GOVERNANCE_REVIEW",
        "user": {"login": "tticom-automation"},
    }
    found = find_current_head_handback(
        [handback], head=head, author="tticom-automation"
    )
    assert found == handback
    assert gate_review_on_handback(
        {"state": "REVIEW_CURRENT_HEAD", "current_review": None}, found
    ) == {"state": "REVIEW_CURRENT_HEAD", "current_review": None}


@pytest.mark.parametrize(
    "comment",
    [
        {
            "id": 1,
            "body": f"Head: {'b' * 40}\nAWAITING_GOVERNANCE_REVIEW",
            "user": {"login": "tticom-automation"},
        },
        {
            "id": 2,
            "body": f"Head: {'a' * 40}\nAWAITING_GOVERNANCE_REVIEW",
            "user": {"login": "tticom-gov"},
        },
        {
            "id": 3,
            "body": f"Head: {'a' * 40}\nTests passed",
            "user": {"login": "tticom-automation"},
        },
    ],
)
def test_stale_wrong_author_or_unmarked_comment_is_not_a_handback(
    comment: dict,
) -> None:
    assert find_current_head_handback(
        [comment], head="a" * 40, author="tticom-automation"
    ) is None


def test_missing_handback_emits_terminal_wait_state() -> None:
    assert gate_review_on_handback(
        {"state": "REVIEW_CURRENT_HEAD", "current_review": None}, None
    ) == {"state": "AWAITING_AGY_HANDBACK", "current_review": None}


def test_stale_marked_handback_reports_expected_and_observed_heads() -> None:
    expected = "d510c68fa1b63192bca52384a718e884037960b5"
    observed = "d510c68c2d1b0922880c85c390bcab8a8e10dfca"
    stale = {
        "id": 5238382950,
        "html_url": "https://github.com/tticom/score2gp/pull/425#issuecomment-5238382950",
        "body": f"Exact Head SHA: `{observed}`\nAWAITING_GOVERNANCE_REVIEW",
        "user": {"login": "tticom-automation"},
    }

    candidate = find_latest_marked_author_handback(
        [stale], author="tticom-automation"
    )

    assert candidate == stale
    assert gate_review_on_handback(
        {"state": "REVIEW_CURRENT_HEAD", "current_review": None},
        None,
        expected_head=expected,
        rejected_handback=candidate,
    ) == {
        "state": "INVALID_OR_STALE_AGY_HANDBACK",
        "current_review": None,
        "expected_head": expected,
        "observed_handback_heads": [observed],
        "rejected_handback_id": 5238382950,
        "rejected_handback_url": stale["html_url"],
        "next_action": "Author must publish a new handback pinned to expected_head.",
    }


def test_handback_gate_does_not_override_other_states() -> None:
    resolved = {
        "state": "AWAITING_AGY_FIXES",
        "current_review": {"id": 99},
    }
    assert gate_review_on_handback(resolved, None) is resolved


def test_agent_review_without_mandatory_summary_is_not_terminal() -> None:
    head = "a" * 40
    review = {
        "id": 42,
        "state": "CHANGES_REQUESTED",
        "commit_id": head,
        "user": {"login": "tticomgov-code"},
    }
    resolved = {"state": "AWAITING_AGY_FIXES", "current_review": review}

    gated, summary = gate_review_on_publication(
        resolved,
        comments=[],
        head=head,
        level="devils-advocate",
    )

    assert gated == {
        "state": "REVIEW_PUBLICATION_INCOMPLETE",
        "current_review": review,
    }
    assert summary is None


def test_weaker_or_wrong_identity_summary_does_not_complete_review() -> None:
    head = "b" * 40
    review = {
        "id": 43,
        "state": "APPROVED",
        "commit_id": head,
        "user": {"login": "tticomgov-code"},
    }
    comments = [
        {
            "id": 1,
            "user": {"login": "tticomgov-code"},
            "body": (
                f"<!-- reviewer-summary:hard:{head} -->\n"
                f"Reviewed head: {head}\nVerdict: APPROVE"
            ),
        },
        {
            "id": 2,
            "user": {"login": "tticom-automation"},
            "body": (
                f"<!-- reviewer-summary:devils-advocate:{head} -->\n"
                f"Reviewed head: {head}\nVerdict: APPROVE"
            ),
        },
    ]

    assert find_current_head_review_summary(
        comments,
        review=review,
        head=head,
        level="devils-advocate",
    ) is None


def test_exact_level_identity_head_and_verdict_complete_review_publication() -> None:
    head = "c" * 40
    review = {
        "id": 44,
        "state": "APPROVED",
        "commit_id": head,
        "user": {"login": "tticomgov-code"},
    }
    summary = {
        "id": 3,
        "user": {"login": "tticomgov-code"},
        "body": (
            f"<!-- reviewer-summary:devils-advocate:{head} -->\n"
            "Review level: DEVILS_ADVOCATE\n"
            f"Reviewed head: {head}\nVerdict: APPROVE"
        ),
    }
    resolved = {"state": "READY_FOR_HUMAN_MERGE", "current_review": review}

    gated, found = gate_review_on_publication(
        resolved,
        comments=[summary],
        head=head,
        level="devils-advocate",
    )

    assert gated is resolved
    assert found == summary


def test_human_maintainer_review_does_not_require_agent_summary() -> None:
    head = "d" * 40
    review = {
        "id": 45,
        "state": "APPROVED",
        "commit_id": head,
        "user": {"login": "tticom"},
    }
    resolved = {"state": "READY_FOR_HUMAN_MERGE", "current_review": review}

    gated, summary = gate_review_on_publication(
        resolved,
        comments=[],
        head=head,
        level="devils-advocate",
    )

    assert gated is resolved
    assert summary is None


def test_agentops_lock_upgrade_uses_proposed_pin_without_activating_it(
    tmp_path: Path,
) -> None:
    proposed = "e" * 40
    lock = tmp_path / "projects/score2gp"
    lock.mkdir(parents=True)
    (lock / "SKILLS_LOCK.md").write_text(
        f"Required source commit:\n  `{proposed}`\n", encoding="utf-8"
    )

    selected = select_review_skills_pin(
        active_pin="f" * 40,
        actual_repository="tticom/score2gp-agentops",
        changed_paths=["projects/score2gp/SKILLS_LOCK.md"],
        review_worktree=tmp_path,
    )

    assert selected == {
        "pin": proposed,
        "mode": "proposed-pin-isolated",
    }


def test_non_lock_review_uses_active_skills_pin(tmp_path: Path) -> None:
    active = "f" * 40
    selected = select_review_skills_pin(
        active_pin=active,
        actual_repository="tticom/score2gp-agentops",
        changed_paths=["projects/score2gp/ACTIVE_TASK.md"],
        review_worktree=tmp_path,
    )
    assert selected == {"pin": active, "mode": "active-pin"}


def test_product_review_uses_active_lock_without_reading_product_as_agentops(
    tmp_path: Path,
) -> None:
    required = {"code-review": "skills/engineering/code-review"}
    assert required_skills_for_review(
        mode="active-pin",
        active_required_skills=required,
        review_worktree=tmp_path,
    ) is required


def test_review_skill_and_publisher_use_same_immutable_checkout(
    tmp_path: Path,
) -> None:
    required = {
        "code-review": "skills/engineering/code-review",
        "devils-advocate-review": "skills/engineering/devils-advocate-review",
    }
    publisher = (
        tmp_path
        / required["code-review"]
        / "scripts"
        / "publish_review.py"
    )
    publisher.parent.mkdir(parents=True)
    publisher.write_text("# publisher\n", encoding="utf-8")

    skill_path, publisher_path = review_tool_paths(
        checkout=tmp_path,
        required_skills=required,
        review_skill_name="devils-advocate-review",
    )

    assert skill_path == str(tmp_path / required["devils-advocate-review"])
    assert publisher_path == str(publisher)
    assert Path(skill_path).is_relative_to(tmp_path)
    assert Path(publisher_path).is_relative_to(tmp_path)


def test_explicit_pr_query_is_bound_to_repository_and_number(monkeypatch) -> None:
    head = "a" * 40

    def runner(command, **kwargs):
        assert command[:5] == [
            "gh", "pr", "view", "515", "--repo",
        ]
        assert command[5] == "tticom/score2gp-agentops"
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=json.dumps({
                "number": 515,
                "state": "OPEN",
                "headRefOid": head,
                "headRefName": "codex/pin-tiered-review-skills",
                "mergedAt": None,
            }),
            stderr="",
        )

    monkeypatch.setattr("scripts.score2gp_got_bootstrap.subprocess.run", runner)
    pr = query_pr_number("tticom/score2gp-agentops", 515)
    assert pr["number"] == 515
    assert pr["headRefOid"] == head


def test_explicit_pr_query_rejects_invalid_head(monkeypatch) -> None:
    def runner(command, **kwargs):
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=json.dumps({
                "number": 515,
                "state": "OPEN",
                "headRefOid": "deadbee",
            }),
            stderr="",
        )

    monkeypatch.setattr("scripts.score2gp_got_bootstrap.subprocess.run", runner)
    with pytest.raises(GotError, match="invalid head SHA"):
        query_pr_number("tticom/score2gp-agentops", 515)


def test_explicit_pr_query_rejects_non_hex_full_length_head(monkeypatch) -> None:
    def runner(command, **kwargs):
        return subprocess.CompletedProcess(
            command,
            0,
            stdout=json.dumps({
                "number": 515,
                "state": "OPEN",
                "headRefOid": "z" * 40,
            }),
            stderr="",
        )

    monkeypatch.setattr("scripts.score2gp_got_bootstrap.subprocess.run", runner)
    with pytest.raises(GotError, match="invalid head SHA"):
        query_pr_number("tticom/score2gp-agentops", 515)
