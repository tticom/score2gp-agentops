# Active Task

**Task**: PDFTAB-DUR-02: Public PDF-Tab Duration Synthetic Fixture Creation
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Developer / Fixture Author
**Repository**: tticom/score2gp
**PR Branch**: `agy/generate-public-pdf-tab-duration-fixture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0019-generate-public-pdf-tab-duration-fixture.md`

## Context

AgentOps PR #386 merged the PDF-tab duration evidence adequacy audit at
`700214c3224478adfe2c5c4a6105875da4fcb279`, returning `PUBLIC_FIXTURE_GAP`.
Existing public PDF-tab test staves lack visual stem/beam/flag duration marks,
so no public fixture provides a duration oracle for PDF-only tab assembly.

## Goal

Create a synthetic PDF-tab duration fixture generator and generated PDF fixture
(`generated_pdf_tab_duration.pdf`) containing multi-bar tablature with drawn stems,
beams, and flags (quarter, eighth, sixteenth notes) and an expected-duration oracle.
Do not modify product code in `src/score2gp/`.

## Allowed Files

- `tests/fixtures/pdf/make_generated_pdf_tab_duration_pdf.py` (in `score2gp`)
- `tests/fixtures/pdf/generated_pdf_tab_duration.pdf` (in `score2gp`)
- `tests/test_pdf_tab_duration_fixture.py` (in `score2gp`)
- `projects/score2gp/runs/2026-07-28-generate-public-pdf-tab-duration-fixture.md` (in `score2gp-agentops`)

Product source code (`src/score2gp/`) remains strictly read-only.

## Non-goals

No product code edits, private inputs, reference GP leakage, automatic merge,
branch deletion, or unauthorized promotion of follow-up implementation.

## Acceptance

The synthetic generator and generated PDF are committed, diagnostic tests verify
that duration candidates are extracted from the fixture staves, pytest and
`agent_verify.py` pass, and a durable run record is published.
