## Current Active Task

## Task 107 — Expose read-only whole-note recognition outcomes through a narrow product-facing CLI/report surface

Status: ACTIVE

Owning repo: score2gp

Context:
Product Task 105 has been recorded as complete. It added the first read-only recognition mapping for whole-note candidates. However, this outcome is currently only surfaced through the raster diagnostics gate report. The next visible product improvement is to make this recognition outcome easier to invoke and inspect via a narrow product-facing surface without turning it into ScoreIR, GP, MusicXML, or full notation recognition.

Goal:
Add the smallest safe product-facing surface for read-only recognition outcomes. Consume existing diagnostic whole-note candidate evidence and the Product Task 105 read-only recogniser to provide deterministic read-only recognition output for the safe public whole-note fixture. Keep the output explicitly diagnostic-derived/read-only and machine-checkable JSON.

Next Step:
Execute Product Task 107 in the `score2gp` repository.
