# Active Task

**Task**: Req-120 / Task 52: Implement semantic candidate CLI/reporting smoke path
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must implement command line interface option and diagnostic reporting to expose extracted semantic candidates (logical clefs and quarter rests).

## 1. Baseline
- The semantic candidate JSON snapshots (Req-119) have been implemented, tested, and merged.
- We need to expose these semantic candidates through the CLI to enable maintainer audits.

## 2. Context
Currently, the diagnostics CLI only outputs geometry candidates. Exposing semantic candidates (clef and quarter rests) via CLI or a diagnostic report will allow users to audit and verify extracted semantic features directly.

## 3. Goal
Modify the CLI commands and diagnostic reporting to include semantic candidate outputs (logical clef and quarter rest candidates).

## 4. Non-goals
- Do not infer pitch or durations.
- Do not modify legacy ScoreIR.
- Do not add private fixtures.

## 5. Required Output & Outcome
A product PR exposing semantic candidates via the CLI/reporting, with accompanying tests.

## 6. Next Steps
- Promote the next valid task, likely Req-121, after Req-120 is reviewed and merged.
