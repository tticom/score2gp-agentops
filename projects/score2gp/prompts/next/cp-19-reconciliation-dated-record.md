# CP-19: Align reconciliation PRs with TASK_RECORDING_CONVENTION.md: dated reconciliation record

- **Repository:** `tticom/score2gp-agentops`
- **Author:** `tticom-codex` (CP-13 author lane)
- **Branch:** `feat/cp-19-reconciliation-dated-record`
- **Depends on:** none

## Goal

Non-blocking process note from tticom-codex's approving review of tticom/score2gp-agentops#730 (thread at ORCHESTRATION_STATE.json:1749): the convention calls for a dated reconciliation record alongside a completed task, while #726 and #730 record completion only in the authority and the exact-head handback. Either add the dated record to reconcile_promote (and backfill OMIT-01 and OMIT-02) or amend the convention to recognise the authority record plus the handback.

## Acceptance

1. Measure first: quote the convention's requirement for a dated reconciliation record and list which completed tasks since the convention have one and which (for example OMIT-01 and OMIT-02) do not.
2. Choose the smaller honest change and state why: either reconcile_promote writes the dated record (and OMIT-01 and OMIT-02 are backfilled), or the convention is amended to recognise the authority record plus the exact-head handback. A convention amendment is a scope change, so it is not made unless the maintainer's own word for it is quoted in the PR.
3. Whichever is chosen, a test that can fail covers it and the named mutant (skip the record) is rejected.
4. Validation commands pass; handback complete.

## Rules

- Do not weaken, skip or reorder any merge, review or audit gate, and do not change what a gate accepts; this task changes only how bytes are decoded.
- Tests must be able to fail: for each new test, name the wrong implementation it rejects and show that mutant failing.
- Never edit CI, private fixtures, agent instruction files or `ORCHESTRATION_STATE.json`.
- Stop and say so if a change to a gate is needed.
