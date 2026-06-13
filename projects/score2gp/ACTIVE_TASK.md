## Current Active Task

## Task 111 — Extract shared whole-note candidate evidence shaping for diagnostics and recognition

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 109 made the read-only whole-note recognition report available through the installed CLI (`score2gp whole-note-recognition`). The next useful increment is to reduce duplication and drift risk between the diagnostics gate report and recognition path. Both paths consume whole-note candidate evidence, so they should use a shared logic for evidence shaping.

Goal:
Centralise the deterministic candidate evidence shaping where safe, so candidate ordering, ID assignment, page index handling, bounding-box shape, and privacy-safe metadata stay consistent across both surfaces (diagnostics and recognition). Preserve existing deterministic ordering, ID assignments, and test outcomes across all paths without changing extraction thresholds.

Next Step:
Execute Product Task 111 in the `score2gp` repository.
