# Active Task

**Product Task 161 — Discover and design read-only ledger-line candidate boundary**

## Context
Product Task 160 successfully introduced an opt-in assumed-treble pitch mapping, but it strictly omits pitches for `staff_position_index` values less than 0 or greater than 8.
To support full pitch inference for the assumed-treble boundary, we must next resolve how to map ledger lines. However, our discovery in Task 158 highlighted that ledger-line primitives are not currently passed to the semantic candidate boundary.

## Goal
This is a discovery and design task. Determine how ledger lines exist within the raster diagnostic output, if and how they can be semantically attached to note candidates (as modifiers or independent positional evidence), and propose a design for a `ledger_line_candidate` output boundary.

## Scope
* Inspect `src/score2gp/pdf_raster_staff_diagnostics.py` and clustering primitives to find ledger-line heuristics.
* Determine whether ledger lines should be treated as properties of note candidates or separate generic candidates.
* Explore test fixtures to see if ledger lines appear in unboxed diagnostic dumps.
* Create a detailed design document in the product repository `tticom/score2gp`, under an appropriate documentation or research directory (e.g. `docs/design/` or similar). Do NOT create it in `tticom/score2gp-agentops`.

## Non-goals
* Do NOT implement ledger-line extraction.
* Do NOT update pitch mapping logic.
* Do NOT commit private fixtures, scratch outputs, dumps, logs, credentials, screenshots, GP files, PDFs, images, or unrelated artifacts.
