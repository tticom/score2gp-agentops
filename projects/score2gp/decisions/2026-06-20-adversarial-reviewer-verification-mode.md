# Adversarial Reviewer Verification Mode

## Decision

Score2GP reviewer roles must use adversarial verification mode.

The Reviewer is a gatekeeper, not a collaborator, cheerleader, second Architect, or implementation assistant. Reviewer approval must start from `cannot verify` and must be earned through independently verified evidence.

## Reason

Recent workflow reviews showed that reviewer agents were too agreeable. They tended to approve plausible architecture or implementation reports instead of actively testing whether the next step was safe, narrow, evidence-backed, and incrementally useful.

This created a risk of false progress: tasks could be approved because they sounded coherent, not because the repository state, source code, fixtures, tests, diagnostics, PR metadata, and artifact hygiene proved readiness.

## Policy Change

`projects/score2gp/AGENT_PR_READINESS.md` now defines `Reviewer Role Contract — Adversarial Verification Mode`.

`projects/score2gp/REQUIREMENT_PROMPTING_CONTRACT.md` now requires reviewer prompts to invoke adversarial verification mode for architecture review, implementation conformance review, PR readiness review, and merge readiness review.

## Required Reviewer Behaviour

Reviewers must:

- start from `cannot verify`;
- treat missing evidence as a blocker;
- independently verify key claims;
- test likely failure modes before approving;
- reject summary-only approval;
- label claims as `verified`, `partially verified`, `not verified`, `contradicted`, or `out of scope`;
- approve only the smallest safe task;
- reject false progress;
- require product-level evidence for recognition, export, conversion, pipeline, and workflow behaviour.

## Consequence

Future reviewer prompts must be written as adversarial verification tasks. A Reviewer that cannot independently verify the evidence must return `cannot verify implementation`, `needs stronger research`, `return to architect`, `NEEDS CHANGES`, or `NOT READY` instead of approving.
