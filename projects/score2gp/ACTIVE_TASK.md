# Active Task

<!-- Generated from ORCHESTRATION_STATE.json; do not edit directly. -->

**Task**: OMIT-02-FU2 — Correct the OMIT-02 design doc: vector repeat dots do occur in the real corpus

**Status**: PROMOTED

**Repository**: tticom/score2gp

**PR Branch**: `feat/omit-02-fu2-design-doc-vector-repeat-dots`

**Pull Request**: TBD

**Owner Role**: implementation

## Objective

Correct the OMIT-02 design doc: vector repeat dots do occur in the real corpus. Source: authority item OMIT-02-FU2. Non-blocking follow-up from tticomgov-code's approving round-2 review 5346382223 of tticom/score2gp#469 (OMIT-02) at d7eef3f. Thread at docs/design/omit-02-double-barlines.md:78 (N2): Gloria.pdf (Guitar Pro 7, macOS Quartz export) draws repeat dots as filled vector drawings with no music font; the reader reads its bars 2, 5 and 8 as repeat-end from two drawing dots each (bar 2 checked visually). The doc calls the vector form unestablished; say it is a real engraving form and cite the count. Documentation only.

## Allowed paths

- `docs/**`

## Validation commands

- `python -m pytest`
- `python -m score2gp.cli export-schema --out schemas`
- `python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json`
- `python scripts/artifact_audit.py`
- `git diff --check`
