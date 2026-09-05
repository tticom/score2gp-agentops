# Score2GP Agent Control

This file is the governance control policy for agentic work on `score2gp`.

## Mandatory remote checkpoints

The maintainer's task-branch/push requirement in
[TASK_CHECKPOINT_POLICY.md](TASK_CHECKPOINT_POLICY.md) applies to all authored
work, including planning and unfinished development. Publish and verify the
task branch before work and checkpoint after meaningful changes and before
pausing. PR readiness is a separate gate; incomplete checkpoints do not require
a PR. This supersedes local-only handoff wording without changing task scope,
private-data exclusions, reviewer authority or merge restrictions.

## Orca orchestration boundary

`ORCHESTRATION_STATE.json` is the sole machine-readable task and incident
authority. `ACTIVE_TASK.md` is a generated human view and must never be edited
as an independent authority. Governance audit rejects drift between them.

`scripts/score2gp_orchestrator.py` exposes the deep decision interface:

```python
decision = advance(authority, live_state)
```

The interface is side-effect-free and idempotent. It returns exactly one of:

- `EXECUTE_ASSIGNMENT`
- `REMEDIATE_CURRENT_PR`
- `AWAIT_REVIEW`
- `AWAIT_HUMAN_MERGE`
- `REQUEST_MUSICAL_ADJUDICATION`
- `PROPOSE_NEXT_TASK`
- `BLOCKED`

`scripts/score2gp_orca_control.py advance` is the command-line adapter. Other
Orca resolver commands and direct `go/got` routing are compatibility adapters
during migration; they must not introduce a second authority or contradict an
`advance` decision.

Orca owns sequencing, isolated worktrees, role dispatch, validation receipts,
and handoffs. A worker receives one bounded assignment and must not select a
next task, change scope, change role, approve its own work, or merge.

The legacy clauses remain applicable only to a direct compatibility `go/got`
run without an Orca assignment. They must not be combined with Orca mode.
Neither Orca prompts nor worker interpretation may override a deterministic
`BLOCKED` or merge `DENY` result.

Agents must not treat `ACTIVE_TASK.md`, `NEXT.md`, task lists, backlog files,
research notes, reports, handoffs, or unchecked checklist items as permission
to execute. They are views, inputs, or compatibility pointers only. An
executable assignment must resolve from `ORCHESTRATION_STATE.json` and current
live state.

Human authority is required only for material scope approval, genuinely
ambiguous musical/source adjudication, and merge. Task execution, validation,
review dispatch, remediation routing, and next-task proposal are autonomous
within the versioned authority contract. `PROPOSE_NEXT_TASK` never authorizes
execution of that proposal.

## Mandatory Startup Protocol

Agents must start from the governance repository owned by their assigned Linux
identity:

- Agy / `tticom-automation`:
  `/home/tticom-automation/work/score2gp-workspace/score2gp-agentops`
- Governance worker / `tticom-gov` using Git/GitHub identity `tticomgov-code`:
  `/home/tticom-gov/work/score2gp-workspace/score2gp-agentops`
- Independent reviewer / `tticom-codex`:
  `/home/tticom-codex/work/score2gp-workspace/score2gp-agentops`

## Identity-Isolated Workspace Gate

`tticom-automation`, `tticom-gov`, and `tticom-codex` must use separate Linux
users, homes, GitHub CLI credential stores, Git identities, and repository
clones. An agent must never operate from the other identity's home or workspace,
must never use another identity's clone, and must never copy GitHub credentials
between homes.

Before any Git, GitHub, filesystem, or task write, prove:

```bash
test "$(whoami)" = "<assigned-linux-user>"
test "$HOME" = "/home/<assigned-linux-user>"
test "$(gh api user --jq .login)" = "<assigned-github-user>"
test "$(git config --global --get user.name)" = "<assigned-git-user>"
test "$(pwd -P)" = "$(git rev-parse --show-toplevel)"
case "$(git rev-parse --show-toplevel)" in
  "$HOME"/work/score2gp-workspace/*) ;;
  *) exit 1 ;;
esac
```

A mismatch is a hard no-write stop. Do not switch accounts inside another
user's workspace, use another user's clone, or fall back to maintainer
credentials.

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

Before reading, writing, or testing, Agy must prove and report that it is in a
canonical repository or a task-specific WSL worktree below the canonical
workspace:

```bash
test "$(uname -s)" = "Linux"
test "$(pwd -P)" = "$(git rev-parse --show-toplevel)"
case "$(git rev-parse --show-toplevel)" in
  /home/tticom-automation/work/score2gp-workspace/score2gp-agentops|/home/tticom-automation/work/score2gp-workspace/score2gp-agentops-*) ;;
  *) exit 1 ;;
esac
test -x /home/tticom-automation/work/score2gp-workspace/score2gp/.venv/bin/python
```

When product work begins, it must similarly prove:

```bash
test "$(pwd -P)" = "$(git rev-parse --show-toplevel)"
case "$(git rev-parse --show-toplevel)" in
  /home/tticom-automation/work/score2gp-workspace/score2gp|/home/tticom-automation/work/score2gp-workspace/score2gp-*) ;;
  *) exit 1 ;;
esac
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

### Supported disposable-container identity

The Docker AGY runtime intentionally runs its unprivileged process as
`agent`/UID 10001 rather than as one of the host worker accounts. This is not a
host-workspace identity. The launcher must pass
`SCORE2GP_AGENT_ROLE=automation` or `SCORE2GP_AGENT_ROLE=gov`; the dispatcher
maps that role to the corresponding author or governance bootstrap and the
bootstrap still verifies the matching GitHub login. A container without that
role attestation fails closed.

The launcher also mounts the source repository's Git administrative directory
at the absolute path recorded by the disposable worktree's `.git` pointer.
Without that mount, Git sees a host-only `gitdir` path and the task worktree is
invalid inside the container.

## WSL Edit Coherency Gate

An IDE “Edited” event is not evidence that the canonical WSL worktree changed.
Before the first write in a task, Agy must prove that its edit mechanism and
its WSL Git commands address the same checkout.

For each file it intends to change, it must use the canonical WSL environment
to run:

```bash
pwd -P
git rev-parse --show-toplevel
git status --short
git diff -- <intended-path>
```

Immediately after an edit and before staging, it must run the same WSL
`git diff -- <intended-path>` command. It may stage only the exact intended
diff displayed from the canonical WSL worktree.

If the editor says a file changed but the WSL diff is empty, or if the path,
worktree root, or branch differs, the editor is attached to a different
checkout. Agy must stop without copying, recreating, resetting, cleaning, or
otherwise synchronizing files between environments. It must report the
mismatch for human workspace correction.

## Agy Fast Delivery Lane

This section supersedes every conflicting local-preparation or GitHub restriction below. It applies only to the authenticated GitHub account tticom-automation.

The installed Score2GP `go` skill is invoked as `/go`; its plain-text
compatibility aliases are `next` and `go`. It means: read
`projects/score2gp/prompts/NEXT.md`, then execute the permanent Agy dispatcher
it names. The dispatcher runs `python3 scripts/score2gp_go_bootstrap.py` to
fetch `origin/main`, synchronize canonical `main` branches, and select the authorised
task branch before checking GitHub PR state and selecting implementation, PR
monitoring, review fixes, a review wait, or a post-merge stop. It must never blindly
replay the original prompt or read task authority from a stale working-tree branch.

The user command `got` is used by the isolated `tticom-gov` and
`tticom-codex` governance/reviewer identities. It executes the permanent
dispatcher named by `NEXT.md`, verifies an exact Agy handback against live
GitHub state, and routes to first review, re-review, wait, readiness reporting,
or post-merge governance. A chat summary alone is never a handback.

Agy may:
- use authenticated WSL gh as tticom-automation after proving the account and local Git identity;
- fetch, create a branch beginning agy/, commit, push that branch, and create or update a pull request;
- run relevant tests and write task-scoped reports or product changes authorized by the current versioned prompt.

Agy must never:
- push directly to main, force-push, delete branches, reset or clean destructively, use admin or bypass flags, enable auto-merge, call a merge API, or merge any pull request;
- begin a second task while its current task PR is open;
- claim musical correctness, a fix, or completion without the prompt's required evidence.

The cadence is one governance step followed by one development step. Agy does
the implementation or evidence collection and publishes its PR. A reviewer
publishes review metadata only and never corrects the reviewed branch, PR body,
task state, report, prompt, or evidence artifact. `tticom-automation` and
`tticom-gov` never merge. `tticom-codex` may merge only in a separate operation
after a current explicit instruction from `tticom` naming the exact repository,
PR number, and reviewed full head SHA. Agy may independently review a
Codex-authored governance PR only when the active authority identifies it.

## Continuous Forward Motion and Real-World Validation

Completion of an architecture, development, review, or merge cycle must
immediately trigger organization of the next governed step. Completion is not
an instruction to become idle.

When the human maintainer reports that a PR is merged, the agent must inspect
the merged state and, in the same working cycle, select and prepare the next
bounded task or the smallest governance action needed to authorize it. The
agent must not wait for the human to ask what comes next.

If no approved task or prompt remains, the agent must assess the actual product
state instead of stopping merely because a queue is empty. That assessment
must use real product evidence where safely available: current merged code,
approved public fixtures, approved private fixtures in place, fresh conversion
output, maintainer real-world test observations, and direct inspection of the
resulting musical artifacts. The outcome must be one or more of:

- a verified next task selected from existing evidence;
- a bounded real-world validation prompt;
- newly recorded candidate bugs or requirements with evidence and limits; or
- an exact external prerequisite or maintainer action, while other safe
  planning continues.

Real-world testing is continuous product evidence, not a final-stage activity.
Maintainer observations must be incorporated at every stage and must override
optimistic aggregate diagnostics when they conflict.

This continuation rule does not authorize product implementation by itself,
permit a second task while a task PR remains open, or weaken identity, WSL,
privacy, review, branch, or merge gates. It requires the next step to be
organized and governed; it does not permit ungoverned execution.

## Unauthorized-Merge Incident Gate

If Agy executes, attempts, or reports any prohibited merge action, bypass flag,
direct push to `main`, force push, destructive worktree command, `git reset
--hard`, or `git clean -fd`,
the current task must be marked `BLOCKED` by a human or external reviewer.
Agy must then perform no further filesystem, Git, GitHub, or task work.

Work may resume only after a human or Codex has independently verified both:
1. the WSL GitHub CLI identifies `tticom-automation` and the local Git identity matches it; and
2. a protected `main` rule requires an independent pull-request approval and
   excludes `tticom-automation` from all bypass permissions.

A policy statement alone is not remediation. The enforcement state and identity
verification must be recorded in a governance PR before a blocked task is
reactivated.

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
3. `projects/score2gp/PR_EVIDENCE_CONTRACT.md` before creating or revising a PR
4. `projects/score2gp/ACTIVE_TASK.md`
5. `projects/score2gp/PLANNING_DATA.md`
6. `projects/score2gp/TASK_RECORDING_CONVENTION.md`
7. Relevant task template(s) under `projects/score2gp/templates/`

## Versioned Workflow Skills

Before executing or reviewing a task, read
`projects/score2gp/SKILLS_LOCK.md` and
`projects/score2gp/WORKFLOW_SKILLS_PROFILE.md`. Verify the installed skills
resolve to the exact locked `agy-skills` revision.

Do not update or relink skills during an active Score2GP task. Skills upgrades
require their own `agy-skills` PR followed by a separate AgentOps lock-update
PR; they are never an incidental part of product conversion work.

The lock-update PR itself is reviewed through a non-activating bootstrap: prove
its proposed pin is merged into `agy-skills/main`, materialize that pin in an
immutable checkout, and invoke the proposed review skill by its returned exact
path. The reviewer must not relink installed skills or treat the unmerged
AgentOps branch as active authority. This exception permits inspection only; it
does not authorize task execution or repository mutation.

The PR Evidence Contract is an author-side gate. It does not replace the
adversarial Reviewer role or human merge requirement. Its purpose is to make
the exact claims, proof, limits, and remaining unknowns inspectable in one
review pass before a PR is opened.

### Role skill loading

Every agent run for the Score2GP project must load and obey:

1. `projects/score2gp/AGENT_CONTROL.md`
2. `projects/score2gp/ACTIVE_TASK.md`
3. the relevant role skill file under `projects/score2gp/skills/<role>/SKILL.md`, if the role has a skill file
4. any task-specific prompt from the Orchestrator

For Architect work, the Architect must read:
`projects/score2gp/skills/architect/SKILL.md`

For Reviewer work, the Reviewer must read the exact pinned `review_skill`
returned by `scripts/score2gp_got_bootstrap.py`, then apply
`projects/score2gp/REVIEW_RULES.md` and the compatibility notes in
`skills/score2gp-pr-hard-review.md`.

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
  - One combined Devil's-Advocate Reviewer performs implementation conformance review and PR readiness review in a single pass for implementation PRs. The dispatch must explicitly invoke `devils-advocate-review`; a generic `code-review` or `hard-review` verdict alone does not satisfy the development loop.
  - One approved task normally produces exactly one product PR.
  - Governance completion records should be bundled with the next Orchestrator decision in `ACTIVE_TASK.md` or updated as direct run records, rather than requiring standalone governance PRs for routine completion bookkeeping.
  - Merge operators still perform the final guarded merge check.

#### Tier A: Full Loop (High-Risk Work)
Required only when a task involves:
- Uncertain architecture or new recognition strategies.
- Product behaviour changes or database schema modifications.
- Policy exceptions, failed reviews, or unapproved external-corpus/sensitive benchmark data claims.
- **Process**: Must follow separate sequential stages: Requirement -> Architect Research -> Reviewer Architecture Verification -> Developer Implementation -> explicit `devils-advocate-review` Conformance Review -> explicit `devils-advocate-review` PR Readiness Review -> Merge.

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

- Agy: `/home/tticom-automation/work/score2gp-workspace/score2gp`
- Governance: `/home/tticom-gov/work/score2gp-workspace/score2gp`

The selected path must match the identity-isolated workspace gate above.

and read:

`AGENTS.md`

n## Planning Data

Queues are non-executable planning data. The JSON task/incident model is the only authored authority. Agents must not execute tasks from a queue or automatically promote tasks without Orca Control Plane dispatch.

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
- **Branch check, switch, and creation workflow**:
  - Always check the current checked-out branch before making modifications.
  - If the current branch has been deleted, switch back to `main`.
  - If a branch already exists for the purpose of the change, switch to that branch.
  - If the changes are not part of the current active task, create a new branch instead of committing to the current branch.

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
- **Reviewer**: reviews code/docs/process/evidence and publishes formal review
  metadata, useful inline comments, and one mandatory PR summary comment. The
  Reviewer never modifies repository content, refs, branches, commits, PR
  bodies, task state, prompts, reports, or evidence artifacts.
- **Researcher**: investigates uncertainty and records evidence without changing product implementation unless approved.

### Forbidden Actions

Agents must not push directly to `main`, force-push, run `git reset --hard`, run
`git clean` with deletion flags, delete branches, bypass failing checks, approve
their own PR, or expand scope without authority. Reviewer mode permits review
metadata only. `tticom-automation` and `tticom-gov` must never attempt a merge.

### Human-Only Operations

Only the human maintainer or a separately operated external release integrator
may merge a PR, approve scope expansion, accept a known failing-check risk, or
explicitly close/abandon a task without merge. `tticom-automation` and
`tticom-gov` have no merge exception. `tticom-codex` may merge only after a
separate current explicit `tticom` instruction naming the exact repository, PR
number, and reviewed full head SHA.

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

Every functional change must be generic and traceable to real-source
PDF/MusicXML/GPIF evidence. Domain acceptance tests must use a genuine approved
source or a reproducible extract that retains source provenance and reaches the
changed production seam. Synthetic, mocked, generated-notation, invented-value,
and data-free tests carry zero acceptance weight for recognition, conversion,
timing, grouping, geometry, parser, or fidelity claims. They may supplement
non-domain infrastructure coverage only with an explicit rationale. General
claims require more than one approved corpus input.

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
