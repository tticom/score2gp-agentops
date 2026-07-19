# Unattended Consecutive Loop Protocol

## Authority

This protocol applies to the Visual Output Correctness Recovery Programme while
the active task explicitly opts in. The maintainer authorizes unattended
Architect, Developer, Reviewer, and Project Director role transitions. It does
not authorize Agy to merge PRs, push to `main`, force-push, delete branches,
expand scope, place private artifacts in Git, or accept known failing
validation.

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
6. If the PR is accepted, Agy records `READY_FOR_EXTERNAL_MERGE` with the exact
   head SHA, validation, risks, and blocked dependent task. It must not merge
   the PR, merge a governance PR, or advance a dependent task as though either
   PR had landed.
7. The human maintainer or separately operated external release integrator
   merges and promotes work. Agy may then reread the merged `ACTIVE_TASK.md`
   and resume the next eligible task.

Role changes, PR creation, a failing first approach, and a completed report
are never stop conditions. An accepted PR awaiting external merge blocks only
work that depends on that merge; Agy may continue an independent approved
research or diagnostic task.

## External Merge Handoff

Before an external release integrator merges, Agy must record all of these:

1. The PR is within the active programme and exact task boundary.
2. `git diff --name-only <approved-base>...<exact-head>` is recorded and every
   changed path is explicitly allowed by `ACTIVE_TASK.md`; any additional path
   is a required-changes finding, not incidental cleanup.
3. The current head SHA has independent Reviewer approval from a context that
   did not author, amend, or push the reviewed product changes.
4. Required local validation and CI are green.
5. Every Codex and reviewer comment is explicitly dispositioned.
6. The PR body and evidence distinguish demonstrated behavior from deferred
   work; it makes no visual-output claim that was not verified.
7. The external integrator must use a normal or squash merge with
   expected-head validation and must not use `--admin`, a bypass flag, or
   bypass repository review protections.

If any condition is absent, keep the PR open and continue the review, rework,
or pivot loop. Do not call it done. Agy never performs the merge.

## Scope-Breach Circuit Breaker

If a merged PR is later found to have violated its approved file or behavioural
boundary, immediately suspend automatic product merges for the programme. The
Project Director must create a governance remediation task that identifies the
exact merged revision, separates evidence from claims, and chooses a clean
revert, salvage, or replacement path. No downstream task may start until an
independent Reviewer accepts that remediation decision.

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
