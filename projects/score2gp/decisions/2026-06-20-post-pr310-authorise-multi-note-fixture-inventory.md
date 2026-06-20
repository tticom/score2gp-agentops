# Post PR 310: Record Filled Single-Note Duration Baseline and Authorise Next Task

## Context and Baseline
* Product PR #310 (merged `499abe6`) successfully implemented Developer Outcome A. It validated candidate symbol_types against expected durations and explicitly added export commands for quarter, 8th, 16th, 32nd, and 64th notes using deterministic vector extraction.
* The product baseline now explicitly supports exporting all single-note durations (whole through 64th) from public generated fixtures.

## Completed State
* Single-note duration classification (filled and hollow) is now verified and merged.
* The `ACTIVE_TASK.md` for single-note duration inventory and proof is complete.

## Authorised Next Product Task
The next product task is a bounded public-fixture inventory for the next logical capabilities: multi-note sequences and rests.
It must begin by inspecting `tticom/score2gp` from a clean branch and produce a fixture inventory of the remaining public simple fixtures (e.g. `HalfNotes.pdf`, `WholeNoteRest.pdf`).

The product task must build a fixture inventory table mapped to expected GP outcomes, verifying if multi-note or rest fixtures exist.
It must attempt to export these fixtures using the existing CLI commands, and this task is inspect/proof only. No implementation is authorised.

## Stop Conditions
* Stop and return to Architect research if multi-note or rest recognition fails or requires a new uncertain approach.
* Stop and report a fixture hygiene blocker if new fixtures are not tracked/public.

## Non-Goals
* Do not modify product repo code in this governance task.
* Do not move, add, rename, or delete fixtures.
* Do not create generated `.gp`, `.json`, `.png`, `.pdf`, logs, dumps, screenshots, or private artifacts.
* Do not authorise broad score conversion, tab-only conversion, OCR, model training, or automatic general recognition without Architect diagnosis.
