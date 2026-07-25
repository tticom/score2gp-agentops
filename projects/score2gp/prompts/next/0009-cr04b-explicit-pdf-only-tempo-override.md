# 0009 - CR-04B Explicit Tempo Override for PDF-Only TabRaw Conversion

## Objective

Implement the smallest public, deterministic way to provide tempo to
PDF-only TabRaw conversion: add a `--tempo-bpm` option to `score2gp convert`
and forward it to the existing `build_ir_from_tabraw_only(..., tempo_bpm=...)`
parameter.

This is a Tier B Developer task. Product implementation is authorised only
within this prompt.

## Start

1. Work only in the canonical Ubuntu WSL repositories below
   `/home/tticom/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, this prompt, the Developer skill,
   product `AGENTS.md`, and
   `tasks/2026-07-25-candidate-task-lesson5-tempo-mismatch.md`.
4. Require clean governance and product worktrees.
5. Fetch both repositories. Use current product `origin/main`, record its full
   SHA, and require it to contain
   `ff9fb4832ef1d4b14ab4b6e369a3c1ceaef9434f`.
6. Run `python scripts/agent_verify.py` before editing. Stop if artifact audit
   fails.
7. Create product branch `agy/cr04b-explicit-pdf-only-tempo-override`.

## Requirement

Add an optional `--tempo-bpm FLOAT` parameter to the `score2gp convert` CLI.

- When `--pdf-only-tab` or `--editable-draft` is active and a valid value is
  supplied, pass it to `build_ir_from_tabraw_only()` and emit that BPM in
  ScoreIR and the generated GP output.
- When the option is omitted, preserve the existing 120 BPM default.
- Reject non-positive or non-finite values with a clear CLI error and no output
  file.
- If `--tempo-bpm` is supplied outside the PDF-only TabRaw paths, refuse it
  rather than silently ignoring it.

## Test-First Acceptance

Add public tests that fail before implementation and prove:

1. `build_ir_from_tabraw_only(..., tempo_bpm=70.0)` emits
   `score.tempo.bpm == 70.0`.
2. Omitting `tempo_bpm` emits `score.tempo.bpm == 120.0`.
3. Non-positive and non-finite builder values raise `BuildIrInputRiskError`.
4. The public CLI conversion path with `--pdf-only-tab --tempo-bpm 70` writes
   `score.ir.json` with tempo 70 and produces the requested GP file.
5. The CLI omitting `--tempo-bpm` preserves tempo 120.
6. The CLI refuses `--tempo-bpm` outside `--pdf-only-tab` /
   `--editable-draft`.

Use tracked public fixtures only. Prefer extending `tests/test_pdf_only_tab.py`
and existing CLI test helpers.

## Approved Implementation Surface

Expected product files:

- `src/score2gp/cli.py`
- `src/score2gp/build_ir.py`
- `tests/test_pdf_only_tab.py`

A narrowly necessary help-text or documentation update is allowed. Stop and
return to governance before changing tempo extraction, notation OMR, MusicXML
import behavior, GP schema, or unrelated conversion code.

## Non-Goals

- Automatic tempo recognition from PDF text, vectors, raster/OCR, or filenames.
- Fixture-specific Lesson-5 logic or coordinates.
- Changes to the 2400-tick final-event duration-padding behavior.
- Changes to MusicXML tempo import or normal sidecar conversion.
- Broad CLI refactoring.
- Private fixtures in tracked tests or committed artifacts.

## Validation

Run:

```bash
python -m pytest tests/test_pdf_only_tab.py
python scripts/agent_verify.py
python -m pytest
python -m score2gp.cli export-schema --out schemas
python -m score2gp.cli validate-ir fixtures/public/tiny_score.ir.json
python scripts/artifact_audit.py
git diff --check
git diff -- schemas
git ls-files fixtures/private work
git status --short
git status --branch
```

The private-safety invariant output from `git ls-files fixtures/private work`
must be exactly `fixtures/private/.gitkeep`.

## Deliverables

1. Commit product code and public tests only on the product task branch.
2. Generate `work/agent_verify.md` and the PR body using
   `scripts/pr_body.py`.
3. Push the product branch and open one product PR in `tticom/score2gp`.
4. Report the branch, PR, full head SHA, test-first evidence, verification
   status, artifact-audit result, changed files, and known limitations.
5. Stop for independent Codex review. Do not merge, enable auto-merge, begin
   the duration-padding task, or perform unrelated governance work.
