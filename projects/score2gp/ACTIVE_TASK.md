## Current Active Task

## Task 111 — Make whole-note recognition CLI tests source-tree-safe

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 109 made the read-only whole-note recognition report available through the installed CLI (`score2gp whole-note-recognition`). However, testing this via `subprocess.run(["score2gp", ...])` causes tests to depend on a globally installed executable, which is fragile for source-tree test runs.

Goal:
Fix `tests/test_whole_note_recognition_cli.py` so normal repository test runs do not depend on a globally installed `score2gp` executable. Prefer `sys.executable -m score2gp.cli` with the right environment or Typer `CliRunner`, after inspecting the existing test style. Preserve proof that the installed CLI command is wired, preserve the source-tree script behaviour, and preserve privacy-safe source metadata. Do not change recognition semantics or extraction logic.

Next Step:
Execute Product Task 111 in the `score2gp` repository.
