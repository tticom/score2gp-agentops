# Completion Record: Quarter-Rest End-to-End PDF-to-GP API Acceptance

## Context
Product PR #321 has been merged into `tticom/score2gp`, providing end-to-end acceptance verification for quarter-rest extraction and GP export via the direct API path.

## Merge Evidence
* PR URL: https://github.com/tticom/score2gp/pull/321
* Final head SHA: `32b4efae23793caf4c587b55a06bcaad68ecee6f`
* Merge commit: `4cf6cbd2b3e63e3d9990e77f2fcc09fe7f94ec90`

## PR Readiness Evidence
- Product PR: `tticom/score2gp#321` (closed / merged)
- Final head SHA: `32b4efae23793caf4c587b55a06bcaad68ecee6f`
- Merge commit: `4cf6cbd2b3e63e3d9990e77f2fcc09fe7f94ec90`
- Reviewer implementation conformance verdict: `approve implementation`
- PR readiness verdict: `READY`
- Merge recommendation: `Authorise supervisor merge`
- Codex/review thread disposition: all PR #321 review threads resolved before merge.
- CI/check disposition: CI and Raster Diagnostics were green before merge.
- Changed file: `tests/test_quarter_rest_e2e_acceptance.py`
- Scope confirmed: test-only product change; no recognition, bridge, timing, or export implementation rewrite.
- Artifact hygiene: generated `.gp` output used pytest `tmp_path / "test_e2e.gp"` and was not committed.
- Limitations preserved:
  - CLI `--pdf-only-tab` still fails with `pdf_only_tab_grouping_unsafe`;
  - Guitar Pro GUI import was not visually validated;
  - tab-only rests remain untested;
  - other rest durations remain untested.

## Exact Capability Proven
A public PDF fixture can now be processed through the direct API path (from extraction to export) preserving a quarter rest in the final `.gp` file without regressing the serialization of adjacent notes.

## Exact Fixture Used
`fixtures/public/generated_simple/simple/QuarterRestThenNotes.pdf`

## Exact Assertions Proven
* The test runs the real PDF recogniser and ScoreIR sequence bridge.
* The first event is sequenced as a quarter rest (`is_rest is True`, `notes == []`, `notated_duration.value == "quarter"`, `duration_ticks == 960`).
* The export utilizes the production relational XML path.
* The exported GPIF asserts:
  * exactly 3 `<Beat>` elements.
  * the first rest `<Beat>` has no beat-level `<Notes>` and no `<Chord>`.
  * rest rhythm resolves to `<NoteValue>Quarter</NoteValue>`.
  * global `<Notes>` database exists and strictly contains exactly 2 note objects (from the two non-rest events).
* `validate_gp(out)["errors"] == []`.
* Generated `.gp` output is safely isolated under pytest `tmp_path` and is not committed.

## Known Limitations Preserved
* CLI `--pdf-only-tab` on this input still fails with `pdf_only_tab_grouping_unsafe`.
* Guitar Pro GUI import was not visually validated.
* Tab-only rests remain untested.
* Other rest durations (eighth, half, whole) remain untested.

## Decision Required
The project requires a Supervisor decision to select the next priority.

Recommended options:
* **Option A**: Authorise a narrow CLI `--pdf-only-tab` investigation for the `pdf_only_tab_grouping_unsafe` gap on `QuarterRestThenNotes.pdf`.
* **Option B**: Authorise a bounded tab-only rest feasibility/diagnostic task.
* **Option C**: Authorise eighth-rest recognition/sequencing/export architecture or diagnostic task.
* **Option D**: Authorise governance milestone review before choosing next symbol.
* **Option E**: Stop/pivot if quarter-rest milestone is sufficient for current project direction.
