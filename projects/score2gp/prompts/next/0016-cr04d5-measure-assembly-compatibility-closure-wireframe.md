# 0016 - CR-04D5 PDF-Only Tab Measure-Assembly Compatibility Closure

## Status

ACTIVE — authorised after product PR #389 merged at
`a8250ea8a1b71f8b64081ee6cf6408dd77398509`.

## Objective

Close CR-04D without changing behaviour. Remove only the dead compatibility
residue verified after D1-D4, document the committed PDF-only Tab
measure-assembly boundary, record residual debt, publish one product PR, and
stop.

## Identity and Preconditions

Before editing:

1. Run `/home/tticom-automation/bin/score2gp-identity-check`.
2. Work only in the `tticom-automation` product clone.
3. Fetch `origin`, switch to `main`, fast-forward it, and verify a clean
   worktree.
4. Verify these merged CR-04D commits are ancestors of `main`:
   - D1: `56eddc2` (PR #386)
   - D2: `36b3016` (PR #387)
   - D3: `cea235d83e72e608b841e5d6d55b631077fa1833` (PR #388)
   - D4: `a8250ea8a1b71f8b64081ee6cf6408dd77398509` (PR #389)
5. Run `python scripts/agent_verify.py` before editing and preserve its result.
6. Create branch
   `agy/cr04d5-measure-assembly-compatibility-closure` from current
   `origin/main`.

If a prerequisite fails, stop and report it. Do not repair unrelated state.

## Authorised Product Changes

Only these product files are authorised:

- `src/score2gp/build_ir.py`
- `docs/musicxml-tabraw-build-ir.md`

In `build_ir.py`, remove only:

- the dead import of `build_pdf_tab_event_from_subgroup`;
- the dead import of `determine_pdf_tab_event_duration`;
- the dead import of `decompose_pdf_tab_measure_remainder_to_rests`;
- the dead import of `is_within_pdf_tab_measure_capacity`;
- the dead import of `select_pdf_tab_grid_spacing_and_duration_name`; and
- the dead `_STRING_TO_BASE_PITCH` constant.

Do not make adjacent cleanup merely because it is convenient.

In `docs/musicxml-tabraw-build-ir.md`, add a concise section describing the
committed CR-04D boundary:

- `pdf_tab_measure_timing.py` owns duration/grid/rest-capacity policy;
- `pdf_tab_event_factory.py` owns normalized event construction;
- `pdf_tab_bar_assembler.py` owns one PDF-only Tab bar assembly;
- `build_ir_from_tabraw_only()` owns orchestration and translation of the
  internal `PdfTabBarAssemblerError` into public `BuildIrInputRiskError`;
- `pdf_tab_test_helpers.py` is test-only setup reuse and is not production API.

The same section must record the four merged PRs/commits above, the validation
performed for closure, the residual-debt list below, and one explicitly
unauthorised next candidate.

## Compatibility Review

Before publishing, inspect the D1-D4 diff and current call graph. Confirm:

- imports are acyclic and production code does not import test helpers;
- refusal `category`, `stage`, `message`, and `details` are preserved;
- event/bar ordering, identifiers, durations, rests, diagnostics, warnings,
  CLI reports, ScoreIR output, and GP validation are unchanged;
- extracted helpers have one production source of truth;
- removing the named imports and constant cannot affect runtime behaviour.

If this review reveals a behaviour defect, cycle, leaked test dependency, or
additional required production edit, stop and report it. Do not expand this
task.

## Residual Debt to Record, Not Fix

Record at least:

- `assemble_pdf_tab_bar()` still receives the historically named
  `subgroup_candidates` input;
- the assembler retains a literal 3840-tick initial bar duration rather than
  importing a shared named constant;
- some focused tests retain intentionally fixed, verbose normalized-`Bar`
  oracles.

Name the first remaining refactor candidate, if any, but state clearly that it
is not authorised by this prompt. Do not create or activate another prompt.

## Frozen Behaviour and Prohibited Scope

Do not change:

- recognition, grouping, chord tolerance, or timing policy;
- public APIs, exception payloads, schemas, models, CLI behaviour, diagnostics,
  warnings, ScoreIR, GPIF, writers, or fixture contents;
- implementation or tests outside the two authorised files;
- the assembler parameter name, the 3840 literal, or fixed characterization
  oracles;
- FS-06 or any unrelated cleanup.

No dependency updates, formatting sweep, broad `build_ir.py` cleanup, or
governance-repository edits are authorised from the product branch.

## Required Validation

Run and report:

```bash
python -m pytest \
  tests/test_pdf_tab_measure_timing.py \
  tests/test_pdf_tab_event_factory.py \
  tests/test_pdf_tab_bar_assembler.py \
  tests/test_pdf_only_tab.py \
  tests/test_pdf_only_tab_quarter_rest.py
python -m pytest
python scripts/agent_verify.py
python scripts/artifact_audit.py
git diff --check
git diff --name-only origin/main...HEAD
git status --short
```

Also verify:

```bash
git grep -n \
  -e build_pdf_tab_event_from_subgroup \
  -e determine_pdf_tab_event_duration \
  -e decompose_pdf_tab_measure_remainder_to_rests \
  -e is_within_pdf_tab_measure_capacity \
  -e select_pdf_tab_grid_spacing_and_duration_name \
  -- src/score2gp/build_ir.py
git grep -n _STRING_TO_BASE_PITCH -- src/score2gp/build_ir.py
```

Both grep commands must return no matches. The approved-path check must list
only the two authorised files. Record the exact commands and results in the
product PR.

## Delivery and Stop Condition

Commit and push the branch using `tticom-automation`, then open one product PR
with:

- title: `refactor(pdf-tab): close CR-04D compatibility boundary`
- the exact base/head SHAs;
- changed paths and the compatibility-review result;
- focused/full test and repository-gate results;
- residual debt and the explicitly unauthorised next candidate.

Do not approve or merge the PR. Stop for independent hard review. CR-04D5 and
the CR-04D sequence are not complete until a maintainer merges that PR.
