# NPG-00A: Baseline and Dependency Inventory

**Date:** 2026-08-20
**Role:** Architect (tticom-codex)
**Status:** Clean

## Exact Revisions (Runtime Provenance)
- **Product (`tticom/score2gp`)**: `9a59c563712c714b4458722cd32a9c4f8794dd37` (origin/main)
- **Governance (`tticom/score2gp-agentops`)**: `fd4a01ca1f8371905636499e487ffb984ead4a76` (origin/main)
- **Skills (`skills-lock.json` v1)**:
  - `orchestration`: `b5c364878fb07d21a369f091f2e96b823da94308b15b39636f2585d8b5621b51`
  - `orca-cli`: `cca6a9098e0dff08ce6fef999da77d98e94255e826b8b9f8132749b5da66dad2`
  - `computer-use`: `afe48be623c1f6190ade7dacc4c1d334d4150b503ed00b28dda23a499e5bdc30`

## Executable Inventory & Call Graphs

### Native PDF-to-GP (Vector Routes)
- **Command Entry**: `python3 -m score2gp.cli extract-tab <pdf_path>`
- **Call Graph**:
  1. `score2gp.cli.extract_tab_command` -> `score2gp.pdf.extract_tab`
  2. `score2gp.pdf.extract_tab` -> `score2gp.pdf_geometry.inspect_pdf` (via `pymupdf`)
  3. `score2gp.pdf_geometry_candidate_extraction` extracts vector primitives.
  4. `score2gp.pdf_tab_bar_assembler` assembles `TabCandidate`s.
- **Dependencies**: `pymupdf>=1.23`

### Audiveris OMR (Legacy Routes)
- **Command Entry**: `python3 -m score2gp.cli note-candidate-recognition --pdf <pdf_path>`
- **Command Entry**: `python3 -m score2gp.cli generate-sidecar --pdf <pdf_path>`
- **Call Graph**:
  1. `score2gp.cli` -> `score2gp.notation_omr.musicxml_generator.generate_musicxml_from_omr`
  2. Subprocess execution to external `Audiveris v5.3` (Java runtime).
- **Dependencies**: `Java JRE`, `Audiveris v5.3` (external binary).

### MusicXML to GPIF Conversion
- **Command Entry**: `python3 -m score2gp.cli convert --pdf <pdf_path> --musicxml <xml_path>`
- **Call Graph**:
  1. `score2gp.build_ir.build_ir` reads standard elements.
  2. `score2gp.gpif_builder.GpifBuilder` transforms IR to `score.gpif`.
  3. `score2gp.gp_package.write_gp` zips outputs to `.gp`.

## Packages and Dependencies
- **Core Runtime (`pyproject.toml`)**: `pydantic>=2.6`, `typer>=0.12`, `pymupdf>=1.23`
- **Dev/Test**: `pytest>=8.0`, `pillow>=10.0`, `opencv-python>=4.9`

## CI Pipeline Inventory
- `.github/workflows/ci.yml`: "CI" (Checks out private corpus, runs unit and real-source tests, hygiene audit)
- `.github/workflows/diagnostics_advisory.yml`: "Raster Diagnostics Gate Advisory" (Runs gate report tests in human, JSON, and check modes)

## Separation of Historical References
- The directory `../score2gp-private-fixtures/fixtures/private/` contains `Lesson-5.pdf`, `Lesson-5.gp`, and synthetic stubs (e.g., `generated_pdf_fret_grouped_success.pdf`).
- These are strictly separated from executable runtime code. They serve as regression test vectors in `.github/workflows/ci.yml` but are not shipped dependencies of `score2gp`.
- Executable Java routes for Audiveris operate only during `generate-sidecar` and are isolated from the native PDF vector pipelines.

## Validation Conclusion
The baseline is completely clean on current `main`. No private artifacts have been copied or committed. No product behavior has been changed. Runtime provenance is exact and recorded above.
