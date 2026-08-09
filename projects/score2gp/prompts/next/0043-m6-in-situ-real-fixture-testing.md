# 0043 - M6: In-Situ Real-Fixture Testing Integration & Fallback Cleanup

Status: SKELETON — blocked pending conversion-recovery architecture and the private test contract. This prompt is not executable.

## Objective
Enforce the ban on synthetic mock-point tests by introducing an in-situ test suite running against real-world private fixtures (`Lesson-5.pdf` and `Lesson-6.pdf`). Remove the hacky snapping tolerances and fallback synthesis paths to ensure true note-for-note conversion correctness.

## Start
1. Branch from `origin/main` in the `score2gp` product repository.
2. Confirm the branch name is `feature/agy/m6-in-situ-testing`.
3. Read `projects/score2gp/reports/2026-08-09-master-conversion-failure-diagnosis.md`.

## Implementation Scope & Seam Contract
Modify the gating, snapping, and test modules:
1. **Remove Fallbacks**: Open `src/score2gp/build_ir.py` and delete the `synthesize_missing_tab` logic. Let the pipeline refuse conversion when candidates are missing.
2. **Reset Snapping Tolerance**: Open `src/score2gp/pdf.py` and reset `outer_tolerance` back to `24.0` points (removing the `300.0` hack).
3. **In-Situ Test Suite**: Create `tests/test_real_fixtures_alignment.py`. This test suite must:
   - Load `Lesson-5.pdf` and `Lesson-6.pdf` from the private fixtures repository.
   - Assert that `_detect_tab_systems` returns exactly `38` and `72` measures respectively.
   - Assert that no unassigned playable fret candidates are present in the final `ScoreIR`.
   - Use `pytest.mark.skipif` to gracefully skip the private fixture tests if the private fixtures directory is not present, allowing public unit tests to run in public CI.
4. **Unit/Contract Testing**: Use provenance-linked cases extracted from real fixture PDFs. Do not invent synthetic geometry, IR, or musical events.

## Validation Commands
1. Run the new in-situ test suite:
   ```bash
   PYTHONPATH=. .venv/bin/python3 -m pytest tests/test_real_fixtures_alignment.py
   ```
2. Run the E2E smoke test pipeline:
   ```bash
   PYTHONPATH=. .venv/bin/python3 scripts/private_e2e_smoke.py
   ```

## Deliverables
- Branch `feature/agy/m6-in-situ-testing` pushed to `origin`.
- Target files: `src/score2gp/build_ir.py`, `src/score2gp/pdf.py`, and `tests/test_real_fixtures_alignment.py` modified/created.
- Pull Request opened on GitHub.

## Stop Conditions
- In-situ test paths are hardcoded as relative to the user's home directory instead of using relative repository locations.
