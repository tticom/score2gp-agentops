# Post-Merge Audit Report: Product PR #239

## Verdict
**Acceptable**

## Metadata
* **Product PR Number**: #239
* **Merge Commit SHA**: `41eee2f02d68276a19f1ff01e66ea2bc1eb8a55f`
* **Final Head SHA Reviewed**: `dc8b1be57c3b8634f41d60a45ba74732820f4dfa`

## Files Inspected
- `src/score2gp/pdf_raster_staff_diagnostics.py`
- `tests/test_pdf_raster_staff_diagnostics.py`
- `tests/test_pdf_standard_staff_diagnostics_snapshots.py`
- Generated negative fixture PDFs and JSONs (`fixtures/public/...` and `tests/fixtures/pdf/...`)
- Failure taxonomy document (`docs/diagnostics_failure_taxonomy.md`)

## Commands Run
```bash
git checkout main && git fetch origin && git merge origin/main && git status --short
git diff --check
git ls-files | grep -Ei "(scratch|tmp|\.log$|screenshot|output|private_diagnostics|rendered|\.png$|\.jpg$|\.jpeg$|\.pdf$|\.gp$)" || true
find . -path "./.git" -prune -o -path "./.venv" -prune -o -type f -size +10M -print
.venv/bin/pytest tests/test_pdf_raster_staff_diagnostics.py
.venv/bin/pytest tests/test_pdf_standard_staff_diagnostics_snapshots.py
```

## Test Results
* Targeted raster diagnostic tests: **Passed (17/17)**
* Targeted snapshot diagnostic tests: **Passed (1/1)**
* Negative fixtures (TAB, blank, noise) correctly prove diagnostic-only rejection by yielding `staff_count == 0` or a label of `unknown` without triggering any ScoreIR fields.

## Privacy/Artifact Check Results
* `git status --short` and `git diff --check`: Clean local state.
* `git ls-files` check: Clean. No unauthorized tracking of private data or non-fixture outputs.
* Large-file check: Clean. No unauthorized blobs.

## Risk Assessment of `pdf_raster_staff_diagnostics.py` Change
The final change adds a spacing check that suppresses 5-line staff extraction if an immediately adjacent 6th line exists with the same spacing (e.g. part of a 6-line TAB staff).
* **Accidental Suppression Risk:** Very Low. Genuine multi-staff notation systems have large vertical gaps between staves. Because the logic explicitly filters only when the adjacent spacing matches the tight internal staff spacing `abs(prev_spacing - avg_spacing) < avg_spacing * 0.35`, it safely targets contiguous >5-line grids (like TAB) and ignores separate standard notation staves.
* **Semantic Leakage Risk:** Zero. The change is strictly limited to extracting bounding boxes from raster images. It does not introduce semantic features (e.g. notes, rests, ScoreIR properties) or `clef` objects. It is strictly diagnostic.

## Required Separate Reporting

* **Strict Mode Result**: N/A — PR #239 was diagnostic-only and did not run or authorise build-ir, ScoreIR emission, GP package generation, or semantic conversion.
* **Remediation / Diagnostic Result**: Passed. The raster diagnostic and standard snapshot tests passed, negative TAB/blank/noise fixtures were checked, and the code remained strictly diagnostic-only.
* **Semantic Round-Trip Result**: N/A — no semantic round-trip was expected or authorised. The PR did not introduce or emit any pitch, rhythm, key, time, note, voice, or recognized clef objects.
* **Generated-File Existence**: Clean. No ScoreIR or GP package files were generated or committed. The only assets added were the expressly authorised synthetic PDF/JSON diagnostic fixtures merged in product PR #239.

## Recommended Next Step
The PR was safe, met all constraints, and remained diagnostic-only. It did not violate the privacy or semantic boundaries. 
**Recommendation:** Proceed to a new governance Task 66.
