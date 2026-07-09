# Active Task

**Task**: Req-132 / Task 84: Implement consolidated diagnostics and CLI reporting format
**Authorised Role**: Developer
**Repository**: `tticom/score2gp`

## Status
APPROVED

## Task Authorised
Yes

## Completion Evidence
Developer must implement the formatted console print table and consolidated JSON reports inside the diagnostics CLI commands in `cli.py` under Req-132, write tests, pass verification, push the branch, and open a product PR.

## 1. Baseline
- Req-132 consolidated diagnostics schema is designed and approved.
- All candidate metrics, pitch mappings, and timeline previews are available in `run_recognition_on_file`.

## 2. Context
Having approved the display formats, we can now wire the final formatted CLI reports in `score2gp`.

## 3. Goal
Update the CLI commands in `cli.py` to format the console summary tables and output consolidated JSON matching the version 1.0.0 schema.

## 4. Non-goals
- Do not modify core ScoreIR or conversion pipeline.

## 5. Scope
Allowed files:
- `src/score2gp/cli.py`
- `tests/` unit/integration tests for CLI reporting

## 6. Suggested Work Branch
`feature/req-132-diagnostics-implementation-v0.1`

## 7. Required Validation
Run the full verification suite `make verify`.

## 8. Acceptance Criteria
- note-candidate diagnostics CLI commands correctly return the consolidated JSON format when `--json` is enabled.
- note-candidate diagnostics CLI commands output a clean, formatted text table summary showing staves, pitches, and timeline measures when `--json` is false.
- Covered by CLI integration tests.
- No changes to ScoreIR, GP writer/package, or downstream conversion behavior.
- `make verify` passes.

## 9. Next Steps
- Review Req-132 consolidated diagnostics implementation.
