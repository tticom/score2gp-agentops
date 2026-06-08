# Score2GP Agent Control

This file is the governance control policy for agentic work on `score2gp`.

Agents must not treat task lists, backlog files, research notes, handoffs, or unchecked checklist items as permission to execute.

The only executable task source is:

`projects/score2gp/ACTIVE_TASK.md`

If `ACTIVE_TASK.md` says `NO_ACTIVE_TASK_APPROVED`, the agent must stop after preflight and report.

## Mandatory Startup Protocol

Agents must start from the governance repository:

`/home/tticom/work/score2gp-workspace/score2gp-agentops`

Before any work, run and report:

- `git status --short`
- `git branch --show-current`
- `git fetch --all --prune`
- `git log --oneline --decorate --max-count=5`

Agents must then read, in this order:

1. `projects/score2gp/AGENT_CONTROL.md`
2. `projects/score2gp/ACTIVE_TASK.md`
3. `projects/score2gp/TASKS.md`

If product work is involved, agents must also inspect the product repository:

`/home/tticom/work/score2gp-workspace/score2gp`

and read:

`AGENTS.md`

## Permission Tiers

### Tier 0: Inspect Only

Default tier.

Allowed:

- read files
- run safe inspection commands
- run non-mutating diagnostics
- report findings

Not allowed:

- modify files
- create branches
- commit
- push
- open PRs
- merge PRs
- delete branches
- mark tasks complete

### Tier 1: Local Edits Only

Allowed only when explicitly approved in `ACTIVE_TASK.md` or the current user session.

Allowed:

- edit only approved files
- run validation commands
- report diffs and results

Not allowed:

- commit
- push
- open PRs
- merge PRs
- delete branches

### Tier 2: Local Commit

Disabled by default.

Allowed only when explicitly approved by the human maintainer.

### Tier 3: Push or Open PR

Disabled for agents.

Only the human maintainer may push or open PRs unless a future written policy explicitly changes this.

### Tier 4: Merge or Delete Branch

Prohibited for agents.

Only the human maintainer may merge PRs or delete branches.

## Absolute Prohibitions

Agents must not:

- push
- create PRs
- edit PRs
- close PRs
- merge PRs
- delete branches
- run `gh pr merge`
- run any command containing `--delete-branch`
- run `gh auth login`
- run `hgh`
- mark `TASKS.md` items complete
- treat unchecked backlog items as approval
- modify files outside the active approved scope
- touch private PDFs, private GP/MusicXML files, generated diagnostic dumps, benchmark artifacts, local work outputs, credentials, tokens, SSH keys, or GitHub CLI authentication state

## Human-Only Commands

The following are human-only:

- `git push`
- `hgh pr create`
- `hgh pr merge`
- `gh auth login`
- branch deletion
- changing GitHub credentials
- changing SSH keys
- changing read-only/write remote configuration

Agents must never use `hgh`.

## Deferred Product Boundaries

Unless explicitly approved by the human maintainer, agents must not implement or integrate:

- pitch inference
- clef handling
- notehead scanning or classification
- rhythm or duration extraction
- voice assignment
- bar-local timing grids
- ScoreIR event creation from geometry diagnostics
- scanned or OCR PDF support
- direct integration of geometry clusters into playback mapping

Geometry diagnostics remain diagnostic-only until separately approved.

## Stop Conditions

Agents must stop and report if:

- `ACTIVE_TASK.md` says `NO_ACTIVE_TASK_APPROVED`
- required preflight checks fail
- the current branch is unexpected
- the working tree contains unrelated changes
- a requested action would push, open a PR, merge, or delete a branch
- a requested action would touch private or generated artifacts
- requirements conflict with repository evidence
- tests fail and the failure is not clearly in scope
- the task would require implementing a deferred capability
- the next step requires human approval
