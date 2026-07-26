# CR-04D5 Promotion

## Trigger

Product PR #389 was externally merged on 2026-07-26.

## Verified Product State

- Product repository: `tticom/score2gp`
- Product merge commit:
  `a8250ea8a1b71f8b64081ee6cf6408dd77398509`
- D1 duration-policy merge: `56eddc2` (PR #386)
- D2 event-factory merge: `36b3016` (PR #387)
- D3 bar-assembler merge:
  `cea235d83e72e608b841e5d6d55b631077fa1833` (PR #388)
- D4 test-helper merge:
  `a8250ea8a1b71f8b64081ee6cf6408dd77398509` (PR #389)

## Revalidation Decision

Prompt 0016 remains viable after D4. Revalidation found exactly five obsolete
D1/D2 helper imports and the obsolete `_STRING_TO_BASE_PITCH` constant in
`src/score2gp/build_ir.py`. The extracted modules are the production sources
of truth, and D4's helper remains test-only.

The closure permits only removal of that verified dead residue and a narrow
update to `docs/musicxml-tabraw-build-ir.md`. It freezes production behaviour
and records, rather than fixes, lower-priority naming, constant-sharing, and
test-oracle debt.

## Authorisation

This governance change promotes only CR-04D5 through:

- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/prompts/NEXT.md`
- `projects/score2gp/prompts/next/0016-cr04d5-measure-assembly-compatibility-closure-wireframe.md`

Agy must publish one bounded product PR and stop for independent review. It
must not merge, begin another refactor, or treat the documented next candidate
as authorised work.

## Sequence Boundary

CR-04D5 is the final planned CR-04D loop. Its product PR must pass independent
hard review and maintainer merge before CR-04D can be declared complete.
