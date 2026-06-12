# Decision: Task 72 — Record Task 71 completion and select next diagnostic-only path

**Date:** 2026-06-12
**Status:** Accepted
**Context:** Product PR #242 (Task 71)

## 1. Task 71 Completion and Available Evidence
Product PR #242 (Task 71) has been merged (merge commit `f645b4e6c8642584e73a62a6fba0e8faaf3b2ae4`, final head SHA `d7cf93000028a64f5121dde7fc00e3e9dc1d65a5`).
This PR improved the raster diagnostics gate report by distinguishing known false negatives, unexpected false negatives, false positives, true negatives / negative fixture outcomes, and skipped optional private fixtures. It did not alter classifier logic or thresholds.

## 2. Block on Semantic Promotion and Classifier Hardening
Raster treble-clef diagnostics remain diagnostic evidence only. Semantic promotion of `treble_clef_candidate` remains explicitly blocked. Furthermore, classifier hardening and threshold tuning are not yet authorised.

## 3. Selected Next Diagnostic-Only Path (Task 73)
PR #242 explicitly notes a limitation: true positive outcomes are classified but not currently aggregated into a top-level totals count. Closing that gap makes the gate report more complete before any classifier hardening is considered. 

**Decision:** We select a new product Task 73 focused on adding a top-level true-positive count and gate status summary to the raster diagnostics gate report.

### Task 73 Requirements and Acceptance Criteria:
- Add a top-level `true_positives` count to the report totals.
- Include true positives in stdout summary.
- Keep existing known/unexpected FN, FP, skipped, unknown, and negative fixture counts.
- Preserve existing classifier behaviour.
- Update tests for true-positive aggregation.
- Avoid adding fixtures unless absolutely necessary.

### Task 73 Non-Goals / Blocked Actions:
- Do not change raster classifier thresholds.
- Do not improve detection heuristics.
- Do not suppress failures silently.
- Do not add semantic recognition or emit ScoreIR.
- Do not create recognised clef objects.
- Do not add OCR or vector/raster fusion.
- Do not expose private paths, private filenames, screenshots, raw diagnostics, or private content.
- Do not modify governance repo files during product implementation.
