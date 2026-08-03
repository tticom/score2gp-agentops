# Active Task

**Task**: MXS-08: Run the Blind Comparative Bake-Off
**Status**: APPROVED
**Assigned Identity**: tticom-gov
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**PR Branch**: `none`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`

## Context

Task `MXS-07` completed, establishing the [Assisted Manual Entry Control Evaluation Report](file:///home/tticom-codex/work/score2gp-workspace/score2gp-agentops/projects/score2gp/reviews/2026-08-03-mxs07-assisted-manual-entry-control-evaluation.md). Manual entry serves as the accuracy ($100\%$) and labor cost (~15 min/page) benchmark. Per the research plan, the project now authorizes task `MXS-08` of the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`).

## Goal

Run all evaluated candidates against the common fixture set and evaluation contract (`score2gp eval-sidecar`). Score note/rest precision and recall, onset/duration agreement, Score2GP handoff, WSL automation, human correction minutes per page, and operational risks in a comparative matrix.

## Allowed Files

- `projects/score2gp/reviews/2026-08-03-mxs08-comparative-bake-off-report.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No product code changes in `score2gp`.
- Do not let weighted scores mask fatal timing errors or empty output.

## Acceptance

Produce comparative bake-off matrix covering Audiveris, PDFtoMusic Pro, `oemer`, PhotoScore/ScanScore, Cloud APIs, and Manual Entry. Prepare the evidence required for the final Architecture Decision Record (**MXS-09**).
