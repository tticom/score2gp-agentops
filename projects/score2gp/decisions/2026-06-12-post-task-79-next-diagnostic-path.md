# Decision: Task 80 — Record Task 79 completion and select next diagnostic-only path

**Date:** 2026-06-12
**Status:** Accepted
**Context:** Product PR #246 (Task 79)

## 1. Task 79 Completion and Available Evidence
Product PR #246 (Task 79) has been merged (merge commit `008b3c5d700da8015b881d8b34af84a341d26ff4`, final head SHA `1cc1d030cda885481e20495014ccfdbd7e8b6c73`).
This PR added real subprocess smoke tests for the raster diagnostics gate report.

Recorded Task 79 result:
* Added real subprocess smoke tests for default human mode, `--json`, `--check`, and `--json --check`.
* Verified PASS-path subprocess execution.
* Verified JSON subprocess output is parseable.
* Did not modify classifier behaviour, thresholds, semantic recognition, ScoreIR, OCR, or vector/raster fusion.
* Known limitation: REVIEW-path subprocess testing was not safely implemented; existing unit tests still cover REVIEW logic with mocks.

## 2. Block on Semantic Promotion, CI Enforcement, and Classifier Hardening
CI enforcement remains blocked until REVIEW-path subprocess behaviour is proven. Raster treble-clef diagnostics remain diagnostic evidence only. Semantic promotion of `treble_clef_candidate` remains explicitly blocked. Furthermore, classifier hardening and threshold tuning are not yet authorised.

## 3. Selected Next Diagnostic-Only Path (Task 81)
Task 79 improved confidence in the gate report CLI by proving real subprocess PASS behaviour. However, the REVIEW subprocess path is still not proven end-to-end. The gate report is close to CI-ready, but enforcing it in CI without a real subprocess REVIEW-path test leaves a blind spot.

**Decision:** We select a new product Task 81 focused on making REVIEW-path subprocess testing safe and deterministic. The task should close the REVIEW-path testability gap before CI integration.

### Task 81 Requirements and Acceptance Criteria:
* Introduce the smallest safe testability seam needed to exercise REVIEW gate status through a real subprocess.
* Prefer a public, test-only input path such as a temporary public case manifest or explicit public fixture selection mechanism.
* Prove `--check` exits 1 for REVIEW via subprocess.
* Prove `--json --check` exits 1 for REVIEW while still emitting parseable JSON.
* Keep default production gate behaviour unchanged.
* Preserve existing PASS-path subprocess tests.
* Avoid private fixture names, private paths, raw diagnostics, screenshots, GP files, generated committed output, or local scratch artifacts.
* Refactoring `scripts/raster_diagnostics_gate_report.py` is allowed only if necessary to support safe test input injection. Any refactor must preserve current default output and current default gate semantics.

### Task 81 Non-Goals / Blocked Actions:
* Do not change raster classifier thresholds.
* Do not improve or tune detection heuristics.
* Do not suppress failures silently.
* Do not add semantic recognition or emit ScoreIR.
* Do not create recognised clef objects.
* Do not add OCR or vector/raster fusion.
* Do not expose private paths, private filenames, screenshots, raw diagnostics, or private content.
* Do not commit generated JSON output, logs, screenshots, PDFs, GP files, or local scratch artifacts.
* Do not modify governance repo files during product implementation.
* Do not add CI enforcement yet.
