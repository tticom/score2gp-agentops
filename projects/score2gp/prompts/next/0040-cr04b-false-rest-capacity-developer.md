# 0040 - CR-04B: False-Rest Rejection and Per-Voice Measure-Capacity Gate

## Objective

Implement a deterministic per-voice measure-capacity gate and false-rest rejection rule in the `score2gp` pipeline. Ensure that any measure where a voice's duration exceeds the expected capacity (based on the time signature) fails closed and reports the appropriate refusal code rather than silently trimming or reporting success.

## Authorized Product Files

### Source Files
- `src/score2gp/build_ir.py`
- `src/score2gp/report.py`

### Test Files
- `tests/test_cli_convert.py`

No other product files in `src/` or `tests/` may be edited in this task.

## Start

1. Work only in the canonical Ubuntu WSL repositories below `/home/tticom-automation/work/score2gp-workspace`.
2. Prove GitHub CLI and local Git identity are `tticom-automation`.
3. Read `projects/score2gp/AGENT_CONTROL.md`, `projects/score2gp/ACTIVE_TASK.md`, `projects/score2gp/reports/2026-08-06-cr04a-architecture.md`, and product repository `AGENTS.md`.
4. Require clean governance and product worktrees.
5. Create product branch `agy/cr04b-false-rest-capacity-gate` in `tticom/score2gp`.
6. Run `python scripts/agent_verify.py` in `score2gp` before making code modifications.

## Implementation Scope & Seam Contract

Based on the `CR-04A` architecture report:
1. **Expected Measure Duration**:
   Calculate the expected capacity (in divisions/ticks) for each measure. For a time signature $N/D$ and divisions $S$:
   $$\text{Expected Divisions} = \frac{N \times 4 \times S}{D}$$
2. **Voice Duration Tracking**:
   Calculate the accumulated duration for each voice in a measure:
   $$\text{VoiceDuration}(V) = \max_{E_i} (\text{Onset}(E_i) + D(E_i))$$
3. **Capacity Gate & Refusal**:
   - If $\text{VoiceDuration}(V) > \text{Expected Divisions}$, classify as **overfull**.
   - Triggers refusal code: `musicxml_measure_overfull`.
   - If backup/forward cursor movement causes voice overlap with a rest candidate, trigger `musicxml_rest_voice_overlap`.
   - **No Mutation**: Do not trim, delete, or modify the overfull notes/rests. Fail closed and report the refusal code in strict mode.
   - Inject the check inside `src/score2gp/build_ir.py` during `ScoreIR` timeline validation.

## Validation Commands

1. `.venv/bin/python -m pytest tests/test_cli_convert.py`
2. `.venv/bin/python -m pytest`
3. Run `python scripts/agent_verify.py` to confirm passes.

## Non-goals

- Do not implement any key signature, meter, layout, double/final barlines, page breaks, or legato/pull-off/slides/vibrato (embellishment) changes.
