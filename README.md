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
