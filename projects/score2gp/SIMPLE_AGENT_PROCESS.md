# Simple Agent Process

The supervisor is the single human interface. It owns task selection, role
assignment, handoffs, validation, review retries, and console status.

1. A developer works on the assigned task.
2. Passing work is handed immediately to an independent devil's-advocate reviewer.
3. `CHANGES_REQUESTED` returns automatically to the developer.
4. The loop continues until review is `APPROVED` or `BLOCKED`.
5. Only those terminal states are shown to the human.

Roles grant capabilities per assignment. A Gov worker may implement governance
code or review product code; a developer may not review its own change; no
agent merges. These are capability checks, not permanent role restrictions.

Every step emits `STATUS`, `HANDOFF`, or `NEXT` lines. A run that is alive emits
a progress line at least every 60 seconds. A run never ends with only a cycle
identifier or a recovery path.

Terminal output is one of:

```text
STATUS APPROVED
NEXT human merge or stop
```

```text
STATUS BLOCKED reason=<plain explanation>
NEXT <one concrete action>
```
