# 0011 - CR-04C Final-Event Duration Consistency Implementation

## Objective

Implement the Architecture-approved resolution (Option A with deterministic greedy rest decomposition and over-capacity refusal) for PDF-only TabRaw final-event duration consistency in `build_ir_from_tabraw_only()`.

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

1. **Note Event Durations**: Set every candidate note event's `duration_ticks = grid_spacing` and `notated_duration = NotatedDuration(value=duration_name, dots=0)`.
2. **Over-Capacity Refusal**: If adding candidate notes causes `current_onset + grid_spacing > 3840` ticks (e.g. 5 quarter-grid candidates in `--editable-draft` mode where $5 \times 960 = 4800 > 3840$), raise `BuildIrInputRiskError(category="pdf_only_tab_measure_overcapacity")`.
3. **Deterministic Rest Decomposition**: If $R = 3840 - \text{current\_onset} > 0$ after placing candidate notes, greedily decompose $R$ into un-dotted rest events (`is_rest=True`, `notes=[]`, `confidence=1.0`) using standard un-dotted notated durations in descending order:
   - `whole` (3840 ticks)
   - `half` (1920 ticks)
   - `quarter` (960 ticks)
   - `eighth` (480 ticks)
   - `16th` (240 ticks)
   - `32nd` (120 ticks)
   - `64th` (60 ticks)
4. **Rest Metadata & Onsets**:
   - Assign rest IDs sequentially as `f"bar-{output_bar_idx}-rest-{seq_idx}"` starting from `seq_idx=1` for the first rest in that bar.
   - Rest onsets start at `current_onset` and advance sequentially by each rest's duration.
   - Set `dots = 0` for all generated rest events.
5. **Invariants**:
   - $\sum_{E \in \text{Bar}} E.\text{duration\_ticks} = C_{\text{measure}} = 3840$ ticks for all PDF-only TabRaw bars.
   - For every event $E$, $E.\text{duration\_ticks} == \text{nominal\_ticks}(E.\text{notated\_duration})$.
   - All emitted note and rest events pass ScoreIR validation (`validate-ir`) and GPIF serialization (`validate_gp`).

## Test-First Acceptance

Add public tests that fail before implementation and prove:

1. **$N=4$ Single Rest Test**: 4 eighth notes ($N=4$) converted via `build_ir_from_tabraw_only()` produces 4 note events (`duration_ticks=480`, `notated_duration.value="eighth"`) and 1 rest event (`duration_ticks=1920`, `is_rest=True`, `notated_duration.value="half"`, `id="bar-1-rest-1"`).
2. **$N=3$ Non-Single Duration Remainder Test**: 3 eighth notes ($N=3$, remainder $R=2400$) produces 3 note events and 2 rest events:
   - Rest 1: `onset=1440, duration=1920, notated={"value": "half", "dots": 0}`, `id="bar-1-rest-1"`.
   - Rest 2: `onset=3360, duration=480, notated={"value": "eighth", "dots": 0}`, `id="bar-1-rest-2"`.
3. **$N=1$ Multi-Rest Remainder Test**: 1 eighth note ($N=1$, remainder $R=3360$) produces 1 note event and 3 rest events (`half` 1920 at 480, `quarter` 960 at 2400, `eighth` 480 at 3360).
4. **Over-Capacity Refusal Test**: 5 quarter-grid candidates in `--editable-draft` mode ($4800 > 3840$) raises `BuildIrInputRiskError(category="pdf_only_tab_measure_overcapacity")`.
5. **Package Serialization**: Generated GP packages pass `validate_gp()` with 0 errors.

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
