import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "supervisor", Path(__file__).parents[1] / "agent-runtime/supervisor.py"
)
supervisor = importlib.util.module_from_spec(spec)
spec.loader.exec_module(supervisor)


def test_retries_developer_until_review_approves():
    events = []
    attempts = []

    def developer(attempt):
        attempts.append(attempt)

    def reviewer(attempt):
        return "CHANGES_REQUESTED" if attempt == 1 else "APPROVED"

    outcome = supervisor.run_loop(developer, reviewer, lambda: None, events.append)

    assert outcome.status == "APPROVED"
    assert outcome.attempts == 2
    assert attempts == [1, 2]
    assert "HANDOFF developer -> devils-advocate-reviewer" in events
    assert "NEXT handoff reviewer -> developer" in events


def test_reviewer_blocker_is_terminal_with_next_option():
    events = []
    outcome = supervisor.run_loop(
        lambda attempt: None,
        lambda attempt: "BLOCKED",
        lambda: None,
        events.append,
    )

    assert outcome.status == "BLOCKED"
    assert outcome.reason == "reviewer"
    assert any(event.startswith("NEXT resolve") for event in events)


def test_developer_blocker_is_terminal():
    events = []

    def developer(attempt):
        raise supervisor.SupervisorBlocked("missing fixture")

    outcome = supervisor.run_loop(developer, lambda attempt: "APPROVED", lambda: None, events.append)

    assert outcome.status == "BLOCKED"
    assert outcome.reason == "missing fixture"
    assert events[-1].startswith("NEXT provide")


def test_max_attempts_is_blocked():
    outcome = supervisor.run_loop(
        lambda attempt: None,
        lambda attempt: "CHANGES_REQUESTED",
        lambda: None,
        lambda event: None,
        max_attempts=2,
    )

    assert outcome == supervisor.Outcome("BLOCKED", 2, "max attempts")
