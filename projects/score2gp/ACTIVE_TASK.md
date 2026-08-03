# Active Task

**Task**: MXS-03: Evaluate Vector-PDF Extraction with PDFtoMusic Pro
**Status**: APPROVED
**Assigned Identity**: tticom-gov
**Authorised Role**: Researcher
**Repository**: tticom/score2gp-agentops
**PR Branch**: `none`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`

## Context

Task `MXS-02` completed, establishing the [Audiveris Control Baseline Report](file:///home/tticom-codex/work/score2gp-workspace/score2gp-agentops/projects/score2gp/reviews/2026-08-03-mxs02-audiveris-control-baseline.md). Audiveris 5.7.0 produced 100% `empty_musicxml` on all mixed notation/TAB fixtures. Per the research plan, the project now authorizes task `MXS-03` of the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`).

## Goal

Evaluate PDFtoMusic Pro on the vector fixture subset identified in `MXS-01`. Record whether vector-native PDF interpretation supports unattended CLI invocation, stable MusicXML export, non-empty note/rest output, and timing-safe handoff via `score2gp eval-sidecar`.

## Allowed Files

- `projects/score2gp/reviews/2026-08-03-mxs03-pdftomusic-pro-evaluation.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No product code changes in `score2gp`.
- Do not purchase licenses without explicit maintainer approval.
- Do not claim raster PDF support (vector PDFs only).

## Acceptance

Apply the common contract using `score2gp eval-sidecar`. Compare exported MusicXML at bar/event level with `generated_tiny_tab.musicxml`. Explicitly document licensing, platform support, CLI availability, and whether at least one mixed vector fixture produces non-empty, timing-safe MusicXML.
