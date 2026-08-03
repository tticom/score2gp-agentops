# Active Task

**Task**: MXS-09: Architecture Decision and Smallest Next Implementation
**Status**: APPROVED
**Assigned Identity**: tticom-gov
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**PR Branch**: `none`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`

## Context

Task `MXS-08` completed, establishing the [Blind Comparative Bake-Off Report](file:///home/tticom-codex/work/score2gp-workspace/score2gp-agentops/projects/score2gp/reviews/2026-08-03-mxs08-comparative-bake-off-report.md). The bake-off established that zero candidates qualify as fully automated headless Linux CLI tools (`viable_automated`), while PDFtoMusic Pro and PhotoScore Ultimate represent the winning assisted sidecar producers (`viable_assisted`). Per the research plan, the project now authorizes task `MXS-09` of the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`).

## Goal

Issue the final Architecture Decision Record (ADR) selecting **Outcome B — Adopt an Assisted Sidecar Workflow**. Define the human operator correction and validation boundary, sidecar provenance manifest, acceptance criteria, and smallest next workflow task.

## Allowed Files

- `projects/score2gp/reviews/2026-08-03-mxs09-architecture-decision-record.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No product code changes in `score2gp`.
- Do not authorize unapproved third-party production dependencies.

## Acceptance

Document the exact selection of Outcome B, formalizing the assisted sidecar ingest workflow, operator validation contract, candidate-neutral evaluator integration (`score2gp eval-sidecar`), and smallest next governance task.
