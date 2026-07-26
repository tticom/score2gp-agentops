# CR-04D PDF-Only Tab Measure-Assembly Refactor Sequence

## Status

COMPLETE. CR-04D1 through CR-04D5 were independently reviewed and externally
merged through product PRs #386-#390. The final product merge is
`d70d559152c5aa357a7d2eb38e65b09f288bb08f`.

This is separate from FS-06 notation-OMR modularisation. FS-06 concerns
`whole_note_recogniser.py`; CR-04D concerns PDF-only TabRaw measure assembly in
`build_ir_from_tabraw_only()`.

## Programme Contract

- Preserve observable behaviour established by merged PR #385.
- One ownership boundary and one product PR per step.
- Do not combine refactoring with recognition, timing-policy, schema, CLI, or
  output changes.
- Preserve exceptions, event ordering, IDs, timing, metadata, warnings,
  diagnostics, ScoreIR, and GPIF.
- Use public tests only; commit no private/generated artifacts.
- Each step starts from the merged predecessor and stops at an independently
  reviewable PR.
- Revise a stale wireframe through governance instead of guessing.

## Ordered Steps

1. **CR-04D1 — Extract pure measure-duration policy**
   Move duration selection, capacity checking, and deterministic remainder
   decomposition behind pure functions.
2. **CR-04D2 — Extract event construction**
   Move subgroup-to-note/rest `Event` construction behind an internal boundary.
3. **CR-04D3 — Extract bar assembly**
   Move per-bar orchestration behind an internal measure assembler.
4. **CR-04D4 — Consolidate behavioural fixtures and invariants**
   Reduce duplicated test setup without weakening visible assertions.
5. **CR-04D5 — Compatibility and closure review**
   Review the resulting boundary, document committed reality, and record debt.

## Promotion Rule

Only `projects/score2gp/prompts/NEXT.md` selects executable work. After each
external merge, governance must record the new product SHA, revalidate the next
wireframe, tighten its allowlist/tests, promote exactly that prompt through
`ACTIVE_TASK.md` and `NEXT.md`, and leave later wireframes inactive.

## Completion

The sequence completes only when all five loops are independently reviewed and
externally merged or explicitly human-closed. Passing tests alone do not prove
behaviour preservation; each PR must compare relevant pre/post public behaviour.
