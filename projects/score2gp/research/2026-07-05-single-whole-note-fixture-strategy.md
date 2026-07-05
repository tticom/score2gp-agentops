# Single Whole-Note PDF Fixture Strategy

## Verdict
Outcome B — No ready-made fixture is approved, but a safe generation-script strategy is viable and should be implemented by a later Developer task.

## Baseline
- **Product PR #335**: Merged at commit `a4235ea55c45a513c671f2cc5f24c916bf58f865`
- **Governance PR #235**: Merged at commit `facf5f2a715febe34af3da4718f4ecd24a10e980`
- **Current ACTIVE_TASK state**: `NO_ACTIVE_TASK_APPROVED`
- **Current blocker**: Positive real-fixture validation for `notation-whole-note-export` is unproven because the available public whole-note fixture (`generated_standard_staff_whole_note.pdf`) contains two whole notes. Under the single-note export validation contract, the command cleanly rejects multiple candidates, leaving positive E2E export validation mock-only.

## Research question
What is the safest strategy for obtaining or generating a born-digital vector PDF containing exactly one standard-notation whole-note candidate on a staff for positive E2E validation of `notation-whole-note-export`?

## Options considered

### Option 1: Pinned Mutopia CC-licensed PDF
- **Source/provenance**: Pinned LilyPond PDF on Mutopia (e.g., BWV 772).
- **License**: CC BY-SA 3.0.
- **License evidence**: Mutopia catalog pages list license terms.
- **Attribution obligations**: High (attributions must be retained; license text and authors must be included if files are distributed).
- **Born-digital/vector evidence**: Yes (PDF created by LilyPond).
- **Font stack evidence**: Emmentaler music fonts.
- **Layout complexity**: High. BWV 772 is a full multi-system, multi-measure keyboard piece.
- **Expected whole-note candidate count**: Multiple candidates (5 at the final chord).
- **Proposed validation command**: `notation-whole-note-export` with `--assume-treble-clef` and `--pdf` pointing to BWV 772.
- **Risks**: Exceeds the single-note contract, causing clean rejection. Truncation or multi-bar writing would violate the current narrow implementation scope.
- **Decision**: Reject.

### Option 2: New Custom Public PDF Download
- **Source/provenance**: Standard-notation PDF from an external open-source sheet music repository (e.g., IMSLP).
- **License**: Public Domain or CC-licensed.
- **License evidence**: Webpage metadata.
- **Attribution obligations**: Variable.
- **Born-digital/vector evidence**: Hard to verify programmatically without manual analysis.
- **Font stack evidence**: Unknown/arbitrary fonts.
- **Layout complexity**: Typically high or unpredictable.
- **Expected whole-note candidate count**: Typically multiple or unknown.
- **Proposed validation command**: CLI execution.
- **Risks**: High license/provenance risk. High risk of parsing/layout failures due to complex or unknown fonts.
- **Decision**: Reject.

### Option 3: Programmatic PDF Generation via Product Script
- **Source/provenance**: Generated programmatically using the product repository's existing PDF generator framework `tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py`.
- **License/provenance**: The proposed fixture source would be authored as minimal coordinate data inside the Score2GP product repository. It would not be derived from any external score, composition, scan, PDF, music engraving, or third-party music source. The resulting source fixture and generated output would be governed by the repository’s existing license and project contribution terms. This strategy introduces no third-party score attribution obligations because no third-party score material is used.
- **License evidence**: The later Developer task must keep the fixture source as repository-authored coordinate data and rely only on the repository’s existing license. No external music source, downloaded PDF, public-domain score, Creative Commons score, or third-party engraving is part of this option.
- **Attribution obligations**: No additional third-party attribution obligations are introduced by the fixture source itself, because the strategy uses repository-authored coordinate data rather than external score material.
- **Born-digital/vector evidence**: Yes. Uses PyMuPDF draw primitives (`draw_line` and `draw_oval`) which compile directly to clean vector structures.
- **Font stack evidence**: Vector primitive shapes (does not depend on external font subsets).
- **Layout complexity**: Minimal. Single-system, single-measure, single-note layout.
- **Expected whole-note candidate count**: Exactly one.
- **Proposed validation command**:
  ```bash
  python tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py
  score2gp notation-whole-note-export \
    --pdf tests/fixtures/pdf/generated_standard_staff_single_whole_note.pdf \
    --out out.gp \
    --assume-treble-clef
  ```
- **Risks**: Extremely low. Uses existing verified tooling and requires only the creation of a new minimal JSON config file.
- **Decision**: Accept.

## Recommended strategy
- **Selected option**: Option 3 (Programmatic PDF Generation via Product Script).
- **Why it is safer than alternatives**: It introduces zero external licensing or provenance risk, uses the repository's own verified vector-drawing primitives, maintains a minimal layout footprint, and guarantees exactly one whole-note candidate.
- **Why it produces incremental progress beyond PR #335**: It enables a true positive E2E integration test on a real, born-digital vector PDF instead of patch-mocking the outcomes of `run_recognition_on_file`.
- **Whether Developer integration should be authorised later**: Yes, under Outcome B, a Developer task should be authorised to integrate the new JSON configuration and PDF generator entry, add the real-fixture E2E integration test, and verify the compiled `.gp` file.

## Required validation for later Developer task
1. **JSON Configuration**: Add `generated_standard_staff_single_whole_note.json` to `fixtures/public/` containing exactly one staff, two barlines, and exactly one whole note candidate:
   ```json
   {
     "page_width": 612.0,
     "page_height": 792.0,
     "notation_staves": [
       {
         "y_start": 200.0,
         "line_gap": 8.5,
         "line_count": 5,
         "x0": 50.0,
         "x1": 550.0
       }
     ],
     "barlines": [
       {
         "x": 50.0,
         "y_min": 200.0,
         "y_max": 240.0
       },
       {
         "x": 550.0,
         "y_min": 200.0,
         "y_max": 240.0
       }
     ],
     "whole_notes": [
       {
         "x0": 100.0,
         "y0": 210.0,
         "x1": 115.0,
         "y1": 220.0
       }
     ]
   }
   ```
2. **Build Integration**: Add a call in `main()` of `tests/fixtures/pdf/make_standard_staff_diagnostics_pdfs.py` to compile this file:
   ```python
   build_pdf("generated_standard_staff_single_whole_note.json", "generated_standard_staff_single_whole_note.pdf")
   ```
3. **E2E Integration Test**: Add an integration test `test_notation_whole_note_export_success_real_fixture` in `tests/test_cli_notation_whole_note_export.py` to run the command on the newly generated PDF with `--assume-treble-clef` and assert that the exit status is `0`, a GP package is written, and `inspect_gp` confirms no validation errors.

## Stop conditions for later implementation
- The generated PDF returns more than one candidate or zero candidates.
- The compiled `.gp` file fails GP structural/package validation.
- Any generated `.gp` or PDF files are committed to the git repository.

## Privacy and artifact hygiene
Confirming that no PDFs, GP files, screenshots, generated outputs, private files, logs, dumps, or binaries were committed during this research task.
