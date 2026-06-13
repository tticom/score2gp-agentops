## Current Active Task

## Task 109 — Expose whole-note recognition report through the installed CLI

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 107 added a source-tree script `scripts/whole_note_recognition_report.py` that successfully exposes read-only whole-note recognition outcomes. However, it is not available to installed users. The product-facing surface should be available through the installed product CLI to make the feature genuinely accessible without broadening recognition semantics.

Goal:
Wire the read-only recognition report into the installed CLI surface (either a subcommand of the existing `score2gp` CLI or a new console script entry point). It must emit machine-checkable JSON. The safe public fixture must produce exactly two outcomes. Source metadata must remain privacy-safe. Existing diagnostics tests and script tests must continue to pass.

Next Step:
Execute Product Task 109 in the `score2gp` repository.
