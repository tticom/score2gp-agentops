# ORC-03 — Automated Post-Merge State Reconciliation

Status: PROMOTED — governance task
Role: Governance worker
Repository: `score2gp-agentops`

## Objective

Automate verified gate-completion transitions so a merged task cannot remain
active indefinitely and the next task cannot become executable implicitly.

## Required work

1. Add a deterministic reconciliation operation to the control-plane flow.
2. Require live PR state `MERGED`, exact authorised task/PR/branch identity,
   product head SHA, and merge commit before changing authority.
3. Move the active task to `completed_tasks` exactly once, retaining its full
   task contract plus `head_sha` and `merge_commit`.
4. Generate `ACTIVE_TASK.md` from the updated JSON authority and validate the
   generated view in the same operation.
5. Keep `next_task_proposal` in `PROPOSED` status; reconciliation must never
   promote or dispatch successor work.
6. Make repeated reconciliation with the same merge idempotent and refuse
   stale, mismatched, incomplete, or already-reconciled inputs without writes.

## Acceptance and falsification

- A verified merged PR produces one completed-task record and a clean audit.
- A wrong PR, branch, head SHA, merge SHA, open PR, or missing merge metadata
  fails closed and leaves authority byte-for-byte unchanged.
- Replaying the same verified merge does not duplicate the completed task.
- The successor remains `PROPOSED` and `advance` cannot return an execution
  assignment for it as a side effect of reconciliation.
- A generated `ACTIVE_TASK.md` never reports the merged task as active.

## Scope

Only the deterministic control-plane scripts and their tests may change. Do not
modify product code, GitHub merge permissions, or unrelated task proposals.

## Validation

```bash
python3 -m pytest tests/test_score2gp_orca_control.py tests/test_score2gp_orchestrator.py tests/test_governance_audit.py
python3 scripts/score2gp_governance_audit.py
python3 -m compileall -q scripts
```

The implementation must use a dry-run or explicit staged write boundary so
live GitHub facts are verified before authority mutation.
