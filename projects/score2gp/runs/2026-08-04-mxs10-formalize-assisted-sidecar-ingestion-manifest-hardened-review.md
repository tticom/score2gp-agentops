# Governance Review Record — MXS-10 Formalize Assisted Sidecar Ingestion & Provenance Manifest Contract (Hardened Head)

**Task**: MXS-10: Formalize Assisted Sidecar Ingestion & Provenance Manifest Contract
**Date**: 2026-08-04
**Governance Publisher**: `tticomgov-code`
**Independent Reviewer**: `tticom-codex`
**Product Repository**: `tticom/score2gp`
**Product Main SHA**: `9e37e89a33f54c71462c976656fda397fb5c02cf`
**Product PR**: [#401](https://github.com/tticom/score2gp/pull/401) (`agy/mxs10-assisted-sidecar-ingestion-manifest`)
**Product Head SHA**: `9a0dd05185ed14596a8804555f8d75bf011720d6`
**Review Verdict**: APPROVED (Review ID `4855160170`)
**AgentOps Main SHA**: `ccd000c0f9b415e30fac953866dcad01d55183ee`
**Skills Lock SHA**: `d24d69a3d23aae733245eabd6b9fcf76c0b16803`

## Executive Summary

Developer task `MXS-10` (Formalize Assisted Sidecar Ingestion & Provenance Manifest Contract) implemented on branch `agy/mxs10-assisted-sidecar-ingestion-manifest` has been re-reviewed against exact hardened head commit `9a0dd05185ed14596a8804555f8d75bf011720d6`.

The updated implementation addresses all 4 reviewer findings from the previous cycle:
1. **Case-Insensitive SHA Comparison**: `actual_sidecar_sha256.lower() != manifest.sidecar_sha256.lower()` and `actual_pdf_sha256.lower() != manifest.pdf_sha256.lower()`.
2. **`pdf_sha256` Cross-Validation**: `validate_sidecar_manifest` cross-validates `manifest.pdf_sha256` against `_compute_sha256(pdf_path)` when supplied in CLI.
3. **Pydantic Model Constraints**: Added `operator_id: min_length=1`, `operator_labor_minutes: ge=0.0`, `sidecar_sha256: pattern=r"^[0-9a-fA-F]{64}$"`, and `pdf_sha256: pattern=r"^[0-9a-fA-F]{64}$"`.
4. **Clean File Path Checks**: Added explicit `is_file()` checks to reject directory paths with clean `ValueError` exceptions before file reads.

## Key Verification Evidence

- **Targeted Suite**: 8 passed in `tests/test_mxs10_sidecar_ingestion_manifest.py`.
- **Independent Reviewer Probes**:
  - Probe 1 (Uppercase SHA-256 case normalization): verified successful validation with uppercase manifest SHA string.
  - Probe 2 (Mismatched `pdf_sha256` rejection): verified `ValueError("PDF SHA-256 mismatch")` raised when PDF SHA mismatches input PDF.
  - Probe 3 (Negative labor minutes rejection): verified Pydantic `ValidationError` raised on `-5.0`.
  - Probe 4 (Non-hex SHA regex rejection): verified Pydantic `ValidationError` raised on invalid hex pattern.
  - Probe 5 (Directory path rejection): verified clean `ValueError` raised on directory paths.
- **Scope Compliance**: Scope strictly restricted to authorized files (`src/score2gp/cli.py`, `src/score2gp/sidecar_evaluator.py`, `src/score2gp/report.py`, `tests/test_mxs10_sidecar_ingestion_manifest.py`).
