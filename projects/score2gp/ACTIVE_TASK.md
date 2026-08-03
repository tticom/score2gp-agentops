# Active Task

**Task**: MXS-07: Measure Assisted Manual Entry as the Accuracy/Cost Control
**Status**: APPROVED
**Assigned Identity**: tticom-gov
**Authorised Role**: Researcher
**Repository**: tticom/score2gp-agentops
**PR Branch**: `none`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`

## Context

Task `MXS-06` completed, establishing the [Cloud/API Routes Privacy Evaluation Report](file:///home/tticom-codex/work/score2gp-workspace/score2gp-agentops/projects/score2gp/reviews/2026-08-03-mxs06-cloud-api-routes-privacy-evaluation.md). Cloud/API routes were rejected due to lack of PDF OMR and unverified data retention terms. Per the research plan, the project now authorizes task `MXS-07` of the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`).

## Goal

Enter the public control score (`generated_tiny_tab.pdf` / `generated_standard_staff_whole_note.pdf`) in a MusicXML-capable notation editor (e.g., MuseScore / Guitar Pro) using a fixed procedure. Measure active entry time, corrections, and final `score2gp eval-sidecar` results as the control for deciding whether OMR saves meaningful effort over manual entry.

## Allowed Files

- `projects/score2gp/reviews/2026-08-03-mxs07-assisted-manual-entry-control-evaluation.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No product code changes in `score2gp`.
- Do not treat manual entry as a scalable product solution without measured comparison.

## Acceptance

Produce timing-safe MusicXML matching the public oracle at bar/event level (`status="passed"`). Record active entry time (minutes per page) and correction count as the baseline control for the comparative bake-off (**MXS-08**).
