# Task branches and remote checkpoints

Maintainer directive, 2026-09-05: all authored work is performed on a task
branch and pushed to GitHub. Ephemeral containers must not be the only place
where work survives. This supersedes local-only handoff and PR-before-push
requirements elsewhere in the workflow.

## Required lifecycle

1. Select the authorized repository and explicit task branch. Never author on
   main/master or detached HEAD. Publish the task branch before starting.
2. Resume from the GitHub branch in an isolated task clone; a source/main clone
   is only a launcher input. Do not mount its shared Git administrative directory.
3. After each meaningful bounded change, and before any pause, handoff or
   session exit, inspect the diff, commit explicit safe task paths, push the
   checkpoint, and verify the full remote branch SHA equals local HEAD.
4. Incomplete code and failing tests may be checkpointed. Identify it clearly
   in the commit and keep sanitized remaining work/validation instructions in
   the task's existing repository-owned handoff or requirement document. A
   checkpoint is neither a successful validation nor approval to merge.
5. Open a PR when the developed change is ready for independent review. Do not
   require a PR merely to preserve work. If one already exists, later pushes
   update it; approvals remain bound to the exact reviewed head.
6. Before disposal, require no uncommitted/untracked task work and an exact
   GitHub receipt. Refused pushes, outages, dirty files, branch mismatch and
   divergence mean `RECOVERY_REQUIRED`; preserve the clone/container and do
   not claim the work is safely handed off. Never reset or force-push to resolve
   this state. Resume publication as soon as the external blocker is removed.

Inside the network-enabled worker, run `task-checkpoint` after committing.
It never stages or commits files; it verifies the assigned branch/origin, pushes
that branch explicitly and reads back GitHub's head. During review it verifies
only, and never pushes the reviewed branch. Reviewer findings remain GitHub
review metadata; this policy does not authorize reviewer source edits.

## Privacy and limits

Push source, tests, plans, task instructions and sanitized handoff information.
Never add secrets, credentials, private source PDFs/GPs, generated private
artifacts or raw private logs to a public task branch. Ignored ephemeral outputs
must be reproducible from the pushed code plus approved durable fixture inputs.
If an irreplaceable private artifact must survive, retain it in the approved
private evidence store before disposal; publishing it to a source branch is
not an acceptable substitute. Do not use blanket staging to satisfy this rule.

An abrupt process/host loss can destroy work since the last checkpoint; no Git
push policy can protect edits that were never committed and transmitted.
Frequent explicit checkpoints bound that exposure. A failed upload is a
recovery incident, not permission to finish with local-only work. Auth/config
volumes are caches, not the source of task recovery truth.

## Scope and rollout

This applies to product, governance, planning and runtime authors, including
host sessions that prepare container work. Existing active-task approval,
identity, private-data, independent-review and human-merge controls remain.
Remote checkpointing is a persistence step, not permission to broaden task scope.

The runtime implementation lives in `agent-runtime/task_branch.py` and the
shared live-worker launcher. Rebuild images after merging runtime changes.
Offline Compose runs are validation-only: the host verifies a previously
pushed task clone before and after execution. They cannot be used to author
work without a network-enabled checkpoint step.
