# Active Task

**Task**: CR-04A: Current-Runtime Lesson-5 Evidence Replay
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr04a-current-runtime-evidence-replay`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0008-cr04a-current-runtime-evidence-replay.md`

## Context

Task `CR-04A` (False-Rest and Per-Voice Capacity Architecture) completed and merged via governance PR #474 (`622a6489e285c670d4942526bc7141541a6f4f1b`). The project now promotes task `CR-04A Evidence Replay` from `APPROVED_TASK_QUEUE.md` to evaluate current runtime Lesson-5 evidence against product `origin/main`.

## Goal

Determine whether the false 1920-tick half rest recorded by the historical Lesson-5 ledger still enters the current conversion path at product `origin/main`. Produce the smallest next decision from current evidence without modifying product code.

## Allowed Files

- `projects/score2gp/reports/2026-07-24-cr04a-current-runtime-replay.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- Architect evidence collection only; no product code modifications.

## Acceptance

Produce the CR-04A current-runtime replay report, update `ACTIVE_TASK.md`, and publish one governance pull request on branch `agy/cr04a-current-runtime-evidence-replay` in `tticom/score2gp-agentops` for independent Codex review.
