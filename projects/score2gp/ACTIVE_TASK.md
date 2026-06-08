# Execute Approved Standard-Staff Feature Queue

Status:
APPROVED

Execution source:
`projects/score2gp/APPROVED_TASK_QUEUE.md`

Agents may execute the next eligible APPROVED queue item in order without a new human prompt or governance PR, provided:
- the previous task PR has been human-merged or explicitly human-closed
- main has been verified after merge
- prerequisites are satisfied
- repos are clean
- the next task remains inside its written scope

Agents must stop at READY_FOR_HUMAN_MERGE for each product PR. Human merge is still required for every PR.

Agents must not skip, reorder, invent, or materially edit queue items.

## Current Active Task

Task 5 — Correct standard-staff fixture coverage review from product main
