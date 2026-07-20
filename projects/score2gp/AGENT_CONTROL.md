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

## WSL Execution Environment Gate

All Score2GP product and governance work must execute in the Ubuntu WSL
workspace, not in a Windows checkout, PowerShell, Command Prompt, or a
`/mnt/c` mirror. A Windows-host `wsl.exe` wrapper is allowed only to enter
the Linux environment; the command it runs must then execute in WSL.

Before reading, writing, testing, or running GitHub CLI commands, Agy must
prove and report:

```bash
test "$(uname -s)" = "Linux"
test "$(pwd -P)" = "/home/tticom/work/score2gp-workspace/score2gp-agentops"
test "$(git rev-parse --show-toplevel)" = "/home/tticom/work/score2gp-workspace/score2gp-agentops"
test -x /home/tticom/work/score2gp-workspace/score2gp/.venv/bin/python
```

When product work begins, it must similarly prove:

```bash
test "$(pwd -P)" = "/home/tticom/work/score2gp-workspace/score2gp"
test "$(git rev-parse --show-toplevel)" = "/home/tticom/work/score2gp-workspace/score2gp"
```

Bare Windows-host `git`, `python`, `gh`, PowerShell, Command Prompt,
`explorer.exe`, `start`, Windows paths such as `C:\\...`, and
`/mnt/c` project worktrees are prohibited for Agy. An "Open using..." chooser
or any attempt to open a project artefact through a Windows application is an
environment-boundary failure: do not select an app, do not continue the task,
and report the command and intended file/URI.

If the WSL proof cannot be established, Agy must make no filesystem, Git, or
GitHub write and stop. It must not compensate by resetting, cleaning, copying,
or recreating a checkout.

## Antigravity Automation Identity Gate

This gate applies to Antigravity/Agy runs. It does not apply to a human
maintainer or a separately authenticated Codex review session.

Before an Agy run creates a branch, commits, pushes, creates a PR, comments on
a PR, or performs any merge operation, it must prove that its active GitHub CLI
identity is the machine user `tticom-automation`:

```bash
test "$(gh api user --jq .login)" = "tticom-automation"
```

It must also verify the local Git author identity in every repository it will
write:

```bash
test "$(git config --local --get user.name)" = "tticom-automation"
test "$(git config --local --get user.email)" = "tticomautomation@gmail.com"
```

If any check fails, Agy may inspect repositories but must make no remote or
local write. It must report the failed identity check and stop. It must not
switch to, use, or borrow the maintainer's `tticom` credentials.

The automation machine user must never use `--admin`, a bypass flag, direct
pushes to `main`, force pushes, `git reset --hard`, `git clean` with deletion
flags, branch deletion for an open PR, or **any PR
merge command or API**. In particular, Agy must never run `gh pr merge`, merge
through the GitHub web UI, invoke a merge API, or treat a PR as merged because
its own checks pass. It opens and revises PRs, then leaves them for an
independently authenticated human maintainer or external release integrator.
No programme, task, prompt, or role transition may create an exception to this
rule. This rule also never permits an amended published commit.

## Runtime Provenance Gate

Before an agent diagnoses or changes `score2gp convert` behaviour, it must
prove the runtime being discussed. Record, in an ignored work directory and in
the PR evidence summary:

```bash
git rev-parse HEAD
git status --short
command -v score2gp
python -c 'import score2gp, pathlib; print(pathlib.Path(score2gp.__file__).resolve())'
```

The record must also include the exact conversion command, PDF path class,
MusicXML sidecar path and SHA-256 when one is used, generated report path, and
the conversion exit status. A claim applies only to that recorded runtime. If
the executable, import path, or uncommitted source differs from the approved
branch, classify it as `uncontrolled_runtime`; do not invent a code path or
implement a repair until the divergence is committed, reviewed, or discarded.

Private inputs and generated diagnostics may be read and written locally, but
they must remain in ignored directories and must not be committed. Sanitized
facts such as counts, status codes, hashes, and source revisions are allowed in
PR evidence.

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
* Agents must stop at PR creation (or `READY_FOR_EXTERNAL_MERGE`) for each product PR. Agy must never push directly to `main` or merge a PR.
* Agents must not skip, reorder, invent, or materially edit queue items unless a task is unblocked by another task.
* Agents must stop if a queued task is ambiguous, stale, blocked, conflicts with current repo state, or would require expanding allowed files/repositories.
* Human approval remains required to add, remove, reorder, or materially change queued tasks.

### Teamwork Programme Exception

A human may explicitly authorise a bounded multi-milestone programme in
`ACTIVE_TASK.md`. This is for a connected product outcome that cannot honestly
be delivered as a single microscopic task, such as correcting PDF-to-GP output
across a defined corpus.

For an active Teamwork programme:

- the programme document is the executable task boundary and may authorise
  coordinated Architect, Researcher, Developer, Reviewer, and Director work;
- because product `AGENTS.md` declares this repository the governance truth,
  the programme may coordinate the named roles but does not override this
  document's no-merge rule for Agy;
- agents may create a sequence of small, independently reviewable product PRs
  without a new human prompt between milestones;
- agents must keep a durable milestone ledger, rerun the programme's output
  evidence after every functional change, and stop only at a documented
  decision gate or a real stop condition;
- after an accepted PR, Agy must mark it `READY_FOR_EXTERNAL_MERGE`, record the
  exact head SHA and validation evidence, and await an external merge; it must
  not advance a dependent task as though the PR had landed;
- programme authority never permits private artifacts in Git, force-pushes,
  branch deletion, scope expansion beyond the named corpus/capabilities, or
  treating a shallow metric as proof of output correctness.

External merge handoff requirements:

1. the PR has a concrete, passed product-output acceptance test;
2. CI and required local verification are green;
3. all review/Codex threads are explicitly dispositioned;
4. the Reviewer has assessed the exact PR head against the programme evidence;
5. the handoff records the exact head SHA, intended merge method, validation,
   unresolved risks, and the dependent task that remains blocked on merge.
6. the merge operation is a normal merge or squash merge, never a bypass.

If any condition is absent, the agent may continue with independent or
stacked work, but must leave that PR open rather than declaring it complete.

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
2. Identify the next eligible `APPROVED` queue item if its prerequisites are satisfied. Do not promote a dependent task until the required product and governance PRs have been externally merged.
3. If no approved queue item exists, identify the smallest credible continuation that stays inside the current product direction and does not require a new human product choice.
4. Prefer product-functional diagnostic, fixture, schema, smoke-test, or fail-closed implementation work over administrative stopping when the next step is already supported by merged backlog or review evidence.
5. Create a governance PR that records the proposed continuation. Leave it `READY_FOR_EXTERNAL_MERGE`; do not treat its task state as active until the governance PR is externally merged.
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
- Do not amend a published commit or force-push. Only the human maintainer may
  intentionally rewrite history, outside an unattended task run.
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

Agents must not push directly to `main`, force-push, run `git reset --hard`, run `git clean` with deletion flags, delete branches, run commands containing `--delete-branch`, use the `hgh` CLI alias, approve their own PR, bypass failing checks, start unrelated backlog work, expand scope without human approval, or mark unmerged work as merged/done. Agy must never run `gh pr merge`, use `--admin`, use a merge API, or merge through a web UI.

### Human-Only Operations

Only the human maintainer or a separately operated external release integrator may merge a PR, approve scope expansion, accept a known failing-check risk, or explicitly close/abandon a task without merge. Agy has no merge exception, including for a Teamwork programme.

## Product Boundaries

The project is authorised to pursue deterministic PDF-to-Guitar-Pro conversion
for the named approved corpus when an active task or Teamwork programme provides
measurable product-output acceptance criteria. This may include clefs,
noteheads, rests, dots, duration/timing, barlines, key/time signatures, ties,
layout breaks, basic guitar position inference, and explicitly scoped
embellishment detection.

The following remain prohibited unless a later task explicitly changes the
boundary:

- opaque ML/model training or unmeasured OCR substitution;
- reference-GP leakage: `--ref-gp` is validation only and must never alter
  generated output, thresholds, tempo, structure, or inferred notes;
- fixture-specific indexes, filenames, literal measure lists, or special cases
  that make one private score pass;
- suppressing warnings, adding rests, changing time signatures, or dropping
  measures merely to make a coarse comparison pass;
- committing private inputs, generated private GP/MusicXML, screenshots,
  overlays, or reports containing extractable private content.

Every functional change must be generic, traceable to PDF/MusicXML/GPIF
evidence, covered by a public synthetic regression where feasible, and checked
against more than one approved corpus input before it is claimed as a fix.

## Product-Output Evidence Standard

For recognition, conversion, MusicXML, ScoreIR, or GPIF work, passing unit
tests and aggregate counts are necessary but not sufficient.

Before an agent claims an output issue is fixed, it must inspect a fresh,
no-reference conversion and produce durable structured evidence at the
smallest relevant scope (usually a bar). The evidence must include, where
applicable:

- bar number and source PDF system/page location;
- ordered event sequence including note versus rest;
- onset, duration, dot state, tie state, chord membership, and pitches;
- fret/string when tablature is emitted;
- time/key/tempo changes;
- barline style and requested system-break/layout marker;
- expected/reference comparison when a reference exists; and
- the first remaining mismatch, rather than a claim of general success.

`compare_gp` aggregate fields are a smoke signal only. They must never be used
as sole acceptance evidence for visual or musical correctness. A bar-level
comparator and/or explicit generated-artifact inspection is required.

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
