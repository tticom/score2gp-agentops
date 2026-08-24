# ScoreToGP Run Record - 2026-05-27

## Repo and Branch
- **Repository**: `score2gp-agentops` and `score2gp`
- **Branch**:
  - `score2gp-agentops`: `docs/mandatory-evidence-records-v0.1`
  - `score2gp`: `docs/agentops-result-record-pointer-v0.1`

## Command(s) Run
```bash
# In score2gp-agentops
git status --short
git branch -a

# In score2gp
python scratch/analyze.py
```

## Input Availability
- **Inputs**:
  - `work/major_triads_failure_model_20260527_1608/lesson_3/tab_raw.json` (private-safe basename)
  - `work/major_triads_failure_model_20260527_1608/lesson_3/warnings.json` (private-safe basename)
  - `work/major_triads_failure_model_20260527_1608/lesson_3/pdf-edge-boundary-report.json` (private-safe basename)

## Output Directory Path
- No product outputs generated. Diagnostic files were read from the existing `work/` folder.

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `fail` (Major Triads Lesson 3 blocks compilation under strict mode due to partial layout grouping)
- **Remediation / Diagnostic Status**: `skipped` / `fail` (investigation only, no compilation run)
- **Generated File Existence**: `no` (ScoreIR and GP files not written)
- **Semantic Round-Trip Status**: `unverified` (investigation only)

## Blocker and Diagnostics
- **Exact Blocker Category**: `partial_pdf_grouping`
- **Diagnostic warnings encountered**:
  - `pdf_barline_too_short`
  - `pdf_barline_does_not_cross_staff`
  - `pdf_barline_outside_staff_region`
  - `pdf_bar_box_edge_boundary_fallback_rejected`
  - `pdf_bar_box_edge_boundary_ambiguous`
  - `pdf_barline_ambiguous`

## Private-Safe Metrics
- Page Count: 4
- Total Candidates: 594
- Playable Fret Candidates: 546
- Candidates with System: 440
- Candidates with Bar: 379
- Candidates with String: 440
- Unassigned-to-System Count: 106
- Unassigned-to-Bar Count: 167
- Unassigned-to-String Count: 106

## Verification Matrix
- `python -m pytest` status: Not run (no product code was altered)
- git diff --check status: Clean

## Private-Safety Audit
- `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep` in `score2gp`: `yes`
- No private score details, pitch steps, lyrics, chord symbols, or raw PDF/MusicXML text are committed: `yes`

## Next Required Evidence
- A public synthetic test fixture named `synthetic_dense_unaligned_barlines.pdf` exercising rhythm-stem filtering and grid-based column reconstruction.
