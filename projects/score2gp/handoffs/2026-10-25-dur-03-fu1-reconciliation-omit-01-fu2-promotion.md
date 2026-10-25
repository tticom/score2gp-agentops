# DUR-03-FU1 Reconciliation and OMIT-01-FU2 Promotion Handoff

## Authority

- Reconciled task: `DUR-03-FU1` - guard the `old_line_rows >= 5` clause on approved real sources (`COMPLETED`)
  - PR tticom/score2gp#513, reviewed head `30115ee8669b77e9c072361713de73e90b914dd5`, approved by `tticomgov-code`
  - Merged through the executor at 2026-10-25T10:56:54Z: merge commit `0c2a704f85bb4e7fca9c4c0d16baeebabf12c7ae`.
- Promoted task: `OMIT-01-FU2` (`PROPOSED` to `PROMOTED`, contract unchanged)
- Authority source: `projects/score2gp/ORCHESTRATION_STATE.json` (authority revision 199 -> 200)
- Governance publisher: `tticomgov-code`, via `launchers/unattended_loop.sh` (mechanical reconciliation)

## Outcome and scope

- DUR-03-FU1 was moved to `completed_tasks` by the control plane's `reconcile_task` from live PR data.
- Only `status` changed on the promoted proposal; queue order and all other authority fields are unchanged.
- No backlog follow-ups, scope amendments or new proposals are recorded by this change.
- Product-level outcome (mutant results over the approved corpus) is in PR #513 and its review; it is not restated here.
