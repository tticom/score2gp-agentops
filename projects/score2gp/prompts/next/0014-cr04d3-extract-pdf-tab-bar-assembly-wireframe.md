# 0014 - CR-04D3 Extract PDF-Only Tab Bar Assembly

## Status

ACTIVE PROMOTED PROMPT — AUTHORISED BY CR-04D REFACTOR SEQUENCE PLAN

## Objective

Extract per-source-bar assembly and orchestration from `build_ir_from_tabraw_only()` in `src/score2gp/build_ir.py` into a dedicated internal assembly module `src/score2gp/pdf_tab_bar_assembly.py`.

## Preconditions

1. CR-04D1 (`pdf_tab_measure_timing.py`) and CR-04D2 (`pdf_tab_event_factory.py`) are merged into product `main` (prerequisite merge SHA `36b3016...` / PR #387).
2. Product `main` passes all tests cleanly (`python -m pytest`, `agent_verify.py`).

## File Allowlist

- `src/score2gp/pdf_tab_bar_assembly.py` [NEW]
- `src/score2gp/build_ir.py` [MODIFY]
- `tests/test_pdf_tab_bar_assembly.py` [NEW]

No other product files or schemas may be modified.

## Directives

1. **Pure Bar Assembler Function**:
   - Create `assemble_pdf_tab_bar()` in `src/score2gp/pdf_tab_bar_assembly.py`.
   - Coordinates subgroup grouping via `PdfOnlyChordEventGrouper`, grid spacing/duration selection via `pdf_tab_measure_timing.py`, capacity validation, event construction via `pdf_tab_event_factory.py`, trailing remainder rests, and `Bar` creation.
   - Accepts bar candidate list, output bar index, chord grouper, canonical `track_id`, `editable_draft`, `tempo_bpm`, and `tempo_is_explicit`.
   - Returns explicit bar result `(Bar, list[Event], list[WarningItem])` or `PdfTabBarAssemblyResult` without mutating caller state.

2. **Integrate into `build_ir.py`**:
   - Update `build_ir_from_tabraw_only()` in `src/score2gp/build_ir.py` to delegate per-bar processing to `assemble_pdf_tab_bar()`.

3. **Strict Non-Circular Imports**:
   - `pdf_tab_bar_assembly.py` imports from `pdf_tab_measure_timing.py`, `pdf_tab_event_factory.py`, `pdf_only_chord_event_grouper.py`, `ir.py`, and `tabraw.py`.
   - `pdf_tab_bar_assembly.py` MUST NOT import `build_ir.py`.
   - `build_ir.py` imports `assemble_pdf_tab_bar` from `pdf_tab_bar_assembly.py`.

4. **Characterization & Equivalence Unit Tests**:
   - Add unit tests in `tests/test_pdf_tab_bar_assembly.py` covering:
     - Empty bar candidate list
     - Single-note bar
     - Multi-note chord bar
     - Sequential events bar
     - Explicit quarter-rest bar
     - Overcapacity refusal bar
     - Trailing remainder rest generation
     - Characterization/equivalence tests against pre-refactor outputs across representative scenarios.

## Acceptance Criteria

1. Pure `assemble_pdf_tab_bar()` function extracted into `src/score2gp/pdf_tab_bar_assembly.py`.
2. `build_ir_from_tabraw_only()` delegates per-bar assembly cleanly to `pdf_tab_bar_assembly.py`.
3. Zero circular imports between `build_ir.py` and `pdf_tab_bar_assembly.py`.
4. Full pytest suite passes (`python -m pytest`).
5. Full `agent_verify.py` passes with `Overall Status: PASS`.
6. One product PR published and stopped for independent review.
