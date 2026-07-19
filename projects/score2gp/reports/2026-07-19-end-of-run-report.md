# End of Run Report

**Date**: 2026-07-19
**Programme**: Runtime-Provenance and Functional-Stabilisation

## Completed Tasks
- **FS-01: Runtime Provenance Baseline**: Implemented and verified the `RuntimeProvenanceRecord` and private smoke test harness modifications. The harness now captures all requested evidence parameters, correctly handling `--pdf-only-tab` versus `--musicxml` classifications.
  - **PR Head**: `feature/fs-01-runtime-provenance`
  - **Merged PR**: #376 (merged to `main` at SHA `38c3a67`)
- **FS-02: Canonical Entry-Point Reconciliation**: Analysed the canonical entry point. Confirmed that the canonical pipeline does not contain an uncontrolled local auto-OMR path; it relies purely on an external MusicXML sidecar.

## Validated Facts
- The canonical path relies on `align_ascii_musicxml_files()` linking to external MusicXML representations to build timing and structure in `ScoreIR`.
- `whole_note_recogniser.py` is strictly isolated to specific diagnostic commands (`diagnose-single-note`, etc.) and is NOT invoked by the core conversion pipeline.
- The `private_e2e_smoke.py` cleanly generates `provenance_record.json` locally and keeps artifacts out of Git tracking.

## Unresolved Divergences
- **Missing Sidecars**: The `fixtures/private/` corpus directory contains only `.pdf` inputs and their `.gp` output targets. No `.mxl` or `.musicxml` files are present.
- **Timing Refusal**: As a direct result, any attempt to run the standard product conversion fails safely at the Orchestration Gate with `missing_musicxml`. Because of this, it is impossible to trace any ghost rests, timing defects, or specific divergences for FS-03/FS-04.

## Genuine Stop Condition
The programme arrived at a genuine stop condition. The baseline relies on "timing refusal" because the necessary dependencies are missing. Since we cannot trace the corpus conversions functionally, we cannot authorise the layout refactoring (FS-06/FS-07) required for production.

## Next Smallest Credible Action
**User Intervention / Research Pivot**: Provide the `.mxl`/`.musicxml` sidecars corresponding to the private corpus (`Lesson-3.pdf`, etc.) so that the canonical pipeline can execute, or formally integrate the diagnostic `whole_note_recogniser` into the canonical path so that the dependency on external OMR is removed.
