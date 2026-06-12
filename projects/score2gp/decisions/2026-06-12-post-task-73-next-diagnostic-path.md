# Decision: Task 74 — Record Task 73 completion and select next diagnostic-only path

**Date:** 2026-06-12
**Status:** Accepted
**Context:** Product PR #243 (Task 73)

## 1. Task 73 Completion and Available Evidence
Product PR #243 (Task 73) has been merged (merge commit `6d45199df44132bc11d3377aadbaf766b245c56b`, final head SHA `f257eb875c8fff327fed858f3d2938004b0b0d93`).
This PR made the raster diagnostics gate report more complete by adding a top-level true-positive count, stdout true-positive summary, and deterministic gate status summary (PASS/REVIEW). 

Observed Task 73 gate report result:
* Total Cases Inspected: 5
* Total Pages Inspected: 15
* Total Staves Detected: 12
* True Positives: 2
* Total False Positives: 0
* Known False Negatives: 0
* Unexpected False Negatives: 0
* Total Unknowns: 1
* Skipped Private Fixtures: 0
* Negative Fixture Outcomes: 3
* Gate Status: PASS

It did not alter classifier logic or thresholds.

## 2. Block on Semantic Promotion and Classifier Hardening
Raster treble-clef diagnostics remain diagnostic evidence only. Semantic promotion of `treble_clef_candidate` remains explicitly blocked. Furthermore, classifier hardening and threshold tuning are not yet authorised.

## 3. Selected Next Diagnostic-Only Path (Task 75)
The gate report now has meaningful totals and a PASS/REVIEW status, but the result is stdout-only. Before any classifier hardening or recognition work, the report should produce structured machine-readable output that CI, reviewers, or governance scripts can consume without scraping human text.

**Decision:** We select a new product Task 75 focused on adding a machine-readable JSON output mode for the raster diagnostics gate report.

### Task 75 Requirements and Acceptance Criteria:
* Add an optional JSON output mode to `scripts/raster_diagnostics_gate_report.py`, for example `--json`.
* Include the same aggregate totals already printed to stdout.
* Include `gate_status`.
* Include safe per-category counts.
* Include safe per-case labels or anonymised case IDs only.
* Preserve the existing human stdout mode by default.
* Avoid writing output files unless explicitly requested by a later task.
* Update tests to verify JSON shape, totals, gate status, and privacy boundaries.

### Task 75 Non-Goals / Blocked Actions:
* Do not change raster classifier thresholds.
* Do not improve detection heuristics.
* Do not suppress failures silently.
* Do not add semantic recognition or emit ScoreIR.
* Do not create recognised clef objects.
* Do not add OCR or vector/raster fusion.
* Do not expose private paths, private filenames, screenshots, raw diagnostics, or private content.
* Do not commit generated JSON output, logs, screenshots, PDFs, GP files, or local scratch artifacts.
* Do not modify governance repo files during product implementation.
