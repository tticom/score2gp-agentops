# CR-04D4 Promotion

## Trigger

Product PR #388 was externally merged on 2026-07-26.

## Verified Product State

- Product repository: `tticom/score2gp`
- Product merge commit:
  `cea235d83e72e608b841e5d6d55b631077fa1833`
- Merged D1 duration-policy module:
  `src/score2gp/pdf_tab_measure_timing.py`
- Merged D2 event factory:
  `src/score2gp/pdf_tab_event_factory.py`
- Merged D3 bar assembler:
  `src/score2gp/pdf_tab_bar_assembler.py`
- The focused D3 test file contains repeated candidate/bbox setup and complete
  literal normalized-`Bar` oracles.

## Revalidation Decision

Prompt 0015 remains viable after D3. Repeated input construction can move to a
small test-only helper without changing production behavior. The full literal
normalized-`Bar` expectations must remain fixed because they are independent
characterization oracles, not setup duplication.

The task is limited to the approved test files and one new test helper.
Production modules, recognition, timing, grouping, schemas, CLI behavior,
diagnostics, refusals, ScoreIR, GPIF, and writers are frozen.

## Authorisation

This governance change promotes only CR-04D4 through:

- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/prompts/NEXT.md`
- `projects/score2gp/prompts/next/0015-cr04d4-consolidate-pdf-tab-test-fixtures-wireframe.md`

Prompt 0016 remains inactive. Agy must publish one test-only product PR and
stop for independent review; it must not merge or begin CR-04D5.
