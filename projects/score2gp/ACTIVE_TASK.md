# Active Task

**Task**: Req-122 / Task 56: Implement semantic candidate no-ScoreIR leakage gate
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must implement a strict test proving that the presence of semantic candidates does not alter the legacy ScoreIR output or playable GP package.

## 1. Baseline
- The fail-closed semantic candidate coverage (Req-121) has been implemented, tested, and merged.
- We need to establish a strict boundary test verifying that these candidates do not leak into downstream ScoreIR translation.

## 2. Context
To maintain the safety and isolation boundary, we must guarantee that introducing new notation candidate diagnostics does not affect or corrupt the existing ScoreIR or playable .gp outputs.

## 3. Goal
Verify or implement a dedicated test suite ensuring complete decoupling of candidate diagnostics from ScoreIR translation.

## 4. Non-goals
- Do not make changes to ScoreIR formats.
- Do not translate or map semantic candidates to playable notes or rests.

## 5. Required Output & Outcome
A product PR confirming the isolation gate with a dedicated test suite and PR verification.

## 6. Next Steps
- Promote the next valid task after Req-122 is reviewed and merged.
