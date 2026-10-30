# CP-16: Governance audit binds an open task PR against the task record on main, not the copy on the PR's own branch

- **Repository:** `tticom/score2gp-agentops`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Branch:** `feat/cp-16-audit-binds-task-record-on-main`
- **Depends on:** none

## Goal

This task is gate-adjacent. It may only make the gate read the evidence it already reads more correctly; no review, merge or audit check may be removed, loosened or reordered, and anything that was denied for a real reason stays denied. Seen 2026-09-27 on #713 (CP-13): governance recorded pull_request 713 on main (#714), but the audit reads the authority in the checkout, so at the PR head it still saw TBD and failed until the author merged origin/main into the branch. Every AgentOps task PR hits this, because the PR number exists only after the branch is cut.

## Acceptance

1. Measure first: reproduce on the base an open AgentOps task PR whose number is recorded on main but still TBD on its branch, and show the audit failing; quote the lookup.
2. The audit takes the task record for an open task PR from origin main, not from the PR's own checkout. A record that is missing or inconsistent on main still fails; a branch that edits its own task record to pass is not trusted.
3. Tests cover: number recorded on main and TBD on the branch (passes), number missing on main (fails), branch rewrites its own record to match (fails); the named mutants (read the branch copy, skip the comparison) are rejected.
4. No audit check is removed or weakened; the audit passes on current main. No gate, role or stop-condition changes.
5. Validation commands pass; handback complete.

## Rules

- Do not weaken, skip or reorder any merge, review or audit gate. The only permitted behaviour change is the one in the acceptance: the audit reads an open task PR's task record from origin main, not from the PR's branch. Every other audit check is unchanged.
- Tests must be able to fail: for each new test, name the wrong implementation it rejects and show that mutant failing.
- Never edit CI, private fixtures, agent instruction files or `ORCHESTRATION_STATE.json`.
- Stop and say so if the task needs any gate change beyond the one the acceptance names.
