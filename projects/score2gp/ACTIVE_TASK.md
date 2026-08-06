# Active Task

**Task**: CR-04A: False-Rest and Per-Voice Capacity Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/cr04a-false-rest-capacity-architecture-v2`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0007-cr04a-false-rest-capacity-architecture.md`

## Context

Task `FS-02` (Reconcile Uncontrolled Runtime and Canonical Conversion Entry Point) completed and merged via PR #472 (`2aa977445d54ab8462dc9432ef9535af2afe57ad`). The project now promotes task `CR-04A` from `APPROVED_TASK_QUEUE.md` under the Visual Output Correctness Series to investigate and define the false-rest rejection and per-voice capacity gate.

## Goal

Locate the first committed-evidence divergence creating the Lesson-5 false-rest candidate, define a deterministic per-voice measure-capacity gate, and produce a Developer-ready rule and public regression plan in an architecture report.

## Allowed Files

- `projects/score2gp/reports/2026-08-06-cr04a-architecture.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Bounded architecture and diagnostic task only; no product code changes in the Architect phase.

## Acceptance

Produce the CR-04A architecture report, update `ACTIVE_TASK.md`, and publish one governance pull request on branch `agy/cr04a-false-rest-capacity-architecture-v2` in `tticom/score2gp-agentops` for independent Codex review.
