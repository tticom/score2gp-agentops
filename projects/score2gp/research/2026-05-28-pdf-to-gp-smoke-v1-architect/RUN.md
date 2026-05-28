# Research Record - PDF-to-GP Smoke Integration Architect Plan (v1.0)

## Summary Verdict
We have successfully aligned and saved the TPO-approved acceptance criteria and updated the architecture plan to restrict the scope exclusively to three robust local deterministic layout filters (Collinear Line Merging, TAB-vs-Notation Staff Pre-Classification, and TAB-Grid Intersect Filtering). These plans have been committed and pushed to the `agent/pdf-to-gp-smoke-v1/architect` branch.

## Prompt Chain
- **Prompt Manifest**: [prompt-manifest.json](prompt-manifest.json)
- **Operative Prompt**: [prompts/001-architect-prompt.md](prompts/001-architect-prompt.md)

## Repositories and Branches
- **Repository (Product)**: `score2gp`
- **Product Branch**: `agent/pdf-to-gp-smoke-v1/architect`
- **Repository (Governance)**: `score2gp-agentops`
- **Governance Branch**: `main`

## Commands Run
- `git status`
- `git diff main`
- `git add agent-workflow/`
- `git commit`
- `git push`

## Input Availability
- **Private Benchmark Input**: `fixtures/private/Lesson-3.pdf` (born-digital PDF).
- **Public Fixtures**: `fixtures/public/tiny_score.ir.json`.

## Output Directory Path
- Worktrees in the local system:
  - `score2gp-architect`: `~/work/score2gp-workspace/agent-worktrees/pdf-to-gp-smoke-v1/score2gp-architect`
  - `score2gp-developer`: `~/work/score2gp-workspace/agent-worktrees/pdf-to-gp-smoke-v1/score2gp-developer`
  - `score2gp-reviewer`: `~/work/score2gp-workspace/agent-worktrees/pdf-to-gp-smoke-v1/score2gp-reviewer`
  - `score2gp-tpo`: `~/work/score2gp-workspace/agent-worktrees/pdf-to-gp-smoke-v1/score2gp-tpo`

## Universal Separate Reporting Statuses
- **Strict Conversion Status**: `fail` (before the implementation of the three layout filters)
- **Remediation / Diagnostic Status**: `pass` (all 391 public tests are passing cleanly)
- **Generated File Existence**: `ScoreIR written (no)` / `GP written (no)`
- **Semantic Round-Trip Status**: `unverified`

## Blocker and Diagnostics
- **Exact Blocker Category**: `missing_pdf_grouping` (due to local layout parsing limitations on multi-staff systems like standard notation + TAB).
- **Diagnostic warnings encountered**:
  - `pdf_partial_system_detection`
  - `pdf_string_assignment_missing`
  - `pdf_playable_candidate_requires_string_assignment`
  - `pdf_grouping_confidence_below_threshold`
  - `pdf_missing_pdf_grouping_blocks_build_ir`

## Private-Safe Metrics (Lesson 3 Baseline)
- **Page Count**: 4
- **Total Candidates**: 591
- **Playable Fret Candidates**: 546
- **Candidates with System**: 440
- **Candidates with String**: 440
- **Candidates with Bar Box**: 379
- **Unassigned-to-Bar Count**: 167

## Verification Matrix
- `python -m pytest` status: passed (all 391 public tests pass cleanly)
- Schema validation status: passed (no schema regressions detected)
- git diff --check status: passed cleanly
- git ls-files fixtures/private work status: checked safely

## Private-Safety Audit
- `git ls-files fixtures/private work` outputs exactly:
  `fixtures/private/.gitkeep`
- No copyrighted PDF/GP contents, exact note lists, or private filenames have been committed.

## Summary of Architecture Plan
The initial global page-level grid alignment plan was rejected by the Technical Product Owner (TPO) due to the high risk of fragility and overfitting.
Instead, we formulated and got approval for a robust, local deterministic layout plan under `src/score2gp/pdf.py`:
1. **Horizontal Collinear Line Merging**: Merging collinear/overlapping horizontal segments sharing the same Y-coordinate within a gap tolerance of 10.0 points before line grouping to prevent collinear system splitting.
2. **TAB-vs-Notation Staff Pre-Classification**: Pre-grouping classification to isolate and strictly exclude standard 5-line notation staves from guitar TAB systems.
3. **TAB-Grid Intersect Filtering**: Filtering candidate barlines strictly based on whether they cleanly intersect the Y-extent of the authoritative 6-string TAB staff region to ignore notation note stems and short TAB rhythm stems.

## Next Required Evidence / Developer Handoff
1. **Developer Hand-Off**: Direct the implementation Developer to implement the three local filters in `src/score2gp/pdf.py` as detailed in the approved implementation plan.
2. **Messy Public Fixture**: Direct the Developer to add `tests/fixtures/pdf/generated_paired_notation_tab_system.pdf` and corresponding unit tests to verify the layout engine ignoring 5-line notation staves and rhythm stems in CI.
3. **E2E Private Smoke Verification**: Direct the Developer to run `python scripts/private_e2e_smoke.py` to confirm that all 546 fret candidates assign cleanly with zero unassigned tokens and successfully generate a validated `.gp` file.
4. **Git Safety Check**: Run `git ls-files fixtures/private work` to ensure no private assets have leaked into Git, then commit and push.
