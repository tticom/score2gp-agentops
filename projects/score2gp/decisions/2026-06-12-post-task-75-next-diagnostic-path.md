# Decision: Task 76 — Record Task 75 completion and select next diagnostic-only path

**Date:** 2026-06-12
**Status:** Accepted
**Context:** Product PR #244 (Task 75)

## 1. Task 75 Completion and Available Evidence
Product PR #244 (Task 75) has been merged (merge commit `8d1983a0cbbea01a3b81d4a7aa2e7110602a1106`, final head SHA `01246dbf486b0d868ef5af8de8b26f058e1a4343`).
This PR successfully added an optional `--json` output mode to the raster diagnostics gate report, maintaining the default human stdout mode. The JSON emitted was proven to correctly encapsulate `schema_version`, `gate_status`, `totals`, `categories`, and `cases`. No private filenames or generated JSON files were committed.

Recorded Task 75 result (Human and JSON):
* Total Cases Inspected: 5
* True Positives: 2
* Negative Fixture Outcomes: 3
* False Positives: 0
* Unexpected False Negatives: 0
* Gate Status: PASS

## 2. Block on Semantic Promotion and Classifier Hardening
Raster treble-clef diagnostics remain diagnostic evidence only. Semantic promotion of `treble_clef_candidate` remains explicitly blocked. Furthermore, classifier hardening and threshold tuning are not yet authorised.

## 3. Selected Next Diagnostic-Only Path (Task 77)
The report now has a deterministic `gate_status` in both human and JSON output, but it likely still exits successfully regardless of `PASS` or `REVIEW`. Before any classifier hardening, the gate should be usable by CI as a read-only quality gate via its exit code.

**Decision:** We select a new product Task 77 focused on adding an explicit command-line gate check mode (`--check`) to the raster diagnostics gate report.

### Task 77 Requirements and Acceptance Criteria:
* Add an optional `--check` mode to `scripts/raster_diagnostics_gate_report.py`.
* Keep default human stdout behavior unchanged.
* Keep `--json` behavior unchanged except for compatible combination with `--check` if implemented.
* Exit with status code `0` when `gate_status == "PASS"`.
* Exit with non-zero status code, preferably `1`, when `gate_status == "REVIEW"`.
* Do not write output files.
* Update tests for PASS and REVIEW exit behavior.
* Keep JSON output parseable if `--json --check` is supported.

### Task 77 Non-Goals / Blocked Actions:
* Do not change raster classifier thresholds.
* Do not improve detection heuristics.
* Do not suppress failures silently.
* Do not add semantic recognition or emit ScoreIR.
* Do not create recognised clef objects.
* Do not add OCR or vector/raster fusion.
* Do not expose private paths, private filenames, screenshots, raw diagnostics, or private content.
* Do not commit generated JSON output, logs, screenshots, PDFs, GP files, or local scratch artifacts.
* Do not modify governance repo files during product implementation.
