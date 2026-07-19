# FS-02: Canonical Entry-Point Reconciliation - Developer Report

**Date**: 2026-07-19
**Programme**: Runtime-Provenance and Functional-Stabilisation
**Role**: Developer

## Objective
Use FS-01 evidence to answer: which committed function path is actually run by the supported command?

## Findings from FS-01 Evidence
1. **The Supported Command**: The canonical product entry point is the CLI command `score2gp convert` (mapped to `convert_command` in `src/score2gp/cli.py`). The programmatic equivalent used by the smoke harness is `run_private_diagnostic_smoke`.
2. **Function Path Executed**:
   - `inspect_pdf_file()` runs deterministic structural analysis on the vector PDF.
   - `extract_tab_file()` pulls out TabRaw candidates (fret/string pairs).
   - If a `--musicxml` sidecar is present, it imports an external file and runs `align_ascii_musicxml_files()`.
   - `build_ir_with_diagnostics_from_files()` generates the `ScoreIR`.
   - Finally, `write_gp()` generates the Guitar Pro package.
3. **No Uncommitted Auto-OMR Engine**: 
   - There is no uncontrolled local auto-OMR path. All conversions require the external MusicXML file for rests, timing, and pitches unless run in `--pdf-only-tab` mode, which simply uses tab geometry without any rest or timing recognition.
   - The diagnostic tools (`whole_note_recogniser.py`, `notation_bridge.py`) are strictly separated CLI endpoints (`diagnose-single-note`, `test-rest-recognition`, etc.) and are completely bypassed during the product `convert` path.

## Conclusion
The `score2gp convert` entry path is stable and fully committed. It exclusively operates as an aligner of vector tab geometry against external MusicXML sidecars (provided by an external OMR engine), with no implicit "auto-OMR" engine running internally for rhythm or rest inference.

## Next Steps
The product baseline has no uncommitted OMR logic to discard or merge. Proceed to Reviewer phase for FS-02 to endorse these findings, after which we can advance to FS-03/FS-04 to address the first shared source/output divergence within this canonical path.
