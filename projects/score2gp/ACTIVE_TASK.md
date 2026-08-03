# Active Task

**Task**: MXS-05: Evaluate Commercial Desktop OMR as Assisted Sidecar Producers
**Status**: APPROVED
**Assigned Identity**: tticom-gov
**Authorised Role**: Researcher
**Repository**: tticom/score2gp-agentops
**PR Branch**: `none`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`

## Context

Task `MXS-04` completed, establishing the [Local Open-Source OMR Challengers Evaluation Report](file:///home/tticom-codex/work/score2gp-workspace/score2gp-agentops/projects/score2gp/reviews/2026-08-03-mxs04-local-omr-challengers-evaluation.md). `oemer` was rejected due to external weight dependencies, image rasterization requirements, and lack of TAB staff support. Per the research plan, the project now authorizes task `MXS-05` of the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`).

## Goal

Evaluate commercial desktop OMR software (ScanScore, SmartScore, PhotoScore, PlayScore) as potential assisted sidecar producers. Establish supported input types, MusicXML export capabilities, platform support, trial limitations, and whether a CLI/SDK/API exists.

## Allowed Files

- `projects/score2gp/reviews/2026-08-03-mxs05-commercial-desktop-omr-evaluation.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No product code changes in `score2gp`.
- Do not purchase licenses or subscriptions without explicit maintainer approval.
- Do not assume automation without verifying CLI/SDK availability.

## Acceptance

Evaluate each commercial tool against the common contract using `score2gp eval-sidecar`. Categorize each tool as `viable_automated`, `viable_assisted`, `not_viable`, or `not_evaluated` with exact blockers.
