from pathlib import Path


ROOT = Path(__file__).parents[1]
COMMAND = (
    "python3 scripts/score2gp_dispatch.py "
    "--product ../score2gp --agentops . --json"
)
GOT_COMMAND = COMMAND


def test_agent_clients_load_executable_go_entrypoint() -> None:
    for name in ("CLAUDE.md", "AGENTS.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert COMMAND in text
        assert "tticom-gov" in text
        assert "ADDRESS_CURRENT_PR_REVIEW" in text
        assert "MERGED_AWAITING_GOVERNANCE_PROMOTION" in text
        assert "next_action" in text
        assert "rerun" in text.lower()


def test_agent_clients_load_executable_got_entrypoint() -> None:
    for name in ("CLAUDE.md", "AGENTS.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert GOT_COMMAND in text
        assert "Linux worker identity" in text
        assert "never resume" in text.lower()
        assert "REVIEW_CURRENT_HEAD" in text
        assert "PROMOTE_MERGED_TASK" in text
        assert "PROMOTE_RESOLVED_TASK" in text
        assert "status-only response is a dispatcher failure" in text.lower()


def test_agy_project_skill_forbids_manual_state_reconstruction() -> None:
    text = (
        ROOT / ".agents/skills/score2gp-project-director/SKILL.md"
    ).read_text(encoding="utf-8")
    assert COMMAND in text
    assert "Do not manually query GitHub" in text
    assert "A status-only response is a dispatcher failure" in " ".join(text.split())
    assert "MERGED_AWAITING_GOVERNANCE_PROMOTION" in text
    assert "Only `EXECUTE_PROMPT`, `ADDRESS_CURRENT_PR_REVIEW`, and `PUBLISH_AGY_HANDBACK` authorize work" in text
    assert GOT_COMMAND in text
    assert "`REVIEW_CURRENT_HEAD`" in text
    assert "`PROMOTE_MERGED_TASK`" in text
    assert "`PROMOTE_RESOLVED_TASK`" in text
    assert "state machine is distinct from `go`" in text


def test_review_dispatch_is_tiered_exact_head_and_metadata_only() -> None:
    for name in ("CLAUDE.md", "AGENTS.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert "review_skill" in text
        assert "review_local_head == pr.headRefOid" in text
        assert "mandatory marked PR summary comment" in text
        assert "Reviewer mode" in text
        assert "must not modify repository" in text or "Do not edit any repository" in text


def test_got_dispatch_uses_pinned_tiered_skills_and_shared_publisher() -> None:
    text = (
        ROOT / "projects/score2gp/prompts/next/got-dispatch.md"
    ).read_text(encoding="utf-8")
    for skill in ("code-review", "hard-review", "devils-advocate-review"):
        assert skill in text
    assert "review_local_head == pr.headRefOid" in text
    assert "real review` means `devils-advocate-review" in text
    assert "synthetic/data-free evidence" in text
    assert "mandatory summary comment" in text
    assert 'python3 "<review_publisher_path>"' in text
    assert "$HOME/.agents/skills/code-review/scripts/publish_review.py" not in text
    assert "scripts/score2gp_publish_review.py" not in text


def test_reviewer_and_merge_role_firewalls_are_explicit() -> None:
    profile = (
        ROOT / "projects/score2gp/WORKFLOW_SKILLS_PROFILE.md"
    ).read_text(encoding="utf-8")
    control = (
        ROOT / "projects/score2gp/AGENT_CONTROL.md"
    ).read_text(encoding="utf-8")
    overlay = (ROOT / "skills/score2gp-pr-hard-review.md").read_text(
        encoding="utf-8"
    )
    for text in (profile, control, overlay):
        assert "`tticom-automation` and `tticom-gov`" in text
        assert "never merge" in text
        assert "`tticom-codex`" in text
        assert "explicit instruction" in text
        assert "PR number" in text
        assert "full head SHA" in text
    assert "review metadata only" in overlay
    assert "Never edit source, tests" in overlay


def test_skills_lock_pins_merged_tiered_review_revision() -> None:
    lock = (ROOT / "projects/score2gp/SKILLS_LOCK.md").read_text(encoding="utf-8")
    assert "439404f7342f4e324147efb6b0276f698fbf2bdb" in lock
    assert "https://github.com/tticom/agy-skills/pull/14" in lock
    assert "`hard-review`" in lock
    assert "`devils-advocate-review`" in lock
