# Score2GP Workflow Skills Profile

This file supplies Score2GP-specific policy to the reusable skills pinned by
`SKILLS_LOCK.md`.

## Authority

- Canonical authority: `projects/score2gp/ACTIVE_TASK.md`
- Fast-lane prompt pointer: `projects/score2gp/prompts/NEXT.md`
- Informative only: queues, plans, reports, research, handoffs, task lists, and
  suggested next candidates
- Concurrency: one active task and one task PR
- Product work requires its predecessor governance promotion to be merged

## Identities and workspaces

### Agy author

- OS user/home: `tticom-automation` / `/home/tticom-automation`
- GitHub and Git name: `tticom-automation`
- Git email: `tticomautomation@gmail.com`
- Workspace prefix:
  `/home/tticom-automation/work/score2gp-workspace`
- Branches: only the pattern authorised by the active prompt
- May push the authorised branch and create/update its PR
- May not self-approve, merge, auto-merge, bypass protection, force-push, or
  delete branches

### Governance worker

- OS user/home: `tticom-gov` / `/home/tticom-gov`
- GitHub and Git name: `tticomgov-code`
- Git email: `tticomgov@gmail.com`
- Workspace prefix: `/home/tticom-gov/work/score2gp-workspace`
- Uses separate clones and credential store
- May publish independent review metadata or, in a separate authoring run,
  bounded governance PRs
- May never modify a reviewed PR branch or merge any PR

### Independent Codex reviewer

- OS user/home: `tticom-codex` / `/home/tticom-codex`
- GitHub and Git name: `tticom-codex`
- Git email: `tticom-codex@users.noreply.github.com`
- Workspace prefix: `/home/tticom-codex/work/score2gp-workspace`
- During review may publish only formal reviews, inline review comments, and
  the mandatory PR summary comment
- May not modify the reviewed repository or author fixes in the review run
- May merge only in a separate operation after a current explicit instruction
  from `tticom` naming the exact repository, PR number, and reviewed full head SHA

`tticom-automation` and `tticom-gov` never merge. Review and governance-authoring
roles must never be mixed in one run. An identity or role mismatch is a
no-write stop.

An identity mismatch is a no-write stop. Never switch accounts inside the
other identity's workspace.

## Skill composition

### Implementation

1. `identity-safe-git`
2. `governed-development-loop`
3. task-specific engineering skills such as `tdd`, `diagnosing-bugs`, or
   `codebase-design` only when their trigger fits
4. `durable-handoff`

### Review

1. `identity-safe-git`
2. the exact review skill returned by `score2gp_got_bootstrap.py`:
   - `code-review` for low-risk documentation-only PRs;
   - `hard-review` for code, tests, fixtures, executable scripts, domain data,
     or empirical claims;
   - `devils-advocate-review` for governance/control-plane changes,
     architecture/research, conversion correctness, or any re-review after a
     trusted review on an earlier head
3. Score2GP project overlay:
   - `projects/score2gp/REVIEW_RULES.md`
   - `projects/score2gp/PR_REVIEW_TEMPLATE.md`
   - `projects/score2gp/PR_EVIDENCE_CONTRACT.md`
   - the active task/prompt
4. unresolved comment/thread disposition
5. publish line-specific review comments where useful, one formal exact-head
   review, and one mandatory marked PR summary comment

For a live PR, Codex must review a detached or dedicated worktree whose local
`HEAD` exactly equals GitHub's full `headRefOid`. Initial live head, reviewed
local head, and final re-queried live head must all be identical before a
verdict is published.

The review worktree must remain byte-for-byte clean. Reviewer probes, bodies,
evidence packets, and notes live outside the reviewed repository. A reviewer
must never edit source, tests, prompts, reports, branches, commits, or PR
content; findings belong in review metadata. Process improvements are proposed
in the mandatory summary and implemented only in a separate authorised cycle.

A review-level declaration may escalate the dispatcher-selected minimum but
may never weaken it. The phrases `real review`, `devil's advocate`, and
`devils-advocate` explicitly select `devils-advocate-review`.

## Control-plane synchronization

Both `go` and `got` automatically fetch and fast-forward only clean canonical
`main` branches with `--ff-only`. They never pull or merge an arbitrary task
branch. Both verify the immutable `SKILLS_LOCK.md` commit from a pinned
checkout; neither silently adopts `agy-skills/main`. When a newly merged lock
names a new commit, the gate fetches that exact object, creates its immutable
pin worktree, and atomically repoints all six required skill symlinks.
It never changes the mutable `agy-skills` source branch.

Every dispatch reports the exact AgentOps main SHA, product main SHA, and
skills SHA. Reviewer dispatch additionally reports equal live and local PR
head SHAs.

All three identities use `scripts/score2gp_pr_review_state.py` as the sole formal
verdict resolver. It queries reviews separately from author handback comments,
filters to the exact live head and the trusted reviewer set (`tticomgov-code`,
`tticom-codex`, and repository owner `tticom`), and selects the latest across
that set by server timestamp then review ID. Reviews from other accounts never
govern dispatch.

Generic skill output never weakens the Score2GP overlay. When rules conflict,
use the stricter identity, privacy, evidence, disconfirmation, or stop rule.

## Product evidence

For conversion claims, retain:

- exact committed runtime, executable and import path;
- exact input class and approved sidecar provenance;
- strict-mode result;
- remediation/diagnostic result;
- semantic round-trip result;
- generated-file existence as a separate channel;
- visual/source inspection above summaries when evidence disagrees;
- coherent fresh artifacts from one run;
- full remote head SHA and changed paths.

Passing tests or file creation alone never proves conversion correctness.

## Repository ownership

### `agy-skills`

Owns reusable execution, identity, Git, review, and handoff mechanics.

### `score2gp-agentops`

Owns Score2GP authority, identities, branch permissions, evidence hierarchy,
privacy, musical acceptance, active prompts, decisions, and durable runs.

### `score2gp`

Owns product source, tests, fixtures, schemas, and product documentation. It
must not become the durable agent-control or skills-version store.

## Stop rules

Stop before writes on identity, workspace, skills-lock, authority, predecessor,
or clean-state failure. Stop before publication when scope or evidence is
incomplete. Stop after publishing one PR for independent review.

A recorded next candidate requires a separate governance promotion before
implementation.
