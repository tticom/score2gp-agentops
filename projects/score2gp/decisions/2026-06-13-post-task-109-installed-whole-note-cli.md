# Decision: Record Product Task 109 and Authorise Product Task 111 (Shared Candidate Shaping)

## Context
Product Task 109 has been implemented and successfully merged. It exposed the read-only whole-note recognition outcomes through the installed product CLI, closing the gap identified in the previous review phase.

Verified evidence:
- **Product PR URL**: https://github.com/tticom/score2gp/pull/261
- **Title**: `feat(cli): expose whole-note recognition report`
- **Head SHA**: `49dac633ebb333860e17fcf4883d928f69e1ff9e`
- **Merge Commit SHA**: `e52833c67b63067d45ad9f5f50a7fc4693692421`
- **Installed CLI command added**: `score2gp whole-note-recognition`
- **Changed Files**:
  - `src/score2gp/whole_note_recogniser.py`
  - `src/score2gp/cli.py`
  - `scripts/whole_note_recognition_report.py`
  - `tests/test_whole_note_recognition_cli.py`
- **Validation**:
  - Shared recognition report execution logic was safely moved to `src/score2gp/whole_note_recogniser.py`.
  - The script `scripts/whole_note_recognition_report.py` was kept as a backwards-compatible thin wrapper.
  - Installed CLI tests (`tests/test_whole_note_recognition_cli.py`) invoke the Typer subcommand directly, verifying structure and deep nested temporary path sanitisation.
  - Privacy-safe source metadata (`pdf_path.name`) is strictly maintained.
  - All CI tests and diagnostic gate checks passed successfully.
- **Codex Disposition**:
  - Comment: "Tests should not depend on a globally installed executable."
  - Disposition: Accepted as blocker for the next product task. Product PR #261 tests invoke the global `score2gp` executable directly, which is fragile for source-tree test runs.

## Decision
We authorise Product Task 111: Make whole-note recognition CLI tests source-tree-safe.

## Constraints for Product Task 111
- Fix `tests/test_whole_note_recognition_cli.py` so normal repository test runs do not depend on a globally installed `score2gp` executable.
- Prefer `sys.executable -m score2gp.cli` with the right environment or Typer `CliRunner`, after inspecting the existing test style.
- Preserve proof that the installed CLI command is wired.
- Preserve the source-tree script behaviour and privacy-safe source metadata.
- Do NOT change recognition semantics or extraction logic.
- Shared candidate shaping will become Product Task 113.

Next recommended action: after this governance PR is merged, create the Product Task 111 executable prompt in ChatGPT.
