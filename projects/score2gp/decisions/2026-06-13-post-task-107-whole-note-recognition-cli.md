# Decision: Record Product Task 107 and Authorise Product Task 109 (Installed CLI Wiring)

## Context
Product Task 107 has been implemented and merged. It successfully exposed read-only whole-note recognition outcomes through a narrow machine-checkable JSON CLI surface.

Verified evidence:
- **Product PR URL**: https://github.com/tticom/score2gp/pull/260
- **Title**: `feat(recognition): expose read-only whole-note recognition report`
- **Head SHA**: `8f655aa03798fb43eb9e1c1ea6b36e5d126f0995`
- **Merge Commit SHA**: `a4f3c79442f87ff1a5d9467a85ecafec38fa8b42`
- **Changed Files**:
  - `scripts/whole_note_recognition_report.py`
  - `tests/test_whole_note_recognition_report.py`
- **Validation**:
  - A focused test validates that the safe public whole-note fixture yields exactly two candidate outcomes.
  - A regression test ensures the source field is sanitised, preventing raw local or absolute path leaks.
  - CI and advisory checks were green.
- **Codex Disposition**:
  - Comment: “Expose the report through the installed CLI”
  - Disposition: Accepted as blocker for the next product task. Product PR #260 was merged with the known limitation that the report is currently only a source-tree script and not available to installed users.

## Decision
We authorise Product Task 109: Expose the whole-note recognition report through the installed CLI.

## Constraints for Product Task 109
- Choose the smallest safe installed CLI surface (either a new console-script entry point or a subcommand in the existing `score2gp` CLI).
- Preserve `scripts/whole_note_recognition_report.py` unless there is a clear architectural reason to move the logic into `src/score2gp/`.
- Ensure the installed CLI path emits deterministic machine-checkable JSON for whole-note candidates.
- Do NOT broaden the semantic scope: no ScoreIR, no GP output, no pitch/rhythm inference, no OCR, and no staff-position semantics.
- Source metadata must remain privacy-safe.
- Maintain existing tests and ensure the diagnostics gate continues to pass.

Next recommended action: after this governance PR is merged, create the Product Task 109 executable prompt in ChatGPT.
