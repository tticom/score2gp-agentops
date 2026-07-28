# Active Task

**Task**: PDFTAB-DUR-03: PDF-Tab Duration Candidate Extraction Architecture
**Status**: APPROVED
**Assigned Identity**: tticom-automation
**Authorised Role**: Architect / Researcher
**Repository**: tticom/score2gp-agentops
**PR Branch**: `agy/pdftab-duration-extraction-architecture`
**Pull Request**: `none`
**Original Prompt**: `projects/score2gp/prompts/next/0020-pdf-tab-duration-candidate-extraction-architecture.md`

## Context

Product PR #391 merged at `1a013cef0f242f1a75428c1ddfa77c251a2b22f0` and AgentOps
PR #388 merged at `af37834cfca753017a557b6926e8ffd28bff997c`, closing the
`PUBLIC_FIXTURE_GAP` by committing synthetic PDF fixture
`generated_pdf_tab_duration.pdf` and generator script.

## Goal

Design the architectural dataflow and spatial association rules for extracting
vertical stem, beam, and flag duration candidates from `NotationStaffDiagnostics`
and integrating them into PDF-only tab bar assembly
(`pdf_tab_bar_assembler.py` / `pdf_tab_measure_timing.py`). Define fallback
boundaries for unstemmed staves and break the work into testable developer
implementation slices. Do not modify product code in `src/score2gp/`.

## Allowed Files

- `projects/score2gp/architectures/2026-07-28-pdf-tab-duration-candidate-extraction-architecture.md` (in `score2gp-agentops`)
- `projects/score2gp/runs/2026-07-28-pdf-tab-duration-candidate-extraction-architecture.md` (in `score2gp-agentops`)

Product source code (`src/score2gp/`) remains strictly read-only during this phase.

## Non-goals

No product code edits, private inputs, reference GP leakage, automatic merge,
branch deletion, or premature implementation work.

## Acceptance

Architecture specification and durable run record are published, stem/beam spatial association rules and dataflow seams are formally defined, fallback boundaries for unstemmed staves are specified, and tests pass.
