# Req-125 Blocker Report: Missing Bass/Alto Clef Fixtures

**Date**: 2026-07-09
**Role**: Developer / Architect
**Scope**: Req-125 Multi-clef classification

## 1. Blocker Description

To extend the semantic candidate left-margin classifier to detect and classify Bass and Alto clefs, we must have deterministic validation evidence. However, a complete inventory of the 145 public and private fixtures reveals that:
- **No public/synthetic fixtures** contain bass or alto clefs.
- **No private fixtures** contain bass or alto clefs (all notation staves contain treble clefs or are tab-only).

Without actual PDF primitives (curves, text spans, lines) representing bass and alto clefs on notation staves, we cannot implement or verify Bass/Alto classification heuristics without inventing classifier success on mock data.

---

## 2. Recommended Action: Public Fixture Generation Task

We recommend pausing implementation of Req-125 and creating a new task to generate the smallest public PDF fixtures containing bass and alto clefs:

### Task: Generate Public PDF Fixtures for Bass and Alto Clefs
- **Allowed Repository**: `score2gp`
- **Goal**: Generate synthetic standard staff PDF files containing:
  - At least one system with a Bass clef (F-clef) on a standard 5-line notation staff.
  - At least one system with an Alto clef (C-clef) on a standard 5-line notation staff.
- **Ready Criteria**: LilyPond or equivalent build script infrastructure present in product tests.
- **Done Criteria**: New synthetic PDFs committed under `tests/fixtures/pdf/` and registered in the test suite.

Once these fixtures are present, the classifier can be extended and validated deterministically.
