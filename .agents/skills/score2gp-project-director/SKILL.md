---
name: score2gp-project-director
description: Apply Score2GP-specific authority, evidence, privacy, review, and continuation policy while running the pinned reusable governed-development-loop skills. Use for Score2GP task promotion, implementation/review handoffs, post-merge continuation, and unattended governed cycles.
---

# Score2GP project profile

This skill is a thin Score2GP adapter. Generic branch, implementation,
publication, handoff, and stop mechanics live in the pinned `agy-skills`
revision; do not restate or fork them here.

## Executable dispatch gate

For any continuation request, execute
`python3 scripts/score2gp_dispatch.py --product ../score2gp --agentops . --json`
as the first task action. The router selects author or governance behavior
from the isolated Linux worker identity, never from ambiguous command prose.
Do not manually query GitHub or reconstruct status from comments. The returned
state and formal `current_review` are authoritative.

On `ADDRESS_CURRENT_PR_REVIEW`, execute
`projects/score2gp/prompts/next/address-current-pr-review.md` immediately with
the returned review ID, commit ID, and body. A status-only response is a
dispatcher failure. Stop on helper failure or missing review data.

Only `EXECUTE_PROMPT` and `ADDRESS_CURRENT_PR_REVIEW` authorize work.
`MERGED_AWAITING_GOVERNANCE_PROMOTION` is a terminal automation state: report
it and stop without rerunning tests, re-verifying the merge, summarizing the
completed task, creating a promotion, or taking any product action. All other
non-action and unknown states are terminal and fail closed.

For a governance/reviewer worker, the router selects `got`; this state machine is distinct from `go`.
`REVIEW_CURRENT_HEAD` requires the returned exact-head
review worktree and the returned `review_skill`. Invoke that skill with the
Score2GP overlay and publish a formal verdict, useful inline comments, and the
mandatory marked PR summary. Reviewer mode is review-metadata-only: never edit
the reviewed repository, branch, PR body, task state, prompt, report, or
evidence artifact. A status-only response is a dispatcher failure.

`READY_FOR_HUMAN_MERGE` and `AWAITING_AGY_FIXES` are report-and-stop states.
`PROMOTE_MERGED_TASK` and `PROMOTE_RESOLVED_TASK` authorize and require the
post-merge continuation described below; a status-only response is a dispatcher
failure.

## Load in order

1. `projects/score2gp/SKILLS_LOCK.md`
2. `projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`
3. `projects/score2gp/AGENT_CONTROL.md`
4. `projects/score2gp/ACTIVE_TASK.md`
5. the exact prompt selected by `projects/score2gp/prompts/NEXT.md`, when the
   active task uses the fast lane
6. project evidence/review contracts referenced by the profile
7. pinned `identity-safe-git`, `governed-development-loop`, `durable-handoff`,
   `code-review`, `hard-review`, and `devils-advocate-review`

For reviews, invoke exactly the dispatcher's selected review skill and overlay
Score2GP's
`REVIEW_RULES.md`, `PR_REVIEW_TEMPLATE.md`, and active prompt.

If the required skills commit is unavailable, not checked out in the assigned
identity's skills clone, or the installed links resolve elsewhere, stop before
writes.

The reusable identity gate must verify the effective global commit identity,
not a repository-local override. Its evidence must include the equivalents of:

```bash
git config --global --get user.name
git config --global --get user.email
```

A local `user.name` or `user.email` override is a no-write stop.

## Score2GP decisions retained here

Apply the project-specific rules in AgentOps:

- only `ACTIVE_TASK.md` or its explicitly selected versioned prompt grants
  execution authority;
- PDF/MusicXML/ScoreIR/GP claims require the evidence channels and hierarchy
  in `REVIEW_RULES.md`;
- private inputs remain local and ignored;
- runtime provenance is required for conversion claims;
- Agy may publish its authorised branch/PR but may not self-approve or merge;
- `tticom-automation` and `tticom-gov` may never merge;
- `tticom-codex` may merge only in a separate operation after a current explicit
  instruction from `tticom` naming the exact repository, PR number, and
  reviewed full head SHA;
- once you have raised a PR, you must expect a review;
- review runs may change review metadata only and must leave the reviewed
  worktree clean;
- you must write an accurate comment to any PR you review, including any you raised;
- Codex independently reviews and may publish its review under the current maintainer policy;
- candidate follow-ups are not active tasks.

## Continuation

After a verified merge, synchronize the product and governance mains and
reread `ACTIVE_TASK.md`.

If a separately authorised task exists, run it through
`governed-development-loop`. If none exists, inspect Score2GP evidence and
prepare one bounded governance proposal. Do not begin product implementation
until that proposal is merged and active.

Rank Score2GP proposals by:

1. the active real-world conversion blocker;
2. observability or reproducibility of existing diagnostics;
3. already-approved schema/design implementation;
4. deterministic public fixtures or approved corpus evidence;
5. no-leakage, compatibility, schema, or CLI hardening;
6. bounded research with a decision gate.

Playable output integration and recognition-policy changes require explicit
architecture authority.

## Durable close-out

Use `durable-handoff` to write AgentOps run records. Record exact product,
governance, and skills revisions, verified evidence, unresolved risks, next
authority, and stop condition. Never put durable agent state in the product
repository.
