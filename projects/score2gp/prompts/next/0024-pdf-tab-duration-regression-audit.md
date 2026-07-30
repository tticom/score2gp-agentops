# Developer Task: PDFTAB-DUR-07 (Regression Audit & System Hardening)

Execute Slice 4 of the PDF-Tab Duration Candidate Extraction Architecture defined in `docs/design/pdf-tab-duration-candidate-extraction.md`.

## Preflight

1. Work exclusively as `tticom-automation` in `/home/tticom-automation/work/score2gp-workspace/score2gp`.
2. Verify identity, HOME, GitHub CLI user, Git global user (`tticom-automation`), and canonical workspace path.
3. Read:
   - `docs/design/pdf-tab-duration-candidate-extraction.md`
   - `src/score2gp/pdf_tab_bar_assembler.py`
   - `src/score2gp/pdf_tab_duration_associator.py`
   - `tests/test_pdf_tab_duration_assembler_integration.py`
4. Checkout branch `agy/pdftab-duration-regression-audit` from `origin/main` (`326fc4baa6d339f7eb73d72d4f6caf0379dcf9df`).

## Requirements

1. **Full Corpus Harness & Regression Audit**:
   - Run the complete pytest test suite (`.venv/bin/python -m pytest -q`) across all public fixtures, ensuring 100% pass rate.
   - Verify unstemmed PDF-tab conversion (`generated_tiny_tab.pdf`), standard notation staves, and IR validation continue to pass with zero regressions.

2. **System Hardening & Schema Export**:
   - Export schemas via `.venv/bin/python -m score2gp.cli export-schema --out schemas` and verify zero uncommitted schema diffs exist.
   - Validate IR schemas on `fixtures/public/tiny_score.ir.json`.
   - Run `python scripts/artifact_audit.py` to confirm zero private fixtures or untracked generated artifacts are leaked.

3. **Mandatory Test Cases (`tests/test_pdf_tab_duration_regression_audit.py`)**:
   Create `tests/test_pdf_tab_duration_regression_audit.py` verifying:
   - **Full Fixture Suite Consistency**: End-to-end PDF-to-GP conversion audit verifying duration evidence handling across all synthetic and public tab staves.
   - **No-Leakage & Diagnostic Cleanliness**: Asserting that no private data, temporary debug dumps, or raw arrays leak into outputs or logs.

4. **Validation**:
   Run `.venv/bin/python scripts/agent_verify.py` and ensure overall status is `PASS`.

5. **Publication**:
   Open PR on `tticom/score2gp` and publish exact-head handback comment with `AWAITING_GOVERNANCE_REVIEW`.
