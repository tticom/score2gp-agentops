## Current Active Task

## Task 113 — Share whole-note candidate evidence shaping for diagnostics and recognition

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 111 made the whole-note recognition CLI tests source-tree-safe. The installed CLI path and source-tree subprocess test path are now covered without requiring a globally installed `score2gp` executable. Whole-note recognition currently derives read-only recognition outcomes from diagnostic candidate evidence. The next small product step is to reduce duplication and make the whole-note candidate evidence shaping shared and explicit across diagnostics and recognition, without broadening recognition semantics.

Goal:
Extract or consolidate shared whole-note candidate evidence shaping so diagnostics and whole-note recognition consume the same safe, read-only candidate evidence structure. Preserve current CLI/script behaviour, JSON shape unless explicitly justified by tests, privacy-safe source metadata, and existing recognition outcomes.

Next Step:
Execute Product Task 113 in the `score2gp` repository.
