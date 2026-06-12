# Decision: Task 70 — Record Task 69 completion and select next diagnostic-only path

**Date:** 2026-06-12
**Status:** Accepted
**Context:** Product PR #241 (Task 69)

## 1. Task 69 Completion and Available Evidence
Product PR #241 (Task 69) has been merged (merge commit `836e9e1f54b2f1c53aee1f8529025270cbaa9a32`, final head SHA `403e2fbca3826af575ea38ba92aeff0e7965873b`).
This PR added a machine-readable JSON manifest (`raster_diagnostics_false_negative_manifest.json`) and integrated it with the gate report. It matched known false negatives cryptographically by their SHA256 hashes without leaking any private fixture paths.

## 2. Block on Semantic Promotion and Classifier Hardening
Raster treble-clef diagnostics remain diagnostic evidence only. Semantic promotion of `treble_clef_candidate` remains explicitly blocked. Furthermore, classifier hardening and threshold tuning are not yet authorised. We must ensure the robustness and clarity of our safety gates before optimising the detector itself.

## 3. Selected Next Diagnostic-Only Path (Task 71)
To improve the gate report's utility as a strict safety net, the report must clearly distinguish expected from unexpected failures before any classifier heuristic changes are introduced. 

**Decision:** We select a new product Task 71 focused on making the raster diagnostics gate report explicitly separate known false negatives from unexpected ones.

### Task 71 Requirements and Acceptance Criteria:
- Make the raster diagnostics gate report explicitly separate:
  - known false negatives from the Task 69 manifest
  - unexpected false negatives
  - false positives
  - unknowns
  - skipped optional private fixtures
  - negative fixture outcomes
- Ensure this separation is clearly aggregated in the stdout summary.
- The report must be more useful as a safety gate without changing any classifier behaviour.

### Task 71 Non-Goals / Blocked Actions:
- Do not change raster classifier thresholds.
- Do not improve detection heuristics.
- Do not suppress failures silently.
- Do not add semantic recognition or emit ScoreIR.
- Do not create recognised clef objects.
- Do not add OCR or vector/raster fusion.
- Do not expose private paths, private filenames, screenshots, raw diagnostics, or private content.
