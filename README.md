# score2gp-agentops

External agent-ops architecture for governing agentic development of ScoreToGP.

This repository is for control-plane artifacts only. It defines how implementation agents, reviewer/architect agents, and human maintainers coordinate work on ScoreToGP without mixing prompts, review rubrics, diagnostic policy, or benchmark governance into product code.

It does not claim conversion progress, does not alter ScoreToGP source code, and must not contain private benchmark assets.

## Bootstrapping

To ensure that agent runs are executed on up-to-date control planes, this repository includes a bootstrap script at `./scripts/bootstrap.py`.

At the start of a conversation, the agent runs:
```bash
./scripts/bootstrap.py
```
This script:
1. Fetches from origin and checks if the local `agentops` repository is behind its remote tracking branch. If behind, it aborts with a non-zero exit code.
2. Reads the JSON agent definitions from `.agents/agents/` and outputs them as a formatted JSON array to stdout, which the parent agent can read and use to register the subagents via the `define_subagent` tool.


## Separation Of Responsibilities

### Product Repository

The ScoreToGP product repository owns:

- Source code, tests, schemas, fixtures, and CLI behavior.
- Public fixtures that are safe to commit.
- Product documentation that explains user-facing behavior.
- Conversion correctness, validation behavior, and export behavior.
- CI for product tests and product quality gates.

The product repository must not become the home for agent-control prose. Product correctness is separate from agent-control prose.

### Agent-Ops Repository

This repository owns:

- Review rules and evidence standards for agentic work.
- Benchmark ladder policy and acceptance targets.
- Prompt templates for implementation and review agents.
- Architecture decisions about agent workflows.
- Rejected claims and recurring failure modes.
- Human maintainer decision workflow.

The agent-ops repository evaluates and directs product work, but it does not prove that the product improved. Handoff quality is not conversion quality.

## Workflow Model

### Implementation Agent

The implementation agent receives a scoped implementation prompt from this repository and works inside the ScoreToGP product repository. It must:

- State the target benchmark rung and acceptance target before editing.
- Keep product code changes separate from agent-control documents.
- Report strict mode, remediation mode, semantic comparison, and generated-file existence separately.
- Use visual/source evidence where available.
- Avoid committing private assets.
- Avoid claiming conversion progress without benchmark evidence.

### Reviewer/Architect Agent

The reviewer/architect agent evaluates the implementation output before writing the next implementation prompt. It must:

- Inspect source artifacts, visual evidence, logs, generated files, and diffs.
- Treat diagnostic tables as evidence, not truth.
- Prefer visual/source evidence over generated summaries.
- Identify whether failures are parser, semantic, rendering, or workflow failures.
- Write the next prompt only after evaluation is complete.

### Human Maintainer

The human maintainer decides:

- Which benchmark rung is currently active.
- Whether a change is accepted, rejected, or needs remediation.
- Whether private evidence can be inspected locally.
- Whether a PR can move from draft to review-ready.
- Whether a benchmark result is meaningful enough to update acceptance targets.

Human maintainers should treat agent output as advisory. Maintainer decisions must be grounded in reproducible checks and direct evidence.

## ScoreToGP Project Documents

Project-specific governance lives under `projects/score2gp/`:

- `REVIEW_RULES.md`
- `BENCHMARK_LADDER.md`
- `ACCEPTANCE_TARGETS.md`
- `ARCHITECTURE_DECISIONS.md`
- `REJECTED_CLAIMS.md`
- `PR_REVIEW_TEMPLATE.md`
- `IMPLEMENTATION_PROMPT_TEMPLATE.md`
- `REVIEW_PROMPT_TEMPLATE.md`

## Privacy Rule

Private assets remain private and must never be committed. Private benchmark names may be referenced as benchmark rungs, but files, images, PDFs, exports, or derived confidential data must stay outside version control.

## AGY Cycle v2 Operation

The supported delivery process is a deterministic, one-task/one-PR AGY cycle.
The full design and comparison with the earlier integrated PR lifecycle are in
[`docs/agy-cycle-v2-plan.md`](docs/agy-cycle-v2-plan.md).

### Source of truth

- [`.agy/flow.yaml`](.agy/flow.yaml) defines lifecycle transitions and hard
  limits. It is the one file a human edits when the state flow is wrong.
- [`plan/backlog.yaml`](plan/backlog.yaml) defines sprints, tasks, ordering,
  dependencies, cardinality, scope, acceptance, and validation.
- `.agy/cycles/` contains ignored runtime records and atomic claim locks.

`ACTIVE_TASK.md` and `ORCHESTRATION_STATE.json` are compatibility views only;
they are not separately authored during an AGY Cycle.

### Normal cycle

From the repository root:

```bash
python3 -m pip install -r requirements-agy-cycle.txt
scripts/agy-cycle claim
scripts/agy-cycle next CYCLE-ID
scripts/agy-cycle run CYCLE-ID
scripts/agy-cycle status CYCLE-ID
```

`run` starts the configured interactive AGY CLI in a PTY and injects the bounded
task prompt. AGY edits only the assigned worktree; it does not select another
task, change lifecycle state, open a second PR, or merge.

The controller/orchestrator then performs explicit transitions and attaches the
single PR:

```bash
scripts/agy-cycle transition CYCLE-ID IMPLEMENTING
scripts/agy-cycle transition CYCLE-ID VALIDATING
scripts/agy-cycle validate CYCLE-ID
scripts/agy-cycle open-pr CYCLE-ID --repository ORG/REPO
scripts/agy-cycle verify-pr CYCLE-ID
scripts/agy-cycle transition CYCLE-ID REVIEW_REQUIRED
```

The PR head must be read back and match the recorded SHA before review or merge
readiness. Reviewers use an exact-head, read-only worktree. Review fixes remain
on the same branch and PR. After a human merge, reconciliation is explicit:

```bash
scripts/agy-cycle transition CYCLE-ID APPROVED
scripts/agy-cycle transition CYCLE-ID MERGE_READY
scripts/agy-cycle reconcile CYCLE-ID
scripts/agy-cycle reconcile CYCLE-ID
```

The second reconciliation call is intentionally safe and demonstrates
idempotence. Successor tasks are prepared only; they are never implicitly
started.

### Concurrent cycles and repair

Task claims are atomic. Independent tasks can run simultaneously because each
cycle has a unique lease, branch, worktree, runtime directory, and PR. Declare
`resource_group` in the backlog when two tasks must not edit the same area at
the same time.

To repair a stuck cycle:

```bash
scripts/agy-cycle status CYCLE-ID
scripts/agy-cycle reset CYCLE-ID FAILED
scripts/agy-cycle reset CYCLE-ID READY
```

Docker is optional hardening, not a process dependency. Normal execution uses
disposable worktrees, explicit allowed paths, sanitized Git configuration,
isolated runtime records, and read-only reviewer worktrees.
