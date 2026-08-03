# Active Task

**Task**: MXS-02: Establish the Current Audiveris Control
**Status**: APPROVED
**Assigned Identity**: tticom-gov
**Authorised Role**: Researcher
**Repository**: tticom/score2gp-agentops
**PR Branch**: `none`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`

## Context

Task `MXS-01` completed, establishing the [Corpus Recoverable PDF Evidence Matrix](file:///home/tticom-codex/work/score2gp-workspace/score2gp-agentops/projects/score2gp/reviews/2026-08-03-mxs01-corpus-recoverable-evidence-matrix.md), confirming 100% of approved public inputs are born-digital vector PDFs. The project now authorizes research task `MXS-02` of the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`).

## Goal

Repeat the common evaluation contract with the current supported Audiveris release and its documented batch transcription/export invocation. Compare it against the historical 5.7.0 zero-note baseline (`FS-03E`) to verify whether the zero-note boundary changes.

## Allowed Files

- `projects/score2gp/reviews/2026-08-03-mxs02-audiveris-control-baseline.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No product code changes in `score2gp`.
- Do not begin product integration if output remains empty or timing-invalid.

## Acceptance

Record exact Audiveris release/hash/runtime, command, logs, output structure, two-run determinism, and fixture matrix. Compare against the candidate-neutral evaluation harness (`score2gp eval-sidecar`).
