# Active Task

**Task**: CR-04B: Explicit Tempo Override for PDF-Only TabRaw Conversion
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer / Pipeline Integrator
**Repository**: tticom/score2gp
**PR Branch**: `agy/cr04b-explicit-pdf-only-tempo-override`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0009-cr04b-explicit-pdf-only-tempo-override.md`

## Context

Following the completion of the CR-04A current-runtime evidence replay (`2026-07-24-cr04a-current-runtime-replay.md`), task CR-04B implements an explicit `--tempo-bpm` CLI override for PDF-only TabRaw conversion, allowing deterministic tempo specification without relying on default 120 BPM.

## Goal

Add an optional `--tempo-bpm FLOAT` parameter to `score2gp convert` for `--pdf-only-tab` and `--editable-draft` paths, passing it to `build_ir_from_tabraw_only()`.

## Allowed Files

- `src/score2gp/cli.py` (in `score2gp`)
- `src/score2gp/build_ir.py` (in `score2gp`)
- `tests/test_pdf_only_tab.py` (in `score2gp`)

## Non-goals

No automatic tempo recognition from PDF text/vectors, no changes to MusicXML import, no schema changes.

## Acceptance

All CLI and builder tests pass cleanly. `agent_verify.py` passes with overall status PASS. Product PR opened and handback published.
