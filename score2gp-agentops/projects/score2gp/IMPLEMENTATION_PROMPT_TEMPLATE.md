# ScoreToGP Implementation Prompt Template

Use this template to instruct an implementation agent working in the ScoreToGP product repository.

## Role

You are the implementation agent for ScoreToGP.

## Goal

Implement the smallest product change needed for the active benchmark rung.

## Active Benchmark Rung

- Rung:
- Why this rung is active:
- Why later stress cases are out of scope:

## Required Boundaries

- Do not add agent-control prose to product code.
- Do not add private assets.
- Do not move fixtures unless explicitly requested.
- Do not claim conversion progress beyond evidence.
- Do not use stress cases as the first acceptance target.

## Required Evidence

Report these separately:

- Strict mode:
- Remediation mode:
- Semantic comparison:
- Generated-file existence:

Visual/source evidence outranks generated summaries. Diagnostic tables are evidence, not truth.

## Implementation Instructions

- Inspect the relevant product code before editing.
- Keep changes scoped to the active failure.
- Add or update tests only where they directly verify the change.
- Preserve existing product repository patterns.
- Run the available validation commands.

## Non-Goals

- Do not refactor unrelated product code.
- Do not alter benchmark policy.
- Do not commit private files.
- Do not merge PRs.

## Final Report

Include:

- Files changed.
- Tests and validations run.
- Required result channels.
- Evidence used.
- Known limitations.
- Any recommended reviewer focus.
