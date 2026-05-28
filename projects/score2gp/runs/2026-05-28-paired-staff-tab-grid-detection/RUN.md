# ScoreToGP Run Record

## Repo and Branch
- **Repository**: score2gp
- **Branch**: bugfix/paired-staff-tab-grid-detection-v0.1

## Prompt Chain
- Prompt manifest: [prompt-manifest.json](prompt-manifest.json)
- Operative prompt: [prompts/001-implementation-prompt.md](prompts/001-implementation-prompt.md)
- Prompt files:
  - [prompts/001-implementation-prompt.md](prompts/001-implementation-prompt.md)

## Command(s) Run
```bash
python -m pytest
python -m score2gp.cli export-schema --out schemas
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
git diff --check
git diff -- schemas
git ls-files fixtures/private work
```

## Input Availability
- **Inputs**: `fixtures/private/Lesson-3.pdf`

## Output Directory Path
- **Output**: `work/paired_staff_tab_grid_detection_20260528_084944/lesson_3`

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `fail` (strict conversion still fails)
- **Remediation / Diagnostic Status**: `pass`
- **Generated File Existence**: `ScoreIR written (no)` / `GP written (no)` (ScoreIR/GP still not written)
- **Semantic Round-Trip Status**: `unverified`

## Implementation Status Summary
- **Strict Conversion**: Still fails.
- **ScoreIR/GP Writing**: Still not written.
- **Private Lesson 3 Smoke Test**: Did not yet demonstrate OMR conversion progress.
- **PR Purpose**: This PR serves strictly as public fixture and guardrail infrastructure for the next OMR layout change.

## Blocker and Diagnostics
- **Exact Blocker Category**: `missing_pdf_grouping` (as expected, global gates are intentionally kept strict)
- **Diagnostic warnings encountered**:
  - `pdf_grouping_confidence_below_threshold`
  - `pdf_grouping_not_safe_for_build_ir`
  - `pdf_layout_detection_requires_manual_review`
  - `pdf_missing_pdf_grouping_blocks_build_ir`
  - `pdf_partial_grouping_with_playable_candidates`
  - `pdf_partial_system_detection`
  - `pdf_playable_candidate_requires_string_assignment`
  - `pdf_string_assignment_compact_staff_ambiguous`
  - `pdf_string_assignment_confidence_below_threshold`
  - `pdf_string_assignment_missing`
  - `pdf_string_assignment_not_enough_for_build_ir`
  - `missing_pdf_grouping`

## Private-Safe Metrics
- Page Count: 1
- Total Candidates: 591
- Playable Fret Candidates: 548
- Candidates with System: 431
- Candidates with Bar: 399
- Candidates with String: 430
- Unassigned-to-System Count: 160
- Unassigned-to-Bar Count: 192
- Unassigned-to-String Count: 161

## Verification Matrix
- `python -m pytest` status: passed (all 132 tests, including new public synthetic fixture tests, pass)
- Schema validation status: passed (schemas matches git index cleanly)
- git diff --check status: passed cleanly

## Private-Safety Audit
- `git ls-files fixtures/private work` outputs only `fixtures/private/.gitkeep`: `yes`
- No private score details, pitch steps, lyrics, chord symbols, or raw PDF/MusicXML text are committed: `yes`

## Next Required Evidence
- Verify that draft PRs are successfully opened and reviewed. The next step is to address subsequent layout refinement tasks once this PR has been merged.
