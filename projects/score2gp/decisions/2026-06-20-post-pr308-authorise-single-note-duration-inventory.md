# Post PR 307 and 308: Authorise Single-Note Duration Inventory

## Context and Baseline
* Product PR #307 (merged `ce77b48`) established an explicit single-half-note notation GP export CLI path. It reported passing tests, but its acceptance evidence used a private fixture (`fixtures/private/simple/1HalfNote.pdf`).
* Product PR #308 (merged `775f1f3`) cleaned up the fixture baseline. It promoted authorised generated/simple fixtures from `fixtures/private/` into `fixtures/public/generated_simple/` and added `.gitignore` protection for `fixtures/private/` and `work/private/`.
* The user has reported adding additional single-note duration fixtures for quarter/q4, 8th, 16th, 32nd, and 64th notes. 

## Unverified State
* The user-reported expanded single-note fixture set is currently unverified. Their exact tracked state, public/private location, filenames, and duration mappings must be verified in the product repository before they can be used as acceptance evidence.

## Active Blocker
The project has explicit single whole-note and single half-note GP export paths, and PR #308 created a safer public generated fixture baseline. The new duration PDFs are not yet verified. The next task must inventory the fixtures, then prove exact capability per duration through the production path, or stop with a precise unsupported-duration report.

## Authorised Next Product Task
The next product task is a bounded public-fixture single-note duration task.
It must begin by inspecting `tticom/score2gp` from a clean branch and produce a fixture inventory.

The product task must build a duration fixture inventory table mapped to GP note values, verifying whole, half, quarter/q4, 8th, 16th, 32nd, and 64th notes if present.
It must prove explicit single-note notation GP export using authorised public generated fixtures, and add support only where the current pipeline already provides sufficient evidence and the change is bounded.

## Stop Conditions
* Stop and return to Architect research if filled-note duration recognition for quarter/eighth/sixteenth/thirty-second/sixty-fourth requires a new uncertain approach.
* Stop and report a fixture hygiene blocker if the new fixtures are not tracked/public.

## Non-Goals
* Do not modify product repo code in this governance task.
* Do not move, add, rename, or delete fixtures.
* Do not create generated `.gp`, `.json`, `.png`, `.pdf`, logs, dumps, screenshots, or private artifacts.
* Do not authorise broad score conversion, tab-only conversion, rest recognition, chords, multi-note sequencing, OCR, model training, or automatic general recognition.
* Do not claim all durations are supported until proven through CLI and GP inspection evidence.
