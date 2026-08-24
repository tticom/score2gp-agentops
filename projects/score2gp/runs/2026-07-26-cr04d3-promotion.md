# CR-04D3 Promotion

## Trigger

Product PR #387 was externally merged on 2026-07-26.

## Verified Product State

- Product repository: `tticom/score2gp`
- Product merge commit:
  `36b30167ad9719e461a8c6b4a6e49f669faf5f4b`
- Merged D1 module: `src/score2gp/pdf_tab_measure_timing.py`
- Merged D2 module: `src/score2gp/pdf_tab_event_factory.py`
- Remaining per-bar orchestration verified in
  `build_ir_from_tabraw_only()` on product `origin/main`.

## Revalidation Decision

Prompt 0014 remains viable after D2. The extracted assembler can depend on the
duration-policy module, event factory, and chord grouper without importing
`build_ir.py`. Public `BuildIrInputRiskError` remains in `build_ir.py`; an
internal structured exception will carry refusal facts across the new seam and
be translated at the existing public boundary.

The task is limited to one internal module, one focused test file, and the
small integration edit in `build_ir.py`. Timing policy, recognition,
diagnostics, warnings, schemas, CLI behavior, and output formats are frozen.

## Authorisation

This governance change promotes only CR-04D3 through:

- `projects/score2gp/ACTIVE_TASK.md`
- `projects/score2gp/prompts/NEXT.md`
- `projects/score2gp/prompts/next/0014-cr04d3-extract-pdf-tab-bar-assembly-wireframe.md`

Prompts 0015 and 0016 remain inactive. Agy must publish one product PR and
stop for independent review; it must not merge or begin CR-04D4.
