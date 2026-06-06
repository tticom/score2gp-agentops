# Release Hardening and Sidecar Acquisition Workflow Definition v0.1

This document defines the release-hardening contract for the current `score2gp` milestone and specifies the sidecar/input acquisition workflow needed for future unsupported or missing-sidecar inputs.

## Verdict
`release hardening contract and sidecar acquisition workflow defined; no implementation gaps found`

---

## Current release contract

The current release contract enforces strict gating at each stage of the conversion pipeline to prevent the generation of invalid or malformed Guitar Pro (`.gp`) packages.

### Supported input classes
1. **Born-Digital Vector PDF + MusicXML/MXL**: A born-digital PDF containing vector drawing primitives for a six-line tab staff with visible barlines, paired with a matching MusicXML sidecar (or compressed `.mxl` package) representing standard notation and timing.
2. **Born-Digital Text PDF with ASCII Tab + MusicXML/MXL**: A text-based PDF containing structured blocks of six ASCII rows, paired with a matching MusicXML sidecar and a pre-generated column-to-onset alignment map.
3. **Hand-Authored ScoreIR**: Valid JSON files conforming to the strict `ScoreIR` Pydantic models.

### Required PDF properties
* **Format**: Must be born-digital (contains vector line geometries and selectable text; scanned or raster images are rejected).
* **Geometry**: Must feature exactly six near-horizontal lines representing the tab staff.
* **Measure Segmentation**: Must contain vertical vector paths representing barlines that cross all six lines of the tab staff to define bounding boxes for each measure.
* **Fret Candidates**: Playable digits (representing fret numbers) must be horizontally positioned within measure boundaries and vertically centered/snapped close to one of the six staff lines.

### Required MusicXML sidecar properties
* **Format**: Well-formed compressed `.mxl` packages or plain `.musicxml`/`.xml` files.
* **Timing Consistency**: Clean voice timelines per measure with no duration overlaps, no overfull/underfull measures, and consistent end-ticks across all active voices.
* **Cursor Movements**: Standard `<backup>` and `<forward>` tags with a maximum of 3 cursor movements per measure to prevent cursor drift.
* **Chord Stacks**: Distinctly classified vertical note stacks utilizing the `<chord/>` tag to distinguish them from timing overlaps.
* **Voice Polyphony**: Free of unsupported cross-voice polyphony (different voices playing overlapping notes in the same track).

### Unsupported input classes
* **Scanned/Raster PDFs**: PDFs containing scanned images or pixels instead of vector shapes. These are rejected as `pdf_no_systems_detected` or `pdf_tab_staff_missing`.
* **ASCII Tab without Sidecar**: Text-based ASCII tabs without matching MusicXML sidecars (rejected as `ascii_tab_timing_unavailable`).
* **Vector TAB-only without Sidecar**: Drawn vector tabs without standard notation timing sidecars (cannot be aligned automatically).
* **Unstructured or Complex Notation**: Inputs with complex overlapping voices or high timing risk (rejected as `musicxml_scoreir_polyphony_gate_refused` or `invalid_timing_refused`).

### Expected refusal codes
* **`missing_pdf_grouping`**: Playable fret candidates exist but system/string/bar grouping is absent.
* **`missing_musicxml`**: MusicXML sidecar is absent for drawn tab.
* **`missing_ascii_alignment_sidecar`**: ASCII tab lacks a corresponding alignment file.
* **`invalid_timing_refused`**: Broken MusicXML timeline (e.g. voice duration overfull).
* **`unsupported_polyphony_refused`**: Valid multi-voice polyphony that cannot be represented in ScoreIR.
* **`ascii_alignment_status_unavailable`** / **`ascii_alignment_status_partial`**: Fails when ASCII/MusicXML alignment status is not `compatible`.

### Expected output artifacts
* **`extracted.tabraw.json`**: Extracted text candidates with stable IDs, bounding boxes, and coordinates.
* **`score.ir.json`**: Intermediate ScoreIR JSON output (if successful).
* **`diagnostics.json`**: Quality audit and alignment match summary.
* **`smoke.gp`**: Serialized Guitar Pro 7 package (if successful).
* **`grouping-diagnostics.html`**: Visual PDF system-line and bar box grouping report.
* **`symbol-attachment-diagnostics.html`**: Visual text symbol and technique attachment report.
* **`musicxml-timing-diagnostics.html`**: Visual table of voice cursor timeline issues.

### Validation commands
* **`PYTHONPATH=. .venv/bin/python3 -m pytest`**: Runs the entire public test suite.
* **`python -m score2gp.cli validate <gp-file>`**: Validates GP package zip structure and GPIF XML well-formedness.
* **`PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py`**: Verifies post-serialization quality gates.

### Private-safety contract
* **Safety Invariant**: Running `git ls-files fixtures/private work` must output exactly `fixtures/private/.gitkeep`.
* All raw score fixtures, private PDFs, MusicXML files, and generated runs in `work/` are excluded from git.
* Anonymized summaries (`private_e2e_summary.json` / `.md`) use redacted labels (`private_input_1`, `private_input_custom_lesson_3`) and omit artist/song details.

---

## Required sidecar workflow

For future score inputs that are unsupported or missing sidecars, developers must follow a standard sidecar acquisition workflow.

### MusicXML sidecar requirements
* **Structure**: The MusicXML sidecar must represent the exact layout structure, bar count, and rhythmic division of the PDF score.
* **Monophonic / Simple Homophonic Track**: Multi-voice polyphony should be simplified in standard notation to keep active voice timelines non-overlapping.
* **Chord Stack Anchors**: All vertical chords must be written as valid XML chord blocks (using `<chord/>` tags linked to a single preceding anchor note).

### Naming/location convention
* For private local development:
  * Place the PDF in `fixtures/private/<Song Name>.pdf`.
  * Place the sidecar in `fixtures/private/<Song Name>.<ext>` (where `<ext>` is `.mxl`, `.musicxml`, or `.xml`).
* The system automatically scans for matching base names and pairs them during `scripts/private_e2e_smoke.py`.
* In CLI workflows, paths are explicitly referenced via `--musicxml`.

### Validation checks before build-ir
The build-ir pipeline automatically parses the MusicXML sidecar and runs voice cursor checks before initiating candidate matching. It validates:
* **Grid partition**: Beats correctly partition into divisions.
* **Voice timelines**: Sum of ticks per voice matches the measure duration.
* **Overlap safety**: No overlapping active durations in a single voice.
* **Polyphony gate**: No cross-voice overlaps.
* **Backup/Forward risk**: Maximum of 3 backup/forward tags per bar.

### Alignment sidecar requirements for ASCII tab
To process ASCII tabs:
1. Run `align-ascii-musicxml` to generate `ascii_musicxml_alignment.json`.
2. Verify that the alignment status is `compatible`.
3. Feed the resulting alignment JSON into the `build-ir` tool via the `--ascii-alignment` argument.

### What is explicitly out of scope
* **OCR/OMR of images**: The project does not convert scanned/raster PDFs or raw images into vector representation.
* **Automatic timing synthesis**: Timing cannot be guessed from spacing alone; a MusicXML sidecar is always required.
* **GPIF layout design**: Creating print-ready styles or complex track layouts in GP packages is out of scope.

---

## Release checklist

The minimum verification checklist before executing a milestone release of `score2gp`:

- [ ] **Sync**: Ensure the product `main` branch is clean and up to date (`git pull --ff-only`).
- [ ] **Unit and Integration Tests**: Run `python -m pytest` and confirm all 467 tests pass.
- [ ] **Private Smoke Pass**: Run `python scripts/private_e2e_smoke.py` and confirm it executes without crashing.
- [ ] **Quality Audit**: Run `python scripts/private_gp_quality_audit.py` and verify:
  - `private_input_1`, `private_input_custom_lesson_3` to `7`, and `private_input_custom_melodic_soloing` pass.
  - Unsupported files output expected failures (`gp_output_empty_or_near_empty`).
- [ ] **Private-Safety Invariant**: Run `git ls-files fixtures/private work` and verify that the output is exactly:
  ```text
  fixtures/private/.gitkeep
  ```
- [ ] **Whitespace Check**: Run `git diff --check` and confirm no whitespace errors exist.
- [ ] **Report Verification**: Confirm the generation of:
  * `work/private_e2e_smoke_v0_1/private_e2e_summary.json`
  * `work/private_e2e_smoke_v0_1/private_e2e_summary.md`
  * `work/private_gp_quality_audit_v0_1/summary.json`
  * `work/private_gp_quality_audit_v0_1/summary.md`
- [ ] **Privacy Check**: Confirm no private filenames, artist names, or lyrics are exposed in public commit logs or documentation.

---

## Documentation gaps

The current repository is missing dedicated files for the following release and input requirements:

1. **`docs/release-contract.md`**: To formalize the input classes, supported features, and refusal behaviors.
2. **`docs/input-requirements.md`**: To document geometry constraints of PDF vector lines, text properties, and the need for digital source material.
3. **`docs/sidecar-workflow.md`**: To document the generation, validation, naming, and alignment of sidecar files.
4. **`TESTING.md`**: To detail how to run public tests and how to trigger the private smoke/quality audits.
5. **`PRIVACY.md`**: To formalize the private-safety invariant, local-only directory conventions, and prevent private data leaks.

---

## Recommended smallest next task

The recommended next task is a **documentation-only/release-contract PR** to add the missing documentation files to the product repository (`score2gp`):
* Create [docs/release-contract.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/release-contract.md)
* Create [docs/input-requirements.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/input-requirements.md)
* Create [docs/sidecar-workflow.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/docs/sidecar-workflow.md)
* Create [TESTING.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/TESTING.md)
* Create [PRIVACY.md](file:///wsl.localhost/Ubuntu-24.04/home/tticom/work/score2gp-workspace/score2gp/PRIVACY.md)

---

## Commands run
1. `git switch main`
2. `git pull --ff-only origin main`
3. `git status --short --branch`
4. `git log --oneline --decorate --max-count=40`
5. `PYTHONPATH=. .venv/bin/python3 -m pytest`
6. `PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py`
7. `PYTHONPATH=. .venv/bin/python3 scripts/private_gp_quality_audit.py`
8. `git ls-files fixtures/private work`
9. `git diff --check`

## Test results
* **Public Tests**: 467 passed.
* **Private Smoke Summary**:
  * 12 private files processed.
  * Successfully wrote `work/private_e2e_smoke_v0_1/private_e2e_summary.json` and `private_e2e_summary.md`.
* **Private Quality Audit Summary**:
  * `private_input_1`: pass (153/153 matched)
  * `private_input_custom_lesson_3`: pass (459/459 matched)
  * `private_input_custom_lesson_4`: pass (546/546 matched)
  * `private_input_custom_lesson_5`: pass (295/295 matched)
  * `private_input_custom_lesson_6`: pass (235/235 matched)
  * `private_input_custom_lesson_7`: pass (624/624 matched)
  * `private_input_custom_melodic_soloing`: pass (82/82 matched)
  * Unsupported/missing-sidecar custom files cleanly marked as `fail` (expected).

## Private-safety result
`git ls-files fixtures/private work` outputs exactly `fixtures/private/.gitkeep`. The safety gate is intact and verified.

## Known limitations
* **Scanned/raster PDFs**: Unsupported (lack vector line path data and text selectable layer).
* **ASCII tab timing**: Characters do not imply timing; cannot convert without a manual sidecar mapping file (`ascii_musicxml_alignment.json`).
* **Complex polyphony**: Cross-voice overlapping notes are rejected.
* **Technique preservation**: Full technique transcription is still restricted; GPIF layout templates are minimal.
