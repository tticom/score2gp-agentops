"""Canonical ACTIVE_TASK status vocabulary shared by Score2GP control tools."""

from __future__ import annotations


EXECUTABLE_TASK_STATUSES = frozenset({"APPROVED", "IN_PROGRESS", "PROMOTED"})
PR_LIFECYCLE_TASK_STATUSES = frozenset({"PR_OPEN", "CHANGES_REQUESTED"})
TERMINAL_TASK_STATUSES = frozenset({"COMPLETED", "RESOLVED", "MERGED"})
KNOWN_TASK_STATUSES = (
    EXECUTABLE_TASK_STATUSES
    | PR_LIFECYCLE_TASK_STATUSES
    | TERMINAL_TASK_STATUSES
)


def normalize_task_status(status: str) -> str:
    return status.strip().upper()
