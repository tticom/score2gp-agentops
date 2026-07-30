from pathlib import Path


ROOT = Path(__file__).parents[1]
COMMAND = (
    "python3 scripts/score2gp_go_bootstrap.py "
    "--product ../score2gp --agentops . --json"
)
GOT_COMMAND = (
    "python3 scripts/score2gp_got_bootstrap.py "
    "--product ../score2gp --agentops ."
)


def test_agent_clients_load_executable_go_entrypoint() -> None:
    for name in ("CLAUDE.md", "AGENTS.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert COMMAND in text
        assert "ADDRESS_CURRENT_PR_REVIEW" in text
        assert "MERGED_AWAITING_GOVERNANCE_PROMOTION" in text
        assert "next_action" in text
        assert "rerun" in text.lower()


def test_agent_clients_load_executable_got_entrypoint() -> None:
    for name in ("CLAUDE.md", "AGENTS.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert GOT_COMMAND in text
        assert "never resume" in text.lower()
        assert "REVIEW_CURRENT_HEAD" in text
        assert "PROMOTE_MERGED_TASK" in text
        assert "status-only response is a dispatcher failure" in text.lower()


def test_agy_project_skill_forbids_manual_state_reconstruction() -> None:
    text = (
        ROOT / ".agents/skills/score2gp-project-director/SKILL.md"
    ).read_text(encoding="utf-8")
    assert COMMAND in text
    assert "Do not manually query GitHub" in text
    assert "A status-only response is a dispatcher failure" in " ".join(text.split())
    assert "MERGED_AWAITING_GOVERNANCE_PROMOTION" in text
    assert "Only `EXECUTE_PROMPT` and `ADDRESS_CURRENT_PR_REVIEW` authorize work" in text
    assert GOT_COMMAND in text
    assert "`REVIEW_CURRENT_HEAD`" in text
    assert "`PROMOTE_MERGED_TASK`" in text
    assert "state machine is distinct from `go`" in text
