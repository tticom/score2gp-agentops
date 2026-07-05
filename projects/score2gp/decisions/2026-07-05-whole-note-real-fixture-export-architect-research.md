# Architect Research — Real-fixture E2E validation of `notation-whole-note-export`

**Date**: 2026-07-05  
**Role**: Architect  
**Outcome**: Outcome B — CLI/export path is partially viable but blocked by specific implementation gaps in the CLI, notation bridge, and `assume_treble_clef` logic.

## 1. Context & Goal
The goal of this research task is to determine whether the existing CLI route `notation-whole-note-export` can run end-to-end on the public synthetic fixture `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf` and produce a structurally correct `.gp` package from the validated whole-note candidates.

## 2. Verification Commands & Results

### Command Attempt 1: Standard CLI Execution
We ran the CLI command using the standard syntax:
```bash
.venv/bin/python -m score2gp.cli notation-whole-note-export --pdf tests/fixtures/pdf/generated_standard_staff_whole_note.pdf --out out.gp
```

**Result**:
```text
NotationBridgeInputError: no_valid_notation_outcomes_found
```
*(Note: Because the CLI failed during the bridge phase, no `.gp` output was generated, and therefore no GP file package structure could be inspected. This confirms that the E2E path is currently blocked prior to file creation.)*

### Analysis of the Failure
To determine the root cause of `no_valid_notation_outcomes_found`, we inspected the outcomes returned by `run_recognition_on_file` using a custom debug script.

We confirmed that `run_recognition_on_file` correctly extracts **two** whole-note candidates with `association_status = "success"`. However, both candidates are annotated with:
```python
'sample_diagnostics': [{'candidate_id': 'whole_note_candidate_001',
                        'skip_reason': 'missing_clef_evidence'},
                       {'candidate_id': 'whole_note_candidate_002',
                        'skip_reason': 'missing_clef_evidence'}]
```

Because the candidates lack a resolved pitch, the notation bridge (`build_ir_from_notation_outcomes`) filters them out. Since all note candidates are filtered out, the bridge raises `NotationBridgeInputError: no_valid_notation_outcomes_found`.

---

## 3. Observed Gaps & Gaps Catalogue

We catalogued the following specific gaps that prevent E2E whole-note GP export:

### Gap 1: Missing Clef Symbols in Synthetic Fixtures
The public synthetic fixture `generated_standard_staff_whole_note.pdf` contains only the staves and notes. It does not draw a treble clef symbol, so `extract_treble_clef_candidate_evidence` correctly returns zero clefs, leaving the staves without any clef context.

### Gap 2: Whole Notes Excluded from `assume_treble_clef`
Even when passing `assume_treble_clef=True` directly into `run_recognition_on_file`, the pitch remains unresolved. This is because `map_assumed_treble_pitch_to_read_only_outcomes` explicitly filters out `whole_note_candidate` and `ledger_line_candidate` (see Code References). Whole notes were never integrated into the fallback treble pitch mapping logic.

### Gap 3: CLI Does Not Expose or Pass `assume_treble_clef`
The `notation-whole-note-export` CLI command does not accept any option to assume a treble clef, nor does it pass `assume_treble_clef=True` when calling `run_recognition_on_file`.

### Gap 4: Test Suite Gaps (Mock-only CLI Tests)
The CLI test suite verifies the CLI by mock-patching the output of `run_recognition_on_file` to include `"clef_resolved_staff_pitch": "B4"`. This mock-patched check hides the E2E integration failures.

---

## 4. Reproducibility & Code References

- **Product Repository**: `tticom/score2gp`
- **Product Commit Inspected**: `05c999ca2010685db7fe7cc12904f818c3d1f05a`
- **Fixture Path**: `tests/fixtures/pdf/generated_standard_staff_whole_note.pdf`

### Code References
1. **CLI Route Implementation**: `src/score2gp/cli.py` (lines 411-453).
2. **Treble Clef Mapping Fallback Exclusion**: `src/score2gp/whole_note_recogniser.py` (lines 974-982).
3. **Mock-patched CLI Test Logic**: `tests/test_cli_notation_whole_note_export.py` (lines 17-58).

### Debug Script for Outcome Inspection
The following script was run locally to verify candidate extraction and pitch mapping:
```python
from pathlib import Path
from score2gp.whole_note_recogniser import run_recognition_on_file

pdf_path = Path("tests/fixtures/pdf/generated_standard_staff_whole_note.pdf")
res = run_recognition_on_file(
    pdf_path,
    include_x_aligned_clusters=True,
    include_left_margin_candidates=True,
    include_ledger_line_candidates=True,
    include_flag_beam_candidates=True,
    assume_treble_clef=True,
)

outcomes = res["read_only_recognition_outcomes"]
print("CLEF RESOLVED PITCH COVERAGE:")
import pprint
pprint.pprint(res["clef_resolved_pitch_coverage"])
```
This produced `skipped_clef_missing: 2` and `note_candidates_with_clef_resolved_staff_pitch: 0`, confirming that `whole_note_candidate` was excluded from pitch mapping.

### Cleanup Confirmation
All local temporary test scripts (e.g. `scratch/print_outcomes.py`, `scratch/test_with_clef.py`, and `scratch/out.gp`) have been deleted. The working tree of the product repository has been verified as clean.

---

## 5. Next Required Loop Step

### Recommended Actions
1. **Update `map_assumed_treble_pitch_to_read_only_outcomes`**: Include `whole_note_candidate` in the fallback treble mapping if no explicit clefs are found.
2. **Update `notation-whole-note-export` CLI**: Accept an optional `--assume-treble-clef` flag and forward it to `run_recognition_on_file`.
3. **Add Integration Tests**: Add a real E2E integration test verifying that `notation-whole-note-export` runs on `generated_standard_staff_whole_note.pdf` and generates a valid GP file when `assume_treble_clef` is active.

### Next Step
Proceed to **Reviewer architecture verification** to approve this corrected research record and authorize the subsequent narrow Developer fix task.
