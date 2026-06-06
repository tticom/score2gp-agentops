# Active Plan: PDF-Only Tab-to-GP MVP

This document outlines the active plan to establish a direct PDF-to-GP pathway in `score2gp`, enabling conversion of born-digital PDF tabs directly into Guitar Pro (`.gp`) files without requiring a MusicXML/MXL timing sidecar.

## 1. Product Goal

The core product goal of `score2gp` is to take a born-digital vector PDF guitar tab and produce a playable Guitar Pro (`.gp`) package, without requiring a matching MusicXML/MXL timing sidecar as a mandatory input.

## 2. Current Verified State

- **Extraction**: The visual parser can successfully extract tab coordinates, fret numbers, and string assignments from born-digital PDFs.
- **Diagnostics**: A comprehensive inspection, grouping diagnostics pipeline, and validation framework exist.
- **GP Writing & Validation**: The pipeline can construct structurally valid Guitar Pro files that pass `validate_gp` checks.
- **Evidence (Lesson 3)**: PDF tab extraction on `Lesson 3` successfully recovered:
  - 512 total candidates
  - 461 playable fret candidates
  - 461 fret candidates with system, bar, and string assignment
  - 23 systems
  - 64 bar boxes
  - 0 unassigned string candidates
  - 0 ambiguous string candidates
  - 0 candidates outside staff
  - 51 non-playable text candidates excluded
  - 137 string lines
- **Active Blocker**: The main `convert` command remains blocked at the `musicxml_timing_risk` preflight step because it requires a MusicXML timing sidecar.
- **Dependency Limitations**: Audiveris OMR is not reliable enough to serve as the core bridge for PDF tab timing recovery.
- **Safety Gates**: The current build gates globally refuse the `Lesson 3` layout because of global grouping warnings (e.g. `partial_pdf_grouping`, `pdf_grouping_confidence_below_threshold`, `pdf_grouping_not_safe_for_build_ir`, `pdf_missing_pdf_grouping_blocks_build_ir`, `pdf_timing_mapping_not_implemented`) and the absence of an alternative timing/rhythm generator.

## 3. Current Active Blocker

The active blocker is the absence of a safe PDF-only `ScoreIR` build path that compiles a valid score from recovered tab geometry with deterministic inferred rhythm rather than demanding a source-notation timing sidecar.

## 4. Strategy

- **Optional Sidecars**: Treat MusicXML/MXL as optional high-quality timing evidence. If present, use it for alignment. If absent, fall back to PDF-only mode.
- **New Explicit Mode**: Add a command-line flag or explicit mode (e.g., `--pdf-only-tab` or a dedicated low-level pipeline command) to run direct PDF-to-GP conversion.
- **Playable Draft Construction**: Build a playable draft from tab raw geometry.
- **Timing Provenance**: Explicitly record inside the `ScoreIR` warnings and metadata that timing is layout-inferred, and display clear user diagnostics.
- **Safety Gate Preservation**: Maintain strict safety gates. Refuse if coordinates, string lines, systems, or bar boxes are missing or ambiguous.
- **Post-Generation Comparison**: Only run semantic round-trip comparisons (`compare_gp`) as a downstream evaluation step against a reference GP if supplied, never as an input requirement.

## 5. Planned Milestones

### Milestone A: PDF-only design note
- Design the CLI option shape, core function boundaries, data contracts, rhythm grid policy, refusal warning classification, and corresponding unit/integration test specifications.
- Do not implement any product code.

### Milestone B: Public fixture PDF-only proof
- Run the PDF-only pipeline on a public generated PDF fixture with safe tab geometry.
- Successfully construct a `ScoreIR` from the `TabRaw` model without a MusicXML sidecar.
- Compile a validated `.gp` file.
- Verify the output is cleanly labelled as layout-inferred timing.

### Milestone C: Lesson 3 page 1 private smoke
- Run the PDF-only pathway locally on Page 1 of the private `Lesson 3` PDF.
- The command must either compile a structurally valid `.gp` package or refuse with a specific grouping/rhythm inference failure reason.
- Keep all private assets outside version control.
- Record only sanitized layout counts in agentops run records.

### Milestone D: Lesson 3 full-score private smoke
- Execute the PDF-only pipeline on the entire multi-page `Lesson 3` PDF.
- Confirm the generated GP package passes structural validation checks.
- Inspect the output GP layout.
- Compare metrics against the reference GP as a post-compile quality audit.

### Milestone E: Rhythm improvement
- Upgrade the inferred rhythm policy from a naive even grid to spacing-aware and x-distance-relative grids.
- Ensure the pipeline remains fully sidecar-free.

### Milestone F: Technique/layout expansion
- Add support for expressive techniques (bends, slides, vibratos, etc.) only after the basic note, measure, string, and fret layout compiles correctly.

## 6. MVP Definition

The PDF-only tab-to-GP MVP is achieved when:
- Given a supported born-digital PDF tab with safe tab geometry (systems, string lines, bar boxes, and unambiguous fret assignments),
- the pipeline compiles a validated `.gp` package without requiring a MusicXML timing sidecar,
- the resulting GP file opens and validates structurally,
- frets, strings, and notes are mostly equivalent to the source notation,
- rhythmic durations are deterministic and explicitly labelled as inferred from the layout,
- any layout safety gate failures exit with specific, actionable diagnostic codes.

## 7. Non-MVP

The following capabilities are out-of-scope for the MVP:
- No Optical Character Recognition (OCR) support.
- No scanned/non-vector PDF support.
- No arbitrary handwritten or custom notation layouts.
- No perfect rhythm/tempo reconstruction.
- No complex technique recovery beyond what is already safe.
- No dependency on Audiveris.
- No dependency on private reference GP files as inputs.

## 8. Safety Model

- **Refusal Conditions**: Unsafe or missing geometry (no systems, missing string lines, missing bar boxes) must trigger exit code 4.
- **Ambiguity Gate**: Ambiguous string or bar assignments must refuse compilation unless a bounded provisional mode is explicitly selected.
- **Content Hygiene**: Non-playable text candidates must be explicitly ignored or preserved in metadata, rather than parsed as notes.
- **File Integrity**: Output generation must not be conflated with correctness. Symmetrical matching rates must be validated separately.
- **Privacy Gate**: Private benchmarks (PDFs, oracle GP files) must remain local and must never be committed to either repository.

## 9. Lesson 3 Evidence Note

- **Sanitized Extraction Metrics**:
  - Total candidates: 512
  - Playable fret candidates: 461
  - Candidates with system/bar/string assignment: 461
  - Detected systems: 23
  - Detected bar boxes: 64
- **Failure Cause**: Checked run outputs are blocked globally by the layout safety gate because the system lacks a sidecar-free timing mapping. The blocker codes recorded are: `partial_pdf_grouping`, `pdf_grouping_confidence_below_threshold`, `pdf_grouping_not_safe_for_build_ir`, `pdf_missing_pdf_grouping_blocks_build_ir`, and `pdf_timing_mapping_not_implemented`.
- **Hygiene**: No raw candidate strings, visual overlay files, local folder paths, or raw coordinates are stored in the active plan.

## 10. Open Questions

- What exact confidence threshold should allow the PDF-only MVP pipeline to run?
- Should the MVP allow compilation if all playable fret candidates have valid system/bar/string assignments, even if global layout confidence warnings exist?
- What rhythm grid policy is best for v0.1: fixed eighths, fixed sixteenths, or a layout-density-based grid?
- How should chords be detected from near-identical horizontal x-positions?
- How should the final event in a measure be duration-filled to satisfy time signatures?
- How should inferred timing warnings be represented in ScoreIR provenance models?
- What CLI shape is most user-friendly: extending `convert` via `--pdf-only-tab` or introducing a separate `build-ir-from-tabraw` command?

## 11. Immediate Next Task

The immediate next task is to create a product architecture and design note for PDF-only ScoreIR generation v0.1, followed by a developer prompt.

## 12. Plan Change Policy

This plan is a living document and is expected to evolve. Every change must be driven by new empirical evidence from code executions, design reviews, or pull request feedback. Update the active blocker and next milestones when evidence invalidates a current design assumption.
