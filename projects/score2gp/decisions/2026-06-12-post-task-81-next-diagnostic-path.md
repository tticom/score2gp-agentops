# Governance Decision: Post-Task 81 Next Diagnostic Path

## Date
2026-06-12

## Context
Product PR #247 (Task 81) was successfully merged:
- Merge commit SHA: 991818bae9b3e0c672c3437f7fc5fd4cc026d01c
- Final head SHA: f8693587fcd3d3cd2162cd0f37d9935daac27698
- Files changed:
  - `scripts/raster_diagnostics_gate_report.py`
  - `tests/test_raster_diagnostics_gate_report.py`

Task 81 closed the remaining pre-CI testability gap by proving both PASS and REVIEW subprocess behaviour safely.
Specifically, it:
- Added a safe `--test-manifest` testability seam.
- Proved REVIEW subprocess behaviour:
  - `--check` returns exit code 1 for REVIEW.
  - `--json --check` returns exit code 1 for REVIEW.
  - JSON remains parseable for REVIEW.
- Preserved PASS-path subprocess tests.
- Rejected unsafe manifest paths without leaking private paths, absolute paths, temp paths, or raw local paths.
- Did not change classifier thresholds, recognition semantics, ScoreIR, OCR, vector/raster fusion, or musical inference.

The raster diagnostics gate report is now suitable for cautious CI integration, but semantic promotion and classifier hardening remain blocked.

## Decision
We authorise **Product Task 83** as the next diagnostic-only product task.

### Recommended Next Path: Task 83
Task 83 will focus on adding a non-enforcing CI/advisory workflow or CI job for the raster diagnostics gate report.

**Rationale:**
The gate report now has:
- human output
- JSON output
- check mode
- subprocess PASS tests
- subprocess REVIEW tests
- privacy-safe manifest handling

The next useful step is to make this repeatable in CI as an advisory/product-health signal before any required branch-protection enforcement or classifier tuning is considered.

### Task 83 Requirements:
Task 83 should:
- add a CI workflow or CI job that runs the raster diagnostics gate report against the authorised public/default fixture set;
- run at least:
  - `python scripts/raster_diagnostics_gate_report.py`
  - `python scripts/raster_diagnostics_gate_report.py --json`
  - `python scripts/raster_diagnostics_gate_report.py --check`
  - optionally `pytest tests/test_raster_diagnostics_gate_report.py`
- ensure JSON output is not committed as an artifact unless explicitly justified and privacy-safe;
- avoid relying on private fixtures in CI;
- document that the CI job is advisory/non-required unless branch protection separately makes it required;
- preserve existing test workflows and avoid broad unrelated CI changes.

Task 83 must not:
- change classifier thresholds;
- tune or harden detection heuristics;
- add semantic recognition;
- emit ScoreIR;
- create recognised clef objects;
- add OCR;
- add vector/raster fusion;
- add pitch/rhythm/key/time inference;
- require private fixtures in CI;
- upload raw diagnostic JSON, screenshots, PDFs, GP files, logs, or private artifacts;
- alter branch protection or repository settings;
- modify governance repo files during product implementation.

## Blocked Actions
CI enforcement may now be explored only as a product CI implementation task, not as semantic promotion.
Semantic promotion, classifier hardening, OCR, vector/raster fusion, and ScoreIR remain strictly **blocked**.
