# Active Task

**Task**: PDFTAB-DUR-06: PDF-Tab Bar Assembler Duration Evidence Integration & Oracle Verification
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer / Pipeline Integrator
**Repository**: tticom/score2gp
**PR Branch**: `agy/pdftab-duration-assembler-integration`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0023-pdf-tab-duration-assembler-integration.md`

## Context

Following the merge of PR #394 (`8830be94a489a9176e80274919eb9941c00db046`), Slice 2 (TabRaw Pipeline Integration) is fully merged in `score2gp`. This task implements Slice 3 (Assembler Integration & Oracle Verification) as defined in Section 7 of `docs/design/pdf-tab-duration-candidate-extraction.md`.

## Goal

Update `assemble_pdf_tab_bar` in `src/score2gp/pdf_tab_bar_assembler.py` and `pdf_tab_measure_timing.py` to inspect `TabCandidate.duration_evidence` on fret event candidates within each chord subgroup.
Assign explicit durations when visual evidence is present; fall back to equal spacing (`select_pdf_tab_grid_spacing_and_duration_name`) when staves are unstemmed.
Implement unit tests in `tests/test_pdf_tab_duration_assembler_integration.py` verifying that `generated_pdf_tab_duration.pdf` extracts quarter, eighth, and sixteenth note durations matching the oracle.

## Allowed Files

- `src/score2gp/pdf_tab_bar_assembler.py` (in `score2gp`)
- `src/score2gp/pdf_tab_measure_timing.py` (in `score2gp`)
- `tests/test_pdf_tab_duration_assembler_integration.py` (in `score2gp`)

## Non-goals

No edits to unrelated parsers, private inputs, reference GP leakage, automatic merge, or branch deletion.

## Acceptance

`pdf_tab_bar_assembler.py` and `pdf_tab_measure_timing.py` are updated in `score2gp` to inspect and assign explicit `TabDurationEvidence`. Unit tests in `tests/test_pdf_tab_duration_assembler_integration.py` pass 100%, demonstrating exact oracle extraction on `generated_pdf_tab_duration.pdf` and preserving unstemmed fallback. `agent_verify.py` passes cleanly, product PR is opened, and handback comment is published.
