# ORC-04 — Integrated PR Lifecycle and Concurrent Review Routing

Status: PROPOSED — one bounded control-plane implementation task
Role: Implementation worker (`tticom-automation`)
Repository: `score2gp-agentops`

## Objective

Make the end of every agent cycle prepare the next governed handoff: verify
the published head, create or update the task PR, dispatch the assigned
reviewer against that exact PR head, and support more than one independent
task in flight without sharing writable source or authority state.

This task must also make the currently open product PR 460 reviewable by Gov
and allow Automation to review a Gov-authored governance PR in read-only
reviewer mode. Codex remains an eligible author and reviewer, but no worker
identity gains merge authority.

## Required state model

Preserve compatibility with the existing `task` view while adding a stable
task registry or equivalent keyed by task ID. Each task record must retain:

- repository, base branch, task branch, owner role, reviewer role;
- PR number and exact live head SHA once published;
- lifecycle state and current cycle/lease identifier;
- validation contract, allowed paths, and recovery receipt location.

The state machine must distinguish authoring, PR-open, review-required,
changes-requested, approved, human-merge, merged, reconciled, and successor
prepared states. A successor may be prepared automatically but never executed
without its own promoted authority.

## Required lifecycle behavior

1. After an author validates and publishes a branch, the host controller must
   create or find exactly one PR for that branch and verify the full remote
   head SHA before reporting cycle completion.
2. The generated handoff must contain the PR URL/number, exact head SHA,
   validation receipt, assigned reviewer, and next state.
3. Reviewer dispatch must accept an explicit repository, PR number, and exact
   head, and must reject a changed head, closed PR, missing PR, or self-review.
4. Reviewers must receive read-only source/context mounts and may publish only
   formal review metadata and the required review summary.
5. Distinct tasks may run concurrently when their task IDs, branches, PRs,
   leases, clones, and recovery directories are distinct. A controller clone
   must not be shared for writable task state.
6. Post-merge reconciliation must be per-task, idempotent, and must preserve
   the next task as proposed/prepared rather than dispatching it implicitly.

## Routing requirements

- Automation author → Gov reviewer for product PRs, including PR 460.
- Gov author → Automation reviewer for governance PRs.
- Codex author → an independent Gov or Automation reviewer.
- No identity may review its own PR, and no Automation, Gov, or Codex worker
  may merge.

## Non-goals

- Do not alter product recognition behavior.
- Do not weaken protected-branch or merge-controller rules.
- Do not use comments as a substitute for formal review state.
- Do not copy credentials, source clones, or shared Git administrative state
  between roles.

## Falsification checks

- Force PR creation to fail and prove the author cycle is not reported
  complete.
- Move the remote branch after assignment creation and prove the cycle is
  retained rather than pushed or reviewed.
- Attempt self-review and cross-task branch reuse and prove both fail closed.
- Run two distinct task assignments concurrently and prove their source,
  Git metadata, receipts, and validation results remain isolated.
- Replay post-merge reconciliation and prove no duplicate completion record or
  implicit successor execution occurs.

## Validation

```bash
python3 -m pytest tests/test_assignment_adapter.py tests/test_disposable_cycle.py tests/test_score2gp_orca_control.py tests/test_score2gp_orchestrator.py
python3 -m compileall -q agent-runtime scripts
python3 scripts/score2gp_governance_audit.py
```

The worker must publish a handback with the exact remote branch head and stop
for independent review. It must not merge this PR.
