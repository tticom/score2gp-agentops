# 0005 - Review FS-07 CLI Facade Migration

## Objective

Independently review product PR #382 at exact head `bea32ac`. Confirm that all
production CLI recognition calls now use `score2gp.notation_omr.pipeline`
without changing CLI behavior, and that the legacy shim remains available for
external compatibility and characterization tests.

## Start

1. Work only under `/home/tticom/work/score2gp-workspace` in Ubuntu WSL.
2. Confirm GitHub CLI and local Git identity are `tticom-automation`.
3. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, the Reviewer skill, and this
   prompt.
4. Fetch both repositories and check out product PR #382 without modifying it.
5. Verify `git rev-parse HEAD` is exactly
   `bea32ac2a239d6fb67707c2d24bb9770b7be33f9`. Stop if it differs.

## Review Scope

- `src/score2gp/cli.py`
- `tests/test_cli_notation_whole_note_export.py`
- `tests/test_single_note_export_cli_rejection.py`

Confirm:

- all five CLI-local imports of `run_recognition_on_file` use
  `.notation_omr.pipeline`;
- affected mocks target the actual imported facade;
- CLI names, options, output, exit behavior, and recognition arguments did not
  change;
- `whole_note_recogniser.py` remains present and compatibility tests still use
  it deliberately;
- no unrelated source or test changes entered the PR.

## Required Verification

Run:

```bash
.venv/bin/python -m pytest
.venv/bin/python -m score2gp.cli export-schema --out schemas
.venv/bin/python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
.venv/bin/python scripts/artifact_audit.py
git diff --check origin/main...HEAD
git diff --exit-code -- schemas
git ls-files fixtures/private work
git status --short
```

## Publication

Publish an independent GitHub review on PR #382:

- request changes for any behavior, scope, or compatibility defect;
- otherwise approve it and state the exact reviewed head and verification;
- do not modify the product branch;
- do not merge the PR;
- do not start another task.
