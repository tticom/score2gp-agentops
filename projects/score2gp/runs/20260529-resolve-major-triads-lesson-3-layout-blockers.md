# ScoreToGP Run Record - 2026-05-29 (Resolving Major Triads Lesson 3 Layout Blockers)

## Repo and Branch
- **Repository**: `score2gp` and `score2gp-agentops`
- **Branch**:
  - `score2gp`: `agent/pdf-to-gp-smoke-v1/developer`
  - `score2gp-agentops`: `main`

## Command(s) Run
```bash
# E2E Single-PDF Private Smoke Test Command
python scripts/private_e2e_smoke.py --pdf fixtures/private/Lesson-3.pdf --out work/verification/lesson_3_smoke

# Verify entire public test suite
python -m pytest

# Verify schemas and IR
python -m score2gp.cli export-schema --out schemas
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
```

## Input Availability
- **Inputs**:
  - `fixtures/private/Lesson-3.pdf` (born-digital private benchmark input)

## Output Directory Path
- **Outputs Directory**: `work/verification/lesson_3_smoke`

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `fail` (Blocked strictly due to lack of a matching clean GP-exported MusicXML timeline; PDF layout grouping itself is 100% complete and passes the strict safety gate)
- **Remediation / Diagnostic Status**: `pass` (All 391 public tests are green; E2E layout extraction passes strict safety gates with zero unassigned playable fret candidates)
- **Generated File Existence**: `no` (ScoreIR and GP package files pending MusicXML timeline integration)
- **Semantic Round-Trip Status**: `unverified` (Pending MusicXML timeline integration)

## Blocker and Diagnostics
- **Exact Blocker Category**: `provide-matching-musicxml-before-build-ir`
- **Fatal layout grouping blockers resolved**:
  - `pdf_playable_candidate_requires_string_assignment`: Resolved (`0` counts)
  - `pdf_candidates_unassigned_to_string`: Resolved (`0` counts)
  - `pdf_string_assignment_missing`: Resolved (`0` counts)
  - `pdf_playable_candidate_unassigned_to_bar`: Resolved (`0` counts)
  - `pdf_candidates_unassigned_to_bar`: Resolved (`0` counts)
- **Diagnostics encountered**:
  - `pdf_barline_too_short` (21 counts)
  - `pdf_barline_does_not_cross_staff` (20 counts)
  - `pdf_barline_double_secondary` (10 counts)
  - `pdf_barline_outside_staff_region` (20 counts)
  - `pdf_bar_boxes_constructed` (23 counts)
  - `pdf_layout_details` (1 count)
  - `pdf_tuning_standard_detected` (1 count)
  - `pdf_timing_mapping_not_implemented` (1 count)

## Private-Safe Metrics (Lesson-3.pdf)
- **Page Count**: 4
- **Total Candidates**: 505
- **Playable Fret Candidates**: 454
- **Candidates with System**: 454 / 454
- **Candidates with Bar**: 454 / 454
- **Candidates with String**: 454 / 454
- **Unassigned Playable Candidates (No System)**: 0
- **Unassigned Playable Candidates (No Bar)**: 0
- **Unassigned Playable Candidates (No String)**: 0

## Verification Matrix
- `python -m pytest` status: Pass (391/391 passed)
- git diff --check status: Clean
- git status --short status: Checked safely
- git status --branch status: Checked safely

## Private-Safety Audit
- `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep` in `score2gp`: `yes`
- No private copyrighted music, exact fret sequences, or licensing/copyright details have been staged or committed: `yes`
