# Active Task

**Task**: MXS-01: Classify Approved Corpus by Recoverable PDF Evidence
**Status**: APPROVED
**Assigned Identity**: tticom-gov
**Authorised Role**: Architect
**Repository**: tticom/score2gp-agentops
**PR Branch**: `none`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`

## Context

PR #400 on `tticom/score2gp` (`agy/mxs00-candidate-neutral-sidecar-evaluation-harness`) was merged into product `main` at commit `9e37e89a33f54c71462c976656fda397fb5c02cf`, establishing the candidate-neutral sidecar evaluation harness (`src/score2gp/sidecar_evaluator.py`). The project now authorizes task `MXS-01` of the MusicXML Sidecar Generation Alternatives Research Plan (`projects/score2gp/tasks/2026-08-03-musicxml-sidecar-generation-alternatives.md`).

## Goal

Classify each approved public input score (and private inputs only locally after explicit maintainer approval) as vector notation, raster scan, mixed vector/raster, or unknown. Record embedded fonts, vector paths/text, page rendering needs, and whether notation objects appear recoverable without raster recognition.

## Allowed Files

- `projects/score2gp/reviews/2026-08-03-mxs01-corpus-recoverable-evidence-matrix.md`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No product code changes in `score2gp`.
- No upload of private input files to third-party services.
- No inference that vector presence guarantees semantic recovery.

## Acceptance

Produce a privacy-safe matrix and select vector-first and raster-first fixture subsets. Enable the decision of whether vector-first extraction (e.g., PDFtoMusic Pro in `MXS-03`) or raster OMR (e.g., Audiveris / `oemer` in `MXS-02`/`MXS-04`) takes priority for the real-world corpus.
