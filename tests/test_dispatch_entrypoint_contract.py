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


def test_agent_clients_load_executable_got_entrypoint() -> None:
    for name in ("CLAUDE.md", "AGENTS.md"):
        text = (ROOT / name).read_text(encoding="utf-8")
        assert GOT_COMMAND in text
        assert "never resume" in text.lower()


def test_agy_project_skill_forbids_manual_state_reconstruction() -> None:
    text = (
        ROOT / ".agents/skills/score2gp-project-director/SKILL.md"
    ).read_text(encoding="utf-8")
    assert COMMAND in text
    assert "Do not manually query GitHub" in text
    assert "A status-only response is a dispatcher failure" in " ".join(text.split())
