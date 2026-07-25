# 0011 - CR-04C Final-Event Duration Consistency Implementation

## Objective

Implement the Architecture-approved resolution (Option A) for PDF-only TabRaw final-event duration consistency in `build_ir_from_tabraw_only()`: set final note `duration_ticks` to `grid_spacing` (matching `notated_duration`), and represent remaining measure capacity $R = 3840 - \text{current\_onset}$ as rest event(s) (`is_rest=True`) with matching `duration_ticks` and valid `notated_duration`.

This is a Tier B Developer task. Product implementation is authorised only within this prompt.

## Start

1. Work only in the canonical Ubuntu WSL repositories below
   `/home/tticom/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `AGENT_CONTROL.md`, `ACTIVE_TASK.md`, this prompt, the Developer skill,
   product `AGENTS.md`, and
   `research/2026-07-25-cr04c-final-event-duration-architecture-decision.md`.
4. Require clean governance and product worktrees.
5. Fetch both repositories. Use current product `origin/main`, record its full
   SHA, and require it to contain merge commit
   `f47194e57b551d4b571a04c0b7641fbe9c173f80`.
6. Run `python scripts/agent_verify.py` before editing. Stop if artifact audit
   fails.
7. Create product branch `agy/cr04c-final-event-duration-consistency-implementation`.

## Requirement

Update `build_ir_from_tabraw_only()` in `src/score2gp/build_ir.py`:

- Every non-rest note event receives `duration_ticks = grid_spacing` and `notated_duration = NotatedDuration(value=duration_name, dots=0)`.
- If `current_onset < 3840` after adding all candidate note subgroups, fill the remaining measure capacity $R = 3840 - \text{current\_onset}$ by appending rest event(s) (`is_rest=True`, `notes=[]`) with `duration_ticks = R` and a matching valid `notated_duration` (e.g. 1920 ticks $\to$ `NotatedDuration(value="half", dots=0)`).
- Enforce the invariant: $\sum_{E \in \text{Bar}} E.\text{duration\_ticks} = C_{\text{measure}} = 3840$ ticks for all PDF-only TabRaw bars.
- Ensure all emitted note and rest events pass ScoreIR validation (`validate-ir`) and GPIF serialization (`validate_gp`).

## Test-First Acceptance

Add public tests that fail before implementation and prove:

1. A 4-candidate TabRaw bar ($N=4$) converted via `build_ir_from_tabraw_only()` produces 4 note events (`duration_ticks=480`, `notated_duration.value="eighth"`) and 1 rest event (`duration_ticks=1920`, `is_rest=True`, `notated_duration.value="half"`).
2. For all events in emitted `score.ir.json`, `duration_ticks` matches nominal ticks of `notated_duration`.
3. Total measure duration equals 3840 ticks ($C_{\text{measure}}$).
4. `score2gp convert --pdf-only-tab ...` and `--editable-draft` succeed and generate valid GP packages that pass `validate_gp()`.

Use tracked public fixtures only. Prefer extending `tests/test_pdf_only_tab.py` and `tests/test_build_ir.py`.

## Approved Implementation Surface

Expected product files:

- `src/score2gp/build_ir.py`
- `tests/test_pdf_only_tab.py`
- `tests/test_build_ir.py`

Stop and return to governance before modifying musicxml import, notation OMR, GP schema, or unrelated conversion code.

## Non-Goals

- Changes to MusicXML sidecar timing alignment or tempo handling.
- Fixture-specific Lesson-5 logic or coordinates.
- Schema redesign or broad CLI refactoring.
- Private fixtures in tracked tests or committed artifacts.

## Validation

Run:

```bash
python -m pytest tests/test_pdf_only_tab.py tests/test_build_ir.py
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
5. Stop for independent Codex review. Do not merge, enable auto-merge, or perform
   unrelated governance work.
