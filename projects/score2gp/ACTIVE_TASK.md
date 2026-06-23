# Active Task: Fixture Hygiene/Review for `chore/adding-tab-only-rest-fixtures`

## Repository
tticom/score2gp

## Goal
Perform a fixture hygiene and review task for the `chore/adding-tab-only-rest-fixtures` branch to verify the newly added PDFs are public-safe, intentionally added, and suitable for a future bounded tab-only rest diagnostic.

## Progress Baseline
* Product PR #321 merged: Quarter-rest direct API PDF-to-GP acceptance is verified end-to-end.
* Architectural Review: CLI `--pdf-only-tab` gap diagnosed as a mode mismatch for standard-notation fixtures.
* Governance Decision: `projects/score2gp/decisions/2026-06-23-musicxml-sidecar-limitation.md` confirms standard-notation-only and mixed notation+tab PDF conversion requires MusicXML/sidecar for now. No user-facing PDF-only notation convert implementation is authorised until standard-notation layout inference is architected.

## Active Blocker
Before tab-only rests can be safely diagnosed or integrated, the incoming fixtures meant to test them must be verified. The current blocker is ensuring the fixtures on the `chore/adding-tab-only-rest-fixtures` branch meet all safety and scope requirements.

## Explicit Scope & Acceptance
* Verify the newly added PDFs in `chore/adding-tab-only-rest-fixtures` are public-safe.
* Verify they are intentionally added and scoped correctly.
* Confirm they are suitable for a future bounded tab-only rest diagnostic.
* Produce a hygiene report or approve the branch if safe.

## Constraints and Preservation
* Do not combine this review with the standard-notation governance PR.
* Do not implement rest recognition logic in this task.
* Do not run diagnostics on the fixtures during this review unless strictly necessary for hygiene verification.
