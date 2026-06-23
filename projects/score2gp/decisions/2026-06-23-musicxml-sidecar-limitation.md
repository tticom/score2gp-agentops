# Decision: Standard-Notation and Mixed PDF Conversion Requires MusicXML Sidecar

## Context
Following the end-to-end API verification of quarter-rest PDF-to-GP extraction (PR #321), an architectural review of the CLI `--pdf-only-tab` product route was conducted.

The investigation confirmed that `--pdf-only-tab` is explicitly intended for tablature extraction and requires 6-line tablature systems and playable fret candidates. Standard notation fixtures (such as `QuarterRestThenNotes.pdf`) are correctly rejected by this route with layout gating warnings (e.g., `pdf_no_systems_detected`, `pdf_only_tab_grouping_unsafe`). 

While standard-notation quarter-rest extraction succeeds via the direct API (`run_recognition_on_file` and `build_ir_from_notation_outcomes`), the underlying structural layout inference required to build ScoreIR from full standard notation PDFs (e.g., multi-bar tracking, 5-line staff grouping, system breaks, and polyphony mapping) does not currently exist. 

## Decision
* **MusicXML Sidecar Requirement:** Standard-notation-only and mixed notation+tab PDF conversion strictly require a MusicXML/sidecar for now.
* **No PDF-only Standard Notation Conversion:** No user-facing PDF-only standard-notation `convert` implementation is authorised until standard-notation layout inference architecture (systems, barlines, structural grouping) is defined and built.
* The `--pdf-only-tab` CLI route remains tablature-exclusive. 

## Governance and Product Limitation
This is recorded as an active product and governance limitation. The user-facing CLI `convert` command will continue to explicitly mandate `--musicxml` unless `--pdf-only-tab` is deliberately specified for tablature-only inputs.
