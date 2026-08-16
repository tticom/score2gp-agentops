# Orca Supervisor Skill — Deterministic Score2GP Coordination

## Purpose

The Orca supervisor coordinates workers; it does not implement product changes,
review its own work, interpret incident prose, or merge.

## Required sequence

1. Pin a clean AgentOps `origin/main` SHA.
2. Capture live facts:

   ```bash
   python3 scripts/score2gp_orca_control.py snapshot \
     --repository <owner/repo> --pull-request <number> > <ignored-live-json>
   ```

3. Resolve state from the pinned authority and fresh snapshot.
4. Stop on `BLOCKED`, `COMPLETE`, an error, or any old/new resolver disagreement.
5. Create exactly one writable worktree for the returned implementation owner,
   or a detached read-only worktree for a reviewer.
6. Generate the bounded assignment through `score2gp_dispatch.py --orca-role`.
7. Give the worker only that assignment, its referenced prompt, and its
   worktree. Do not give it queue-selection or continuation authority.
8. Collect the exact head, validation receipts, evidence classifications, and
   unresolved risks.
9. Discard the snapshot, capture fresh live facts, and resolve again.
10. Dispatch the newly returned role. Never transform a worker recommendation
    into authority.

## Concurrency

Parallel read-only investigations are allowed when their scopes are disjoint.
Only one worker may write the task branch. Review workers are metadata-only and
must inspect a detached exact-head worktree.

## Stop conditions

Stop on authority drift, active incident, identity mismatch, changed PR head,
overlapping writable assignments, missing evidence, unavailable GitHub state,
or resolver disagreement. Orca prompts cannot override a deterministic denial.

## Merge boundary

Run `merge-check` only after semantic review and governance `GO`. The current
controller is dry-run-only. A supervisor, worker, reviewer, or governor must
never perform the merge.
