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
2. `projects/score2gp/AGENT_PR_READINESS.md`
3. `projects/score2gp/ACTIVE_TASK.md`
4. `projects/score2gp/APPROVED_TASK_QUEUE.md`
5. `projects/score2gp/TASKS.md`
6. Relevant task template(s) under `projects/score2gp/templates/`

### Role skill loading

Every agent run for the Score2GP project must load and obey:

1. `projects/score2gp/AGENT_CONTROL.md`
2. `projects/score2gp/ACTIVE_TASK.md`
3. the relevant role skill file under `projects/score2gp/skills/<role>/SKILL.md`, if the role has a skill file
4. any task-specific prompt from the Orchestrator

For Architect work, the Architect must read:
`projects/score2gp/skills/architect/SKILL.md`

For Reviewer work, the Reviewer must read:
`projects/score2gp/skills/reviewer/SKILL.md`

For Developer work, the Developer must read:
`projects/score2gp/skills/developer/SKILL.md`

If a role skill file exists and cannot be read, the agent must stop and report rather than continue from memory or guesswork.

If task instructions conflict with the role skill file, the stricter safety/research/review rule wins unless the user explicitly overrides it.

If a task asks for uncertain, experimental, or architectural work but does not include measurable stop/continue/pivot criteria, the Architect must create those criteria or stop and return to governance.

### Workflow loop tiers

To balance safety and speed, Score2GP utilizes two workflow tiers, with Tier B as the standard default:

#### Tier B: Compressed Loop (Default Low-Risk Work)
This is the default loop for low-risk tasks, including:
- Markdown-only governance recording or minor process improvements.
- Narrow bug fixes with pre-approved architecture.
- Fixture/test-only changes where expected behaviour is already authorised.
- PRs with no product behaviour broadening.
- Clean public test suites, no private benchmark claims, and no unresolved Codex threads.
- **Compression Rules**:
  - The requirement packet includes acceptance and readiness criteria up front.
  - One combined Reviewer performs implementation conformance review and PR readiness review in a single pass.
  - One approved task normally produces exactly one product PR.
  - Governance completion records should be bundled with the next Orchestrator decision in `ACTIVE_TASK.md` or updated as direct run records, rather than requiring standalone governance PRs for routine completion bookkeeping.
  - Merge operators still perform the final guarded merge check.

#### Tier A: Full Loop (High-Risk Work)
Required only when a task involves:
- Uncertain architecture or new recognition strategies.
- Product behaviour changes or database schema modifications.
- Policy exceptions, failed reviews, or unapproved external-corpus/sensitive benchmark data claims.
- **Process**: Must follow separate sequential stages: Requirement -> Architect Research -> Reviewer Architecture Verification -> Developer Implementation -> Reviewer Conformance Review -> PR Readiness Review -> Merge.

### Verification and Report Automation
Agents must execute and rely on product-level automation tools instead of copying raw logs:
- Run `python scripts/agent_verify.py` to validate codebase correctness.
- Run `python scripts/pr_body.py` to generate PR descriptions automatically.
- Run `python scripts/artifact_audit.py` (which is run inside `agent_verify.py`) to verify repository hygiene.

### Approved Fixture Access Policy

Approved fixture inputs include:

- tracked public fixtures in `score2gp`;
- the sibling private fixture repository `score2gp-private-fixtures`;
- local fixture paths explicitly named by the human maintainer or the active task.

Agents may inspect, interrogate, and run diagnostics against approved fixture inputs when the active task allows fixture or corpus work. Fixture approval is a project/test-data boundary, not a publication claim.

Agents must not copy raw private fixture files, generated conversion artifacts, screenshots, overlays, or logs into unrelated Git commits. Reports should prefer sanitized evidence such as counts, statuses, warning categories, command names, and artifact paths unless the active task explicitly authorizes a different artifact.

Developer implementation work must not begin unless it is explicitly authorised in `projects/score2gp/ACTIVE_TASK.md`.

For Tier B tasks, `ACTIVE_TASK.md` may reference a requirement packet that contains acceptance criteria, readiness criteria, validation commands, artifact constraints, and reporting requirements. The requirement packet alone is not executable authorisation.

Tier B compression shortens review sequencing; it does not weaken task authorisation, artifact controls, Codex/review-thread handling, or guarded merge requirements.

Developer implementation work must not begin unless one of these is true:
- the task is Tier B (compressed loop) and is explicitly authorised in `projects/score2gp/ACTIVE_TASK.md`; or
- Outcome A or Outcome B has been verified by Reviewer architecture/reference verification; and
- the task contains measurable acceptance criteria.

Developer implementation must not begin after Outcome C.

If the Developer cannot identify the requirement, approved approach, acceptance criteria, or validation evidence, the Developer must stop and report instead of guessing.

If product work is involved, agents must also inspect the product repository:

`/home/tticom/work/score2gp-workspace/score2gp`

and read:

`AGENTS.md`

## Approved Task Queue

* `ACTIVE_TASK.md` remains the immediate execution contract.
* `APPROVED_TASK_QUEUE.md` is an ordered list of pre-approved bounded tasks.
* The human approves the queue by merging the governance PR that adds or changes it.
* Agents may execute the next eligible APPROVED queue item in order without a new human prompt or governance PR, provided:
  * the current task has been completed and a PR has been opened (or the task is explicitly marked as skipped/abandoned)
  * prerequisites for the next task are satisfied
  * repos are clean
  * the next task remains inside its written scope
  * the dependency relationship is clear (branching from current `main` for independent tasks, or stacking onto a dependent branch if the prior PR is unmerged)
* Agents must stop at PR creation (or READY_FOR_HUMAN_MERGE) for each product PR. Human merge is still required for every PR. Agents must never merge to main.
* Agents must not skip, reorder, invent, or materially edit queue items unless a task is unblocked by another task.
* Agents must stop if a queued task is ambiguous, stale, blocked, conflicts with current repo state, or would require expanding allowed files/repositories.
* Human approval remains required to add, remove, reorder, or materially change queued tasks.

Continuous Execution Rule:
After finishing a task, the agent should:
- run required validation
- commit
- push the branch
- open a PR
- report the PR link and evidence
- inspect the next queue item
- continue to the next eligible approved task if it is not blocked
- stop only if a stop condition is met

Queue status updates are operational bookkeeping only. Agents may report local task completion and next-task selection in their run report. Material queue edits, new tasks, reordering, scope changes, or removing tasks still require a governance PR and human merge.

### Post-Completion Continuation Protocol

When a task and its required review/promotion work are complete, agents must not default to `NO_ACTIVE_TASK_APPROVED`.

Before stopping after successful completion, the agent must perform a continuation audit:

1. Inspect `APPROVED_TASK_QUEUE.md`, current backlog reports, recent review reports, and active blockers.
2. Promote the next eligible `APPROVED` queue item if its prerequisites are satisfied.
3. If no approved queue item exists, identify the smallest credible continuation that stays inside the current product direction and does not require a new human product choice.
4. Prefer product-functional diagnostic, fixture, schema, smoke-test, or fail-closed implementation work over administrative stopping when the next step is already supported by merged backlog or review evidence.
5. Create a governance PR that records the completed work, adds the continuation task, and makes it active.
6. Set `ACTIVE_TASK.md` to `NO_ACTIVE_TASK_APPROVED` only when the continuation audit finds no credible safe continuation, or when every candidate continuation would require a new product direction, destructive action, unapproved data source, or speculative musical inference.

Examples of credible post-completion continuations:

- clef classifier complete -> expand diagnostic-only rest candidate coverage before pitch mapping;
- fixture gap closed -> resume the previously blocked feature task;
- schema hardening complete -> add snapshot, CLI, or leakage gates that make the schema observable;
- corpus audit complete -> implement the smallest model/schema correction backed by that audit.

Successful completion is not a stop condition while an evidence-backed continuation exists.

Review tasks must include an explicit continuation audit in the review report or governance PR body. The audit must name either:

- the next active task being promoted; or
- the concrete reason no safe continuation exists.

Marking a review task `DONE` and setting `ACTIVE_TASK.md` to `NO_ACTIVE_TASK_APPROVED` without this audit is non-compliant unless the active task already documented an unavoidable terminal boundary.

### Handoffless Role Transition Protocol

Promoting a next task is not a completion point.

After a governance PR merges and `ACTIVE_TASK.md` names a new approved task, the same autonomous run must immediately continue into that task when the work can be performed from the available repositories and tools.

This applies even when the next task changes:

- role, for example Reviewer -> Architect or Architect -> Developer;
- repository, for example `score2gp-agentops` -> `score2gp`;
- task type, for example review -> research -> implementation.

The agent may pause only for the same stop conditions that would apply at the start of any active task. A role transition, repository switch, successful PR merge, or walkthrough/report update is not by itself a stop condition.

When continuing across roles, the agent must:

1. pull the relevant repository main branch after the merge;
2. reread `ACTIVE_TASK.md`;
3. create the suggested branch if the task permits branch work;
4. execute the task's required role and validation;
5. continue through review/promotion according to the normal queue rules.

If the next active task is research-only or architecture-only, perform that task rather than stopping for human permission.

### Blocker Pivot Protocol

When an active task encounters a blocker, agents must not default to `NO_ACTIVE_TASK_APPROVED`.

Before stopping, the agent must perform a bounded pivot audit:

1. Identify whether the blocker has a credible unblocker within the project direction.
2. Check whether the unblocker can be expressed as a smaller research, fixture, test, reporting, or feature task.
3. Prefer an evidence-building pivot over waiting for the human when the pivot stays inside approved repositories, approved fixture locations, and existing product goals.
4. If a credible pivot exists, create a governance update that records the blocker, marks the blocked task accurately, and promotes the smallest safe pivot task into `ACTIVE_TASK.md`.
5. If no credible pivot exists, or every pivot would require a new product direction, destructive action, unapproved data source, or explicit human product choice, then set `ACTIVE_TASK.md` to `NO_ACTIVE_TASK_APPROVED` and explain why all credible alternatives were rejected.

Examples of credible pivots:

- missing fixtures -> generate or authorise the smallest fixture set;
- insufficient evidence -> run a bounded corpus audit or focused research task;
- unsafe classifier scope -> add fail-closed tests or schema/reporting guards;
- stale PR/branch state -> perform branch hygiene before product work.

Routine blockers are not stop conditions when a credible pivot task can unblock them.

## Permission Tiers

### Tier 0: Inspect Only

Agents may inspect repositories, read files, run safe status/log commands, and report.  
Agents must not modify files, create branches, commit, push, create PRs, merge PRs, or update task status.

### Tier 1: Local Research / Documentation Only

Agents may create local documentation or research notes within the files allowed by `ACTIVE_TASK.md`.  
Agents may commit locally only if explicitly allowed by `ACTIVE_TASK.md`.  
Agents must not push, create PRs, merge PRs, or modify product code.

### Tier 2: Branch and PR Work

Agents may create a task branch, modify files allowed by `ACTIVE_TASK.md`, run tests, commit, push the task branch to the human remote, and open a PR.

**Human approval is for the task boundary, not role transitions.**
An approved `ACTIVE_TASK.md` authorizes the full lifecycle of that task:
* research
* architecture
* development
* review
* reviewer-requested fixes
* testing
* re-review
* evidence recording
* pushing follow-up commits to the same branch
* updating the same PR

No extra human approval is needed to move from Architect to Developer to Reviewer as long as the work stays inside the approved task boundary.

**One task should normally produce one PR.**
The default model is:
* one approved task
* one task branch
* one PR in the repository that owns the durable output
* many review/fix/re-review cycles on that same branch and PR

Branching Rules:
- If the task is independent: branch from current `main`.
- If the task depends on an unmerged task PR: branch from the dependent task branch (creating a stacked/dependent branch).
- Require stacked PRs to clearly state their dependency in the PR body.
- Do not force-push unless explicitly instructed by a human.
- Do not merge main.
- Do not push to main.
- Do not combine unrelated tasks into one branch.
- Do not silently rewrite another agent’s branch.

Do not create separate PRs for Architect, Developer, and Reviewer phases.

**Governance PRs are only for governance.**
A governance PR is appropriate when changing:
* `ACTIVE_TASK.md`
* task templates
* control policy
* orchestration notes
* review records
* evidence/handoff records

A governance PR is not the right place for durable product design knowledge.
Durable product architecture, parser design, diagnostics design, fixture plans, test plans, implementation notes, scripts, generated public fixtures, and product documentation belong in `score2gp`.

Agents may update task-tracking files only for the approved task, and only to reflect accurate state.

A task must not be marked `DONE` until the human has actually merged the PR and it has been verified on main.

## Status Model

Statuses must strictly distinguish:

- `NO_ACTIVE_TASK_APPROVED`: Agents may inspect and report only.
- `APPROVED`: The task may start.
- `IN_PROGRESS`: Agents are working inside the approved task boundary.
- `PR_OPEN`: A task PR exists. Agents may continue review, fixes, tests, follow-up commits, and re-review on the same branch/PR.
- `CHANGES_REQUESTED`: Reviewer found issues. Developer may fix them on the same branch/PR without new human approval.
- `READY_FOR_HUMAN_MERGE`: Reviewer says acceptance criteria are met and all Codex comments on the PR are addressed. Agents must stop before merge.
- `BLOCKED`: Human decision is required.
- `DONE`: Only after human merge or explicit human closure.

## Task Scope and Exploration

**Tasks should be meaningful, not microscopic.**
Avoid process theatre. A task may include multiple cycles of research, development, and review if that is what is needed to reach a useful outcome.

A task is valid if either:
* the expected outcome is well-defined, with acceptance criteria, or
* it is explicitly a research task, where the output is evidence, constraints, options, risks, and a recommended next step

For research tasks, the result does not have to be predetermined. The point is to discover reality safely and report it clearly.

**Branches make exploration safe, but not uncontrolled.**
It is acceptable to explore, test, refine, or discard work on a task branch. However, the branch does not remove the task boundary. Agents must still stop if:
* the work exceeds approved scope
* sensitive material or unapproved fixture artifacts would be exposed
* allowed files or repositories need expansion
* destructive commands are required
* tests fail and the cause is unclear
* the task needs a human architectural/product decision
* merge is required
* force-push or branch deletion would be needed

## Role Boundaries

Agents operate under the following role boundaries during team operation:

- **Orchestrator**: identifies active blocker, sequences approved work, reports state.
- **Architect**: defines requirements, assumptions, acceptance criteria, risks.
- **Developer**: implements smallest useful approved change.
- **Reviewer**: reviews code/docs/process/evidence and comments, ensures all Codex comments on the PR are addressed before claiming that the PR is ready for review, but does not merge or self-approve.
- **Researcher**: investigates uncertainty and records evidence without changing product implementation unless approved.

### Forbidden Actions

Agents must not merge PRs, push directly to main, force-push, delete branches, run `gh pr merge`, run commands containing `--delete-branch`, use the `hgh` CLI alias, approve their own PR, bypass failing checks, start unrelated backlog work, expand scope without human approval, or mark unmerged work as merged/done.

### Human-Only Operations

Only the human maintainer may merge PRs, approve scope expansion, approve movement to a different task, close or abandon task PRs, accept a known failing-check risk, or explicitly close a task without merge.

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

## Validation Permission

Within an approved task, agents are authorized to run and re-run relevant non-destructive validation commands inside the task boundary without per-test human approval. This includes targeted pytest tests, the full pytest suite, diff checks, schema checks, and fixture-generation smoke checks when relevant to the task.

Human approval is only needed if validation would:
- exceed the approved task boundary
- require destructive commands
- use sensitive data or fixture sources outside the approved public/private fixture locations
- create large generated artifacts
- need unexpected network access
- alter dependencies/environment configuration
- modify files outside the allowed scope

## Stop Conditions

Agents must stop and report if:

- the next task has unmet prerequisites
- the next task depends on an unmerged branch and the dependency relationship is unclear
- product or governance main cannot be updated cleanly
- a branch conflict requires human decision
- PR creation or branch push is blocked
- `ACTIVE_TASK.md` says `NO_ACTIVE_TASK_APPROVED`
- the blocker pivot audit finds no credible safe pivot task
- the post-completion continuation audit finds no credible safe continuation task
- required preflight checks fail
- the current branch is unexpected
- the working tree contains unrelated changes
- a requested action would merge or delete a branch, or perform an unauthorized push/PR
- a requested action would touch private or generated artifacts
- requirements conflict with repository evidence
- tests fail and the failure is not clearly in scope or cannot be explained
- the task would require implementing a deferred capability
- the task requires modifying files outside its allowed scope
- destructive changes would be required
- the next step requires human approval
