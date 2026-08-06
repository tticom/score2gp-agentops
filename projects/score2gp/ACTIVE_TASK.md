# Active Task

**Task**: FS-02: Reconcile Uncontrolled Runtime and Canonical Conversion Entry Point
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/fs02-reconcile-entry-point`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/2026-07-19-teamwork-runtime-provenance-functional-stabilisation.md`

## Context

Task `FS-01` (Runtime Provenance Baseline and Corpus Stabilisation Harness) completed and merged via product PR #409 (`2101d8cf65ed6fad3d3984657703d131a165b97b`). The project now promotes task `FS-02` from `APPROVED_TASK_QUEUE.md` under the `Runtime-Provenance and Functional-Stabilisation Series` to reconcile the canonical conversion entry point and establish a committed source-to-output call chain.

## Goal

Conduct an Architect phase for `FS-02` to verify and trace the canonical conversion route in `score2gp`, confirming whether `score2gp convert` or `score2gp omr` forms the committed entry point and establishing evidence bounds for downstream functional gates (FS-03/FS-04).

## Allowed Files

- `projects/score2gp/reports/2026-08-06-fs02-canonical-entry-point-architecture.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No product code changes in the Architect phase.
- Do not bypass canonical entry-point verification or invent uncommitted conversion routes.

## Acceptance

Produce an architecture report detailing the verified source-to-output conversion entry point, allowed call chain, and evidence bounds. Publish one governance pull request on branch `gov/promote-fs02-reconcile-entry-point` in `tticom/score2gp-agentops` for independent Codex review.
