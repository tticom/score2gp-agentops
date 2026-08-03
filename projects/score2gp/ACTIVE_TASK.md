# Active Task

**Task**: MXS-04: Evaluate Local Open-Source OMR Challengers
**Status**: APPROVED
**Assigned Identity**: tticom-gov
**Authorised Role**: Researcher
**Repository**: tticom/score2gp-agentops
**PR Branch**: `none`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`

## Context

Task `MXS-03` completed, establishing the [PDFtoMusic Pro Evaluation Report](projects/score2gp/reviews/2026-08-03-mxs03-pdftomusic-pro-evaluation.md). PDFtoMusic Pro was classified as `viable_assisted` for vector PDFs but `not_viable_automated` for headless Linux server pipelines. The project now authorizes task `MXS-04` of the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`).

## Goal

Evaluate local open-source OMR engines (beginning with `oemer` and `homr`-class systems) in isolated environments. Record repository revision, licence, model provenance, model-download hashes, CPU/GPU requirements, supported notation, offline operation, and whether PDF rendering/preprocessing is required. Apply `score2gp eval-sidecar` to evaluate exported MusicXML artifacts against the common contract.

## Allowed Files

- `projects/score2gp/reviews/2026-08-03-mxs04-local-open-source-omr-challengers.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No product code changes in `score2gp`.
- Do not contaminate candidate verdicts if one engine or model fails.
- No opaque model training or unapproved model downloads.

## Acceptance

Apply the common contract using `score2gp eval-sidecar`. Evaluate candidate engines in isolated Linux environments and record cold-start, repeat-run determinism, licensing, model provenance, and exported MusicXML quality.
