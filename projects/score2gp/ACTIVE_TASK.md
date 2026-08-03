# Active Task

**Task**: MXS-10: Formalize Assisted Sidecar Ingestion & Provenance Manifest Contract
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/mxs10-assisted-sidecar-ingestion-manifest`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0029-mxs10-assisted-sidecar-ingestion-manifest.md`

## Context

Task `MXS-09` completed, issuing the [Architecture Decision Record (ADR)](file:///home/tticom-codex/work/score2gp-workspace/score2gp-agentops/projects/score2gp/reviews/2026-08-03-mxs09-architecture-decision-record.md) selecting **Outcome B — Adopt an Assisted Sidecar Workflow**. The project now authorizes Developer slice `MXS-10` in `tticom/score2gp` to formalize the assisted sidecar ingestion and provenance manifest contract.

## Goal

Extend `score2gp convert` to support `--sidecar-manifest <path>`, validating sidecar SHA-256 hashes against `SidecarEvaluationResult`, requiring `eval_status == "passed"`, and embedding sidecar provenance into generated HTML conversion reports.

## Allowed Files

- `src/score2gp/cli.py`
- `src/score2gp/sidecar_evaluator.py`
- `src/score2gp/report.py`
- `tests/test_mxs10_sidecar_ingestion_manifest.py`

## Non-goals

- No change to default PDF-only processing when no `--musicxml` sidecar is specified.
- No third-party network API calls or unapproved dependency additions.

## Acceptance

Pass validation suite (`pytest tests/test_mxs10_sidecar_ingestion_manifest.py` and `python scripts/agent_verify.py`). Assert exact validation behavior for valid manifests, SHA-256 mismatches, and unpassed eval statuses. Publish one Developer pull request on branch `agy/mxs10-assisted-sidecar-ingestion-manifest` in `tticom/score2gp` for independent Codex review.
