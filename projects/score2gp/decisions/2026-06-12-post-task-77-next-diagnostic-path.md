# Decision: Task 78 — Record Task 77 completion and select next diagnostic-only path

**Date:** 2026-06-12
**Status:** Accepted
**Context:** Product PR #245 (Task 77)

## 1. Task 77 Completion and Available Evidence
Product PR #245 (Task 77) has been merged (merge commit `686fc846556c65c922f6ad70a10efbb83b0e3455`, final head SHA `7c961bb09e617171d7e9d25aaf7d81b1d5d38fb6`).
This PR made the raster diagnostics gate report usable as a command-line quality gate by adding an explicit `--check` mode.

Recorded Task 77 result:
* `--check` mode was added.
* `--check` exits 0 for PASS and 1 for REVIEW.
* `--json --check` remains parseable and exits according to gate status.
* Human output remains default.
* No classifier behaviour, thresholds, semantic recognition, ScoreIR, OCR, or vector/raster fusion were authorised.

## 2. Block on Semantic Promotion and Classifier Hardening
Raster treble-clef diagnostics remain diagnostic evidence only. Semantic promotion of `treble_clef_candidate` remains explicitly blocked. Furthermore, classifier hardening and threshold tuning are not yet authorised.

## 3. Selected Next Diagnostic-Only Path (Task 79)
Task 77 made the raster diagnostics gate report usable as a command-line quality gate, but the PR report notes a testing limitation: CLI exit behaviour is tested by mocking `sys.exit`, not by executing the script as a real subprocess. Before wiring the gate into CI or using it as an enforced quality gate, we should prove the actual command-line behaviour end-to-end to reduce operational risk without changing classifier behaviour.

**Decision:** We select a new product Task 79 focused on adding subprocess-level CLI smoke tests for the raster diagnostics gate report.

### Task 79 Requirements and Acceptance Criteria:
* Add subprocess-level tests for `scripts/raster_diagnostics_gate_report.py`.
* Prove default human mode exits 0 and emits human-readable output.
* Prove `--json` exits 0 and emits parseable JSON only.
* Prove `--check` exits 0 for PASS.
* Prove `--check` exits 1 for REVIEW.
* Prove `--json --check` emits parseable JSON and returns the expected exit code.
* Avoid relying only on mocked `sys.exit`.
* Preserve existing unit tests if still useful.
* Avoid writing output files.
* Refactoring the script is allowed only if needed to make CLI behaviour testable, but any refactor must preserve existing report semantics.

### Task 79 Non-Goals / Blocked Actions:
* Do not change raster classifier thresholds.
* Do not improve detection heuristics.
* Do not suppress failures silently.
* Do not add semantic recognition or emit ScoreIR.
* Do not create recognised clef objects.
* Do not add OCR or vector/raster fusion.
* Do not expose private paths, private filenames, screenshots, raw diagnostics, or private content.
* Do not commit generated JSON output, logs, screenshots, PDFs, GP files, or local scratch artifacts.
* Do not modify governance repo files during product implementation.
* Do not add CI enforcement yet.
