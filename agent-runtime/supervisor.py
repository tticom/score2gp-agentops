"""Small, capability-based developer/reviewer loop.

The supervisor owns sequencing and status; role adapters only provide the
developer, reviewer, and validation operations.
"""
from __future__ import annotations

from typing import Callable, Literal

Verdict = Literal["APPROVED", "CHANGES_REQUESTED", "BLOCKED"]


class SupervisorBlocked(RuntimeError):
    """A participant could not continue without an external decision."""


class Outcome:
    __slots__ = ("status", "attempts", "reason")

    def __init__(self, status: Literal["APPROVED", "BLOCKED"], attempts: int, reason: str = ""):
        self.status = status
        self.attempts = attempts
        self.reason = reason

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Outcome) and (
            self.status, self.attempts, self.reason
        ) == (other.status, other.attempts, other.reason)


def run_loop(
    developer: Callable[[int], None],
    reviewer: Callable[[int], Verdict],
    validate: Callable[[], None],
    emit: Callable[[str], None] = print,
    max_attempts: int = 5,
) -> Outcome:
    """Run developer -> devil's-advocate review until terminal state."""
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")
    for attempt in range(1, max_attempts + 1):
        emit(f"STATUS DEVELOPING attempt={attempt}")
        try:
            developer(attempt)
            emit("STATUS VALIDATING")
            validate()
            emit("HANDOFF developer -> devils-advocate-reviewer")
            verdict = reviewer(attempt)
        except SupervisorBlocked as error:
            reason = str(error) or "participant blocked"
            emit(f"STATUS BLOCKED reason={reason}")
            emit("NEXT provide the missing decision or evidence, then rerun")
            return Outcome("BLOCKED", attempt, reason)
        if verdict == "APPROVED":
            emit("STATUS APPROVED")
            emit("NEXT human merge or stop")
            return Outcome("APPROVED", attempt)
        if verdict == "BLOCKED":
            emit("STATUS BLOCKED reason=reviewer")
            emit("NEXT resolve the reviewer blocker, then rerun")
            return Outcome("BLOCKED", attempt, "reviewer")
        if verdict != "CHANGES_REQUESTED":
            raise ValueError(f"unsupported reviewer verdict: {verdict}")
        emit("STATUS CHANGES_REQUESTED")
        emit("NEXT handoff reviewer -> developer")
    emit(f"STATUS BLOCKED reason=max_attempts={max_attempts}")
    emit("NEXT inspect the latest review and choose whether to continue")
    return Outcome("BLOCKED", max_attempts, "max attempts")
