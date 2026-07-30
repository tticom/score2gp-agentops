# Developer Task: PDFTAB-DUR-06 (PDF-Tab Bar Assembler Duration Evidence Integration & Oracle Verification)

Execute Slice 3 of the PDF-Tab Duration Candidate Extraction Architecture defined in `docs/design/pdf-tab-duration-candidate-extraction.md`.

## Preflight

1. Work exclusively as `tticom-automation` in `/home/tticom-automation/work/score2gp-workspace/score2gp`.
2. Verify identity, HOME, GitHub CLI user, Git global user (`tticom-automation`), and canonical workspace path.
3. Read:
   - `docs/design/pdf-tab-duration-candidate-extraction.md`
   - `src/score2gp/pdf_tab_duration_types.py`
   - `src/score2gp/pdf_tab_duration_associator.py`
   - `src/score2gp/tabraw.py`
   - `src/score2gp/pdf_tab_bar_assembler.py`
   - `src/score2gp/pdf_tab_measure_timing.py`
4. Checkout branch `agy/pdftab-duration-assembler-integration` from `origin/main` (`8830be94a489a9176e80274919eb9941c00db046`).

## Requirements

1. **Assembler Duration Evidence Integration (`src/score2gp/pdf_tab_bar_assembler.py` & `pdf_tab_measure_timing.py`)**:
   - Update `assemble_pdf_tab_bar` (and timing helpers in `pdf_tab_measure_timing.py`) to check `candidate.duration_evidence` on fret event candidates within each chord subgroup.
   - When explicit visual duration evidence is attached to event candidates, resolve beat event durations and ticks using `duration_evidence.duration_name` and `duration_evidence.duration_ticks`.
   - Maintain equal-spacing heuristic fallback via `select_pdf_tab_grid_spacing_and_duration_name` when staves are unstemmed or candidates lack visual morphology evidence.

2. **Measure Capacity & Fail-Closed Safety**:
   - Enforce total measure tick capacity constraints via `is_within_pdf_tab_measure_capacity` ($\sum \text{duration\_ticks} \le 3840$).
   - If explicit visual duration evidence causes measure capacity overflow, fail closed with `PdfTabBarAssemblerError`.

3. **Mandatory Test Cases (`tests/test_pdf_tab_duration_assembler_integration.py`)**:
   Create `tests/test_pdf_tab_duration_assembler_integration.py` verifying:
   - **Synthetic Fixture Oracle Extraction**: Running PDF-tab bar assembly on `tests/fixtures/pdf/generated_pdf_tab_duration.pdf` extracts exact expected quarter, eighth, and sixteenth note event durations.
   - **Unstemmed Fallback Preservation**: Verifying unstemmed tab staves (e.g. `generated_tiny_tab.pdf`) fall back cleanly to equal-spacing grid heuristics.
   - **Mixed Measure & Capacity Boundaries**: Verifying measure tick capacity enforcement and mixed stemmed/unstemmed subgroup behavior.

4. **Validation**:
   Run `.venv/bin/python scripts/agent_verify.py` and ensure all unit tests pass cleanly.

5. **Publication**:
   Open PR on `tticom/score2gp` and publish exact-head handback comment with `AWAITING_GOVERNANCE_REVIEW`.
