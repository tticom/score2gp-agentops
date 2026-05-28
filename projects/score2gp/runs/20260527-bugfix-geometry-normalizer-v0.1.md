# ScoreToGP Run Record - 2026-05-27 (Geometry-Normalizer Slice & Native GP7 Evaluation Track)

## Repo and Branch
- **Repository**: `score2gp-agentops` and `score2gp`
- **Branch**:
  - `score2gp-agentops`: `main`
  - `score2gp`: `bugfix/pipeline-geometry-normalizer-slice-v0.1`

## Command(s) Run
```bash
# Standalone E2E GP Round-trip Evaluation Command
python scripts/gp_roundtrip_eval.py --pdf fixtures/private/Lesson-3.pdf --gp fixtures/private/Lesson-3.gp --out work/roundtrip_eval_clean_normalizer_v4

# Verify schemas and IR
python -m score2gp.cli export-schema --out schemas
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
```

## Input Availability
- **Inputs**:
  - `fixtures/private/Lesson-3.pdf`
  - `fixtures/private/Lesson-3.gp`

## Output Directory Path
- **Outputs Directory**: `work/roundtrip_eval_clean_normalizer_v4`

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `fail` (Blocked by `missing_pdf_grouping` from other remaining layout issues)
- **Remediation / Diagnostic Status**: `partial` (Edge boundary fallbacks now completely boxed)
- **Generated File Existence**: `no` (ScoreIR and GP files not written)
- **Semantic Round-Trip Status**: `unverified` (E2E timing alignment pending)

## Blocker and Diagnostics
- **Exact Blocker Category**: `missing_pdf_grouping`
- **Fatal edge boundary fallback blocker resolved**:
  - `pdf_bar_box_edge_boundary_fallback_rejected`: Resolved (`0` counts)
- **Diagnostics encountered**:
  - `pdf_bar_box_edge_boundary_fallback_used` (4 counts - fallbacks successfully applied)
  - `pdf_barline_outside_staff_region`
  - `pdf_barline_outside_system_bounds`
  - `pdf_barline_ambiguous`

## Private-Safe Metrics
- Page Count: 4
- Total Candidates: 591
- Playable Fret Candidates: 548
- Candidates with System: 437
- Candidates with Bar: 399 (increased from `380` baseline)
- Candidates with String: 436
- Unassigned-to-System Count: 154
- Unassigned-to-Bar Count: 192
- Unassigned-to-String Count: 155

## Verification Matrix
- `python -m pytest` status: Pass (386/386 passed)
- git diff --check status: Clean

## Private-Safety Audit
- `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep` in `score2gp`: `yes`
- No private score details, pitch steps, lyrics, chord symbols, or raw PDF/MusicXML text are committed: `yes`
