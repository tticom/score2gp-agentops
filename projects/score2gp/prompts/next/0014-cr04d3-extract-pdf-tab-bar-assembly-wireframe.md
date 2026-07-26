# 0014 - CR-04D3 Extract PDF-Only Tab Bar Assembly (Wireframe)

## Status

INACTIVE WIREFRAME until CR-04D2 is merged, revalidated, and promoted.

## Intended Objective

Extract per-source-bar orchestration from `build_ir_from_tabraw_only()` into an
internal measure assembler using the D1/D2 boundaries.

## Preconditions and Boundary

D1/D2 are merged; call graph and dependency direction are mapped; final prompt
fixes the module/API and allowlist. The assembler may coordinate grouping,
duration selection, event construction, refusal, remainder rests, and `Bar`
construction, returning explicit values rather than mutating global state.

Preserve bar indexes, event order/IDs, diagnostics, warnings, timing, refusal,
empty-bar behaviour, and public interfaces. Do not refactor unrelated phases.

Characterise empty, one-event, chord, sequential, explicit-rest,
mixed-overcapacity, multi-bar, and cross-page cases and compare normalized
ScoreIR before/after.

If recognition policy or schema must change, return to governance. Publish one
PR and stop before CR-04D4.
