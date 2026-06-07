# ScoreToGP Run Record - PDF Notation Diagnostics Exception Handling Refactor

## Repo and Branches
- **Repository**: `tticom/score2gp` and `tticom/score2gp-agentops`
- **Product Branch**: `refactor/pdf-staff-notation-diagnostics-exceptions-v0.1` (PR #185)
- **Agent-ops Branch**: `run/2026-06-07-pdf-staff-notation-diagnostics-exceptions-v0.1`
- **Commit Hash**: `35d6b05c7745e69d6bab97bba36d2cbf59dcad5a`
- **Product PR #185**: https://github.com/tticom/score2gp/pull/185

## Relationship to Past PRs
* **PR #183 (Diagnostics Contract)**: Closed unmerged. It was a test-only diagnostics contract PR. Useful privacy, filtering, and schema tests from #183 were carried forward into #185, but the silent-exception assertions were replaced with status assertions.
* **PR #184 (Timing Aligner)**: Already merged into `main`. It resolved the standard staff / TAB staff pair timing alignment mismatch.

## Prompt Chain
- **Prompt Manifest**: [prompt-manifest.json](prompt-manifest.json)
- **Operative Prompt**: [prompts/001-pdf-staff-notation-diagnostics-exceptions.md](prompts/001-pdf-staff-notation-diagnostics-exceptions.md)

## Plan Evidence
- **Implementation Plan**: [implementation_plan.md](implementation_plan.md)
- **Tasks**: [task.md](task.md)
- **Walkthrough**: [walkthrough.md](walkthrough.md)

## Files Changed

### Product Repository (`score2gp`):
* `src/score2gp/pdf.py`
* `src/score2gp/pdf_staff_geometry.py`
* `tests/test_pdf_staff_geometry_diagnostics.py`

### Agent-ops Repository (`score2gp-agentops`):
* `projects/score2gp/runs/2026-06-07-pdf-staff-notation-diagnostics-exceptions-v0.1/` (New run record directory)

## Expected Behaviour
* **Success Path**: When diagnostics extraction succeeds, the inspection JSON includes `status: "success"`.
* **Failure Path**: When either standard staff detection or diagnostics building raises an exception, the inspection output captures a private-safe warning status: `status: "pdf_notation_geometry_diagnostics_failed"` under the `"pdf_staff_notation_diagnostics"` block.
* **Privacy Boundary**: Failure status dumps contain no raw exception text, stack traces, local filesystem paths, private fixture names, raw score/span text, PUA glyphs, or raw coordinate dumps.

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `pass` (Standard PDF inspection status)
- **Remediation / Diagnostic Status**: `pass` (All tests pass cleanly)
- **Generated File Existence**: `yes` (Inspection outputs written and verified in temporary paths)
- **Semantic Round-Trip Status**: `unaffected` (Product code for MusicXML to GP conversion is unchanged)

## Validation Commands Run
```bash
env PYTHONPATH=src .venv/bin/python3 -m pytest tests/test_pdf_staff_geometry_diagnostics.py -v
env PYTHONPATH=src .venv/bin/python3 -m pytest -q
git diff --check
git status
git ls-files fixtures/private work
find . -path "./.git" -prune -o -type f -size +10M -print
```

## Private-Safety Audit
* Checked and verified that only `fixtures/private/.gitkeep` is tracked in the repository. All private PDF inputs and generated coordinate/layout logs are properly ignored.

---

## Known Limitations and Next Recommended Task
* **Known Limitations**: Standard staff diagnostics are collected in the JSON report but are not yet used as timing evidence.
* **Next Recommended Task**: `run/pdf-staff-notation-diagnostics-smoke-refresh-v0.1`
  * **Goal**: Run private-safe smoke inspection on real born-digital PDFs and report only:
    * page counts
    * status counts
    * diagnostic warning/status categories
    * staff counts
    * primitive/font count summaries
    * artifact paths (only if private-safe)
  * **Restrictions**: Do not commit private PDFs, generated GP/GPIF/XML/MXL/MusicXML, raw diagnostics JSON, screenshots, overlays, raw coordinate dumps, local absolute paths, private fixture names, or raw score content.
