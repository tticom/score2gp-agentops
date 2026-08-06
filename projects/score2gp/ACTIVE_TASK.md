# Active Task

**Task**: MXS-10: Assisted Sidecar Ingestion Manifest
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer
**Repository**: tticom/score2gp
**PR Branch**: `agy/mxs10-assisted-sidecar-ingestion-manifest-v2`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0029-mxs10-assisted-sidecar-ingestion-manifest.md`

## Context

Task `MXS-00` (Candidate-Neutral Sidecar Evaluation Harness) completed and merged via product PR #411 (`562ea6f83b57588a3a4579debae79867b0d24ff5`). The project now promotes task `MXS-10` from `APPROVED_TASK_QUEUE.md` under the MusicXML Sidecar Ingestion Series to formalize assisted sidecar ingestion and provenance manifest contract.

## Goal

Extend `score2gp convert` to support `--sidecar-manifest <path>`, validating sidecar SHA-256 hashes against `SidecarEvaluationResult`, requiring `eval_status == "passed"`, and embedding sidecar provenance into generated HTML conversion reports.

## Allowed Files

- `src/score2gp/cli.py`
- `src/score2gp/sidecar_evaluator.py`
- `src/score2gp/report.py`
- `tests/test_mxs10_sidecar_ingestion_manifest.py`
- `projects/score2gp/ACTIVE_TASK.md`

## Non-goals

- No change to default PDF-only processing when no `--musicxml` sidecar is specified.
- No third-party network API calls or unapproved dependency additions.

## Acceptance

Extend `sidecar_evaluator.py` with `SidecarProvenanceManifest` and `validate_sidecar_manifest()`, add `--sidecar-manifest` cli flag, update HTML report rendering, pass `test_mxs10_sidecar_ingestion_manifest.py` and `scripts/agent_verify.py`, update `ACTIVE_TASK.md`, and publish one product pull request on branch `agy/mxs10-assisted-sidecar-ingestion-manifest-v2` in `tticom/score2gp` for independent Codex review.
