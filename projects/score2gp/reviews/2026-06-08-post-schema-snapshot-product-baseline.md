# Post-Schema-Snapshot Product Baseline Review

**Date:** 2026-06-08
**Reviewer:** Antigravity

## Context
This governance review records the exact product baseline state after PR #203 (the schema snapshot gate). This provides a durable reference point before beginning the playability-oriented recognition roadmap.

## Evidence

- **Product Main Commit SHA:** `0b73bd90898bc1f5a1bda6f5e61920d1e952c7f9`
- **Merged PRs Verified:** PRs #197 through #203 are fully merged in the product baseline.
- **Fixture Files Present:**
  - `generated_standard_staff_dense_margin.json`/`.pdf`
  - `generated_standard_staff_sparse.json`/`.pdf`
  - `generated_standard_staff_wide_curves.json`/`.pdf`
  - `generated_standard_staff_complex_cluster.json`/`.pdf`
- **Schema Snapshot Present:** `fixtures/public/pdf_staff_geometry_diagnostics_schema.json`
- **Commands Run:**
  ```bash
  cd /home/tticom/work/score2gp-workspace/score2gp
  git fetch --all --prune
  git switch main
  git pull --ff-only human main
  git status --short
  git log --oneline --decorate --max-count=12
  .venv/bin/python -m pytest tests/test_pdf_standard_staff_diagnostics_fixtures.py
  .venv/bin/python -m pytest tests/test_pdf_staff_geometry_diagnostics.py
  .venv/bin/python -m pytest
  git status --short
  git status --ignored
  find . -path "./.git" -prune -o -type f -size +10M -print
  ```
- **Test Evidence:**
  - `test_pdf_standard_staff_diagnostics_fixtures.py`: 9 passed
  - `test_pdf_staff_geometry_diagnostics.py`: 13 passed
  - Full pytest suite: 549 passed in 10.49s
- **Product Working Tree:** Remained completely clean (`nothing to commit, working tree clean`).
- **Privacy/Artifact Check:** Verified using `find`. No unintended large artifacts, sensitive documents, or un-ignored private files exist in the `.git` tree or working directory. The large files are correctly excluded or represent valid dependencies/fixtures.
- **Known Limitations:** The product currently handles pure geometric staff diagnostics only. No semantic capabilities (e.g. pitch, duration, voice, clef, key signature, rhythm interpretation) are active for standard-staff glyphs.

## Verdict
The product `main` baseline is verified, clean, structurally sound, and test-protected. The strict geometric boundaries laid down by Tasks 1-6 are successfully enforced via the snapshot gate. The repo is ready for Task 8.
