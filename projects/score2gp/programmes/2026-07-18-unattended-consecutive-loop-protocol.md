# Unattended Consecutive Loop Protocol

## Authority

This protocol applies to the Visual Output Correctness Recovery Programme while
the active task explicitly opts in. The maintainer authorizes unattended
Architect, Developer, Reviewer, Project Director, and Release Integrator role
transitions, including guarded PR merges. It does not authorize pushing to
`main`, force-pushing, branch deletion, scope expansion, private artifacts in
Git, or acceptance of known failing validation.

## Consecutive Loop

1. The Developer implements only the current `ACTIVE_TASK.md` boundary on a
   branch based on the required approved parent.
2. The Developer validates, commits, pushes, and opens or updates one product
   PR. It records actual results and limitations; a green suite alone is not
   acceptance.
3. A distinct Reviewer context starts from fresh repository state, inspects the
   exact PR head, reruns focused validation, reads all review comments, and
   checks the stated output evidence.
4. If changes are required, the Developer fixes the same PR and the loop
   repeats from step 2 without maintainer interaction.
5. If the same root cause survives two review cycles, the Reviewer records an
   evidence-backed pivot in AgentOps. The Project Director promotes the
   smallest safe research, diagnostic, or implementation task and continues.
6. If the PR is accepted, the Release Integrator re-reads the exact head SHA
   and guarded-merge conditions, merges normally or by squash, pulls `main`,
   then begins the governance completion/promotion loop.
7. The Project Director updates the task state through a governance PR, merges
   it under the same guarded conditions, rereads `ACTIVE_TASK.md`, and begins
   the next eligible task immediately.

Role changes, PR creation, a successful merge, a failing first approach, and a
completed report are never stop conditions.

## Guarded Autonomous Merge

A Release Integrator may merge only when all of these are true:

1. The PR is within the active programme and exact task boundary.
2. The current head SHA has independent Reviewer approval.
3. Required local validation and CI are green.
4. Every Codex and reviewer comment is explicitly dispositioned.
5. The PR body and evidence distinguish demonstrated behavior from deferred
   work; it makes no visual-output claim that was not verified.
6. The merge is normal or squash, uses expected-head validation, and does not
   push directly to `main`.

If any condition is absent, keep the PR open and continue the review, rework,
or pivot loop. Do not call it done.

## End Of Run Report

At the end of an unattended run, or before a genuine stop, commit a concise
AgentOps report under `projects/score2gp/reports/` that lists completed tasks,
opened/merged/blocked PRs, validation and visible-output evidence, rework or
pivot decisions, current active task, and the exact reason for any stop.

## Genuine Stop Conditions

Stop only when there is no credible task or pivot inside the approved programme,
credentials or repositories remain unavailable after retry, validation failure
cannot be isolated, or proceeding would need a new product direction,
destructive operation, unapproved data source, or unsafe speculative inference.
