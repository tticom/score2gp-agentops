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

### Codex reviewer/governor

- OS user/home: `tticom-codex` / `/home/tticom-codex`
- GitHub and Git name: `tticom-codex`
- Git email: `tticom-codex@users.noreply.github.com`
- Workspace prefix: `/home/tticom-codex/work/score2gp-workspace`
- Uses separate clones and credential store
- May publish independent reviews and bounded governance PRs
- Merge remains a maintainer action unless the user explicitly authorises the
  exact merge

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
2. `code-review` for separate Standards and Spec axes
3. Score2GP hard-review overlay:
   - `projects/score2gp/REVIEW_RULES.md`
   - `projects/score2gp/PR_REVIEW_TEMPLATE.md`
   - `projects/score2gp/PR_EVIDENCE_CONTRACT.md`
   - the active task/prompt
4. unresolved comment/thread disposition
5. publish the review when reviewer authority permits
6. `durable-handoff` when a durable review record is required

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
